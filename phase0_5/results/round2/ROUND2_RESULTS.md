# ROUND2_RESULTS.md — Consolidation of the Eight Round-2 Authorized Analyses

Scope: RR-43, RR-44, RR-30/RR-58, RR-16, RR-14, RR-29, RR-13/RR-59, RR-28, all run against the frozen
calibration tree. All eight verified the three frozen hashes before computing and all eight report a
match:

- `results/statistics.json` — `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`
- `results/analysis_final.csv` — `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`
- `phase0_5/results/phase0_5_statistics.json` — `3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b`

No analysis modified a frozen file and none edited `NUMBERS.md`. Every estimator was imported from
`phase0_5/src/02_phase0_5_analysis.py`; none was reimplemented. Every post hoc interval below uses
20,000 nominal protein-cluster draws at seed 20260728 unless stated otherwise. Retained draws are
given for every interval.

---

## 1. Does the story hold?

**Yes. The near-chance reading survives both the stricter endpoint and the direction-specific
endpoint.**

**RR-43, stricter endpoints.** Raising the screen-positive threshold from ≥1 called condition to ≥2
and ≥3 moves the primary AUC from 0.526823 to 0.549918 to 0.563096, and every interval still spans
0.5 by a wide margin — the widest lower bound is 0.448441 and the highest upper bound is 0.671997.
The estimate moves 0.023 and 0.036 against an interval half-width of 0.098 to 0.114. The ≥3 interval
is *wider* than the ≥2 interval because the positive class shrinks to 47 sites in 30 of 48 proteins.
The three endpoints share all 163 rows and differ only in labels, so no paired test across them is
valid and none was computed; the shifts are descriptive.

**RR-44, direction-specific endpoint.** Restricting the outcome to growth defect — the direction the
mechanistic hypothesis predicts — moves the primary AUC *toward* chance, 0.526823 → 0.504686, with
intervals 0.416106–0.630551 and 0.395574–0.604167 overlapping over nearly their whole length. The
enhancement-specific arm is nominally the highest of the three at 0.542880, opposite to the
prediction, and equally uninformative. No paired interval exists for the difference: the frozen
`paired_auc_difference` varies the score under a fixed label, and here the label changes under a
fixed score.

Neither analysis changes the manuscript's framing. Two side findings do change reader-facing text:

1. **RR-43 reverses the primary/inclusive ordering at ≥2.** The inclusive arm's published advantage
   (0.544135 vs 0.526823) is carried entirely by the three annotation-coincident sites at distance
   0.000, each with exactly one called condition. At ≥2 all three flip to negatives at distance zero
   and the inclusive AUC falls below the primary (0.534642 vs 0.549918); the two positive classes are
   then identical in size (58 at ≥2, 47 at ≥3). This supports the decision to exclude
   annotation-coincident sites from the primary cohort and should be stated.
2. **RR-44 replaces R3's dominance figure.** R3's "18 of 79 enhancement-dominant" came from profile
   extremes (`sscore_max > -sscore_min`, ignoring whether the extreme condition was called). Under
   called conditions the split is **46 defect-dominant, 25 enhancement-dominant, 8 exact ties**. The
   two rules disagree on 16 of 79 sites.

Two of the other six analyses were flagged as story-changing by their authors. Neither touches the
near-chance conclusion; both are mandatory disclosure corrections:

- **RR-13**: two published tyrosine intervals have an upper endpoint of exactly 1.000 and retained
  19,335 and 19,404 of 20,000 draws. Under the project's own convention they may not be reported as
  intervals. `NUMBERS.md` §12 currently reports both as intervals.
- **RR-59**: the pooled out-of-fold AUC for `distance_only` is 0.392556 against a split-averaged
  0.483677. The sign of the distance effect flips between the pooled cross-validated ranking and the
  primary arm AUC. `NUMBERS.md` §12 currently reports only the split-averaged value.
- **RR-28**: the design cannot be run on experimentally-evidenced annotation at all — only 24 of 163
  substitutions in 7 of 48 proteins retain any target. This forecloses the "the null is an annotation
  quality artifact" reading rather than changing the null.

---

## 2. Results tables

All intervals are 95% protein-cluster percentile intervals, resampling unit = UniProt accession,
seed 20260728, 20,000 nominal draws, unless the row says otherwise.

### 2.1 RR-43 — stricter outcome endpoints, `avg` rule (the published operationalisation)

| Endpoint | Arm | n | Positive | Proteins | Proteins with a positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ≥1 (published) | primary | 163 | 79 | 48 | 35 | 0.526823 | 0.416106–0.630551 | 20,000 | 20,000 |
| ≥1 (published) | inclusive | 166 | 82 | 50 | 37 | 0.544135 | 0.434521–0.647659 | 20,000 | 20,000 |
| ≥2 | primary | 163 | 58 | 48 | 32 | 0.549918 | 0.448441–0.645103 | 20,000 | 20,000 |
| ≥2 | inclusive | 166 | 58 | 50 | 32 | 0.534642 | 0.432551–0.629520 | 20,000 | 20,000 |
| ≥3 | primary | 163 | 47 | 48 | 30 | 0.563096 | 0.444859–0.671997 | 20,000 | 20,000 |
| ≥3 | inclusive | 166 | 47 | 50 | 30 | 0.548900 | 0.432560–0.657714 | 20,000 | 20,000 |

### 2.2 RR-43 — `all` rule (strict replicate consensus, sensitivity only)

| Endpoint | Arm | n | Positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|
| ≥1 | primary | 163 | 78 | 0.535294 | 0.426684–0.637653 | 20,000 | 20,000 |
| ≥1 | inclusive | 166 | 81 | 0.552505 | 0.443268–0.654998 | 20,000 | 20,000 |
| ≥2 | primary | 163 | 57 | 0.559583 | 0.460937–0.651591 | 20,000 | 20,000 |
| ≥2 | inclusive | 166 | 57 | 0.544182 | 0.444647–0.636630 | 20,000 | 20,000 |
| ≥3 | primary | 163 | 46 | 0.574322 | 0.460573–0.679588 | 20,000 | 20,000 |
| ≥3 | inclusive | 166 | 46 | 0.559964 | 0.447419–0.665008 | 20,000 | 20,000 |

The `avg` and `any` rules agree on all 166 substitutions at all three thresholds; `any` is not a
separate result. The `all` rule differs on exactly one substitution, P43565 S1764A, at every
threshold including the published ≥1.

### 2.3 RR-44 — direction-specific endpoints

| Arm | Endpoint | n | Proteins | Positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | Direction-agnostic (published) | 163 | 48 | 79 | 0.5268234 | 0.416106–0.630551 | 20,000 | 20,000 |
| Primary | Defect-specific | 163 | 48 | 66 | 0.5046860 | 0.395574–0.604167 | 20,000 | 20,000 |
| Primary | Enhancement-specific | 163 | 48 | 60 | 0.5428803 | 0.434432–0.647714 | 20,000 | 20,000 |
| Inclusive | Direction-agnostic (published) | 166 | 50 | 82 | 0.5441347 | 0.434521–0.647659 | 20,000 | 20,000 |
| Inclusive | Defect-specific | 166 | 50 | 69 | 0.5262214 | 0.418308–0.627313 | 20,000 | 20,000 |
| Inclusive | Enhancement-specific | 166 | 50 | 60 | 0.5275157 | 0.416943–0.632647 | 20,000 | 20,000 |

### 2.4 RR-30 / RR-58 — comparator predictors, primary cohort (n = 163, 79 positive, 48 proteins)

| # | Predictor | Orientation | AUC | 95% CI | Nom / Ret | Δ vs `min_dist_A` | Δ 95% CI | Δ Nom / Ret |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | min \|pos − target pos\|, eligible set | smaller → positive | 0.5498041 | 0.4340705–0.6526297 | 20,000 / 20,000 | +0.0229807 | −0.0493801–+0.0902666 | 20,000 / 20,000 |
| 2 | \|pos − nearest_feat_pos\| | smaller → positive | 0.5333785 | 0.4155022–0.6391447 | 20,000 / 20,000 | +0.0065552 | −0.0837502–+0.0933298 | 20,000 / 20,000 |
| 3 | protein_length | larger → positive | 0.5493520 | 0.4437905–0.6596845 | 20,000 / 20,000 | +0.0225286 | −0.1587298–+0.2154142 | 20,000 / 20,000 |
| 4 | site pLDDT | larger → positive | 0.5551537 | 0.4636676–0.6407907 | 20,000 / 20,000 | +0.0283303 | −0.0667389–+0.1313505 | 20,000 / 20,000 |
| 5 | inverse RSA (−rsa) | smaller rsa → positive | 0.5866486 | 0.4890610–0.6719103 | 20,000 / 20,000 | +0.0598252 | −0.0413001–+0.1619905 | 20,000 / 20,000 |
| 6 | n_annot_residues | larger → positive | 0.5553797 | 0.4701127–0.6485676 | 20,000 / 20,000 | +0.0285564 | −0.0822575–+0.1522954 | 20,000 / 20,000 |
| 7 | raw_conditions (negative control) | larger → positive | 0.4615732 | 0.4259259–0.4957457 | 20,000 / 20,000 | −0.0652502 | −0.1832897–+0.0574866 | 20,000 / 20,000 |
| 8 | **min_dist_A (declared)** | smaller → positive | 0.5268234 | 0.4161065–0.6305512 | 20,000 / 20,000 | 0 (reference) | not reported | — |

