# AI-Assisted Internal Adversarial Review of Manuscript Claims

**Status:** AI-assisted internal adversarial review. This is **not independent peer review** and does not satisfy the manuscript's stated requirement for an independent methods review.

> **Post-review serialization addendum:** A later clean-environment run canonicalized last-bit
> continuous-model fields and refroze the Phase 0.5 JSON without changing any reported value. Use the
> current `NUMBERS.md` header, not the historical hash quoted below; see `RESPONSE_LOG.md`.

**Artifact reviewed:** `manuscript/preprint_draft_v1.md` line by line, with comparison to `NUMBERS.md`, `phase0_5/ANALYSIS_PROVENANCE.md`, the current PDF and rendered pages, figure files, release metadata, and reproducibility files.

**Disposition:** **Not ready for public posting.** The scientific headline is internally reconciled, but release blockers remain in author attestation, external review, archive reproducibility, and third-party rights. Several manuscript statements also require clarification before submission.

## Authority and Scope

`NUMBERS.md` is treated as the sole numerical authority. Before reviewing or repeating any project result, the three frozen artifacts were re-hashed locally. All matched `NUMBERS.md:5-9` exactly:

| Frozen artifact | SHA-256 from `NUMBERS.md` | Re-verification |
|---|---|---|
| `results/statistics.json` | `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401` | Match |
| `results/analysis_final.csv` | `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4` | Match |
| `phase0_5/results/phase0_5_statistics.json` | `569a3c5eab309e3ac3572d84718ce8b59ad3bd0762ed9d085aeafb6584f2e3e9` | Match |

The review used only files under this public-data Fulbright project. `phase0_5/ANALYSIS_PROVENANCE.md:9-18` documents the same project boundary. No Einstein or NYU evidence was consulted.

Literature assertions, source licenses, and preprint-platform requirements were not independently verified against external websites in this internal pass. Those items are identified below as release work rather than treated as passed.

## Blocking Findings

### B1. Author identity and declarations are explicitly unfinished

**Evidence**

- `manuscript/preprint_draft_v1.md:3-7` supplies a name and “Independent researcher” affiliation but no corresponding-author email, ORCID, or other finalized identity metadata, and explicitly prohibits public posting until identity fields are resolved.
- `manuscript/preprint_draft_v1.md:143-153` marks the funding, competing-interest, and CRediT statements as requiring author confirmation.
- `manuscript/preprint_draft_v1.md:159-161` states that the human author inspected the source data, executed and checked the analyses, reviewed the manuscript, and accepts responsibility. This is a human attestation and cannot be established by this AI review.
- The current PDF repeats “DRAFT — NOT FOR POSTING” in its page furniture and reproduces the unresolved declaration language.

**Required action**

1. Kyle must confirm the displayed author name and affiliation, provide the corresponding email, and decide whether to include an ORCID.
2. Kyle must personally confirm or correct funding, competing interests, CRediT roles, acknowledgements, and each factual statement in the AI-assistance disclosure.
3. Remove the draft prohibition and draft qualifiers only after every blocking item in this report is resolved; then rebuild the PDF and rendered-page manifest.

### B2. No citable public archive or clean-room reproduction exists

**Evidence**

- `manuscript/preprint_draft_v1.md:135-137` states that no public repository or archive DOI exists and that the package has not passed a clean-room rerun.
- `phase0_5/ANALYSIS_PROVENANCE.md:73-77` records the same limitation.
- `phase0_5/run_all.sh:10-17` invokes parent build, structure, analysis, and figure scripts. `phase0_5/results/release_manifest.csv` includes the parent analysis and figure scripts but omits `src/01_build_sites.py`, `src/02_structures.py`, the root launcher, the root requirements file, and the root license. A package assembled from the current manifest is therefore not the complete runnable project described by the launcher.
- `src/01_build_sites.py:54-88` can fetch source supplements and the current reviewed proteome, while `src/02_structures.py:30-49` can fetch the current AlphaFold model. The release manifest does not carry the full frozen parent inputs needed to guarantee reconstruction of the manuscript's stated source versions.

**Required action**

1. Define a self-contained public-release file set that includes every invoked script, environment specification, license, retrieval script, and required frozen or checksum-addressed input.
2. Build that package in a new empty environment and run it without relying on files outside the archive.
3. Compare the regenerated frozen artifacts with the hashes in `NUMBERS.md`; fail the release if they differ.
4. Deposit the reconciled package in a public repository and immutable archive, obtain a DOI, and replace the local-only availability statement with stable links.

### B3. Third-party redistribution and attribution rights remain unresolved

**Evidence**

