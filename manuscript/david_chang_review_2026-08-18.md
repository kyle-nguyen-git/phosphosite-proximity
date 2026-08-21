# David Chang — Review Of The Paper

Received: 2026-08-18, by email. Reviewer: David Chang, added as third author 2026-08-18.

He reviewed a build that predates the 2026-08-14 cohort rebuild and the 2026-08-18 AlphaFold isoform
audit, and says so. Each claim below was checked against the current source before any action was taken;
the verdict column records that check, not his accuracy against the build he held.

## What he raised

| # | Claim | Verdict against the current source |
|---|---|---|
| 1 | Distance is taken from any heavy atom including backbone, but the phosphate attaches to the side-chain tip (OG/OG1/OH). The peptide-bond artefact is therefore a consequence of the measurement definition, not a finding in the data. No comparator is a better-specified version of the same idea, so the conclusion's scope is narrower than the paper reads. | **Live.** §4.5 states the choice; the alternative was never tested. |
| 2 | The heuristic is a local claim, but the AUC ranks every pair at every distance, and ~95% of pairs are comparisons the heuristic never made. Report AUC restricted to 15 Å and 10 Å, and give the threshold contrast a protein-cluster interval and an *n*. | **Live.** §2.3's 40.0% vs 49.0% is descriptive, with no interval. |
| 3a | Numbers disagree between sections: inverse RSA 0.604 vs 0.607; experimental-target arm 0.575/287 vs 0.576/286; §2.1's primary interval. | **Two live, one already correct.** §2.7.2 and Table 4's fitness row are stale. §2.1 already reads 0.417–0.632. |
| 3b | §4.7 says the human cohort cannot be rebuilt end to end; Data Availability says the generator exists. The sections contradict each other, and "reproduces 1,587 of 1,595 rows" is the language of a reconstruction checked against an original, not a generator. | **Live, and he is right about the direction.** Data Availability was rewritten 2026-08-14; §4.7 was not. The generator now is the generator, and the eight rows and the TKT S308 misassignment were resolved on 2026-08-14. |
| 4 | Three within-protein estimates are reported separately and never combined, leaving the paper's most useful quantity unestimated. Combine yeast with one designated human screen; the two human screens share all sites and are not independent. Add a conditional logistic regression stratified on protein. | **Live.** |

## What he raised that the current build had already closed

The generator exists and is fail-closed offline; the yeast builder's sequence and model-version
assertions are ported; the TKT S308 misassignment is corrected; the cohort is rebuilt to 1,470 sites in
787 proteins with every structure asserted to be the exact canonical AFDB v6 model; and the package
verifier binds the human rebuild manifest and its hashes.

## One correction to his proposal

His second variant under point 1 — subtracting the phosphate's effective reach of three or four
ångströms — cannot change any AUC. Subtracting a constant from every distance leaves the ranking
identical, and the AUC is a rank statistic. It does move sites across a fixed cut-off, so it is relevant
to the threshold and range-restricted analyses of point 2, and it is used there rather than as a
comparator.

## Source

His email is held by Kyle Nguyen. It is not reproduced here: this directory is synced to a public
repository, and a co-author's private correspondence does not belong in it. The claims above are quoted
only as far as needed to record what was checked and what was found.
