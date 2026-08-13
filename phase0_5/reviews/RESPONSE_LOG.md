# Internal Adversarial Review Response Log

## Status

The analysis and release candidate have been revised in response to the internal adversarial reviews.
Technical dispositions below do not sign Kyle Nguyen's declarations, create an independent human review,
or authorize public posting. Those gates remain in `release/AUTHOR_SIGNOFF.md` and
`release/EXTERNAL_METHODS_REVIEW.md`.

## Original Five Blocking Items

| Finding | Disposition | Evidence |
|---|---|---|
| RNG-sensitive exclusion claim | Resolved | One canonical high-draw interval is frozen in `NUMBERS.md`, loaded before claims are checked, and reconciled across Markdown, PDF, and analysis outputs by `phase0_5/src/04_verify_release.py`. The manuscript treats the endpoint as a confidence bound, not a utility margin. |
| Unresolved exact-overlap estimand | Resolved with explicit post-outcome disclosure | `exclude_annotation_coincident` is primary; `include_annotation_coincident` is the named literal-distance sensitivity. Both arms are emitted in one run. The decision and its timing are recorded in `phase0_5/ANALYSIS_PROVENANCE.md`, the abstract, Methods, and Table 2. |
| Selected confidence strata | Resolved | `phase0_5/results/confidence_strata.csv` emits the complete declared family for both arms, and Figure 2 plots every row. |
| Undisclosed and selected PAE definition | Resolved as sensitivity | `pae_pair_max` is named and defined; all available PAE summaries and the complete filter grids are retained as post-result sensitivity families. |
| Incorrect range-restriction caveat | Resolved | The caveat is absent from the manuscript and results. Provenance records why it is inapplicable to rank-based AUC. |

## Statistical Methods Review

| Item | Disposition | Evidence |
|---|---|---|
| Within-protein heading stronger than the intervals | Resolved | The heading now describes estimates as centered near chance and imprecise; the paragraph preserves the full uncertainty. |
| Cutoff chronology called prespecified | Resolved | `NUMBERS.md`, provenance, Methods, Results, and Table 2 identify the cutoff family as post-result and descriptive. |
| SIFT interval containment used as comparison | Resolved | Comparative wording rests on the paired common-support analysis; point-estimate containment is labeled descriptive. |
| Missing logistic diagnostics | Resolved | `phase0_5/src/04_build_release_artifacts.py` emits `logistic_fit_diagnostics.csv`, which is included in the supplementary workbook. |
| Upper bound could be mistaken for materiality margin | Resolved in wording | The abstract and Discussion state that the endpoint is not a predeclared equivalence, noninferiority, or utility threshold. |

## Biological and Structural Review

| Item | Disposition | Evidence |
|---|---|---|
| Heterogeneous UniProt feature evidence | Resolved for the narrow estimand | The predictor is consistently named as an expanded UniProt `ACT_SITE`/`BINDING` coordinate. `feature_evidence_audit.csv` separates geometry and evidence classes, and the manuscript states that reviewed-entry status does not imply direct experimental support for each feature. Broader feature sensitivities are identified as conditional on the core-eligible cohort. |
| Any-heavy-atom metric could imply phosphate geometry | Resolved in scope | The manuscript and legends specify minimum residue–residue heavy-atom distance and state that a short value may arise from backbone packing or local sequence adjacency rather than phosphate-mediated contact. |
| Direction, condition, and replicate pooling | Resolved in definition and audit | The endpoint is named direction-agnostic and any-condition. The logical any-positive-replicate consequence is explicit, and strain-level behavior is emitted in `replicate_aggregation_audit.csv`. No phosphorylation-dependent-function claim is made. |
| AlphaFold retrieval and mapping did not fail closed | Resolved technically | Exact v6 cache URLs and hashes are manifest-bound. Parent and Phase 0.5 builders verify monomer/version fields, complete UniProt/metadata/mmCIF sequence identity, residue numbering, bounds, and PAE dimensions before measurement. `tools/verify_third_party_cache.py` repeats these checks. |
| pLDDT called a disorder proxy | Resolved | Code and manuscript call pLDDT model-local confidence; source disorder annotations remain separate. |
| PAE conditional on coordinate-selected target | Resolved in Methods | Confidence belongs to the coordinate-selected nearest target; filtering does not reselect a different biological target. |
| RSA lacks native interfaces and ligands | Resolved in scope | RSA is described as an isolated-monomer covariate and inherits the monomer-state limitation. |

## Manuscript and Release Review

