# Human replication — Kennedy 2024

The second cohort in Results §2.7 of the manuscript. Human Jurkat and HEK293 cells, phosphosites altered
by base editing. **Two screens with different readouts, not one proliferation endpoint:** Supplementary Table 3 compares sgRNA abundance before and after ABE8e introduction, a fitness readout; Supplementary Table 4 compares GFP-high against GFP-low bins, an NFAT reporter-activity readout. Every "either screen" figure is a union across two phenotypes. See `NUMBERS.md` Section 22.

Kennedy PH, Alborzian Deh Sheikh A, Balakar M, et al. Post-translational modification-centric base
editor screens to assess phosphorylation site functionality in high throughput. *Nature Methods*
2024;21:1033–1043. doi:10.1038/s41592-024-02256-z. PMC11804830.

`NUMBERS.md` Section 20 is the numerical authority for everything here, and Section 20.9 carries the
binding claim rules. Do not restate a number from a script's output into a manuscript, slide or email —
take it from Section 20.

## What is here, and what is not

Shipped: the scripts, and the derived cohort and results they produce.

| File | What it is |
|---|---|
| `build_cohort.py` | Assembles the cohort: UniProt features, AlphaFold models, distances |
| `analyse.py` | Primary estimate, sensitivities, paired differences, permutation null |
| `perturbation_arms.py` | Splits the cohort by what the editor did to the target residue |
| `positive_control.py` | Twelve published Ochoa 2020 features tested on this outcome |
| `endpoint_characterisation.py` | Shows the outcome column is not a p-value, and repairs it |
| `kennedy_analysis.csv` | The derived cohort: 1,475 sites in 793 proteins |
| `*.json` | The results each script wrote |

Not shipped, for the same reason the yeast source workbooks are not: they are third-party files this
project does not have the right to redistribute, and together they are about 730 MB.

| Needed | Size | Where it goes |
|---|---:|---|
| Kennedy 2024 Supplementary Tables | ~38 MB | `cache/kennedy_supplement.xlsx` |
| Ochoa 2020 Supplementary Data | ~52 MB | `cache/ochoa_functional_score.xlsx` |
| UniProt entry JSON, one per accession | ~61 MB | `cache/uniprot/` |
| AlphaFold DB v6 monomer models | ~579 MB | `cache/af/` |

`build_cohort.py` retrieves the UniProt and AlphaFold files itself and caches them; the two supplement
workbooks must be downloaded from the publishers. `SOURCE_RETRIEVAL.md` at the repository root records
the retrieval for every source.

## Running

`analyse.py` and `perturbation_arms.py` need only `kennedy_analysis.csv`, which is shipped, plus the
Kennedy supplement for the perturbation classes. `positive_control.py` needs the Ochoa workbook.
`endpoint_characterisation.py` needs the Kennedy supplement. `build_cohort.py` needs the network and
several hours.

```bash
python analyse.py                  # reproduces Section 20.3-20.5 from the shipped cohort
python endpoint_characterisation.py   # reproduces Section 20.10; needs the Kennedy workbook
```

Estimators are not reimplemented here. `_paths.py` locates the frozen analysis module — this repository
ships it as `robustness/src/02_robustness_analysis.py`, and the working tree it was written in calls it
`phase0_5/src/02_phase0_5_analysis.py` — so both cohorts are computed by the same code and the
comparison between them means something.

## One thing to read before using any number here

The screen's released per-site value is the smaller of MAGeCK's two one-sided gene-level p-values, not a
two-sided p-value. Under the null that minimum is distributed roughly uniformly on 0 to 0.5, so the 0.05
cut-off used for the primary endpoint admits about twice the nominal rate — measured at 10.5% and 9.9%
on the two screens' non-control sites. The error runs in the direction that favours the manuscript's
near-chance reading, because label noise pulls an AUC toward 0.5.

Section 20.10 records this, and reports the estimate under two definitions that do not inherit the
defect: a corrected two-sided test, and the top decile of log fold change, which uses no p-value at all.
Both contain 0.5. The precision claim is quoted from the repaired endpoint — half-width 0.056 against
0.107 in yeast, not the 0.040 the uncorrected label gives.
