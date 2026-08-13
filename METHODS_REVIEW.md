# Independent Human Methods Review Packet

## Status

No independent human review is recorded in this file. The AI-assisted reports under
`phase0_5/reviews/` are internal adversarial checks and do not satisfy this gate. The simulated
five-seat panel in `../../peer_review_round1/` does not satisfy it either — five personas on one
model family are not five referees.

**Reviewer identified 2026-08-12: David Chang**, a colleague of Kyle Nguyen. He is eligible on the
written criteria below: he did not construct this analysis and did not write this manuscript. He is a
different person from Dr. Roger Chang (Albert Einstein College of Medicine), who is a confirmed
Fulbright recommender and Kyle's SURP supervisor — do not merge the two records. Nothing has been
sent yet. The packet is hash-bound, so it goes out only after the manuscript revision and the archive
rebuild, or the review will name a package that the rebuild invalidates.

## Reviewer eligibility

The reviewer should be a human who did not construct the analysis or manuscript and can assess clustered
inference and/or structural bioinformatics. Either competence alone is sufficient; the required questions
below are split so a statistician and a structural biologist each have a scope they can answer.

The reviewer does **not** have to be a stranger, a senior scientist, anonymous, or unaffiliated with the
authors. A mentor, former supervisor, recommender, or personal acquaintance is eligible, provided they
did not build this analysis or write this manuscript. Record any relationship with each author and any
conflict of interest; the relationship is disclosed, not disqualifying.

Both listed authors are ineligible, and so is anyone whose contribution to this work has already been
credited as authorship. A reviewer should be acknowledged unless their contribution reaches the
applicable authorship standard — so keep the engagement to critique and sign-off. A reviewer who begins
redesigning the analysis or drafting manuscript text has become an author, and the gate reopens.

## Minimum review set

Read:

- `NUMBERS.md` and verify its three frozen hashes before using any project result;
- `manuscript/preprint_current.md` and `.pdf` — the manuscript that would be posted. Ignore
  `manuscript/preprint_draft_v1.*`: it is a superseded single-author draft kept only because the
  verifier binds to its hash, and it states a claim since retired. `manuscript/README.md` says which is
  which;
- `robustness/ANALYSIS_PROVENANCE.md`;
- `results/cohort_disposition.csv`;
- `src/01_build_sites.py`, `src/03_analysis.py`, and `robustness/src/02_robustness_analysis.py`;
- `robustness/results/verification_report.json`;
- `SOURCE_RETRIEVAL.md`, `THIRD_PARTY_NOTICES.md`, and the clean-room report.

## Required questions

1. Does the post-outcome decision to exclude annotation-coincident substitutions remain plainly disclosed,
   with the literal-distance inclusive arm co-reported?
2. Does the cohort ledger implement Supplementary Data 1 constructs, Data 3 outcomes, and exact Data 8
   exclusions without using Data 6 to select the cohort?
3. Is the direction-agnostic any-condition endpoint and its replicate rule biologically and statistically
   described without implying phosphorylation-dependent function?
4. Does the protein-cluster bootstrap match the site-weighted estimand, and are its limitations clear?
5. Are cutoff, confidence, PAE, feature, SIFT, within-protein, and prediction analyses labeled post-result
   where appropriate?
6. Are UniProt entry review status, feature-evidence heterogeneity, interval expansion, and the
   residue–residue any-heavy-atom definition distinguished from experimental catalytic geometry?
7. Do AlphaFold v6 hashes, URLs, sequences, residue numbering, monomer status, and PAE dimensions fail
   closed in the release candidate?
8. Does the manuscript avoid “distance is uninformative,” SIFT-inferiority, universal-threshold, causal,
   or priority claims that the analysis cannot support?
9. Can the archive be reproduced in a fresh environment without any file outside the release plus the
   authoritative source retrieval?

## Reviewer record

- Reviewer name and credentials: `[required]`
- Affiliation: `[required]`
- Contact email: `[required for private response record; public display optional]`
- Relationship to each author (Kyle Nguyen; Arkady Marchenko): `[required]`
- Conflicts of interest: `[required]`
- Review date: `[required]`
- Repository commit reviewed (git SHA): `[required]`
- Manuscript file reviewed, with its SHA-256: `[required]`
- Recommendation: `[accept / revise / do not post]`

Review findings: `[attach or enter]`

## Author response

For every blocking or major finding, list the finding, disposition, changed file, and verification step.
Do not mark this gate complete until the reviewer has seen the response or the response explains why a
requested change was not made.

Reviewer confirmation/signature: ______________________________

Date (YYYY-MM-DD): _____________________________________________
