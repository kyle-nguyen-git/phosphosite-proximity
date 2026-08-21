# Phosphosite-Proximity Manuscript Version Map

Updated: 2026-08-18 06:40 CDT

This file is the routing authority for reader-facing manuscript versions. It separates the current
manuscript from superseded author drafts and from verifier-bound legacy artifacts that must remain at
their historical paths.

## Submission status

Updated: 2026-08-18 10:05 CDT

The package passes **161 of 161** checks. AI use is disclosed in Methods §4.9 and nowhere else: the paper
makes no claim that its methods were reviewed, and S2 Appendix, which logged the review rounds, has been
removed from the package at the authors' direction. The AI-use disclosure itself is unchanged and is
required by a verifier check.

Author actions remain: the deposit identifier is undecided, and `AUTHOR_SIGNOFF.md` is unexecuted.

## Current manuscript

Edit only the Markdown source. The PDF and DOCX are build products and should be rebuilt together.

| Role | File | Snapshot | SHA-256 | Status |
|---|---|---|---|---|
| Source of record | `phosphosite_proximity_paper.md` | 2026-08-18 08:10 CDT; 16,905 whitespace-delimited words | `d1ed96bb61603acd7636f62787415ca4ee01ed3c2403fbe8b3c18d73bdf1301c` | **Current; edit this file** |
| Reader PDF | `phosphosite_proximity_paper.pdf` | 2026-08-18 06:38 CDT; 28 US-Letter pages | `83e5e56d12113e853e28c5574b5a81103644e05b272b38ce58aeeb970e7c9d9b` | **Current reading build; UT corresponding-author email present** |
| Editable Word build | `phosphosite_proximity_paper.docx` | 2026-08-18 00:25:36 CDT; rendered to 26 US-Letter pages | `d370dd662c92effc68ee06a285cc00f19abb5ebe274ed21b4b93831431f633a2` | **Current reading build; do not edit directly** |
| Journal-submission Word build | `phosphosite_proximity_paper_SUBMISSION.docx` | 2026-08-18 00:25:43 CDT; rendered to 37 US-Letter pages | `c80f70eac41ae77ad33fcf60029d36d357fa5b8d765b9a40e40a614d3735e9cb` | **Current formatted build; UT corresponding-author email present** |
| Submission Figure 1 | `manuscript_build/submission_figures/Fig1.tif` | 2,162 × 875 px; RGB; 300 dpi | `8bbe8c9366ffcffd577f4cc14da6c2942303cf5838f9bda1d928d96476602a9e` | **Technical specification passes; visual revisions recommended** |
| Submission Figure 2 | `manuscript_build/submission_figures/Fig2.tif` | 2,162 × 827 px; RGB; 300 dpi | `3105cd3f05c7a1674e2bc4376667cc743de1a4bc528c351b9b768a47e2552cff` | **Current two-panel TIFF; technical specification passes** |
| Submission Figure 3 | `manuscript_build/submission_figures/Fig3.tif` | 2,162 × 922 px; RGB; 300 dpi | `8ec1520e9e8a767c528f5d955c6d4cbc0ed67b03a643761465fe4fefc5058a71` | **Current; add left white border before submission** |
| Supporting Figure 1 | `manuscript_build/submission_figures/S1_Fig.tif` | 2,162 × 827 px; RGB; 300 dpi | `e081636b5c64e29f9f0b4d2d77d147dd2f02f54a8bcffa6c289a245e4c9702aa` | **Current; technical specification passes** |
| Supporting Figure 2 | `manuscript_build/submission_figures/S2_Fig.tif` | 2,162 × 969 px; RGB; 300 dpi | `be99c45c4d08691e60c8192c2bf0652c2020b56ed933e77551ff91183a127fba` | **Current; technical specification passes** |

The current title is *Distance to the nearest annotated active or binding residue: what it measures,
and how it ranks sites in yeast and human phosphosite-mutant screens*. The corresponding-author email
was changed to `ktn965@my.utexas.edu` on 2026-08-18 and all three reader/submission builds were saved.
The current package passes 139 of 140 submission checks. The single failure is deliberate: the third author's affiliation is the placeholder `AFFILIATION-TO-CONFIRM`, and the verifier blocks submission until it is filled in. A later build invalidates the hashes above and
requires this table to be updated. `preprint_final_gap_review_2026-08-14.md` remains a historical review
of the 02:40 package, not an independent review of the hashes above.

## Superseded reader-facing drafts

All ordinary older manuscript versions are under `superseded/`. They are retained for provenance and
must not be cited, edited, sent for review, or used as a build source.

| File | Date | Historical role |
|---|---|---|
| `superseded/phase0_calibration_preprint_editable.docx` | 2026-07-30 | First editable, single-author Word build |
| `superseded/phase0_calibration_preprint_humanized_v2.docx` | 2026-07-30 | Early human-readable Word revision |
| `superseded/phase0_calibration_preprint_black_text_v3.docx` | 2026-07-31 | Single-author title block; partial style correction |
| `superseded/phase0_calibration_preprint_two_author_all_black_v4.docx` | 2026-08-02 | Two authors and UT affiliation; predates round-2 analyses |
| `superseded/phase0_calibration_preprint_two_author_all_black_v5.docx` | 2026-08-03 | Rebuilt after Figure 1B and Figure 2A caption changes |
| `superseded/phase0_calibration_preprint_humanized_v2.md` | 2026-08-03 | Source of record until 2026-08-12; contains retired claims |

