# Source Retrieval and Checksum Contract

## Summary

The analysis requires four supplementary workbooks from Viéitez et al., *High-throughput functional
characterization of protein phosphorylation sites in yeast* (DOI
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