- `manuscript/preprint_draft_v1.md:135-137` says source workbooks will not be redistributed unless reuse terms are confirmed.
- `phase0_5/README.md:29-30` states that no redistribution license is asserted for the source workbooks.
- The root `LICENSE:1-18` is an MIT software license; it does not inventory or grant rights for third-party supplementary workbooks, UniProt payloads, AlphaFold coordinate files, PAE documents, or source-study content.
- `phase0_5/results/source_manifest.json:1-68` records local input hashes, but it is not a third-party notices file and does not state the license, attribution, retrieval URL, or redistribution decision for each source class.

**Required action**

1. Create a source-rights inventory for the source-study supplements, UniProt records, AlphaFold models, PAE files, and any copied figure or text content.
2. For each source class, record the authoritative URL, citation, license or terms, required attribution, checksum, and whether the file will be redistributed or fetched by the user.
3. Exclude any source that cannot legally be redistributed and provide a deterministic retrieval-plus-checksum workflow instead.
4. Add a third-party notices file and make the scope of the MIT license explicit.

### B4. The required independent methods review has not occurred

**Evidence**

- `manuscript/preprint_draft_v1.md:7` makes independent methods review a condition of posting.
- `phase0_5/ANALYSIS_PROVENANCE.md:3-5` and `manuscript/preprint_draft_v1.md:23,95` describe reviewer-style or adversarial internal audits, not independent review.
- `manuscript/preprint_draft_v1.md:155-157` names no individual reviewer.

**Required action**

Obtain review from a human methods reader who was not involved in the analysis or manuscript construction. The review should cover the post-outcome estimand decision, clustered bootstrap, replicate aggregation, manual HOG1 coordinate resolution, annotation-evidence heterogeneity, confidence-family multiplicity, and archive reproduction. Preserve the dated review and a response record. This report can be supplied as a checklist but cannot substitute for that review.

## Major Findings

### M1. The post-outcome timing of the primary estimand decision is not stated plainly enough in the manuscript

**Evidence**

- `phase0_5/ANALYSIS_PROVENANCE.md:22-30,34-40` states explicitly that exclusion of annotation-coincident substitutions was a reviewer-audit decision made after outcome inspection.
- `manuscript/preprint_draft_v1.md:95` describes a later audit but does not say directly that the exclusion-primary decision itself was made after outcomes were known.
- `manuscript/preprint_draft_v1.md:180-183` labels the relevant table column “Timing,” but the primary and inclusive rows say only “Exact overlaps excluded” and “Named estimand sensitivity.” Neither entry gives the actual timing.

The abstract's side-by-side primary and inclusive presentation is correct and substantially mitigates this issue, but it does not replace an explicit chronology statement in Methods and the timing table.

**Actionable edit**

Add a direct sentence to `Study design and analysis chronology`: “The decision to exclude annotation-coincident substitutions from the primary estimand was made after outcome inspection; the literal-distance inclusive arm is therefore co-reported as a named sensitivity.” Rename the Table 2 column to “Status and timing,” and identify both exact-overlap rows as a post-outcome estimand decision. Preserve the current side-by-side abstract reporting required by `NUMBERS.md:15-26`.

### M2. “Prespecified” cutoff language conflicts with the post-result description

**Evidence**

- `manuscript/preprint_draft_v1.md:43` calls the cutoff summaries post-result.
- `manuscript/preprint_draft_v1.md:121` calls the same descriptive cutoffs prespecified.
- `phase0_5/ANALYSIS_PROVENANCE.md:32` states that no Phase 0.5 analysis was preregistered or confirmatory.

“Prespecified” may mean fixed before one script was run, but readers commonly interpret it as fixed before outcome inspection. The current wording leaves the timing ambiguous.

**Actionable edit**

Replace “Prespecified descriptive distance cutoffs” with wording that records the true chronology, such as “The descriptive cutoff set was fixed for the post-result sensitivity analysis after the primary outcome had been inspected.” If that chronology is not correct, amend `ANALYSIS_PROVENANCE.md` first and then use the verified wording consistently.

### M3. Several numerical method settings are outside the declared numerical authority

**Evidence**

- `NUMBERS.md:1-11` says that it is the sole numerical authority.
- `manuscript/preprint_draft_v1.md:119,127,129,133` supplies additional analysis-specific draw counts, split counts, and a base seed that are not recorded in `NUMBERS.md`.
- The canonical arm draw count and seed are present in `NUMBERS.md:24`; the additional settings are not.

This finding does not establish that those settings are wrong. It establishes that they cannot be considered reconciled under the project's stated authority rule.

**Actionable edit**

Add a “Computational contracts” section to `NUMBERS.md` containing every numerical method setting that appears in the manuscript, after verifying each against code and emitted metadata. Alternatively, remove nonessential settings from the manuscript. Do not copy values directly from prose or code into a release draft without first routing them through `NUMBERS.md`.

