# Third-Party Data and Notices

## Scope

This file inventories third-party source classes used by the release. File-level paths, URLs, versions,
and SHA-256 values for redistributed caches are in
`release_metadata/third_party_data_manifest.csv`. Original project software is covered separately by the
MIT `LICENSE`.

## Viéitez et al. supplementary workbooks

- Source: Cristina Viéitez, Bede P. Busby, David Ochoa, et al. *High-throughput functional
  characterization of protein phosphorylation sites in yeast*. *Nature Biotechnology* 40, 382–390
  (2022). DOI: <https://doi.org/10.1038/s41587-021-01051-x>. Europe PMC: <https://europepmc.org/articles/PMC7612524>.
- Terms identified in the Europe PMC full-text record: Springer Nature accepted-manuscript terms,
  <https://www.springernature.com/gp/open-research/policies/accepted-manuscript-terms>.
- Release decision: **not redistributed**. `tools/fetch_sources.py` retrieves the files from the
  authoritative Europe PMC supplementary endpoint and verifies the required workbook hashes.

## Kennedy et al. supplementary tables

- Source: Philip H. Kennedy, Amin Alborzian Deh Sheikh, Matthew Balakar, et al. *Post-translational
  modification-centric base editor screens to assess phosphorylation site functionality in high
  throughput*. *Nature Methods* 21, 1033–1043 (2024). DOI:
  <https://doi.org/10.1038/s41592-024-02256-z>. Europe PMC: <https://europepmc.org/articles/PMC11804830>.
- Release decision: **not redistributed**. `kennedy_replication/README.md` states which file is needed
  and where it goes. The derived cohort `kennedy_replication/kennedy_analysis.csv` is an original
  research table produced by this project from that source.

## Ochoa et al. functional-score supplementary data

- Source: David Ochoa, Andrew F. Jarnuczak, Cristina Viéitez, et al. *The functional landscape of the
  human phosphoproteome*. *Nature Biotechnology* 38, 365–373 (2020). DOI:
  <https://doi.org/10.1038/s41587-019-0344-3>.
- Use: the 59-feature annotated phosphoproteome, twelve features of which were tested as candidate
  positive controls in `kennedy_replication/positive_control.py`.
- Release decision: **not redistributed**.

## Charis SIL

- Source: SIL International, Charis SIL 6.101, <https://software.sil.org/charis/>.
- License: SIL Open Font License 1.1, reproduced verbatim at `manuscript_build/fonts/OFL.txt`.
- Release decision: **redistributed** under `manuscript_build/fonts/`, which the OFL permits. The four
  files are the upstream release, unmodified. They are vendored because the copies embedded in a PDF are
  content-reduced and cannot typeset new text, so without them the manuscript cannot be rebuilt in its
  own design. The OFL's reserved font name applies: a modified version may not be called "Charis SIL".

## UniProt database content

- Source: UniProt Knowledgebase records and reviewed *Saccharomyces cerevisiae* proteome data retrieved
  through the UniProt REST API.
- License: Creative Commons Attribution 4.0 International for copyrightable database content,
  <https://www.uniprot.org/help/license>.
- Required attribution/citation: The UniProt Consortium, *UniProt: the Universal Protein Knowledgebase
  in 2023*, *Nucleic Acids Research* 51, D523–D531 (2023), DOI
  <https://doi.org/10.1093/nar/gkac1052>.
- Release decision: the checksum-pinned TSV and JSON caches are redistributed under CC BY 4.0 so a
  clean-room rerun does not silently move to a later database release. UniProt's disclaimer and possible
  third-party rights continue to apply.

## AlphaFold Protein Structure Database content

- Source: AlphaFold DB v6 monomer mmCIF models, metadata, and predicted aligned error documents.
- Copyright and license: AlphaFold Data Copyright (2021) DeepMind Technologies Limited; data available
  under Creative Commons Attribution 4.0 International. License and disclaimer:
  <https://alphafold.ebi.ac.uk/assets/License-Disclaimer.pdf>.
- Required citations: Jumper et al., *Nature* 596, 583–589 (2021), DOI
  <https://doi.org/10.1038/s41586-021-03819-2>; Varadi et al., *Nucleic Acids Research* 52, D368–D375
  (2024), DOI <https://doi.org/10.1093/nar/gkad1011>.
- Release decision: exact v6 mmCIF, metadata, and locally gzip-compressed PAE caches are redistributed
  under CC BY 4.0 with file-level source URLs and hashes. The AlphaFold DB disclaimer applies: these are
  predictions with variable confidence and are provided as-is.

## Software dependencies

Third-party Python packages are installed from their upstream distributions and are not vendored in the
archive. Their exact versions are listed in `requirements-lock.txt`; each retains its upstream license.
