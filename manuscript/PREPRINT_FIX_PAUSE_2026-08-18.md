# Preprint Repair Pause Record

Recorded: 2026-08-18 01:54 CDT

Status: **RESOLVED 2026-08-18 06:40 CDT.** Items 1–6 of "Do next" are complete and item 7 is complete
except for the independent review of the final hashes. The manuscript, `NUMBERS.md` §27, every table,
Figure 3 and all build products now describe the 1,470-site/787-protein cohort. The package passes 125
of 125 submission checks, which now bind the offline human rebuild manifest and its hashes. The safety
hold in `MANUSCRIPT_VERSION_MAP.md` is lifted.

The original pause record follows unchanged.

## Completed before the pause

1. Audited every quoted criticism against the current manuscript.
   - Already closed in the current source: Figure 2 points to
     `manuscript_build/submission_figures/Fig2.png`; S2 Table contains twelve 10 Å summaries and three
     72-cell grids (216 grid cells); the human label shuffle is described as diagnostic and has no
     claimed p-value; the 255-estimate family is explicitly yeast-only; Correa Marrero is already
     described as analogous rather than identical; both analysed Kennedy screens are identified as
     Jurkat/ABE8e; the cross-cohort precision comparison is explicitly declined.
   - Still live when checked: Table 2's four-test union was computed from released per-site columns,
     the human reproducibility paragraph was stale, the package verifier did not bind the human cache,
     and the bibliography lacked the MAGeCK methods paper and exact official UniProt/AFDB documents.

2. Rebuilt the four-direction union from the source MAGeCK `neg|p-value` and `pos|p-value` columns on
   the then-current 1,471-site cohort. It changed from 86 sites, AUC 0.541860 [0.465780, 0.615698], to
   88 sites, AUC 0.539013 [0.463862, 0.612724]. This output is now **stale again** because the canonical
   human cohort changed to 1,470 sites during the cache repair. File:
   `kennedy_replication/endpoint_options_source_corrected.json`, SHA-256
   `7166523bc58449d99f58264eb074b32c57015d79b8de7955938c49cbe9273bce`.

3. Made the candidate-table build fail closed offline.
   - Cascade reproduced: 7,425 source rows → 6,968 parsable S/T/Y sites → 6,907 unique reviewed-human
     mappings → 6,113 canonical-sequence matches → 1,590 candidate sites in 812 proteins.
   - Against the superseded 1,595-row table: 1,587 rows shared, 8 removed ambiguous mappings, 3 newly
     resolved rows.
   - Missing cached UniProt JSON now stops the build instead of silently dropping an accession.

4. Added model provenance and sequence assertions. This exposed a new bug: the original AlphaFold
   downloader took the first API result, which was an isoform for 11 accessions.
   - Replaced active cache entries for Q96EY9, Q14669 and P24928 with exact canonical AFDB v6 models.
   - Removed active entries for O43149, Q8TD26, O94854, Q63HN8, Q5T4S7, O75962, Q9Y4D8 and Q9P2D1
     because the official API returned no exact canonical entry.
   - All 11 displaced files are retained under
     `kennedy_replication/cache/af_superseded_wrong_isoform/`.
   - The active manifest now covers 812 candidate accessions and 789 exact-canonical v6 models:
     `kennedy_replication/cache/af_v6_manifest.csv`, SHA-256
     `e9f39d6705fa13f91b40d8e4edd5c45fc23425cb17cc32f0a35fd6d34ac82cc5`.

5. Ran two fresh, network-disabled source-to-cohort rebuilds with canonical-model, model-sequence and
   residue-number assertions. Both produced **1,470 sites in 787 proteins**. The prior analysis had
   1,475 rows, four without a distance; the corrected build has 1,470 distance-bearing rows. The only
   previously analysed distance row removed was CHD6 S27 (Q8TD26). Four TRIO rows (O75962) already had
   no distance.
   - Current corrected analysis: `kennedy_replication/kennedy_analysis_corrected.csv`, SHA-256
     `90d4be92fa92c738ec65f84a77d4c766199000e548cc87efbcd79b3d4417557b`.
   - Prior table retained as `kennedy_replication/kennedy_analysis_pre_isoform_fix.csv`, SHA-256
     `660bdfcc41bae4ddd6e33a7686be090c7fda986e8e5cd2917119e560074e0b03`.
   - Offline rebuild manifest: `kennedy_replication/human_rebuild_manifest.json`, SHA-256
     `7b74f039397f0a9269e703ebea3e3ec510f43041499ae8f4e8466c9ce1045248`; status PASS and every
     candidate/analysis row and column matched the canonical files.