The detailed reason each file was replaced is in `superseded/README.md`.

## Frozen legacy artifacts that remain in place

These are older manuscripts, but they cannot be moved into `superseded/` without breaking historical
paths, hashes, manifests, or release-verifier expectations.

| File set | SHA-256 | Why it remains |
|---|---|---|
| `phase0_calibration/manuscript/preprint_draft_v1.md` | `061e45006f6cca141e47ff40a05659dbd668d5f0eb6c59b71452ef2aa9d0dafb` | Frozen 11-page, yeast-only verifier input; single author; not current |
| `phase0_calibration/manuscript/preprint_draft_v1.pdf` | `ba484a32af7322843d0378fd2078b0a0689849d9edf8ec29459e25bf3e729574` | Frozen A4 review PDF; verifier-bound; not current |
| `phase0_calibration/release/build/phase0-calibration-v0.5.0-rc1/manuscript/preprint_draft_v1.{md,pdf}` | Same hashes as the two files above | Byte-identical package copies required to preserve the historical release candidate |

The old PDF is 11 A4 pages, has the title *Exploratory calibration of AlphaFold-derived distance*, and
names Kyle Nguyen alone. Those properties identify it as legacy even when it is opened outside the
vault. No file named `preprint_current` exists in the local release-candidate package despite older
review instructions referring to one.

## Snapshot-specific reviews

The following documents are evidence about older snapshots, not reviews of the current 2026-08-18
build:

- `peer_review_round1/` and `revision_round1/` reviewed the August 3 `humanized_v2` lineage or the
  frozen `preprint_draft_v1` lineage.
- `preprint_review_2026-08-13.md` and `preprint_reference_audit_2026-08-13.md` are bound to the 17:52 CDT
  snapshot.
- `preprint_review_change_verification_2026-08-13.md` is bound to the 18:55 CDT snapshot.
- `preprint_review_revised_2026-08-13.md` is the review of the superseded 22:12 CDT build and is bound to
  PDF SHA-256 `afe0736469d0fcd2162168e6e3fc4645fb744e9734db3234eabc5bad1a465121`.
- `preprint_review_latest_2026-08-14.md` is the complete independent review of the current 23:49 CDT
  build. It is bound to Markdown SHA-256 `5381719242d08331385f510bcad727ac8b3c81234a9e1f09441893820aeea73c`
  and PDF SHA-256 `26bf164807dc14fa11b45c4b4fdd91f170214c811744104ef55e7c80c42d8a0c`.
- `preprint_journal_format_review_2026-08-14.md` reviews the superseded 01:12/01:25 package and its two
  submission TIFFs. Its historical hashes are recorded inside that review.
- `preprint_final_gap_review_2026-08-14.md` reviews the historical 02:40 package, all five TIFFs and the
  separate supporting files. Its bound hashes are recorded inside the review.

Every human quantity is now registered in `NUMBERS.md` §26, which supersedes §§22–25. The human cohort
was rebuilt from the Kennedy supplement and UniProt by `kennedy_replication/build_candidate_table.py`,
which reproduces 1,587 of the 1,595 rows of the earlier build and found one site assigned to the wrong
protein (TKT S308 had been mapped to an entry for DDR2). The corrected cohort is **1,471 sites in 788
proteins**; fitness **0.557829 [0.473557, 0.636888]** on 72 affected, reporter **0.483301
[0.418057, 0.549886]** on 82. Both declared estimates moved by less than 0.003 and both contain 0.5.

The reporter's equal-protein within-protein interval ended at 0.489 on the corrected cohort. Three
independent adversarial checks refuted it and it is retired in §26.4: the whole effect is PIDD1, one
protein contributing one pair, dropped by the ambiguous-symbol rule.

Current build, 2026-08-18 00:28 CDT, 107 of 107 submission checks passing:

| Artifact | SHA-256 |
|---|---|
| `phosphosite_proximity_paper.md` | `5f2a08c09a3142a7fee82812dc15a3725d70ce95f70f730fe5306c37152bf46f` |
| `phosphosite_proximity_paper.pdf` | `0c86035d594fe977946700a99e77ce46e35a30a4a7fe0d5a37e409dde20358c8` |
| `phosphosite_proximity_paper.docx` | `06dd7c1eca4db9b3c6806d3454d657ede7057e9894e5f71ad8379fb6648ab31b` |
| `phosphosite_proximity_paper_SUBMISSION.docx` | `380fe10a51abdaf5c8acc67403507fee285b9f523931b915d9a85a3d7a937881` |
| `manuscript_build/submission_manifest.json` | `12a0155ed7034101885e2c74d8cf069261379f605b30656f8d87f003ff086fd2` |

All three earlier reviews on this page are bound to superseded hashes and describe defects that have
since been repaired. `preprint_final_gap_review_2026-08-14.md` reviewed the 02:40 package; its twelve
claims were independently verified before action (nine confirmed, three partial) and all are addressed.

## Handling rules

1. Send `phosphosite_proximity_paper.pdf` for reading and review.
2. Edit `phosphosite_proximity_paper.md` only, then rebuild PDF and DOCX together.
3. Do not use a filename containing `v1`, `v2`, `v3`, `v4`, `v5`, `draft`, `humanized`, or
   `all_black` as the current manuscript.
4. Do not move, rename, or delete the verifier-bound `phase0_calibration/manuscript/preprint_draft_v1`
   files or their release-package copies.
5. Bind every new review to a modification time and SHA-256 so later revisions cannot be mistaken for
   the file that was actually reviewed.
