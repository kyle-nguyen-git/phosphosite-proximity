# RR-28 — Characterization of the annotation target set

Script: `rr28/rr28_annotation_target_set.py`. Machine-readable results: `rr28/rr28_results.json`.
Per-row tables: `rr28_substitution_target_evidence.csv` (163 rows), `rr28_expanded_target_residues.csv`
(533 rows), `rr28_experimental_only_distances.csv` (163 rows), `rr28_primary_cohort_proteins.csv` (48 rows).

Frozen hashes for `results/statistics.json`, `results/analysis_final.csv`, and
`phase0_5/results/phase0_5_statistics.json` were verified before any computation and all three matched.
Nothing under the frozen tree was written.

Estimators (`auc_from_ranks`, `bootstrap_auc`, `paired_auc_difference`) were imported from
`phase0_5/src/02_phase0_5_analysis.py`. That module is guarded by `if __name__ == "__main__"`, so
importing it does not execute `main()`; the functions used are the published ones, not copies.

Distances for the restricted target set (item 6) had to be recomputed from the cached AlphaFold models in
`data/af/`, because the frozen tables store only the distance to the nearest target under the *full*
annotation set. The recomputation was validated by first reproducing the full-set distances:
maximum absolute deviation from the frozen `min_dist_A` was **1.42e-14 Å** over all 163 rows, and
`nearest_feat_pos` agreed on **163/163**. Same atom–atom minimum-distance rule as `src/02_structures.py`.

Conventions used, as declared: score = `-min_dist_A` (shorter distance toward screen-positive);
resampling unit = UniProt accession; post hoc intervals = 20,000 nominal protein-cluster draws, seed
20260728 (the module `SEED`); retained draw counts reported next to nominal.

**Experimental / non-experimental split (stated definition).** A record is *experimental* if its
evidence-code set intersects {ECO:0000269 (experimental evidence, manual assertion), ECO:0007744
(combinatorial experimental + manual, here PDB structures and MS)}. Everything else is
*non-experimental*: ECO:0000255 (sequence-model / PROSITE-ProRule), ECO:0000250 (by similarity),
ECO:0000305 (curator inference), or no evidence code. A residue can be covered by more than one feature
record; the union of codes over all covering records is used, and the multiplicity is reported.

---

## 1. Evidence of the NEAREST target actually used (substitution level, n = 163)

| Evidence-code set of the nearest target residue | n |
|---|---|
| ECO:0000255 | 101 |
| ECO:0000250 | 33 |
| ECO:0000269;ECO:0007744 | 12 |
| ECO:0000305 | 8 |
| ECO:0000269 | 4 |
| ECO:0000305;ECO:0007744 | 3 |
| ECO:0000250;ECO:0000269;ECO:0007744 | 1 |
| none | 1 |

**Experimental 20 / 163 (12.3%); non-experimental 143 / 163 (87.7%).**

The prior check (101 / 34 / 12 / 8 / 4 / 3 / 1) is confirmed with one refinement: exactly one
substitution's nearest residue is covered by three overlapping records whose codes union to
ECO:0000250 + ECO:0000269 + ECO:0007744. Assigning that residue by a single record gives the prior
count of 34 for ECO:0000250 and an experimental count of 19; the union rule used here gives 33 and 20.
That is the only ambiguous row (`n_covering_records > 1` for 1 of 163; max 3).

## 2. Same at expanded-residue level (whole eligible target set, 48 proteins)

533 eligible target residues (matches the sum of `n_annot_residues` over the 48 primary-cohort
proteins, 533).

| Evidence-code set | residues |
|---|---|
| ECO:0000255 | 313 |
| ECO:0000250 | 120 |
| ECO:0000269;ECO:0007744 | 55 |
| ECO:0000269 | 15 |
| ECO:0000305;ECO:0007744 | 15 |
| ECO:0000250;ECO:0000269;ECO:0007744 | 7 |
| ECO:0000305 | 5 |
| ECO:0000250;ECO:0000255 | 2 |
| none | 1 |