6. Verified the intended new references against primary or official sources, but did not edit the
   manuscript bibliography:
   - Li et al. 2014, MAGeCK, Genome Biology 15:554, DOI 10.1186/s13059-014-0554-4.
   - Official UniProt release 2026_02 note, dated 10 June 2026.
   - Official PDBe AlphaFold DB v6 release note, dated 21 October 2025.
   - Official AlphaFold DB FAQ for PAE JSON orientation and matrix format.

## Interrupted work

`rebuild_endpoints.py` was stopped at the user's request. It had completed the fitness primary on the
new 1,470-site cohort: 72 positives, AUC 0.557632 [0.472659, 0.638588], equal-protein within-protein AUC
0.510684 [0.373932, 0.645299]. The script writes its JSON only at completion, so
`rebuilt_endpoints_corrected.json` remains the **stale 2026-08-14 file** (SHA-256
`58cf24cffb03f60f396437704ca0658dff83c2736a0fd38ceaf86849e7404c8f`) and must not be treated as the
new result.

## Do next

1. Complete `rebuild_endpoints.py` on `kennedy_analysis_corrected.csv`; then rerun
   `endpoint_options.py`. Do not reuse the interrupted fitness-only console output as numerical
   authority.
2. Register the complete 1,470-site/787-protein result family in a new `NUMBERS.md` section that
   supersedes §26. Until then, all human numbers are suspended.
3. Regenerate every human-dependent table and figure, especially Table 2, Table 3, Table 4 and Fig 3.
4. Edit the manuscript only after the new numerical section exists: cohort cascade, endpoint mismatch
   counts, screen overlap, pooled and within-protein pair counts, primary/comparator estimates,
   reproducibility text and the four-test union.
5. Add the MAGeCK paper and the exact official UniProt release, AFDB v6 release and PAE-format
   documentation; attach each citation only to the claim it supports.
6. Extend `verify_submission_package.py` to require the human rebuild manifest, its hashes and the new
   cohort/result invariants. The current 107/107 result predates this correction and is not a valid
   submission clearance.
7. Rebuild the reader PDF, editable DOCX and submission DOCX; render and inspect every page; update the
   manifest and version map; then obtain an independent review of the exact final hashes.



## Resolution — 2026-08-18 06:40 CDT

1. **Done.** `rebuild_endpoints.py` completed on `kennedy_analysis_corrected.csv` → `rebuilt_endpoints_1470.json`.
   Fitness 72 positives, 0.557632 [0.472659, 0.638588] — reproducing the interrupted console output exactly.
   Reporter 82 positives, 0.483113 [0.418242, 0.550433]. `endpoint_options.py` rerun → `endpoint_options_1470.json`;
   the four-direction union is 88 sites, 0.538819 [0.462346, 0.614406]. Every arm contains 0.5.
2. **Done.** Registered as `NUMBERS.md` §27, superseding §26 and with it §§22–25, with the bound hashes of
   the cohort, the AFDB v6 manifest and the offline rebuild manifest.
3. **Done.** Figure 3 repointed at the new endpoint file and all five TIFFs rebuilt; Tables 2, 3 and 4 updated.
4. **Done.** Cohort cascade, mismatch counts (46 and 100 of 1,470), screen overlap (66/76/6), pair counts
   (102 of 100,656; 184 of 113,816), primaries, comparators, reproducibility text and the union arm.
5. **Done.** MAGeCK, the UniProt 2026_02 release note, the PDBe AFDB v6 release note and the AlphaFold PAE
   FAQ added, each attached only to the claim it supports. The bibliography was found not to be in
   first-citation order — `[1,4,3,2,5,…]`, contrary to PLOS's numbering rule — and was renumbered into
   citation order across 26 references, verified for order, orphans, danglers and per-entry identity.
6. **Done.** `verify_submission_package.py` now binds the three human-rebuild hashes, requires the manifest
   to report PASS, requires the current result files, and asserts the cohort is 1,470 × 787. All five new
   checks were negative-controlled and all five caught their mutation. 107 → 125 checks.
7. **Build done, review outstanding.** Reader PDF (28 pages), editable DOCX and submission DOCX rebuilt and
   inspected page by page: no empty shaded boxes, no horizontal overflow, and the apparent vertical
   overflow is 4–5 pt of normal glyph extent past the baseline margin. Manifest and version map updated.
   **The independent review of the final hashes has not been obtained.**

### Two defects found and fixed during this work

- The first renumbering script rebuilt the References section and truncated everything after it, deleting
  the Supporting information section. Caught by the package verifier, restored from a backup taken before
  the edit, and redone preserving the tail. The lesson is recorded because the failure was silent in the
  Markdown and only a downstream structural check surfaced it.
- The build-product freshness check fired correctly after the negative-control run rewrote the Markdown,
  demonstrating it is not a no-op.
