# RR-29 — Sequence-adjacency sensitivity and short-range composition

Script: `rr29_sequence_adjacency/rr29_sequence_adjacency.py`
Outputs: `rr29_within15A_primary.csv`, `rr29_auc_sensitivity.csv`, `rr29_cutoffs.csv`, `rr29_results.json`

Frozen hashes for `results/statistics.json`, `results/analysis_final.csv`, and
`phase0_5/results/phase0_5_statistics.json` were verified before computation and all three matched.
No existing file was modified. Estimators (`auc_from_ranks`, `bootstrap_auc`) were loaded from
`phase0_5/src/02_phase0_5_analysis.py`; that module is guarded by `if __name__ == "__main__"`, so the
import does not run `main()` and nothing was rewritten.

## Definitions and conventions

- `dpos` = `|pos - nearest_feat_pos|`. Sequence-adjacent = `dpos <= 2`.
- `min_dist_A` is identical to `dist_core_A` on all 166 rows, and `nearest_feat_pos` is identical to
  `nearest_core_pos` on all 166 rows (asserted in the script). The "nearest target" distance is therefore
  unambiguous, and the score is the published one: `-dist_core_A`, shorter distance toward screen-positive.
- Bootstrap: 20,000 nominal protein-cluster draws, seed 20260728 (the module's `SEED`), resampling unit
  = UniProt accession, all substitutions of a sampled protein retained.
- Retained draws were 20,000 of 20,000 nominal for every interval below; no resample drew a single
  outcome class. No interval endpoint touches 0 or 1.

## 1. Composition of the sub-5 Å bin (primary cohort)

The prior check is confirmed exactly. Of the 10 primary substitutions at ≤ 5 Å, **5 sit at
1.3296–1.3419 Å with `dpos` = 1**:

| acc | gene | pos | wt→mut | distance (Å) | nearest_feat_pos | dpos | has_pheno |
|---|---|---|---|---|---|---|---|
| P16387 | PDA1 | 313 | S→A | 1.3296478986740112 | 312 | 1 | 0 |
| P37263 | YCR087C-A | 49 | T→A | 1.3308113813400269 | 48 | 1 | 0 |
| P16140 | VMA2 | 380 | S→A | 1.3399593830108645 | 381 | 1 | 1 |
| P11986 | INO1 | 368 | S→A | 1.340893030166626 | 369 | 1 | 1 |
| P02829 | HSP82 | 379 | S→A | 1.3419464826583862 | 380 | 1 | 0 |
| Q12222 | YGK3 | 211 | S→A | 2.6456551551818848 | 173 | 38 | 0 |
| P12688 | YPK1 | 508 | T→A | 2.836493015289306 | 470 | 38 | 1 |
| P53599 | SSK2 | 1460 | T→A | 3.208043336868286 | 1390 | 70 | 0 |
| Q03656 | SKY1 | 388 | S→A | 3.58735728263855 | 164 | 224 | 1 |
| P37263 | YCR087C-A | 53 | S→A | 3.604691743850708 | 51 | 2 | 0 |

So **6 of the 10 sub-5 Å substitutions are sequence-adjacent** (5 at `dpos` = 1, 1 at `dpos` = 2).
The 1.33 Å cluster is the C–N peptide bond: an i±1 neighbour has a fixed backbone contact distance and
the minimum-atom-pair distance cannot exceed it. Those five values encode sequence adjacency, not
spatial proximity to the functional target. Their outcomes are 2 positive / 3 negative.

The remaining four sub-5 Å substitutions (`dpos` = 38, 38, 70, 224) are genuine long-range-in-sequence
spatial contacts, 2 positive / 2 negative.

Whole-cohort `dpos` distribution (primary, n = 163): five rows at `dpos` = 1, one at `dpos` = 2, and
157 at `dpos` ≥ 3. Within 15 Å there are 43 primary substitutions, 6 of them sequence-adjacent — every
sequence-adjacent pair in the cohort falls inside 15 Å, and in fact inside 5 Å.

## 2. Declared sensitivity: AUCs with `|dpos| <= 2` excluded

Protein-cluster bootstrap, 20,000 nominal draws, seed 20260728.

| arm | filter | n sites | n proteins | n pos | n neg | AUC | 95% CI | nominal draws | retained draws |
|---|---|---|---|---|---|---|---|---|---|
| primary (exclude annotation-coincident) | all | 163 | 48 | 79 | 84 | 0.526823 | 0.416106–0.630551 | 20000 | 20000 |
| primary | `dpos` > 2 | 157 | 48 | 77 | 80 | **0.540584** | 0.428570–0.648366 | 20000 | 20000 |
| inclusive sensitivity | all | 166 | 50 | 82 | 84 | 0.544135 | 0.434521–0.647659 | 20000 | 20000 |
| inclusive sensitivity | `dpos` > 2 | 157 | 48 | 77 | 80 | **0.540584** | 0.428570–0.648366 | 20000 | 20000 |

**Reconciliation with the Devil's Advocate.** The reported 0.541 for the primary arm is confirmed:
the computed value is 0.540584, which rounds to 0.541 at three decimals. No discrepancy.

**The two arms collapse onto one cohort under this filter.** The three substitutions that separate the
inclusive arm from the primary arm are exactly the annotation-coincident ones (`is_itself_annot`), and
all three have `dpos` = 0. Removing `dpos <= 2` therefore removes them along with the six primary
sequence-adjacent rows (3 + 6 = 9; 166 − 9 = 157), and the inclusive and primary sensitivity cohorts
are the same 157 substitutions in 48 proteins. The two bottom rows of the table are one number reported
twice, not an independent confirmation. Any downstream text should say so rather than presenting them
as two arms agreeing.

Both intervals span 0.5 and are roughly 0.22 wide. The interval on the filtered cohort is not narrower
than the unfiltered one.

## 3. Descriptive cutoff table with `|dpos| <= 2` removed

Primary cohort. "All substitutions" rows reproduce the published table; the filtered rows are new.
Because the filter removes no substitution beyond 5 Å, the "beyond" column is unchanged at every cutoff.

| filter | cutoff (Å) | n within | pos within | rate within | n beyond | pos beyond | rate beyond | descriptive OR |
|---|---|---|---|---|---|---|---|---|
| all | 5 | 10 | 4 | 0.400000 | 153 | 75 | 0.490196 | 0.693333 |
| all | 8 | 20 | 12 | 0.600000 | 143 | 67 | 0.468531 | 1.701493 |
| all | 10 | 30 | 17 | 0.566667 | 133 | 62 | 0.466165 | 1.497519 |
| all | 15 | 43 | 24 | 0.558140 | 120 | 55 | 0.458333 | 1.492823 |
| `dpos` > 2 | 5 | **4** | 2 | 0.500000 | 153 | 75 | 0.490196 | 1.040000 |
| `dpos` > 2 | 8 | 14 | 10 | 0.714286 | 143 | 67 | 0.468531 | 2.835821 |
| `dpos` > 2 | 10 | 24 | 15 | 0.625000 | 133 | 62 | 0.466165 | 1.908602 |
| `dpos` > 2 | 15 | 37 | 22 | 0.594595 | 120 | 55 | 0.458333 | 1.733333 |

The inclusive arm's filtered rows are byte-identical to the primary arm's filtered rows, for the reason
in §2; they are in `rr29_cutoffs.csv` but carry no additional information.

The 5 Å group after filtering is **4 substitutions in 4 proteins, 2 positive** (YGK3 S211A negative,
YPK1 T508A positive, SSK2 T1460A negative, SKY1 S388A positive). No interval is quoted for that bin:
at n = 4 with 2 positives a Wilson interval runs from roughly 0.15 to 0.85 and any binomial interval on
a proportion this small is uninformative. Report the count, not a rate.

The one apparent inversion in the published table — the 5 Å bin at 0.400 below the beyond-rate of 0.490,
OR 0.693 — is produced entirely by the peptide-bond-adjacent pairs. With them removed the 5 Å bin sits
at 2/4 and OR 1.040, indistinguishable from the far group. The 8 Å OR rises from 1.701 to 2.836, but
that is 10 positives of 14 and it moves back toward 1 at 10 and 15 Å.

## 4. Does this change the reading?

Removing sequence-adjacent pairs **leaves the reading unchanged: distance still carries no
discrimination.**

- The primary AUC moves 0.526823 → 0.540584, i.e. 0.014 further from chance, on a 95% interval of
  0.428570–0.648366 that comfortably contains 0.5. The inclusive AUC moves the other way,
  0.544135 → 0.540584. The shift is well inside the sampling noise of the estimate.
- The filter changes n by 6 of 163 substitutions and changes no protein count (48 before and after).
  There is no cohort large enough here for a 0.014 AUC change to mean anything.
- What the filter does change is the *story of the 5 Å bin*, and in the direction of removing an
  artifact rather than revealing a signal. The published sub-5 Å bin was half peptide-bond neighbours
  whose 1.33 Å distances are structurally uninformative; with those gone the bin is 4 substitutions,
  2 positive, and the descriptive OR is 1.04. That is a cleaner null, not a weaker or stronger one.

The defensible statement for the manuscript: the sub-5 Å bin is dominated by i±1 sequence neighbours at
the fixed C–N peptide-bond distance, and both the AUC and the descriptive cutoff table are insensitive
to their removal (primary AUC 0.541, 95% CI 0.429–0.648, n = 157 in 48 proteins, 77 positive).

## Caveats

- The `dpos <= 2` threshold is a choice, not something the data determines. There are no substitutions
  at `dpos` = 3–37 in this cohort (the distribution jumps from 2 to 38), so any threshold between 3 and
  37 gives the identical 157-row cohort. The result is robust to the threshold within that window and
  the window is wide, but the threshold is still declared post hoc.
- The 4-substitution 5 Å bin is too small for any inferential claim. It is reported as counts.
- Bootstrap intervals here use 20,000 draws at seed 20260728 as declared for post hoc sensitivity; the
  published headline intervals use 200,000 draws and seed `SEED + 1` for the protein-cluster arm. Point
  estimates are unaffected by that difference; interval endpoints will differ in the third decimal.
- None of these numbers is in `NUMBERS.md`. Anything from §2–§3 that goes into reader-facing text must
  be entered there first by the author.
