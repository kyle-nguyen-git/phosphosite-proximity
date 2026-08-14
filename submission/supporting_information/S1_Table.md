# S1 Table. The eleven-stratum confidence family

| Stratum | Primary AUC | 95% interval | n | Inclusive AUC | 95% interval | n |
|---|---:|---:|---:|---:|---:|---:|
| All | 0.527 | 0.417–0.632 | 163 | 0.544 | 0.436–0.649 | 166 |
| Site pLDDT ≥50 | 0.489 | 0.347–0.634 | 79 | 0.522 | 0.380–0.665 | 82 |
| Site pLDDT ≥70 | 0.459 | 0.303–0.618 | 60 | 0.507 | 0.351–0.663 | 63 |
| Site and target pLDDT ≥70 | 0.450 | 0.288–0.606 | 58 | 0.500 | 0.337–0.658 | 61 |
| Site pLDDT ≥90 | 0.570 | 0.371–0.746 | 35 | 0.622 | 0.435–0.791 | 38 |
| Site and target pLDDT ≥90 | 0.641 | 0.464–0.789 | 28 | 0.697 | 0.536–0.842 | 31 |
| `pae_pair_max` ≤5 Å | 0.488 | 0.261–0.666 | 37 | 0.555 | 0.332–0.730 | 40 |
| `pae_pair_max` ≤10 Å | 0.436 | 0.208–0.633 | 44 | 0.496 | 0.277–0.692 | 47 |
| `pae_pair_max` ≤15 Å | 0.520 | 0.321–0.679 | 55 | 0.564 | 0.377–0.714 | 58 |
| Both-residue pLDDT ≥70 and `pae_pair_max` ≤10 Å | 0.416 (family minimum) | 0.192–0.617 | 41 | 0.486 | 0.271–0.684 | 44 |
| Both-residue pLDDT ≥90 and `pae_pair_max` ≤10 Å | 0.683 (family maximum) | 0.481–0.864 | 27 | 0.736 | 0.553–0.903 | 30 |

All eleven strata are post hoc and are shown here and in S1 Fig for both cohort versions. The number of sites falls from 163 to 27 across the primary family, whose lowest and highest values are 0.416 and 0.683. Four strata kept fewer than their nominal 20,000 resamples: 19,999 for the two primary high-confidence rows, and 19,997 and 19,999 for their inclusive counterparts. Tightening the PAE threshold does not move the AUC steadily in either direction, in either cohort version.
