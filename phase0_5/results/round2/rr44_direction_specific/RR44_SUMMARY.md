# RR-44 — Direction-Specific Endpoint (Growth Defect vs Growth Enhancement)

## Summary

Every published outcome in this project is direction-agnostic: a substitution is outcome-positive
when its replicate-averaged count of called conditions (`qvalue < 0.05`) exceeds zero, whatever the
sign of the S-score. RR-44 splits that endpoint by direction. The defect-specific endpoint — the one
matching the mechanistic prediction that a phosphosite near a catalytic or binding residue should
impair function — gives **AUC 0.5047 [0.396, 0.604] in the primary arm, versus 0.5268 [0.416, 0.631]
direction-agnostic**. Discrimination does not improve; the point estimate falls by 0.0221 and both
intervals straddle 0.5 across almost identical ranges. Restricting the outcome to the mechanistically
predicted direction does not rescue distance as a predictor.

R3's estimate that 18 of 79 primary-cohort positives are enhancement-dominant came from profile
extremes and does not survive the proper computation: **25 of 79 are enhancement-dominant, 46
defect-dominant, and 8 are exact ties** under called conditions only.

## Provenance and conventions

Frozen hashes verified before and after the run; all three match, and no file outside
`rr44_direction_specific/` was written.

| File | SHA-256 |
|---|---|
| `results/statistics.json` | `57d02d5b…48a0401` |
| `results/analysis_final.csv` | `e666827d…451ac4dd4` |
| `phase0_5/results/phase0_5_statistics.json` | `3ea01c7b…f050d02b` |

- Estimators loaded from the frozen `phase0_5/src/02_phase0_5_analysis.py` via `importlib`. The
  module is guarded by `if __name__ == "__main__": main()` and `exec_module` sets `__name__` to the
  spec name `p05`, so `main()` does not run. The script checks for the guard and aborts if it is
  absent; no estimator was copied or reimplemented.
- Post hoc sensitivity intervals: **20,000 protein-cluster draws, seed 20260728** (the module's
  `SEED`). This differs from the published primary interval, which uses 200,000 draws at seed
  `SEED + 1`; the direction-agnostic row below is therefore recomputed under the post hoc convention
  so all six rows are comparable. Its point estimate reproduces the published value exactly
  (0.5268234, `NUMBERS.md` §Two-arm table); only the Monte Carlo endpoints differ
  (0.416106–0.630551 here vs 0.416744–0.631539 published).
- Resampling unit: UniProt accession. Every substitution of a sampled protein is retained.
- Scoring orientation: `score = -dist_core_A`; shorter distance scored toward a screen-positive label.
- **Retained draws: 20,000 of 20,000 nominal for all six intervals.** No resample drew a single
  outcome class, which is expected with 60–82 positives out of 163–166. (RR-13)
- No interval endpoint touches exactly 0 or 1, so all six are reportable as intervals.

## Endpoint construction

Replicate aggregation follows `phase0_5/src/01_build_phase0_5_dataset.py::aggregate_raw_scores`
(lines 133–175): Supplementary Data 3 is inner-joined to `results/analysis_site_members.csv` on
`PBY ID` with `validate="many_to_one"`, per-strain counts are formed, then averaged over the
replicate strains of a substitution. That is the same per-strain-then-mean rule the outcome ledger
uses (`src/01_build_sites.py`: `raw_n_q05` aggregated with `"mean"`, label = mean > 0). Only the
counting predicate changes:

| Endpoint | Per-strain predicate |
|---|---|
| Direction-agnostic (published) | `qvalue < 0.05` |
| Defect-specific | `qvalue < 0.05 AND Score < 0` |
| Enhancement-specific | `qvalue < 0.05 AND Score > 0` |

Join: 17,214 strain-condition rows, 169 strains, 166 substitutions, 102 conditions. Of the 18,720
called rows in the full source table, 14,637 are `Score < 0` and 4,083 are `Score > 0`; **no row has
`Score` exactly 0 and no `Score` or `qvalue` is missing**, so the two direction-specific counts
partition the called conditions exactly and the definition carries no tie-breaking ambiguity at the
condition level.

Reconstruction check: rebuilding the direction-agnostic label through this path reproduces
`has_pheno` for all 166 rows (0 mismatches) and matches the published `raw_q05_mean_per_strain`
column to machine zero (max absolute delta 0). The direction-specific arms therefore differ from the
published endpoint only in the predicate, not in the join or the aggregation.

## Results

All AUCs use `score = -dist_core_A`; intervals are 20,000-draw protein-cluster percentile intervals
at seed 20260728.

| Arm | Endpoint | n | Proteins | Positives | AUC | 95% CI | Nominal draws | Retained draws |
|---|---|---|---|---|---|---|---|---|
| Primary (exclude annotation-coincident) | Direction-agnostic (published) | 163 | 48 | 79 | **0.5268234** | 0.416106–0.630551 | 20,000 | 20,000 |
| Primary | **Defect-specific** | 163 | 48 | **66** | **0.5046860** | 0.395574–0.604167 | 20,000 | 20,000 |
| Primary | Enhancement-specific | 163 | 48 | 60 | 0.5428803 | 0.434432–0.647714 | 20,000 | 20,000 |
| Inclusive sensitivity | Direction-agnostic (published) | 166 | 50 | 82 | 0.5441347 | 0.434521–0.647659 | 20,000 | 20,000 |
| Inclusive | **Defect-specific** | 166 | 50 | **69** | **0.5262214** | 0.418308–0.627313 | 20,000 | 20,000 |
| Inclusive | Enhancement-specific | 166 | 50 | 60 | 0.5275157 | 0.416943–0.632647 | 20,000 | 20,000 |

