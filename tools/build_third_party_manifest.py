"""Write the file-level UniProt and AlphaFold redistribution manifest."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release_metadata" / "third_party_data_manifest.csv"
AF_LICENSE = "https://alphafold.ebi.ac.uk/assets/License-Disclaimer.pdf"
UNIPROT_LICENSE = "https://www.uniprot.org/help/license"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def row(
    path: Path,
    source: str,
    source_url: str,
    source_version: str,
    license_name: str,
    license_url: str,
    transformation: str,
) -> dict[str, str | int]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "source": source,
        "source_url": source_url,
        "source_version": source_version,
        "license": license_name,
        "license_url": license_url,
        "transformation": transformation,
    }


def main() -> None:
    rows: list[dict[str, str | int]] = []
    raw_uniprot = ROOT / "data" / "uniprot_entries_raw.json"
    uniprot_document = json.loads(raw_uniprot.read_text())
    release = ";".join(uniprot_document.get("uniprot_release", []))
    rows.append(
        row(
            ROOT / "data" / "yeast_sgd_uniprot.tsv",
            "UniProtKB reviewed Saccharomyces cerevisiae proteome",
            "https://rest.uniprot.org/uniprotkb/stream",
            release,
            "CC BY 4.0",
            UNIPROT_LICENSE,
            "REST query serialized as TSV",
        )
    )
    rows.append(
        row(
            raw_uniprot,
            "UniProtKB feature records",
            "https://rest.uniprot.org/uniprotkb/search",
            release,
            "CC BY 4.0",
            UNIPROT_LICENSE,
            "batched REST responses preserved as JSON",
        )
    )

    metadata_paths = sorted((ROOT / "phase0_5" / "data" / "pae").glob("*_metadata.json"))
    if not metadata_paths:
        raise SystemExit("no AlphaFold metadata cache found")
    for metadata_path in metadata_paths:
        metadata = json.loads(metadata_path.read_text())
        acc = metadata["uniprotAccession"]
        version = int(metadata["latestVersion"])
        if version != 6 or metadata.get("isComplex"):
            raise SystemExit(f"unexpected AlphaFold model contract for {acc}")
        cif_path = ROOT / "data" / "af" / f"{acc}.cif"
        pae_path = metadata_path.with_name(f"{acc}_v{version}_pae.json.gz")
        if not cif_path.is_file() or not pae_path.is_file():
            raise SystemExit(f"incomplete AlphaFold cache for {acc}")
        if f"model_v{version}.cif" not in metadata["cifUrl"]:
            raise SystemExit(f"unversioned AlphaFold CIF URL for {acc}")
        if f"error_v{version}.json" not in metadata["paeDocUrl"]:
            raise SystemExit(f"unversioned AlphaFold PAE URL for {acc}")
        rows.extend(
            [
                row(
                    cif_path,
                    "AlphaFold Protein Structure Database monomer model",
                    metadata["cifUrl"],
                    f"v{version}",
                    "CC BY 4.0",
                    AF_LICENSE,
                    "none",
                ),
                row(
                    metadata_path,
                    "AlphaFold Protein Structure Database API metadata",
                    f"https://alphafold.ebi.ac.uk/api/prediction/{acc}",
                    f"v{version}",
                    "CC BY 4.0",
                    AF_LICENSE,
                    "first API record serialized as indented JSON",
                ),
                row(
                    pae_path,
                    "AlphaFold Protein Structure Database predicted aligned error",
                    metadata["paeDocUrl"],
                    f"v{version}",
                    "CC BY 4.0",
                    AF_LICENSE,
                    "source JSON serialized compactly and gzip-compressed",
                ),
            ]
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "path",
        "bytes",
        "sha256",
        "source",
        "source_url",
        "source_version",
        "license",
        "license_url",
        "transformation",
    ]
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda item: str(item["path"])))
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(rows)} files")


if __name__ == "__main__":
    main()
