# RR-13 and RR-59 disclosure audits

Frozen-tree hashes verified before computation: `results/statistics.json`
`57d02d5b…a0401`, `results/analysis_final.csv` `e666827d…ac4dd4`,
`phase0_5/results/phase0_5_statistics.json` `3ea01c7b…50d02b`. All three match. Re-verified
unchanged after the run.

Estimators were loaded from the frozen module `phase0_5/src/02_phase0_5_analysis.py`. That file
guards `main()` behind `if __name__ == "__main__":`, so importing by spec executes definitions
only; nothing was reimplemented. Constants read from the module: `SEED = 20260728`,
`N_PRIMARY_BOOT = 200000`, `N_SENSITIVITY_BOOT = 20000`, `N_CORR_BOOT = 4000`, `N_WILD = 9999`.

Script: `audit_rr13_rr59/rr13_rr59_audit.py`.
Outputs: `rr13_bootstrap_draw_audit.csv` (217 interval records), `rr59_predictor_benchmark_dual_summary.csv`,
`rr13_rr59_audit.json`.

---

## RR-13 — bootstrap draw retention

217 stored interval records were found across `results/` and `phase0_5/results/`. Of those, 167
come from a resampling estimator and 50 are analytic logistic intervals (Wald / cluster-robust)
that involve no draws. Twelve records show a shortfall against their nominal count; those twelve
are six distinct quantities, each stored twice (once in `phase0_5_statistics.json`, once in the
matching CSV). Four records — two distinct quantities, each stored twice — have an interval
endpoint at exactly 1.000. No endpoint anywhere touches 0.

### Table S-RR13a. Bootstrap intervals that retained fewer than their nominal draws

All are protein-cluster `bootstrap_auc` calls at a nominal 20,000 draws. Shortfall is the number
of resamples discarded because the resampled set contained a single outcome class.

| Quantity | Stored in | n sites / proteins / positive | AUC | 95% interval | Nominal | Retained | Shortfall | Discarded % | Endpoint at 0 or 1 |
|---|---|---|---|---|---|---|---|---|---|
| `cohort_sensitivity`: primary_tyrosine_only | `phase0_5_statistics.json` `/cohort_sensitivity[5]`; `cohort_sensitivity.csv` row 6 | 16 / 12 / 12 | 0.6041666666666666 | 0.2718831168831169 – 1.0 | 20 000 | 19 335 | 665 | 3.325 % | yes, upper = 1.000 |
| `residue_class_sensitivity`: Y | `phase0_5_statistics.json` `/residue_class_sensitivity[2]`; `residue_class_sensitivity.csv` row 3 | 16 / 12 / 12 | 0.6041666666666666 | 0.26666666666666666 – 1.0 | 20 000 | 19 404 | 596 | 2.980 % | yes, upper = 1.000 |
| `confidence_strata` exclude / site_plddt_ge_90 | `phase0_5_statistics.json`; `confidence_strata.csv` row 5 | 35 / 16 / 22 | 0.5699300699300699 | 0.37074235288521007 – 0.7464123376623376 | 20 000 | 19 999 | 1 | 0.005 % | no |
| `confidence_strata` exclude / very_high_confidence_joint | `phase0_5_statistics.json`; `confidence_strata.csv` row 11 | 27 / 13 / 15 | 0.6833333333333333 | 0.4807692307692308 – 0.8640098765432097 | 20 000 | 19 999 | 1 | 0.005 % | no |
| `confidence_strata` include / site_and_target_plddt_ge_90 | `phase0_5_statistics.json`; `confidence_strata.csv` row 17 | 31 / 15 / 19 | 0.6973684210526315 | 0.5357142857142857 – 0.8421052631578947 | 20 000 | 19 997 | 3 | 0.015 % | no |
| `confidence_strata` include / very_high_confidence_joint | `phase0_5_statistics.json`; `confidence_strata.csv` row 22 | 30 / 15 / 18 | 0.7361111111111112 | 0.553030303030303 – 0.9027777777777778 | 20 000 | 19 999 | 1 | 0.005 % | no |

The prior spot check is confirmed: 19,335 (tyrosine-only cohort arm) and 19,404 (residue class Y)
against a declared 20,000. It was incomplete — four further shortfalls exist, all in
`confidence_strata`, all one to three draws.

The two tyrosine records are the same 16 sites (12 proteins, 12 positive, 4 negative) estimated
twice under different seed offsets. Same point estimate, different lower endpoints
(0.2718831168831169 vs 0.26666666666666666), different retention (19,335 vs 19,404). With four
negatives spread over 12 proteins, 3 % of protein resamples contain no negative at all, which is
also why the upper endpoint saturates.

