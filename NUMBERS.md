# NUMBERS.md — Canonical Numbers for the Phosphosite-Distance Calibration Preprint

Refrozen **2026-07-29 16:33 CDT** after clean-environment reconciliation and deterministic
serialization of machine-precision continuous-model fields. Cohorts, estimates, intervals, and every
reported scientific value are unchanged. This file is the sole numerical authority for manuscript and
release work.

Editorial authority was extended on **2026-07-30** to catalogue the source and method metadata in
Section 16 and to resolve a duplicated tyrosine-subgroup bootstrap in the reader-facing manuscript.
The frozen numerical outputs and their hashes are unchanged.

Extended again on **2026-08-12** with Section 17 (figure provenance, 2026-08-03) and Section 18
(round-2 authorized analyses). Section 18 values are `[POST-HOC]`, not `[REPO]`: they come from scripts
under `robustness/results/round2/` that verify the three frozen hashes below before computing, import the
frozen estimators without reimplementation, and write nothing into the frozen tree. The frozen numerical
outputs and their hashes are unchanged by either extension.

Frozen source hashes (SHA-256):

- `results/statistics.json` — `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`
- `results/analysis_final.csv` — `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`
- `robustness/results/robustness_statistics.json` — `3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b`

The pre-repair audit baseline was independently hash-verified before the rerun: `73398b41…566e`, `a42f8d18…bceb`, and `e82b7e11…8434`, respectively. `[REPO]` means the value is emitted by the current seeded repository pipeline. Manuscripts, tables, figures, and release checks must take numerical claims from this file and reconcile them to the frozen outputs above.

---

## 1. Primary Estimand `[REPO]`

The **primary cohort excludes the three annotation-coincident substitutions**. The inclusive cohort is a named sensitivity and must appear beside the primary result in the abstract.

| Arm | n | Proteins | Positive | AUC | Protein-cluster 95% CI |
|---|---:|---:|---:|---:|---:|
| **Primary: annotation-coincident substitutions excluded** | **163** | **48** | **79** | **0.5268234** | **0.416744–0.631539** → **0.527 [0.417, 0.632]** |
| **Sensitivity: annotation-coincident substitutions included at 0 Å** | **166** | **50** | **82** | **0.5441347** | **0.435756–0.648746** → **0.544 [0.436, 0.649]** |

Both protein-cluster intervals use **200,000 draws** and seed **20260729**. The substitution-level dependence diagnostics use 200,000 draws and are **0.436735–0.617369** for primary and **0.455384–0.632703** for inclusive.

The manuscript may say that the primary design excludes distance discrimination materially above the upper bound **0.632**. It must not say that distance is uninformative or that the study excludes AUC ≥0.63 based on a rounded Monte Carlo endpoint.

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
- `robustness/results/confidence_strata.csv`
- `robustness/results/cohort_arm_primary_estimates.csv`
- `robustness/results/cohort_arm_cutoffs.csv`
- `robustness/results/regression_models.csv`
- `robustness/results/cohort_arm_descriptives.csv`

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

The core UniProt payload contains **41 active-site** and **221 binding-site feature records**. Expansion gives **564 feature-residue rows representing 560 unique residues**. **Correction 2026-08-12: the 564 does not reproduce and may not be cited** — two independent round-2 analyses both get 594 record-residue rows, 565 or 566 after deduplication, the excess arising from P12904's intervals recorded once per ligand. The 560 unique residues, which is the quantity defining the target set, reproduces exactly. See Section 18.10. The inclusive arm contains **109 serines, 41 threonines, and 16 tyrosines**. The primary arm contains **107 serines, 40 threonines, and 16 tyrosines**.

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
  `robustness/reviews/` still quote 66/66 and are dated artifacts, not current state.
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
- Base the robustness analysis random seed: **20260728**. Canonical arm intervals use **200,000**
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
  `robustness/results/replicate_aggregation_audit.csv` exposes the strain-level audit; no post-result
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
| Legacy (frozen review PDF) | `manuscript/figure1_cohort_estimand_primary.{png,pdf}`, `robustness/results/robustness_robustness_summary.{png,pdf}` | `manuscript/src/build_figure1.py`, `robustness/src/03_robustness_figure.py` | `manuscript/preprint_draft_v1.{md,pdf}`, whose SHA-256 is frozen in Section 14 |

The legacy Figure 1 compresses the cascade into five boxes, merging the whole-genome-sequencing
and scar-correlation stages into one "427 records after source QC" step. Section 4 declares six
stages. Both renderings are numerically correct; only the panel figure shows every declared stage.
Do not describe the two as the same figure.

Panel inputs, all committed pipeline outputs: `results/cohort_disposition.csv`,
`results/analysis_final.csv`, `results/analysis_inclusive_sensitivity.csv`,
`robustness/results/robustness_analysis.csv`, `confidence_strata.csv`, `cohort_sensitivity.csv`,
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