Missingness: none. All eight predictors are complete on all 163 rows, so every paired comparison
runs on the full 163.

### 2.5 RR-16 — permutation null, primary estimand (observed AUC 0.5268233876)

20,000 permutations per scheme, seed 20260728.

| Quantity | (a) Unrestricted | (b) Within protein |
|---|---:|---:|
| null mean | 0.5001785940 | 0.5119963382 |
| null SD | 0.0452408316 | 0.0304784446 |
| 2.5th percentile | 0.4106351718 | 0.4531344183 |
| 97.5th percentile | 0.5883062086 | 0.5726341169 |
| full range | 0.3288125377–0.6832429174 | 0.3982820976–0.6424050633 |
| two-sided p, `(b+1)/(n+1)` | 0.5547722614 (about 0.5) | 0.6300184991 (about the null mean) |
| two-sided p, raw | 0.55475 (11,095 / 20,000) | 0.6300 (12,600 / 20,000) |
| z about the null center | 0.5889545488 | 0.4864765774 |

(b) is the appropriate reference: the estimand is protein-clustered. (b) holds 51 of 163
substitutions fixed (the 25 single-label proteins); 23 of 48 proteins carrying 112 of 163
substitutions are permutable. The cluster-bootstrap interval recomputed under the post hoc
convention is 0.5268233876 [0.4161064594, 0.6305511618], **20,000 / 20,000 retained**.

Family-size context, 255 declared post hoc estimates (22 confidence-strata + 216 PAE-grid + 5 feature
definitions + 7 cohort/residue + 5 continuous):

| | Unrestricted null | Within-protein null |
|---|---:|---:|
| median max \|AUC − null mean\| over 255 draws | 0.1351836230 | 0.0915298825 |
| 95th percentile of that max | 0.1583270141 | 0.1124580671 |
| implied largest AUC by chance (median / 95th) | 0.6354 / 0.6585 | 0.6035 / 0.6245 |

### 2.6 RR-14 — SIFT missingness and extremal bound

Missingness, primary cohort n = 163:

| Group | n | Proteins | Positive | Outcome rate | Median distance (Å) |
|---|---:|---:|---:|---:|---:|
| SIFT observed | 152 | 48 | 71 | 0.4671052632 | 28.5204000473 |
| SIFT missing | 11 | 6 | 8 | 0.7272727273 | 51.7973747253 |
| all primary | 163 | 48 | 79 | 0.4846625767 | 28.9301929474 |

Probability that a randomly chosen missing site is farther from core than a randomly chosen scored
site: **0.6543062201**.

Extremal bound on the paired SIFT-minus-distance AUC difference, seed 20260728:

| Arm | n | SIFT AUC | SIFT − distance | 95% CI | Nominal | Retained |
|---|---:|---:|---:|---:|---:|---:|
| published, common support | 152 | 0.6061554512 | 0.0744218397 | −0.0368868449–+0.1915291204 | 20,000 | 20,000 |
| least favourable for SIFT | 163 | 0.5253164557 | −0.0015069319 | −0.1193531746–+0.1250491696 | 20,000 | 20,000 |
| most favourable for SIFT | 163 | 0.6586799277 | +0.1318565401 | +0.0243755261–+0.2477263488 | 20,000 | 20,000 |

The published common-support row in `rr14_bounds.csv` reproduces `NUMBERS.md` §10 exactly, to every
stored digit of the estimate and both endpoints.
Distance AUC on the 152-row common support is 0.5317336115; on all 163 rows it is 0.5268233876
[0.4161064594, 0.6305511618], **20,000 / 20,000 retained**, i.e. 0.0049 lower.

### 2.7 RR-29 — sequence-adjacency sensitivity

| Arm | Filter | n | Proteins | Positive | Negative | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| primary | all | 163 | 48 | 79 | 84 | 0.526823 | 0.416106–0.630551 | 20,000 | 20,000 |
| primary | `dpos` > 2 | 157 | 48 | 77 | 80 | **0.540584** | 0.428570–0.648366 | 20,000 | 20,000 |
| inclusive | all | 166 | 50 | 82 | 84 | 0.544135 | 0.434521–0.647659 | 20,000 | 20,000 |
| inclusive | `dpos` > 2 | 157 | 48 | 77 | 80 | 0.540584 | 0.428570–0.648366 | 20,000 | 20,000 |

The two filtered rows are the same 157 substitutions in 48 proteins, not two arms agreeing. Of the 10
primary substitutions at ≤5 Å, 5 sit at 1.3296–1.3419 Å with `dpos` = 1 (the C–N peptide bond) and a
sixth has `dpos` = 2; the cohort has 5 rows at `dpos` = 1, 1 at `dpos` = 2, and 157 at `dpos` ≥ 3,
with no row between 3 and 37.

Descriptive cutoff table, `dpos` > 2, primary cohort (the "beyond" column is unchanged from the
published table at every cutoff, because the filter removes nothing beyond 5 Å):

| Cutoff | n within | Positive within | Rate within | n beyond | Positive beyond | Rate beyond | Descriptive OR |
|---:|---:|---:|---:|---:|---:|---:|---:|
| ≤5 Å | 4 | 2 | 50.0000% | 153 | 75 | 49.0196% | 1.040000 |
| ≤8 Å | 14 | 10 | 71.4286% | 143 | 67 | 46.8531% | 2.835821 |
| ≤10 Å | 24 | 15 | 62.5000% | 133 | 62 | 46.6165% | 1.908602 |
| ≤15 Å | 37 | 22 | 59.4595% | 120 | 55 | 45.8333% | 1.733333 |

### 2.8 RR-13 — bootstrap draw retention

217 stored interval records: 167 from a resampling estimator, 50 analytic logistic intervals with no
draws.

Canonical arm intervals, **all four retained 200,000 of 200,000, zero discarded**:

| Arm | Unit | Estimate | 95% interval | Nominal | Retained |
|---|---|---:|---:|---:|---:|
| Primary (163 / 48 / 79 pos) | protein cluster | 0.5268233876 | 0.4167443197–0.6315393408 | 200,000 | 200,000 |
| Inclusive (166 / 50 / 82 pos) | protein cluster | 0.5441347271 | 0.4357555293–0.6487455197 | 200,000 | 200,000 |
| Primary, naive site | site | 0.5268233876 | 0.4367346939–0.6173687783 | 200,000 | 200,000 |
| Inclusive, naive site | site | 0.5441347271 | 0.4553844563–0.6327034884 | 200,000 | 200,000 |

Intervals that retained fewer than their nominal 20,000:

| Quantity | n sites / proteins / positive | AUC | 95% interval | Nominal | Retained | Shortfall | Discarded | Endpoint at 1 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `cohort_sensitivity` primary_tyrosine_only | 16 / 12 / 12 | 0.6041666667 | 0.2718831169–1.0 | 20,000 | 19,335 | 665 | 3.325% | yes |
| `residue_class_sensitivity` Y | 16 / 12 / 12 | 0.6041666667 | 0.2666666667–1.0 | 20,000 | 19,404 | 596 | 2.980% | yes |
| `confidence_strata` exclude / site_plddt_ge_90 | 35 / 16 / 22 | 0.5699300699 | 0.3707423529–0.7464123377 | 20,000 | 19,999 | 1 | 0.005% | no |
| `confidence_strata` exclude / very_high_confidence_joint | 27 / 13 / 15 | 0.6833333333 | 0.4807692308–0.8640098765 | 20,000 | 19,999 | 1 | 0.005% | no |
| `confidence_strata` include / site_and_target_plddt_ge_90 | 31 / 15 / 19 | 0.6973684211 | 0.5357142857–0.8421052632 | 20,000 | 19,997 | 3 | 0.015% | no |
| `confidence_strata` include / very_high_confidence_joint | 30 / 15 / 18 | 0.7361111111 | 0.5530303030–0.9027777778 | 20,000 | 19,999 | 1 | 0.005% | no |