### M4. “Reviewed UniProt annotation” can be read as stronger evidence than the feature records support

**Evidence**

- `manuscript/preprint_draft_v1.md:11,23,75,109` repeatedly couples “reviewed UniProt” with the active-site/binding-site target annotations.
- `NUMBERS.md:28-36` records the exact-overlap annotation evidence as `ECO:0000250` for every annotation-coincident substitution.
- `manuscript/preprint_draft_v1.md:85` correctly acknowledges that binding features are heterogeneous in ligand and evidence.

The UniProt entries are reviewed; that does not make every feature experimentally established. The present phrasing can blur entry review status with feature-evidence status.

**Actionable edit**

Use “ACT_SITE and BINDING features from reviewed UniProt yeast entries” throughout. Add one Methods sentence stating that feature evidence was retained without restricting eligibility to experimentally supported features, and keep the evidence-heterogeneity limitation in Discussion. Do not characterize the exact-overlap annotations as experimentally validated unless a source-specific review establishes that claim.

### M5. The discussion invokes protein-length/annotation-count analyses that are not reported

**Evidence**

- `manuscript/preprint_draft_v1.md:85` states that “protein-length/annotation-count analyses reduced some architectural confounding.”
- No corresponding result, estimate, interval, table row, or dedicated method is provided elsewhere in the manuscript.
- Those effects are not part of the canonical claims in `NUMBERS.md`.

The phrase both asserts an analysis and interprets its effect without giving the reader anything to inspect.

**Actionable edit**

Either delete “and protein-length/annotation-count analyses” or fully report the model definition, estimate, uncertainty, timing, and limitations in Methods and Results. Any new numerical statement must first be verified and added to `NUMBERS.md`.

### M6. The reproducibility statement overstates the environment lock

**Evidence**

- `manuscript/preprint_draft_v1.md:131-133` says exact versions are pinned in the release environment.
- `phase0_5/requirements-lock.txt:1-9` pins only the listed top-level packages and does not capture the full transitive environment or interpreter patch version.
- The root `requirements.txt` and the Phase 0.5 lock disagree on the pinned `requests` version.
- `src/02_structures.py:10,30-49` deliberately resolves the current AlphaFold model from the API instead of pinning the manuscript source version. `src/01_build_sites.py:71-88` likewise fetches the current reviewed proteome when the cache is absent.

**Actionable edit**

Either soften the sentence to “direct dependencies are version-pinned” or produce a complete environment lock/container with the interpreter version, transitive packages, installation command, and platform information. Pin remote source versions or retrieve checksum-addressed snapshots, then demonstrate the clean-room rerun before claiming release reproducibility.

### M7. The HOG1 coordinate sensitivity is described generally but reported only for the inclusive arm

**Evidence**

- `manuscript/preprint_draft_v1.md:29,101` says analyses excluding the provisionally resolved HOG1 row were retained, without naming an arm.
- `manuscript/preprint_draft_v1.md:57` reports the exclusion only as an inclusive-arm sensitivity.
- `NUMBERS.md` contains an inclusive HOG1-omission row but no corresponding primary-arm value.

Because the primary arm is the headline, readers may reasonably expect the manual coordinate decision to be tested directly in that arm.

**Actionable edit**

Either change every general mention to “an inclusive-arm exclusion sensitivity” and explain why that is sufficient, or emit the corresponding primary-arm sensitivity, route it through `NUMBERS.md`, and report both arms consistently.

### M8. The replicate-outcome rule is mathematically clear but its consequence is underexplained

**Evidence**

- `manuscript/preprint_draft_v1.md:103-105` averages each replicate's count of source-significant conditions and labels a substitution positive when that average is above zero.
- Under this rule, one retained replicate with any positive count is sufficient for the substitution-level binary label; replicate agreement is not required.
- `manuscript/preprint_draft_v1.md:83` discusses phenotype compression across conditions but not replicate discordance.

**Actionable edit**

State the logical consequence of the aggregation rule explicitly. Report how replicated substitutions behaved and add a replicate-consistency sensitivity if discordance is nontrivial. Any counts or sensitivity estimates must be added to `NUMBERS.md` before appearing in the manuscript.

## Minor Findings

### m1. Outcome terminology varies unnecessarily

The manuscript alternates among “source-defined growth phenotype,” “outcome-positive,” “detected growth phenotype,” and “any-condition yeast phosphomutant growth outcome” (`manuscript/preprint_draft_v1.md:11,23,75,196-198`). Define one binary outcome name after first use and use it consistently in text, tables, and figure labels. Standardize `q-value` typography as well.

### m2. Figure text is small at manuscript-page scale

Visual inspection of `manuscript/rendered/page-02.png` and `page-03.png` found no clipping or overlap, but several panel labels, stratum labels, and footnotes require substantial zoom. Supply the figures as separate full-resolution files, increase the smallest label sizes, and verify them against the target venue's minimum type-size requirement.

