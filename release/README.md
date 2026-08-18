# Release packaging

## `build/` and `dist/` are a frozen snapshot, and they predate the current manuscript

`phosphosite-proximity-v0.5.0-rc1` was packaged on **2026-08-13 at 03:55**. The manuscript was revised
substantially later the same day. The packaged tree therefore does **not** match the working tree, and
the mismatch is not a defect in the package — a release candidate is a snapshot by definition — but it
is a trap, because of one filename.

**`build/phosphosite-proximity-v0.5.0-rc1/manuscript/paper_current.md` is not the current
manuscript.** It is the single-cohort version, under the retired title *No structural or sequence
proximity feature is distinguishable from chance in a yeast phosphosite-mutant screen*. Do not read it,
cite it, or send it to a reviewer. The current manuscript is `manuscript/paper_current.{md,pdf}` at
the repository root.

What the packaged copy is missing, all added after it was built:

- Results §2.7 and §2.7.1–2, the human replication on the Kennedy 2024 base-editor screen: 1,475 sites
  in 793 proteins, and the endpoint defect in that screen's released per-site value.
- Methods §4.7, and Kennedy et al. as reference 21.
- The retirement of the "there is no positive control for the outcome" claim from Discussion §3.2.
- The QC-inclusive arm and the measured bootstrap coverage, in §2.1 and §3.2.
- The current title.

Its `NUMBERS.md` is likewise the pre-Section-20 copy, and still licenses the 0.632 exclusion claim that
was retired by author decision on 2026-08-12.

## What the package is still good for

`clean_room_report.json`, `package_build_report.json` and `release_readiness_report.json` describe that
snapshot and remain valid statements about it. The archive is the exact-reproduction target the older
verifier binds to. Nothing here should be deleted to tidy up: the verifier's hash checks reference it.

## Before any deposition

Repackage from the current tree, and do not deposit `v0.5.0-rc1` as though it were the paper. The
Zenodo template at `ZENODO_METADATA_TEMPLATE.json` still carries the retired title and the single-source
citation, and must be updated with the current title and the Kennedy et al. 2024 reference first.
