# AI-Assisted Internal Reproducibility and Release Review

**Date:** 2026-07-29  
**Scope:** Current release/reproduction tooling and package boundary only. The analysis was not rerun. This is an AI-assisted internal audit, not author approval, independent human review, peer review, or permission to post.

> **Post-review serialization addendum:** The subsequent clean-environment run found only last-bit
> BLAS drift in continuous-model serialization. The deterministic contract and current refrozen hash
> are in `NUMBERS.md`; hashes and archive observations below describe the pre-fix audit snapshot.

## Verdict

**Technical release status: not complete.** The frozen numerical sources remain intact, and the current PDF/render set and supplement pass read-only consistency checks. The built archive and recorded verification reports do not represent the current tree, and no fresh-environment reproduction report exists.

## Numerical Authority Check

This check was completed before considering any project result. The three SHA-256 values frozen in `NUMBERS.md` match the current files exactly:

- `results/statistics.json` — `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401`
- `results/analysis_final.csv` — `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4`
- `phase0_5/results/phase0_5_statistics.json` — `569a3c5eab309e3ac3572d84718ce8b59ad3bd0762ed9d085aeafb6584f2e3e9`

No numerical source other than `NUMBERS.md` was treated as authoritative.

## Blockers

1. **The archive is not the current release candidate.** Current `NUMBERS.md` binds the manuscript PDF to SHA-256 `ee7854dd5e4d6d7dfa50542e0cce4d53bcbd221f0ccf991571a07ce3afccc462`, which matches the live PDF and render manifest. The existing archive contains the earlier PDF and `NUMBERS.md` state bound to `d950619eafa53d68905a983bebdf4179b7d2d7757f4e654d53b050fa9ce16868`. It also omits the reviews README, response log, and this review; its supplement and verification artifacts differ from the live tree. The archive must be rebuilt from a quiescent current snapshot.
2. **No clean-room evidence exists.** `release/clean_room_report.json` is absent. `release/RELEASE_CHECKLIST.md` correctly leaves fresh-environment reproduction in progress, but `phase0_5/reviews/RESPONSE_LOG.md` incorrectly says that the report records a fresh-environment run. Do not claim standalone reproduction until `tools/run_clean_room.py` succeeds on the rebuilt archive and the report is retained.
3. **The recorded technical verdict is not releasable.** `release/release_readiness_report.json` currently reports `FAIL` because this review was absent, and it records the older PDF/archive snapshot. Creating this file resolves only the source-tree existence check; the scientific verifier, release manifest, archive builder, archive verifier, and clean-room run still need to be executed in order on one unchanged snapshot.

## Majors

1. **Archive freshness is not enforced by `verify_release_package.py`.** Its archive mode checks path safety, source-workbook omission, and internal checksums, while required-document checks are performed against the live root. It does not require the archive's package manifest or source-tree fingerprint to equal the current source tree. A stale, internally valid archive can therefore pass after the live-root review file appears. Compare fingerprints and required file hashes inside the archive, or make a passing clean-room report for the exact archive mandatory input to release readiness.
2. **The environment contract is incomplete.** `render_preprint.py` requires host `pdftoppm`, but the README and Python lock do not install or version Poppler. The clean-room tool also creates its environment from the invoking interpreter; the README permits any CPython 3.12 although `NUMBERS.md` records CPython 3.12.4. The dependency file pins versions but not distribution hashes. Document the supported OS, exact interpreter, Poppler installation/version, and network requirement; preferably add a container or hash-locked installation path.
3. **License metadata remains mixed.** `CITATION.cff` declares `MIT`, while `LICENSES.md` limits MIT to original software and leaves the manuscript, figures, and derived tables under an author-selected future license. Before deposition, make the citation/archive metadata express the scoped mixed-license package and the author's signed choice without implying that MIT covers research artifacts or third-party caches.

## Minors

- The root README documents reproduction but not the supported commands for package build, archive verification, or clean-room execution. Add the release sequence and expected reports.
- The duplicate Phase 0.5 `CITATION.cff` is not checked against the canonical root file and can drift; either generate it or verify the shared fields.
- The review PDF is untagged. This is not a scientific blocker, but a public production route should add semantic tagging and an accessibility check.

## Passed Checks

- The frozen numerical hashes above were independently recomputed and match.
- Current PDF-to-render-manifest binding, page-image hashes, and contact-sheet hash pass.
- The current supplementary workbook has the expected 22 sheets and tables, matches CSV row counts, and contains no formulas or spreadsheet error tokens.
- Shell entry points pass `bash -n` and retain executable mode; all 38 Python files parse successfully.
- The source-study workbooks are excluded from the archive and have authoritative retrieval plus inner-file checksum contracts. The inspected archive has one safe top-level tree, no symlinks or unsafe paths, no forbidden source-study files, and valid internal checksums.
- UniProt and AlphaFold caches have file-level provenance, attribution, versions, and hashes; the stored cache report records passing file, sequence, model-version, numbering, and PAE-dimension checks.
- Release documents explicitly keep AI-assisted internal review distinct from human author responsibility and independent review.

## Gate Separation

| Gate | Current state | Completion evidence |
|---|---|---|
| Technical release/reproduction | **Incomplete** | Rebuild current archive; run scientific and archive verifiers; complete same-author clean-room reproduction; retain matching fingerprints and hashes. |
| Author signoff | **Pending Kyle Nguyen** | Kyle completes `release/AUTHOR_SIGNOFF.md`, confirms identity, affiliation, declarations, license, and line-by-line approval. No AI or reviewer can satisfy this gate. |
| Independent human review | **Pending** | An eligible human who did not build the analysis completes `release/EXTERNAL_METHODS_REVIEW.md`, and responses are recorded and returned to the reviewer. Internal AI reports do not satisfy this gate. |
| Public repository / DOI / preprint | **Not started; no external action authorized** | After the preceding gates: push the exact approved candidate, deposit the same archive, verify commit/archive hashes, publish the DOI, update metadata and manuscript links, rebuild and reverify, then submit the matching preprint. |