### m3. Table 2 splits across pages without an explicit continuation label

`manuscript/rendered/page-08.png` and `page-09.png` repeat the column headers, but the second page does not say “Table 2 continued.” Add a continuation label or keep the table together if the target format permits.

### m4. PDF accessibility and metadata are incomplete

The current PDF is visually intact, but `pdfinfo` reports an untagged document and an empty keyword metadata field. Add document language, tagged reading order if supported by the production route, complete keywords, and final repository/DOI metadata. These are not scientific blockers but improve discoverability and accessibility.

### m5. `CITATION.cff` asserts a release before the manuscript is releasable

`phase0_5/CITATION.cff:8-9` supplies a software version and release date even though the manuscript says no public release exists. At release, replace provisional metadata with the actual version/date and add the repository URL, archive DOI, license, and ORCID if used. Until then, label the metadata as provisional or omit the release date.

### m6. Software reporting relies too heavily on an unavailable archive

`manuscript/preprint_draft_v1.md:133` names the principal libraries but cites only scikit-learn and sends exact versions to the release environment, which is not public. Once the environment is frozen, provide a concise software/version statement or supplementary environment table and cite software packages according to the target venue's policy.

## Passed Checks

### Numerical and estimand checks

- The three frozen hashes match `NUMBERS.md` exactly.
- The abstract reports the exclusion-primary arm and names the inclusive arm beside it, matching `NUMBERS.md:15-26` (`manuscript/preprint_draft_v1.md:11`).
- Results, Discussion, Methods, Tables 1–2, Figure 1, and the PDF consistently call the exclusion arm primary and the literal self-distance arm an inclusive sensitivity.
- The previously identified stale endpoint pair is absent from both the Markdown source and extracted PDF text.
- The manuscript does not make the withdrawn rounded-threshold exclusion claim. Its wording that performance materially above the primary upper bound is excluded is the wording permitted by `NUMBERS.md:26,227-244`.
- The manuscript does not claim that distance is uninformative or inferior to SIFT (`manuscript/preprint_draft_v1.md:11,69,87`).

### Confidence, PAE, and comparator checks

- Figure 2B displays the complete declared confidence family for both arms, consistent with `NUMBERS.md:122-158`; it does not select only the descending cells.
- The PAE sequence is described as nonmonotonic (`manuscript/preprint_draft_v1.md:49`).
- `pae_pair_max` is named and defined as the larger directed value in Results, Methods, and the Figure 2 legend (`manuscript/preprint_draft_v1.md:49-51,115,125,198`).
- The four PAE summaries and the full grids are presented as post-result sensitivity families rather than promoted results (`manuscript/preprint_draft_v1.md:51,125`).
- No range-restriction explanation for AUC appears in the manuscript.
- SIFT is identified as a post-result comparator, not independent validation, and its point estimate is correctly described as lying within the primary distance interval (`manuscript/preprint_draft_v1.md:69,87,129`).

### Claims, figures, and declarations

- No “first,” “novel,” “unprecedented,” or equivalent priority claim appears in the manuscript.
- The Discussion distinguishes the narrow monomeric distance feature from broader spatial regulation and multifeature tools (`manuscript/preprint_draft_v1.md:79-89`).
- The annotation-selected cohort, monomer/ligand/interface limitations, proxy outcome, post-result analysis timing, and lack of external representativeness are disclosed.
- Figure 1 shows both arm curves and labels the exact-overlap decision. Figure 2 shows all declared strata and names the PAE definition. Visual inspection found no clipping, overlap, black boxes, or missing panels.
- The PDF hash and rendered-page binding match the artifact state recorded in `NUMBERS.md:248-254` and `manuscript/rendered/render_manifest.json`.
- Ethics, funding, competing-interests, author-contribution, acknowledgement, and AI-assistance sections are present. Their existence passes; the human confirmations identified in B1 do not.
- The local release verifier reports all of its encoded checks as passing. That verifier covers numerical and artifact consistency, but it does not resolve the semantic, rights, attestation, or independent-review findings in this report.

## Minimum Release Sequence

1. Resolve B1 with explicit human attestations and final author metadata.
2. Obtain and respond to the independent human methods review in B4.
3. Resolve M1–M8 in the manuscript and, where required, route newly verified method settings or results through `NUMBERS.md`.
4. Resolve source rights and third-party notices in B3.
5. Assemble the complete archive, perform the clean-room rerun, and create the public repository and DOI in B2.
6. Rebuild the manuscript PDF and rendered pages, rerun the fail-closed verifier, and conduct a final visual and line-by-line check before removing “DRAFT — NOT FOR POSTING.”
