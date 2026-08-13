# Phase 0.5 Results — Two-Arm Exploratory Analyses

## Summary

The primary arm contains **163 substitutions from 48 proteins** and gives AUC **0.527 [0.417, 0.632]**. The named inclusive 0 Å sensitivity contains **166 substitutions from 50 proteins** and gives **0.544 [0.436, 0.649]**. Confidence restrictions, within-protein comparisons, continuous growth-profile summaries, residue and feature definitions, and protein-isolated prediction did not identify stable incremental discrimination. Every Phase 0.5 analysis was specified after the initial distance result.

Numerical authority: `../NUMBERS.md`.

## Structural-Confidence Sensitivity

All PAE rows use **`pae_pair_max`**, the larger directed site-target PAE value. Every declared stratum is shown for both arms.

| Stratum | Primary n | Primary AUC [95% CI] | Inclusive n | Inclusive AUC [95% CI] |
|---|---:|---:|---:|---:|
| All substitutions | 163 | 0.527 [0.417, 0.632] | 166 | 0.544 [0.436, 0.649] |
| Site pLDDT ≥50 | 79 | 0.489 [0.346, 0.634] | 82 | 0.522 [0.380, 0.665] |
| Site pLDDT ≥70 | 60 | 0.459 [0.303, 0.618] | 63 | 0.507 [0.351, 0.663] |
| Site and target pLDDT ≥70 | 58 | 0.450 [0.288, 0.606] | 61 | 0.500 [0.337, 0.658] |
| Site pLDDT ≥90 | 35 | 0.570 [0.371, 0.746] | 38 | 0.622 [0.435, 0.791] |
| Site and target pLDDT ≥90 | 28 | 0.641 [0.464, 0.789] | 31 | 0.697 [0.536, 0.842] |
| `pae_pair_max` ≤5 Å | 37 | 0.488 [0.261, 0.666] | 40 | 0.555 [0.332, 0.730] |
| `pae_pair_max` ≤10 Å | 44 | 0.436 [0.208, 0.633] | 47 | 0.496 [0.277, 0.692] |
| `pae_pair_max` ≤15 Å | 55 | 0.520 [0.321, 0.679] | 58 | 0.564 [0.377, 0.714] |
| Both-residue pLDDT ≥70 and `pae_pair_max` ≤10 Å | 41 | 0.416 [0.192, 0.617] | 44 | 0.486 [0.271, 0.684] |
| Both-residue pLDDT ≥90 and `pae_pair_max` ≤10 Å | 27 | 0.683 [0.481, 0.864] | 30 | 0.736 [0.553, 0.903] |

The three `pae_pair_max` threshold estimates are **0.488, 0.436, 0.520** in the primary arm and **0.555, 0.496, 0.564** in the inclusive arm. Neither sequence is monotonic. Distance correlates with `pae_pair_max`, so these restrictions change both measurement confidence and the predictor distribution; they are sensitivity analyses, not rescued primary results.

## PAE Definition Sensitivity

At PAE ≤10 Å, the four available summaries give:

| Cohort | `pae_pair_max` | Site-to-target | Pair mean | Target-to-site | 72-cell range |
|---|---:|---:|---:|---:|---:|
| Primary exclude | 0.436 | 0.459 | 0.489 | 0.521 | 0.416–0.569 |
| Inclusive sensitivity | 0.496 | 0.513 | 0.539 | 0.565 | 0.486–0.601 |
| Legacy 158-site | 0.423 | 0.446 | 0.477 | 0.505 | 0.406–0.554 |

For each cohort, the joint `pae_pair_max ≤10` and site-pLDDT ≥70 cell ranks **1 of 72** from low to high. This multiplicity and column dependence preclude promoting the selected cell.

## Cohort and Biological Sensitivities

| Analysis | Sites | Proteins | Positives | AUC [95% CI] |
|---|---:|---:|---:|---:|
| Primary, exact overlaps omitted | 163 | 48 | 79 | 0.527 [0.417, 0.632] |
| Inclusive, exact overlaps = 0 Å | 166 | 50 | 82 | 0.544 [0.436, 0.649] |
| Inclusive, resolved HOG1 row omitted | 165 | 50 | 81 | 0.540 [0.433, 0.645] |
| Legacy Supplementary Data 6-selected cohort | 158 | 48 | 74 | 0.522 [0.408, 0.632] |
| Primary Ser/Thr only | 147 | 48 | 67 | 0.499 [0.389, 0.605] |
| Primary Tyr only | 16 | 12 | 12 | 0.604 [0.272, 1.000] |
| Inclusive, PRM15 S158 omitted | 165 | 49 | 81 | 0.539 [0.429, 0.641] |

ACT_SITE-only distance gives AUC **0.570 [0.453, 0.677]** on 107 substitutions. BINDING-only distance gives **0.525 [0.415, 0.632]** on 155 substitutions. Adding broader SITE and DNA-binding annotations changes the primary estimate by less than 0.002. These definitions were examined after the outcome.

## Within-Protein Identification

Twenty-three proteins contribute both outcome classes, comprising **112 substitutions** and **176** positive-negative pairs. Pair-weighted within-protein AUC is **0.528 [0.368, 0.709]**; equal-protein-weight AUC is **0.497 [0.351, 0.642]**. The primary within-protein distance-percentile AUC is **0.511 [0.412, 0.612]**.

## Continuous Outcomes and Internal Prediction

The five continuous-outcome Spearman estimates range from **−0.115 to −0.076**, and every protein-bootstrap interval crosses zero. Protein-isolated mean split AUCs are **0.484** for distance alone, **0.558** for structural features, **0.590** for source annotations, and **0.587** for the combined model. The structural increment over source annotations is **−0.003**, with split range **−0.039 to 0.034**. These are partition-stability summaries, not external validation or sampling intervals.

## Post-Result SIFT Comparator

On the primary common support of **152 substitutions**, inverse SIFT gives AUC **0.606 [0.522, 0.690]** and distance gives **0.532 [0.418, 0.647]**. Their paired difference is **0.074 [−0.037, 0.192]**. The SIFT point estimate lies inside the full primary distance interval **0.417–0.632**. SIFT is a post-result comparator, not independent validation; the comparison does not show that distance is uninformative or inferior.

## Quality Checks

Raw S-scores and AlphaFold pair PAE are complete for both arms. No retained primary or inclusive strain carries a Supplementary Data 8 WGS or scar-control-correlation flag. `results/phase0_5_statistics.json` is machine-readable; `results/verification_report.json` records executable release checks.
