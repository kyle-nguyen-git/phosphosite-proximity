# Source Retrieval and Checksum Contract

## Summary

This file covers the **yeast** cohort, which `tools/fetch_sources.py` retrieves and hash-verifies. The
**human** cohort added on 2026-08-13 has its own sources, listed at the end of this file and described
in `kennedy_replication/README.md`; `fetch_sources.py` does not retrieve them and does not know about
them.

The yeast analysis requires four supplementary workbooks from Viéitez et al., *High-throughput
functional characterization of protein phosphorylation sites in yeast* (DOI
[`10.1038/s41587-021-01051-x`](https://doi.org/10.1038/s41587-021-01051-x); Europe PMC
[`PMC7612524`](https://europepmc.org/articles/PMC7612524)). They are not included in this repository or
archive.

The Europe PMC copy is an accepted manuscript governed by the source article's stated
[accepted-manuscript terms](https://www.springernature.com/gp/open-research/policies/accepted-manuscript-terms).
Those terms permit academic research access and data mining but are not treated here as permission to
redistribute the supplementary workbooks. Each user retrieves the source from Europe PMC directly.

## Automated retrieval

From the release root:

```bash
python tools/fetch_sources.py
```

The script downloads the Europe PMC supplementary archive, extracts only Supplementary Data 1, 3, 6,
and 8, and verifies each workbook against `sources.lock.json` before placing it under `data/`. It does
not extract or retain the other article files. A changed archive container is accepted only when every
required inner workbook still matches its frozen SHA-256; any changed required workbook fails closed.

For an offline or manually downloaded archive:

```bash
python tools/fetch_sources.py --archive /absolute/path/to/PMC7612524_supplementary.zip
```

## Source roles

- Supplementary Data 1: point-mutant constructs and coordinates.
- Supplementary Data 3: condition-level S-scores and source q-values; this is the outcome ledger.
- Supplementary Data 6: annotations only; it does not select the analytical cohort.
- Supplementary Data 8: strain-specific WGS and scar-control-correlation exclusions.

The exact URL, source citation, archive observation, and required workbook hashes are machine-readable in
`sources.lock.json`.

## Human cohort sources (Kennedy 2024), added 2026-08-13

These are **not** retrieved or hash-verified by `tools/fetch_sources.py`. They are downloaded by hand,
or by `kennedy_replication/build_cohort.py` in the case of UniProt and AlphaFold. None is redistributed.

| Source | Where it goes | Retrieved by |
|---|---|---|
| Kennedy et al. 2024 Supplementary Tables, *Nature Methods* 21:1033–1043, DOI [`10.1038/s41592-024-02256-z`](https://doi.org/10.1038/s41592-024-02256-z), Europe PMC [`PMC11804830`](https://europepmc.org/articles/PMC11804830) | `kennedy_replication/cache/kennedy_supplement.xlsx` | by hand from the publisher |
| Ochoa et al. 2020 Supplementary Data, *Nature Biotechnology* 38:365–373, DOI [`10.1038/s41587-019-0344-3`](https://doi.org/10.1038/s41587-019-0344-3) | `kennedy_replication/cache/ochoa_functional_score.xlsx` | by hand from the publisher |
| UniProt entry JSON, one per accession | `kennedy_replication/cache/uniprot/` | `build_cohort.py`, UniProt REST |
| AlphaFold DB v6 monomer models | `kennedy_replication/cache/af/` | `build_cohort.py`, AlphaFold DB API |

Together these are about 730 MB, which is why the derived cohort `kennedy_replication/kennedy_analysis.csv`
is shipped instead: `analyse.py` and `perturbation_arms.py` reproduce the reported estimates from it
without the originals.

**No checksum contract exists for these four sources.** The yeast workbooks are pinned by SHA-256 in
`sources.lock.json`; the human sources are not, so a silent upstream revision would not be detected.
That is a real gap and is recorded rather than papered over.