The two tyrosine records are the same 16 sites (12 proteins, 12 positive, 4 negative) estimated twice
under different seed offsets. No endpoint anywhere touches 0.

Undocumented retention, three gaps, none of which changes a number: 16 records in
`results/statistics.json` (`auc_other_predictors` for pLDDT, RSA, `n_annot_residues`, and
`sift_comparator`) carry no draw count at all; `phase0_5/results/sift_comparator_sensitivity.csv` has
no `draws` column though the same 9 intervals in `phase0_5_statistics.json` carry 20,000 with zero
shortfall; and 11 `cluster_boot_spearman` records at a nominal 4,000 draws store no retained count.

Provenance caveat: `phase0_5/src/02_phase0_5_analysis.py` writes `"draws"` as a *measured retained*
count; `src/03_analysis.py` writes `N_PRIMARY_BOOT` as a literal, so the 200,000 entries in
`results/statistics.json` and `results/cohort_arm_primary_estimates.csv` are nominal, not measured.
Cite `phase0_5_statistics.json` for any retention claim.

### 2.9 RR-59 — predictor benchmark, both summaries

10 repeated stratified group 5-fold splits; n = 163, 79 positive. The pooled column was
independently re-derived from the stored out-of-fold predictions with the frozen `auc_from_ranks`
and agrees to every printed digit in all five cases.

| Model | Split-averaged AUC | 2.5–97.5 pct across 10 repeats | Pooled OOF AUC | Pooled − split | Brier |
|---|---:|---:|---:|---:|---:|
| constant_prevalence | 0.5000000000 | 0.500000–0.500000 | 0.5000000000 | 0.0000000000 | 0.2497647634 |
| distance_only | 0.4836766942 | 0.4127008753–0.5267466119 | **0.3925557565** | −0.0911209377 | 0.2583952944 |
| structural | 0.5579874728 | 0.5185344010–0.6066437347 | 0.5230560579 | −0.0349314149 | 0.2588919486 |
| published_annotations | 0.5896358605 | 0.5558254359–0.6398948737 | 0.5732368897 | −0.0163989708 | 0.2524937894 |
| combined | 0.5869982934 | 0.5321894181–0.6241394352 | 0.5688667872 | −0.0181315062 | 0.2592420171 |

No protein-cluster bootstrap interval is stored for any benchmark model. The `split_low` /
`split_high` columns are percentiles of 10 repeat values and describe the repeated-splitting
procedure, not sampling uncertainty. Ordering is identical under both summaries:
`published_annotations` > `combined` > `structural` > `distance_only`.

### 2.10 RR-28 — the annotation target set

Evidence of the nearest target actually used, n = 163: ECO:0000255 101, ECO:0000250 33,
ECO:0000269;ECO:0007744 12, ECO:0000305 8, ECO:0000269 4, ECO:0000305;ECO:0007744 3,
ECO:0000250;ECO:0000269;ECO:0007744 1, none 1. **Experimental 20 / 163 (12.3%); non-experimental
143 / 163 (87.7%).**

Expanded-residue level, 48 primary-cohort proteins, 533 eligible target residues: ECO:0000255 313,
ECO:0000250 120, ECO:0000269;ECO:0007744 55, ECO:0000269 15, ECO:0000305;ECO:0007744 15,
ECO:0000250;ECO:0000269;ECO:0007744 7, ECO:0000305 5, ECO:0000250;ECO:0000255 2, none 1.
**Experimental 92 / 533 (17.3%); non-experimental 441 / 533 (82.7%).** 21 of 533 are covered by more
than one record.

ATP is the nearest-target ligand for **86 of 163 (52.8%)**, 87 under a permissive reading of the one
ADP;AMP;ATP row. **24 of 48 (50%)** primary-cohort proteins are protein kinases or kinase-complex
subunits by UniProt protein name. BINDING interval widths: median 1, maximum 9; **33 records of width
≥ 8 contribute 289 of the 533 eligible residues (54.2%)**.

Restricting the eligible set to ECO:0000269 / ECO:0007744 residues:

| Quantity | Value |
|---|---:|
| substitutions retaining any target | **24 of 163 (14.7%)** |
| substitutions losing every target | 139 |
| proteins retaining any target | **7 of 48** |
| retained class balance | 11 positive / 13 negative |
| median distance, retained positives | 20.191083908 Å |
| median distance, retained negatives | 21.811134338 Å |
| rows whose nearest target was already experimental | 20 of 24 |
| mean per-row distance increase | 1.273656805 Å (median 0, max 14.142353058 Å) |

| Estimate | n | Proteins | AUC | 95% CI | Nominal | Retained |
|---|---:|---:|---:|---:|---:|---:|
| Experimental-only targets | 24 | 7 | 0.4195804196 | 0.2435897436–0.7083333333 | 20,000 | 19,991 |
| Same 24 rows, full-annotation distance | 24 | 7 | 0.4405594406 | 0.2283950617–0.7666666667 | 20,000 | 19,991 |
| Paired difference (exp − full) | 24 | 7 | −0.0209790210 | −0.1666666667–+0.0495867769 | 20,000 | 19,991 |

Recomputation validity: reproducing the full-set distances from the cached AlphaFold models gave a
maximum absolute deviation of 1.42e-14 Å over all 163 rows and `nearest_feat_pos` agreement on
163 / 163.

---

## 3. Proposed `NUMBERS.md` section — complete and copy-pasteable

> Copy the block below into `NUMBERS.md` after Section 17. It is written to that file's conventions.
> **`NUMBERS.md` was not edited by this consolidation.** Section 18 is deliberately *not* tagged
> `[REPO]`: none of these values is emitted by the seeded repository pipeline. They come from post hoc
> scripts in sibling directories that import the frozen estimators and read the frozen tree. The tag
> distinction is itself a claim rule and should not be blurred.

<!-- BEGIN PROPOSED SECTION 18 -->

## 18. Round-2 Authorized Analyses `[POST-HOC]`

Added **2026-08-12**. These values are **not** `[REPO]`: they are produced by scripts under
`rr43_stricter_endpoints/`, `rr44_direction_specific/`, `notes/rr30_rr58/`, `rr16_permutation_null/`,
`rr14/`, `rr29_sequence_adjacency/`, `audit_rr13_rr59/`, and `rr28/`, each of which verifies the three
frozen hashes in the header of this file, imports `auc_from_ranks`, `bootstrap_auc`, and
`paired_auc_difference` from `phase0_5/src/02_phase0_5_analysis.py` without reimplementation, and
writes nothing into the frozen tree. Every value here is post hoc and none was preregistered.

**Declared convention for this section.** All intervals are 95% protein-cluster percentile intervals
at **20,000 nominal draws, seed 20260728** (the module `SEED`, `N_SENSITIVITY_BOOT`), resampling unit
the UniProt accession with every substitution of a sampled protein retained, score `-dist_core_A` so
that shorter distance is scored toward the screen-positive label, unless a row declares otherwise.
Retained draws are stated for every interval. The published headline intervals use 200,000 draws at
seed `SEED + 1`; point estimates are unaffected by that difference, interval endpoints differ in the
third decimal. Rows labelled "(published)" reproduce the frozen point estimate exactly and differ from
Sections 1 and 8 only in Monte Carlo endpoints.

### 18.1 Stricter outcome endpoints (RR-43)

Raising the screen-positive threshold reclassifies former positives as negatives; it does not delete
them, so cohort n is unchanged at every endpoint.

| Endpoint | Arm | n | Positive | Proteins | Proteins with a positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ≥1 (published) | primary | 163 | 79 | 48 | 35 | 0.526823 | 0.416106–0.630551 | 20,000 | 20,000 |
| ≥1 (published) | inclusive | 166 | 82 | 50 | 37 | 0.544135 | 0.434521–0.647659 | 20,000 | 20,000 |
| ≥2 | primary | 163 | 58 | 48 | 32 | **0.549918** | **0.448441–0.645103** | 20,000 | 20,000 |
| ≥2 | inclusive | 166 | 58 | 50 | 32 | 0.534642 | 0.432551–0.629520 | 20,000 | 20,000 |
| ≥3 | primary | 163 | 47 | 48 | 30 | **0.563096** | **0.444859–0.671997** | 20,000 | 20,000 |
| ≥3 | inclusive | 166 | 47 | 50 | 30 | 0.548900 | 0.432560–0.657714 | 20,000 | 20,000 |

