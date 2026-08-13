# Phase 0.5 Release Package

This directory extends the public-data Phase 0 calibration with protein-cluster uncertainty, AlphaFold v6
pairwise PAE, raw 102-condition growth-profile summaries, alternative feature definitions, and grouped
out-of-sample benchmarks.

## Run

```bash
./run_all.sh
```

Use Python 3.12 with the versions in `requirements-lock.txt`. Cached AlphaFold PAE files permit offline
reruns after the first successful retrieval.

## Main files

- `RESULTS.md` — findings and interpretation boundary.
- `ANALYSIS_PROVENANCE.md` — exploratory status and decision history.
- `results/phase0_5_publication_data.csv` — one row per analyzed phosphosite.
- `results/phase0_5_statistics.json` — machine-readable results.
- `results/phase0_5_supplement.xlsx` — formatted tables, analysis data, source manifest, and mismatch audit.
- `results/pae_column_sensitivity_at_10A.csv` and `results/pae_filter_grid_72x3.csv` — all four PAE definitions and the primary, inclusive, and legacy 72-cell grids.
- `results/sift_comparator_sensitivity.csv` — primary, inclusive, and legacy common-support SIFT comparisons.
- `results/phase0_5_robustness_summary.{pdf,png}` — one-page summary figure.
- `results/verification_report.json` — fail-closed reconciliation checks.
- `results/release_manifest.csv` — SHA-256 checksums.

Source spreadsheets are read but never modified. The source files retain their original terms; no license
for redistribution of those workbooks is asserted here.
