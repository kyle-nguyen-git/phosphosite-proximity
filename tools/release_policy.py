"""Shared inclusion policy for the public release candidate."""

from __future__ import annotations

import hashlib
from pathlib import Path


EXCLUDED_DIRECTORY_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
}
EXCLUDED_EXACT_PATHS = {
    "release/clean_room_report.json",
    "release/package_build_report.json",
    "release/release_readiness_report.json",
    "tools/internal_workbook_qa.mjs",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_source_workbook(relative: Path) -> bool:
    return (
        len(relative.parts) == 2
        and relative.parts[0] == "data"
        and relative.name.startswith("EMS132528-supplement-Supplementary_Data_")
        and relative.suffix.lower() == ".xlsx"
    )


def is_release_source(path: Path, root: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    relative = path.relative_to(root)
    relative_text = relative.as_posix()
    if any(part in EXCLUDED_DIRECTORY_PARTS for part in relative.parts):
        return False
    if relative.parts[:2] in {("release", "build"), ("release", "dist")}:
        return False
    if relative.parts[:2] == ("phase0_5", "verification"):
        return False
    if relative_text in EXCLUDED_EXACT_PATHS:
        return False
    if path.suffix.lower() == ".pyc" or path.name.endswith(".inspect.ndjson"):
        return False
    if path.name in {".DS_Store", "PMC7612524_supplementary.zip"}:
        return False
    if is_source_workbook(relative):
        return False
    if relative_text == "data/EMS132528-supplement-Supplementary_Information.pdf":
        return False
    return True


def release_source_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if is_release_source(path, root))


def source_tree_fingerprint(root: Path, files: list[Path] | None = None) -> str:
    """Hash release inputs while excluding self-referential clean-room evidence."""
    selected = files if files is not None else release_source_files(root)
    digest = hashlib.sha256()
    for path in selected:
        relative = path.relative_to(root).as_posix()
        if (
            relative.startswith("results/")
            or relative.startswith("phase0_5/results/")
            or relative.startswith("manuscript/rendered/")
            or relative in {
                "manuscript/preprint_draft_v1.pdf",
                "manuscript/figure1_cohort_estimand_primary.pdf",
                "manuscript/figure1_cohort_estimand_primary.png",
                "release_metadata/cache_verification_report.json",
            }
        ):
            continue
        if relative in {
            "release/clean_room_report.json",
            "phase0_5/results/release_manifest.csv",
            "phase0_5/results/verification_report.json",
            "release/release_readiness_report.json",
            "PACKAGE_METADATA.json",
            "PACKAGE_MANIFEST.csv",
            "SHA256SUMS",
        }:
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()