Panel builds are byte-reproducible **within one environment**: matplotlib PDF `CreationDate` is
suppressed in `manuscript/panels/src/_style.py`, and `compose.py` saves with `no_new_id=1` so MuPDF
writes no trailer `/ID`. PNG output carries no timestamp. `PyMuPDF==1.28.0` is pinned in
`requirements-lock.txt`; the composed PNGs are rasterized at 600 dpi through it.

**They are not byte-reproducible across environments, and the dependency lock cannot make them so**
(established 2026-08-13). `requirements-lock.txt` pins `matplotlib==3.8.4`, but matplotlib links a
bundled FreeType whose version depends on how matplotlib was built. The figures declared here were
produced against FreeType **2.12.1** (the Anaconda build); a virtual environment installing the PyPI
wheel gets FreeType **2.6.1** and renders glyphs differently, giving `figure1.png` SHA-256
`cfffacd6…` against the declared `8fffd9cc…`. Rebuilding twice in either environment reproduces that
environment's own bytes exactly.

Consequence for the release checks: `panel_figures_match_numbers` and the clean-room artifact
comparison for the figures are **environment-specific**, and will fail for an independent reproducer
using a pip-installed matplotlib even when the analysis is correct. Read a failure of those two checks
as a rendering-environment difference until the underlying numbers are shown to differ. The scientific
outputs — the three frozen analysis artifacts in the header — are unaffected, because they contain no
rendered glyphs.

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
`paired_auc_difference` from `robustness/src/02_robustness_analysis.py` without reimplementation, and
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

217 stored interval records across `results/` and `robustness/results/`: 167 from a resampling
estimator, 50 analytic logistic (Wald / cluster-robust) intervals involving no draws.

**Both canonical 200,000-draw arm intervals retained all 200,000 draws — zero discarded.**

| Arm | Unit | Estimate | 95% interval | Nominal | Retained | Shortfall |
|---|---|---:|---:|---:|---:|---:|
| Primary, 163 / 48 / 79 positive | protein cluster | 0.5268233876 | 0.4167443197–0.6315393408 | 200,000 | 200,000 | 0 |
| Inclusive, 166 / 50 / 82 positive | protein cluster | 0.5441347271 | 0.4357555293–0.6487455197 | 200,000 | 200,000 | 0 |
| Primary, naive site | site | 0.5268233876 | 0.4367346939–0.6173687783 | 200,000 | 200,000 | 0 |
| Inclusive, naive site | site | 0.5441347271 | 0.4553844563–0.6327034884 | 200,000 | 200,000 | 0 |

**Table S-RR13a. Six sensitivity intervals retained fewer than their nominal 20,000.** These are six
distinct quantities, each stored twice (once in `robustness_statistics.json`, once in the matching CSV).

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

**Provenance rule for the `draws` field.** `robustness/src/02_robustness_analysis.py::bootstrap_auc` and
`paired_auc_difference` return `"draws": len(draws)`, the count *after* discarding single-class
resamples, so every `draws` value under `robustness/results/` is a measured retained count.
`src/03_analysis.py::boot_auc` returns only `(point, lo, hi)`, and `results/statistics.json` then
writes `"draws"` and `"naive_site_draws"` as the literal constant `N_PRIMARY_BOOT`; those 200,000
entries, and the same literals in `results/cohort_arm_primary_estimates.csv`, are **nominal, not
measured**. They are correct — the phase-0.5 recomputation of the identical quantity at the same seed
offset gives the same estimate and endpoints to full precision with a true retained count of
200,000 — but cite `robustness_statistics.json`, not `results/statistics.json`, for any retention claim.

Three undocumented-retention gaps, none of which changes a number: 16 records in
`results/statistics.json` (`auc_other_predictors` for pLDDT, RSA and `n_annot_residues`, plus
`sift_comparator`, across four duplicated cohort blocks) store an interval with no draw count at all,
nominal 20,000 by the `boot_auc` default and retention unrecoverable without a rerun;
`robustness/results/sift_comparator_sensitivity.csv` has no `draws` column, though the same nine
intervals in `robustness_statistics.json` carry 20,000 with zero shortfall; and 11
`cluster_boot_spearman` records (`continuous_outcomes`, `confidence_correlations`) at a nominal 4,000
draws store no retained count and silently drop non-finite ρ. If the supplement quotes those
correlation intervals, their retention is undocumented.

### 18.8 Predictor benchmark, both summaries (RR-59)

10 repeated stratified group 5-fold splits, n = 163, 79 positive. The pooled column was independently
re-derived from the stored out-of-fold predictions in
`robustness_analysis_with_oof_predictions.csv` using the frozen `auc_from_ranks`; all five agree to
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
