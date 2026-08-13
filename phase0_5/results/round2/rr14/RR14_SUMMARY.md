# RR-14 — SIFT missingness disclosure and extremal bound on the paired difference

Script: `rr14/rr14_sift_missingness_bound.py`. Outputs: `rr14/rr14_results.json`,
`rr14/rr14_missingness.csv`, `rr14/rr14_bounds.csv`. Nothing outside `rr14/` was written.

Frozen hashes for `results/statistics.json`, `results/analysis_final.csv`, and
`phase0_5/results/phase0_5_statistics.json` were verified before any computation and all three
matched. `phase0_5/src/02_phase0_5_analysis.py` is guarded by `if __name__ == "__main__"`, so it was
imported directly and `auc_from_ranks`, `bootstrap_auc`, and `paired_auc_difference` were used
unmodified. Nothing was reimplemented.

Conventions: 20,000 protein-cluster draws, base seed 20260728 (the module's `SEED`), resampling unit
the UniProt accession with every substitution of a sampled protein retained, distance scored as
`-dist_core_A` so that shorter distance is scored toward a screen-positive label. `sift_ala_score_inv`
is already oriented the same way. **Every interval below retained 20,000 of 20,000 nominal draws** —
no resample drew a single outcome class, which is expected given 79 positives across 48 proteins. No
interval endpoint falls at exactly 0 or 1.

## 1. Missingness comparison, primary cohort (n = 163)

| group | n | proteins | positives | outcome rate | median distance (Å) | IQR (Å) | Q1–Q3 (Å) |
|---|---|---|---|---|---|---|---|
| SIFT observed | 152 | 48 | 71 | 0.46710526315789475 | 28.520400047302246 | 28.673699617385864 | 13.894179105758667 – 42.56787872314453 |
| SIFT missing | 11 | 6 | 8 | 0.7272727272727273 | 51.7973747253418 | 42.01997947692871 | 19.099620819091797 – 61.11960029602051 |
| all primary | 163 | 48 | 79 | 0.48466257668711654 | 28.930192947387695 | 29.69598150253296 | 13.744385242462158 – 43.44036674499512 |

The missingness is not random on either axis. The 11 unscored substitutions are outcome-positive at
0.727 against 0.467 in the scored set, and they sit farther from the nearest core annotation: median
51.80 Å against 28.52 Å. Expressed with the project's own rank statistic, the probability that a
randomly chosen missing site is farther from core than a randomly chosen scored site is
**0.6543062200956937**.

The 11 rows come from 6 proteins (P06782 ×3, P16140 ×3, P32561 ×2, P32485, P47116, Q04439), so the
missingness is clustered by protein and the cluster bootstrap propagates that clustering correctly.
Their per-row detail is in `rr14_results.json` under `missing_records`.

## 2. Direction of the selection

Far-from-core plus outcome-positive is exactly the combination that the distance score gets wrong,
because shorter distance is scored toward positive. Dropping those 11 rows therefore removes cases
that penalise distance. The frozen distance AUC on the 152-row common support is
0.5317336115458181; recomputed on the full 163 with the same estimator and seed it is
**0.5268233875828813 (95% CI 0.4161064593848292 to 0.6305511618234994, 20,000 of 20,000 draws
retained)**, i.e. 0.0049 lower.

The selection runs mildly **in distance's favour**, which means it runs against SIFT's measured
margin. The published difference of 0.074 is, if anything, a slight understatement. The selection
does not flatter the manuscript's own predictor.

## 3. Extremal bound on the paired SIFT-minus-distance AUC difference (full n = 163)

Both bounds impute the 11 missing SIFT values at the extremal rank conditional on outcome — for the
least-favourable case, all 8 missing positives are ranked below every observed value and all 3
missing negatives above every observed value; the most-favourable case reverses that. Because AUC
depends only on ranks, these are the logical minimum and maximum attainable by any imputation
whatsoever, not a plausible-data interval. Both use seed 20260728 and 20,000 protein-cluster draws.

| arm | n | SIFT AUC | SIFT − distance | 95% CI | draws retained / nominal |
|---|---|---|---|---|---|
| published, common support | 152 | 0.6061554512258738 | 0.07442183968005567 | −0.036886844864257466 to 0.1915291204090428 | 20,000 / 20,000 |
| least favourable for SIFT | 163 | 0.5253164556962026 | **−0.0015069318866787196** | −0.11935317460317457 to 0.125049169600256 | 20,000 / 20,000 |
| most favourable for SIFT | 163 | 0.6586799276672695 | **0.13185654008438819** | 0.024375526072497974 to 0.2477263487541264 | 20,000 / 20,000 |

The bound on the point estimate is −0.0015 to +0.1319, containing the published 0.0744.

## 4. What survives and what does not

Survives both bounds: distance does not outperform the cheap sequence comparator anywhere in the
range. Even when the missing data are stacked maximally against SIFT, the paired difference is
−0.0015 — a dead heat, not a distance advantage — and its interval spans zero symmetrically. The
manuscript's substantive reading, that proximity to a core annotation carries no discriminative
advantage over a sequence-constraint baseline, is not sensitive to the 11 missing scores.

Does not survive the extreme: the narrower statement that SIFT's advantage over distance is
statistically indistinguishable from zero holds at the point estimate and under the least-favourable
imputation, but fails under the most-favourable one, where the interval is 0.0244 to 0.2477 and
excludes zero. That case requires all 8 unscored positives to be more constrained than every one of
the 152 scored sites and all 3 unscored negatives less constrained than every one of them
simultaneously, which is an adversarial construction rather than a credible scenario. It should be
disclosed as the boundary of the claim, not treated as evidence that SIFT wins.

Recommended reader-facing framing: report the published common-support value with its n, state the
missingness (11 of 163, enriched for positives and for long distances), state that the exclusion is
mildly favourable to distance, and give the extremal range −0.002 to +0.132 with the note that only
the most-favourable extreme moves the interval off zero.

## 5. Caveats and ambiguities, stated rather than resolved silently

- "Least/most favourable rank" is implemented as the extremal outcome-conditional rank assignment.
  It is the widest logically possible bound. Any distributional imputation — median SIFT, protein
  mean, multiple imputation from the observed marginal — lies strictly inside it and would produce a
  narrower range. If the intended reading of RR-14 was a plausible-data bound rather than a logical
  one, this over-covers and should be re-run with a stated imputation model.
- The imputed values are placed outside the observed `sift_ala_score_inv` support (which runs −1.0 to
  0.0 with 124 distinct values among the 152). This is harmless for a rank-based AUC but means the
  imputed columns are not interpretable as SIFT scores and must not be reused for any non-rank
  statistic.
- Both bounds use the same seed, so the two arms are compared on identical protein resamples. The
  published common-support value used the module's `SEED + 12` offset, so its interval is not draw-for-draw
  comparable to the bounds; the point estimates are exact and are.
- With 6 distinct proteins carrying all 11 missing rows, a protein-cluster resample either takes a
  missing protein's full block or none of it. The bound intervals are consequently coarser than their
  width suggests, and their endpoints should be read to two decimals rather than three.
- No new numbers here are authorised for NUMBERS.md. They are proposed for the author to enter.