Primary shift from the published endpoint: **+0.023095** at ≥2 and **+0.036273** at ≥3. Inclusive
shift: −0.009492 and +0.004766. Of the 79 primary positives, **58 survive at ≥2 and 47 at ≥3**; the
21 lost at ≥2 all have exactly 1 called condition from a single strain and a mean distance of
**34.3945 Å** against a primary cohort mean of **30.7487 Å**. Median distance among primary positives
falls 26.233 → 25.932 → 25.631 Å and among negatives 31.827 → 30.462 → 30.656 Å.

Strict-consensus replicate rule (`all`), sensitivity only. The published rule is `avg`
(replicate-averaged count > 0); `any` is algebraically identical to `avg` on all 166 rows at all three
thresholds and is not a separate result. `all` differs on exactly one substitution, P43565 S1764A,
whose three strains have 16, 0 and 8 called conditions.

| Endpoint | Arm | n | Positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|
| ≥1 | primary | 163 | 78 | 0.535294 | 0.426684–0.637653 | 20,000 | 20,000 |
| ≥1 | inclusive | 166 | 81 | 0.552505 | 0.443268–0.654998 | 20,000 | 20,000 |
| ≥2 | primary | 163 | 57 | 0.559583 | 0.460937–0.651591 | 20,000 | 20,000 |
| ≥2 | inclusive | 166 | 57 | 0.544182 | 0.444647–0.636630 | 20,000 | 20,000 |
| ≥3 | primary | 163 | 46 | 0.574322 | 0.460573–0.679588 | 20,000 | 20,000 |
| ≥3 | inclusive | 166 | 46 | 0.559964 | 0.447419–0.665008 | 20,000 | 20,000 |

Allowed: that all six `avg`-rule intervals contain 0.5; that the primary/inclusive ordering reverses
at ≥2 because the three annotation-coincident 0 Å rows each carry exactly one called condition and
flip to negatives there. Not allowed: a paired test or difference interval across endpoints — the
three endpoints share all 163 rows and differ only in labels, `paired_auc_difference` does not apply,
and none was computed. Not allowed: presenting ≥2 or ≥3 as a competing primary result, or reporting
the `all` rule without stating that it changes the published ≥1 label of P43565 S1764A.

### 18.2 Direction-specific endpoints (RR-44)

Per-strain predicates: direction-agnostic `qvalue < 0.05`; defect-specific `qvalue < 0.05 AND
Score < 0`; enhancement-specific `qvalue < 0.05 AND Score > 0`. Join: 17,214 strain-condition rows,
169 strains, 166 substitutions, 102 conditions. Of the 18,720 called rows in the source table,
**14,637 have Score < 0 and 4,083 Score > 0; no row has Score exactly 0** and no Score or qvalue is
missing, so the two direction-specific counts partition the called conditions exactly. Rebuilding the
direction-agnostic label through this path reproduces `has_pheno` on all 166 rows and matches
`raw_q05_mean_per_strain` to machine zero.

| Arm | Endpoint | n | Proteins | Positive | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | Direction-agnostic (published) | 163 | 48 | 79 | 0.5268234 | 0.416106–0.630551 | 20,000 | 20,000 |
| Primary | **Defect-specific** | 163 | 48 | **66** | **0.5046860** | **0.395574–0.604167** | 20,000 | 20,000 |
| Primary | Enhancement-specific | 163 | 48 | 60 | 0.5428803 | 0.434432–0.647714 | 20,000 | 20,000 |
| Inclusive | Direction-agnostic (published) | 166 | 50 | 82 | 0.5441347 | 0.434521–0.647659 | 20,000 | 20,000 |
| Inclusive | **Defect-specific** | 166 | 50 | **69** | **0.5262214** | **0.418308–0.627313** | 20,000 | 20,000 |
| Inclusive | Enhancement-specific | 166 | 50 | 60 | 0.5275157 | 0.416943–0.632647 | 20,000 | 20,000 |

Label overlap — primary (163): defect+/enh+ 47, defect+/enh− 19, defect−/enh+ 13, defect−/enh− 84.
Inclusive (166): 50, 19, 10, 87. The three annotation-coincident 0 Å substitutions are all
defect-positive and none is enhancement-positive.

Dominance among the 79 primary-cohort positives, computed on called conditions only:
**46 defect-dominant, 25 enhancement-dominant, 8 exact ties.** Purity of the same 79: 19 defect-only,
13 enhancement-only, 47 called in both directions. The 8 ties are all single-replicate strains with
equal called defect and enhancement counts (ENO1 S188 3v3, SAT4 S155 3v3, SKY1 S445 2v2, and SNF1
T487, VMA2 S503, GCN5 S64, SKY1 S427, MYO5 S359 at 1v1).

Allowed: that the defect-specific endpoint moves the primary estimate **0.0221374 toward chance**,
not away from it; that the enhancement-specific arm is nominally highest at 0.5428803, contrary to
the mechanistic prediction, and equally uninformative at an interval of 0.434–0.648.
Not allowed: a paired interval on the direction contrast — the frozen `paired_auc_difference` holds
the label fixed and varies the score, and here the score is fixed and the label changes; the
difference is a difference of point estimates with two marginal intervals, and those marginals
overstate the uncertainty in the difference because the endpoints share 163 rows and 47 positives.
Not allowed: quoting **25 of 79** without the tie count. The same data give 25 excluding ties, 33
under `mean_enhance >= mean_defect`, and 13 counting only sites with no called defect condition.
**R3's "18 of 79 enhancement-dominant" is superseded.** Its rule was `sscore_max > -sscore_min` over
all 102 conditions, which ignores whether the extreme condition was called; the two classifications
disagree on 16 of 79 sites.

### 18.3 Comparator predictor table (RR-30 / RR-58)

Primary cohort, **n = 163 sites, 79 positive, 48 proteins**. All eight predictors are complete on all
163 rows; there is no missingness and every paired comparison runs on the full 163. Each predictor is
signed so that increasing score is the direction hypothesised to favour a screen-positive label.

| # | Predictor | Orientation | AUC | 95% CI | Nom / Ret | Δ vs `min_dist_A` | Δ 95% CI | Δ Nom / Ret |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | min \|pos − target pos\|, eligible ACT_SITE+BINDING set | smaller → positive | 0.5498041 | 0.4340705–0.6526297 | 20,000 / 20,000 | +0.0229807 | −0.0493801–+0.0902666 | 20,000 / 20,000 |
| 2 | \|pos − nearest_feat_pos\| | smaller → positive | 0.5333785 | 0.4155022–0.6391447 | 20,000 / 20,000 | +0.0065552 | −0.0837502–+0.0933298 | 20,000 / 20,000 |
| 3 | protein_length | larger → positive | 0.5493520 | 0.4437905–0.6596845 | 20,000 / 20,000 | +0.0225286 | −0.1587298–+0.2154142 | 20,000 / 20,000 |
| 4 | site pLDDT | larger → positive | 0.5551537 | 0.4636676–0.6407907 | 20,000 / 20,000 | +0.0283303 | −0.0667389–+0.1313505 | 20,000 / 20,000 |
| 5 | inverse relative solvent accessibility | smaller rsa → positive | 0.5866486 | 0.4890610–0.6719103 | 20,000 / 20,000 | +0.0598252 | −0.0413001–+0.1619905 | 20,000 / 20,000 |
| 6 | n_annot_residues | larger → positive | 0.5553797 | 0.4701127–0.6485676 | 20,000 / 20,000 | +0.0285564 | −0.0822575–+0.1522954 | 20,000 / 20,000 |
| 7 | raw_conditions (bookkeeping negative control) | larger → positive | 0.4615732 | 0.4259259–0.4957457 | 20,000 / 20,000 | −0.0652502 | −0.1832897–+0.0574866 | 20,000 / 20,000 |
| 8 | **min_dist_A (declared predictor)** | smaller → positive | 0.5268234 | 0.4161065–0.6305512 | 20,000 / 20,000 | 0 (reference) | not reported | — |

