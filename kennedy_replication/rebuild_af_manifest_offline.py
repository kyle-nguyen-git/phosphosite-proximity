"""Rebuild the AFDB v6 provenance manifest after the wrong-isoform cache repair."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd
from Bio.Data.IUPACData import protein_letters_3to1_extended as three_to_one
from Bio.PDB import MMCIFParser

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
AF = CACHE / "af"
MANIFEST = CACHE / "af_v6_manifest.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect(path: Path) -> tuple[str, str]:
    text = path.read_text(errors="replace", encoding="utf-8")
    match = re.search(r"^_entry\.id\s+(\S+)", text, re.M)
    entry_id = match.group(1) if match else ""
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
    return entry_id, "".join(residues[p] for p in positions)


def main() -> int:
    old = pd.read_csv(MANIFEST).set_index("accession")
    accessions = sorted(pd.read_csv(HERE / "kennedy2024_cohort_candidate.rebuilt.csv").acc.unique())
    overrides = {}
    for path in Path("/private/tmp").glob("afmeta_*.json"):
        acc = path.stem.removeprefix("afmeta_")
        payload = json.loads(path.read_text())
        exact = [item for item in payload if item.get("uniprotAccession") == acc]
        overrides[acc] = exact[0] if len(exact) == 1 else None

    rows = []
    for acc in accessions:
        path = AF / f"{acc}.cif"
        item = overrides.get(acc, "not-queried")
        prior = old.loc[acc] if acc in old.index else None
        if item == "not-queried":
            version = int(prior.latest_version) if prior is not None and pd.notna(prior.latest_version) else None
            is_complex = bool(prior.is_complex) if prior is not None else None
            cif_url = str(prior.cif_url) if prior is not None else ""
        elif item is None:
            version, is_complex, cif_url = None, None, ""
        else:
            version = item.get("latestVersion")
            is_complex = item.get("isComplex")
            cif_url = item.get("cifUrl", "")

        entry_id = model_seq = ""
        if path.exists():
            entry_id, model_seq = inspect(path)
        exact_entry = bool(path.exists() and entry_id == f"AF-{acc}-F1")
        rows.append({
            "accession": acc,
            "api_status": 200 if version is not None else 404,
            "exact_canonical_entry": exact_entry,
            "latest_version": version,
            "is_complex": is_complex,
            "cif_url": cif_url,
            "entry_id": entry_id,
            "sequence_start": 1 if model_seq else None,
            "sequence_end": len(model_seq) if model_seq else None,
            "model_sequence": model_seq,
            "local_present": path.exists(),
            "local_bytes": path.stat().st_size if path.exists() else 0,
            "local_sha256": sha256(path) if path.exists() else "",
        })
    frame = pd.DataFrame(rows)
    cached = frame[frame.local_present]
    bad = cached[
        ~cached.exact_canonical_entry
        | (pd.to_numeric(cached.latest_version, errors="coerce") != 6)
        | (cached.is_complex != False)  # noqa: E712
        | ~cached.cif_url.str.endswith("model_v6.cif")
    ]
    if len(bad):
        print(bad[["accession", "entry_id", "latest_version", "cif_url"]].to_string(index=False))
        raise SystemExit(f"{len(bad)} active cache entries fail exact-canonical v6 checks")
    frame.to_csv(MANIFEST, index=False)
    print(f"wrote {MANIFEST.name}: {len(frame)} accessions, {len(cached)} exact canonical v6 models")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
