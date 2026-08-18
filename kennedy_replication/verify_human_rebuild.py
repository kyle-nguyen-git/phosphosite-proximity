"""Fail-closed verification of the Kennedy source-to-cohort build and its pinned inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
MANIFEST = HERE / "human_rebuild_manifest.json"
CURRENT_CANDIDATE = HERE / "kennedy2024_cohort_candidate.rebuilt.csv"
CURRENT_ANALYSIS = HERE / "kennedy_analysis_corrected.csv"
AF_MANIFEST = CACHE / "af_v6_manifest.csv"

PINNED = [
    CACHE / "kennedy_supplement.xlsx",
    CACHE / "screens_parsed.csv",
    CACHE / "gs_SuppTable_3_MAGeCK_gene_summary.csv",
    CACHE / "gs_SuppTable4_MAGeCK_gene_summary.csv",
    CACHE / "genemap.json",
    CURRENT_CANDIDATE,
    CURRENT_ANALYSIS,
    HERE / "build_candidate_table.py",
    HERE / "build_cohort.py",
    HERE / "rebuild_endpoints.py",
    HERE / "endpoint_options.py",
    HERE / "endpoint_options_source_corrected.json",
    AF_MANIFEST,
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_digest(directory: Path, suffix: str) -> tuple[int, str]:
    h = hashlib.sha256()
    files = sorted(directory.glob(f"*{suffix}"))
    for path in files:
        h.update(path.name.encode())
        h.update(b"\0")
        h.update(sha256(path).encode())
        h.update(b"\n")
    return len(files), h.hexdigest()


def compare_csv(expected: Path, observed: Path) -> None:
    left = pd.read_csv(expected)
    right = pd.read_csv(observed)
    assert_frame_equal(left, right, check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-12)


def run_offline_rebuild(update_current_analysis: bool = False) -> dict:
    with tempfile.TemporaryDirectory(prefix="kennedy_offline_") as td:
        tmp = Path(td)
        candidate = tmp / "candidate.csv"
        analysis = tmp / "analysis.csv"
        targets = tmp / "targets.csv"
        subprocess.run([sys.executable, str(HERE / "build_candidate_table.py"), "--offline",
                        "--out", str(candidate)], check=True)
        compare_csv(CURRENT_CANDIDATE, candidate)
        subprocess.run([sys.executable, str(HERE / "build_cohort.py"), "--offline",
                        "--cohort", str(candidate), "--out", str(analysis),
                        "--targets-out", str(targets)], check=True)
        try:
            compare_csv(CURRENT_ANALYSIS, analysis)
        except AssertionError:
            if not update_current_analysis:
                raise
            backup = HERE / "kennedy_analysis_pre_isoform_fix.csv"
            if not backup.exists():
                shutil.copy2(CURRENT_ANALYSIS, backup)
            shutil.copy2(analysis, CURRENT_ANALYSIS)
            compare_csv(CURRENT_ANALYSIS, analysis)
            print(f"updated {CURRENT_ANALYSIS.name}; prior table retained as {backup.name}")
        return {
            "candidate_rows": len(pd.read_csv(candidate)),
            "candidate_sha256": sha256(candidate),
            "analysis_rows": len(pd.read_csv(analysis)),
            "analysis_proteins": int(pd.read_csv(analysis).acc.nunique()),
            "analysis_sha256": sha256(analysis),
            "every_row_and_column_matches": True,
        }


def build_manifest(rebuild: dict) -> dict:
    missing = [str(p) for p in PINNED if not p.exists()]
    if missing:
        raise SystemExit("missing pinned human-build artifacts: " + ", ".join(missing))
    cache = {}
    for name, directory, suffix in (
        ("alphafold_cif", CACHE / "af", ".cif"),
        ("uniprot_primary_json", CACHE / "uniprot", ".json"),
        ("uniprot_annotation_json", CACHE / "uniprot_annot", ".json"),
    ):
        count, digest = cache_digest(directory, suffix)
        cache[name] = {"files": count, "aggregate_sha256": digest}
    return {
        "schema_version": 1,
        "status": "PASS",
        "offline_source_to_cohort": rebuild,
        "pinned_files": {str(p.relative_to(HERE)): sha256(p) for p in PINNED},
        "cache_aggregates": cache,
    }


def check_manifest(manifest: dict) -> None:
    if manifest.get("status") != "PASS":
        raise SystemExit("human rebuild manifest status is not PASS")
    for rel, expected in manifest["pinned_files"].items():
        path = HERE / rel
        if not path.exists() or sha256(path) != expected:
            raise SystemExit(f"human rebuild hash mismatch: {rel}")
    for name, directory, suffix in (
        ("alphafold_cif", CACHE / "af", ".cif"),
        ("uniprot_primary_json", CACHE / "uniprot", ".json"),
        ("uniprot_annotation_json", CACHE / "uniprot_annot", ".json"),
    ):
        count, digest = cache_digest(directory, suffix)
        declared = manifest["cache_aggregates"][name]
        if count != declared["files"] or digest != declared["aggregate_sha256"]:
            raise SystemExit(f"human cache aggregate mismatch: {name}")
    af = pd.read_csv(AF_MANIFEST)
    cached = af[af.local_present]
    if not ((cached.api_status == 200)
            & (pd.to_numeric(cached.latest_version, errors="coerce") == 6)
            & (cached.is_complex == False)  # noqa: E712
            & cached.cif_url.str.endswith("model_v6.cif")).all():
        raise SystemExit("AlphaFold v6 metadata assertion failed")
    for row in cached.itertuples():
        path = CACHE / "af" / f"{row.accession}.cif"
        if sha256(path) != row.local_sha256:
            raise SystemExit(f"AlphaFold cache hash mismatch: {row.accession}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true",
                    help="run a fresh offline source-to-cohort rebuild before writing the manifest")
    ap.add_argument("--write-manifest", action="store_true")
    ap.add_argument("--update-current-analysis", action="store_true",
                    help="replace the canonical analysis if the fresh corrected rebuild differs")
    args = ap.parse_args()

    rebuild = run_offline_rebuild(args.update_current_analysis) if args.rebuild else None
    if args.write_manifest:
        if rebuild is None:
            raise SystemExit("--write-manifest requires --rebuild")
        manifest = build_manifest(rebuild)
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"wrote {MANIFEST.name}")
    manifest = json.loads(MANIFEST.read_text())
    check_manifest(manifest)
    print("human source-to-cohort verification PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
