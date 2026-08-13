# AI-Assisted Internal Adversarial Statistical Methods Review

> **Review status:** AI-assisted internal adversarial review conducted on 2026-07-29. This is not independent peer review, external statistical review, or confirmation by a senior author. It does not satisfy the manuscript's independent-methods-review release gate.

> **Post-review serialization addendum:** A later clean-environment run canonicalized last-bit
> continuous-model fields and refroze the Phase 0.5 JSON without changing any reported value. Use the
> current `NUMBERS.md` header, not the historical hash quoted below; see `RESPONSE_LOG.md`.

## Scope and Numerical Authority

This review was restricted to the public-data Fulbright project at `outputs/fulbright/research/phase0_calibration`. No Einstein or NYU evidence was consulted. The audit covered the estimand, exact-overlap handling, two-arm pipeline, protein-cluster bootstrap, AUC interpretation, logistic models, within-protein analyses, post-result multiplicity, SIFT comparison, and whether the manuscript's claims follow from the reported intervals.

`NUMBERS.md` was read before any numerical assessment and was treated as the sole numerical authority. The three frozen artifacts were re-hashed read-only before review:

- `results/statistics.json` matched `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`.
- `results/analysis_final.csv` matched `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`.
- `phase0_5/results/phase0_5_statistics.json` matched `569a3c5eab309e3ac3572d84718ce8b59ad3bd0762ed9d085aeafb6584f2e3e9`.

Evidence: `NUMBERS.md:3-11`; `phase0_5/src/04_verify_release.py:102-141`; `phase0_5/results/verification_report.json` (`numbers_authority`).

## Overall Judgment

**Disposition: pass with minor manuscript clarifications. No surviving statistical blocker or unresolved major statistical error was found in the assigned scope.**

The canonical result is internally supported as an exploratory, conditional estimate: the exclusion-primary cohort has **163 substitutions from 48 proteins, AUC 0.527 [0.417, 0.632]**; the named inclusive sensitivity has **166 substitutions from 50 proteins, AUC 0.544 [0.436, 0.649]**. The analysis does not establish equivalence to chance, absence of information, superiority or inferiority to SIFT, or a universal distance threshold. The current manuscript generally observes those boundaries.

Evidence: `NUMBERS.md:15-26,227-244`; `manuscript/preprint_draft_v1.md:9-23,73-89`; `phase0_5/ANALYSIS_PROVENANCE.md:20-46`.

## Blocking Findings

None found.

The earlier blockers—RNG-sensitive headline interval, unresolved exact-overlap estimand, incomplete confidence-strata display, undisclosed PAE definition, and the incorrect AUC range-restriction caveat—do not survive in the audited code and narrative.

Evidence: `NUMBERS.md:15-52,122-181,227-254`; `phase0_5/ANALYSIS_PROVENANCE.md:34-58`; `phase0_5/src/04_verify_release.py:214-412,414-533`.

## Major Findings

No unresolved major finding.

The post-outcome timing of the primary estimand remains a major interpretation constraint, but it is not hidden: the provenance states that the exclusion decision followed outcome inspection, both arms are emitted together, the inclusive result appears in the abstract, and neither arm is presented as confirmatory. Those disclosures must remain. Removing the inclusive arm or describing the exclusion-primary interval as preregistered, confirmatory, or selection-adjusted would create a major problem.

Evidence: `phase0_5/ANALYSIS_PROVENANCE.md:22-40`; `manuscript/preprint_draft_v1.md:9-23,93-95`; `NUMBERS.md:28-52`.

## Minor Findings

### M1. The within-protein section heading is stronger than its intervals

`manuscript/preprint_draft_v1.md:61` says “Within-protein comparisons were close to chance.” The point estimates are numerically near chance, but the pair-weighted interval is **0.368–0.709** and the equal-protein interval is **0.351–0.642**. The paragraph itself is appropriately cautious; the heading could still be read as an equivalence claim. A more accurate heading would describe the estimates as centered near chance and imprecise.

Evidence: `NUMBERS.md:183-190`; `manuscript/preprint_draft_v1.md:61-63`.

### M2. “Prespecified” cutoff timing is not supported by the decision record

The Methods call the descriptive distance cutoffs “prespecified” (`manuscript/preprint_draft_v1.md:121`), while the Results call the threshold summaries post-result (`manuscript/preprint_draft_v1.md:43`) and the provenance decision table does not record their timing (`phase0_5/ANALYSIS_PROVENANCE.md:20-32`). Either document when they were fixed or remove “prespecified.” This does not alter the analysis because the cutoff groups are explicitly nested and descriptive, with no threshold-test inference.

