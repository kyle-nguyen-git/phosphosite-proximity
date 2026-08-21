# NUMBERS.md — Canonical Numbers for the Phosphosite-Distance Calibration Preprint

> **HUMAN-NUMBER HOLD — DISCHARGED 2026-08-18 06:40 CDT.** The exact-canonical AlphaFold audit removed
> the wrong-isoform CHD6 S27 row; the cohort is 1,470 sites in 787 proteins and the complete dependent
> family is registered in **Section 27**, which supersedes 26 and with it 22–25 for every human quantity.
> Reviewer-proposed analyses are in **Section 28**. Pause record:
> `outputs/fulbright/research/PREPRINT_FIX_PAUSE_2026-08-18.md`.

Refrozen **2026-07-29 16:33 CDT** after clean-environment reconciliation and deterministic
serialization of machine-precision continuous-model fields. Cohorts, estimates, intervals, and every
reported scientific value are unchanged. This file is the sole numerical authority for manuscript and
release work.

Editorial authority was extended on **2026-07-30** to catalogue the source and method metadata in
Section 16 and to resolve a duplicated tyrosine-subgroup bootstrap in the reader-facing manuscript.
The frozen numerical outputs and their hashes are unchanged.

Extended again on **2026-08-12** with Section 17 (figure provenance, 2026-08-03) and Section 18
(round-2 authorized analyses). Section 18 values are `[POST-HOC]`, not `[REPO]`: they come from scripts
under `phase0_5/results/round2/` that verify the three frozen hashes below before computing, import the
frozen estimators without reimplementation, and write nothing into the frozen tree. The frozen numerical
outputs and their hashes are unchanged by either extension.

Frozen source hashes (SHA-256):

- `results/statistics.json` — `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`
- `results/analysis_final.csv` — `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`
- `phase0_5/results/phase0_5_statistics.json` — `3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b`

The pre-repair audit baseline was independently hash-verified before the rerun: `73398b41…566e`, `a42f8d18…bceb`, and `e82b7e11…8434`, respectively. `[REPO]` means the value is emitted by the current seeded repository pipeline. Manuscripts, tables, figures, and release checks must take numerical claims from this file and reconcile them to the frozen outputs above.

---

## 1. Primary Estimand `[REPO]`

The **primary cohort excludes the three annotation-coincident substitutions**. The inclusive cohort is a named sensitivity and must appear beside the primary result in the abstract.

| Arm | n | Proteins | Positive | AUC | Protein-cluster 95% CI |
|---|---:|---:|---:|---:|---:|
| **Primary: annotation-coincident substitutions excluded** | **163** | **48** | **79** | **0.5268234** | **0.416744–0.631539** → **0.527 [0.417, 0.632]** |
| **Sensitivity: annotation-coincident substitutions included at 0 Å** | **166** | **50** | **82** | **0.5441347** | **0.435756–0.648746** → **0.544 [0.436, 0.649]** |

Both protein-cluster intervals use **200,000 draws** and seed **20260729**. The substitution-level dependence diagnostics use 200,000 draws and are **0.436735–0.617369** for primary and **0.455384–0.632703** for inclusive.

The manuscript may report the primary interval endpoint **0.632**. It may not frame that endpoint as excluding performance above any value. This August 12 retirement is binding under Section 13. It must not say that distance is uninformative or that the study excludes AUC ≥0.63 based on a rounded Monte Carlo endpoint.

## 2. Annotation-Coincident Substitutions `[REPO]`

| Accession | Gene/site | Distance | Outcome-positive | Annotation evidence |
|---|---|---:|---:|---|
| P00359 | TDH3 S149 | 0 Å | yes | ECO:0000250 |
| P00359 | TDH3 T151 | 0 Å | yes | ECO:0000250 |
| Q03262 | PRM15 S158 | 0 Å | yes | ECO:0000250 |

All three are outcome-positive and occupy the predictor extreme. Their inclusion moves pooled AUC from **0.527** to **0.544**. The two extra proteins in the inclusive arm are TDH3 and PRM15; neither contributes another substitution. Inclusion is therefore a declared sensitivity, not the primary target population.

## 3. Two-Arm Pipeline Status `[REPO]`

The named switch is now implemented as `exclude_annotation_coincident` and `include_annotation_coincident`. One seeded run emits complete primary and inclusive arms in:

- `results/cohort_arm_primary_estimates.csv`
- `results/cohort_arm_cutoffs.csv`
- `results/cohort_arm_logistic.csv`
- `results/cohort_arm_descriptives.csv`
- `phase0_5/results/confidence_strata.csv`
- `phase0_5/results/cohort_arm_primary_estimates.csv`
- `phase0_5/results/cohort_arm_cutoffs.csv`
- `phase0_5/results/regression_models.csv`
- `phase0_5/results/cohort_arm_descriptives.csv`

The primary analysis files contain 163 substitutions and no annotation-coincident rows. The inclusive files contain 166 substitutions and all three 0 Å rows.

## 4. Cohort Cascade `[REPO]`

| Stage | Strain records | Unique substitutions | Proteins |
|---|---:|---:|---:|
| Point-mutant source rows | 497 | 490 | 116 |
| Sequence matched after PBY107 resolution | 487 | 479 | 113 |
| Sequence matched with a raw profile | 465 | 458 | 111 |
| After WGS exclusion | 447 | 443 | 110 |
| After scar-control-correlation exclusion | 427 | 423 | 107 |
| Core annotation and structure eligible | 169 | 166 | 50 |

The core UniProt payload contains **41 active-site** and **221 binding-site feature records** and defines **560 unique target residues**. An earlier feature-residue-row total is withdrawn because it does not reproduce; no artifact may cite it. Two independent round-2 analyses get 594 record-residue rows, 565 or 566 after deduplication, with the excess arising from P12904 intervals recorded once per ligand. See Sections 13 and 18.10. The inclusive arm contains **109 serines, 41 threonines, and 16 tyrosines**. The primary arm contains **107 serines, 40 threonines, and 16 tyrosines**.

## 5. Distance Descriptives `[REPO]`

| Quantity | Primary exclude | Inclusive sensitivity |
|---|---:|---:|
| Median distance, outcome-positive | **26.233 Å** | 25.757 Å |
| Median distance, outcome-negative | **31.827 Å** | 31.827 Å |
| Overall median distance | **28.930 Å** | 28.520 Å |
| Median site pLDDT | **46.50** | 49.44 |
| Median RSA | **0.5705** | 0.5693 |
| Correlation, log10(distance + 1) vs site pLDDT | **−0.5408** | −0.5616 |

## 6. Descriptive Cutoff Tables `[REPO]`

These are nested descriptive groups, not independent threshold tests.

### Primary exclude arm

| Cutoff | n within | Positive within | Rate within | n beyond | Positive beyond | Rate beyond | Descriptive OR |
|---:|---:|---:|---:|---:|---:|---:|---:|
| ≤5 Å | 10 | 4 | 40.00% | 153 | 75 | 49.02% | 0.693 |
| ≤8 Å | 20 | 12 | 60.00% | 143 | 67 | 46.85% | 1.701 |
| ≤10 Å | 30 | 17 | 56.67% | 133 | 62 | 46.62% | 1.498 |
| ≤15 Å | 43 | 24 | 55.81% | 120 | 55 | 45.83% | 1.493 |

### Inclusive sensitivity

| Cutoff | n within | Positive within | Rate within | n beyond | Positive beyond | Rate beyond | Descriptive OR |
|---:|---:|---:|---:|---:|---:|---:|---:|
| ≤5 Å | 13 | 7 | 53.85% | 153 | 75 | 49.02% | 1.213 |
| ≤8 Å | 23 | 15 | 65.22% | 143 | 67 | 46.85% | 2.127 |
| ≤10 Å | 33 | 20 | 60.61% | 133 | 62 | 46.62% | 1.762 |
| ≤15 Å | 46 | 27 | 58.70% | 120 | 55 | 45.83% | 1.679 |

The 5 Å descriptive odds ratio changes from **0.69** in the primary arm to **1.21** in the inclusive sensitivity.

## 7. Logistic Models `[REPO]`

Odds ratios are per ten-fold increase in distance + 1 Å with protein-cluster sandwich covariance.

### Primary exclude arm

| Formula | OR | 95% CI | Cluster p |
|---|---:|---:|---:|
| `y ~ logd` | **0.767** | 0.274–2.150 | 0.614 |
| `y ~ logd + plddt` | **1.045** | 0.305–3.581 | 0.944 |
| `y ~ logd + plddt + rsa` | **1.313** | 0.383–4.508 | 0.665 |

### Inclusive sensitivity

| Formula | OR | 95% CI | Cluster p |
|---|---:|---:|---:|
| `y ~ logd` | 0.587 | 0.235–1.469 | 0.255 |
| `y ~ logd + plddt` | 0.762 | 0.250–2.322 | 0.633 |
| `y ~ logd + plddt + rsa` | 0.952 | 0.306–2.967 | 0.933 |

## 8. Structural-Confidence Strata `[REPO]`

All PAE strata use **`pae_pair_max`**, the larger directed site-target PAE value. The complete 11-row family must be displayed for both arms.

### Primary exclude arm

| Stratum | n | Positive | AUC | Protein-cluster 95% CI |
|---|---:|---:|---:|---:|
| All | 163 | 79 | **0.5268** | **0.4167–0.6315** |
| Site pLDDT ≥50 | 79 | 43 | 0.4890 | 0.3465–0.6340 |
| Site pLDDT ≥70 | 60 | 31 | 0.4594 | 0.3027–0.6181 |
| Site and target pLDDT ≥70 | 58 | 30 | 0.4500 | 0.2876–0.6063 |
| Site pLDDT ≥90 | 35 | 22 | 0.5699 | 0.3707–0.7464 |
| Site and target pLDDT ≥90 | 28 | 16 | 0.6406 | 0.4643–0.7895 |
| `pae_pair_max` ≤5 Å | 37 | 20 | 0.4882 | 0.2609–0.6658 |
| `pae_pair_max` ≤10 Å | 44 | 25 | 0.4358 | 0.2083–0.6330 |
| `pae_pair_max` ≤15 Å | 55 | 30 | 0.5200 | 0.3214–0.6790 |
| Both-residue pLDDT ≥70 and `pae_pair_max` ≤10 Å | 41 | 22 | 0.4163 | 0.1917–0.6167 |
| Both-residue pLDDT ≥90 and `pae_pair_max` ≤10 Å | 27 | 15 | 0.6833 | 0.4808–0.8640 |

### Inclusive sensitivity

| Stratum | n | Positive | AUC | Protein-cluster 95% CI |
|---|---:|---:|---:|---:|
| All | 166 | 82 | 0.5441 | 0.4358–0.6487 |
| Site pLDDT ≥50 | 82 | 46 | 0.5223 | 0.3801–0.6649 |
| Site pLDDT ≥70 | 63 | 34 | 0.5071 | 0.3506–0.6630 |
| Site and target pLDDT ≥70 | 61 | 33 | 0.5000 | 0.3365–0.6579 |
| Site pLDDT ≥90 | 38 | 25 | 0.6215 | 0.4348–0.7909 |
| Site and target pLDDT ≥90 | 31 | 19 | 0.6974 | 0.5357–0.8421 |
| `pae_pair_max` ≤5 Å | 40 | 23 | 0.5550 | 0.3322–0.7296 |
| `pae_pair_max` ≤10 Å | 47 | 28 | 0.4962 | 0.2770–0.6923 |
| `pae_pair_max` ≤15 Å | 58 | 33 | 0.5636 | 0.3767–0.7143 |
| Both-residue pLDDT ≥70 and `pae_pair_max` ≤10 Å | 44 | 25 | 0.4863 | 0.2708–0.6838 |
| Both-residue pLDDT ≥90 and `pae_pair_max` ≤10 Å | 30 | 18 | 0.7361 | 0.5530–0.9028 |

The PAE-threshold sequences are not monotonic in either arm.

## 9. PAE Definition Sensitivity `[REPO]`

At PAE ≤10 Å, the four columns give:

| Cohort | `pae_pair_max` | Site-to-target | Pair mean | Target-to-site | Grid range | Rank of joint pair-max ≤10/site pLDDT ≥70 |
|---|---:|---:|---:|---:|---:|---:|
| Primary exclude | **0.436** | 0.459 | 0.489 | 0.521 | 0.416–0.569 | 1 of 72 |
| Inclusive sensitivity | 0.496 | 0.513 | 0.539 | 0.565 | 0.486–0.601 | 1 of 72 |
| Legacy 158-site | 0.423 | 0.446 | 0.477 | 0.505 | 0.406–0.554 | 1 of 72 |

The four summaries and 72-cell grids are post-result sensitivity families. No PAE column is promoted as a result.

## 10. SIFT Comparator `[REPO]`

SIFT is a post-result comparator, not independent validation.

| Arm/support | n | Positive | SIFT AUC | 95% CI | Distance AUC | 95% CI | SIFT − distance |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Primary exclude common support** | **152** | **71** | **0.606155** | **0.522180–0.690150** | **0.531734** | **0.418014–0.646578** | **0.074422 [−0.036887, 0.191529]** |
| Inclusive common support | 155 | 74 | 0.619119 | 0.535204–0.703728 | 0.550717 | 0.440277–0.664346 | 0.068402 [−0.038414, 0.179261] |

The primary SIFT point estimate lies inside the primary distance interval **0.417–0.632**. The inclusive SIFT point estimate lies inside the inclusive distance interval **0.436–0.649**.

## 11. Within-Protein Results `[REPO]`

- **23 proteins**, **112 substitutions**, and **176** positive-negative pairs are informative.
- Pair-weighted within-protein AUC: **0.52841 [0.36842, 0.70900]**.
- Equal-protein-weight AUC: **0.49722 [0.35072, 0.64215]**.
- Primary within-protein distance-percentile AUC: **0.51100 [0.41161, 0.61152]**.

