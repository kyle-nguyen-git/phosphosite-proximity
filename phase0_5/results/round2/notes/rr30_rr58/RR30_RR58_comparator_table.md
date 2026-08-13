# RR-30 / RR-58 — comparator predictor table (primary cohort)

Proposed numbers. Nothing here has been entered into `NUMBERS.md`; the author does that.

## Provenance and conventions

- Frozen hashes verified before computing; all three match.
  - `results/statistics.json` = `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`
  - `results/analysis_final.csv` = `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`
  - `phase0_5/results/phase0_5_statistics.json` = `3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b`
- Estimators loaded from `phase0_5/src/02_phase0_5_analysis.py` (`auc_from_ranks`,
  `bootstrap_auc`, `paired_auc_difference`). That module is guarded by
  `if __name__ == "__main__": main()`, checked in-script before import, so importing it as
  `p05` does not execute `main()`. No estimator was reimplemented.
- Cohort: `phase0_5/results/phase0_5_analysis.csv` filtered on
  `cohort_primary_exclude_annotation_coincident`. n = 163 sites, 79 positives, 48 proteins.
  The (acc, pos) key set is identical to `results/analysis_final.csv`.
  `protein_length` exists only in the phase-0.5 table, which is why that table is the source.
- Bootstrap: 20,000 protein-cluster draws, seed 20260728 (= module `SEED`,
  `N_SENSITIVITY_BOOT`). Resampling unit is the UniProt accession; every substitution retained.
- Retained draws reported for every interval (RR-13). All 15 intervals retained 20,000 / 20,000 —
  no resample drew a single outcome class, expected with 79/163 positives spread over 48 proteins.
- No interval endpoint touches 0 or 1, so every interval is reportable as computed.
- Missingness: none. All eight predictors are complete on all 163 rows, so common support for
  every paired comparison is the full 163 and no comparison is run on a reduced set.

## Eligible target set (the check you asked for)

From `results/uniprot_features_detailed.csv`, `feat_type` in {`Active site`, `Binding site`}:

| quantity | value |
|---|---|
| total feature records in file | 278 |
| eligible records (ACT_SITE + BINDING) | 262 (41 active site, 221 binding site) |
| **unique target residues after interval expansion** | **560** |
| accessions carrying at least one eligible target | 50 |
| cohort accessions with no eligible target | 0 |

560 matches `NUMBERS.md` Section 4 exactly. The excluded types are `Site` (8 records) and
`DNA binding` (8 records), which is the correction the earlier check needed.

One bookkeeping discrepancy, flagged rather than papered over: `NUMBERS.md` Section 4 says
"564 feature-residue rows representing 560 unique residues". Expanding all 262 eligible records
gives **594** record-residue rows; deduplicating on (acc, start, end) gives 565, and on
(acc, start, end, feat_type) gives 566. I cannot reproduce 564 by any simple rule. The excess over
560 comes from P12904, whose 221–222 and 309–312 intervals are each recorded three times (ADP, AMP,
ATP ligands). The unique-residue count — the thing that defines the target set — is unaffected.

## Table

All predictors signed so that increasing score is the direction hypothesised to favour a
screen-positive label. "Orientation" states which raw direction that is.

| # | Predictor | Orientation | n | AUC | 95% CI (protein cluster) | draws nominal / retained | Δ AUC vs min_dist_A | Δ 95% CI | Δ draws nom / ret |
|---|---|---|---|---|---|---|---|---|---|
| 1 | min \|pos − target pos\|, eligible ACT_SITE+BINDING set | smaller → positive | 163 | 0.5498040989 | 0.4340704552 – 0.6526297339 | 20000 / 20000 | +0.0229807113 | −0.0493801068 – +0.0902666092 | 20000 / 20000 |
| 2 | \|pos − nearest_feat_pos\| (seq sep to 3D-nearest target) | smaller → positive | 163 | 0.5333785413 | 0.4155022136 – 0.6391446767 | 20000 / 20000 | +0.0065551537 | −0.0837502209 – +0.0933298291 | 20000 / 20000 |
| 3 | protein_length | larger → positive | 163 | 0.5493520193 | 0.4437904559 – 0.6596844589 | 20000 / 20000 | +0.0225286317 | −0.1587297500 – +0.2154142057 | 20000 / 20000 |
| 4 | site pLDDT | larger → positive | 163 | 0.5551537071 | 0.4636676033 – 0.6407906549 | 20000 / 20000 | +0.0283303195 | −0.0667388543 – +0.1313504601 | 20000 / 20000 |
| 5 | inverse relative solvent accessibility (−rsa) | smaller rsa → positive | 163 | 0.5866485835 | 0.4890609978 – 0.6719102695 | 20000 / 20000 | +0.0598251959 | −0.0413000990 – +0.1619905318 | 20000 / 20000 |
| 6 | n_annot_residues (annotated-target count) | larger → positive | 163 | 0.5553797468 | 0.4701126761 – 0.6485675836 | 20000 / 20000 | +0.0285563593 | −0.0822575359 – +0.1522954487 | 20000 / 20000 |
| 7 | raw_conditions (bookkeeping negative control) | larger → positive | 163 | 0.4615732369 | 0.4259259259 – 0.4957457390 | 20000 / 20000 | −0.0652501507 | −0.1832896737 – +0.0574866346 | 20000 / 20000 |
| 8 | **min_dist_A (declared predictor)** | smaller → positive | 163 | 0.5268233876 | 0.4161064594 – 0.6305511618 | 20000 / 20000 | 0 (reference) | not reported | — |

