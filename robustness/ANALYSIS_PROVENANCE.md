# the robustness analysis Analysis Provenance

## Summary

This is an exploratory secondary analysis. The original 158-substitution result was observed before the robustness analysis was designed. A reviewer-style reconstruction found that Supplementary Data 6 had been used incorrectly as an eligibility ledger, exact annotation overlaps had not been handled as a named estimand decision, and a low-draw bootstrap endpoint had been overinterpreted. The cohort and uncertainty analysis were rebuilt before the preprint was reconciled.

Numerical authority: `../NUMBERS.md`. The frozen hashes in its header must be re-verified before any numerical claim is changed.

During the clean-environment audit on 29 July 2026, pip-wheel and conda BLAS implementations differed
only in the last machine-precision digits of adjusted continuous-outcome OLS sensitivity fields. Those
fields are now serialized at the 12-decimal computational contract recorded in `NUMBERS.md`. No cohort,
estimate, interval, or reported scientific value changed; the the robustness analysis JSON hash was then refrozen and
is verified before use.

## Data Boundary

All inputs are public: Viéitez et al. supplementary data, reviewed *Saccharomyces cerevisiae* UniProt records, and AlphaFold DB structures and PAE documents. No Einstein/Chang-lab data, models, or code are used. No NYU data are used.

The source supplements have distinct roles:

- Supplementary Data 1 defines point-mutant constructs.
- Supplementary Data 3 is the raw growth-screen ledger and defines the outcome.
- Supplementary Data 6 contributes optional annotations only.
- Supplementary Data 8 supplies strain-specific WGS and scar-control-correlation exclusions.

## Decision Record

| Decision | Timing | Status |
|---|---|---|
| Binary outcome: at least one raw condition with `qvalue < 0.05` | Initial concept; reconstructed during review | Primary descriptive outcome |
| Predictor: minimum heavy-atom distance to ACT_SITE/BINDING | Initial Phase 0 | Primary predictor already observed |
| Protein-cluster bootstrap AUC | the robustness analysis | Post-outcome robustness analysis |
| Raw-ledger cohort reconstruction | Reviewer audit | Required correction, not a new hypothesis |
| Exclude annotation-coincident substitutions from primary | Reviewer audit after outcome inspection | Primary estimand decision; inclusive 0 Å arm named in abstract |
| Resolve PBY107 to HOG1 T174A | Reviewer audit | Source-coordinate correction |
| Pairwise PAE, confidence strata, feature definitions, continuous outcomes, SIFT, and grouped prediction | the robustness analysis or later audit | Post-outcome sensitivity analyses |

No the robustness analysis analysis is preregistered or confirmatory. Complete sensitivity families are reported; no extreme cell is promoted.

## Exact-Overlap Estimand Resolution — 2026-07-29

The primary estimand excludes substitutions that are themselves an eligible ACT_SITE or BINDING residue. For these records, a 0 Å self-distance is categorically different from distance to another annotated residue and places the substitutions at a deterministic predictor boundary. The three records—TDH3 S149, TDH3 T151, and PRM15 S158—are all outcome-positive.

The inclusive arm retains all three at their literal 0 Å distance. Because this decision was made after outcomes were known and moves AUC from **0.527** to **0.544**, both arms are generated from the same run and the inclusive estimate is named in the abstract. Neither arm is described as independent confirmation.

Implementation is explicit: `exclude_annotation_coincident` is primary and `include_annotation_coincident` is the sensitivity. Parent and the robustness analysis scripts emit both arms' estimates, cutoff tables, logistic models, descriptives, confidence strata, and figures.

## Bootstrap Precision

The canonical primary result is **0.527 [0.417, 0.632]**. The named inclusive sensitivity is **0.544 [0.436, 0.649]**. Both protein-cluster intervals use **200,000 draws** with seed **20260729**. The stored intervals are reused rather than resimulated for prose, tables, and figures.

An earlier statement that the study “excluded AUC ≥0.63” was based on a low-draw interval whose rounded endpoint changed with the random seed. That statement is retracted. The manuscript instead states that discrimination materially above the primary upper bound **0.632** is excluded. It does not claim that distance is uninformative.

## Structural Confidence and PAE Definition

Pairwise PAE strata use **`pae_pair_max`**, the larger of the two directed AlphaFold PAE entries. The full 11-stratum family is emitted for both arms and plotted without selecting a monotone subset.

The four PAE columns at 10 Å differ. In the primary arm they give **0.436, 0.459, 0.489, and 0.521** for pair maximum, site-to-target, pair mean, and target-to-site. The joint `pae_pair_max ≤10` and site-pLDDT ≥70 cell ranks **1 of 72** from low to high in the primary, inclusive, and legacy grids. PAE analyses are therefore described only as post-result sensitivity families.

No range-restriction caveat is used for AUC. AUC is rank-invariant under monotone transformations, so an Ångström-range explanation would be incorrect.

## SIFT Comparator

Inverse SIFT was examined after the distance result. On primary common support its AUC is **0.606 [0.522, 0.690]**. The point estimate lies inside the primary distance interval **0.417–0.632**. The manuscript therefore does not claim that distance is uninformative or inferior to SIFT.

## Cohort and Quality Rules

- Every point-mutant source row has an inclusion or exclusion reason in `results/cohort_disposition.csv`.
- PBY107 is analyzed as HOG1 T174A; an exclusion sensitivity is retained because the workbooks are inconsistent.
- Unresolved sequence mismatches remain visible in `results/residue_mismatch_audit.csv`.
- Supplementary Data 8 flags are applied to exact strain IDs.
- Replicate-strain S-scores are averaged within condition before continuous summaries.
- The binary endpoint averages each retained strain's nonnegative count of source-significant conditions
  and then tests whether the mean is greater than zero. This is logically an any-positive-replicate rule,
  not a replicate-unanimity rule. The strain-level audit is emitted as
  `results/replicate_aggregation_audit.csv`.
- The 5, 8, 10, and 15 Å descriptive cutoff set was fixed for post-result sensitivity analysis after the
  primary outcome had been inspected. These nested groups are not independent threshold tests.
- Outcome-derived fields and phenotype labels are excluded from predictor benchmarking.

## Statistical Units

The primary point estimate is site-weighted. Protein-cluster intervals retain every substitution from each sampled protein. Within-protein positive-negative comparisons and equal-protein weighting are reported separately because clustered uncertainty does not remove protein-level confounding from a site-weighted point estimate.

## Reproducibility Status

`run_all.sh` rebuilds the parent and the robustness analysis analyses. Random analyses use base seed **20260728**; canonical arm intervals use **20260729**. Cached AlphaFold metadata, mmCIF files, and PAE documents retain version, URL, and SHA-256 information. The release verifier must reconcile both arms, numerical text, the final PDF, and the rendered-page manifest.

The release tooling performs a same-author clean-room rerun from the exact archive in a fresh temporary
environment and records its evidence in `release/clean_room_report.json`. This is technical
reproduction, not independent replication or the separate human methods review.