Label overlap (each arm, 166/163 rows):

| Arm | Defect+ / Enh+ | Defect+ / Enh− | Defect− / Enh+ | Defect− / Enh− |
|---|---|---|---|---|
| Primary (163) | 47 | 19 | 13 | 84 |
| Inclusive (166) | 50 | 19 | 10 | 87 |

The three annotation-coincident 0 Å substitutions that separate the arms are all defect-positive and
none is enhancement-positive, which is why the enhancement arm has 60 positives in both cohorts.

## Does the defect-specific endpoint discriminate differently?

**No.** In the primary arm the defect-specific AUC is 0.5046860 against 0.5268234
direction-agnostic, a decrease of **0.0221374**. The two intervals (0.396–0.604 and 0.416–0.631)
overlap over nearly their whole length and both contain 0.5 comfortably. The inclusive arm behaves
the same way: 0.5262214 against 0.5441347, a decrease of 0.0179133. The mechanistically motivated
restriction moves the estimate slightly toward chance, not away from it.

Two caveats on that comparison:

1. **No paired interval is available for the difference.** The frozen `paired_auc_difference` holds
   the label fixed and varies the score; here the score is fixed and the *label* changes. The frozen
   module has no estimator for that contrast, and the instruction not to reimplement the bootstrap
   was followed, so the difference is reported as a difference of point estimates with two marginal
   intervals. The two endpoints share 163 rows and 47 of their positives, so their sampling errors
   are strongly positively correlated and the marginal intervals overstate the uncertainty in the
   difference. A paired estimator would be needed to say whether −0.0221 is distinguishable from
   zero; it almost certainly is not, given the magnitude, but that is an inference and not a
   computed interval.
2. The enhancement-specific AUC in the primary arm (0.5429) is nominally the highest of the three,
   which runs opposite to the mechanistic prediction. With 60 positives and an interval of
   0.434–0.648 this is not evidence of anything; it is noted only so the defect result is not read
   as a directional signal that got diluted.

## Defect-dominant vs enhancement-dominant among the 79 primary-cohort positives

Dominance computed under called conditions only, comparing the replicate-averaged count of called
defect conditions with the replicate-averaged count of called enhancement conditions:

| Class | Count |
|---|---|
| Defect-dominant (`mean_defect > mean_enhance`) | **46** |
| Enhancement-dominant (`mean_enhance > mean_defect`) | **25** |
| Exact tie | **8** |
| Total | 79 |

Purity of the same 79: 19 defect-only, 13 enhancement-only, 47 called in both directions. Most
positives are mixed, which is why the answer is sensitive to the definition of "dominant."

**This does not agree with R3's 18 of 79.** R3's number is reproducible and its rule is
identifiable: classifying a positive as enhancement-dominant when the largest S-score over all 102
conditions exceeds the magnitude of the smallest (`sscore_max > -sscore_min`) gives exactly 18 of 79.
That rule ignores whether the extreme condition was called at all, and it forces a binary decision on
sites that are genuine ties. Cross-tabulated against the proper computation:

| R3 profile-extreme rule | Defect-dominant | Enhancement-dominant | Tied |
|---|---|---|---|
| Defect (61) | 42 | 12 | 7 |
| Enhancement (18) | 4 | 13 | 1 |

The two classifications disagree on 16 of 79 sites and agree on 55 of the 71 that are not ties. Of
R3's 18, only 13 are enhancement-dominant under called conditions; 12 sites R3 assigned to defect are
enhancement-dominant once the count is restricted to called conditions. R3 flagged the estimate as an
approximation and it should be replaced by **25 of 79** (with 8 ties reported alongside, not absorbed
into either class).

### Definitional ambiguity worth stating

The 8 ties are all single-replicate strains with an equal number of called defect and called
enhancement conditions (ENO1 S188 3v3, SAT4 S155 3v3, SKY1 S445 2v2, and five 1v1 sites: SNF1 T487,
VMA2 S503, GCN5 S64, SKY1 S427, MYO5 S359). They are not artefacts of replicate averaging. Any
statement of the form "N of 79 are enhancement-dominant" must say what happens to them: 25 excludes
ties, 33 would count `mean_enhance >= mean_defect`, and 13 counts only sites with no called defect
condition at all. Those three numbers describe the same data. Reporting one without the tie count is
what made R3's approximation look precise.

## Files

- `rr44_direction_specific_endpoint.py` — script; verifies hashes, aborts on mismatch.
- `rr44_direction_specific_results.csv` — the six-row estimate table.
- `rr44_direction_specific_results.json` — same plus join counts, reconstruction check, label
  cross-tabulation, dominance counts, and the R3 comparison.
- `rr44_primary_positive_dominance.csv` — the 79 primary-cohort positives with per-site defect and
  enhancement counts, dominance class, S-score extremes, and the R3 profile-extreme class.

## Proposed for NUMBERS.md

Not entered by this run. `NUMBERS.md` was not modified. The candidate entries are the six rows of the
estimate table, the dominance triple 46/25/8 of 79, and the declared convention line
(20,000 draws, seed 20260728, 20,000 retained for all six intervals).
