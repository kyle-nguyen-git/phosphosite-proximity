# Robustness arms

Two analyses added after the round-1 review, both on the yeast cohort. `NUMBERS.md` Section 21 is the
numerical authority for both, and carries their claim rules.

Everything these scripts need is in this repository. No third-party download, no network.

## `qc_inclusive_arm.py` — restoring the source quality-control exclusions

The two source filters removed 38 strain records, 34 of them screen-positive against 39.6% among the 427
kept, and the scar-correlation filter decides by comparing a strain's phenotype to a marker control — so
for those records the exclusion depends on the outcome. The objection is that dropping
outcome-associated records and then reporting a near-chance estimate manufactures the result.

Two things come out of it.

All 20 scar-flagged records sit in proteins for which UniProt records no active or binding site, so they
are removed by annotation eligibility before that filter is ever consulted. The filter conditioned on
the outcome removes nothing from the analysis cohort.

Of the 38, ten are in a protein carrying an eligible annotation with a model, and all ten are
screen-positive. Restoring them adds nine sites the cohort does not otherwise contain:

| Arm | n | Positive | AUC | 95% interval |
|---|---:|---:|---:|---:|
| Primary as published | 163 | 79 | 0.526823 | 0.416170–0.631766 |
| QC-inclusive | 172 | 88 | 0.501894 | 0.392384–0.608166 |

Restoring the exclusions moves the estimate toward chance by 0.0249, not away from it.

```bash
python qc_inclusive_arm.py    # ~3 min; 200,000 protein-cluster resamples per arm
```

The script recomputes the primary arm alongside the new one. If its primary row does not reproduce
`NUMBERS.md` Section 12 to six decimals, its cohort assembly has drifted from the pipeline and its
second row should not be believed.

## `bootstrap_coverage.py` — measuring the interval's coverage

The manuscript's headline product is an interval on 48 uneven protein clusters with a Kish effective
count of 29.0. Resampling more times controls resampling noise; it does not make a percentile interval
cover at its stated rate. This measures what the coverage actually is.

Cohorts are rebuilt 1,000 times at the observed structure — the real protein-size distribution, the
observed prevalence, and a protein-level random intercept set from the outcome intraclass correlation
measured on the real cohort — under five known population AUCs.

| True AUC | Percentile coverage | BCa coverage |
|---:|---:|---:|
| 0.50 | 0.936 | 0.942 |
| 0.55 | 0.941 | 0.945 |
| 0.60 | 0.949 | 0.952 |
| 0.65 | 0.941 | 0.943 |
| 0.70 | 0.948 | 0.953 |

Monte Carlo standard error is 0.0069. The declared interval covers between 0.936 and 0.949; the worst
case is the null scenario, which is where the primary estimate sits, short by 1.4 points or two Monte
Carlo standard errors. BCa is nearer nominal everywhere but by less than the Monte Carlo error at four
of five scenarios, so it is reported rather than adopted.

```bash
python bootstrap_coverage.py   # ~8 min
```

Before simulating anything the script asserts its AUC equals the frozen `auc_from_ranks` on the real
cohort to within 1e-12. If that assertion fails the coverage numbers describe a different estimator than
the one the paper uses.

## Paths

`_paths.py` locates the calibration tree and the frozen estimator by probing for files that must exist,
because this repository is flattened — `results/`, `data/` and `src/` at the root, with the robustness
analysis under `robustness/` — while the working tree these were written in nests everything under
`phase0_calibration/` and calls that directory `phase0_5/`. Hardcoding either layout breaks the other.