Allowed: that **no comparator's AUC interval excludes 0.5 except the negative control, and no paired
difference against `min_dist_A` excludes zero**; that the largest point difference is inverse RSA at
+0.0598 with interval −0.0413–+0.1620.
Not allowed: reading `raw_conditions` as anti-predictive. The variable takes five values on the
cohort and 155 of 163 sites share the value 102, so almost every pair is tied and contributes exactly
0.5; the point estimate is pinned near 0.5 by construction and the narrow interval reflects
near-constancy, not precision. The exclusion of 0.5 is stable to seed (upper bounds 0.4954, 0.4955,
0.4963, 0.4957 at seeds 20260729, 1, 12345, 999999) and is driven by **8 of 163 sites**; its paired
difference against distance does include zero. Report it as a tie-structure artifact.
Not allowed: shipping rows 3, 4, 6 or 7 without stating their orientation on the face of the table.
For those four there is no prior fixing the direction; larger → positive was chosen because it
reproduces every prior spot check. Flipping maps AUC to 1 − AUC; every conclusion is unchanged except
that `raw_conditions` would read 0.5384 (CI 0.5043–0.5741).
Not allowed: citing row 1 and row 2 as the same quantity. Row 1 minimises sequence separation over
all eligible targets; row 2 reads the sequence separation of whichever target is nearest in 3D. They
differ by 0.0164 in AUC.

### 18.4 Permutation null for the primary estimand (RR-16)

20,000 permutations per scheme, seed 20260728, `numpy.random.default_rng`. Observed AUC recomputed
with the frozen `auc_from_ranks` is **0.5268233875828813**, identical to `results/statistics.json`.

| Quantity | (a) Unrestricted across 163 | (b) Within protein |
|---|---:|---:|
| null mean | 0.5001785940 | 0.5119963382 |
| null SD | **0.0452408316** | **0.0304784446** |
| 2.5th percentile | 0.4106351718 | 0.4531344183 |
| 97.5th percentile | 0.5883062086 | 0.5726341169 |
| full range | 0.32881–0.68324 | 0.39828–0.64241 |
| two-sided p, `(b+1)/(n+1)` | **0.5547722614** (about 0.5) | **0.6300184991** (about the null mean) |
| two-sided p, raw | 0.55475 (11,095 / 20,000) | 0.6300 (12,600 / 20,000) |
| z about the null center | 0.5889545488 | 0.4864765774 |

(b) permutes labels only within an accession. 23 of 48 proteins carry both labels (112 of 163
substitutions); the other 25 proteins (51 substitutions) are single-label and are held fixed by
construction. The (b) null is centered at 0.51200, not 0.5, because between-protein pairs are fixed;
the p-value to quote for (b) is the mean-centered 0.6300, and the 0.4137 figure centered on 0.5 is
recorded only to show that the choice of center does not approach significance either.

Family-size context. The declared post hoc families total **255** estimates: confidence strata
11 × 2 arms = 22, PAE grids 72 × 3 cohorts = 216, feature definitions 5, cohort/residue sensitivities
7, continuous outcomes 5. At 255 estimates, 12.75 are expected to clear p < 0.05 by chance.

| | Unrestricted null | Within-protein null |
|---|---:|---:|
| median of max \|AUC − null mean\| over 255 draws | 0.1351836230 | 0.0915298825 |
| 95th percentile of that max | 0.1583270141 | 0.1124580671 |
| implied largest AUC seen by chance (median / 95th) | 0.6354 / 0.6585 | 0.6035 / 0.6245 |

Allowed: that the observed AUC is indistinguishable from chance under both schemes, sitting 0.59 (a)
or 0.49 (b) null SDs from its null center; that a post hoc subgroup AUC of roughly 0.64 (unrestricted)
or 0.60 (clustered) is the *typical* maximum a family of 255 null estimates produces, so any post hoc
AUC below those values carries no evidence once the family is counted.
Not allowed: quoting 0.410–0.588 as the null *range*. Those are the 2.5/97.5 percentiles of (a); the
full range is 0.32881–0.68324. **R1's "range 0.410–0.588" is mislabelled** and understates the null's
extremes by 0.082 low and 0.095 high, which matters exactly where it is used.
Not allowed: quoting either range to three decimals. A min/max over 20,000 draws moves with seed by
order 0.01 and is the least stable statistic in this subsection. The p-values are stable to the second
decimal (Monte Carlo SE 0.0035 at 20,000 permutations) and the SDs to ~0.0002.
Not allowed: treating the 255 family estimates as independent — the PAE grid cells are heavily
overlapping subsets, so this calculation overstates the spread and is a conservative bound.

### 18.5 SIFT missingness and the extremal bound (RR-14)

| Group | n | Proteins | Positive | Outcome rate | Median distance (Å) | Q1–Q3 (Å) |
|---|---:|---:|---:|---:|---:|---|
| SIFT observed | 152 | 48 | 71 | 0.4671052632 | 28.5204000473 | 13.8941791058–42.5678787231 |
| SIFT missing | 11 | 6 | 8 | 0.7272727273 | 51.7973747253 | 19.0996208191–61.1196002960 |
| All primary | 163 | 48 | 79 | 0.4846625767 | 28.9301929474 | 13.7443852425–43.4403667450 |

The 11 unscored substitutions come from **6 proteins** (P06782 ×3, P16140 ×3, P32561 ×2, P32485,
P47116, Q04439). The probability that a randomly chosen missing site is farther from core than a
randomly chosen scored site is **0.6543062201**. Distance AUC on the 152-row common support is
0.5317336115; on all 163 rows it is 0.5268233876 [0.4161064594, 0.6305511618], 20,000 / 20,000
retained — **0.0049 lower**, so the common-support restriction runs mildly in distance's favour.

Extremal bound, seed 20260728. Both bounds impute the 11 missing SIFT values at the extremal rank
conditional on outcome; because AUC depends only on ranks these are the logical minimum and maximum
attainable by any imputation whatsoever.

| Case | n | SIFT AUC | SIFT − distance | 95% CI | Nominal | Retained |
|---|---:|---:|---:|---:|---:|---:|
| Published common support (Section 10) | 152 | 0.6061554512 | 0.0744218397 | −0.0368868449–+0.1915291204 | 20,000 | 20,000 |
| Least favourable for SIFT | 163 | 0.5253164557 | **−0.0015069319** | −0.1193531746–+0.1250491696 | 20,000 | 20,000 |
| Most favourable for SIFT | 163 | 0.6586799277 | **+0.1318565401** | +0.0243755261–+0.2477263488 | 20,000 | 20,000 |

The bound on the point estimate is **−0.002 to +0.132**, containing the published 0.074.

Allowed: that the manuscript's reading — proximity to a core annotation carries no discriminative
advantage over a sequence-constraint baseline — is not sensitive to the 11 missing scores; that the
missingness must be disclosed with its direction (11 of 163, enriched for positives at 0.727 vs 0.467
and for long distances at 51.80 vs 28.52 Å, and mildly favourable to distance).
Not allowed: reporting the extremal range as a plausible-data interval. It is a logical bound; any
distributional imputation lies strictly inside it. Not allowed: reading the most-favourable case as
evidence that SIFT wins — its interval excludes zero only under a construction requiring all 8
unscored positives to be more constrained than every one of the 152 scored sites and all 3 unscored
negatives less constrained than every one of them simultaneously. Not allowed: reusing the imputed
`sift_ala_score_inv` columns for any non-rank statistic; the imputed values sit outside the observed
support (−1.0 to 0.0, 124 distinct values among 152). Not allowed: quoting the bound endpoints to
three decimals — with 6 proteins carrying all 11 missing rows, a cluster resample takes a missing
protein's whole block or none of it, so read them to two.

### 18.6 Sequence-adjacency sensitivity (RR-29)

`dpos` = `|pos - nearest_feat_pos|`; sequence-adjacent is `dpos <= 2`. `min_dist_A` equals
`dist_core_A` and `nearest_feat_pos` equals `nearest_core_pos` on all 166 rows.

**Of the 10 primary substitutions at ≤5 Å, 5 sit at 1.3296–1.3419 Å with `dpos` = 1** — PDA1 S313
1.3296478987, YCR087C-A T49 1.3308113813, VMA2 S380 1.3399593830, INO1 S368 1.3408930302, HSP82 S379
1.3419464827 — and a sixth (YCR087C-A S53, 3.6046917439 Å) has `dpos` = 2. That 1.33 Å cluster is the
C–N peptide bond: an i±1 neighbour has a fixed backbone contact distance and the minimum-atom-pair
distance cannot exceed it. Their outcomes are 2 positive / 3 negative. The remaining four sub-5 Å
substitutions have `dpos` = 38, 38, 70, 224 and are 2 positive / 2 negative. Cohort `dpos`
distribution (primary, n = 163): 5 rows at 1, 1 at 2, 157 at ≥ 3, and **no row between 3 and 37**.

