"""Replace wrong-isoform AlphaFold cache entries with exact canonical v6 models.

The original downloader took the first API result. For accessions with isoform results, that can be a
different sequence. This repair keeps each displaced file under `cache/af_superseded_wrong_isoform/`,
installs an already-downloaded exact canonical entry when one exists, and removes the active cache
entry when AFDB has no exact canonical model. API metadata and replacement files are read from
`/private/tmp`; this makes the repair itself deterministic and offline.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from Bio.Data.IUPACData import protein_letters_3to1_extended as three_to_one
from Bio.PDB import MMCIFParser

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
AF = CACHE / "af"
BACKUP = CACHE / "af_superseded_wrong_isoform"
REPAIR_ACCESSIONS = [
    "O43149", "Q8TD26", "O94854", "Q63HN8", "Q96EY9", "Q5T4S7", "Q14669",
    "P24928", "O75962", "Q9Y4D8", "Q9P2D1",
]


def model_sequence(path: Path) -> str:
    structure = MMCIFParser(QUIET=True).get_structure(path.stem, path)
    residues = {}
    for residue in structure[0].get_residues():
        if residue.id[0] != " ":
            continue
        try:
            residues[residue.id[1]] = three_to_one[residue.get_resname().capitalize()]
        except KeyError:
            continue
    positions = sorted(residues)
    if positions != list(range(1, len(positions) + 1)):
        raise RuntimeError(f"non-contiguous model numbering: {path.name}")
    return "".join(residues[p] for p in positions)


def main() -> int:
    BACKUP.mkdir(exist_ok=True)
    repaired = removed = 0
    for acc in REPAIR_ACCESSIONS:
        payload = json.loads(Path(f"/private/tmp/afmeta_{acc}.json").read_text())
        exact = [item for item in payload if item.get("uniprotAccession") == acc]
        if len(exact) > 1:
            raise RuntimeError(f"multiple exact canonical AFDB entries for {acc}")
        path = AF / f"{acc}.cif"
        if not path.exists():
            raise FileNotFoundError(f"expected wrong active cache entry is missing: {acc}")
        backup = BACKUP / path.name
        if not backup.exists():
            shutil.move(path, backup)
        else:
            path.unlink()
        if not exact:
            removed += 1
            print(f"removed {acc}: AFDB API has no exact canonical entry")
            continue
        item = exact[0]
        expected = item["sequence"]
        tmp = Path(f"/private/tmp/afmodel_{acc}.cif")
        if not tmp.exists():
            raise FileNotFoundError(f"downloaded canonical replacement is missing: {acc}")
        if model_sequence(tmp) != expected:
            raise RuntimeError(f"downloaded canonical model sequence mismatch: {acc}")
        shutil.copy2(tmp, path)
        repaired += 1
        print(f"repaired {acc}: exact canonical v6 model")
    print(f"repaired {repaired}; removed {removed}; backups retained in {BACKUP.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