| Item | Disposition | Evidence |
|---|---|---|
| Author identity, declarations, and line-by-line approval | Pending human action | `release/AUTHOR_SIGNOFF.md` records every required field and attestation. The PDF remains marked `DRAFT — NOT FOR POSTING`. |
| No standalone clean-room package | Resolved technically when the recorded clean-room report passes | `reproduce.sh`, the complete dependency lock, source fetcher, cache verifier, package builder, and technical verifier are included. `release/clean_room_report.json` records a fresh-environment run and frozen-hash comparison. |
| Third-party rights and attribution not inventoried | Resolved for the candidate | Source-study workbooks are omitted and retrieved with inner-file checksums. `THIRD_PARTY_NOTICES.md`, `LICENSES.md`, and the file-level cache manifest record source class, terms, attribution, hash, and redistribution decision. |
| Independent methods review absent | Pending human action | `release/EXTERNAL_METHODS_REVIEW.md` is ready for an eligible reviewer. Internal AI reports do not satisfy it. |
| Exact-overlap chronology too indirect | Resolved | Direct post-outcome language appears in study chronology and Table 2. |
| Method settings outside `NUMBERS.md` | Resolved | `NUMBERS.md` contains the computational contracts used in the manuscript. |
| Reviewed entry versus feature evidence blurred | Resolved | Terminology and feature-evidence disclosure were revised throughout. |
| Unsupported architectural-confounding statement | Resolved | The claim was removed; adjusted models remain available without being promoted as proof of resolved confounding. |
| Environment/source versions not locked | Resolved technically | Direct and transitive dependencies are pinned; structural caches are checksum-addressed; the clean-room report records the interpreter, installed environment, and renderer. |
| HOG1 sensitivity arm ambiguous | Resolved | The manuscript identifies it specifically as an inclusive-arm exclusion sensitivity. |
| Replicate consequence underexplained | Resolved | Methods and the replicate audit disclose the exact aggregation consequence and retained replicate patterns. |
| Small figure labels | Resolved | Minimum label sizes were increased and separate full-resolution PDF/PNG figures remain in the release. |
| Table split/continuation | Resolved | Each table is kept on its own page in the rebuilt review PDF. |
| PDF metadata/accessibility | Partially resolved | Title, author, subject, keywords, creator, and document language are embedded. The ReportLab review PDF remains untagged; semantic tagging is deferred to a venue-compatible production route and is not a scientific gate. |
| Premature citation metadata | Resolved | Citation files are marked release-candidate versions with no DOI or asserted public release date. |

## Gates That Remain Outside This Response Log

- Kyle Nguyen must complete the author sign-off, public identity, affiliation, declarations, license
  choice, and line-by-line review.
- An eligible human who did not build the analysis must complete the independent methods review and see
  the response.
- A public repository, immutable archive DOI, and preprint submission may be created only from the exact
  candidate approved at those two gates. No external account has been modified during this work.

## Reproducibility and Release Review

| Item | Disposition | Evidence |
|---|---|---|
| Archive was stale relative to the live candidate | Resolved by final sequence | The scientific verifier is run first, then `tools/build_release.py` rebuilds the archive from the quiescent tree. Archive metadata carries the source/input fingerprint, and the package manifest binds every copied file. |
| Clean environment changed the frozen Phase 0.5 JSON hash | Resolved without changing reported values | The diff was confined to last-bit BLAS variation in adjusted continuous-outcome OLS sensitivities. The pipeline now applies the 12-decimal serialization contract in `NUMBERS.md`; the Phase 0.5 hash was refrozen only after cohorts, estimates, intervals, and reported values were confirmed unchanged. |
| Supplement workbook changed across identical builds | Resolved | The only differing ZIP member was the workbook core-properties modification timestamp. The deterministic normalizer now fixes that XML field as well as ZIP entry timestamps; repeated builds are byte-identical. |
| Clean-room report absent | Resolved when final recorded run passes | `tools/run_clean_room.py` executes the exact archive from an empty temporary directory and a second fresh virtual environment, then records frozen hashes, deterministic artifact checks, package set, renderer, commands, and exact tested archive hash in the companion report. |
| Technical verdict referenced an older snapshot | Resolved by final sequence | `tools/verify_release_package.py --archive ...` runs after clean-room completion and requires the exact archive named by the passing clean-room report. |
| Archive freshness not enforced | Resolved | The archive verifier compares `PACKAGE_METADATA.json`'s source/input fingerprint with the live root and reconciles every row in `PACKAGE_MANIFEST.csv` against the current candidate. |
| Interpreter, Poppler, platform, and network contract incomplete | Resolved in documented support boundary | `reproduce.sh` requires the interpreter patch in `NUMBERS.md` and `pdftoppm`; README and `NUMBERS.md` record the tested host and renderer, network requirement, and the fact that distribution hashes are not included. The clean-room report records the resolved environment. A cross-platform container remains optional future hardening, not a claim made by this release. |
| Mixed-license CFF metadata | Resolved provisionally | The release-candidate CFF files no longer claim that MIT covers the mixed package. `LICENSES.md` retains the scoped software license and requires the human author's research-artifact license choice before deposition. |
| Release commands absent from README | Resolved | README now gives package-build, clean-room, and exact-archive verification commands and names their reports. |
| Duplicate CFF could drift | Resolved | The technical verifier compares canonical shared fields and requires provisional metadata without a public release date. |
| Untagged PDF | Deferred transparently | Metadata and language are present; semantic tagging remains a venue-production accessibility task and is not represented as complete. |
