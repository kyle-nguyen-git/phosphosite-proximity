"""Reproduce the release in a fresh virtual environment and record the evidence."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from release_policy import sha256, source_tree_fingerprint


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "release" / "clean_room_report.json"
ARTIFACTS = [
    "manuscript/preprint_draft_v1.pdf",
    "manuscript/figure1_cohort_estimand_primary.png",
    "manuscript/figure1.png",
    "manuscript/figure2.png",
    "manuscript/figure1.pdf",
    "manuscript/figure2.pdf",
    "robustness/results/robustness_supplement.xlsx",
    "robustness/results/robustness_two_arm_robustness_summary.png",
]


def run_logged(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> tuple[int, str]:
    print("$ " + " ".join(command), flush=True)
    process = subprocess.Popen(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    lines: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
        lines.append(line)
    return process.wait(), "".join(lines)


def parse_frozen(root: Path) -> dict[str, str]:
    return dict(re.findall(
        r"^- `([^`]+)` — `([0-9a-f]{64})`$",
        (root / "NUMBERS.md").read_text(),
        re.MULTILINE,
    ))


def safe_extract(archive_path: Path, destination: Path) -> Path:
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        if any(
            member.name.startswith("/") or ".." in Path(member.name).parts
            or member.issym() or member.islnk()
            for member in members
        ):
            raise RuntimeError("release archive contains an unsafe member")
        roots = {Path(member.name).parts[0] for member in members if member.name}
        if len(roots) != 1:
            raise RuntimeError("release archive does not contain one top-level directory")
        archive.extractall(destination, filter="data")
    return destination / next(iter(roots))


def main() -> None:
    if sys.version_info[:3] != (3, 12, 4):
        raise SystemExit(
            "clean-room base interpreter must be CPython 3.12.4; "
            f"found {sys.version.split()[0]}"
        )
    started = datetime.now(timezone.utc).isoformat()
    build_code, build_log = run_logged([sys.executable, "tools/build_release.py"], ROOT)
    if build_code:
        raise SystemExit("release package build failed")
    package = json.loads((ROOT / "release" / "package_build_report.json").read_text())
    archive = ROOT / package["archive"]

    with tempfile.TemporaryDirectory(prefix="phase0-clean-room-") as temporary_text:
        temporary = Path(temporary_text)
        candidate = safe_extract(archive, temporary / "candidate")
        expected = parse_frozen(candidate)
        before_artifacts = {
            relative: sha256(candidate / relative) for relative in ARTIFACTS
        }
        venv = temporary / "venv"
        create_code, create_log = run_logged([sys.executable, "-m", "venv", str(venv)], temporary)
        if create_code:
            raise SystemExit("clean-room virtual environment creation failed")
        python = venv / "bin" / "python"
        install_code, install_log = run_logged(
            [str(python), "-m", "pip", "install", "-r", "requirements-lock.txt"],
            candidate,
        )
        if install_code:
            raise SystemExit("clean-room dependency installation failed")
        environment = os.environ.copy()
        environment["PYTHON_BIN"] = str(python)
        environment["MPLCONFIGDIR"] = str(temporary / "matplotlib")
        run_code, reproduction_log = run_logged(["bash", "./reproduce.sh"], candidate, environment)

        observed = {
            relative: sha256(candidate / relative) for relative in expected
            if (candidate / relative).is_file()
        }
        freeze_checks = {
            relative: observed.get(relative) == expected_hash
            for relative, expected_hash in expected.items()
        }
        after_artifacts = {
            relative: sha256(candidate / relative) for relative in ARTIFACTS
        }
        artifact_checks = {
            relative: before_artifacts[relative] == after_artifacts[relative]
            for relative in ARTIFACTS
        }
        scientific = json.loads(
            (candidate / "robustness" / "results" / "verification_report.json").read_text()
        )
        technical = json.loads(
            (candidate / "release" / "release_readiness_report.json").read_text()
        )
        freeze_code, freeze_output = run_logged([str(python), "-m", "pip", "freeze"], candidate)
        pdftoppm = shutil.which("pdftoppm")
        renderer = subprocess.run(
            [pdftoppm, "-v"] if pdftoppm else ["true"],
            capture_output=True,
            text=True,
        )
        candidate_fingerprint = source_tree_fingerprint(candidate)

    passed = (
        run_code == 0
        and all(freeze_checks.values())
        and all(artifact_checks.values())
        and scientific.get("status") == "PASS"
        and technical.get("status") == "PASS"
        and freeze_code == 0
        and candidate_fingerprint
        == package["source_tree_fingerprint_excluding_runtime_reports"]
    )
    report = {
        "status": "PASS" if passed else "FAIL",
        "scope": "same-author clean-room technical reproduction; not independent replication",
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "host": {
            "platform": platform.platform(),
            "base_python": sys.version,
        },
        "tested_archive": {
            "path": package["archive"],
            "sha256": sha256(archive),
            "source_tree_fingerprint_excluding_runtime_reports": package[
                "source_tree_fingerprint_excluding_runtime_reports"
            ],
            "extracted_tree_fingerprint_after_run": candidate_fingerprint,
        },
        "fresh_environment": {
            "created_with": sys.executable,
            "requirements_lock_sha256": sha256(ROOT / "requirements-lock.txt"),
            "pip_freeze": freeze_output.splitlines(),
            "pdftoppm": (renderer.stderr or renderer.stdout).strip(),
        },
        "checks": {
            "reproduction_command_exit_zero": run_code == 0,
            "frozen_hashes_match_numbers": all(freeze_checks.values()),
            "generated_artifacts_are_byte_stable": all(artifact_checks.values()),
            "scientific_verifier_passes": scientific.get("status") == "PASS",
            "technical_verifier_passes": technical.get("status") == "PASS",
            "release_source_tree_is_byte_stable": (
                candidate_fingerprint
                == package["source_tree_fingerprint_excluding_runtime_reports"]
            ),
        },
        "freeze_hash_checks": freeze_checks,
        "artifact_hash_checks": artifact_checks,
        "artifact_hashes": {
            relative: {
                "before": before_artifacts[relative],
                "after": after_artifacts[relative],
                "match": artifact_checks[relative],
            }
            for relative in ARTIFACTS
        },
        "commands": {
            "package_build": build_log,
            "venv_create": create_log,
            "dependency_install": install_log,
            "reproduction": reproduction_log,
        },
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    if not passed:
        raise SystemExit("clean-room reproduction failed; see release/clean_room_report.json")
    print("clean-room reproduction PASS; frozen hashes and generated artifacts match")


if __name__ == "__main__":
    main()