**Experimental 92 / 533 (17.3%); non-experimental 441 / 533 (82.7%).** 21 of the 533 residues are
covered by more than one record.

## 3. Ligand of the nearest target

**ATP is the nearest-target ligand for 86 of 163 substitutions (52.8%)** — the prior check is confirmed.
One further substitution has a nearest residue covered by records naming ADP, AMP and ATP, so 87/163
involve ATP under a permissive reading.

| Ligand of nearest target | n |
|---|---|
| ATP | 86 |
| (no ligand: Active site, or BINDING without a ligand field) | 40 |
| Zn(2+) | 10 |
| NADP(+) | 5 |
| NAD(+) | 4 |
| substrate | 3 |
| GTP | 3 |
| PtdIns(4)P | 3 |
| ADP | 2 |
| thiamine diphosphate | 2 |
| ADP;AMP;ATP | 1 |
| CoA, Mn(2+), acetyl-CoA, Mg(2+) | 1 each |

Over expanded BINDING residues (sum of interval widths, all 57 feature-carrying proteins) the same
skew holds: ATP 315, NAD(+) 33, NADP(+) 28, CoA 24, Zn(2+) 24, substrate 21, ADP 16, Mg(2+) 15,
GTP 15, acetyl-CoA 14, pyruvate 11, thiamine diphosphate 9, AMP 8, G3P 7, Mn(2+) 6, PtdIns(4)P 4,
arsenite 3.

## 4. Interval widths of BINDING records

221 BINDING records (all in the feature file; 199 of them on the 48 primary-cohort proteins).

| Width (residues) | records |
|---|---|
| 1 | 156 |
| 2 | 11 |
| 3 | 9 |
| 4 | 8 |
| 6 | 1 |
| 7 | 3 |
| 8 | 8 |
| 9 | 25 |

Median width 1, maximum 9. **33 records have width ≥ 8 and contribute 289 expanded residues** — the
prior check's 289-from-33 is confirmed. All 33 wide records sit on the 48 primary-cohort proteins.

The denominator 594 is the sum of interval widths over all ACT_SITE + BINDING records in the feature
file (BINDING 553 + ACT_SITE 41 = 594), before de-duplication of overlapping positions. After
de-duplication the eligible set is 533 residues on the 48 cohort proteins, of which **289 (54.2%) come
from a BINDING record of width ≥ 8** — the ATP-binding-region intervals. So more than half the target
set is contributed by 33 range annotations, i.e. by "somewhere in this stretch" statements rather than
by named contact residues.

## 5. Protein kinases among the 48 primary-cohort proteins

**24 of 48 (50%)** have "kinase" in their UniProt protein name (`data/yeast_sgd_uniprot.tsv`), and all
24 are protein kinases or protein-kinase-complex subunits — none is a metabolic sugar/nucleotide kinase.
23 are catalytic protein kinases (TPK1, SNF1, PBS2, SCH9, YPK1, KIN1, MCK1, DBF2, STE11, SAT4, DBF20,
HOG1, MKK1, ELM1, RIM15, PTK2, SSK2, SLT2, STE20, TDA1, SKY1, YGK3, MRK1); the 24th, SNF4, is the AMPK
gamma regulatory subunit (AMP/ATP-binding, not catalytic). This is a name-based classification from the
local proteome table, not a curated kinome list; the assignment is unambiguous for every entry above.
Full list with names: `rr28_primary_cohort_proteins.csv`.

That 50% kinase share is the direct cause of the ATP dominance in item 3.

## 6. KEY NUMBER — restricting the eligible set to experimentally-evidenced residues

Restricting each protein's target set to residues from records with ECO:0000269 or ECO:0007744:

- **24 of 163 substitutions (14.7%) retain any target at all. 139 lose every target.**
- Those 24 sit on **7 of 48 proteins** (only 7 of the 48 carry any experimentally-evidenced
  ACT_SITE/BINDING record at all; 8 of the 57 feature-carrying proteins do).
