"""Snapshot AlphaFold DB API metadata for the cached human models.

The original human builder cached only mmCIF bytes, so the local filename did not record the AFDB
release. This script records the current API's versioned URL beside the local SHA-256. It does not
claim that an API URL proves the history of a pre-existing byte file; the local hash remains the
authority for the exact coordinates analysed.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
AF = HERE / "cache" / "af"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(acc: str) -> dict:
    path = AF / f"{acc}.cif"
    response = requests.get(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}", timeout=90)
    payload = response.json() if response.status_code == 200 else []
    exact = [item for item in payload if item.get("uniprotAccession") == acc]
    item = exact[0] if len(exact) == 1 else {}
    return {
        "accession": acc,
        "api_status": response.status_code,
        "exact_canonical_entry": len(exact) == 1,
        "latest_version": item.get("latestVersion"),
        "is_complex": item.get("isComplex"),
        "cif_url": item.get("cifUrl", ""),
        "entry_id": item.get("entryId", ""),
        "sequence_start": item.get("sequenceStart"),
        "sequence_end": item.get("sequenceEnd"),
        "model_sequence": item.get("sequence", ""),
        "model_sequence_checksum": item.get("sequenceChecksum", ""),
        "local_present": path.exists(),
        "local_bytes": path.stat().st_size if path.exists() else 0,
        "local_sha256": sha256(path) if path.exists() else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", default=HERE / "kennedy2024_cohort_candidate.rebuilt.csv")
    ap.add_argument("--out", default=HERE / "cache" / "af_v6_manifest.csv")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()

    accessions = sorted(pd.read_csv(args.candidate).acc.astype(str).unique())
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(fetch, accessions))
    frame = pd.DataFrame(rows).sort_values("accession")
    frame.to_csv(args.out, index=False)

    cached = frame[frame.local_present]
    bad = cached[
        (cached.api_status != 200)
        | ~cached.exact_canonical_entry
        | (pd.to_numeric(cached.latest_version, errors="coerce") != 6)
        | (cached.is_complex != False)  # noqa: E712
        | ~cached.cif_url.str.endswith("model_v6.cif")
    ]
    print(f"wrote {Path(args.out).name}: {len(frame)} accessions, {len(cached)} cached models")
    if len(bad):
        print(f"ERROR: {len(bad)} cached models lack current v6 monomer metadata")
        return 1
    print("all cached models map to exact canonical AFDB v6 monomer entries; local hashes recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
