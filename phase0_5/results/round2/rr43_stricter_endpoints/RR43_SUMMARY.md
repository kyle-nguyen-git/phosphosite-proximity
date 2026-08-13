# RR-43: Stricter Outcome Endpoints

## Summary

Raising the screen-positive endpoint from >= 1 called condition to >= 2 and >= 3 moves 21 of the 79 primary positives to the negative class at >= 2, and 32 of 79 at >= 3. The primary AUC rises monotonically (0.526823 -> 0.549918 -> 0.563096) and the inclusive AUC does not (0.544135 -> 0.534642 -> 0.548900). Every protein-cluster interval still spans 0.5 by a wide margin, so the conclusion of the calibration is unchanged: distance to the nearest core functional annotation does not usefully rank phosphosites by screen phenotype, at any of the three endpoints tested.

Files: `rr43_stricter_endpoints.py`, `rr43_endpoint_results.csv`, `rr43_endpoint_results.json` (all in this directory). Nothing in the frozen tree was written or modified.

## Provenance and conventions

All three frozen hashes verified before computation and matched:

- `results/statistics.json` = `57d02d5b…a0401`
- `results/analysis_final.csv` = `e666827d…ac4dd4`
- `phase0_5/results/phase0_5_statistics.json` = `3ea01c7b…f050d02b`

`phase0_5/src/02_phase0_5_analysis.py` guards `main()` behind `if __name__ == "__main__"`, so it was imported directly with `importlib` and executes definitions only. `auc_from_ranks` and `bootstrap_auc` are the frozen module's own functions; nothing was reimplemented.