No paired interval is reported for row 8: the difference of a predictor against itself is
identically 0 in every resample, so an interval would be [0, 0] and carries no information.

## Reconciliation against the prior spot checks

Every prior value reproduces.

| prior spot check | value here | agrees |
|---|---|---|
| sequence separation 0.5498 | 0.5498040989 (row 1) | yes |
| inverse RSA 0.5866 | 0.5866485835 | yes |
| pLDDT 0.5552 | 0.5551537071 | yes (0.5552 to 4 dp) |
| target count ~0.5554 | 0.5553797468 | yes |
| protein length ~0.549 | 0.5493520193 | yes |
| raw_conditions ~0.462 | 0.4615732369 | yes |
| distance 0.5268 | 0.5268233876 | yes |

The prior list has seven values for eight predictors. Row 2, `|pos − nearest_feat_pos|`
(0.5333785413), had no prior spot check; the "sequence separation 0.5498" figure corresponds to
row 1, the minimum over the eligible target set, not to row 2. These are different quantities —
row 1 minimises sequence separation over all eligible targets, row 2 reads off the sequence
separation of whichever target is nearest in 3D — and they differ by 0.0164 in AUC.

## What excludes 0.5, and what excludes 0

**AUC intervals excluding 0.5: exactly one, and it is the negative control.**
`raw_conditions` has interval 0.4259259259 – 0.4957457390, entirely below 0.5. All seven substantive
predictors — including the declared distance predictor and the best-performing inverse RSA
(0.5866, CI 0.4891 – 0.6719) — have intervals that contain 0.5.

**Paired differences excluding 0: none.** All seven intervals against `min_dist_A` straddle zero.
The largest point difference, inverse RSA at +0.0598, has interval −0.0413 – +0.1620.

So: on the primary cohort, no comparator is distinguishable from chance, none is distinguishable
from minimum heavy-atom distance, and the only variable whose interval clears 0.5 is a bookkeeping
count that should carry no signal at all.

## Two things that are not clean

1. **The `raw_conditions` result is real but mechanically odd, and it is not Monte Carlo noise.**
   The variable takes five values on the cohort and 155 of 163 sites share the value 102, so almost
   every pair is tied and contributes exactly 0.5 to the AUC. The point estimate is therefore pinned
   near 0.5 by construction and the bootstrap interval is narrow for the same reason — a narrow
   interval here reflects near-constancy, not precision about a real effect. Re-running the interval
   at seeds 20260729, 1, 12345 and 999999 gives upper bounds 0.4954, 0.4955, 0.4963, 0.4957: the
   exclusion of 0.5 is stable to resampling error, and it is driven by 8 sites. I would report it as
   an artifact of the tie structure and of those 8 sites, not as evidence that condition count is
   anti-predictive. Its paired difference against distance (−0.0653, CI −0.1833 – +0.0575) does
   include zero, which is the more honest comparison.

2. **"Scored in the direction that would favour a screen-positive label" is under-determined for
   rows 3, 4, 6 and 7.** For distance and for RSA the direction follows from the hypothesis
   (closer, more buried). For protein length, pLDDT, target count and condition count there is no
   comparable prior, so I fixed the orientation as larger → positive for all four, which is the
   choice that reproduces every prior spot check including the sub-0.5 value for `raw_conditions`.
   Flipping any of these maps AUC to 1 − AUC and the paired difference accordingly; none of the
   qualitative conclusions change, since all four intervals contain 0.5 in either orientation
   except `raw_conditions`, which would then read 0.5384 (CI 0.5043 – 0.5741). If a reader-facing
   version of this table ships, the orientation of these four should be stated on its face.

## Files

- Script: `notes/rr30_rr58/rr30_rr58_comparator_table.py`
- Results: `notes/rr30_rr58/rr30_rr58_comparator_table.csv`,
  `notes/rr30_rr58/rr30_rr58_comparator_table.json`
- Nothing outside `notes/rr30_rr58/` was created or modified. The task specification gave the
  output directory as the literal string `undefined` (a templating failure); `notes/` was empty,
  so `notes/rr30_rr58/` was created inside it and no existing file was touched.
- One unavoidable side effect to disclose: importing the frozen analysis module caused CPython to
  refresh `phase0_5/src/__pycache__/02_phase0_5_analysis.cpython-312.pyc`. That is an automatic
  bytecode cache, regenerated deterministically from unchanged source. The source is byte-identical
  (`02_phase0_5_analysis.py` sha256 `cba6d8c7b440c967096c57a66f8c2d419a358e4ba9750ea21bd2c4461c87aa49`,
  mtime unchanged at 2026-07-29 16:30) and all three frozen hashes re-verify after the run.
  The two other inputs read are also unchanged:
  `results/uniprot_features_detailed.csv` sha256 `9fa9a87a11756bf147f4e6a20853ecd1ca5aaf7966812e3da155c363ecf5e614`,
  `phase0_5/results/phase0_5_analysis.csv` sha256 `8437294a8a94d2cf280e4811cbd2221326da4f250728375a9a06f1f8b760b801`.
