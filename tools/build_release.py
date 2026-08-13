"""Build a deterministic, source-rights-aware release-candidate archive."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from pathlib import Path

from release_policy import release_source_files, sha256, source_tree_fingerprint


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
BUILD = RELEASE / "build"
DIST = RELEASE / "dist"
CANDIDATE_NAME = "phase0-calibration-v0.5.0-rc1"
REPORT = RELEASE / "package_build_report.json"


def write_internal_manifests(candidate: Path, source_fingerprint: str) -> None:
    (candidate / "PACKAGE_METADATA.json").write_text(json.dumps({
        "schema_version": 1,
        "candidate_name": CANDIDATE_NAME,
        "source_tree_fingerprint_excluding_generated_outputs": source_fingerprint,
        "source_workbooks_redistributed": False,
    }, indent=2) + "\n")
    files = sorted(path for path in candidate.rglob("*") if path.is_file())
    rows = [
        {
            "path": path.relative_to(candidate).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in files
    ]
    manifest = candidate / "PACKAGE_MANIFEST.csv"
    with manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    checksum_files = sorted(
        path for path in candidate.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (candidate / "SHA256SUMS").write_text("".join(
        f"{sha256(path)}  {path.relative_to(candidate).as_posix()}\n"
        for path in checksum_files
    ))


def deterministic_archive(candidate: Path, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".building")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                paths = [candidate, *sorted(candidate.rglob("*"))]
                for path in paths:
                    relative = Path(CANDIDATE_NAME) / path.relative_to(candidate)
                    info = archive.gettarinfo(str(path), arcname=relative.as_posix())
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    if info.isfile():
                        with path.open("rb") as handle:
                            archive.addfile(info, handle)
                    else:
                        archive.addfile(info)
    os.replace(temporary, destination)


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    source_files = release_source_files(ROOT)
    fingerprint = source_tree_fingerprint(ROOT, source_files)
    with tempfile.TemporaryDirectory(prefix="release-stage-", dir=BUILD) as temporary:
        staged = Path(temporary) / CANDIDATE_NAME
        staged.mkdir()
        for source in source_files:
            relative = source.relative_to(ROOT)
            destination = staged / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        write_internal_manifests(staged, fingerprint)

        destination = BUILD / CANDIDATE_NAME
        if destination.exists():
            if destination.parent != BUILD or destination.name != CANDIDATE_NAME:
                raise RuntimeError(f"refusing to replace unexpected path: {destination}")
            shutil.rmtree(destination)
        shutil.copytree(staged, destination)

    archive = DIST / f"{CANDIDATE_NAME}.tar.gz"
    deterministic_archive(BUILD / CANDIDATE_NAME, archive)
    report = {
        "status": "PASS",
        "candidate_name": CANDIDATE_NAME,
        "source_tree_fingerprint_excluding_runtime_reports": fingerprint,
        "copied_source_files": len(source_files),
        "candidate_files": sum(1 for path in (BUILD / CANDIDATE_NAME).rglob("*") if path.is_file()),
        "archive": str(archive.relative_to(ROOT)),
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256(archive),
        "source_workbooks_redistributed": False,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"built {archive.relative_to(ROOT)}; sha256={report['archive_sha256']}; "
        f"source files={report['copied_source_files']}"
    )


if __name__ == "__main__":
    main()