### Table S-RR13b. Intervals with an endpoint at exactly 0 or 1

| Quantity | Stored in | n sites / proteins | positive / negative | AUC | Interval as stored | Retained draws |
|---|---|---|---|---|---|---|
| primary_tyrosine_only cohort arm | `phase0_5_statistics.json` `/cohort_sensitivity[5]`; `cohort_sensitivity.csv` | 16 / 12 | 12 / 4 | 0.604 | 0.272 – **1.000** | 19 335 |
| residue class Y | `phase0_5_statistics.json` `/residue_class_sensitivity[2]`; `residue_class_sensitivity.csv` | 16 / 12 | 12 / 4 | 0.604 | 0.267 – **1.000** | 19 404 |

Under the declared convention, neither interval may be reported. The upper endpoint of 1.000 is
not an estimate of the sampling limit — it is the boundary of the AUC statistic being hit by
resamples in which the four negatives collapse, so the percentile is uninformative there. Both
should appear in reader-facing text as a point estimate with its counts and no interval:

> Tyrosine sites: AUC 0.604 (16 sites in 12 proteins; 12 phenotype-positive, 4 negative). No
> interval is reported — the protein-cluster bootstrap upper endpoint reaches the boundary value
> of 1, and 3.3 % (665/20,000) of resamples were discarded for containing a single outcome class.

The tyrosine AUC of 0.604 and the residue-class-Y AUC of 0.604 are the same quantity computed
twice; the supplement should say so rather than presenting them as two results.

### The canonical 200,000-draw arm intervals

Stated explicitly, as asked: **yes, both retained all 200,000 draws — zero discarded.**

| Arm | Resampling unit | Estimate | 95% interval | Nominal | Retained | Shortfall |
|---|---|---|---|---|---|---|
| Primary (exclude_annotation_coincident), 163 sites / 48 proteins / 79 positive | protein cluster | 0.5268233875828813 | 0.41674431974078835 – 0.6315393408472534 | 200 000 | 200 000 | 0 |
| Inclusive sensitivity (include_annotation_coincident), 166 sites / 50 proteins / 82 positive | protein cluster | 0.5441347270615563 | 0.43575552928798883 – 0.6487455197132617 | 200 000 | 200 000 | 0 |
| Primary, naive site bootstrap | site | 0.5268233875828813 | 0.43673469387755104 – 0.6173687782887222 | 200 000 | 200 000 | 0 |
| Inclusive, naive site bootstrap | site | 0.5441347270615563 | 0.4553844562647754 – 0.632703488372093 | 200 000 | 200 000 | 0 |

With 79 positives and 84 negatives spread across 48 proteins, a single-class protein resample is
effectively impossible, so full retention is the expected result rather than a surprise.

### Provenance caveat on the `draws` field — read before quoting a retained count

The two source modules do not mean the same thing by `draws`.

- `phase0_5/src/02_phase0_5_analysis.py::bootstrap_auc` and `paired_auc_difference` return
  `"draws": len(draws)` — the count after discarding single-class resamples. **Every `draws`
  value written under `phase0_5/results/` is a measured retained count.** The four 200,000 rows
  above come from there and are real.
- `src/03_analysis.py::boot_auc` returns only `(point, lo, hi)`. `results/statistics.json` then
  writes `"draws": N_PRIMARY_BOOT` and `"naive_site_draws": N_PRIMARY_BOOT` as literal constants
  (lines 124 and 129), and `results/cohort_arm_primary_estimates.csv` carries those same
  literals. **Those 200,000 entries are nominal, not measured.** They happen to be correct — the
  phase-0.5 recomputation of the identical quantity, same seed offset, same point estimate and
  same endpoints to full precision, reports a true retained count of 200,000 — but the phase-0
  file is not itself evidence of retention. Cite `phase0_5_statistics.json` for the claim.

Three further disclosure gaps, none of which change a number:

1. `results/statistics.json` stores intervals for `auc_other_predictors` (pLDDT, RSA,
   n_annot_residues) and for `sift_comparator` with **no draw count at all** — 16 records across
   the four duplicated cohort blocks. Nominal is 20,000 by the `boot_auc` default. Retained is
   unrecoverable without rerunning, which this audit did not do.
2. `phase0_5/results/sift_comparator_sensitivity.csv` has no `draws` column, but the same nine
   intervals in `phase0_5_statistics.json` carry `draws = 20000` with zero shortfall.