- Resampling unit: UniProt accession (`acc`). Every substitution of a sampled protein is retained.
- Post hoc sensitivity intervals: 20,000 protein-cluster draws, seed 20260728 (the module's `SEED`).
- Score: `-dist_core_A`. Shorter distance is scored toward the screen-positive label.
- Retained draws (RR-13): **20,000 of 20,000 nominal for all 18 intervals below.** No resample drew a single outcome class, which is expected given that the smallest positive class here is 46-47 sites spread over 30 proteins.
- No interval endpoint touches 0 or 1, so all intervals are reported.

The published primary interval uses n=200,000 and seed `SEED+1`. Recomputing at those settings reproduces the frozen file exactly: primary AUC 0.5268233875828813, CI [0.4167443197407883, 0.6315393408472534]; inclusive AUC 0.5441347270615563, CI [0.4357555292879888, 0.6487455197132617]. The >= 1 rows in the table below differ from the published CI only in the draw count and seed offset declared for post hoc work.

**Endpoint handling.** Raising the threshold reclassifies former positives as negatives; it does not delete them. Cohort n stays at 163 (primary) and 166 (inclusive) at every endpoint. Dropping rather than reclassifying is a defensible alternative that I did not compute — flag it if you want it.

## The replicate rule

164 of the 166 substitutions map to exactly one strain, so the rule only has bite for two rows. Per-strain called-condition counts, recomputed from `EMS132528-supplement-Supplementary_Data_3.xlsx`:

| acc | substitution | strains | per-strain counts | mean |
|---|---|---|---|---|
| P32324 | T566A | PBY662; PBY663 | 12; 3 | 7.5 |
| P43565 | S1764A | PBY77; PBY78; PBY79 | 16; 0; 8 | 8.0 |

The recomputed mean reproduces `raw_q05_mean_per_strain` exactly (max absolute difference 0), and `raw_q05_mean_per_strain > 0` reproduces `has_pheno` for all 166 rows.

Three rules are distinguishable:

- **avg** — threshold the replicate-averaged count (`mean >= k`). This is the published operationalisation; at k=1 it is `mean > 0`.
- **any** — threshold per strain, positive if any member strain qualifies (`max >= k`).
- **all** — threshold per strain, positive only if every member strain qualifies (`min >= k`).

**avg and any agree on all 166 substitutions at all three thresholds.** At k=1 they are algebraically identical (mean > 0 iff any strain has >= 1), and both were verified to reproduce `has_pheno` exactly. At k=2 and k=3 the two replicated rows have per-strain maxima of 12 and 16, far above both thresholds, so no row separates them. The primary analysis below is therefore the avg rule, and the any rule is not a separate result.

**The all rule differs on exactly one substitution, P43565 S1764A, at every threshold including the published k=1** — because strain PBY78 has zero called conditions while PBY77 and PBY79 have 16 and 8. Under a strict-consensus reading that site is a negative in the published analysis too. It is one site out of 163, and it shifts the primary AUC by about +0.008 at each endpoint (it is a 51.5 A site currently labeled positive, so removing it from the positive class helps the score). The all-rule numbers are in the results table for completeness. I do not think consensus-across-replicates is the right reading of "at least one condition with qvalue < 0.05" — the published sentence is a per-substitution existence claim — but the choice is genuinely ambiguous in the source and it is worth one sentence in the manuscript rather than silence.

## Results, avg rule (the published operationalisation)

95% protein-cluster percentile intervals, 20,000 nominal draws, seed 20260728, all 20,000 retained.

| Endpoint | Arm | n | positives | proteins | proteins with a positive | AUC | 95% CI | retained / nominal |
|---|---|---|---|---|---|---|---|---|
| >= 1 (published) | primary | 163 | 79 | 48 | 35 | 0.526823 | [0.416106, 0.630551] | 20000 / 20000 |
| >= 1 (published) | inclusive | 166 | 82 | 50 | 37 | 0.544135 | [0.434521, 0.647659] | 20000 / 20000 |
| >= 2 | primary | 163 | 58 | 48 | 32 | 0.549918 | [0.448441, 0.645103] | 20000 / 20000 |
| >= 2 | inclusive | 166 | 58 | 50 | 32 | 0.534642 | [0.432551, 0.629520] | 20000 / 20000 |
| >= 3 | primary | 163 | 47 | 48 | 30 | 0.563096 | [0.444859, 0.671997] | 20000 / 20000 |
| >= 3 | inclusive | 166 | 47 | 50 | 30 | 0.548900 | [0.432560, 0.657714] | 20000 / 20000 |

Change from the published endpoint: primary +0.023095 at >= 2 and +0.036273 at >= 3; inclusive -0.009492 at >= 2 and +0.004766 at >= 3.

### Results, all rule (strict consensus, sensitivity only)

| Endpoint | Arm | n | positives | AUC | 95% CI | retained / nominal |
|---|---|---|---|---|---|---|
| >= 1 | primary | 163 | 78 | 0.535294 | [0.426684, 0.637653] | 20000 / 20000 |
| >= 1 | inclusive | 166 | 81 | 0.552505 | [0.443268, 0.654998] | 20000 / 20000 |
| >= 2 | primary | 163 | 57 | 0.559583 | [0.460937, 0.651591] | 20000 / 20000 |
| >= 2 | inclusive | 166 | 57 | 0.544182 | [0.444647, 0.636630] | 20000 / 20000 |
| >= 3 | primary | 163 | 46 | 0.574322 | [0.460573, 0.679588] | 20000 / 20000 |
| >= 3 | inclusive | 166 | 46 | 0.559964 | [0.447419, 0.665008] | 20000 / 20000 |

## Survival of the 79 primary positives

| Endpoint | surviving | lost |
|---|---|---|
| >= 1 | 79 | 0 |
| >= 2 | 58 | 21 |
| >= 3 | 47 | 32 |

The 21 that drop at >= 2 all have exactly 1 called condition and all come from a single strain, so the avg/any/all distinction does not touch any of them:

P02829 T533A (HSP82, 66.664 A); P02829 T612A (HSP82, 59.302); P11792 S288A (SCH9, 25.882); P12683 S575A (HMG1, 31.562); P12683 S577A (HMG1, 32.681); P13185 T990A (KIN1, 48.552); P16140 Y370A (VMA2, 21.586); P23561 S323A (STE11, 19.635); P32490 S163A (MKK1, 17.495); P32490 S192A (MKK1, 32.591); P32490 S194A (MKK1, 27.681); P32490 S458A (MKK1, 24.666); P32561 S388A (RPD3, 28.466); P47116 S587A (PTK2, 20.922); P50873 S323A (MRK1, 10.152); P50873 Y324A (MRK1, 8.921); P53599 S1424A (SSK2, 21.311); Q00772 S428A (SLT2, 11.048); Q04439 S992A (MYO5, 86.019); Q04439 S1205A (MYO5, 53.577); Q12271 S975A (INP53, 73.571).

A further 11 drop at >= 3, all with exactly 2 called conditions: P06782 S211A (SNF1, 9.060 A); P06782 S487A (SNF1, 67.486); P11986 S368A (INO1, 1.341); P16140 S503A (VMA2, 58.452); P16387 S315A (PDA1, 6.331); P25333 S123A (SAT4, 52.424); Q03330 S64A (GCN5, 24.499); Q03330 S204A (GCN5, 10.286); Q03533 T513A (TDA1, 30.850); Q03656 S427A (SKY1, 56.106); Q04439 Y359A (MYO5, 43.379).

Positive-carrying proteins fall from 35 to 32 to 30 out of 48. Four of the 21 dropouts at >= 2 are MKK1 sites and two are MYO5 sites, so the loss is not spread evenly across proteins — relevant because the resampling unit is the protein.

## What moved, and why

The primary gain is small and mechanical. Median distance among primary positives falls from 26.233 A (k>=1) to 25.932 (k>=2) to 25.631 (k>=3), while median distance among negatives falls too (31.827 -> 30.462 -> 30.656). The 21 sites dropped at >= 2 have a mean distance of 34.3945 A, above the primary cohort mean of 30.7487 A, so removing them from the positive class tightens the positive class slightly toward the annotation. This is a modest re-sorting, not a new signal: the point estimate moves 0.023 and the interval half-width is roughly 0.10.

The inclusive arm's non-monotonicity has a specific cause. The 3 rows unique to the inclusive arm — P00359 S149A, P00359 T151A, Q03262 S158A — are annotation-coincident, so all three sit at `dist_core_A` = 0.000, and all three have exactly 1 called condition. At the published endpoint they are positives at distance zero, which is the entire source of the inclusive arm's apparent advantage over the primary arm (0.544 vs 0.527). At >= 2 they flip to negatives at distance zero, and the inclusive AUC drops below the primary AUC (0.535 vs 0.550); the positive classes of the two arms then have identical size (58, and 47 at >= 3). That the primary/inclusive ordering reverses under a stricter endpoint is a point in favor of the decision to exclude annotation-coincident sites from the primary cohort — the inclusive arm's higher published AUC was carried by three zero-distance sites with the weakest possible phenotype evidence.

## Does discrimination improve?

Marginally in the primary arm, and not in a way that survives scrutiny. All six avg-rule intervals contain 0.5:

- lower bounds range from 0.416 to 0.448
- the largest point estimate, 0.563 at >= 3 primary, has interval [0.445, 0.672]

The interval at >= 3 is *wider* than at >= 2 (half-width 0.114 vs 0.098) because the positive class has shrunk to 47 sites in 30 proteins. Any real improvement in ranking is being bought with precision.

The three endpoints share 163 of 163 rows and differ only in labels, so the estimates are strongly dependent and there is no valid paired test across them. I did not compute one, and `paired_auc_difference` does not apply here — it compares two scores under a fixed label, not two labels under a fixed score. Treat the 0.023 and 0.036 shifts as descriptive.

## Caveats

- The >= 2 and >= 3 endpoints are post hoc and were not preregistered. They are sensitivity analyses, not competing primary results.
- Reclassifying rather than dropping is a choice; the alternative was not computed.
- The strict-consensus (all) replicate rule changes the published k=1 label for P43565 S1764A. The source does not settle which reading is intended.
- The called-condition count is a count of conditions passing qvalue < 0.05 in the source supplement; it is not an effect-size threshold. A substitution with 8 weakly-called conditions outranks one with 1 strongly-called condition under this endpoint. An S-score-magnitude endpoint would be a different and arguably better test of the same question.
- Nothing here belongs in a manuscript, wiki page, or figure until it is entered in `NUMBERS.md` by the author. These are proposed numbers.