| Arm | Filter | n | Proteins | Positive | Negative | AUC | 95% CI | Nominal | Retained |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| primary | all | 163 | 48 | 79 | 84 | 0.526823 | 0.416106–0.630551 | 20,000 | 20,000 |
| primary | `dpos` > 2 | 157 | 48 | 77 | 80 | **0.540584** | **0.428570–0.648366** | 20,000 | 20,000 |
| inclusive | all | 166 | 50 | 82 | 84 | 0.544135 | 0.434521–0.647659 | 20,000 | 20,000 |
| inclusive | `dpos` > 2 | 157 | 48 | 77 | 80 | 0.540584 | 0.428570–0.648366 | 20,000 | 20,000 |

Descriptive cutoff table, `dpos` > 2, primary cohort. The "beyond" columns are unchanged from
Section 6 because the filter removes nothing beyond 5 Å.

| Cutoff | n within | Positive within | Rate within | n beyond | Positive beyond | Rate beyond | Descriptive OR |
|---:|---:|---:|---:|---:|---:|---:|---:|
| ≤5 Å | 4 | 2 | 50.00% | 153 | 75 | 49.02% | 1.040 |
| ≤8 Å | 14 | 10 | 71.43% | 143 | 67 | 46.85% | 2.836 |
| ≤10 Å | 24 | 15 | 62.50% | 133 | 62 | 46.62% | 1.909 |
| ≤15 Å | 37 | 22 | 59.46% | 120 | 55 | 45.83% | 1.733 |

Allowed: the defensible manuscript sentence — the sub-5 Å bin is dominated by i±1 sequence neighbours
at the fixed C–N peptide-bond distance, and both the AUC and the descriptive cutoff table are
insensitive to their removal (**primary AUC 0.541, 95% CI 0.429–0.648, n = 157 in 48 proteins, 77
positive, 20,000 / 20,000 retained**). Allowed: that the published 5 Å inversion (rate 0.400 within
against 0.490 beyond, OR 0.693) is produced entirely by peptide-bond-adjacent pairs and becomes
2 of 4, OR 1.040, once they are removed — a cleaner null, not a weaker or stronger one.
Not allowed: presenting the two filtered rows as two arms agreeing. The three substitutions that
separate the arms are the annotation-coincident ones and all three have `dpos` = 0, so the filter
collapses both arms onto the **same 157 substitutions in 48 proteins**; it is one number reported
twice. Not allowed: any inferential claim on the 4-substitution 5 Å bin — report the count, not a
rate. Not allowed: describing `dpos <= 2` as data-determined; any threshold between 3 and 37 gives the
identical 157-row cohort, so the result is robust within that window, but the threshold is post hoc.

### 18.7 Bootstrap draw retention (RR-13)

217 stored interval records across `results/` and `phase0_5/results/`: 167 from a resampling
estimator, 50 analytic logistic (Wald / cluster-robust) intervals involving no draws.

**Both canonical 200,000-draw arm intervals retained all 200,000 draws — zero discarded.**

| Arm | Unit | Estimate | 95% interval | Nominal | Retained | Shortfall |
|---|---|---:|---:|---:|---:|---:|
| Primary, 163 / 48 / 79 positive | protein cluster | 0.5268233876 | 0.4167443197–0.6315393408 | 200,000 | 200,000 | 0 |
| Inclusive, 166 / 50 / 82 positive | protein cluster | 0.5441347271 | 0.4357555293–0.6487455197 | 200,000 | 200,000 | 0 |
| Primary, naive site | site | 0.5268233876 | 0.4367346939–0.6173687783 | 200,000 | 200,000 | 0 |
| Inclusive, naive site | site | 0.5441347271 | 0.4553844563–0.6327034884 | 200,000 | 200,000 | 0 |

**Table S-RR13a. Six sensitivity intervals retained fewer than their nominal 20,000.** These are six
distinct quantities, each stored twice (once in `phase0_5_statistics.json`, once in the matching CSV).

| Quantity | n sites / proteins / positive | AUC | 95% interval | Nominal | Retained | Shortfall | Discarded | Endpoint at 1 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `cohort_sensitivity` primary_tyrosine_only | 16 / 12 / 12 | 0.6041666667 | 0.2718831169–1.000 | 20,000 | **19,335** | 665 | 3.325% | **yes** |
| `residue_class_sensitivity` Y | 16 / 12 / 12 | 0.6041666667 | 0.2666666667–1.000 | 20,000 | **19,404** | 596 | 2.980% | **yes** |
| `confidence_strata` exclude / site_plddt_ge_90 | 35 / 16 / 22 | 0.5699300699 | 0.3707423529–0.7464123377 | 20,000 | 19,999 | 1 | 0.005% | no |
| `confidence_strata` exclude / very_high_confidence_joint | 27 / 13 / 15 | 0.6833333333 | 0.4807692308–0.8640098765 | 20,000 | 19,999 | 1 | 0.005% | no |
| `confidence_strata` include / site_and_target_plddt_ge_90 | 31 / 15 / 19 | 0.6973684211 | 0.5357142857–0.8421052632 | 20,000 | 19,997 | 3 | 0.015% | no |
| `confidence_strata` include / very_high_confidence_joint | 30 / 15 / 18 | 0.7361111111 | 0.5530303030–0.9027777778 | 20,000 | 19,999 | 1 | 0.005% | no |

No stored interval endpoint anywhere touches 0.

**Amendment required to Section 12.** The two tyrosine records are the same 16 sites (12 proteins, 12
positive, 4 negative) estimated twice under different seed offsets — same point estimate, different
lower endpoints, different retention. Both have an upper endpoint of exactly 1.000, which is the AUC
boundary being hit by resamples in which the four negatives collapse, not an estimate of the sampling
limit. Under the declared convention **neither may be reported as an interval.** Reader-facing text
must read:

> Tyrosine sites: AUC 0.604 (16 sites in 12 proteins; 12 phenotype-positive, 4 negative). No interval
> is reported — the protein-cluster bootstrap upper endpoint reaches the boundary value of 1, and
> 3.3% (665 / 20,000) of resamples were discarded for containing a single outcome class.

Not allowed: printing 0.604 [0.267, 1.000] or 0.604 [0.272, 1.000]. Not allowed: presenting the
tyrosine-only cohort AUC and the residue-class-Y AUC as two results; they are one quantity computed
twice.

**Provenance rule for the `draws` field.** `phase0_5/src/02_phase0_5_analysis.py::bootstrap_auc` and
`paired_auc_difference` return `"draws": len(draws)`, the count *after* discarding single-class
resamples, so every `draws` value under `phase0_5/results/` is a measured retained count.
`src/03_analysis.py::boot_auc` returns only `(point, lo, hi)`, and `results/statistics.json` then
writes `"draws"` and `"naive_site_draws"` as the literal constant `N_PRIMARY_BOOT`; those 200,000
entries, and the same literals in `results/cohort_arm_primary_estimates.csv`, are **nominal, not
measured**. They are correct — the phase-0.5 recomputation of the identical quantity at the same seed
offset gives the same estimate and endpoints to full precision with a true retained count of
200,000 — but cite `phase0_5_statistics.json`, not `results/statistics.json`, for any retention claim.

Three undocumented-retention gaps, none of which changes a number: 16 records in
`results/statistics.json` (`auc_other_predictors` for pLDDT, RSA and `n_annot_residues`, plus
`sift_comparator`, across four duplicated cohort blocks) store an interval with no draw count at all,
nominal 20,000 by the `boot_auc` default and retention unrecoverable without a rerun;
`phase0_5/results/sift_comparator_sensitivity.csv` has no `draws` column, though the same nine
intervals in `phase0_5_statistics.json` carry 20,000 with zero shortfall; and 11
`cluster_boot_spearman` records (`continuous_outcomes`, `confidence_correlations`) at a nominal 4,000
draws store no retained count and silently drop non-finite ρ. If the supplement quotes those
correlation intervals, their retention is undocumented.

### 18.8 Predictor benchmark, both summaries (RR-59)

10 repeated stratified group 5-fold splits, n = 163, 79 positive. The pooled column was independently
re-derived from the stored out-of-fold predictions in
`phase0_5_analysis_with_oof_predictions.csv` using the frozen `auc_from_ranks`; all five agree to
every printed digit.

