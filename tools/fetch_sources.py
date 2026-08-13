"""Retrieve the four required Viéitez workbooks and fail on changed inner files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOCK_PATH = ROOT / "sources.lock.json"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with temporary.open("wb") as handle:
            for block in response.iter_content(chunk_size=1024 * 1024):
                if block:
                    handle.write(block)
    os.replace(temporary, destination)


def verify_existing(required: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    mismatched: list[str] = []
    for item in required:
        path = DATA / item["name"]
        if not path.is_file():
            missing.append(item["name"])
        elif sha256_file(path) != item["sha256"]:
            mismatched.append(item["name"])
    return missing, mismatched


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--archive",
        type=Path,
        help="Use an already downloaded Europe PMC supplementary ZIP.",
    )
    args = parser.parse_args()

    lock = json.loads(LOCK_PATH.read_text())
    archive_contract = lock["supplementary_archive"]
    required = archive_contract["required_files"]
    DATA.mkdir(parents=True, exist_ok=True)

    missing, mismatched = verify_existing(required)
    if mismatched:
        raise SystemExit(
            "refusing to overwrite source workbooks with unexpected hashes: "
            + ", ".join(mismatched)
        )
    if not missing:
        print(f"source verification PASS: {len(required)} required workbooks already match")
        return

    archive = args.archive.resolve() if args.archive else DATA / "PMC7612524_supplementary.zip"
    if not archive.is_file():
        if args.archive:
            raise SystemExit(f"archive not found: {archive}")
        print(f"retrieving {archive_contract['url']}")
        download(archive_contract["url"], archive)

    observed_archive_hash = sha256_file(archive)
    if observed_archive_hash != archive_contract["observed_sha256"]:
        print(
            "warning: supplementary ZIP container hash changed; required inner files "
            "must still match exactly",
            file=sys.stderr,
        )

    with zipfile.ZipFile(archive) as bundle:
        members = {Path(name).name: name for name in bundle.namelist()}
        staged: list[tuple[Path, bytes]] = []
        for item in required:
            name = item["name"]
            if name not in members:
                raise SystemExit(f"required workbook absent from supplementary archive: {name}")
            payload = bundle.read(members[name])
            observed = sha256_bytes(payload)
            if observed != item["sha256"]:
                raise SystemExit(
                    f"required workbook hash mismatch for {name}: {observed}"
                )
            staged.append((DATA / name, payload))

    for destination, payload in staged:
        temporary = destination.with_suffix(destination.suffix + ".part")
        temporary.write_bytes(payload)
        os.replace(temporary, destination)

    missing, mismatched = verify_existing(required)
    if missing or mismatched:
        raise SystemExit(
            f"post-extraction source verification failed; missing={missing}, mismatched={mismatched}"
        )
    print(
        f"source verification PASS: {len(required)} workbooks; "
        f"archive sha256={observed_archive_hash}"
    )


if __name__ == "__main__":
    main()