The annotation-coincident substitutions contribute no within-protein positive-negative pairs, so the pair-weighted and equal-protein estimates do not move with their exclusion. The site-weighted percentile analysis is reported for the primary arm.

## 12. Other Post-Result Sensitivities `[REPO]`

### Cohort and residue definitions

| Analysis | n | Proteins | Positive | AUC | 95% CI |
|---|---:|---:|---:|---:|---:|
| Primary exclude | 163 | 48 | 79 | 0.527 | 0.417–0.632 |
| Inclusive 0 Å sensitivity | 166 | 50 | 82 | 0.544 | 0.436–0.649 |
| Inclusive, omit resolved HOG1 row | 165 | 50 | 81 | 0.540 | 0.433–0.645 |
| Legacy Supplementary Data 6-selected cohort | 158 | 48 | 74 | 0.522 | 0.408–0.632 |
| Primary Ser/Thr only | 147 | 48 | 67 | 0.499 | 0.389–0.605 |
| Primary Tyr only | 16 | 12 | 12 | 0.604 | 0.272–1.000 |
| Inclusive, omit PRM15 S158 | 165 | 49 | 81 | 0.539 | 0.429–0.641 |

Residue-specific primary AUCs are **0.494 [0.381, 0.602]** for serine, **0.503 [0.295, 0.714]** for threonine, and **0.604 [0.267, 1.000]** for tyrosine.

**Correction 2026-08-12: neither tyrosine interval is reportable.** Both upper endpoints sit exactly at
the AUC boundary of 1.000, and the two records differ in retained draws (19,335 and 19,404 of a nominal
20,000) for the same reason — the 16-substitution subset carries only 4 negatives, so protein resamples
frequently degenerate. Report the point estimate **0.604** with n = 16 and no interval. See Section 18.7.

The tyrosine-only subset was also duplicated in the cohort-sensitivity family, where a separate
20,000-draw seed gave **0.604 [0.272, 1.000]**. This is Monte Carlo variation for the same 16-site
subset, not a distinct biological analysis. Reader-facing prose and tables use the dedicated
residue-class interval, **0.604 [0.267, 1.000]**; the duplicate cohort-family value remains visible in
the frozen output for reproducibility.

### Feature definitions

| Distance definition | n | Proteins | Positive | AUC | 95% CI |
|---|---:|---:|---:|---:|---:|
| ACT_SITE only | 107 | 31 | 54 | 0.570 | 0.453–0.677 |
| BINDING only | 155 | 46 | 77 | 0.525 | 0.415–0.632 |
| ACT_SITE/BINDING primary | 163 | 48 | 79 | 0.527 | 0.417–0.632 |
| Add SITE | 163 | 48 | 79 | 0.526 | 0.414–0.633 |
| Add SITE and DNA-binding | 163 | 48 | 79 | 0.525 | 0.414–0.630 |

### Confidence, continuous outcomes, and prediction

- Spearman distance versus `pae_pair_max`: **0.753 [0.661, 0.827]**.
- Spearman site pLDDT versus `pae_pair_max`: **−0.795 [−0.852, −0.688]**.
- The five continuous-outcome Spearman estimates range from **−0.115 to −0.076**; every protein-bootstrap interval crosses zero.
- Protein-isolated mean split AUCs: distance only **0.484**, structural **0.558**, source annotations **0.590**, combined **0.587**.
- Structural increment over source annotations: **−0.003**, split range **−0.039 to 0.034**.
- Adjusted linear-probability wild-cluster p: **0.675** using **9,999** Rademacher draws.

## 13. Claims and Artifact Rules

Allowed:

- Primary: **163 substitutions, AUC 0.527 [0.417, 0.632]**.
- Named inclusive sensitivity: **166 substitutions, AUC 0.544 [0.436, 0.649]**.
- ~~The primary interval excludes discrimination materially above **0.632**.~~ **Retired by author
  decision 2026-08-12.** The manuscript makes no exclusion claim. The interval endpoint is still
  0.631539 and may be reported as an endpoint, but no artifact may frame it as excluding
  performance above any value. See the Not allowed list below.
- Chance-level and SIFT-like ranking remain compatible with the primary result.

Not allowed:

- Calling the inclusive arm primary.
- Any statement that the interval excludes discrimination above a value, including the 0.632
  endpoint (retired 2026-08-12; the claim appeared in the superseded `preprint_draft_v1`).
- “This study excludes AUC ≥0.63” based on a low-draw rounded endpoint.
- “Distance is uninformative.”
- A range-restriction caveat for AUC.
- A monotone PAE-confidence trend.
- Showing only a selected subset of the confidence-strata family.
- Leaving the PAE column unnamed.
- Reporting either tyrosine AUC with an interval; both endpoints touch 1.000 (Sections 12, 18.7).
- Reporting a benchmark model's split-averaged AUC without its pooled out-of-fold counterpart (18.8).
- "Distance performs below chance", from the pooled out-of-fold 0.3926 (18.8).
- "The null is an artifact of annotation quality" — 18.9 shows the design cannot be run on
  experimentally-evidenced annotation at all, which is a different and stronger statement.
- "The stricter endpoint improves discrimination" — the ≥3 interval is wider than the ≥2 (18.1).
- Any paired difference across outcome endpoints (18.1) or across outcome directions (18.2); no
  estimator for either contrast exists in the frozen module and none was written.
