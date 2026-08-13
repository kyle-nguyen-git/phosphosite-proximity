# manuscript/

Two manuscripts live here and they are not interchangeable.

## `preprint_current.md` / `.pdf` — read this one

The current manuscript. Two authors, and it makes no exclusion claim: the title reports that no
structural or sequence proximity feature was distinguishable from chance on this cohort, and the
Results lead with what the distance measurement is composed of rather than with how it performed.
Figures 1 and 2 are `figure1.png` and `figure2.png` in this directory, built by `panels/build_all.sh`
and bound by hash in `NUMBERS.md` Section 17.

It is a draft. It still carries an `[UNAUTHORIZED: ...]` marker where a literature value could not be
retrieved, and several `[AUTHOR CONFIRMATION REQUIRED]` fields in the declarations. Nothing is posted to
a preprint server yet.

## `preprint_draft_v1.md` / `.pdf` — superseded, retained for verification only

An earlier single-author draft with a different framing. It states that the primary interval "excludes
discrimination materially above 0.632". **That claim is retired.** `NUMBERS.md` Section 13 lists it
under Not allowed, and the current manuscript makes no such claim.

It is still in the repository because the verification pipeline binds to its SHA-256 and page count, and
because `manuscript/rendered/` holds a page-image manifest tied to that exact PDF. Removing it would
break checks that exist to prove the frozen analysis outputs have not moved. Treat it as a build
artifact, not as a paper.

## Everything else here

- `figure1.{png,pdf}`, `figure2.{png,pdf}` — the composed figures used by the current manuscript.
- `figure1_cohort_estimand_primary.{png,pdf}`, and `robustness/results/robustness_summary.*` — the older
  figure lineage embedded in `preprint_draft_v1`. Section 17 of `NUMBERS.md` explains which is which.
- `panels/` — the panel scripts and their composer. Counts asserted in the panels are parsed from
  `NUMBERS.md` at build time rather than typed in.
- `rendered/` — page images of `preprint_draft_v1.pdf` with a manifest bound to its hash.
- `src/` — the figure and PDF builders invoked by the pipeline.
