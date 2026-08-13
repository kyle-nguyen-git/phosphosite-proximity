"""Fail-closed verification of redistributed UniProt and AlphaFold input caches."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser
from Bio.PDB.Polypeptide import protein_letters_3to1


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release_metadata" / "third_party_data_manifest.csv"
REPORT = ROOT / "release_metadata" / "cache_verification_report.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def structure_sequence(path: Path) -> tuple[str, list[int]]:
    structure = MMCIFParser(QUIET=True).get_structure(path.stem, str(path))
    letters: list[str] = []
    positions: list[int] = []
    for residue in structure[0].get_residues():
        if residue.id[0] != " ":
            continue
        try:
            letter = protein_letters_3to1[residue.get_resname()]
        except KeyError as error:
            raise RuntimeError(f"unexpected residue {residue.get_resname()} in {path}") from error
        positions.append(int(residue.id[1]))
        letters.append(letter)
    return "".join(letters), positions


def main() -> None:
    rows = list(csv.DictReader(MANIFEST.open()))
    file_checks: dict[str, bool] = {}
    for item in rows:
        path = ROOT / item["path"]
        file_checks[item["path"]] = (
            path.is_file()
            and path.stat().st_size == int(item["bytes"])
            and sha256(path) == item["sha256"]
        )
    if not all(file_checks.values()):
        failed = [path for path, passed in file_checks.items() if not passed]
        raise SystemExit("third-party cache hash failure: " + ", ".join(failed))

    expected_paths = {
        "data/yeast_sgd_uniprot.tsv",
        "data/uniprot_entries_raw.json",
        *{
            str(path.relative_to(ROOT))
            for path in (ROOT / "data" / "af").glob("*.cif")
        },
        *{
            str(path.relative_to(ROOT))
            for path in (ROOT / "phase0_5" / "data" / "pae").glob("*")
            if path.is_file()
        },
    }
    manifested_paths = {item["path"] for item in rows}
    if expected_paths != manifested_paths:
        missing = sorted(expected_paths - manifested_paths)
        extra = sorted(manifested_paths - expected_paths)
        raise SystemExit(f"cache manifest coverage failure; missing={missing}, extra={extra}")

    proteome = pd.read_csv(ROOT / "data" / "yeast_sgd_uniprot.tsv", sep="\t")
    proteome.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "length"]
    sequences = dict(zip(proteome.acc.astype(str), proteome.seq.astype(str)))
    parser_checks: dict[str, dict[str, bool | int]] = {}
    metadata_paths = sorted((ROOT / "phase0_5" / "data" / "pae").glob("*_metadata.json"))
    for metadata_path in metadata_paths:
        metadata = json.loads(metadata_path.read_text())
        acc = metadata["uniprotAccession"]
        sequence = str(metadata["sequence"])
        cif_path = ROOT / "data" / "af" / f"{acc}.cif"
        cif_sequence, positions = structure_sequence(cif_path)
        pae_path = metadata_path.with_name(f"{acc}_v6_pae.json.gz")
        with gzip.open(pae_path, "rt") as handle:
            pae_document = json.load(handle)
        payload = pae_document[0] if isinstance(pae_document, list) else pae_document
        pae = np.asarray(payload["predicted_aligned_error"], dtype=float)
        checks = {
            "version_is_6": int(metadata["latestVersion"]) == 6,
            "is_monomer": not bool(metadata.get("isComplex")),
            "versioned_cif_url": bool(re.search(r"model_v6\.cif$", metadata["cifUrl"])),
            "versioned_pae_url": bool(re.search(r"error_v6\.json$", metadata["paeDocUrl"])),
            "metadata_bounds_cover_sequence": (
                int(metadata["sequenceStart"]) == 1
                and int(metadata["sequenceEnd"]) == len(sequence)
                and int(metadata["uniprotStart"]) == 1
                and int(metadata["uniprotEnd"]) == len(sequence)
            ),
            "metadata_sequences_agree": str(metadata.get("uniprotSequence")) == sequence,
            "uniprot_sequence_agrees": sequences.get(acc) == sequence,
            "cif_sequence_agrees": cif_sequence == sequence,
            "cif_numbering_contiguous": positions == list(range(1, len(sequence) + 1)),
            "pae_dimensions_agree": pae.shape == (len(sequence), len(sequence)),
        }
        if not all(bool(value) for value in checks.values()):
            failed = [name for name, passed in checks.items() if not passed]
            raise SystemExit(f"AlphaFold sequence/provenance failure for {acc}: {failed}")
        parser_checks[acc] = {**checks, "sequence_length": len(sequence)}

    report = {
        "status": "PASS",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "manifest_file_count": len(rows),
        "alphafold_accessions": len(parser_checks),
        "all_file_hashes_match": all(file_checks.values()),
        "all_sequences_versions_and_pae_dimensions_match": True,
        "per_accession": parser_checks,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"third-party cache verification PASS: {len(rows)} files, "
        f"{len(parser_checks)} AlphaFold accessions"
    )


if __name__ == "__main__":
    main()
