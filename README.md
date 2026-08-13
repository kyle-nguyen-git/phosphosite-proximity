# phosphosite-proximity

Proximity features in a yeast phosphosite-mutant screen.

Code and derived data for a two-author exploratory secondary analysis of a public yeast
phosphosite-mutant growth screen (Viéitez et al. 2022).

**What this measures.** For each serine, threonine or tyrosine site replaced by alanine in the source
screen, we compute the shortest distance between non-hydrogen atoms of that residue and the nearest
residue UniProt annotates as an active site (`ACT_SITE`) or a binding site (`BINDING`), in an AlphaFold
DB version 6 model of the protein on its own. A site counts as affected when the source study reported a
growth change in at least one condition, in either direction. The analysis asks what that distance
measurement is made of and how well it separates affected from unaffected sites.

**Status.** Exploratory, not peer reviewed, and not yet posted to a preprint server. An independent
methods review is underway; see `METHODS_REVIEW.md`. Nothing here has been through peer review, and
the AI-assistance disclosure in the manuscript describes how the work was produced. The primary cohort
designation was made after the outcome data had been inspected, and most analyses here are post hoc; `NUMBERS.md` Section 13 records which
claims the evidence does and does not support. No manuscript is posted yet, and this repository has no
archived DOI.

**Authors.** Kyle Nguyen and Arkady Marchenko, College of Natural Sciences, The University of Texas at
Austin. The work was carried out independently of the university, without institutional funding,
supervision, or resources, and implies no endorsement by UT Austin.

**`NUMBERS.md` is the numerical authority.** Every number in the manuscript comes from it, and its
header freezes the three canonical analysis artifacts by SHA-256. The verifier checks those hashes
before loading any reported result. If you want to check a claim, start there.

**Licensing.** `LICENSE` (MIT) covers the original analysis code only. It does not license the
third-party data caches, the source-study supplements, the manuscript, or the figures — see
`LICENSES.md` and `THIRD_PARTY_NOTICES.md`.

**Source data are not redistributed.** The four Viéitez supplementary workbooks carry their own terms
and are not in this repository. `SOURCE_RETRIEVAL.md` gives the Europe PMC record, the exact filenames,
and their checksums, and the pipeline fetches and verifies them for you.

**Reproducibility, honestly.** `reproduce.sh` rebuilds the analysis from the source workbooks and
the pinned environment, and the fail-closed verifier checks every reported number against
`NUMBERS.md`. One limit is worth knowing before you run it: the *figure* hash checks are
environment-specific. matplotlib bundles a FreeType whose version depends on how matplotlib was
built, and the committed figures were rendered against FreeType 2.12.1. A pip-installed matplotlib
brings 2.6.1 and renders glyphs differently, so `panel_figures_match_numbers` will fail for you even
when the analysis is correct. The numerical outputs are unaffected — see `NUMBERS.md` Section 17.

**Methods review.** `METHODS_REVIEW.md` is the packet for the independent methods read: what to
look at, nine questions to answer, and the record to fill in. It is open — no review has been
completed.

**The manuscript.** `manuscript/preprint_current.{md,pdf}` is the current draft — two authors, and it
makes no exclusion claim. `manuscript/preprint_draft_v1.*` is a superseded single-author draft that
states a claim since retired; it stays only because the verification pipeline binds to its hash and page
count. `manuscript/README.md` explains the difference. Nothing is posted to a preprint server yet.

`NUMBERS.md` is the sole numerical authority for manuscript and release claims. Its header freezes the
three canonical analysis artifacts by SHA-256, and the verifier checks those hashes before loading any
reported result.

## Reproduce

The tested environment is macOS 15.7.2 on arm64, CPython 3.12.4, and Poppler `pdftoppm`
26.05.0. The release runner fails on another Python patch version and requires `pdftoppm` on `PATH`.
Install the complete version-pinned Python environment:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
PYTHON_BIN=.venv/bin/python ./reproduce.sh
```

The reproduction runner:

1. retrieves only the four required Viéitez source workbooks from Europe PMC and verifies their hashes;
2. verifies every redistributed UniProt and AlphaFold cache against a file-level manifest;
3. rebuilds the parent Phase 0 and the robustness analysis analyses from one named two-arm pipeline;
4. rebuilds the supplement, both figure lineages, manuscript PDF, and rendered-page manifest; and
5. runs the fail-closed scientific and release verifiers.

Two figure lineages exist and `NUMBERS.md` Section 17 is authoritative on which is which.
`manuscript/src/build_figure1.py` and `robustness/src/03_robustness_figure.py` build the figures embedded in
the frozen review PDF. `manuscript/panels/build_all.sh` builds six panels under `manuscript/panels/src/`
and composes them into `manuscript/figure1.{png,pdf}` and `manuscript/figure2.{png,pdf}`, which are the
figures the editable two-author manuscript embeds. Panel builds are byte-reproducible: PDF creation
dates are suppressed and the composer writes no document `/ID`. The cohort counts panels assert against
are parsed from `NUMBERS.md` Sections 1 and 4 at build time, and three verifier checks bind the composed
figures to the hashes declared in Section 17.

Source retrieval requires network access to the Europe PMC endpoint. Python package versions are fully
pinned, but wheel/sdist distribution hashes are not; the clean-room report records the installed
environment. Source-study files and redistributed scientific caches are separately checksum-addressed.

## Build and test the release archive

After `reproduce.sh` passes on a quiescent tree:

```bash
.venv/bin/python tools/build_release.py
.venv/bin/python tools/run_clean_room.py
.venv/bin/python tools/verify_release_package.py \
  --archive release/dist/phosphosite-proximity-v0.5.0-rc1.tar.gz
```

The package builder emits a deterministic archive plus `release/package_build_report.json`. The
clean-room command creates a second fresh virtual environment, runs the exact archive from an empty
temporary directory, and writes the companion `release/clean_room_report.json`. The final verifier
requires that report to name the exact archive SHA-256 and requires the archive's source fingerprint and
file manifest to match the live candidate. Runtime reports are intentionally outside the archive to
avoid a self-referential archive hash.

The Viéitez workbooks are intentionally absent from the release archive. See `SOURCE_RETRIEVAL.md`.
Cached UniProt and AlphaFold DB records are included under their CC BY 4.0 terms so the structural inputs
do not drift during a clean-room rerun. See `THIRD_PARTY_NOTICES.md` and
`release_metadata/third_party_data_manifest.csv`.

## Main artifacts

- `manuscript/preprint_draft_v1.md` and `.pdf` — review manuscript; still marked not for posting until
  human author and external-review gates are signed.
- `robustness/results/robustness_supplement.xlsx` — reproducibly generated supplementary workbook.
- `robustness/results/verification_report.json` — scientific reconciliation report.
- `release/clean_room_report.json` and `release/release_readiness_report.json` — companion technical
  evidence for the exact local archive.
- `release/RELEASE_CHECKLIST.md` — technical, author, external-review, and deposition gates.
- `release/AUTHOR_SIGNOFF.md` — fields that only Kyle Nguyen can attest.
- `release/EXTERNAL_METHODS_REVIEW.md` — packet for a genuinely independent human reader.

## Status

This is a local release candidate, not a public preprint, peer-reviewed article, repository release, or
DOI-bearing record. AI-assisted adversarial reports in `robustness/reviews/` are internal review aids and
do not satisfy the independent-review gate.

## Licenses

Original software is MIT licensed. Third-party data retain their source licenses and terms. The author
must select and sign the license for the manuscript, original figures, and derived research tables before
public deposition. Scope is detailed in `LICENSES.md`.
