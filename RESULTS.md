# Phase 0 Results — Two-Arm Raw-Ledger Rerun

## Summary

The primary cohort excludes three substitutions that are themselves an eligible UniProt active-site or binding-site residue. It contains **163 substitutions from 48 proteins**, including **79 substitutions with at least one source-defined growth phenotype**. Shorter minimum heavy-atom distance gave AUC **0.527** with protein-cluster 95% CI **0.417–0.632**. The named inclusive sensitivity retains the three substitutions at 0 Å and contains **166 substitutions from 50 proteins**, with AUC **0.544 [0.436, 0.649]**.

Numerical authority: `NUMBERS.md`. Machine-readable arm outputs: `results/cohort_arm_primary_estimates.csv`, `results/cohort_arm_cutoffs.csv`, `results/cohort_arm_logistic.csv`, and `results/cohort_arm_descriptives.csv`.

## Cohort Reconstruction

The outcome was rebuilt from Supplementary Data 3 rather than selected through Supplementary Data 6. Supplementary Data 6 contributes annotations only. Supplementary Data 8 supplies exact strain-level WGS and scar-control-correlation exclusions.

| Stage | Strain records | Unique substitutions | Proteins |
|---|---:|---:|---:|
| Point-mutant source rows | 497 | 490 | 116 |
| Sequence matched after PBY107 resolution | 487 | 479 | 113 |
| Sequence matched with a raw profile | 465 | 458 | 111 |
| After WGS exclusion | 447 | 443 | 110 |
| After scar-control-correlation exclusion | 427 | 423 | 107 |
| Core annotation and structure eligible | 169 | 166 | 50 |

Every source point-mutant row has a disposition in `results/cohort_disposition.csv`. Two substitutions had replicate strains; their condition-level S-scores and significant-condition counts were averaged at the substitution level.

## Estimand and Primary Estimate

TDH3 S149, TDH3 T151, and PRM15 S158 coincide with an eligible annotation. All three are outcome-positive. The primary arm excludes them because self-distance is a distinct predictor case; the literal 0 Å definition is retained as the named inclusive sensitivity. Both arms are emitted from the same seeded run.

In the primary arm, median distance was **26.233 Å** for outcome-positive substitutions and **31.827 Å** for outcome-negative substitutions. The protein-cluster interval used **200,000** resamples with seed **20260729**. A substitution-level interval of **0.437–0.617** is reported only as a dependence diagnostic.

Cluster-robust logistic regression on `log10(distance + 1)` gave OR **0.767 [0.274, 2.150]** per ten-fold increase in distance + 1 Å. With site pLDDT and relative solvent accessibility included, the OR was **1.313 [0.383, 4.508]**.

## Descriptive Distance Cutoffs

Only **10 of 163** primary substitutions were within 5 Å. Four of 10 (**40.0%**) were outcome-positive, compared with 75 of 153 (**49.0%**) beyond 5 Å. The inclusive arm contains 13 substitutions within 5 Å because it adds three outcome-positive exact overlaps. All cutoff groups are nested and descriptive; they do not test a universal threshold.

## Interpretation Boundary

The primary interval excludes discrimination materially above **0.632**, but it does not establish equivalence to chance. The SIFT comparator point estimate lies within this interval. The study therefore does not support the statements that distance is uninformative or that it performs worse than SIFT.

The outcome is an any-condition growth phenotype after alanine substitution, not a direct assay of phosphorylation. The predictor is one distance in an AlphaFold DB v6 monomer model; ligands, complexes, interfaces, alternative conformations, and the phosphorylated state are absent. Only proteins carrying reviewed UniProt active-site or binding-site annotations can enter the analysis.

the robustness analysis contains the post-result confidence, within-protein, residue-class, feature-definition, continuous-outcome, SIFT, and grouped-prediction analyses.