3. `phase0_5_statistics.json` `continuous_outcomes` and `confidence_correlations` are
   `cluster_boot_spearman` results, nominal 4,000 draws, and that function stores no retained
   count either — it silently drops non-finite ρ. Eleven records. If the supplement quotes these
   correlation intervals, the retention is undocumented.

---

## RR-59 — predictor benchmark, both summaries, all four models

Every value below was read from `phase0_5/results/predictor_benchmark.csv` and matches the prior
reading exactly. The pooled column was independently re-derived from the stored out-of-fold
predictions in `phase0_5_analysis_with_oof_predictions.csv` (163 rows, 79 positive) using the
frozen module's own `auc_from_ranks`; all five agree to every printed digit.

### Table S-RR59. Cross-validated discrimination, split-averaged and pooled

| Model | Features | Split-averaged AUC | 2.5th–97.5th pct across 10 repeats | Pooled out-of-fold AUC | Pooled − split-averaged | Brier |
|---|---|---|---|---|---|---|
| constant_prevalence | none | 0.500000 | 0.500000 – 0.500000 | 0.500000 | 0.000000 | 0.24976476344612142 |
| distance_only | logd | 0.483676694194521 | 0.4127008752537201 – 0.5267466119493138 | 0.3925557564798071 | −0.0911209377147139 | 0.2583952943656099 |
| structural | logd; plddt; rsa; pae_pair_max; log_n_annot | 0.5579874728059712 | 0.5185344009650704 – 0.6066437347484296 | 0.5230560578661845 | −0.0349314149397867 | 0.25889194860959397 |
| published_annotations | supp_is_disopred; age_ordinal; has_uniprot_domain; sift_ala_score_inv; PWM_nkinTop01 | 0.5896358604696592 | 0.5558254359273878 – 0.6398948737175367 | 0.5732368896925859 | −0.0163989707770733 | 0.25249378935322414 |
| combined | all ten of the above | 0.5869982933996968 | 0.5321894180819378 – 0.6241394351860644 | 0.5688667872212176 | −0.0181315061784792 | 0.25924201709527217 |

Recomputed pooled values, frozen `auc_from_ranks` on the stored OOF columns: constant_prevalence
0.5, distance_only 0.3925557564798071, structural 0.5230560578661845, published_annotations
0.5732368896925859, combined 0.5688667872212176. Identical to the stored column in all five cases.

The prompt's prior reading gave only the pooled figure for `structural` (0.523056) and `combined`
(0.568867). Their split-averaged counterparts are 0.5579874728059712 and 0.5869982933996968.

### What the pooled column changes

The pooled AUC is lower than the split-averaged estimate for all four fitted models, by 0.016 to
0.091. The two summaries are not interchangeable and the gap is not noise: the split-averaged
number is the mean over 10 repeats of a positive–negative-pair-weighted average of five per-fold
AUCs, so it never compares a case in fold 1 against a case in fold 4. The pooled number ranks all
163 out-of-fold predictions against each other, which additionally penalizes any fold-to-fold
shift in the predicted probability scale. Reporting only the split-averaged value overstates
every model.

For `distance_only` the difference is qualitative. Split-averaged, 0.4837 reads as "at chance,
maybe a hair below." Pooled, 0.3926 is 0.107 below chance — the same direction that the primary
protein-clustered arm estimate (0.527, interval spanning 0.5) declines to resolve, but here far
enough from 0.5 that describing distance as uninformative is the wrong description. The honest
statement is that the sign of the distance effect flips between the pooled cross-validated
ranking and the primary arm AUC, and neither is precise enough to settle it. Note that the
pooled figure carries no interval at all in the stored file, so it cannot be used to claim
below-chance performance is statistically established.

Ordering is unaffected: `published_annotations` > `combined` > `structural` > `distance_only`
under both summaries. Adding the five structural features to the five published annotations does
not improve either summary (−0.0026 split-averaged, −0.0044 pooled) and worsens the Brier score
(0.25249 → 0.25924).

### Interval caveat on `split_low` / `split_high`

These columns are the 2.5th and 97.5th percentiles of **10** repeat values. They describe the
spread of the repeated-splitting procedure, not sampling uncertainty about the population AUC,
and with n = 10 the percentiles are interpolated between the extreme order statistics. They
should not be labelled a 95 % confidence interval in the supplement. No protein-cluster bootstrap
interval is stored for any benchmark model.