| Model | Features | Split-averaged AUC | 2.5–97.5 pct over 10 repeats | Pooled OOF AUC | Pooled − split | Brier |
|---|---|---:|---:|---:|---:|---:|
| constant_prevalence | none | 0.5000000000 | 0.500000–0.500000 | 0.5000000000 | 0.0000000000 | 0.2497647634 |
| distance_only | logd | 0.4836766942 | 0.4127008753–0.5267466119 | **0.3925557565** | **−0.0911209377** | 0.2583952944 |
| structural | logd; plddt; rsa; pae_pair_max; log_n_annot | 0.5579874728 | 0.5185344010–0.6066437347 | 0.5230560579 | −0.0349314149 | 0.2588919486 |
| published_annotations | supp_is_disopred; age_ordinal; has_uniprot_domain; sift_ala_score_inv; PWM_nkinTop01 | 0.5896358605 | 0.5558254359–0.6398948737 | 0.5732368897 | −0.0163989708 | 0.2524937894 |
| combined | all ten of the above | 0.5869982934 | 0.5321894181–0.6241394352 | 0.5688667872 | −0.0181315062 | 0.2592420171 |

**Amendment required to Section 12.** The pooled AUC is lower than the split-averaged estimate for
all four fitted models, by 0.016 to 0.091, and the gap is structural rather than noise: the
split-averaged number is the mean over 10 repeats of a pair-weighted average of five per-fold AUCs, so
it never compares a case in fold 1 against a case in fold 4; the pooled number ranks all 163
out-of-fold predictions against each other and additionally penalizes fold-to-fold shifts in the
predicted probability scale. Section 12 currently reports only the split-averaged values
(distance only 0.484, structural 0.558, source annotations 0.590, combined 0.587) and must carry both.

Allowed: that the model ordering is identical under both summaries — `published_annotations` >
`combined` > `structural` > `distance_only`; that adding the five structural features to the five
published annotations improves neither summary (−0.0026 split-averaged, −0.0044 pooled) and worsens
the Brier score (0.2524938 → 0.2592420).
Not allowed: reporting the split-averaged value alone. It overstates every model.
Not allowed: claiming from **0.3926** that distance performs below chance. No interval is stored for
any pooled figure and no protein-cluster bootstrap interval exists for any benchmark model. The
correct statement is that the sign of the distance effect flips between the pooled cross-validated
ranking (0.393) and the primary arm AUC (0.527, interval spanning 0.5), and neither is precise enough
to settle it.
Not allowed: labelling `split_low` / `split_high` a 95% confidence interval. They are the 2.5th and
97.5th percentiles of **10** repeat values, interpolated between extreme order statistics, and
describe the repeated-splitting procedure rather than sampling uncertainty about the population AUC.

### 18.9 Characterization of the annotation target set (RR-28)

A record is *experimental* if its evidence-code set intersects {ECO:0000269, ECO:0007744}. Everything
else — ECO:0000255, ECO:0000250, ECO:0000305, or no code — is non-experimental. Codes are unioned over
all records covering a residue.

Evidence of the nearest target actually used, n = 163: ECO:0000255 **101**, ECO:0000250 **33**,
ECO:0000269;ECO:0007744 **12**, ECO:0000305 **8**, ECO:0000269 **4**, ECO:0000305;ECO:0007744 **3**,
ECO:0000250;ECO:0000269;ECO:0007744 **1**, none **1**. **Experimental 20 / 163 (12.3%);
non-experimental 143 / 163 (87.7%).**

Expanded-residue level, **533 eligible target residues on the 48 primary-cohort proteins** (matches
the sum of `n_annot_residues` over those 48): ECO:0000255 313, ECO:0000250 120,
ECO:0000269;ECO:0007744 55, ECO:0000269 15, ECO:0000305;ECO:0007744 15,
ECO:0000250;ECO:0000269;ECO:0007744 7, ECO:0000305 5, ECO:0000250;ECO:0000255 2, none 1.
**Experimental 92 / 533 (17.3%); non-experimental 441 / 533 (82.7%).** 21 of 533 residues are covered
by more than one record.

Composition of the target set: **ATP is the nearest-target ligand for 86 of 163 substitutions
(52.8%)**, 87 under a permissive reading of the single ADP;AMP;ATP row. BINDING interval widths have
median 1 and maximum 9; **33 records of width ≥ 8 contribute 289 of the 533 eligible residues
(54.2%)**. **24 of the 48 primary-cohort proteins (50%)** are protein kinases or protein-kinase-complex
subunits by UniProt protein name — 23 catalytic kinases plus SNF4, the AMPK gamma regulatory subunit —
which is the direct cause of the ATP dominance.

Restricting each protein's eligible set to experimentally-evidenced residues:

| Quantity | Value |
|---|---:|
| substitutions retaining any target | **24 of 163 (14.7%)** |
| substitutions losing every target | **139** |
| proteins retaining any target | **7 of 48** |
| retained class balance | 11 positive / 13 negative |
| retained substitutions at distance 0 | 0 |
| median distance, retained positives | 20.191083908 Å |
| median distance, retained negatives | 21.811134338 Å |
| rows whose nearest target was already experimental | 20 of 24 |
| mean per-row distance increase | 1.273656805 Å (median 0, max 14.142353058 Å) |

| Estimate | n | Proteins | AUC | 95% CI | Nominal | Retained |
|---|---:|---:|---:|---:|---:|---:|
| Experimental-only targets | 24 | 7 | **0.4195804196** | 0.2435897436–0.7083333333 | 20,000 | **19,991** |
| Same 24 rows, full-annotation distance | 24 | 7 | 0.4405594406 | 0.2283950617–0.7666666667 | 20,000 | **19,991** |
| Paired difference, experimental − full | 24 | 7 | −0.0209790210 | −0.1666666667–+0.0495867769 | 20,000 | **19,991** |

Per-protein composition of the retained 24: ENO1 (P00924) 4 substitutions / 1 positive / 12 target
residues / median 11.64 Å; HSP82 (P02829) 6 / 3 / 16 / 37.25; RPO21 (P04050) 2 / 0 / 11 / 46.03;
INO1 (P11986) 4 / 2 / 27 / 20.48; SNF4 (P12904) 3 / 0 / 8 / 21.81; EFT1;EFT2 (P32324) 3 / 3 / 15 /
31.05; HOG1 (P32485) 2 / 2 / 3 / 16.48.

Recomputation validity: distances for the restricted set were recomputed from the cached AlphaFold
models in `data/af/` under the same atom–atom minimum-distance rule as `src/02_structures.py`, because
the frozen tables store only distance to the nearest target under the full annotation set. Reproducing
the full-set distances first gave a maximum absolute deviation of **1.42e-14 Å** over all 163 rows and
`nearest_feat_pos` agreement on **163 / 163**.

Allowed, and this is the reportable finding: **the published near-null AUC cannot be attributed to
annotation quality, because the design cannot be run on high-quality annotation at all.** Under an
experimentally-evidenced-only target set it loses 85% of its substitutions and 41 of 48 proteins.
Allowed: that 87.7% of the nearest targets actually used are non-experimental and 54.2% of the
eligible residues come from 33 wide interval annotations, so the quantity being measured is, for most
rows, distance to a rule-propagated ATP-region boundary.
Not allowed: reading 0.4196 as evidence of anti-discrimination. The interval spans 0.24–0.71 on 7
resampling units and is compatible with anything from strong anti-discrimination to moderate
discrimination; percentile endpoints from 7 clusters are coarse. Treat it as a descriptive range.
Not allowed: quoting the experimental count at the nearest-target level without stating the rule. It
is **20** under the union-of-covering-records rule and **19** if the single triple-covered residue is
assigned to its ECO:0000250 record; that one row is the only ambiguous case (`n_covering_records` > 1
for 1 of 163, maximum 3). Similarly, item 6's restriction is applied permissively at the record level
— a residue is experimental if *any* covering record carries ECO:0000269/ECO:0007744; requiring every
covering record to be experimental would retain fewer than 24.

### 18.10 Bookkeeping discrepancy against Section 4

Section 4 states "**564** feature-residue rows representing **560** unique residues". The 560 unique
residues reproduce exactly. The 564 does not: expanding all 262 eligible ACT_SITE + BINDING records
gives **594** record-residue rows (BINDING 553 + ACT_SITE 41); de-duplicating on (acc, start, end)
gives **565**, and on (acc, start, end, feat_type) gives **566**. No simple rule reproduces 564. The
excess over 560 comes from P12904, whose 221–222 and 309–312 intervals are each recorded three times
(ADP, AMP, ATP ligands). The unique-residue count — the quantity that defines the target set — is
unaffected, and the eligible record counts (41 active site, 221 binding site, 262 total, from 278
records in `results/uniprot_features_detailed.csv`, excluding 8 `Site` and 8 `DNA binding`) reproduce
exactly. **Section 4's 564 must be corrected or its derivation stated;** until then no artifact may
cite it.