- Class balance on the retained subset: 11 positive, 13 negative.
- No retained substitution has distance 0 (the primary cohort already excludes annotation-coincident
  sites).
- Median nearest-experimental-target distance on the retained 24: 20.19 Å (positives), 21.81 Å
  (negatives). On the same 24 rows under the full annotation set the medians are 20.19 Å and 15.85 Å,
  so the restriction moves negatives further from a target and leaves positives unchanged at the
  median. Per-row the distance increases by a mean of 1.27 Å (median 0, max 14.14 Å): for 18 of 24
  rows (20 of 24) the nearest target was already an experimentally-evidenced residue.
- For context, the full primary cohort (n = 163) has median distances 26.23 Å (positives) and
  31.83 Å (negatives) under the full annotation set.

**AUC, experimental-only targets, n = 24, 7 proteins: 0.4196, 95% protein-cluster interval
[0.2436, 0.7083], 19,991 retained of 20,000 nominal draws, seed 20260728.**

Reference points on the same 24 substitutions, scored with the original full-annotation distance:
AUC 0.4406 [0.2284, 0.7667], 19,991/20,000 retained. Paired difference (experimental-only minus
full-annotation, same rows): −0.0210 [−0.1667, +0.0496], 19,991/20,000 retained.

Neither interval endpoint touches 0 or 1, so all three are reportable as intervals.

Per-protein composition of the retained subset:

| acc | gene | substitutions | positives | experimental target residues | median dist (Å) |
|---|---|---|---|---|---|
| P00924 | ENO1 | 4 | 1 | 12 | 11.64 |
| P02829 | HSP82 | 6 | 3 | 16 | 37.25 |
| P04050 | RPO21 | 2 | 0 | 11 | 46.03 |
| P11986 | INO1 | 4 | 2 | 27 | 20.48 |
| P12904 | SNF4 | 3 | 0 | 8 | 21.81 |
| P32324 | EFT1; EFT2 | 3 | 3 | 15 | 31.05 |
| P32485 | HOG1 | 2 | 2 | 3 | 16.48 |

### Reading

The result is a collapse, and the collapse is the finding. Under an experimentally-evidenced-only
target set the design loses 85% of its substitutions and 41 of 48 proteins, leaving 24 sites in 7
proteins. At that n the interval spans 0.24–0.71 and is compatible with anything from strong
anti-discrimination to moderate discrimination; the point estimate 0.4196 is below 0.5, in the same
direction as the published null but with no resolving power.

What this quantifies: the published near-null AUC cannot be attributed to annotation quality, because
the design cannot be run on high-quality annotation. 87.7% of the nearest targets actually used are
non-experimental (ECO:0000255 ProRule patterns and ECO:0000250 by-similarity transfers), and 54.2% of
the eligible residues come from 33 wide interval annotations, mostly ATP-binding regions on the 24
kinases in the cohort. The "distance to the nearest functional-site residue" being measured is, for
most rows, distance to a rule-propagated ATP-region boundary. Any future version of this estimand needs
a target set built from structures or mutagenesis, and the cohort would have to be assembled around
that constraint from the start rather than filtered down to it.

### Stability caveats

- Item 1's experimental count is 20 under the union-of-covering-records rule and 19 if the single
  triple-covered residue is assigned to its ECO:0000250 record. Both numbers are reported rather than
  one being chosen silently.
- Item 6's interval rests on 7 resampling units. Percentile endpoints from 7 clusters are coarse
  (the retained-draw loss, 9 of 20,000, is small, but the support of the bootstrap distribution is
  small too). Treat it as a descriptive range, not an inferential claim.
- The restriction in item 6 is applied at the record level: a residue is experimental if any record
  covering it carries ECO:0000269/ECO:0007744, which is the permissive direction. A stricter rule
  (every covering record experimental) would retain fewer than 24.