- Citing Section 4's "564 feature-residue rows" (18.10).
- ~~"There is no positive control for the outcome."~~ **Retired 2026-08-13.** Section 10's SIFT interval
  0.522180–0.690150 does not contain 0.5, so the manuscript computed a positive control and then denied
  having one. The retired sentence stood in the v3 Discussion §3.2 and in §2.4.1's closing line; both are
  rewritten. Allowed in its place: the outcome is not blind, so a near-chance estimate on this cohort is a
  real negative. Not allowed in its place: that SIFT outperforms distance (the paired difference
  0.074422 [−0.036887, 0.191529] contains zero) or that SIFT resolves sites within a protein (not
  estimated in this cohort; the human replication's within-protein SIFT interval contains 0.5, Section 20.8.3).

Allowed, added 2026-08-12 on the strength of Sections 18.1–18.9:

- The near-chance primary reading survives stricter endpoints (≥2 and ≥3 called conditions) and a
  defect-specific direction endpoint; every one of those intervals contains 0.5.
- No comparator predictor and no cheap sequence or structural baseline is distinguishable from chance
  or from the declared predictor on the primary cohort.
- The primary AUC is indistinguishable from chance under both an unrestricted and a within-protein
  permutation null.

`manuscript/preprint_draft_v1.pdf` and every file under `manuscript/rendered/` must be rebuilt from the exclude-primary manuscript and figures. The release verifier must inspect the PDF text and require a rendered-page manifest tied to the current PDF hash; a Markdown-only scan is insufficient.

## 14. Reconciled Release Artifact State

- The fail-closed verifier passes **69/69 checks**; the release-manifest file count is refreshed by every verified run.
  The count rose from 66 on **2026-08-03** with three checks binding the panel-composed figures: their
  hashes against Section 17, the presence of the figure-provenance declaration, and agreement between the
  Figure 1B ROC-envelope contract and `manuscript/panels/src/p1b_roc.py`. Internal review records under
  `phase0_5/reviews/` still quote 66/66 and are dated artifacts, not current state.
- The rebuilt review PDF contains **11 pages**. Its SHA-256 is `ba484a32af7322843d0378fd2078b0a0689849d9edf8ec29459e25bf3e729574`.
- `manuscript/rendered/render_manifest.json` binds **11 rendered pages** and the contact sheet to that PDF hash, with no extra rendered pages.
- The corrected supplementary workbook contains **22 sheets**, including separate primary and inclusive data, estimates, cutoffs, descriptives, confidence strata, models, fit diagnostics, feature-evidence and replicate audits, PAE tables, and SIFT results.
- The obsolete `pae_filter_grid_72x2.csv` is removed. The current grid is `pae_filter_grid_72x3.csv`, with **72 cells for each of the primary, inclusive, and legacy cohorts**.

## 15. Computational Contracts and Replicate Audit `[REPO]`

- Frozen analysis environment: CPython **3.12.4**, NumPy **1.26.4**, pandas **2.2.2**, SciPy
  **1.13.1**, scikit-learn **1.4.2**, statsmodels **0.14.2**, and Biopython **1.85**. The complete
  transitive release environment is pinned in `requirements-lock.txt`.
- Tested release host: macOS **15.7.2** on **arm64** with Poppler `pdftoppm` **26.05.0**. The Python
  package lock fixes versions but does not include distribution hashes; clean-room evidence records the
  resolved package set and renderer.
- Continuous clustered-OLS sensitivity fields are serialized after rounding to **12 decimal places**.
  This is below manuscript reporting precision and removes BLAS-dependent last-bit drift without changing
  any reported value.
- Base Phase 0.5 random seed: **20260728**. Canonical arm intervals use **200,000**
  protein-cluster draws and seed **20260729**; substitution-level dependence intervals also use
  **200,000** draws.
- Post-result AUC sensitivity intervals use **20,000** draws. Continuous-outcome Spearman intervals use
  **4,000** protein-cluster draws. The adjusted linear-probability sensitivity uses **9,999**
  Rademacher wild-cluster draws.
- Internal prediction uses **10** repeated stratified group **5-fold** splits. Splitter seeds are
  **20260728–20260737**; the within-fold logistic model uses random state **20260728**.
- The descriptive cutoff set (**5, 8, 10, and 15 Å**) was fixed for post-result sensitivity analysis
  after the primary outcome had been inspected. The groups are nested and are not independent threshold
  tests.
- The source binary endpoint uses `qvalue < 0.05`. Replicate-strain counts are nonnegative and are averaged
  before testing whether the mean is greater than zero; this is logically an **any-positive-replicate**
  rule, not a unanimity rule.
- **Two** inclusive-arm substitutions have more than one retained strain. P32324 position 566 has **2/2**
  screen-positive strains with per-strain called-condition counts **12 and 3**. P43565 position 1764 has
  **2/3** screen-positive strains with counts **16, 0, and 8**. Thus **one of two** replicated
  substitutions is discordant under the binary endpoint. The file
  `phase0_5/results/replicate_aggregation_audit.csv` exposes the strain-level audit; no post-result
  replicate-unanimity outcome is promoted as a replacement endpoint.

## 16. Source and Method Metadata for the Manuscript `[REPO]`

- The public yeast screen contains **102 conditions**. Individual retained profiles can contain fewer
  observed condition values; the binary outcome is reconstructed from each available source profile.
- The four required source workbooks are Supplementary Data **1, 3, 6, and 8** from Europe PMC record
  PMC7612524. They define constructs, condition-level outcomes, optional annotations, and source quality
  control, respectively.
- The PBY107 workbook coordinate is HOG1 **T178A**. The source article identifies HOG1 **T174A** as the
  regulatory control, and T174 matches the reviewed sequence. PBY107 is analyzed at **T174**, with a
  named exclusion sensitivity.
- UniProt records were retrieved on **29 July 2026**. The response reported release **2026_02**, dated
  **10 June 2026**.
- Included AlphaFold DB structures and PAE documents are checksum-pinned **version 6 monomer** records.
  **Added 2026-08-12:** all **50** cached mmCIF files declare `_ma_model_list.model_group_name`
  "**AlphaFold Monomer v2.0 model**", verified across the whole cache. The database entry version (6)
  and the predictor version (AlphaFold2 monomer v2.0) are distinct; the manuscript must give both at
  first use, per RR-36.
- The PAE grid comprises **four** PAE summaries, **six** PAE thresholds, and **three** site-pLDDT floors,
  giving **72** cells per cohort.
- Of the **48** primary-cohort proteins, **12** contain only outcome-positive substitutions, **13** only
  outcome-negative substitutions, and **23** both outcome classes.
- Replicate-averaged S-score profiles are summarized by mean, standard deviation, root-mean-square,
  mean absolute value, maximum absolute value, minimum, and maximum. The five continuous outcomes
  analyzed against distance are the called-condition count, negative log10 minimum raw q-value,
  root-mean-square S-score, mean absolute S-score, and maximum absolute S-score. Only the three
  absolute-value summaries are direction-agnostic.

## 17. Figure Provenance `[REPO]`

Added **2026-08-03**. Two figure lineages exist and they are not interchangeable.

| Figure set | Files | Builder | Used by |
|---|---|---|---|
| Panel-composed (current, reader-facing) | `manuscript/figure1.{png,pdf}`, `manuscript/figure2.{png,pdf}` | `manuscript/panels/src/p*.py` → `manuscript/panels/compose.py`, driven by `manuscript/panels/build_all.sh` | the editable manuscript Markdown and the current Word build |
| Legacy (frozen review PDF) | `manuscript/figure1_cohort_estimand_primary.{png,pdf}`, `phase0_5/results/phase0_5_robustness_summary.{png,pdf}` | `manuscript/src/build_figure1.py`, `phase0_5/src/03_phase0_5_figure.py` | `manuscript/preprint_draft_v1.{md,pdf}`, whose SHA-256 is frozen in Section 14 |

The legacy Figure 1 compresses the cascade into five boxes, merging the whole-genome-sequencing
and scar-correlation stages into one "427 records after source QC" step. Section 4 declares six
stages. Both renderings are numerically correct; only the panel figure shows every declared stage.
Do not describe the two as the same figure.

Panel inputs, all committed pipeline outputs: `results/cohort_disposition.csv`,
`results/analysis_final.csv`, `results/analysis_inclusive_sensitivity.csv`,
`phase0_5/results/phase0_5_analysis.csv`, `confidence_strata.csv`, `cohort_sensitivity.csv`,
`residue_class_sensitivity.csv`, `feature_definition_sensitivity.csv`, and
`sift_comparator_sensitivity.csv`. The cohort counts a panel asserts against are parsed from
Sections 1 and 4 of this file at build time; no count is typed into panel source.

**Figure 1B ROC envelope.** The shaded band uses **2,000** protein-cluster draws at
seed **20260729**, resampling accessions with every substitution of a sampled protein retained.
Resamples that draw a single outcome class are discarded before percentiles are taken, so the
effective count is at most 2,000; at the committed data and seed none are discarded. The band is a
**pointwise 2.5th-to-97.5th percentile envelope over the false-positive grid, not the AUC interval**.
It is wider than the declared AUC interval by construction and must never be reported as one. The
canonical AUC intervals remain the 200,000-draw values in Section 1.

**Figure 2A separation.** The annotated maximum vertical separation between the two empirical
cumulative distance distributions is the two-sample Kolmogorov–Smirnov statistic
**0.137131 → 0.137** on the primary cohort (79 outcome-positive, 84 outcome-negative). It is a
descriptive distance between distributions, not a test result; no KS p-value is reported.

Panel builds are byte-reproducible for an unchanged environment and input tree: matplotlib PDF
`CreationDate` is suppressed in `manuscript/panels/src/_style.py`, and `compose.py` saves with
`no_new_id=1` so MuPDF writes no trailer `/ID`. PNG output carries no timestamp. `PyMuPDF==1.28.0`
is pinned in `requirements-lock.txt`; the composed PNGs are rasterized at 600 dpi through it.

Current panel-composed figure hashes (SHA-256), bound by the release verifier:

- `manuscript/figure1.png` — `8fffd9ccd5dda7f92c41a87c58aade58e46c8b726a1e8017fcdbae06b95b3598`
- `manuscript/figure2.png` — `22790831c9d856eed417d3a1d098910a3cfcdfe7f61d5dd87acae3a80acbc62c`
- `manuscript/figure1.pdf` — `850cfad2ef91fa8ed4d2680542408edb3a11e81c1efcd7ff97a98b1369acbe62`
- `manuscript/figure2.pdf` — `98ffbff1f88a5f2ea6c34a45a25660619d835ae3447cce52b4afdb356ed8f711`

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


## 19. Values Released for the v3 Draft `[POST-HOC]`

Added **2026-08-12** to discharge the blocking set in `v3_draft/V3_CLAIMS_LEDGER.md`. Every value was
computed directly against the frozen tree, not taken from a review or an agent report; two review
figures are superseded below. Intervals use 20,000 protein-cluster draws at seed 20260728 with retained
draws stated, matching the Section 18 convention.

### 19.1 Ranked-pair decomposition (RR-53, RR-18)

The primary arm ranks **79 × 84 = 6,636** positive–negative pairs, of which **176 (2.65%)** are
within-protein. **23** of the 48 proteins carry both outcome classes and hold **112** of the 163
substitutions.

| Quantity | Value |
|---|---:|
| Largest single contributor, Q03656 | **50** pairs, **28.4%** |
| Second, P16140 | 36 pairs, 20.5% |
| Five largest combined | **69.3%** |
| Proteins contributing exactly one pair | **4** (within-protein AUC mechanically 0 or 1) |

**Correction.** Round-1 review material named P16140 as the largest contributor at 20%. P16140's 36
pairs are correct; it is not the maximum. Q03656 is.

### 19.2 Cluster structure (RR-61)

**48** clusters, sizes **1–15**, Kish effective cluster count **29.0**, six largest proteins holding
**55** of 163 substitutions. Quote the effective count wherever the nominal 48 is described.

### 19.3 Site-confidence fractions (RR-37)

**84 of 163** substituted residues have site pLDDT below 50; **103 of 163** below 70. Exact complements
of the Section 8 strata.

### 19.4 Endpoint denominator (RR-19)

`raw_conditions` takes five values in the primary cohort: 96 (2 substitutions), 98 (1), 100 (3),
101 (2), 102 (155). **8** substitutions carry fewer than 102 observed conditions and **7 of those 8** are
screen-positive.

| Restriction | n | Positive | AUC | 95% CI | Nominal | Retained |
|---|---:|---:|---:|---:|---:|---:|
| Complete profiles only (102 conditions) | 155 | 72 | **0.500000** | 0.389831–0.603604 | 20,000 | 20,000 |

The complete-profile estimate sits at exactly 0.5. Report it as a restriction result; it is not evidence
of anything beyond the eight excluded substitutions and their outcome composition.

### 19.5 Source quality-control exclusions (RR-41, RR-13 counts)

| Group | Records | Screen-positive | Rate |
|---|---:|---:|---:|
| Sequencing-flagged | **18** | **18** | 100.0% |
| Scar-correlation | **20** | **16** | 80.0% |
| Both exclusion groups | **38** | **34** | 89.5% |
| Retained | 427 | 169 | 39.6% |

The scar-correlation filter is defined on phenotype similarity to a marker control, so for those 20
records the exclusion is conditioned on the outcome by construction. No cohort arm retains them and no
distances were computed for them.

### 19.6 Sequencing coverage (RR-42)

**244 of 497** point-mutant records were sequenced. Of the **169** strain records in the eligible cohort,
**88** were sequenced. Among those 88: **46** carry a coding variant in another gene, **4** in the focal
gene, **3** are CNV-flagged, and **0** carry a nonempty free-text quality-control note — which is the only
field the exclusion rule reads, and the reason all 88 were retained.

**Supersedes** the round-1 figures of 86 of 166 and 45 of 86, which counted substitutions where the
denominator is strain records.

### 19.7 Eligibility selection (RR-56)

| Group | n | Positive | Rate | Proteins |
|---|---:|---:|---:|---:|
| Annotation-eligible | **169** | **84** | **49.7%** | 50 |
| Ineligible, quality-control-passing | **258** | **85** | **32.9%** | 57 |

Gap **16.8 percentage points**. Eligibility conditions on a protein-level variable associated with the
outcome before any site-level contrast is measured.

### 19.8 Small-sample logistic correction (RR-21)

t(47) critical value **2.0117** against the normal 1.9600.

| Model | OR per 10× distance + 1 Å | Normal 95% CI | t(47) 95% CI |
|---|---:|---:|---:|
| `y ~ logd` | 0.767 | 0.274–2.150 | **0.266–2.210** |
| `y ~ logd + plddt + rsa` | 1.313 | 0.383–4.508 | **0.370–4.657** |

Intervals widen by 3.6% and 3.9%. No reported conclusion changes; the direction of the uncorrected error
favoured the manuscript, and the corrected intervals still cross 1.

### 19.9 Resolution against feature spread (RR-62)

Primary interval half-width **0.107** (from 0.416744–0.631539). The spread between the lowest and highest
single-feature point estimates reported on this cohort is **0.079** (0.527 for the declared predictor,
0.606 for SIFT). **Caveat that must travel with the comparison:** the two estimates rest on different
support — 163 substitutions against 152 — so the spread is indicative, not a like-for-like contrast. The
arithmetic supports the statement that the design cannot resolve differences of this size. It does not
support ranking the features.

### 19.10 Additions to the Section 13 claim rules

Not allowed, added:

- Naming P16140 as the largest within-protein contributor (19.1).
- Quoting 86 of 166 or 45 of 86 for sequencing coverage (19.6).
- Reading the complete-profile AUC of 0.500000 as a result about distance (19.4).
- Using the 0.107-against-0.079 arithmetic to rank features, or stating it without the different-support
  caveat (19.9).

## 20. Independent Human Replication — Kennedy 2024 `[REPLICATION]`

A second cohort, computed by the same estimators. Not part of the frozen yeast tree and not covered by
the three frozen content hashes. Working directory `outputs/fulbright/research/kennedy_replication/`;
results in `kennedy_results.json`, `perturbation_arms.json`, `positive_control.json`. Every interval is
a protein-clustered percentile bootstrap, 20,000 draws, seed 20260728, **20,000 retained on every
estimate reported here**. Estimators are imported from `phase0_5/src/02_phase0_5_analysis.py` rather
than reimplemented.

### 20.1 Source

Kennedy PH, Alborzian Deh Sheikh A, Balakar M, et al. "Post-translational modification-centric base
editor screens to assess phosphorylation site functionality in high throughput." *Nature Methods* 2024.
doi:10.1038/s41592-024-02256-z. PMC11804830. Human Jurkat and HEK293. **Two screens with different
readouts, not one proliferation endpoint** (corrected 2026-08-13 19:05 CDT, see Section 22.1): Supplementary
Table 3 is sgRNA abundance before against after ABE8e introduction, a fitness readout; Supplementary
Table 4 is GFP-high against GFP-low bins, an NFAT reporter-activity readout. Everything in this
section that says "either screen" is a union across those two phenotypes.
**An earlier scan of this vault attributed the screen to "Coelho et al." That attribution is wrong and
must not be repeated.**

### 20.2 Cohort

| Quantity | Value |
|---|---:|
| Sites with a distance | **1,475** |
| Proteins | **793** |
| Positives, primary endpoint (raw *p* < 0.05 in either screen) | **293** (19.86%) |
| Sites retaining an experimentally-evidenced target | **512** in 287 proteins |
| Sites matched into the Ochoa 2020 phosphoproteome | **1,172** of 1,475 |
| Median distance | **41.75 Å** (yeast primary 28.930 Å) |
| Median site pLDDT | **37.19** (yeast primary 46.50) |

Human sites sit farther from an annotated target and in lower-confidence structure than the yeast
cohort: median distance 41.75 Å against 28.930 Å, median site pLDDT 37.19 against 46.50. Both shifts are
expected for a mammalian phosphoproteome enriched in disordered regions, and both work against the
feature under test rather than for it.

Distance is the same definition as the yeast pipeline: minimum heavy-atom separation from the edited
residue to the nearest UniProt ACT_SITE or BINDING residue in an AlphaFold DB monomer model, expanded
over feature ranges, self-excluded.

### 20.3 Primary and sensitivities

| Estimate | n | positives | proteins | AUC | 95% interval |
|---|---:|---:|---:|---:|---:|
| **Distance, primary endpoint** | 1,475 | 293 | 793 | **0.505573** | 0.465509–0.545511 |
| Distance, FDR < 0.25 either screen | 1,475 | 19 | 793 | 0.613939 | 0.432767–0.781183 |
| Distance, experimentally-evidenced targets only | 512 | 115 | 287 | 0.510546 | 0.445122–0.575965 |
| Distance, sequence-adjacent pairs excluded | 1,459 | 289 | 784 | 0.503925 | 0.464529–0.544296 |
| Minimum sequence separation | 1,475 | 293 | 793 | 0.520052 | 0.481942–0.558181 |
| Site pLDDT | 1,475 | 293 | 793 | 0.511544 | 0.472533–0.549858 |
| Inverse relative solvent accessibility | 1,475 | 293 | 793 | 0.515685 | 0.476511–0.554024 |
| Annotated target count in the protein | 1,475 | 293 | 793 | 0.458233 | 0.424064–0.494130 |

**Every interval contains 0.5 except the annotated-target-count row**, which sits below chance. That row
is a cohort-composition property — proteins carrying more annotated residues contribute fewer called
sites — and must not be reported as an inverse predictor of function.

The FDR < 0.25 arm rests on **19 positives**. Its point estimate is the highest in the table and its
interval is the widest; it is reported for endpoint sensitivity and carries no weight.

### 20.3.1 The two cohorts are not endpoint-equivalent — disclose with every replication claim

The yeast primary endpoint is **`qvalue < 0.05`** in at least one condition (Section 4.3 of the
manuscript) — multiplicity-controlled. The human primary endpoint is **raw *p* < 0.05 in either
screen** — uncorrected. They are not the same standard, and the replication claim must say so.

The reason for the choice, stated rather than hidden: the Kennedy release's own FDR columns leave too
few positives to estimate anything.

| Human endpoint | Positives of 1,475 | Rate |
|---|---:|---:|
| Raw *p* < 0.05 either screen (**used as primary**) | **293** | 19.86% |
| FDR < 0.25 either screen | 19 | 1.29% |
| FDR < 0.10 either screen | 12 | 0.81% |
| FDR < 0.05 either screen | 11 | 0.75% |

**The consequence runs against the replication.** An uncorrected call admits false positives among the
sites labelled affected, and non-differential label noise attenuates AUC toward 0.5. Part of the human
0.505573 is therefore attributable to a noisier endpoint rather than to the feature.

**What limits that concern, and by how much.** SIFT reaches 0.571553 [0.528833, 0.615294] on the same
endpoint, in the same cohort, under the same noise. An endpoint too noisy to support any discrimination
could not do that. The attenuation is therefore bounded below the level that would explain an arbitrary
null — but it is not quantified, and no correction for it is applied. A true value of, say, 0.55
attenuated to 0.506 is not excluded by anything computed here.

### 20.4 Paired differences against distance

Same sites, same clustering, computed by `p05.paired_auc_difference`.

| Comparator | Difference | 95% interval | Excludes zero |
|---|---:|---:|:--:|
| Minimum sequence separation | +0.014479 | −0.024783 to +0.053812 | no |
| Site pLDDT | +0.005971 | −0.035674 to +0.047568 | no |
| Inverse relative solvent accessibility | +0.010112 | −0.029647 to +0.048894 | no |
| Annotated target count | −0.047340 | −0.093782 to +0.001689 | no |
| **SIFT minimum (Section 20.7)** | **+0.0537** | **−0.0002 to +0.1085** | **no** |

### 20.5 Permutation null and pair decomposition

Permutation null on the primary: observed **0.505573**, null mean 0.500196, null SD 0.018860, two-sided
**p = 0.7742** over 20,000 permutations. The observed value therefore sits **0.285** standard deviations
from the null centre — (0.505573 − 0.500196) / 0.018860 — which is the form the manuscript reports, to
match the yeast statement's "0.59 standard deviations out".

Ranked pairs **346,326**; within-protein **476**, or **0.14%**, over **134** informative proteins.
The yeast figure is 176 of 6,636, or 2.65%. The across-protein share is therefore **99.86%** here — the
architecture confound is worse in the larger cohort, not better.

Short range: **37** sites within 5 Å, of which **16** are sequence-adjacent (|Δpos| ≤ 2) and **13** fall
in the 1.30–1.35 Å peptide-bond band. The yeast artifact reproduces.

### 20.6 Perturbation classes

Guides in Supplementary Table 2: **26,076**; with a parsable edit at the intended target site:
**25,408**. Substitution at the target residue, by editor:

| Editor | Top substitutions at the target residue |
|---|---|
| ABE8e | S→P 33.0%, S→G 22.3%, silent S→S 17.4%, T→A 9.5% |
| BE4 | S→N 22.1%, silent 21.6%, S→F 17.7% |

**These supersede an earlier pass reporting 36.1% and 11.1%**, which used all S/T/Y-changing edits as the
denominator instead of edits at the intended site. The earlier figures must not be cited.

| Arm | n | positives | proteins | AUC | 95% interval |
|---|---:|---:|---:|---:|---:|
| All sites (reference) | 1,475 | 293 | 793 | 0.505573 | 0.465509–0.545511 |
| **T→A only — clean phospho-null** | **39** | 9 | 36 | 0.470370 | 0.211537–0.732719 |
| S→P only — backbone-disruptive | 390 | 84 | 294 | 0.533185 | 0.460371–0.605643 |
| S→G only | 200 | 36 | 183 | 0.442243 | 0.350312–0.534134 |
| Sites with any silent edit at the target | 487 | 92 | 365 | 0.511585 | 0.443864–0.578183 |
| Single-edit guides only, no bystander | 425 | 90 | 316 | 0.495954 | 0.431124–0.562590 |

Every interval contains 0.5. Two limits are binding on any use of this table:

- The T→A arm is **39 sites with an interval half-width of 0.26**. It is consistent with anything.
- The "any silent edit" arm is **not a negative control**. Those sites carry a silent edit *and* at least
  one non-silent edit; no silent-only arm can be constructed, because every one of the 1,475 cohort sites
  carries a non-silent edit. The screen's 208 essential-splice-site controls carry no phosphosite and
  never enter the cohort.

### 20.7 The positive control

Twelve published features from the Ochoa et al. 2020 59-feature set, each tested as a predictor of the
primary endpoint with the same estimator.

| Feature | n | proteins | AUC | 95% interval | Excludes 0.5 |
|---|---:|---:|---:|---:|:--:|
| **SIFT minimum score** | 997 | 572 | **0.571553** | 0.528833–0.615294 | **yes** |
| **SIFT alanine score** | 997 | 572 | **0.564884** | 0.520492–0.608844 | **yes** |
| Phosphorylation hotspot flag | 110 | 73 | 0.560417 | 0.424687–0.682461 | no |
| Best kinase-motif match score | 1,172 | 650 | 0.533029 | 0.492646–0.572005 | no |
| Predicted disorder | 1,172 | 650 | 0.514729 | 0.469870–0.560236 | no |
| Distance (reference) | 1,475 | 793 | 0.505573 | 0.465509–0.545511 | no |
| Protein abundance | 1,168 | 647 | 0.501351 | 0.455455–0.547335 | no |
| NetPhos maximum | 1,172 | 650 | 0.495505 | 0.454276–0.536742 | no |
| Protein length | 1,172 | 650 | 0.482924 | 0.440315–0.526055 | no |
| Hotspot *p*-value | 110 | 73 | 0.470625 | 0.324085–0.646245 | no |
| Evolutionary-coupling alanine prediction | 61 | 50 | 0.464912 | 0.302196–0.627907 | no |
| Neighbouring PTMs within 21 residues | 1,085 | 616 | 0.461106 | 0.420969–0.502074 | no |
| Protein-interface flag | 45 | 38 | 0.500000 | degenerate | — |

The protein-interface row returned a point estimate and interval of exactly 0.5 on 45 sites; the flag is
constant or near-constant on that support. **It must be reported as uninformative, not as a
chance-level result.**

PhosphoSitePlus curated regulatory sites, tested separately: **84** of 1,475 cohort sites match; hit rate
**22.62%** against 19.70% for the rest, a 2.92-point difference; as a predictor **0.504927
[0.488802, 0.522425]**. It does not function as a positive control.

**The yeast cohort already contained a positive control and the manuscript did not recognise it.**
Section 10 records SIFT at **0.606 [0.522, 0.690]** on the primary common support, lower bound above 0.5.

### 20.8 Bounds on the positive control

Three, all binding.

1. **Multiplicity.** Twelve features were tested at α = 0.05; the expected number of intervals excluding
   0.5 by chance is **0.6**, and two did, both SIFT variants (Pearson r = **0.410** between them).
   Correcting the SIFT-minimum interval for all twelve tests (99.583% percentile interval, same draws)
   gives **0.5070–0.6338**, which still excludes 0.5. The control survives multiplicity correction.
2. **The paired difference against distance contains zero.** On the 997 common-support sites, SIFT minus
   distance is **+0.0537 [−0.0002, +0.1085]**, and distance restricted to that same support rises to
   **0.5178 [0.4698, 0.5658]**. Conservation is not shown to outperform proximity.
3. **The within-protein estimate is uninformative.** Restricted to comparisons inside a single protein,
   SIFT gives **0.6038 [0.4577, 0.7506]** on **265** ranked pairs over **91** informative proteins; the
   interval contains 0.5. Distance on the same 265 pairs is 0.4415. Conservation is not shown to rank
   sites within a protein.

### 20.10 The outcome variable is not a p-value `[REPLICATION]`

Found 2026-08-13 while assessing the work for journal submission. Computed by
`kennedy_replication/endpoint_characterisation.py`, output `endpoint_characterisation.json`.

`analyse.py` calls a site affected at `p3 < 0.05 or p4 < 0.05`. Those columns **track** the minimum of
MAGeCK's two one-sided gene-level p-values, `neg|p-value` and `pos|p-value`, on most rows but **not
all**: `p3` reproduces it on **1,428 of 1,475** and `p4` on **1,372 of 1,475** (Section 22.2). A
minimum of two one-sided tests is not a two-sided p-value. The construction of the remaining 47 and
103 rows is not established, so every figure below describes the released columns, not a definition
verified row by row.

A minimum of two one-sided tests is distributed roughly U(0, 0.5) under the null, so a 0.05 cut-off
admits about twice the nominal rate. Measured on the screens' own non-control rows:

| Screen | Rows | Median min-p | Fraction < 0.05 | Inflation over 0.05 |
|---|---:|---:|---:|---:|
| Screen 3 | 7,217 | 0.244700 | **0.105307** | **2.106x** |
| Screen 4 | 7,217 | 0.239370 | **0.099210** | **1.984x** |

**The direction of the error flatters the paper, under a stated condition.** Label noise attenuates AUC
toward 0.5 **only if it is non-differential** — unrelated to distance. Errors that depend on distance
can move an AUC either way. Nothing here establishes which holds, so the attenuation reading must
carry that condition every time it is used. This must be stated wherever the human null is reported.

#### Endpoint sensitivity on the screen's own lethal controls

The 208 `_Essentialsplicesite` guides should deplete. Median min-p **0.020969**, median `neg|lfc`
**−1.01865**, and only **59.62%** are called at min-p < 0.05. The endpoint misses roughly two of every
five guides that disrupt an essential splice site. This is a positive control for the **endpoint**,
and is distinct from the Ochoa-feature positive control for the **predictor** in Section 20.7.

#### The near-chance reading survives every repair tried

| Outcome definition | n | positives | AUC | 95% interval | Contains 0.5 |
|---|---:|---:|---:|---:|:--:|
| As used: min(neg,pos) < 0.05 either screen | 1,475 | 293 | 0.505573 | 0.465509–0.545511 | yes |
| **Repaired: 2 x min(neg,pos) < 0.05 either screen** | 1,475 | **145** | **0.518170** | 0.461972–0.574069 | **yes** |
| MAGeCK FDR < 0.25 either screen | 1,475 | 19 | 0.613939 | 0.432767–0.781183 | yes |
| **Top decile of |log2 fold change|** — no p-value used | 1,475 | **148** | **0.516716** | 0.462815–0.570750 | **yes** |

The last row uses no p-value construction at all, so it does not inherit the defect. Every definition
contains 0.5. The conclusion is robust to the endpoint; the **precision claim is not**.

#### The precision claim must be restated

Half-widths: as-used **0.040001**, repaired two-sided **0.056049**, top-decile **0.053968**, against
yeast's **0.107398**. The ratio is therefore **2.69x on the anti-conservative endpoint** but
**1.92x repaired** and **1.99x on fold-change magnitude**. Report 1.9x, not 2.7x.

### 20.9 Additions to the Section 13 claim rules

Allowed:

- ~~The near-chance yeast result replicates in an independent human system at 2.7 times the precision:
  interval half-width **0.040** against **0.107**, on **793** protein clusters against 48.~~
  **Restated 2026-08-13 (20.10).** The 0.040 half-width is precision on an anti-conservative label.
  Allowed instead: the near-chance yeast result holds in an independent human system under every
  outcome definition tried, including one using no p-value at all, at **roughly 1.9 times the yeast
  precision** on the repaired endpoints, on 793 protein clusters against 48.
- Poor annotation quality does not explain the null. The experimental-evidence restriction, which
  collapsed to 24 sites in yeast, retains **512** sites here and gives 0.510546 [0.445122, 0.575965].
- At least one published site-level feature separates the classes at a precision excluding chance in
  both systems, so the endpoint is not blind and a feature returning 0.5 on it returns a real negative.
- The across-protein architecture is more extreme in the human cohort: 99.86% of ranked pairs.

Not allowed:

- "Conservation separates the classes and proximity does not." The paired difference is
  +0.0537 [−0.0002, +0.1085] and contains zero (20.8.2). **Any claim of the form "A separates and B does
  not" must cite a paired difference on common support, not two separate intervals.**
- "Conservation is a site-level predictor" or any reading of SIFT as resolving sites within a protein
  (20.8.3).
- Citing the 36.1% / 11.1% substitution frequencies (20.6).
- Treating the "any silent edit" arm as a negative control (20.6).
- Reporting the annotated-target-count AUC of 0.458233 as an inverse predictor of function (20.3).
- Reporting the protein-interface flag as a chance-level result; it is degenerate on 45 sites (20.7).
- Any weight on the FDR < 0.25 arm, which rests on 19 positives (20.3).
- "The replication uses the same endpoint as the yeast analysis." It does not: yeast is
  multiplicity-controlled `qvalue < 0.05`, human is uncorrected raw *p* < 0.05 (20.3.1). Every
  replication claim must carry this disclosure.
- Reporting the human null without stating that an uncorrected endpoint attenuates AUC toward 0.5, or
  claiming that the positive control fully rules that attenuation out — it bounds it, and the bound is
  not quantified (20.3.1).
- Citing the 2.7x precision ratio, or the 0.040 half-width, as the replication's precision (20.10).
  Use 1.9x and 0.056.
- Treating `p3`/`p4` as p-values. They are `min(neg|p-value, pos|p-value)`, inflated about 2.1x and
  2.0x over nominal on the two screens (20.10). Any artifact reporting the human result must say so.
- Reporting the human replication without the endpoint-sensitivity figure: the screen detects only
  59.62% of its own 208 essential-splice-site controls (20.10).
- "The clean phospho-null arm confirms the result" — T→A is 39 sites, half-width 0.26 (20.6).
- Attributing the screen to Coelho et al. (20.1).

## 21. Post-Review Robustness Arms `[POST-HOC]`

Run 2026-08-13 to close two objections the round-1 dossier and the journal assessment both raised.
Code in `outputs/fulbright/research/robustness_arms/`. Both scripts import the frozen estimators and
the frozen distance definition rather than reimplementing them.

### 21.1 QC-inclusive arm — the exclusions were not holding the null up

`qc_inclusive_arm.py`, output `qc_inclusive_arm.json` and `qc_inclusive_cohort.csv`.

Section 19.5 records that the two source quality-control filters removed **38** strain records of which
**34** are screen-positive (89.5%, against 39.6% among the 427 retained), and that the scar-correlation
filter is conditioned on the outcome by construction. No arm retained them. The objection is that
dropping outcome-associated records and then reporting a near-chance estimate manufactures the result.

| Quantity | Value |
|---|---:|
| Excluded records | 38 in 17 proteins (18 sequencing-flagged, 20 scar-flagged) |
| Restorable — protein carries an eligible annotation and a cached model | **10** in 6 proteins |
| Of those, screen-positive | **10 of 10** |
| Of those, scar-flagged | **0** |
| Not restorable, protein carries no eligible annotation | 28 |
| Distinct sites restored | 10, of which 1 already in the primary cohort |
| New sites added to the cohort | **9** |
| Median distance of the restored sites | 44.1352 Å |

**All 20 scar-flagged records fall in proteins carrying no eligible ACT_SITE or BINDING annotation, so
none of them could ever have entered the analysis cohort.** The filter conditioned on the outcome
removes nothing from the estimate. That disposes of the outcome-conditioning objection for this design,
and it is a stronger answer than a sensitivity arm.

| Arm | n | Positive | Proteins | AUC | 95% interval | Half-width |
|---|---:|---:|---:|---:|---:|---:|
| Primary as published | 163 | 79 | 48 | **0.526823** | 0.416170–0.631766 | 0.107798 |
| **QC-inclusive** | **172** | **88** | 48 | **0.501894** | 0.392384–0.608166 | 0.107891 |

200,000 draws, seed 20260728, all retained on both. The primary row reproduces Section 12 exactly,
which is the check that this script's cohort assembly matches the pipeline's.

**Restoring the exclusions moves the estimate toward chance, by −0.024929, not away from it.** The
exclusions were not propping up the near-chance reading; they were mildly working against it.

### 21.2 Bootstrap coverage — measured, not assumed

`bootstrap_coverage.py`, output `bootstrap_coverage.json`. Discussion §3.2 stated that 200,000
resamples control resampling noise without making a percentile interval cover at its stated rate on 48
uneven clusters, and left it there. This measures it.

**Design.** Each replicate rebuilds a cohort with the observed structure: the real protein-size
distribution, prevalence **0.484663**, and a protein-level random intercept whose size is set from the
outcome intraclass correlation measured on the real cohort, **0.127125** (σ_u = 0.381441). Scores are
standard normal with positives shifted, so the population AUC is known; it is computed once at 40x
cohort size for each scenario. The reproduced Kish effective count is **29.037158**, matching Section
12's 29.0, and the reproduced cohort is 163 sites in 48 proteins. 1,000 replicates x 1,000
protein-cluster resamples per scenario, seed 20260728. Before any simulation runs, the script asserts
its AUC equals `p05.auc_from_ranks` on the real cohort to within 1e-12.

| True AUC | Population AUC | Percentile coverage | BCa coverage | Median interval width |
|---:|---:|---:|---:|---:|
| 0.50 | 0.4984 | **0.936** | 0.942 | 0.1769 |
| 0.55 | 0.5483 | 0.941 | 0.945 | 0.1745 |
| 0.60 | 0.5982 | **0.949** | 0.952 | 0.1720 |
| 0.65 | 0.6482 | 0.941 | 0.943 | 0.1656 |
| 0.70 | 0.6982 | 0.948 | **0.953** | 0.1572 |

Monte Carlo standard error at 1,000 replicates and nominal 0.95 is **0.0069**. The percentile
bootstrap covers between **0.936 and 0.949**; the largest shortfall, at the null, is 1.4 percentage
points, or 2.0 Monte Carlo standard errors. BCa covers between 0.942 and 0.953 and is nearer nominal at
every scenario, by 0.2 to 0.6 points.

**What this licenses.** The declared interval is close to nominal on a cohort of this size and shape.
The paper may state a measured coverage rather than an unverified caveat. It may not state that
coverage is exact: the null scenario is the worst case and it is short by about two Monte Carlo
standard errors, which is the scenario the primary estimate sits in.

**Not allowed:** claiming the percentile interval is exactly calibrated; quoting BCa coverage as a
reason the reported intervals are wrong, since the two differ by less than the Monte Carlo error at
four of five scenarios; or extending these coverage figures to the human cohort, whose cluster count
and size distribution differ and which was not simulated.

## 22. Current-Manuscript Human-Endpoint Audit `[AUDIT]`

Added 2026-08-13 after the 24-page two-cohort manuscript was reviewed against the Kennedy source
workbook and current code. This section corrects the description of Section 20 without changing the
stored AUCs. The findings are source-definition and reproducibility failures that must be resolved
before a new human estimate is treated as authoritative.

### 22.1 The two screens measure different phenotypes

The Kennedy workbook states:

- Supplementary Table 3: differential sgRNA abundance **before versus after ABE8e introduction**, a
  proliferation/survival or cell-fitness screen.
- Supplementary Table 4: differential sgRNA abundance **between GFP-high and GFP-low bins**, an NFAT
  reporter-activity screen.

The manuscript's “either screen” label unions two distinct outcomes. It is not one proliferation
endpoint. Any revised analysis must report the two screens separately before considering a declared
union.

### 22.2 The stored columns do not reproduce the claimed directional minimum

Direct comparison of the 1,475 distance-bearing rows in `kennedy_analysis.csv` against the two MAGeCK
gene-summary sheets gives:

| Stored column | Equals `min(neg|p-value, pos|p-value)` | Does not equal it |
|---|---:|---:|
| `p3` | **1,428** | **47** |
| `p4` | **1,372** | **103** |

Reconstructing both directional minima from the source workbook changes the raw `<0.05` union from
**293 to 301** positives and the `<0.025` union from **145 to 148**. The source column's actual
construction must be established before either it or a reconstruction is used. The current AUCs are
valid descriptions of the stored columns; they are not reproducible under the manuscript's stated
column definition.

### 22.3 The current “two-sided” repair does not correct the two-screen union

`endpoint_characterisation.py` defines a repaired call as `p3 < 0.025 OR p4 < 0.025`. Even if each
stored column were the minimum of two directional tests, this corrects direction within a screen and
then unions two screens without correcting that second multiplicity layer. Under independent null
screens, two per-screen 0.05 calls have a union probability of `1 - 0.95^2 = 0.0975`; the observed
stored-column call rate is **145/1,475 = 0.0983**. This is not a 5% site-level endpoint.

The paper must not call this a valid or corrected two-sided endpoint. A revision needs screen-specific
endpoints or a declared correction across both direction and screen, followed by recomputation of the
AUC, interval, controls, and precision statement.

### 22.4 Verification and reconstruction scope

The current human build cascade is **7,425** source phosphosite rows, **6,968** parseable S/T/Y sites,
**6,950** reviewed-UniProt mappings, **6,148** canonical-residue matches, **1,595**
annotation-eligible sites in **818** proteins, and **1,475** sites in **793** proteins with a distance.
The first five stages are recorded in `second_dataset_scan/C_deep_mutational_scanning.md`; the final
cohort and protein count are recorded in `kennedy_replication/kennedy_results.json`. These counts
describe the present files and do not repair the missing upstream candidate-table generator.

The **69/69** report binds the older 11-page
`phase0_calibration/manuscript/preprint_draft_v1.pdf`, not the current 24-page
`phosphosite_proximity_paper.pdf`. Section 20 is outside the three frozen yeast hashes. The earlier
clean-room report also targets the release archive that predates the Kennedy scripts.

The human cohort is not end-to-end rebuildable from the current tree:

- `kennedy_replication/build_cohort.py` starts from
  `second_dataset_scan/kennedy2024_cohort_candidate.csv`, but no script creating that candidate table
  is present;
- UniProt and AlphaFold inputs are cached without a frozen source manifest for this cohort;
- the builder retrieves canonical sequences but does not use them to validate the cached model rows;
- only the estimator is imported from the yeast analysis module, so “same procedure and same code” is
  not an accurate description of the cohort build.

### 22.5 Additions to the claim rules

Not allowed until the audit is resolved:

- describing both Kennedy screens as proliferation;
- stating that every `p3` and `p4` value is `min(neg|p-value, pos|p-value)`;
- calling `p3 < 0.025 OR p4 < 0.025` a valid or corrected two-sided site-level test;
- calling the human result a like-for-like replication without reporting screen-specific results and
  harmonizing the annotation-coincident rule;
- stating that the 69-check verifier or prior clean-room report covers the current humanized paper;
- stating that the human cohort uses the same construction procedure and code as yeast.

## 23. Declared Human Endpoints — the union is withdrawn `[DECLARED]`

Author decision, 2026-08-13. Section 20's union `p3 < 0.05 or p4 < 0.05` is **withdrawn as the human
primary**. It pools two different phenotypes and leaves two multiplicity layers uncorrected. Code:
`kennedy_replication/endpoint_options.py` and `primary_recompute.py`; outputs `endpoint_options.json`
and `primary_recompute.json`. The choice was made after seeing that every candidate primary contains
0.5, and every candidate is reported below, which is the only defence available for a post-hoc
endpoint decision.

### 23.1 Why the union was withdrawn

At a direction-corrected 5%, the two screens call almost disjoint site sets: **65 in the fitness screen
only, 74 in the reporter only, 6 in both**, of 1,475. Jaccard **0.0414**; Spearman between the two log
fold changes **0.1224**. A union across assays that agree on six sites is not one endpoint.

### 23.2 The declared primaries

Two primaries, because these are two experiments.

| Declared | Definition | Positives | AUC | 95% interval | Half-width |
|---|---|---:|---:|---:|---:|
| **A1, fitness** (Supp. Table 3) | `2 × p3 < 0.05` | **71** | **0.559317** | 0.475714–0.640813 | 0.082549 |
| **A2, NFAT reporter** (Supp. Table 4) | `2 × p4 < 0.05` | **80** | **0.486873** | 0.420572–0.554196 | 0.066812 |

Both contain 0.5, on opposite sides. Permutation nulls: A1 observed 0.559317, **p = 0.0920**, 1.677 SD
from centre; A2 observed 0.486873, **p = 0.6836**, 0.408 SD. **A1's p = 0.0920 must be reported plainly
and never rounded to "near chance" without it.**

### 23.3 Full endpoint family, all reported

| Arm | Positives | AUC | 95% interval |
|---|---:|---:|---:|
| Withdrawn union, `p3<0.05 or p4<0.05` | 293 | 0.505573 | 0.465509–0.545511 |
| **A1 fitness, direction-corrected** | 71 | 0.559317 | 0.475714–0.640813 |
| **A2 reporter, direction-corrected** | 80 | 0.486873 | 0.420572–0.554196 |
| B union corrected 4 ways, `2p < 0.025` | 85 | 0.540796 | 0.464247–0.616524 |
| C1 top decile \|log2 FC\|, fitness | 148 | 0.507057 | 0.454537–0.560195 |
| C2 top decile \|log2 FC\|, reporter | 148 | 0.508763 | 0.456513–0.560710 |
| C3 top decile \|log2 FC\|, larger of the two | 148 | 0.516716 | 0.462815–0.570750 |
| D MAGeCK FDR < 0.25 either | 19 | 0.613939 | 0.432767–0.781183 |

**Every one contains 0.5.** C1, C2 and C3 — **three** rows, not two — use no p-value, so they do not
inherit the unreproduced-column problem of Section 22.2.

### 23.4 Dependent quantities, recomputed

Everything that depends on which sites are positive moved with the primary. Section 20's values for
these are superseded.

| Quantity | A1 fitness | A2 reporter |
|---|---:|---:|
| Experimentally-evidenced targets only (512 sites) | 0.574927 [0.446209, 0.699308], 29 pos | 0.491016 [0.390608, 0.589686], 34 pos |
| Ranked pairs | 99,684 | 111,600 |
| Within-protein pairs | **102 (0.1023%)** | **180 (0.1613%)** |
| Informative proteins | 39 | 48 |
| Minimum sequence separation | 0.537644 [0.460435, 0.610878] | 0.557881 [0.492038, 0.624173] |
| Site pLDDT | 0.510709 [0.431314, 0.588473] | 0.547652 [0.483932, 0.612270] |
| Inverse relative solvent accessibility | **0.603648 [0.527526, 0.675313]** | 0.524185 [0.458971, 0.589920] |
| Annotated target count | 0.466584 [0.398333, 0.534749] | 0.444857 [0.382744, 0.508410] |
| SIFT minimum score (997 sites) | **0.646354 [0.564566, 0.722769]** | 0.564520 [0.486261, 0.642506] |
| SIFT alanine score (997 sites) | **0.630042 [0.544713, 0.708286]** | 0.548015 [0.470713, 0.623808] |

Predictor-only quantities do not move and were checked: 37 sites within 5 Å, 16 sequence-adjacent, 13
in the 1.30–1.35 Å band, median distance 41.7549 Å, median site pLDDT 37.19.

### 23.5 Two results that the union concealed

**Inverse relative solvent accessibility has an interval above 0.5 in the fitness screen**: 0.603648
[0.527526, 0.675313]. Its **paired difference against distance is +0.044330 [−0.024533, +0.115051] and
contains zero**, so burial is not shown to outperform distance. Reporting it as "burial, not distance"
was the interval-comparison error again and is retired.

**A structure-free feature outranks the declared predictor in the reporter screen on the paired
comparison, and this is the first paired difference anywhere in this project to exclude zero.** Minimum
sequence separation minus distance is **+0.071008 [+0.004800, +0.136900]**. Its own marginal interval,
0.557881 [0.492038, 0.624173], **contains 0.5**, so it does not separate the classes on its own account.
Every other paired difference in both screens contains zero.

### 23.6 The positive control is screen-dependent

SIFT excludes 0.5 in the fitness screen (0.646354 [0.564566, 0.722769]) and **contains 0.5 in the
reporter screen** (0.564520 [0.486261, 0.642506]). The endpoint-not-blind argument therefore holds for
A1 and is not established for A2.

### 23.7 Additions to the claim rules

Allowed:

- Both declared primaries contain 0.5, as do all six alternative endpoint definitions, including two
  that use no p-value.
- The across-protein architecture is more extreme under the declared primaries than under the union:
  99.90% and 99.84% of ranked pairs.

Not allowed:

- Any use of the withdrawn union 0.505573 as the human primary, or of its dependent Section 20 values
  for the experimental-evidence arm, comparators, paired differences, permutation null, pair
  decomposition, or positive control (23.4 supersedes them).
- **Any precision claim comparing the human and yeast intervals.** Half-widths are 0.0825 and 0.0668
  against yeast's 0.1074, so the ratios are 1.30x and 1.61x; the 1.9x and 2.7x figures are retired.
- Reporting A1 as "near chance" without its permutation **p = 0.0920** (23.2).
- "No feature separates the classes." Inverse RSA does in the fitness screen, and sequence separation
  beats distance there by a paired difference excluding zero (23.5).
- Citing SIFT as a positive control for the reporter screen (23.6).
- "Burial, not distance" or any claim that inverse RSA outperforms distance: the paired difference
  +0.044330 [−0.024533, +0.115051] contains zero (23.5).
- Describing sequence separation as separating the classes in the reporter screen. Its marginal
  interval contains 0.5; only the paired difference against distance excludes zero (23.5).
- Reporting either 23.5 result without stating that both are post hoc and unadjusted for the number of
  features and endpoints examined.
- "The same code computed both cohorts." Only the distance definition and the estimator are shared;
  the human cohort has its own builder, lacks the yeast builder's sequence and model-version checks,
  and starts from a table whose generator is not deposited (22.4–22.5).
- Describing the two screens as one phenotype, or their union as a replication endpoint (23.1).

## 24. Within-Protein Discrimination in the Human Cohort `[POST-HOC]`

Computed 2026-08-13 to answer the second review's central design objection: the pooled AUC is dominated
by comparisons between proteins, and pair counts state that without estimating the within-protein
quantity. Code `kennedy_replication/within_protein.py`; estimator is the frozen
`within_protein_discrimination` imported from the yeast module, so yeast and human are computed the same
way. 20,000 protein resamples, seed 20260728.

| | A1 fitness | A2 reporter | Yeast (Section 11) |
|---|---:|---:|---:|
| Informative proteins | 39 | 48 | 23 |
| Informative sites | 132 | 210 | 112 |
| Within-protein pairs | 102 | 180 | 176 |
| All-positive proteins | 26 | 28 | — |
| All-negative proteins | 728 | 717 | — |
| **Pair-weighted AUC** | **0.627451** [0.452044, 0.767677] | **0.422222** [0.322403, 0.520548] | 0.52841 [0.36842, 0.70900] |
| **Equal-protein-weight AUC** | **0.510684** [0.373932, 0.645299] | **0.383805** [0.271626, 0.498044] | 0.49722 [0.35072, 0.64215] |

**Three of the four human intervals contain 0.5.** The exception is the reporter screen's
equal-protein-weight estimate, **0.383805 [0.271626, 0.498044]**, whose upper endpoint is below 0.5.

**How that one must be reported.** It points the opposite way to the hypothesis: within a protein,
greater distance to an annotated residue is associated with being called. It rests on 48 proteins and
180 pairs; the pair-weighted aggregation on the same data gives 0.422222 with an interval that includes
0.5 at 0.520548; and the fitness screen's two aggregations point the other way. It is one estimate in a
post-hoc family and is not adjusted for it. Report it as a single below-chance interval in one of four
aggregations, not as evidence that proximity is inversely related to function.

**What the table settles.** The within-protein question is now estimated rather than only described, in
both cohorts, and no aggregation in either shows the declared predictor ranking sites within a protein
above chance. The two aggregations disagree in both screens, which is what these pair counts support.

### 24.1 Single-edit, no-bystander arm under the declared primaries

`NUMBERS.md` §20.6 carried this arm under the withdrawn union endpoint only.

| Arm | n | Positive | Proteins | AUC | 95% interval |
|---|---:|---:|---:|---:|---:|
| Single-edit guides, A1 fitness | 425 | 25 | 316 | 0.515900 | 0.391680–0.640514 |
| Single-edit guides, A2 reporter | 425 | 25 | 316 | 0.526800 | 0.415405–0.638762 |

Both contain 0.5. 20,000 draws retained on each.

### 24.2 Claim rules

Allowed:

- No aggregation in either cohort shows the declared predictor ranking sites within a protein above
  chance, and the within-protein question is now estimated rather than inferred from pair counts.
- The pooled estimate is a mostly across-protein quantity: 97.35% in yeast, 99.90% and 99.84% in the two
  human screens.

Not allowed:

- Reporting the reporter screen's equal-protein-weight 0.383805 as evidence of an inverse relationship
  between proximity and function, or without the pair-weighted 0.422222 [0.322403, 0.520548] beside it
  and the statement that it is one of four aggregations in a post-hoc family (24).
- Any claim that the within-protein question is resolved. Every interval here is wide, and the two
  aggregations disagree in both screens.
- Citing §20.6's single-edit arm, which rests on the withdrawn union endpoint; use 24.1.

## 25. Human Endpoints Rebuilt From Source Directions `[DECLARED]`

Author decision 2026-08-14, after an exact-package review found the reporter endpoint stale. Code
`kennedy_replication/rebuild_endpoints.py`, output `rebuilt_endpoints.json`. **This section supersedes
Sections 23.2–23.6 and 24 for the reporter screen.** The fitness screen does not move.

### 25.1 What changed and why

Sections 23 and 24 doubled each screen's **released** per-site column. Section 22.2 records that the
released column reproduces `min(neg|p-value, pos|p-value)` on 1,428 of 1,475 rows for fitness and 1,372
of 1,475 for the reporter, so a doubled released column is not a doubled reconstruction from the two
directions. The endpoint is now defined once, from the source `MAGeCK gene_summary` columns.

| Screen | Positives, released column | Positives, reconstructed | Sites changing |
|---|---:|---:|---|
| Fitness | 71 | **71** | none — no mismatched row crosses the threshold |
| Reporter | 80 | **83** | TBKBP1_S335, PDE4A_S13, BRSK2_S367 |

### 25.2 Declared primaries, rebuilt

| Screen | n | Positives | AUC | 95% interval | Permutation *p* |
|---|---:|---:|---:|---:|---:|
| Fitness | 1,475 | 71 | **0.559317** | 0.475714–0.640813 | 0.0920 |
| Reporter | 1,475 | **83** | **0.486100** | 0.421537–0.552153 | 0.6664 |

### 25.3 Every reporter-dependent value, rebuilt

| Quantity | Superseded (23/24) | **Rebuilt** |
|---|---:|---:|
| Experimentally-evidenced targets, 512 sites | 0.491016 [0.390608, 0.589686], 34 pos | **0.485415 [0.387567, 0.582436], 35 pos** |
| Ranked pairs | 111,600 | **115,536** |
| Within-protein pairs | 180 (0.1613%) | **185 (0.1601%)** |
| Informative proteins | 48 | **50** |
| Within-protein, pair-weighted | 0.422222 [0.322403, 0.520548] | **0.416216 [0.316770, 0.515627]** |
| Within-protein, equal-protein weight | 0.383805 [0.271626, 0.498044] | **0.388452 [0.278904, 0.501814]** |
| Within-protein informative sites | 210 | **217** |
| Minimum sequence separation | 0.557881 [0.492038, 0.624173] | **0.550880 [0.486354, 0.615531]** |
| Site pLDDT | 0.547652 [0.483932, 0.612270] | **0.548162 [0.485547, 0.611391]** |
| Inverse relative solvent accessibility | 0.524185 [0.458971, 0.589920] | **0.521206 [0.456165, 0.585652]** |
| Annotated target count | 0.444857 [0.382744, 0.508410] | **0.441282 [0.381015, 0.502983]** |
| SIFT minimum score, 997 sites | 0.564520 [0.486261, 0.642506] | **0.574228 [0.497254, 0.651030]** |
| SIFT alanine score, 997 sites | 0.548015 [0.470713, 0.623808] | **0.557898 [0.482233, 0.632537]** |
| Single-edit, no bystander | 0.526800 [0.415405, 0.638762] | **0.512146 [0.401635, 0.624320], 26 pos** |

Fitness-screen values are unchanged from Sections 23.4 and 24 and are not restated here.

### 25.4 Two results do not survive the rebuild

**The only paired difference in the project that excluded zero no longer does.** Sequence separation
minus distance in the reporter screen was **+0.071008 [+0.004800, +0.136900]**. Rebuilt it is
**+0.064781 [−0.000591, +0.130482]**, which contains zero. **No paired difference in either cohort now
excludes zero** — the full rebuilt set is in `rebuilt_endpoints.json`.

**The only interval that excluded 0.5 from below no longer does.** The reporter's equal-protein
within-protein estimate was 0.383805 [0.271626, **0.498044**]. Rebuilt it is 0.388452 [0.278904,
**0.501814**]. **No within-protein interval in either cohort excludes 0.5 in either direction.**

What survives from Section 23.5 is the fitness screen's inverse relative solvent accessibility,
0.603648 [0.527526, 0.675313], whose paired difference against distance is +0.044330 [−0.024533,
+0.115051] and contains zero, and the fitness SIFT control at 0.646354 [0.564566, 0.722769]. Both are
fitness-screen quantities and neither moved.

### 25.5 Claim rules

Allowed:

- The endpoint is a doubled reconstruction from the two MAGeCK directional columns, defined once from
  source. Both screens' declared primaries contain 0.5.
- No comparator paired difference in either cohort excludes zero (see 27.7 and 28.4 for the tip-oxygen
  exception), and no within-protein interval in either cohort
  excludes 0.5.

Not allowed:

- **Any use of the superseded reporter values in Sections 23.2–23.6 or 24**, which rest on the released
  column. Section 25.3 is the authority for every reporter-dependent quantity.
- **"Sequence separation beats distance in the reporter screen", or any claim that a paired difference
  excludes zero.** Retired 2026-08-14 (25.4). This was reported in the abstract, Results §2.7.2, Table 4
  and §23.5, and every instance is withdrawn.
- **"The only interval excluding 0.5 from below."** Retired 2026-08-14 (25.4).
- Calling either endpoint "direction-corrected" without stating that it is reconstructed from the two
  directional columns rather than doubled from the released one.

## 26. Human Cohort Rebuilt From Source, And Its Corrected Endpoints `[DECLARED]`

Author decision 2026-08-14, after a final-gap review found the human cohort had no deposited generator.
Code `kennedy_replication/build_candidate_table.py` (candidate table) and `build_cohort.py --cohort`
(distances), outputs `kennedy2024_cohort_candidate.rebuilt.csv`, `kennedy_analysis_corrected.csv` and
`rebuilt_endpoints_corrected.json`. **This section supersedes Sections 22–25 for every human quantity.**

### 26.1 The generator, and what it found

The cascade, against the one recorded in 22.4:

| Stage | 22.4 | Rebuild |
|---|---:|---:|
| Rows in the source phosphosite table | 7,425 | 7,425 |
| Parsable S/T/Y position | 6,968 | 6,968 |
| Gene symbol maps to one reviewed human entry | 6,950 | **6,907** |
| Residue matches the canonical sequence | 6,148 | **6,113** |
| In a protein with an eligible annotation | 1,595 in 818 | **1,590 in 812** |

**1,587 of the 1,595 deposited rows reproduce exactly.** The eight differences all arise from gene
symbols that map to more than one reviewed human entry. The generator's rule is that a site enters only
when its symbol matches exactly one reviewed entry, preferring a primary-name match and accepting a
unique synonym match; an ambiguous symbol is dropped rather than guessed.

**One deposited row is a mismapping.** `TKT_S308` was assigned to `Q16832`, which is DDR2, not
transketolase. Both carry a serine at 308, so the residue check did not catch it. Its distance of
34.26 Å was measured on the wrong protein. The site is unaffected in both screens.

Corrected cohort after the distance stage: **1,471 sites in 788 proteins**, against 1,475 in 793.
Every one of the 1,472 sites common to both cohorts has an identical distance to six decimal places.

### 26.2 Declared primaries, corrected cohort

| Screen | n | Positives | AUC | 95% interval | Permutation *p* (diagnostic) |
|---|---:|---:|---:|---:|---:|
| Fitness | 1,471 | 72 | **0.557829** | 0.473557–0.636888 | 0.0985 |
| Reporter | 1,471 | **82** | **0.483301** | 0.418057–0.549886 | 0.6234 |

Superseded values, 25.2: fitness 0.559317 [0.475714, 0.640813] on 71 positives; reporter 0.486100
[0.421537, 0.552153] on 83. **Both intervals still contain 0.5, and both moved by less than 0.003.**

Reporter sites changing classification between the released column and the reconstruction, on the
corrected cohort: BRSK2_S367, DDX47_S9, NR1D1_S280, PDE4A_S13, TBKBP1_S335 (81 → 82).

### 26.3 Every dependent quantity, corrected

| Quantity | Fitness | Reporter |
|---|---:|---:|
| Experimentally-evidenced targets, 512 sites | 0.575569 [0.448808, 0.702799], 29 pos | 0.477972 [0.375991, 0.577000], 34 pos |
| Ranked pairs | 100,728 | 113,898 |
| Within-protein pairs | 102 (0.1013%) | 184 (0.1615%) |
| Across-protein share | 99.8987% | 99.8385% |
| Informative proteins | 39 | 49 |
| Within-protein, pair-weighted | 0.627451 [0.452044, 0.767677] | 0.413043 [0.312500, 0.510490] |
| Within-protein, equal-protein weight | 0.510684 [0.373932, 0.645299] | 0.375972 [0.266300, **0.489213**] |
| Single-edit guides only | 0.515900 [0.391680, 0.640514], n=425 | 0.512146 [0.401635, 0.624320], n=425 |
| SIFT minimum score (positive control) | 0.646934 [0.564873, 0.723475] | 0.574725 [0.496691, 0.650868] |
| SIFT alanine score (positive control) | 0.629982 [0.544857, 0.707810] | 0.557941 [0.481626, 0.632690] |

Comparators and their paired differences against distance, corrected cohort:

| Comparator | Fitness AUC | Paired difference | Reporter AUC | Paired difference |
|---|---:|---:|---:|---:|
| Minimum sequence separation | 0.542183 [0.465347, 0.614078] | −0.015646 [−0.089474, +0.059088] | 0.548824 [0.484557, 0.612993] | +0.065524 [−0.001087, +0.130542] |
| Site pLDDT | 0.512330 [0.433425, 0.588918] | −0.045499 [−0.121255, +0.032181] | 0.545348 [0.482242, 0.608598] | +0.062047 [−0.005566, +0.130271] |
| Inverse relative solvent accessibility | 0.606981 [0.530278, 0.677533] | +0.049152 [−0.018584, +0.119612] | 0.518806 [0.455161, 0.583671] | +0.035505 [−0.026693, +0.096394] |
| Annotated target count | 0.460736 [0.393114, 0.528528] | −0.097093 [−0.191701, +0.005550] | 0.444701 [0.384016, 0.506025] | −0.038600 [−0.116311, +0.037641] |

**No paired difference in either screen excludes zero.** The fitness screen's inverse relative solvent
accessibility interval lies above 0.5, as a post hoc comparator.

### 26.4 The reporter within-protein exclusion is one protein carrying one pair `[RETIRED]`

The reporter's equal-protein-weight within-protein interval takes three values across three defensible
constructions of the same quantity:

| Construction | Estimate | Interval | Excludes 0.5 below |
|---|---:|---:|:--:|
| Released column, deposited cohort (23.5, retired) | 0.383805 | 0.271626–0.498044 | yes |
| Reconstructed endpoint, deposited cohort (25.4) | 0.388452 | 0.278904–0.501814 | no |
| Reconstructed endpoint, corrected cohort (26.3) | 0.375972 | 0.266300–0.489213 | yes |

The third row was checked against source on 2026-08-14 and does not survive. The mechanism was verified
directly.

**The whole difference is one protein contributing one pair.** The deposited cohort has 50 informative
proteins and the corrected cohort 49. The single protein in the deposited set and not the corrected one
is Q9HB75 (PIDD1), which carries exactly two sites: S299, positive, at 24.909126 Å, and S304, negative,
at 32.818466 Å. That is one positive–negative pair and a per-protein AUC of exactly 1.0. No protein
shared by the two cohorts changed its within-protein AUC. PIDD1 was dropped by the generator's mapping
rule, not by evidence: `cache/genemap.json` records `PIDD1 -> None` because the symbol matches more than
one reviewed human entry. Restoring it returns the estimate to the deposited value and the interval
across 0.5.

**The estimator has 49 units, and most are coin flips.** Of the 49 informative proteins, 47 carry
exactly one positive site and 14 contribute exactly one positive–negative pair, so their per-protein AUC
is forced to 0 or 1. Thirty-two of the 49 per-protein AUCs are degenerate at exactly 0 or exactly 1. The
49 values have standard deviation 0.401247 and standard error 0.057321; a one-sample *t* against 0.5
gives *t*(48) = 2.164, *p* = 0.0355, and a within-protein permutation null over 50,000 draws gives
*z* = −2.134, two-sided *p* = 0.0324. The 184 within-protein pairs are 0.1615% of the screen's 113,898
ranked pairs.

**It is marginal on its own terms.** The interval is 0.222913 wide and its upper bound sits 0.010787
below 0.5, which is 4.8% of the width. Flipping any single one of the 14 forced coin flips from 0 to 1
puts the upper bound at 0.510060. Leave-one-protein-out over all 49 never crosses 0.5, but the closest
removal reaches 0.499976. The exclusion is not a Monte Carlo artefact — across 40 bootstrap seeds the
97.5th percentile ranges 0.486544 to 0.490914 — which makes it sampling fragility rather than noise.

**The same data under the sibling aggregation shows nothing.** The identical 49 proteins and 184 pairs
pair-weighted give 0.413043 [0.312500, 0.510490]. The reporter primary over all 113,898 pairs is
0.483301 [0.418057, 0.549886] with a diagnostic permutation *p* of 0.6234. The fitness screen's
equal-protein weight is 0.510684 [0.373932, 0.645299]. One of four constructions of this quantity
excludes 0.5.

This is the sixth positive finding in this project to fail on rebuild. It is retired on the day it
appeared and must not be reported as a result.

### 26.6 Candidate endpoint family, corrected cohort

Code `kennedy_replication/endpoint_options.py --cohort kennedy_analysis_corrected.csv`, output
`endpoint_options_corrected.json`. These supersede 23.3 for every arm.

| Arm | Positives | AUC | 95% interval |
|---|---:|---:|---:|
| Fitness alone, reconstructed and doubled (declared) | 72 | 0.557829 | 0.473557–0.636888 |
| Reporter alone, reconstructed and doubled (declared) | 82 | 0.483301 | 0.418057–0.549886 |
| Union of both screens, uncorrected (withdrawn) | 296 | 0.504733 | 0.464532–0.544839 |
| Union, 0.05 split over two directions and two screens | 86 | 0.541860 | 0.465780–0.615698 |
| Top decile of \|log2 fold change\|, fitness | 148 | 0.508611 | 0.454726–0.561404 |
| Top decile of \|log2 fold change\|, reporter | 148 | 0.505909 | 0.454088–0.558178 |
| Top decile of \|log2 fold change\|, larger of the two | 148 | 0.510597 | 0.456129–0.564164 |
| MAGeCK FDR below 0.25 in either screen | 19 | 0.614325 | 0.427322–0.777787 |

Reporter alone on the **released** column, corrected cohort, for comparison only: 81 positives,
0.484501 [0.419490, 0.550190]. The declared reporter arm is the reconstruction, 82 and 0.483301.

Screen agreement on the corrected cohort: 66 fitness-only, 76 reporter-only, 6 both, Jaccard 0.0408,
Spearman of the two log fold changes 0.1193.

**Every arm's interval contains 0.5.**

### 26.7 Yeast multiplicity family support range

The 255-estimate yeast family's per-estimate support runs from **16 to 166 sites**, taken from
`phase0_5/results/` — PAE grid 34–166, confidence strata 27–166, cohort sensitivity 16–166, feature
definitions 107–163, continuous outcomes 163. An earlier draft gave this range as "27 to 1,475"; 1,475
was the human cohort size and no human estimate is in the yeast family.

### 26.5 Claim rules

Allowed:

- The human cohort rebuilds from the Kennedy supplement and UniProt, reproducing 1,587 of 1,595 rows.
- One deposited site was assigned to the wrong protein and is corrected.
- Both declared primaries contain 0.5 on the corrected cohort, and neither moved by more than 0.003.
- No **comparator** paired difference excludes zero. The tip-oxygen predictor of 28.1 is not a comparator
  in this sense and its fitness-screen difference does exclude zero; any blanket statement that no paired
  difference excludes zero must be scoped to the comparators of 27.4.
- The reporter within-protein equal-protein interval reverses across constructions because one protein
  carrying one pair enters or leaves the cohort (26.4). No within-protein interval is reported as
  excluding 0.5.

Not allowed:

- **Any human number from Sections 22–25 in a reader-facing document.** 26.2 and 26.3 are the authority.
- **"The reporter ranks affected sites farther from targets within a protein", or any statement that a
  within-protein interval excludes 0.5.** Retired 2026-08-14 (26.4); it does not survive
  checking, and the mechanism is a single protein with a single pair.
- Any claim that the corrected cohort changes a conclusion. It does not.
- Citing 1,475 sites or 793 proteins for the human cohort; it is 1,471 in 788.

## 27. Human Cohort After The Exact-Canonical AlphaFold Audit `[DECLARED]`

Author decision 2026-08-18, after a model-provenance audit found the AlphaFold downloader had taken the
first API result rather than the exact canonical entry. **This section supersedes Section 26, and with it
Sections 22–25, for every human quantity.** Code `kennedy_replication/build_candidate_table.py`
(candidate table, `--offline`), `build_cohort.py --cohort` (distances), `rebuild_endpoints.py` and
`endpoint_options.py`. Outputs `kennedy_analysis_corrected.csv`, `rebuilt_endpoints_1470.json` and
`endpoint_options_1470.json`.

### 27.1 What the audit changed

The original downloader accepted the first entry the AlphaFold API returned, which was an **isoform
model for 11 accessions**. Three (Q96EY9, Q14669, P24928) were replaced with exact canonical AFDB v6
models. Eight (O43149, Q8TD26, O94854, Q63HN8, Q5T4S7, O75962, Q9Y4D8, Q9P2D1) had no exact canonical
entry and were removed. All 11 displaced files are retained under
`kennedy_replication/cache/af_superseded_wrong_isoform/`.

| Quantity | Section 26 | **Section 27** |
|---|---:|---:|
| Candidate sites / proteins | 1,590 / 812 | 1,590 / 812 |
| Analysed sites / proteins | 1,471 / 788 | **1,470 / 787** |
| Exact-canonical v6 models | not asserted | **789 of 812 candidate accessions** |

The only previously analysed distance-bearing row removed is **CHD6 S27 (Q8TD26)**. Four TRIO rows
(O75962) already carried no distance. Two network-disabled source-to-cohort rebuilds with canonical-model,
model-sequence and residue-number assertions both produced 1,470 sites in 787 proteins.

Bound artifacts, SHA-256:

| File | Hash |
|---|---|
| `kennedy_analysis_corrected.csv` | `90d4be92fa92c738ec65f84a77d4c766199000e548cc87efbcd79b3d4417557b` |
| `cache/af_v6_manifest.csv` | `e9f39d6705fa13f91b40d8e4edd5c45fc23425cb17cc32f0a35fd6d34ac82cc5` |
| `human_rebuild_manifest.json` | `7b74f039397f0a9269e703ebea3e3ec510f43041499ae8f4e8466c9ce1045248` |
| `kennedy_analysis_pre_isoform_fix.csv` (superseded) | `660bdfcc41bae4ddd6e33a7686be090c7fda986e8e5cd2917119e560074e0b03` |

### 27.2 Cohort cascade

7,425 rows in the source phosphosite table → 6,968 with a parsable S/T/Y position → 6,907 whose gene
symbol maps to **exactly one** reviewed human entry → 6,113 whose residue matches the canonical sequence
→ 1,590 sites in 812 proteins carrying an eligible annotation → **1,470 sites in 787 proteins** with a
distance on an exact-canonical AFDB v6 model.

Against the superseded 1,595-row candidate table: 1,587 shared, 8 removed as ambiguous symbol mappings,
3 newly resolved. A symbol matching more than one reviewed human entry is dropped rather than assigned.

### 27.3 Declared primaries

| Screen | n | Positives | AUC | 95% interval | Permutation (diagnostic) |
|---|---:|---:|---:|---:|---:|
| Fitness | 1,470 | 72 | **0.557632** | 0.472659–0.638588 | 1.642 SD, *p* 0.0991 |
| Reporter | 1,470 | **82** | **0.483113** | 0.418242–0.550433 | 0.526 SD, *p* 0.6000 |

Superseded (26.2): fitness 0.557829 [0.473557, 0.636888]; reporter 0.483301 [0.418057, 0.549886].
**Both intervals contain 0.5 and both moved by less than 0.0003.**

The released per-site column reproduces the reconstructed directional minimum on **1,424 of 1,470** rows
for fitness and **1,370 of 1,470** for the reporter, so the endpoint is reconstructed from the two
directional columns. Reporter sites changing classification: BRSK2_S367, DDX47_S9, NR1D1_S280,
PDE4A_S13, TBKBP1_S335 (81 → 82). Fitness does not move.

Screen agreement: **66 fitness-only, 76 reporter-only, 6 both**, 1,322 neither; Jaccard 0.0405;
Spearman of the two log fold changes 0.1195.

### 27.4 Every dependent quantity

| Quantity | Fitness | Reporter |
|---|---:|---:|
| Experimentally-evidenced targets, 512 sites in 286 proteins | 0.575569 [0.448808, 0.702799], 29 pos | 0.477972 [0.375991, 0.577000], 34 pos |
| Ranked pairs | 100,656 | 113,816 |
| Within-protein pairs | 102 (0.1013%) | 184 (0.1617%) |
| Across-protein share | 99.8987% | 99.8383% |
| Informative proteins / sites | 39 / 132 | 49 / 215 |
| Within-protein, pair-weighted | 0.627451 [0.452044, 0.767677] | 0.413043 [0.312500, 0.510490] |
| Within-protein, equal-protein weight | 0.510684 [0.373932, 0.645299] | 0.375972 [0.266300, **0.489213**] |
| Single-edit guides only | 0.515900 [0.391680, 0.640514], n=425 | 0.512146 [0.401635, 0.624320], n=425 |
| SIFT minimum score (positive control) | 0.646934 [0.564873, 0.723475] | 0.574725 [0.496691, 0.650868] |
| SIFT alanine score (positive control) | 0.629982 [0.544857, 0.707810] | 0.557941 [0.481626, 0.632690] |

Comparators and their paired differences against distance:

| Comparator | Fitness AUC | Paired difference | Reporter AUC | Paired difference |
|---|---:|---:|---:|---:|
| Minimum sequence separation | 0.542024 [0.463942, 0.615126] | −0.015608 [−0.089816, +0.060014] | 0.548649 [0.484514, 0.613753] | +0.065536 [−0.000634, +0.130758] |
| Site pLDDT | 0.512011 [0.433458, 0.589407] | −0.045621 [−0.121755, +0.033591] | 0.545038 [0.481542, 0.608744] | +0.061925 [−0.006457, +0.129162] |
| Inverse relative solvent accessibility | 0.606829 [0.531350, 0.678545] | +0.049197 [−0.018812, +0.119892] | 0.518644 [0.454335, 0.585084] | +0.035531 [−0.026992, +0.096512] |
| Annotated target count | 0.460648 [0.392095, 0.527440] | −0.096984 [−0.193458, +0.005646] | 0.444665 [0.384382, 0.505258] | −0.038448 [−0.117322, +0.038368] |

**No paired difference in either screen excludes zero.** The fitness screen's inverse relative solvent
accessibility interval lies above 0.5 as a post hoc comparator.

### 27.5 Candidate endpoint family

All arms reconstructed from the four source MAGeCK directional columns except the withdrawn uncorrected
union and the source FDR arm, which use the released columns.

| Arm | Positives | AUC | 95% interval |
|---|---:|---:|---:|
| A1 fitness alone, doubled directional minimum (declared) | 72 | 0.557632 | 0.472659–0.638588 |
| A2 reporter alone, doubled directional minimum (declared) | 82 | 0.483113 | 0.418242–0.550433 |
| Union of both screens, uncorrected (withdrawn) | 296 | 0.504498 | 0.464445–0.544626 |
| B union, Bonferroni over four directional p-values | **88** | **0.538819** | 0.462346–0.614406 |
| C1 top decile of \|log2 fold change\|, fitness | 147 | 0.508266 | 0.454556–0.560941 |
| C2 top decile of \|log2 fold change\|, reporter | 147 | 0.504024 | 0.451256–0.556691 |
| C3 top decile of \|log2 fold change\|, larger of the two | 147 | 0.507618 | 0.453568–0.561438 |
| D MAGeCK FDR below 0.25 in either screen | 19 | 0.614241 | 0.428625–0.781056 |

**Every arm's interval contains 0.5.** Section 26.6's B arm (86 sites, 0.541860) rested on released
columns and is superseded; the interrupted 1,471-site value (88 sites, 0.539013) is also superseded.

### 27.6 The reporter within-protein exclusion is unchanged and stays retired

The reporter's equal-protein-weight interval is **0.375972 [0.266300, 0.489213]** — numerically identical
to 26.3, because CHD6 S27 is not in a protein carrying both outcome classes and no informative protein
changed. Section 26.4's refutation therefore stands without modification: the exclusion is produced by
PIDD1, one protein contributing one pair, dropped by the ambiguous-symbol rule. It remains **retired** and
must not be reported as a result.

### 27.7 Claim rules

Allowed:

- The human cohort is **1,470 sites in 787 proteins**, rebuilt offline from source with canonical-model,
  model-sequence and residue-number assertions.
- Both declared primaries contain 0.5 and every candidate endpoint arm contains 0.5.
- No **comparator** paired difference excludes zero. Scope every blanket statement of this to the four
  comparators of 27.4: the tip-oxygen predictor of 28.1 has a fitness-screen paired difference of
  +0.004024 [+0.000120, +0.007827] that does exclude zero, and 28.4 records why it is not a performance
  claim. An unqualified "no paired difference excludes zero" is now false.
- 789 of 812 candidate accessions have an exact-canonical AFDB v6 model; 11 isoform models were displaced.

Not allowed:

- **Any human number from Sections 22–26 in a reader-facing document.** 27.3–27.5 are the authority.
- Citing 1,471 sites, 788 proteins, 0.557829, 0.483301, or the 86- or 88-site B arm of Section 26.6.
- Reporting any within-protein interval as excluding 0.5 (27.6, 26.4).
- Treating `rebuilt_endpoints_corrected.json` or `endpoint_options_source_corrected.json` as current;
  both are superseded by `rebuilt_endpoints_1470.json` and `endpoint_options_1470.json`.

## 28. Reviewer-Proposed Analyses, 2026-08-18 `[DECLARED POST HOC]`

Four analyses proposed by David Chang after all other results were known. Every estimate here is post
hoc and unadjusted, and none was in any declared family. Code `tip_atom/`, `range_restricted/`,
`within_protein_combined/`. This section adds to Section 27; it supersedes nothing.

### 28.1 Distance from the phospho-accepting oxygen

The declared predictor takes the shortest heavy-atom separation, backbone included. The phosphate
attaches to the side-chain tip — OG in serine, OG1 in threonine, OH in tyrosine — and consecutive
residues are covalently bonded backbone-to-backbone at a fixed distance, so under the declared rule any
adjacent pair returns that constant. The alternative measures from the tip oxygen to any non-hydrogen
atom of the target; everything else is unchanged.

| Cohort | Declared | Tip oxygen | Paired difference, tip − declared |
|---|---:|---:|---:|
| Yeast, 163 sites | 0.526823 [0.416106, 0.630551] | **0.526673** [0.415600, 0.633201] | −0.000151 [−0.006507, +0.008175] |
| Human fitness, 1,470 | 0.557632 [0.472659, 0.638588] | **0.561656** [0.477035, 0.642158] | **+0.004024 [+0.000120, +0.007827]** |
| Human reporter, 1,470 | 0.483113 [0.418242, 0.550433] | **0.484589** [0.418935, 0.552177] | +0.001476 [−0.001996, +0.005013] |

**The peptide-bond band is a property of the atom-selection rule.** Sites in the 1.30–1.35 Å band go
from 5 to **0** in yeast and from 13 to **0** in human. The shortest tip distance is 2.6457 Å in yeast
and 2.5610 Å in human. The five yeast sites at 1.33–1.34 Å move to 3.44–4.15 Å. Spearman correlation
between the two predictors is 0.9962 in yeast.

Subtracting a constant for the phosphate's reach cannot change any of these AUCs: the AUC is a rank
statistic and a constant offset leaves every ranking identical. It moves sites across a fixed cut-off
and so bears only on 28.2.

### 28.2 Restricted range and the declared cut-off grid

Methods §4.5 declares four descriptive cut-offs — 5, 8, 10 and 15 Å — and all four are run. An earlier
version of the script ran only three and dropped 8 Å without comment, which made the reported grid a
selected subset of an already-declared grid; that version's output is superseded.

AUC restricted to sites inside each cut-off:

| Cut-off | Yeast | Human fitness | Human reporter |
|---|---:|---:|---:|
| All range | 0.526823 [0.416106, 0.630551] | 0.557632 [0.472659, 0.638588] | 0.483113 [0.418242, 0.550433] |
| 15 Å | 0.530702 [0.310923, 0.722222], n=43 | 0.538570 [0.405228, 0.690324], n=175 | 0.406961 [0.242464, 0.581765], n=175 |
| 10 Å | 0.447964 [0.224484, 0.697537], n=30 | 0.656977 [0.442767, 0.819373], n=94 | 0.399267 [0.057471, 0.722222], n=94 |
| 8 Å | 0.291667 [0.041667, 0.607143], n=20 | 0.640693 [0.441836, 0.809091], n=73 | n=73, 2 affected; no interval |
| 5 Å | 0.458333 [0.111111, 0.833333], n=10 | 0.575758 [0.114286, 0.852941], n=37 | n=37, 1 affected; no interval |

**Every restricted interval contains 0.5.** Twelve threshold contrasts were computed; one excludes zero
(28.4). Expected at 5% across twelve is 0.6, and P(at least one) is 0.46.

Affected-rate contrasts, inside minus outside, protein-cluster interval:

| Cut-off | Yeast | Human fitness | Human reporter |
|---|---:|---:|---:|
| 15 Å | +0.100 [−0.109, +0.300] | **+0.061 [+0.009, +0.119]** | −0.005 [−0.039, +0.033] |
| 10 Å | +0.101 [−0.118, +0.304] | +0.039 [−0.019, +0.104] | −0.025 [−0.059, +0.018] |
| 8 Å | +0.131 [−0.119, +0.380] | +0.049 [−0.020, +0.130] | −0.030 [−0.063, +0.015] |
| 5 Å | −0.090 [−0.449, +0.319] | +0.061 [−0.026, +0.171] | −0.029 [−0.066, +0.035] |

### 28.3 Combined within-protein estimate and the conditional model

The two human screens share all 1,470 sites and are not independent, so only one enters the combination.
**The fitness screen is designated**, being the proliferation and survival readout the source experiment
leads with; the reporter substitution is a sensitivity arm and is not pooled with it.

| Arm | Equal-protein within-protein AUC | Informative proteins / sites |
|---|---:|---:|
| Yeast | 0.497222 [0.351208, 0.643237] | 23 / 112 |
| Human fitness | 0.510684 [0.373932, 0.645299] | 39 / 132 |
| Human reporter | 0.375972 [0.266300, 0.489213] | 49 / 215 |

| Combination | Fixed effect | Random effects | Q, df, I² |
|---|---:|---:|---:|
| **Yeast + human fitness (designated)** | **0.504446 [0.405051, 0.603841]** | 0.504446 [0.405051, 0.603841] | 0.0175, 1, 0.00% |
| Yeast + human reporter (sensitivity) | 0.420611 [0.332015, 0.509207] | 0.427045 [0.309707, 0.544384] | 1.6737, 1, 40.25% |

The designated combination rests on **278 within-protein pairs in 62 proteins over 244 sites** (176
yeast pairs plus 102 human fitness pairs). **Both combinations contain 0.5.**

Conditional logistic regression stratified on protein, distance per 10 Å:

| Cohort | Odds ratio | 95% interval | *p* | Strata / sites |
|---|---:|---:|---:|---:|
| Yeast | 0.983341 | 0.772926–1.251036 | 0.8912 | 23 / 112 |
| Human fitness | 0.904768 | 0.706983–1.157885 | 0.4265 | 39 / 132 |
| Human reporter | 1.125185 | 0.936080–1.352492 | 0.2090 | 49 / 215 |

**All three contain an odds ratio of 1.**

### 28.4 Two positives, both retired the day they appeared `[RETIRED]`

**The 15 Å cut-off contrast in the human fitness screen**, +0.061 [+0.009, +0.119]. Three independent
adversarial checks refuted it and the mechanism was verified directly.

It is not distance. Sites inside 15 Å are a structurally distinct subset: mean relative solvent
accessibility **0.346 against 0.618**, mean pLDDT **74.99 against 42.67**, mean annotated target count
16.28 against 11.13. They are buried residues in folded, well-modelled domains; the rest are exposed
residues in poorly modelled tails. Adjusting the contrast for relative solvent accessibility alone moves
the inside-15 Å coefficient from 0.9688 (*p* = 0.0007) to 0.5304 (*p* = 0.1208). Burial is already
registered in 27.4 as a comparator with an interval above 0.5, so the covariate was not chosen to
explain this away.

It also does not survive its own family. Twelve threshold contrasts were computed and this is the only
one excluding zero; the bootstrap two-sided *p* is 0.0187 and a Šidák correction over the grid gives an
interval containing zero. The AUC on the same 175 sites is 0.538570 [0.405228, 0.690324] and contains
0.5, and the same 175 sites in the reporter screen give −0.005 [−0.039, +0.033], the opposite sign.

It is **not** a cut-off artefact, and must not be described as one: it survives leave-one-protein-out at
all 787 proteins, survives moving the cut-off to 12, 14, 16 and 18 Å, and excludes zero under 20 of 20
bootstrap seeds. The reason it fails is confounding and multiplicity, not instability.

**The tip-oxygen paired difference in the human fitness screen**, +0.004024 [+0.000120, +0.007827].
Refuted as a performance claim. Expressed as pairs, the two predictors give the same ordering on
**99,013 of the 100,656 ranked pairs, 98.368%**. Of the 1,643 ordered differently the tip predictor wins
1,024 and the declared predictor 619, a net **405 of 100,656**, which is +0.004024 exactly. An earlier
draft of this section gave 435 of 99,258 and 98.383%; those came from the superseded 1,469-site run and
are retired. An AUC gain of 0.004 from predictors correlating at 0.996 is
statistically distinguishable from zero and substantively negligible. It is reported as the atom choice
not mattering to the conclusion, never as the tip predictor outperforming the declared one.

### 28.5 Claim rules

Allowed:

- The peptide-bond band is a consequence of including backbone atoms and disappears entirely under the
  tip-oxygen definition, in both cohorts.
- The distance heuristic fails in its most mechanistically faithful form: every tip-oxygen interval
  contains 0.5 and no restricted interval excludes it.
- No aggregation of within-protein comparisons across two organisms separates the classes; the
  designated combination is 0.504446 [0.405051, 0.603841] on 278 pairs in 62 proteins.
- These cohorts hold too few short-range sites to test the heuristic where it is claimed: 10 of 163 in
  yeast within 5 Å, of which 5 are peptide-bond neighbours, and 37 of 1,470 in human, of which 13 are.

Not allowed:

- **Any claim that proximity within 15 Å raises the affected rate.** Retired 2026-08-18 (28.4).
- **Describing the 15 Å contrast as a cut-off artefact or as unstable.** It is confounded with burial and
  unadjusted for its family; it is not unstable, and saying so would be false.
- **Any claim that the tip-oxygen predictor outperforms the declared one.** Retired 2026-08-18 (28.4).
- Reporting any 28.2 or 28.3 estimate without stating that it is post hoc and unadjusted.
- Citing the superseded three-cut-off grid, or any tip-oxygen figure computed on 1,469 sites.

### 28.6 Quantities the manuscript reports that 27 and 28 did not declare `[DECLARED POST HOC]`

A package audit on 2026-08-18 found reader-facing values with no entry in the current authority. All are recomputed on the deposited 1,470-site cohort and registered here.

| Quantity | Value |
|---|---|
| 15 Å threshold decomposition, fitness | 18 affected of 175 inside; 54 of 1,295 outside |
| Sites with an FDR below 0.05 in either screen | 11 |
| Sites with an FDR below 0.25 in either screen | 19 |
| Sites within 5 Å with \|Δposition\| ≤ 2 | 16 of 37 |
| Sites within 5 Å in the 1.30–1.35 Å band | 13 of 37 |
| SIFT common support | 997 sites |
| Experimentally-evidenced arm | 512 sites in **286** proteins |
| Yeast sites within 5 Å with \|Δposition\| ≤ 2 | 6 of 10 |
| Yeast sites within 5 Å in the peptide-bond band | 5 of 10 |

### 28.7 The threonine-to-alanine arm is not estimable `[RETIRED]`

An earlier draft reported an AUC of 0.470 [0.211537, 0.732719] on 39 threonine-to-alanine sites. That
value comes from Section 20.6, which rests on the **withdrawn union endpoint** and the superseded
1,475-site cohort, and Section 23.7 already bars its dependent values.

Recomputed on the 1,470-site cohort under the declared endpoints, the 39 clean T→A sites carry **1
affected site under the fitness endpoint and 0 under the reporter endpoint**. No interval is estimable
in either screen. The arm is retired: report the counts or nothing, never an AUC.

### 28.8 Endpoint sensitivity from the screen's own controls `[DECLARED]`

Required by Section 20.9, which Sections 22–28 do not repeal. The source experiment carries 208
essential-splice-site controls; **59.62% are detected at a minimum directional *p* below 0.05**
(`kennedy_replication/endpoint_characterisation.json`, `screen3.essential_splice_controls`). The figure
is guide-level and unaffected by the cohort rebuilds. The declared endpoint doubles that minimum, so it
is stricter and the sensitivity under the declared endpoint is lower than 59.62%.

Allowed: stating that fewer than three in five of the screen's own positive controls clear the
unadjusted threshold, and that the declared endpoint is stricter still.

Not allowed: presenting 59.62% as the sensitivity of the declared endpoint.