### 18.11 Additions to the Section 13 claim rules

Allowed, on the strength of Sections 18.1–18.9:

- The near-chance primary reading survives stricter outcome endpoints (≥2 and ≥3 called conditions)
  and a defect-specific direction endpoint. Every one of those intervals contains 0.5.
- The primary/inclusive ordering reverses at the ≥2 endpoint, which supports excluding
  annotation-coincident substitutions from the primary cohort.
- No comparator predictor, and no cheap sequence or structural baseline, is distinguishable from
  chance or from `min_dist_A` on the primary cohort.
- The primary AUC is indistinguishable from chance under both an unrestricted and a within-protein
  permutation null.

Not allowed, added:

- Reporting the tyrosine AUC with an interval (see 18.7).
- Reporting a benchmark model's split-averaged AUC without its pooled counterpart (see 18.8).
- "Distance performs below chance" from the pooled 0.3926 (see 18.8).
- "The null is an artifact of annotation quality" — 18.9 shows the design cannot be run on
  experimental annotation at all, which is a different and stronger statement.
- "The stricter endpoint improves discrimination" — the ≥3 interval is wider than the ≥2 interval and
  any change in ranking is bought with precision.
- Any paired difference across endpoints (18.1) or across outcome directions (18.2). No estimator for
  either contrast exists in the frozen module and none was written.
- Citing Section 4's "564 feature-residue rows" (see 18.10).

<!-- END PROPOSED SECTION 18 -->

---

## 4. What changed and what did not

### Changed against pre-existing published values

| Item | Published | Round-2 | Consequence |
|---|---|---|---|
| Tyrosine AUC interval, §12 | 0.604 [0.267, 1.000] and [0.272, 1.000] | retained 19,404 and 19,335 of 20,000; both upper endpoints at the AUC boundary | Both must be reported as a point estimate with counts and no interval. Reader-facing change. |
| Predictor benchmark, §12 | split-averaged only: distance 0.484, structural 0.558, annotations 0.590, combined 0.587 | pooled OOF: 0.392556, 0.523056, 0.573237, 0.568867 | Both summaries must be carried. The sign of the distance effect flips between pooled CV and the primary arm. |
| Feature-residue rows, §4 | 564 | 594 raw / 565 or 566 de-duplicated; not reproducible | Correct or derive; 560 unique residues stands. |
| R3's dominance figure | 18 of 79 enhancement-dominant | 46 defect / 25 enhancement / 8 ties | R3's rule ignored whether the extreme condition was called; the two disagree on 16 of 79. |
| R1's permutation null | "range 0.410–0.588" | those are the 2.5/97.5 percentiles; the range is 0.32881–0.68324 | R1's figure understates the null's extremes by 0.082 low and 0.095 high. |
| Annotation-quality attribution | open question | 24 of 163 substitutions in 7 of 48 proteins survive an experimental-only target set | The attribution is foreclosed, not answered. |
| §12 tyrosine duplication note | already flags Monte Carlo variation | the two records differ in retention (19,335 vs 19,404) as well as seed | The retention difference has the same cause as the boundary saturation. |

### Unchanged

- **Primary estimand.** AUC 0.5268233875828813 reproduced exactly by RR-43, RR-44, RR-16, RR-29,
  RR-14 and RR-13; the 200,000-draw interval 0.4167443197–0.6315393408 reproduced exactly at seed
  `SEED + 1`, **200,000 / 200,000 retained**.
- **Inclusive sensitivity.** 0.5441347270615563, interval 0.4357555293–0.6487455197,
  **200,000 / 200,000 retained**.
- **Both naive site-bootstrap intervals**, 200,000 / 200,000 retained.
- **Every confidence-strata point estimate** in §8, and every published cutoff-table row in §6
  (reproduced by RR-29's "all" rows).
- **SIFT comparator**, §10: 0.606155, distance 0.531734, difference 0.074422 on the 152-row common
  support — RR-14 reproduces all three and shows the missingness runs mildly in distance's favour.
- **§4 target-set counts** other than 564: 41 active site, 221 binding site, 560 unique residues, the
  48/50-protein cohort structure.
- **§15 replicate rule**: the any-positive-replicate reading reproduces `has_pheno` on all 166 rows
  and `raw_q05_mean_per_strain` to machine zero (RR-43, RR-44).
- **§13's existing bans**, all of which survive; three are strengthened (distance is not uninformative;
  the inclusive arm is not primary; no post hoc subgroup below ~0.60–0.64 carries evidence).

---

## 5. Unstable, ambiguous, or contradictory

1. **Two published tyrosine intervals are not reportable under the project's own convention.** §12
   prints both; RR-13 shows both saturate at 1.000 with 2.98–3.33% of resamples discarded. This is a
   direct internal contradiction in the frozen release, not a new finding.
2. **§4's "564 feature-residue rows" is not reproducible by any simple rule.** RR-30/RR-58 gets 594,
   565 or 566; RR-28 independently gets 594. The two analyses agree with each other and disagree with
   the published file.
3. **The sign of the distance effect is not settled.** Primary arm 0.527 (interval spanning 0.5),
   pooled cross-validated 0.393, experimental-only-target 0.420, `raw_conditions` control 0.462.
   Nothing here resolves direction, and the pooled figure carries no interval at all.
4. **`raw_conditions` excludes 0.5 and should not.** Interval 0.4259–0.4957, stable across four seeds,
   driven by 8 of 163 sites in a variable where 155 of 163 share one value. It is a tie-structure
   artifact; its paired difference against distance does include zero.
5. **Predictor orientation is under-determined for four of eight comparators** (protein length, site
   pLDDT, target count, condition count). The chosen direction reproduces every prior spot check;
   flipping maps AUC to 1 − AUC and would make `raw_conditions` read 0.5384 [0.5043, 0.5741].
6. **The replicate rule is genuinely ambiguous at the published endpoint.** The strict-consensus
   reading changes the label of P43565 S1764A (strain counts 16, 0, 8) and shifts the primary AUC from
   0.526823 to 0.535294. The source sentence is a per-substitution existence claim, which favours the
   published `avg`/`any` reading, but the source does not settle it.
7. **"N of 79 enhancement-dominant" has three defensible values** — 25 excluding ties, 33 under
   `mean_enhance >= mean_defect`, 13 counting only sites with no called defect condition — because 8
   of the 79 are exact ties. Reporting one without the tie count is what made R3's approximation look
   precise.
8. **RR-29's two filtered rows are one number reported twice.** The primary and inclusive cohorts
   collapse onto the same 157 substitutions in 48 proteins under `dpos > 2`, because all three
   annotation-coincident rows have `dpos` = 0.
9. **Permutation range endpoints are seed-unstable** by order 0.01 and must not be quoted to three
   decimals. The p-values (SE 0.0035 at 20,000 permutations) and SDs (~0.0002) are stable.
10. **RR-28's nearest-target experimental count is 20 or 19** depending on whether one triple-covered
    residue is assigned by union or by single record. Both are reported; neither was chosen silently.
11. **RR-28's summary text contains an internal typo.** §6 reads "for 18 of 24 rows (20 of 24) the
    nearest target was already an experimentally-evidenced residue." Recomputed from
    `rr28_experimental_only_distances.csv`, the correct count is **20 of 24** (rows with zero distance
    change). Use 20; the parenthetical is right and the leading figure is wrong.
12. **Retention is undocumented for 27 stored intervals** — 16 with no draw field
    (`auc_other_predictors`, `sift_comparator`) and 11 `cluster_boot_spearman` records at a nominal
    4,000 draws. Recovering them requires a rerun, which no Round-2 analysis performed.
13. **`results/statistics.json` draw counts are nominal, not measured.** They happen to be correct for
    the four 200,000 rows, but only `phase0_5_statistics.json` can be cited as evidence of retention.
14. **Stricter endpoints buy precision with the estimate.** The ≥3 interval half-width is 0.114
    against 0.098 at ≥2, and positive-carrying proteins fall from 35 to 32 to 30 of 48, with 4 of the
    21 sites lost at ≥2 coming from MKK1 and 2 from MYO5 — the loss is not spread evenly across the
    resampling unit.
