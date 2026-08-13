# RR-16 — Permutation null for the primary estimand

Estimand: AUC of `-min_dist_A` (shorter distance scored toward the screen-positive label) for `y`,
primary cohort `exclude_annotation_coincident`. n = 163 substitutions, 48 UniProt accessions,
79 positive / 84 negative. Observed AUC recomputed with the frozen `auc_from_ranks`:
**0.5268233875828813**, identical to `results/statistics.json`.

Frozen hashes for `results/statistics.json`, `results/analysis_final.csv`, and
`phase0_5/results/phase0_5_statistics.json` were verified before any computation and all three match.
The phase 0.5 module is `__main__`-guarded, so it was imported and its `auc_from_ranks` /
`bootstrap_auc` were used directly; nothing was reimplemented.

20,000 permutations, seed 20260728 (`p05.SEED`), `numpy.random.default_rng`.

## (a) Unrestricted label permutation across all 163 substitutions

| quantity | value |
|---|---|
| null mean | 0.5001785940325497 |
| null SD | 0.04524083158115652 |
| 2.5th pct | 0.41063517179023507 |
| 97.5th pct | 0.5883062085593731 |
| full range | 0.32881253767329716 – 0.6832429174201327 |
| two-sided p (about 0.5, `(b+1)/(n+1)`) | 0.5547722613869307 |
| two-sided p (about 0.5, raw `b/n`) | 0.55475 (11,095 / 20,000) |
| z about the null mean | 0.5889545487804321 |

## (b) Permutation within protein

Labels shuffled only among the substitutions of the same accession. 23 of 48 proteins carry both
labels (112 of 163 substitutions); the other 25 proteins (51 substitutions) are single-label and are
therefore held fixed by construction.

| quantity | value |
|---|---|
| null mean | 0.5119963381555154 |
| null SD | 0.030478444626320225 |
| 2.5th pct | 0.45313441832429174 |
| 97.5th pct | 0.5726341169379144 |
| full range | 0.39828209764918626 – 0.6424050632911392 |
| two-sided p about the null mean 0.51200 (`(b+1)/(n+1)`) | 0.6300184990750463 |
| two-sided p about the null mean, raw | 0.6300 (12,600 / 20,000) |
| two-sided p about 0.5 (`(b+1)/(n+1)`) | 0.4136793160341983 |
| z about the null mean | 0.48647657743537637 |

The within-protein null is not centered at 0.5 (mean 0.51200). Between-protein pairs are held fixed
by this permutation, and their fixed contribution sits slightly above chance, so 0.5 is the wrong
reference point here. The p-value to quote for (b) is the one centered on the null mean, 0.6300;
the 0.4137 figure is reported only to show that the choice of center moves the number and neither
choice approaches significance.

## Which null is the appropriate reference

(b), within protein. The estimand is protein-clustered: outcomes are correlated within an accession
(25 of 48 proteins are entirely one label), and distance is likewise a protein-level property in part.
Unrestricted permutation destroys that clustering, so its null is generated from a data-generating
process the design does not have — it treats 163 substitutions as 163 independent units when the
effective number is closer to 48. Its SD (0.04524) is 1.48x the clustered SD (0.03048) here, so the
unrestricted null is the *wider*, and therefore the more conservative, reference in this dataset;
its width is not a property of the estimand but an artifact of resampling at the wrong unit. (a) is
reported for completeness and because it is what R1 appears to have computed.

Neither null supports discrimination: the observed AUC sits 0.59 (a) or 0.49 (b) null SDs from its
null center.

## Cluster-bootstrap interval for the observed AUC (declared convention)

`bootstrap_auc(y, -min_dist_A, groups=acc, n=20000, seed=20260728)`:
0.5268233875828813, 95% percentile interval [0.4161064593848292, 0.6305511618234994].
**Retained draws 20,000 of a nominal 20,000** — no resample drew a single outcome class (RR-13).
Neither endpoint touches 0 or 1.

## The null spread against the size of the declared post hoc families

| family | count |
|---|---|
| confidence strata (11) x cohorts (2) | 22 |
| PAE grids (72 cells) x cohorts (3) | 216 |
| feature definitions | 5 |
| cohort/residue sensitivities | 7 |
| continuous outcomes | 5 |
| **total estimates across all declared families** | **255** |

At 255 estimates, 12.75 are expected to clear p < 0.05 by chance alone. Treating the 255 as
independent draws from the null (they are not — the PAE grid cells in particular are heavily
overlapping subsets, so this overstates the spread):

| | unrestricted null | within-protein null |
|---|---|---|
| median of the max \|AUC − null mean\| over 255 draws | 0.13518362300034822 | 0.09152988245931282 |
| 95th pct of that max | 0.15832701411204905 | 0.11245806713840868 |
| implied largest AUC seen by chance (median / 95th) | 0.6354 / 0.6585 | 0.6035 / 0.6245 |

So a post hoc subgroup AUC of roughly 0.64 (unrestricted null) or 0.60 (clustered null) is the
*typical* maximum a family of 255 null estimates produces. Any post hoc AUC below those values
carries no evidence at all once the family is counted, and the observed primary AUC of 0.5268 is far
inside even a single null's 95% interval.

## Reconciliation with R1

R1 (unverified): SD 0.045, range 0.410–0.588, p 0.55.

- SD 0.045 matches (a) to the precision quoted: 0.04524 rounds to 0.045. Agrees.
- p 0.55 matches (a): 0.55475 raw, 0.55477 with the +1 correction. Agrees.
- **"Range 0.410–0.588" is mislabelled.** Those are the 2.5/97.5 percentiles of (a)
  (0.41064, 0.58831), not the range. The actual full range of the 20,000 unrestricted permutation
  AUCs is 0.32881 – 0.68324. Reported as a range, R1's interval understates the null's extremes by
  0.082 at the low end and 0.095 at the high end — which matters exactly where it is used, as the
  benchmark for how extreme a post hoc subgroup AUC can get by chance.
- R1 reports no within-protein null. (b) is a different and narrower distribution
  (SD 0.03048, p 0.6300 about its own mean) and is the reference that matches the design.

Substantive conclusion is unchanged: the primary AUC is indistinguishable from chance under either
permutation scheme.

## Stability and ambiguities, stated rather than resolved silently

- Monte Carlo SE of the (a) p-value at 20,000 permutations is sqrt(0.5548 x 0.4452 / 20000) =
  0.0035, so p is stable to the second decimal. The SDs are stable to ~0.0002. The **range** endpoints
  are the least stable statistic reported here — a min/max over 20,000 draws moves with seed by
  order 0.01. Do not quote the range to three decimals as if it were reproducible.
- The centering of the (b) p-value is a genuine definitional choice (0.5 vs the permutation mean
  0.51200). Both are given above. The mean-centered version is the internally consistent one.
- (b) fixes 51 of 163 substitutions (the 25 single-label proteins). The within-protein null therefore
  tests a strictly weaker hypothesis than (a): whether distance ranks substitutions correctly
  *inside* a protein. That is the right question for this estimand, but it is a different question
  from the one (a) asks.

## Files

- Script: `rr16_permutation_null.py`
- `rr16_permutation_null.json` (all numbers at full precision), `rr16_permutation_null.csv`
- `rr16_null_draws_unrestricted.npy`, `rr16_null_draws_within_protein.npy` (the 20,000 draws each)

Nothing in the frozen tree was modified. `NUMBERS.md` was not edited; the numbers above are proposed
for the author to enter.