Evidence: `NUMBERS.md:78-100`; `src/03_analysis.py:135-156`; `phase0_5/src/02_phase0_5_analysis.py:401-452`.

### M3. The paired SIFT interval is the comparative evidence; interval containment is not a test

The abstract and Discussion emphasize that the SIFT point estimate lies inside the full-cohort distance interval (`manuscript/preprint_draft_v1.md:11,87`). That statement is numerically true, but containment of one point estimate within another estimator's interval is not itself a paired comparison. The stronger evidence is already present: on common support, the paired SIFT-minus-distance estimate is **0.074 [−0.037, 0.192]**. Comparative language should rest on that paired interval, while retaining the correct conclusion that inferiority was not shown.

Evidence: `NUMBERS.md:172-181`; `phase0_5/src/02_phase0_5_analysis.py:85-104,501-565`; `manuscript/preprint_draft_v1.md:65-71,123-129`.

### M4. Logistic diagnostics are not emitted as release artifacts

The stored logistic models use protein-cluster sandwich covariance and the manuscript reports broad intervals that include the null. Review-time, read-only refits reproduced the stored coefficients and cluster p-values, and every fitted formula reported convergence. The pipeline does not, however, emit convergence status, leverage/influence diagnostics, or a small-cluster correction specifically for the logistic odds-ratio intervals. The wild-cluster linear-probability sensitivity supports the qualitative null result but is not an interval check for the logistic odds ratios. Emitting basic fit diagnostics would strengthen the supplement; their absence is not a blocker because no logistic significance claim drives the paper.

Evidence: `NUMBERS.md:102-120,218-225`; `src/03_analysis.py:158-172`; `phase0_5/src/02_phase0_5_analysis.py:469-499,944-945`; `manuscript/preprint_draft_v1.md:37-43,117-127`.

### M5. The upper confidence endpoint is not a predeclared materiality margin

The sentence that the primary interval excludes discrimination materially above **0.632** is supportable only as a confidence-bound statement for the retrospectively defined primary estimand. The endpoint is not a formal equivalence, noninferiority, or practical-utility margin. The manuscript currently pairs the sentence with explicit statements that chance-level and SIFT-like ranking remain compatible and that distance is not shown to be uninformative. Those qualifications should remain adjacent to the claim.

Evidence: `NUMBERS.md:24-26,227-244`; `manuscript/preprint_draft_v1.md:73-89,117-121`; `phase0_5/ANALYSIS_PROVENANCE.md:42-46`.

## Passed Checks

### P1. Estimand and exact-overlap handling

The predictor direction and target population are explicit. The primary estimand excludes annotation-coincident substitutions; the inclusive arm retains their literal self-distance at 0 Å. The outcome-informed timing and the fact that all excluded records are outcome-positive are disclosed. The primary is not silently substituted for the inclusive arm.

Evidence: `NUMBERS.md:15-36`; `src/01_build_sites.py:326-378`; `src/03_analysis.py:74-95`; `manuscript/preprint_draft_v1.md:23,27-39,111-119`.

### P2. Complete two-arm cohort propagation

The parent and Phase 0.5 analyses define named `exclude_annotation_coincident` and `include_annotation_coincident` cohorts, derive them from the same inclusive table, and emit both arms' estimates, cutoffs, descriptives, logistic models, and confidence strata. The verifier confirms that primary is exactly inclusive minus the annotation-coincident rows and that parent and Phase 0.5 site keys agree.

Evidence: `NUMBERS.md:38-52`; `src/03_analysis.py:26-30,74-95,234-279`; `phase0_5/src/02_phase0_5_analysis.py:27-33,303-399,401-452,469-499,586-654`; `phase0_5/src/04_verify_release.py:214-350`.

### P3. Protein-cluster bootstrap implementation

The AUC code samples protein identifiers with replacement, retains every substitution belonging to each sampled protein, discards resamples lacking both outcome classes, and forms percentile intervals. The headline intervals use **200,000 draws** and seed **20260729**. The site-weighted point estimand and the distinction between cluster-aware uncertainty and protein-level confounding are stated explicitly.

Evidence: `NUMBERS.md:19-26`; `src/03_analysis.py:35-71,98-131`; `phase0_5/src/02_phase0_5_analysis.py:48-82,356-379`; `phase0_5/ANALYSIS_PROVENANCE.md:42-46,69-75`; `manuscript/preprint_draft_v1.md:117-121`.

### P4. AUC orientation and headline claims

Shorter distance is consistently scored as the positive direction by passing negative distance to the AUC function. A review-time rank calculation reproduced the frozen point estimate without writing an output. The manuscript reports the primary and inclusive intervals together and does not claim that distance is uninformative or that AUC at or above a rounded 0.63 threshold was excluded.

Evidence: `src/03_analysis.py:35-44,114-130`; `phase0_5/src/02_phase0_5_analysis.py:48-57,356-379`; `NUMBERS.md:15-26,227-244`; `manuscript/preprint_draft_v1.md:37-43,73-89`.

### P5. Logistic analyses

The logistic predictor is `log10(distance + 1)`, estimates are reported per ten-fold increase in that transformed quantity, and sandwich covariance is clustered by protein. Both arms are emitted. The primary unadjusted and pLDDT/RSA-adjusted intervals are wide and include the null, matching the manuscript's statement that both directions remain compatible.

Evidence: `NUMBERS.md:102-120`; `src/03_analysis.py:158-172,234-270`; `phase0_5/src/02_phase0_5_analysis.py:469-499`; `manuscript/preprint_draft_v1.md:37-43,117-121`.

### P6. Within-protein analyses

The pair-weighted estimand is the positive-negative-pair-weighted mean of protein-specific AUCs; a separate estimate gives each informative protein equal weight. Intervals resample informative proteins. A review-time recomputation reproduced both stored point aggregations. The manuscript identifies the conditioning set and reports the broader within-protein percentile sensitivity separately. Annotation-coincident substitutions contribute no informative within-protein pair, so their exclusion does not covertly change the pair-based estimates.

Evidence: `NUMBERS.md:183-190`; `phase0_5/src/02_phase0_5_analysis.py:130-177,454-467`; `manuscript/preprint_draft_v1.md:61-63,123-127`.

### P7. Sensitivity multiplicity

The confidence analysis displays the complete declared family for both arms. PAE analyses name `pae_pair_max`, show all four PAE summaries, and retain each full **72-cell** grid. The nonmonotonic pattern and post-result timing are disclosed; no lowest or highest cell is promoted as confirmatory. In this descriptive framework, lack of a multiplicity-adjusted p-value is acceptable. Any future promotion of one cell would require independent specification or multiplicity-aware inference.

Evidence: `NUMBERS.md:122-170,227-244`; `phase0_5/src/02_phase0_5_analysis.py:568-721`; `phase0_5/RESULTS.md:9-39`; `manuscript/preprint_draft_v1.md:45-59,123-125`.

### P8. SIFT comparison

SIFT and distance are evaluated on common support, and their difference uses paired protein resampling. Review-time point recalculation reproduced the stored SIFT AUC, common-support distance AUC, and their difference. The paired interval crosses zero, so the manuscript correctly avoids claiming that distance is inferior. SIFT is labeled post-result and not independent validation.

Evidence: `NUMBERS.md:172-181`; `phase0_5/src/02_phase0_5_analysis.py:85-104,501-565`; `phase0_5/RESULTS.md:63-65`; `manuscript/preprint_draft_v1.md:65-71,123-129`.

### P9. Claims follow from intervals within the exploratory frame

The manuscript distinguishes a weak point estimate from proof of no association, reports uncertainty rather than a low-draw rounded cutoff, treats threshold rates as descriptive, and avoids a range-restriction explanation for AUC. Chance-level and SIFT-like ranking remain compatible with the primary interval. Subject to M1 and M5, the central claims do not exceed the reported precision.

Evidence: `NUMBERS.md:24-26,227-244`; `phase0_5/ANALYSIS_PROVENANCE.md:42-58`; `manuscript/preprint_draft_v1.md:37-51,73-89`.

### P10. Executable release reconciliation

The fail-closed verifier checks frozen hashes before parsing numbers, reconciles both arms across parent and Phase 0.5 tables, confirms complete sensitivity families, scans manuscript and PDF text, and binds rendered pages to the current PDF. `NUMBERS.md` records a **66/66** pass. This is strong internal consistency evidence, although it is not a substitute for a clean-room rerun or external review.

Evidence: `NUMBERS.md:248-254`; `phase0_5/src/04_verify_release.py:102-141,214-412,414-606`; `phase0_5/results/verification_report.json`.

## Release Recommendation

No statistical rerun is required on the basis of this internal audit. Resolve M1–M3 in the manuscript, consider M4 for the supplement, and preserve the qualifications in M5. A separate human methods reviewer and clean-room reproduction remain necessary because this report is AI-assisted internal review, not independent peer review.
