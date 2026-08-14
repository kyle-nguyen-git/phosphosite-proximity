# Distance to the nearest annotated active or binding residue: what it measures, and how it ranks sites in yeast and human phosphosite-mutant screens

**Short title:** Phosphosite distance to annotated residues in yeast and human screens

**Kyle Nguyen**^1^\*, **Arkady Marchenko**^2^

^1^ Human Biology, College of Natural Sciences, The University of Texas at Austin, Austin, Texas, USA

^2^ Department of Computer Science, College of Natural Sciences, The University of Texas at Austin, Austin, Texas, USA

\* Corresponding author. Email: ktnuyen04@gmail.com

**Author note:** The affiliations identify where the authors study. This work was carried out independently of the university, without institutional funding, supervision, or resources, and implies no endorsement by The University of Texas at Austin.

## Abstract

Work that ranks which protein modification sites are worth following up often leans on how close a site sits to a residue already annotated as part of an active or binding site. This paper asks what that measurement contains, and how well it separates sites whose mutation changed a phenotype from those whose mutation did not.

The predictor is the shortest distance between any non-hydrogen atom of the modified residue and any non-hydrogen atom of the nearest annotated residue, in an AlphaFold DB version 6 monomer model. It was measured on 163 alanine substitutions in 48 yeast proteins, and on 1,471 base-edited sites in 788 human proteins. The cohorts share the distance definition and the estimator, not a builder.

In yeast, distance ranked sites at an area under the receiver-operating-characteristic curve of 0.527 (95% confidence interval 0.417–0.632, resampling whole proteins), where 0.5 is uninformative; a second cohort version keeping the three self-annotated sites gives 0.544 (0.436–0.649) on 166 sites. The human experiment reports two screens with different readouts, analysed separately: 0.558 (0.474–0.637) on a fitness screen and 0.483 (0.418–0.550) on an NFAT reporter screen. Five further endpoint definitions, three using no p-value, all give intervals containing 0.5.

What the statistic rests on is mostly not experimental and mostly not within a protein. Of 163 yeast nearest-target assignments, 143 were not experimentally established; half the sites within 5 Å are the next residue along the chain; and 2.65% of yeast and 0.10% and 0.16% of human ranked pairs compare two sites in one protein. One post hoc result stands out and is not adjusted for multiplicity: how deeply a residue is buried has an interval above 0.5 in the fitness screen, 0.607 (0.530–0.678), although its paired difference against distance contains zero. No paired difference in either cohort excludes zero.

**Keywords:** phosphorylation; AlphaFold; yeast; mutational phenotype; structural bioinformatics; exploratory analysis

## 1. Introduction

A phosphosite is a serine, threonine or tyrosine that the cell can tag with a phosphate group to change how a protein behaves. Most phosphosites that have been observed have no assigned function. Methods that pick out the ones worth studying score each site by combining several kinds of evidence: how conserved the position is across species, the surrounding sequence, the protein domain it sits in, how exposed it is on the surface, and whether it lies where two proteins touch [1–4]. Distance to a residue already annotated as an active site or a binding site is not among the features those published scores combine. The largest of them, the 59-feature model of Ochoa et al. [3], contains no such distance, and we checked its released feature table rather than inferring this.

What the literature contains instead is proximity used as evidence in two other forms. One is enrichment: asking whether functional sites cluster near catalytic residues, across groups of residues rather than site by site. The other is a fixed cut-off used to decide that two residues are in contact. In a literature sweep completed on 11 August 2026 we located no method, database or paper that ranks or scores individual sites by distance to the nearest annotated active or binding residue.

That absence is the reason for this paper rather than an objection to it. A quantity can circulate as a rule of thumb without ever being calibrated, and these two forms together make a short distance to a functional residue read as evidence that a site matters. What that reading is worth, applied one site at a time against a measured phenotype, is not recorded anywhere. This paper writes the heuristic down as a single number, applies it to two mutational screens, and asks what it separates. No probability calibration is performed; the question is ranking.

The 5 Å figure that travels with this idea traces to Strumillo et al. [2]. They mapped conserved phosphorylation hotspots onto experimentally determined structures from the Protein Data Bank and tested closeness to catalytic residues with Fisher's exact test. In enzyme domains, 3.3% of hotspot residues lie within 5 Å of a catalytic residue against 0.97% of other residues, which they report as hotspot positions being "5 times more likely to be within 5 Å distance" of a catalytic residue (p = 1.5 × 10⁻⁸). A 15 Å criterion appears in the same analysis. That figure is an enrichment ratio: one group of residues compared against the other residues of the same proteins. No individual site is classified by its distance, and the area under the ROC curve that the paper reports belongs to a conservation p-value.

Similar distance figures elsewhere in the field are cut-offs for deciding that two residues touch. PTMcode v2 calls two modified residues in contact below 4.69 Å [5]; the cited paper states the threshold without setting out its derivation. ProtVar highlights residues at a contact between two chains at 8 Å [6]. HotSpot3D pairs mutations at 10 Å or less within a chain, requiring more than twenty residues of separation along the sequence, and allows up to 20 Å between chains and for drug–mutation pairs [7]; the 20 Å figure is the between-chain rule, not a universal one. None of the three ranks sites.

Beltrao et al. [8] prioritized modification sites by evolutionary and structural context across eleven eukaryotes, with validation in yeast. Phosphosites are enriched at interfaces in heterooligomers and in weak transient homooligomers [9], which is narrower than a claim about protein contact surfaces in general. A model of a protein on its own — a monomer model, which is what is used here — contains no such surface, because the partner is absent. Complexes can be obtained experimentally, by homology, by docking, or by prediction methods including AlphaFold-Multimer [10]; none is used here.

Two studies sit closer to this one than the rest, in different ways. Correa Marrero et al. [21] measure distance from a phosphosite to the nearest functional site directly, in paired phosphorylated and unphosphorylated structures, and relate it to mechanical strain; they report co-straining for about 5% of phosphosite–functional-site pairs. That is an analogous phosphosite-to-functional-site relation rather than the same measurement: they work from paired experimental structures over a broader set of functional-site categories, and this paper works from AlphaFold monomers, restricted to `ACT_SITE` and `BINDING`, using the closest pair of non-hydrogen atoms. The evaluation differs too — theirs against structural response, this against a phenotype. StructureMap [4] is the closer relative on method rather than on quantity: it also works from AlphaFold monomer coordinates, binning distances at 1 Å up to 35 Å in 5 Å steps, with co-localization bins starting at 0 Å and no minimum separation along the sequence. Its headline structural variable is side-chain exposure, computed within a 12 Å radius and a 70° angle, and it reports no discrimination statistic for distance taken on its own. The 59-feature functional score of Ochoa et al. [3] names "1D structural properties, phosphorylation structural hotspots, structural stability and interfaces and protein topology annotations". Its Supplementary Table 2 does report a mean AUC for each feature before training, in a `feature_relevance` sheet, and that same workbook supplies the twelve comparators used in §2.7.5. Those per-feature values are computed against that study's own curated labels and validation design, so they are not a like-for-like comparator for a mutant-screen estimate, and none of the features it lists is a distance to the nearest annotated active or binding residue.

Figure 2d of Viéitez et al. [1] reports areas under the ROC curve for sorting sites into loss-of-function or gain-of-function against unchanged, using categories of evidence that include "position on protein structure". The area under the ROC curve, written AUC below, is the chance that a randomly chosen site with a growth change is ranked ahead of a randomly chosen site without one, where 0.5 is what an uninformative measurement gives. The values behind those categories are distributed in their Supplementary Data 6.

What that figure measures and what this paper measures are three different things. The outcome here is a single yes-or-no label: did the source report a growth change at this site in at least one condition, in either direction. It is not a loss-versus-gain call against unchanged. The predictor here is one continuous number declared in advance: the shortest distance between any non-hydrogen atom of the replaced residue and any non-hydrogen atom of the nearest residue that UniProt annotates as an active site (`ACT_SITE`) or a binding site (`BINDING`), with records that span several residues expanded to every residue they span. This is the minimum heavy-atom distance, called the distance below. And the cohort here is rebuilt from the condition-by-condition screening data to 163 replaced sites in 48 proteins; Supplementary Data 6 supplies annotations only and takes no part in deciding which sites are eligible or in the outcome. We did not retrieve the numeric values plotted in Figure 2d and make no comparison against them.

To our knowledge, based on searches of Europe PMC, publisher full texts, and tool documentation as of 11 August 2026, no earlier study tests minimum heavy-atom distance from an observed phosphosite to the nearest annotated active or binding residue, in a monomer model, against a phenotype measured in a mutant screen, with uncertainty computed over proteins. That statement is bounded by those databases, that search date, that model type, that target definition, that endpoint and that inferential unit; it is not a claim that proximity to functional sites is unstudied, and [21] measures an analogous phosphosite-to-functional-site distance against a structural rather than a phenotypic outcome.

This paper asks four things about one measurement. First, what the cohort of sites and the set of annotated target residues are actually made of. Second, whether distance separates the sites the screen reported a growth change at from the rest. That is tested against a permutation null, meaning the outcome labels shuffled at random many times to show what the measurement returns when there is nothing to find; against other predictors computed on exactly the same sites; and under stricter and direction-specific definitions of what counts as an affected site. Third, what distance stands in for, both at very short range and when sites in different proteins are compared. Fourth, what a study of this size, with this outcome and this annotation, can settle at all.

The fourth question can be answered before any estimate is reported. Uncertainty here is expressed by resampling whole proteins rather than individual sites, a protein-cluster bootstrap, because sites in the same protein are not independent of one another. The 95% interval built that way around the primary AUC (163 replaced sites) has a half-width of 0.107. The lowest and highest single-feature point estimates reported on this cohort are 0.527 and 0.606, a spread of 0.079. Those two estimates rest on different numbers of sites, 163 against 152, so the spread is indicative and not a like-for-like contrast. Read with that caveat, the arithmetic says the study cannot resolve differences of the size it is measuring. It does not license putting the features in order, and no such ordering appears anywhere below.

The analysis is exploratory. The main quantity to be estimated was fixed after the outcome data had already been looked at, and none of the round-2 analyses reported here was registered in advance. Methods §4.1 gives the order in which things happened and marks what was decided after seeing results.

## Terms used

- **Phosphosite** — a serine, threonine or tyrosine that the cell can tag with a phosphate group.
- **Replaced site (substitution)** — one such residue changed to alanine in the source screen.
- **Affected site** — the source reported a growth change there in at least one condition, in either direction.
- **Distance** — the shortest atom-to-atom distance from the replaced residue to its nearest annotated target, non-hydrogen atoms only (minimum heavy-atom distance).
- **Annotated target** — a residue UniProt records as an active site (`ACT_SITE`) or a binding site (`BINDING`).
- **Monomer model** — an AlphaFold model of a protein on its own, no partners or ligands.
- **AUC** — area under the ROC curve: the chance a randomly chosen affected site ranks ahead of a randomly chosen unaffected one. 0.5 is what an uninformative measurement gives.
- **pLDDT** — AlphaFold's confidence score for a residue; higher is more confident.
- **PAE** — predicted aligned error: AlphaFold's estimate, in ångströms, of how wrong one residue's placement is relative to another.
- **Protein-cluster bootstrap** — an uncertainty interval built by resampling whole proteins rather than single sites.
- **Post hoc** — decided after the results had been seen.

## 2. Results

### 2.1 Most nearest targets are not experimentally evidenced, and half the proteins are kinases

Supplementary Data 1 of the source screen [1] contains 497 point-mutant strain records, covering 490 replaced sites as numbered in the source, in 116 UniProt entries. After one provisional coordinate resolution, 487 records matched the reviewed sequence (479 replaced sites, 113 proteins). Of those, 465 carried a growth profile across conditions (458, 111). Two strain-level quality-control filters then left 447 (443, 110) and 427 (423, 107). Requiring both an annotated active or binding residue and an AlphaFold model left 169 strain records in 50 proteins, which collapse to 166 distinct replaced sites once repeat strains are averaged (Table 1, Fig 1A).

**Table 1. Cohort reconstruction.**

| Stage | Strain records | Substitutions | Proteins | Role or exclusion |
|---|---:|---:|---:|---|
| Point-mutant source rows | 497 | 490 source-coordinate | 116 | Supplementary Data 1 constructs |
| Sequence matched after PBY107 resolution | 487 | 479 resolved-coordinate | 113 | 10 unresolved mismatches excluded |
| With a condition-level profile | 465 | 458 | 111 | 22 lacked a Supplementary Data 3 profile |
| After sequencing exclusion | 447 | 443 | 110 | 18 excluded; all 18 affected |
| After scar-correlation exclusion | 427 | 423 | 107 | 20 excluded, 16 affected; filter defined on phenotype similarity to a marker control |
| Annotation and structure eligible | 169 | 166 | 50 | Annotated active or binding residue, AlphaFold model, repeat strains averaged |
| Primary cohort | — | 163 | 48 | 79 affected, 84 unaffected |
| Inclusive 0 Å sensitivity cohort | — | 166 | 50 | 82 affected; three 0 Å sites retained |

Of the 427 retained records 169 (39.6%) are affected, against 34 of the 38 excluded (89.5%).

![Fig 1. Cohort reconstruction and the primary distance estimate.](manuscript_build/submission_figures/Fig1.png)

**Fig 1. Cohort reconstruction and the primary distance estimate.** (A) The cohort cascade, counting strain records separately from distinct replaced sites. Stage one counts sites as numbered in the source, and later stages count them after coordinates are resolved, which is why 490 becomes 479 rather than 480 once PBY107 is resolved onto a position PBY131 already occupies. All six declared stages are shown and the panel matches Table 1 row for row. Supplementary Data 1 supplied the constructs, Data 3 the outcomes and Data 8 the quality-control flags; Data 6 contributed annotations only and did not determine eligibility. (B) ROC curves for both cohorts, with shorter distance scored toward an affected label; the dashed diagonal is chance. The band is the 2.5th-to-97.5th percentile envelope, at each false-positive rate, of 2,000 protein-cluster bootstrap curves. It is wider than the confidence interval on the AUC by construction and is not that interval; no resamples were discarded at the committed data and seed. The predictor is the shortest heavy-atom distance from the replaced residue to the nearest UniProt-annotated active or binding residue, annotations expanded to every residue they cover, in an AlphaFold DB version 6 model of the protein on its own. A site counts as affected when the source reports a q-value below 0.05 in at least one condition it was measured in. Primary AUC 0.527 (protein-cluster bootstrap 95% confidence interval, 0.417–0.632); inclusive 0.544 (0.436–0.649).

A site counts as affected when the source reports a q-value below 0.05 — a p-value adjusted so that, among all the calls made, the expected share of false ones is controlled — in at least one condition it was measured in, whatever the sign of the effect. The primary cohort drops the three sites that are themselves an annotated residue: 163 replaced sites in 48 proteins, 79 affected and 84 unaffected. A second version of the cohort, called the inclusive arm below, keeps those three at their distance to themselves of 0 Å: 166 replaced sites in 50 proteins, 82 affected.

Separation is measured throughout as the AUC, with shorter distance scored toward an affected label, and every interval is a 95% percentile bootstrap that resamples the UniProt entries rather than the individual sites. Omitting the provisionally resolved HOG1 record from the inclusive arm gives 0.540 (protein-cluster bootstrap 95% confidence interval, 0.433–0.645) on 165 replaced sites, 81 affected.

The two filters removed 38 records, 34 of them affected (89.5%), against 169 affected among the 427 kept (39.6%). All 18 records flagged by sequencing were affected, as were 16 of the 20 flagged by scar correlation (80.0%). The scar-correlation filter works by comparing a strain's phenotype with that of a marker control, so for those 20 records the decision to exclude depends on the outcome by construction. None of those 20 reaches the analysis cohort by any route: all 20 sit in proteins for which UniProt records no active or binding site, so they are removed by annotation eligibility before the filter is consulted. Of the 38 excluded records, 10 are in a protein carrying an eligible annotation with a model, all 10 flagged by sequencing and all 10 affected. Restoring them adds 9 sites the cohort does not otherwise contain and gives 172 sites in 48 proteins, 88 affected, with an AUC of 0.502 (0.392–0.608) against the primary 0.527 (0.416–0.632) at the same 200,000 resamples. Restoring the excluded records moves the estimate toward 0.5 by 0.025, not away from it.

Among the records that passed quality control, the 169 that were annotation-eligible, in 50 proteins, are 84 affected (49.7%); the 258 that were not eligible, in 57 proteins, are 85 affected (32.9%). The gap is 16.8 percentage points. Eligibility turns on a property of the whole protein — whether UniProt records an active or binding site for it at all — before any site-by-site comparison begins.

Sequencing covered 244 of the 497 point-mutant records and 88 of the 169 eligible strain records. Among those 88, 46 carry a coding variant in some other gene, 4 carry one in the gene being tested, and 3 are flagged for copy-number change; none carries any text in the free-text quality-control note. That note is the only field the exclusion rule reads, so all 88 were kept. The number of conditions behind each site is not the same for every site. `raw_conditions`, the count of conditions with a measured value, takes five values in the primary cohort — 96, 98, 100, 101 and 102, with 155 replaced sites at 102 — and 7 of the 8 sites below 102 are affected.

What follows about the target set was worked out after the primary result, and is post hoc. The eligible annotations are 262 UniProt records — 41 `ACT_SITE`, 221 `BINDING` — drawn from 278 after setting aside 8 `Site` and 8 `DNA binding` records, and they define a target set of **560 distinct residues**. S1 Appendix gives the record-to-residue expansion, the duplicate-removal rules that give 565 and 566 rows, the source of the excess over 560, and the earlier expanded row count that does not reproduce and is withdrawn.

UniProt tags each annotation with an ECO evidence code recording how it was established. Of the 163 nearest targets actually used, 101 carry ECO:0000255, meaning a curated automated rule, and 33 carry ECO:0000250, meaning inferred from a similar protein. Taking the union of evidence codes across every record covering a residue, 20 of 163 (12.3%) rest on experimental evidence, ECO:0000269 or ECO:0007744, and 143 of 163 (87.7%) do not. The count is 19 if the single residue covered by three records is assigned instead to its ECO:0000250 record; that is the only ambiguous row of the 163, so the count travels with the rule used to settle it. Counting residues rather than sites, the 48 proteins carry 533 eligible target residues, 92 of them experimental (17.3%). ATP is the bound molecule at the nearest target for 86 of 163 replaced sites (52.8%), and 24 of the 48 proteins (50%) are protein kinases or subunits of protein-kinase complexes. `BINDING` records span a median of 1 residue and at most 9, and the 33 records spanning 8 or more supply 289 of the 533 residues (54.2%).

Keeping only targets with experimental evidence leaves 24 of the 163 replaced sites (14.7%) with any target at all, in 7 of the 48 proteins; the other 139 lose every target. Those 24 are 11 affected and 13 unaffected, and give an AUC of 0.420 (0.244–0.708) with 19,991 of 20,000 resamples retained. With only 7 proteins to resample the interval endpoints are coarse. The same restriction on the human cohort of §2.7 retains 512 sites in 287 proteins and can be read. The interval is a descriptive range, equally compatible with distance ranking sites the wrong way round and with moderate discrimination. Whether better-evidenced annotation would move the estimate cannot be asked of this design.

### 2.2 The estimate sits inside the spread of a shuffled-label null

The median distance to the nearest annotated target is 26.23 Å at affected sites and 31.83 Å at unaffected ones. The primary AUC is 0.527 (protein-cluster bootstrap 95% confidence interval, 0.417–0.632; Fig 1B) on 163 replaced sites in 48 proteins. The inclusive arm gives 0.544 (0.436–0.649) on 166 replaced sites in 50 proteins. Both intervals use 200,000 protein-cluster resamples at seed 20260729, and all 200,000 were usable.

The rest of this subsection was specified after the primary result. Shuffling the affected and unaffected labels 20,000 times across the whole cohort gives a null distribution centred at 0.500 with a standard deviation of 0.045, and 2.5th and 97.5th percentiles at 0.411 and 0.588. The observed value sits 0.59 standard deviations above that centre, two-sided p = 0.55. Shuffling labels only within each protein keeps every comparison between proteins fixed; that null centres at 0.512 with a standard deviation of 0.030, and the observed value sits 0.49 standard deviations above its centre, p = 0.63 measured from that centre.

**Both of these are diagnostic reference distributions rather than tests, and are reported as such.** Uncertainty everywhere else in this paper treats the protein as the resampling unit, on the grounds that sites in one protein are not independent. Shuffling labels across the whole cohort breaks that structure, since it moves labels between proteins and so destroys the protein-level composition the clustered interval is built to respect. Shuffling within proteins preserves it but leaves every between-protein comparison fixed, and those comparisons are 97.35% of the statistic, which is why that null centres at 0.512 rather than 0.500. Neither is the null distribution of the clustered site-weighted quantity actually reported. No p-value in this paper should be read as a formal test of that quantity; a null-generating process that preserves the relevant cluster structure was not constructed here.

The declared post hoc families of the yeast analysis come to 255 estimates: 11 model-confidence strata in each of two cohort versions, 72 cells of a PAE grid in each of three cohorts, 5 alternative definitions of the distance feature, 7 cohort and residue-class checks, and 5 continuous outcomes. Out of 255 estimates, 12.75 are expected to reach p < 0.05 by chance alone. Drawing 255 values from the nulls above, the median of the largest departure from the null centre corresponds to an AUC of 0.635 under the unrestricted null and 0.604 under the within-protein null. Those two figures come from drawing 255 independent values, which the actual family is not: the PAE grid cells are heavily overlapping subsets of the same sites, supports range from 16 to 166, and the variances differ. Independence is not guaranteed to bound the maximum of a dependent family in either direction, so the calculation is an illustrative reference rather than a bound. Permuting the complete family, preserving its filters and supports, would be required to make it one, and that was not done. The count is of yeast estimates only; the human endpoint, comparator and within-protein estimates of §2.7 are not in it, and no combined family was frozen.

The AUC in the primary arm averages over every pairing of one affected site with one unaffected site: 79 × 84 = 6,636 pairs. Only 176 of them (2.65%) put two sites in the same protein. Twenty-three of the 48 proteins contain both affected and unaffected sites and hold 112 of the 163 replaced sites; the other 25 proteins hold 51 sites that are all of one class and contribute only comparisons across proteins.

Restricted to those 176 within-protein pairs, weighting every pair equally, the AUC is 0.528 (0.368–0.709) on 112 replaced sites in 23 proteins. That is the designated within-protein quantity. Weighting every protein equally instead gives 0.497 (0.351–0.642) across the 23 proteins, and ranking each site by its distance percentile inside its own protein gives 0.511 (0.412–0.612) on all 163 sites; both are reported as checks. The pairs sit in a few proteins. Q03656 supplies 50 of the 176 (28.4%), the five largest proteins supply 69.3% between them, and four proteins supply exactly one pair each, on which a within-protein AUC can only be 0 or 1. Across the whole cohort the 48 proteins hold between 1 and 15 sites each, the six largest hold 55 of the 163 replaced sites, and the Kish effective cluster count — how many equally sized proteins would give the same resampling precision — is 29.0 against the nominal 48.

A logistic model, with standard errors that allow sites in the same protein to be correlated, gives an odds ratio of 0.77 (0.27–2.15) per ten-fold increase in distance plus 1 Å. Adjusting for two further quantities moves it to 1.31 (0.38–4.51). Those two are site pLDDT, AlphaFold's confidence score for that residue, stored in the model as the mean atom B factor, where higher is more confident; and relative solvent accessibility, how much of the residue's surface is exposed to solvent as a fraction of the most it could be, computed on the protein alone. Both intervals contain 1, the value that means no association. Against a t distribution with 47 degrees of freedom in place of the normal reference they widen to 0.27–2.21 and 0.37–4.66.

### 2.3 Half the sites inside 5 Å are the neighbouring residue in the chain

Ten sites in the primary cohort sit within 5 Å of their nearest target. Five of them — PDA1 S313, YCR087C-A T49, VMA2 S380, INO1 S368 and HSP82 S379 — sit at 1.33–1.34 Å and are the next residue along the chain from their target, |Δposition| = 1, where |Δposition| is the gap in sequence position between the replaced residue and its nearest target. That is the C–N peptide bond joining one residue to the next: for residues *i* and *i*±1 the bonded C–N pair is itself one of the candidate atom pairs, so the shortest heavy-atom distance cannot exceed that fixed backbone contact and the measured value is a constant of the chemistry. Their outcomes are 2 affected and 3 unaffected. A sixth, YCR087C-A S53 at 3.60 Å, has |Δposition| = 2. The remaining four have |Δposition| of 38, 38, 70 and 224, and are 2 affected and 2 unaffected.

Across the cohort, |Δposition| is 1 for 5 sites, 2 for 1 site and 3 or more for 157, with nothing between 3 and 37, so any cut-off in that window picks out the same 157 sites. Both the cut-off and the check built on it are post hoc. Dropping the sites with |Δposition| ≤ 2 gives an AUC of 0.541 (0.429–0.648) on 157 replaced sites in 48 proteins, 77 affected and 80 unaffected, with all 20,000 protein-cluster resamples retained at seed 20260728. The three sites that distinguish the two cohort versions are the ones coinciding with an annotated residue, at |Δposition| = 0, so this filter reduces both versions to the same 157 sites. That is one estimate, not two versions agreeing.

Sites inside the 5 Å cut-off are affected less often than sites beyond it, 40.0% against 49.0%, a descriptive odds ratio of 0.693 on 10 sites; the two distance distributions are drawn in Fig 2A. That inversion comes entirely from the peptide-bond neighbours. With those removed the cut-off holds 4 sites, 2 of them affected, an odds ratio of 1.040; on a bin of four sites only the count is reported. The declared predictor is not redefined. `min_dist_A`, the distance on all 163 rows, remains the primary quantity.

![Fig 2. What the distance measurement contains.](manuscript_build/submission_figures/Fig2.png)

**Fig 2. What the distance measurement contains.** (A) Cumulative distance distributions in the primary cohort, drawn separately for screen-negative and screen-positive sites, with the three inclusive-only sites at 0 Å marked. (B) Maximum directional predicted aligned error for each site–target pair against the distance between them, with each point coloured by the confidence the model assigns the site. Longer distances co-occur with lower site confidence and higher pair error, so distance and model confidence are not separable in this cohort. The eleven-stratum confidence family and the cohort, residue-class and feature-definition checks that earlier occupied this figure are S1 Fig and S2 Fig.

### 2.4 No alternative predictor is distinguishable from distance on the same sites

Seven other predictors were computed on the same 163 replaced sites of the primary cohort and compared with `min_dist_A`, the declared distance. Each comparison is a paired difference: both predictors are scored on the same sites inside the same protein resamples, so the variation the two share cancels and the interval reflects only how they differ. All of this was done after the primary result. All eight predictors have a value on all 163 rows.

| Predictor | Orientation | AUC | 95% interval | Δ vs `min_dist_A` | Δ 95% interval |
|---|---|---:|---:|---:|---:|
| min \|Δposition\| over the eligible `ACT_SITE` + `BINDING` set | smaller → positive | 0.550 | 0.434–0.653 | +0.023 | −0.049 to +0.090 |
| \|position − `nearest_feat_pos`\| | smaller → positive | 0.533 | 0.416–0.639 | +0.007 | −0.084 to +0.093 |
| Protein length | larger → positive | 0.549 | 0.444–0.660 | +0.023 | −0.159 to +0.215 |
| Site pLDDT | larger → positive | 0.555 | 0.464–0.641 | +0.028 | −0.067 to +0.131 |
| Inverse relative solvent accessibility | smaller RSA → positive | 0.587 | 0.489–0.672 | +0.060 | −0.041 to +0.162 |
| `n_annot_residues`, eligible annotated residues in the protein | larger → positive | 0.555 | 0.470–0.649 | +0.029 | −0.082 to +0.152 |
| `raw_conditions` (bookkeeping negative control) | larger → positive | 0.462 | 0.426–0.496 | −0.065 | −0.183 to +0.057 |
| `min_dist_A` (declared predictor) | smaller → positive | 0.527 | 0.416–0.631 | reference | — |

Intervals in the table use 20,000 protein-cluster resamples at seed 20260728, all retained, which is why the row for the declared predictor differs in the third decimal from the headline interval built from 200,000 resamples, 0.417–0.632. For protein length, site pLDDT, `n_annot_residues` and `raw_conditions` there was no prior reason to expect one direction rather than the other; the table prints the direction chosen.

No comparator's interval excludes 0.5 except the bookkeeping negative control, and no paired difference against `min_dist_A` excludes zero. The largest point difference is inverse relative solvent accessibility at +0.060. Rows 1 and 2 use sequence position only and need no structure at all: the first takes the smallest sequence gap to any eligible target, the second takes the sequence gap to whichever target is nearest in three dimensions. Their AUCs differ by 0.016.

`raw_conditions` is an artefact of ties, not a predictor that points the wrong way. It takes five values on this cohort and 155 of the 163 sites share the value 102, so almost every pair of sites is tied and contributes exactly 0.5 to the AUC. The point estimate is pinned near 0.5 by construction, and the narrow interval reflects a variable that barely varies, not a precise measurement. Its interval excludes 0.5 on the strength of 8 sites out of 163, that behaviour is stable across seeds, and its paired difference against distance does include zero.

#### 2.4.1 SIFT scores are missing disproportionately at long distances and affected sites

SIFT [11] predicts from sequence conservation whether replacing one amino acid with another will damage the protein; a lower score means more damaging, so the score is inverted here to point the same way as the other predictors. It was available for 152 of the 163 replaced sites, 71 of them affected. On those 152 sites SIFT gave 0.606 (0.522–0.690) against 0.532 (0.418–0.647) for distance, and the paired difference, SIFT minus distance, was 0.074 (−0.037 to 0.192). SIFT was computed after the primary result. Its interval does not contain 0.5, which is what a positive control for this outcome requires; §3.2 sets out what that does and does not license.

The 11 sites with no SIFT score come from 6 proteins, and whether a score is missing is related to both the outcome and the distance. Eight of the 11 are affected, 72.7% against 46.7% among the scored sites, and their median distance is 51.80 Å against 28.52 Å. Dropping to the sites both predictors cover moves the distance AUC from 0.527 to 0.532, slightly in distance's favour.

The AUC depends only on the order of the scores, so filling those 11 missing values in at the most extreme rank each site's outcome allows brackets everything any filling-in could produce. That range is −0.00 to +0.13 on the paired point estimate, read to two decimals because all 11 missing rows come from 6 proteins, and it contains the reported 0.074. It is a bound on what is arithmetically possible, not a range of plausible values, and its upper end is reached only if all 8 unscored affected sites rank above every scored site and all 3 unscored unaffected sites rank below.

#### 2.4.2 Feature combinations are not distinguishable at this sample size

Models were fitted and tested on the same 163 replaced sites by five-fold cross-validation: the sites are split into five parts with the affected and unaffected balanced across them, each part is predicted in turn by a model fitted on the other four, and whole proteins are kept together so no protein is split across parts. The split was repeated 10 times, over 10 split seeds, and folds were weighted by the number of affected/unaffected pairs they contain. Two summaries are given for each model. Split-averaged means the AUC is computed inside each fold and then averaged. Pooled out-of-fold means the 163 predictions, each made by a model that never saw that site, are put together and ranked once.

The model is L2-penalised logistic regression at the scikit-learn default inverse regularisation strength of 1.0, solved by liblinear, with no hyperparameter search. Every preprocessing step sits inside the cross-validation pipeline and is therefore fitted on the training rows of each fold only: missing values are filled with the training-fold median and a binary indicator column is added for each feature that had any, then all features are standardised to zero mean and unit variance on the training fold. That imputation is why models using inverse SIFT report all 163 sites although SIFT covers 152; the 11 sites without a score are given the fold median and flagged, rather than dropped. Splits use scikit-learn's stratified grouped five-fold splitter with the protein as the group.

| Model | Features | Split-averaged AUC | Pooled out-of-fold AUC | Brier |
|---|---|---:|---:|---:|
| Constant prevalence | none | 0.500 | 0.500 | 0.250 |
| Distance only | `logd` | 0.484 | 0.393 | 0.258 |
| Structural | `logd`, pLDDT, RSA, `pae_pair_max`, log target count | 0.558 | 0.523 | 0.259 |
| Published annotations | disorder, evolutionary age, UniProt domain, inverse SIFT, kinase-motif score | 0.590 | 0.573 | 0.252 |
| Combined | all ten of the above | 0.587 | 0.569 | 0.259 |

`logd` is log10(distance + 1 Å). `pae_pair_max` is the larger of the two predicted aligned error values for the site–target pair; predicted aligned error is AlphaFold's estimate, in ångströms, of how far off one residue is placed when the model is aligned on the other, and it is reported separately in each direction. Log target count is the log of `n_annot_residues`, the number of eligible annotated residues in the protein.

No interval is stored for any pooled figure, and none exists for the benchmark models. The 2.5th and 97.5th percentiles across the 10 repeats describe how much the answer moves when the data are divided differently; they are not sampling uncertainty. No paired sampling-uncertainty comparison between the models was computed, so this paper reports no inferential comparison among them; the four summaries are given as they stand. Adding the five structural features to the five published annotations improves neither summary, by −0.003 split-averaged and −0.004 pooled, and worsens the Brier score, which measures how far predicted probabilities sit from the observed outcomes, from 0.252 to 0.259.

The pooled value is lower than the split-averaged value for all four fitted models, by 0.016 to 0.091. That gap is built into the two definitions: the split-averaged number never compares a site in fold 1 against a site in fold 4, and the pooled number does. For distance the sign of the effect flips between the pooled ranking, 0.393, and the primary AUC, 0.527 with an interval spanning 0.5, and neither is precise enough to settle it.

### 2.5 Stricter and direction-specific outcome definitions leave the estimate near chance

Requiring a site to be called in more conditions before it counts as affected moves sites from affected to unaffected without removing any, so the cohort stays at 163 replaced sites in 48 proteins under every definition. Requiring at least 2 called conditions gives an AUC of 0.550 (0.448–0.645) with 58 affected sites in 32 of the 48 proteins; requiring at least 3 gives 0.563 (0.445–0.672) with 47 affected sites in 30 proteins. All six intervals under the published rule for combining repeat strains contain 0.5, and the ≥3 interval is wider than the ≥2 interval. No paired difference between outcome definitions is reported: they share all 163 rows and differ only in the labels, the frozen analysis code contains no estimator for that comparison, and none was computed.

The 21 sites that stop counting as affected at ≥2 each rest on exactly one called condition in a single strain, and their mean distance is 34.39 Å against 30.75 Å across the primary cohort.

At ≥2 the two cohort versions swap order, 0.550 against 0.535, because the three sites coinciding with an annotated residue at 0 Å each rest on exactly one called condition and become unaffected there. That reversal is produced by those three sites' outcomes: they are affected under the any-condition rule and unaffected under the ≥2 rule, which is what swaps the order. It is therefore not an outcome-independent reason for leaving them out of the primary cohort, and no such reason is offered here.

The outcome can also be split by the direction of the growth change. Counting only sites where growth got worse — a q-value below 0.05 with a negative S-score, the direction the stated mechanism predicts — gives 0.505 (0.396–0.604) on 66 affected sites, moving the primary estimate 0.022 toward chance. Counting only sites where growth improved, the same q-value threshold with a positive S-score, gives 0.543 (0.434–0.648) on 60 affected sites, nominally the higher of the two and opposite to what the mechanism predicts. No paired interval on the difference between directions is reported, for the same reason as above, and the separate intervals overstate the uncertainty in that difference because the two definitions share 163 rows and 47 affected sites.

Among the 79 affected sites of the primary cohort, counting only the conditions actually called, 46 are dominated by worse growth, 25 by better growth and 8 are exact ties. The count depends on the counting rule: the same data give 25 if ties are dropped, 33 under `mean_enhance ≥ mean_defect`, and 13 counting only sites with no called defect condition. Whether the outcome reproduces can be checked only on the two sites that kept more than one strain, and those two disagree in one case. The strict-consensus rule, which requires every strain for a site to agree, changes exactly one published label, P43565 S1764A, whose three strains have 16, 0 and 8 called conditions. All of these variants are post hoc.

### 2.6 Distance and model confidence are largely the same variable here

Median site pLDDT in the primary cohort is 46.50; 84 of the 163 replaced residues sit below 50 and 103 of 163 below 70. The Spearman rank correlation between log10(distance + 1 Å) and site pLDDT is −0.541 (Fig 2B). Distance correlates with `pae_pair_max` at 0.753 (0.661–0.827), and site pLDDT with `pae_pair_max` at −0.795 (−0.852 to −0.688). The long distances here are measured where AlphaFold is least sure how the two residues sit relative to one another, so distance and model confidence are largely the same variable on this cohort.

The full eleven-stratum family, for both cohort versions, is S1 Table and S1 Fig. The four predicted-aligned-error summaries at 10 Å and the 72-cell grids are S2 Table. Its primary-cohort values run from 0.416 on 41 sites to 0.683 on 27, and the number of sites falls from 163 to 27 across the family.
The rise where both the site and its target are above pLDDT 90 appears in both cohort versions, 0.641 on 28 primary sites and 0.697 on 31 inclusive. This design cannot separate an effect in well-folded regions from what picking out a stratum of 28 sites can produce on its own.

Tyrosine sites alone give an AUC of 0.604 (16 sites in 12 proteins; 12 affected, 4 unaffected). S2 Fig places this and the other cohort, residue-class and feature-definition checks on one scale. No interval is reported: the upper end of the protein-cluster bootstrap reaches 1, the highest value an AUC can take, and 3.3% (665 / 20,000) of resamples were discarded because every site in them had the same outcome.

The four PAE summaries at 10 Å and the 72-cell grids are in the supplement; its 72 primary-cohort cells run from 0.416 to 0.569.


### 2.7 The same measurement in an independent human experiment, on two screens that disagree

The yeast cohort holds 48 proteins, and its interval is wider than the spread of feature estimates it would have to separate. That objection cannot be answered inside the cohort, so the same measurement was made on a second, independent experiment: Kennedy et al. [20] edited phosphosites in human T cells with base editors; both screens analysed here were run in Jurkat-lineage cells. The predictor, the annotation source, the structure source and the estimator are the ones declared above. The cohort holds **1,471 edited sites in 788 proteins**, against 163 sites in 48 proteins in yeast.

That experiment reports two screens with different readouts, and they are kept apart here. Supplementary Table 3 compares sgRNA abundance before and after introduction of the ABE8e editor, a fitness readout. Supplementary Table 4 compares abundance between GFP-high and GFP-low bins, which reports NFAT reporter activity. They are not two measurements of one thing: at a direction-corrected 5% they call **66 sites in the fitness screen only, 76 in the reporter only, and 6 in both**, and their log fold changes correlate at a Spearman coefficient of 0.12. Pooling them was the first version of this analysis and is withdrawn.

Each screen releases one value per site. That value tracks the smaller of MAGeCK's two one-sided gene-level p-values on most rows but not all: reconstructing that minimum reproduces it on 1,424 of the 1,471 rows for the fitness screen and 1,371 of 1,471 for the reporter screen, and the construction of the remaining 47 and 100 is not established here. A minimum of two one-sided tests is not a two-sided p-value, so the endpoint doubles that minimum. Because the released column does not reproduce it on the 47 and 100 rows above, the minimum is reconstructed from the two directional columns of the source rather than taken from the released one, and doubled. Reconstructing changes nothing in the fitness screen, where no mismatched row crosses the threshold, and moves the reporter screen from 81 affected sites to 82, with BRSK2 S367, DDX47 S9, NR1D1 S280, PDE4A S13 and TBKBP1 S335 changing classification. Keeping the screens apart means there is no second union to correct.

Distance gave **0.558 (0.474–0.637)** on the fitness screen, where 72 sites are affected, and **0.483 (0.418–0.550)** on the reporter screen, where 82 are. The two land on opposite sides of 0.5 from the same predictor on the same 1,471 sites. Both intervals contain 0.5, and the fitness value is the further from it: shuffling the outcome labels 20,000 times puts it 1.66 standard deviations from the centre of that distribution. The shuffle moves labels between proteins and so is a diagnostic reference distribution rather than a test, for the reason given in §2.2, and no p-value is claimed from it.

#### 2.7.1 The reading does not depend on which endpoint is chosen

The endpoint was declared after it was clear that no candidate separated the classes, which makes the choice post hoc. The defence available is to report every candidate, so all of them are in Table 2.

**Table 2. Distance under every human endpoint considered.**

| Endpoint | Affected | AUC | 95% interval |
|---|---:|---:|---:|
| Fitness screen, reconstructed and doubled (declared) | 72 | 0.558 | 0.474–0.637 |
| Reporter screen, reconstructed and doubled (declared) | 82 | 0.483 | 0.418–0.550 |
| Union of both screens, uncorrected (withdrawn) | 296 | 0.505 | 0.465–0.545 |
| Union, corrected for two directions and two screens | 86 | 0.542 | 0.466–0.616 |
| Top tenth by size of log fold change, fitness | 148 | 0.509 | 0.455–0.561 |
| Top tenth by size of log fold change, reporter | 148 | 0.506 | 0.454–0.558 |
| Top tenth by size of log fold change, larger of the two | 148 | 0.511 | 0.456–0.564 |
| The screens' own false-discovery control, below 0.25 | 19 | 0.614 | 0.427–0.778 |

Every interval contains 0.5. The three rows using the size of the fold change use no p-value at all, so they do not inherit the unresolved question about how the released columns were built.

#### 2.7.2 Two features that the pooled version hid

Keeping the screens apart makes two things visible that the union did not.

How deeply a residue is buried has the largest comparator estimate in the fitness screen. Inverse relative solvent accessibility gives **0.604 (0.528–0.675)**, an interval that does not contain 0.5, against 0.524 (0.459–0.590) in the reporter screen, and in the yeast cohort the same quantity had the largest comparator point estimate at 0.587 without excluding 0.5. Its paired difference against distance on the same fitness sites is +0.044 (−0.025 to +0.115) and contains zero, so burial is not shown to outperform distance; the marginal result is a post hoc hypothesis about burial, not a demonstration that burial rather than distance tracks this outcome.

In the reporter screen the smallest gap in sequence position to an eligible annotated residue gives 0.549 (0.485–0.613), an interval containing 0.5, and its paired difference against distance is +0.066 (−0.001 to +0.131), which also contains zero. An earlier version of this analysis reported that difference as +0.071 (+0.005 to +0.137), excluding zero; that rested on the screen's released per-site column rather than a reconstruction from the two directional columns, and it does not survive the endpoint being rebuilt from source. **No paired difference in either cohort excludes zero.** The burial result above is post hoc and unadjusted for the number of features and endpoints examined; it is the strongest lead here, not a finding.

#### 2.7.3 What the pooled statistic estimates, and the within-protein estimate

The comparison remains almost entirely between proteins. Within-protein pairs are **102 of 100,728** on the fitness screen and **184 of 113,898** on the reporter screen, which is 0.10% and 0.16% against 2.65% in yeast. The larger cohort makes this worse, because adding proteins adds across-protein pairs quadratically and within-protein pairs linearly. Only 39 and 49 proteins contribute any within-protein comparison at all; the rest carry a single outcome class throughout.

The pooled AUC is therefore a mostly across-protein quantity. It can track protein length, annotation density, typical fold geometry and anything else that varies between proteins, and resampling proteins fixes the dependence without changing what the statistic averages. That is a different question from the one a user of this shortcut usually asks, which is which site inside a given protein to follow up.

That question can be asked directly, on the proteins carrying both classes. Table 3 gives the numbers and Fig 3 puts them on one scale beside the pooled estimate for all three cohorts. No aggregation in either cohort has an interval excluding 0.5 from above within a protein.

![Fig 3. What the statistic estimates, in both organisms.](manuscript_build/submission_figures/Fig3.png)

**Fig 3. What the statistic estimates, in both organisms.** Pooled and within-protein estimates for the yeast cohort and for each human screen, on one axis, with the number of sites and informative proteins behind each. The pooled estimate is a mostly across-protein quantity; the two within-protein aggregations weight each protein by the affected/unaffected pairs it contributes and equally. Bars are 95% protein-cluster bootstrap intervals and the dashed line is chance. Every interval crosses it. Estimand is distinguished by colour, marker and line style together, so the panel survives grayscale.

**Table 3. Discrimination using only comparisons inside one protein.**

| Cohort | Informative proteins | Pairs | Pair-weighted AUC | Equal-protein-weight AUC |
|---|---:|---:|---:|---:|
| Yeast primary | 23 | 176 | 0.528 (0.368–0.709) | 0.497 (0.351–0.642) |
| Human, fitness screen | 39 | 102 | 0.627 (0.452–0.768) | 0.511 (0.374–0.645) |
| Human, reporter screen | 49 | 184 | 0.413 (0.313–0.510) | 0.376 (0.266–0.489) |

Five of the six intervals contain 0.5. The reporter screen's two aggregations sit below it and the fitness screen's two above, on 39 and 49 informative proteins and 102 and 184 pairs. The exception is the reporter's equal-protein-weight interval, whose upper endpoint is 0.489, and it is not reported here as a result. Its exclusion of 0.5 turns on one protein contributing one pair: PIDD1 carries two sites, one affected at 24.9 Å and one unaffected at 32.8 Å, and its gene symbol matches more than one reviewed UniProt entry, so the cohort rule drops it. Restoring it returns the upper endpoint to 0.502. Of the 49 informative proteins, 47 carry exactly one affected site and 14 contribute exactly one pair, so 32 of the 49 per-protein values are forced to exactly 0 or exactly 1; the 49 values have a standard error of 0.057 and a one-sample *t* against 0.5 gives *p* = 0.04, unadjusted. The same 49 proteins and 184 pairs weighted by pair give 0.413 (0.313–0.510). An earlier version of this analysis reported the same quantity as 0.384 (0.272–0.498) on the released per-site column and as 0.388 (0.279–0.502) on a cohort retaining PIDD1. A quantity that changes which side of 0.5 it falls on when one of 788 proteins enters or leaves is measuring the precision of the estimator, not the predictor.

What this paper can therefore support is an audit of a mostly cross-protein ranking. It does not evaluate within-protein prioritisation, in the sense of establishing what that ranking is worth; it establishes only that no aggregation tried here separates the classes with an interval excluding 0.5 from above, on pair counts this small.

#### 2.7.4 Three properties of the yeast measurement reappear

Restricting to targets carrying experimental evidence, which leaves 24 of 163 sites in yeast and so cannot be asked there, leaves **512 sites in 286 proteins** here: 0.576 (0.449–0.703) on the fitness screen and 0.478 (0.376–0.577) on the reporter screen. Annotation evidence does not move the reading in either.

The short end is again sequence position. **37** sites lie within 5 Å of their nearest target; **16** of those are one or two residues away in the chain and **13** sit in the 1.30–1.35 Å band that is the peptide bond.

#### 2.7.5 A published feature separates the classes, in one screen

Twelve features from the human phosphoproteome annotation of Ochoa et al. [3] were tested on the same sites with the same estimator. On the fitness screen SIFT, which scores how damaging a substitution is expected to be from sequence conservation, gives **0.646 (0.565–0.723)** on the 997 sites carrying a score. On the reporter screen the same feature gives 0.574 (0.497–0.651), an interval that contains 0.5.

So the fitness endpoint can support discrimination by a general substitution-effect predictor, and endpoint blindness alone does not explain its near-chance distance estimate. The same argument is not available for the reporter screen. Neither result shows that either endpoint resolves loss of phosphorylation: SIFT scores intolerance to substitution, and the substitutions here are mostly serine to proline (33.0%) and serine to glycine (22.3%), with threonine to alanine — the clean removal of a phosphoacceptor — reaching only 9.5%. Restricted to those 39 threonine-to-alanine sites the AUC is 0.470 (0.212–0.733), an interval too wide to carry any reading. Restricting instead to the 425 sites edited by a guide that made only one change, so no bystander edit is present, gives 0.516 (0.392–0.641) on the fitness screen and 0.512 (0.402–0.624) on the reporter screen. Li et al. [22], profiling 584,337 serine, threonine and tyrosine positions with 817,089 guides, report that serine-to-proline substitution disrupts domain structure broadly, which is the confound this arm cannot separate from loss of the phosphoacceptor.

#### 2.7.6 What the two cohorts do not share

The yeast outcome is multiplicity-controlled at a q-value below 0.05 within each condition; the human outcomes are direction-corrected within a screen and are not controlled across sites. The screens' own false-discovery columns leave 19 sites at 0.25 and 11 at 0.05, too few to estimate anything, which is why the corrected raw call is used. The perturbations differ as well: every yeast mutant replaces the residue with alanine, while the base editors mostly produce the substitutions listed above. The two cohorts also treat a site that is itself an annotated target differently — yeast removes it, the human workflow keeps it and removes that residue from its own target set — so the human result is an external extension using a related implementation rather than a like-for-like repeat.

## 3. Discussion

### 3.1 What the proxy measures

Only 176 of the 6,636 ranked pairs compare two sites inside the same protein. Every other comparison sets a site in one protein against a site in a different protein, so properties of whole proteins — length, the number of annotated targets, how far a typical residue sits from one — feed into the estimate on the same terms as the within-protein comparison the mechanism is about.

At the short end the quantity being measured is sequence position. Six of the ten sites inside 5 Å sit one or two residues from their nearest target, five of them at the fixed C–N peptide-bond distance. Across the cohort the target that sets the distance is usually a ligand boundary copied in by an automated rule: not established by experiment in 143 of the 163 rows, an ATP contact in 86, in a cohort where half the proteins are protein kinases or subunits of kinase complexes.

Distance and model confidence are largely one variable here. Median site pLDDT is 46.50 and log10(distance + 1) correlates with it at −0.541, so a long measured distance is more often than not a distance between a confidently folded region and a residue the model places with little to constrain it.

How deeply a residue is buried is a candidate common cause of any association between distance and outcome that remains. Inverse relative solvent accessibility, computed on the same 163 rows, has the largest comparator point estimate at 0.587, and the largest paired difference against the declared predictor in the table. Adding relative solvent accessibility to the logistic model moves the odds ratio per ten-fold increase in distance from 0.77 to 1.31, with both intervals crossing 1. Buried sites lie closer to buried annotated residues, and a buried residue replaced by alanine may be more disruptive, which is a mechanism by which burial could sit upstream of both terms. The coefficient change alone does not establish it: collinearity between the two terms and the non-collapsibility of logistic coefficients can move a coefficient without any confounding. It is a hypothesis to test, not a result.

What is measured here is narrower than how position in space regulates a protein inside a cell. The structures are single proteins, so the partners, ligands and contact surfaces that complete many annotated sites are absent. A `BINDING` annotation marks a residue associated with a ligand, not a whole pocket, and the distance is the minimum over non-hydrogen atoms, so a short value can record nothing more than backbone packing between neighbouring residues.

### 3.2 What this design can resolve

The interval on the primary estimate is wider than the spread of single-feature point estimates it would have to separate, as set out in the Introduction, so no feature is ranked anywhere in this paper.

A positive control was computed here and was not treated as one. SIFT gives 0.606 (0.522–0.690) on the 152 sites carrying a score, and that interval does not contain 0.5. A feature already known to track the consequences of an amino-acid substitution does separate affected from unaffected sites on this outcome. So the endpoint can support discrimination by a general substitution-effect predictor, and endpoint blindness alone does not explain the near-chance point estimate. It does not follow that the endpoint resolves loss of phosphorylation specifically: SIFT scores intolerance to substitution, and the substitutions here are alanine in yeast and mostly proline and glycine in human.

Three things bound how far that reading goes. Eight predictors besides the declared distance were computed at the 5% level, so 0.4 intervals excluding 0.5 were expected by chance alone and two were observed, one of which is the `raw_conditions` tie artefact. The paired difference, SIFT minus distance on the 152 shared sites, is 0.074 (−0.037 to 0.192) and contains zero, so SIFT is not shown to outperform the declared predictor. And SIFT is scored on the same cohort in which 176 of 6,636 ranked pairs compare two sites in one protein, so whether its discrimination is between sites or between proteins is not resolved here. Neither is it resolved in the human cohort, where the corresponding counts are 102 of 100,728 and 184 of 113,898, and Table 3 estimates the quantity directly (§2.7.3) and only 39 and 49 proteins contribute a within-protein comparison at all. What the control establishes, in the fitness screen of §2.7.5, is that the outcome is not blind. It does not establish that any outcome here resolves sites within a protein, which is the comparison the mechanism is about, and no cohort assembled for this paper can settle it.

If sites are mislabelled in a way unrelated to their distance, the AUC is pulled toward 0.5. The source q-values control the error rate within each condition across strains, not within each strain across the panel of 102 conditions, and how often the any-called-condition rule labels an unaffected site as affected cannot be estimated from the released data. The error rate this implies at the level of individual sites is not stated.

The intervals rest on fewer effective units than the 48 proteins being resampled: proteins hold between 1 and 15 sites, and the Kish effective count is 29.0. The 200,000 resamples behind the primary interval control the noise from resampling itself; they do not by themselves make a percentile bootstrap cover the true value at its stated rate when the clusters are this few and this uneven. That was measured rather than left open. Cohorts were rebuilt 1,000 times at the observed protein-size distribution, the observed prevalence of 0.485, and a protein-level random intercept set from the outcome intraclass correlation of 0.127 measured on the real cohort, under five known population AUCs from 0.50 to 0.70. Under that one generating process the declared interval covered the truth between 93.6% and 94.9% of the time, against a nominal 95% and a Monte Carlo standard error of 0.7 percentage points. The result is specific to a parametric model with the observed cluster sizes and a random-intercept outcome; it does not establish coverage under predictor clustering, informative cluster size, or other mechanisms that were not simulated. The worst case is the null scenario, which is the one the primary estimate sits in, and it is short by 1.4 points or two Monte Carlo standard errors. A bias-corrected and accelerated interval computed on the same replicates covered between 94.2% and 95.3%, nearer nominal everywhere but by less than the Monte Carlo error at four of the five scenarios. The interval reported here is therefore close to its stated rate and slightly optimistic at the null; it is not exact.

Every point mutant in the source screen replaces the residue with alanine, and the screen includes no mutant that mimics the phosphorylated state, so loss of the side chain cannot be separated from loss of phosphoregulation. Replacing a residue at or beside a catalytic or ligand-binding residue with alanine can disrupt function through removal of the side chain alone, a bias that could inflate the association being tested. Its direction was not estimated here, so whether the design favours the hypothesis is a conditional expectation rather than something this analysis shows.

### 3.3 Limitations

**Models of single proteins.** Distances were measured in AlphaFold models of each protein on its own, and four proteins in the cohort carry annotated sites that a single chain cannot complete. The thiamine-diphosphate binding residues of PDA1 are completed by the β subunit of the pyruvate dehydrogenase E1 component. TDH3 works as a four-copy assembly, ENO1 as a two-copy assembly, and VMA2 is the V1 B subunit of the V-ATPase. No protein-by-protein check of which proteins assemble with partners was carried out, and no version of the analysis restricted to proteins with no annotated obligate partner is reported.

**A cohort selected by annotation.** A site could enter only if its protein carried a reviewed `ACT_SITE` or `BINDING` record, and that requirement is itself associated with the outcome by 16.8 percentage points (§2.1). A protein carrying no such annotation cannot enter regardless of mechanism.

**A cohort fixed after the outcome was seen.** The primary cohort was fixed by removing three sites that coincide with an annotated residue, after the outcome had been inspected, and every estimate is reported for both versions of the cohort. Reporting both discloses the choice. It does not make the version chosen after both were seen any more trustworthy. The three removed sites are PRM15 S158, annotated `ACT_SITE` "Phosphoserine intermediate", and TDH3 S149 and T151, which sit either side of the catalytic nucleophile inside a `BINDING` interval. All three carry `ECO:0000250` evidence, all three are affected, and all three sit at 0 Å. The removal is not re-grounded on that catalytic criterion here.

**Reproducibility of the outcome.** Only two sites kept more than one strain, and one of those two disagrees across its strains under the yes-or-no rule, which cannot characterize how reproducible the outcome is. Two rules for combining repeat strains are reported, along with one difference between figure versions in how the cohort cascade is drawn, and the withdrawn expanded row count of §2.1.

**The review behind this revision.** Revisions to this manuscript responded in part to simulated reviews in which every reviewer was an AI agent running on one model family. That is not peer review, and agreement among those reviewers is not independent replication. S2 Appendix records what was run and when.

### 3.4 What the analysis supports, and what a usable design would need


**Table 4. Selected results from both cohorts.** Values are AUCs — the chance an affected site ranks ahead of an unaffected one — unless the row names another quantity. Declared quantities are marked; everything else is post hoc.

| Analysis | Cohort | n | Value | 95% interval | Timing |
|---|---|---|---:|---:|---|
| Distance, primary | Yeast | 163 sites, 48 proteins | 0.527 | 0.417–0.632 | Cohort version fixed after outcome inspection |
| Distance, inclusive 0 Å | Yeast | 166, 50 proteins | 0.544 | 0.436–0.649 | Reported alongside as a check |
| **Distance, declared primary** | Human, fitness | 1,471 sites, 788 proteins; 72 affected | 0.558 | 0.474–0.637 | Endpoint declared after all candidates were known |
| **Distance, declared primary** | Human, reporter | 1,471, 788; 82 affected | 0.483 | 0.418–0.550 | Endpoint declared after all candidates were known |
| Within-protein, pair-weighted | Yeast | 112 sites, 23 proteins, 176 pairs | 0.528 | 0.368–0.709 | Post hoc |
| Within-protein, pair-weighted | Human, fitness | 132 sites, 39 proteins, 102 pairs | 0.627 | 0.452–0.768 | Post hoc |
| Within-protein, pair-weighted | Human, reporter | 215 sites, 49 proteins, 184 pairs | 0.413 | 0.313–0.510 | Post hoc |
| Within-protein, equal-protein weight | Human, reporter | 49 proteins | 0.376 | 0.266–0.489 | Post hoc |
| Minimum sequence separation | Yeast | 163 | 0.550 | 0.434–0.653 | Post hoc comparator |
| Minimum sequence separation | Human, reporter | 1,471 | 0.549 | 0.485–0.613 | Post hoc comparator |
| Difference in AUC, sequence separation minus distance, paired | Human, reporter | 1,471 | +0.066 | −0.001 to +0.131 | Post hoc; contains zero, as does every other paired difference |
| Inverse relative solvent accessibility | Yeast | 163 | 0.587 | 0.489–0.672 | Post hoc comparator |
| Inverse relative solvent accessibility | Human, fitness | 1,471 | 0.607 | 0.530–0.678 | Post hoc comparator |
| SIFT, common support | Yeast | 152 | 0.606 | 0.522–0.690 | Post hoc comparator |
| SIFT, common support | Human, fitness | 997 | 0.646 | 0.565–0.723 | Post hoc comparator |
| SIFT, common support | Human, reporter | 997 | 0.574 | 0.497–0.651 | Post hoc comparator |
| **Odds ratio** per ten-fold increase in distance + 1 Å | Yeast | 163 | 0.77 | 0.27–2.21 | Cluster covariance, t(47) |
| **Odds ratio** adjusted for pLDDT and solvent accessibility | Yeast | 163 | 1.31 | 0.37–4.66 | Cluster covariance, t(47) |
| Experimentally-evidenced targets only | Yeast | 24 sites, 7 proteins | 0.420 | 0.244–0.708 | Descriptive range on 7 proteins |
| Experimentally-evidenced targets only | Human, fitness | 512 sites, 287 proteins | 0.575 | 0.446–0.699 | Post hoc |
| Experimentally-evidenced targets only | Human, reporter | 512, 286 | 0.478 | 0.376–0.577 | Post hoc |

The two yeast cohort intervals use 200,000 protein-cluster resamples at seed 20260729; every other bootstrap interval here uses 20,000 at seed 20260728. All draws were retained except in the yeast experimental-target interval, which retained 19,991 of 20,000.

Table 4 collects the quantities this paper reports for both cohorts on one scale. What this analysis supports is specific to these two cohorts. In yeast, on 163 replaced sites in 48 proteins, the shortest heavy-atom distance to the nearest annotated active- or binding-site residue gave an AUC of 0.527 (0.417–0.632), which is 0.59 standard deviations from the centre of a null built by shuffling the labels 20,000 times (two-sided p = 0.55). The smallest gap in sequence position to an eligible annotated residue, computed on the same rows with no structure used at all, gave 0.550 (0.434–0.653); the paired difference was +0.023 (−0.049 to +0.090).

Keeping only sites where the model is confident produced no steady improvement. The eleven strata of the primary cohort run from a low of 0.416 on 41 sites to a high of 0.683 on 27, and tightening the PAE threshold moves the value up and down in both cohort versions. Keeping only targets with experimental evidence behind them left 24 of the 163 sites in 7 of the 48 proteins, so whether better annotation would change the picture cannot be asked of this design.

The cross-validation values for the four models are given descriptively below and are not ranked against each other, since no paired sampling-uncertainty comparison between them was computed. Under repeated cross-validation with proteins kept together, a five-feature model built from published annotations gave 0.590 split-averaged and 0.573 pooled out-of-fold, against 0.484 and 0.393 for distance alone, with the same ordering of models under both summaries. These estimates are post hoc, the ranges across split seeds describe how stable the answer is to how the data are divided rather than being confidence intervals, and the four models are not distinguishable at this sample size.

All of the above is bounded by these two cohorts, these definitions of an affected site, and models of single proteins. The human experiment contributes 788 protein clusters against 48, an experimental-evidence arm that retains 512 sites where the yeast design retains 24, and the finding that the across-protein architecture and the peptide-bond artefact are not particular to yeast. It does not contribute a tighter interval in any sense this paper relies on: the declared human intervals are numerically narrower than the yeast one, at widths of 0.163 and 0.132 against 0.215, but the three are built on different cohorts, outcomes and perturbation chemistries, so no precision comparison between them is made anywhere in this paper. It does not settle the question that matters biologically, which is between sites in one protein; that is unresolved in every cohort here, and the human data make it harder rather than easier, because adding proteins adds across-protein pairs faster than within-protein ones. Nor does any of it speak to phosphosite biology in general: the outcomes are yeast colony growth, human cell fitness, and reporter activity, under two perturbation chemistries, and §2.7.6 sets out where the designs diverge.

A design that could resolve the question would need structures that include a protein's partners, targets carrying experimental evidence, outcomes specific to the direction of the growth change, and sites concentrated within 15 Å of a target. No projection of the required cohort size is given here, because it inherits the coverage question the cluster bootstrap leaves open.

The derived cohort table is an output of this work: 163 replaced sites with resolved coordinates, the distance to and identity of the nearest target, evidence codes, model-confidence values and screen outcomes, deposited with the 22-sheet supplement.

## 4. Methods

### 4.1 Design, chronology, and what is post hoc

This is an exploratory reanalysis of data others have published. Nothing was registered in advance and no analysis here is confirmatory. The yes-or-no outcome and the nearest-target distance were both defined before the first AUC was computed. Everything else was specified after that result had been inspected: the protein-cluster intervals, the model-confidence strata, the alternative definitions of the distance feature, the continuous outcomes, the SIFT comparison, the combined models, and the within-protein and residue-class analyses. The declared post hoc families are listed in §2.2, and the round-2 analyses of §4.6 are labelled post hoc wherever their values appear.

A later methods review identified five defects in the first cohort build: Supplementary Data 6 was being used to decide which sites were eligible; sites coinciding with an annotated target had no settled treatment; the HOG1 coordinate conflicted between workbook and article; repeat strains had not been combined; and a two-proportion power calculation was invalid. We rebuilt the cohort, averaged the profiles of repeat strains, and removed the power and negative-binomial claims. The decision to drop target-coincident sites from the primary analysis was made after the outcome had been inspected, so the inclusive cohort, which keeps them at their literal distance, is reported alongside throughout as a named check.

### 4.2 Source data and cohort construction

Four supplementary workbooks from Viéitez et al. [1] were obtained from Europe PMC record PMC7612524. Supplementary Data 1 defines the point-mutant constructs. Supplementary Data 3 gives the S-scores and q-values condition by condition, where the S-score measures how much better or worse a strain grew than expected. Supplementary Data 8 holds the sequencing quality-control notes and the phosphomutant records reported to correlate with scar controls. Supplementary Data 6 was used only for annotations: SIFT, disorder, domain membership, evolutionary age and phenotype-group labels.

Point-mutant rows were matched from yeast systematic gene names to reviewed budding-yeast (*Saccharomyces cerevisiae*) UniProt entries by ordered-locus name, and the wild-type residue stated in the workbook had to match the reviewed sequence. Two records carry a HOG1 label. PBY107 is labelled T178A in Supplementary Data 1; the source article names T174A as the regulatory control and T174 matches the reviewed sequence, so it is analysed at T174, with a named check that drops it. S178 and T179 were compatible alternatives and were not adopted. PBY131 carries the T174A label in Supplementary Data 8 and was removed by the sequencing-note exclusion, so no analysed record carries that label. No other mismatch was shifted.

A record had to have a growth profile in Supplementary Data 3, and was excluded if it carried any text in the Supplementary Data 8 sequencing note or appeared exactly in that file's scar-correlation table. As implemented, the rule reads the free-text note only. The numeric columns recording secondary variants and the copy-number flag were not used, and no eligible strain record carries any text in the note (§2.1).

This reanalysis reverses the selection role one source file is stated to have, and overrides one source coordinate. The source screen's authors were not consulted, and no endorsement by them is claimed or implied.

### 4.3 The outcome, the rule for repeat strains, and the variant definitions

The source's yes-or-no outcome is `qvalue < 0.05` in at least one condition the strain was measured in, whatever the sign of the S-score. For each strain we counted the conditions meeting that test, and a site counted as affected when its count, averaged over repeat strains, was above zero. Because those counts are never negative, this is in effect a rule that one qualifying strain is enough, not a rule that all strains must agree. The all-strains-must-agree (`all`) rule is reported as a check and changes one published label (§2.5).

The number of conditions behind a site is not the same for every site (§2.1). The source q-values are computed within each condition across strains, so the false-discovery rate is controlled within a condition, not within a strain across the panel.

Two stricter definitions require at least 2 and at least 3 called conditions; raising the threshold moves sites from affected to unaffected without deleting rows, so the number of sites is unchanged. Two direction-specific definitions apply the per-strain tests `qvalue < 0.05 AND Score < 0` (worse growth) and `qvalue < 0.05 AND Score > 0` (better growth). All four were built from a condition-by-condition table of 17,214 strain–condition rows covering 169 strains, 166 replaced sites and 102 conditions. Rebuilding the either-direction label through that table reproduces the published label on all 166 rows.

### 4.4 Annotations and structures

The reviewed yeast proteome and its UniProt annotations were retrieved through the UniProt REST API on 29 July 2026; the response reported release 2026_02, dated 10 June 2026 [12]. The target set is the Active site (`ACT_SITE`) and Binding site (`BINDING`) records of reviewed entries, with `Site` and `DNA binding` records excluded (§2.1). That release documents the merge of the former `NP_BIND`, `METAL` and `CA_BIND` types into `BINDING`, so one `BINDING` record may describe a nucleotide, a metal or a calcium interaction [12]. Evidence codes were kept but were not used to decide eligibility, so an entry being reviewed does not mean any particular annotation on it has experimental support. Records covering several residues were expanded to one row per covered residue. `ACT_SITE` covers a single residue everywhere in this data, so the expansion affects `BINDING` only; the resulting counts are in §2.1.

Structures were AlphaFold DB entry version 6, which are AlphaFold2 predictions of each protein on its own (monomer v2.0) [13,14], cached with model metadata, predicted-aligned-error files, source URLs and SHA-256 hashes. Automated checks compared sequences, residue numbering, version fields and predicted-aligned-error matrix dimensions across the UniProt, AlphaFold and mmCIF records before any distance was measured, and stopped the analysis on any mismatch.

pLDDT for the site and for its nearest target is the mean atom B factor stored in the mmCIF, read as the model's local confidence and not as a measurement of disorder, though regions of low pLDDT are frequently intrinsically disordered [15,16]. Relative solvent accessibility was computed on the protein alone as Shrake–Rupley solvent-accessible surface area [17] divided by the per-residue maxima of Tien et al. [18]. Both directions of the predicted aligned error were kept for the nearest site–target pair. Following the AlphaFold DB definition, the entry at row *i*, column *j* is the expected positional error at residue *j* when the prediction is aligned on residue *i*; `pae_site_to_target` therefore takes *i* = site, *j* = target, as the supplementary PAE table header states. `pae_pair_max`, used for the declared PAE strata, is the larger of the two.

### 4.5 Predictor and statistical analysis

The predictor was the shortest straight-line distance between any non-hydrogen atom of the replaced residue and any non-hydrogen atom of an eligible target residue. It was not restricted to the oxygen that accepts the phosphate, no phosphate was modelled, backbone and side-chain geometry were not separated, and the two residues were not required to lie in the same folded domain. No minimum separation along the sequence was imposed. Sites that are themselves an eligible target residue were excluded from the primary cohort; their distance to themselves of 0 Å appears only in the inclusive version.

The unit of analysis was one distinct amino-acid substitution, and shorter distance was scored toward the affected label. The headline quantity is the AUC on the primary cohort with every site weighted equally. The designated within-protein quantity is the AUC over proteins carrying both affected and unaffected sites with every pair weighted equally; the version weighting every protein equally is reported as a check.

Intervals are 95% percentile bootstraps that resample the 48 UniProt entries, keeping every site of a protein whenever that protein is drawn. The two main cohort intervals use 200,000 resamples at seed 20260729. Checks run after the primary result use 20,000 resamples at seed 20260728, rank-correlation intervals for the continuous outcomes use 4,000, and the adjusted linear-probability check uses 9,999 Rademacher wild-cluster draws. A resample counts only if both affected and unaffected sites survive in it, and percentiles are taken over the ones that do, so the number retained is stated wherever it fell below the nominal count; both main cohort intervals retained all 200,000. No interval is reported for an estimate whose bootstrap endpoint reaches 0 or 1; the point estimate, its n and the discarded fraction are given instead. Retention for the 11 clustered rank-correlation intervals is undocumented and is not asserted.

Logistic models used log10(distance + 1), with standard errors that allow sites in the same protein to be correlated, and a t distribution with 47 degrees of freedom in place of the normal reference, giving a critical value of 2.0117 against 1.9600. The descriptive cut-offs of 5, 8, 10 and 15 Å were fixed after the primary outcome was inspected, and the groups they define are nested inside one another rather than being independent threshold tests. Two nulls of 20,000 label shuffles each were computed, one shuffling across the whole cohort and one shuffling only within a protein. The within-protein null holds the between-protein pairs fixed and is centred above 0.5, so its p-value is measured from its own centre. No unclustered Mann–Whitney or Fisher test was used for inference, and no power calculation is reported.

### 4.6 Round-2 analyses, software, and reproducibility

The eight round-2 analyses were run outside the frozen analysis tree. Each one checks the three frozen input hashes before computing anything, imports the frozen estimators from `phase0_5/src/02_phase0_5_analysis.py` rather than reimplementing them, and writes nothing into the frozen tree. Every value they produce is post hoc.

The frozen software environment was CPython 3.12.4 with NumPy 1.26.4, pandas 2.2.2, SciPy 1.13.1, scikit-learn 1.4.2 [19], statsmodels 0.14.2 and Biopython 1.85, with the full set of dependencies pinned in `requirements-lock.txt`. Automated checks verified how the cohort was built, that the outcome could be rebuilt from the condition-level data, that structures and predicted-aligned-error files were complete, that the distances were computed as specified, that outputs had the expected dimensions, and that the numerical outputs, figures and text agree. All passed before the manuscript was prepared.

A rerun in a clean environment by the same authors confirmed that the computations reproduce. That is not independent replication and not independent review.

`NUMBERS.md`, deposited with the analysis materials, is the numerical authority for this manuscript: every value reported here is declared there, and values it does not declare are not reported.

### 4.7 The human replication cohort

Sites, guide assignments and per-site screen statistics come from the Supplementary Tables of Kennedy et al. [20], retrieved from the publisher and verified against Europe PMC record PMC11804830. UniProt `ACT_SITE` and `BINDING` features were expanded over their recorded ranges and AlphaFold DB v6 monomer models retrieved, following the same procedure as the yeast cohort but through a separate builder; distance is the same minimum heavy-atom separation, with the substituted residue excluded from its own target set — which is not the yeast rule, where a site coinciding with a target is removed instead. The human builder does not carry the yeast builder's sequence and model-version checks, and the table it starts from has no generator in the deposited materials, so this cohort cannot at present be rebuilt end to end from source. Sites were kept when the model reproduced the reviewed sequence at that position and the protein carried at least one eligible annotated residue, leaving 1,471 sites in 788 proteins.

The cohort cascade runs 7,425 rows in the source phosphosite table, to 6,968 with a parsable serine, threonine or tyrosine position, to 6,907 mapping to exactly one reviewed UniProt entry, to 6,113 whose residue matches the canonical sequence at that position, to 1,590 sites in 812 proteins carrying at least one eligible annotated residue, to **1,471 sites in 788 proteins** with a distance. A gene symbol matching more than one reviewed human entry is dropped rather than assigned, which removes 8 of the 1,595 sites an earlier build retained; one of those, TKT S308, had been assigned to an entry for a different protein. Guides are aggregated to the site they target: a site enters once, and where several guides name the same site the screen's own per-site summary is used rather than a guide-level average. Sites edited by more than one guide, and guides producing bystander edits at neighbouring residues, are retained in the primary cohorts and separated in the single-edit arm of §2.7.5. Both screens analysed here use the adenine base editor ABE8e. Editor identity is recorded per guide and used only in the substitution-class arms; it does not enter the primary.

The two screens are analysed separately and each supplies its own declared outcome: a site counts as affected in a screen when twice the smaller of that screen's two one-sided MAGeCK gene-level p-values is below 0.05, with that minimum reconstructed from the two directional columns of the source `gene_summary` sheet rather than taken from the released per-site column. The doubling corrects the two directions MAGeCK reports inside a screen; keeping the screens apart leaves no union to correct. §2.7 records that the released column does not reproduce the reconstructed minimum on 47 fitness rows and 100 reporter rows, which is why the endpoint is built from the directional columns. The first version of this analysis pooled the two screens at an uncorrected 0.05 and is withdrawn; that arm and the six other candidate definitions are reported in Table 2, and the numerical authority marks the declaration as post hoc.

Intervals use the same protein-cluster percentile bootstrap at 20,000 resamples and seed 20260728, with the estimator imported from the yeast analysis module rather than reimplemented, so the two cohorts share an estimator even though they do not share a cohort builder. Every interval reported for this cohort retained all 20,000 resamples.

### 4.8 Ethics

This secondary computational analysis used public data only: a yeast growth screen and two published human cell-line screens in Jurkat-lineage cells. No participant-level data and no human specimens were analysed, and no human-participant or animal-subject approval was required.

### 4.9 Use of AI tools

We disclose that data exploration, data analysis, and manuscript writing were supported by AI-based tools.
The authors take full responsibility for the data, code, analyses, conclusions, and writing.

The tools were large language models used through Anthropic's Claude Code interface between 2026-07 and 2026-08. Their outputs were used for prose drafting, code drafting, literature search and adversarial review of the authors' own claims. Every number reported in this manuscript was recomputed from the deposited code and checked against the numerical authority before it was written, and several claims produced with that assistance were retracted on recomputation; those retractions are recorded in the analysis materials. The authors take responsibility for the accuracy of all content, and the interpretations and conclusions are their own.

## Data and code availability

The source screen is available with Viéitez et al. [1] through Europe PMC record PMC7612524. The four workbooks are not redistributed; the workflow retrieves them and verifies their inner-file hashes. The materials prepared for deposition are the derived cohort-disposition table, an output of this work, the analysis and round-2 code, the supplementary workbook, manifests, and versions and SHA-256 hashes for the UniProt and AlphaFold DB inputs. `NUMBERS.md` is deposited with them and is the numerical authority for every value reported here. Stored cohort intervals were reused in every reader-facing table and figure rather than recomputed at build time. The code and derived data are at https://github.com/kyle-nguyen-git/phosphosite-proximity. No archive DOI has been minted yet, so cite the repository and commit rather than a DOI.

The human cohort draws on Supplementary Tables 3 and 4 of Kennedy et al. [20] — the `Phosphosites` and `MAGeCK gene_summary` sheets of each — and on the `annotated_phosphoproteome` and `known_regulatory_PSP` sheets of the Ochoa et al. [3] Supplementary Table 2, from which twelve named feature columns were read. Neither workbook is redistributed. The derived human cohort table, the scripts that build and analyse it, and the result files are deposited with the analysis materials. The candidate table the human build starts from is generated by `build_candidate_table.py`, which reads the two `Phosphosites` sheets, resolves each gene symbol against UniProt, checks the residue against the canonical sequence and applies the annotation filter; it reproduces 1,587 of the 1,595 rows of an earlier build, and the eight differences are gene symbols matching more than one reviewed entry. One limit remains recorded rather than worked around: the human builder does not carry the model-version assertions the yeast builder applies, so the deposited AlphaFold cache rather than a version check is the authority for which models were used.
## Acknowledgements

The authors thank Viéitez and colleagues for making the yeast phosphomutant screen and its supplementary data available, and Kennedy and colleagues for the human base-editor screens and their supplementary tables.

## References

1. Viéitez C, Busby BP, Ochoa D, Mateus A, Memon D, Galardini M, et al. High-throughput functional characterization of protein phosphorylation sites in yeast. Nat Biotechnol. 2022;40: 382-390. doi: 10.1038/s41587-021-01051-x
2. Strumillo MJ, Oplová M, Viéitez C, Ochoa D, Shahraz M, Busby BP, et al. Conserved phosphorylation hotspots in eukaryotic protein domain families. Nat Commun. 2019;10: 1977. doi: 10.1038/s41467-019-09952-x
3. Ochoa D, Jarnuczak AF, Viéitez C, Gehre M, Soucheray M, Mateus A, et al. The functional landscape of the human phosphoproteome. Nat Biotechnol. 2020;38: 365-373. doi: 10.1038/s41587-019-0344-3
4. Bludau I, Willems S, Zeng WF, Strauss MT, Hansen FM, Tanzer MC, et al. The structural context of posttranslational modifications at a proteome-wide scale. PLoS Biol. 2022;20: e3001636. doi: 10.1371/journal.pbio.3001636
5. Minguez P, Letunic I, Parca L, Garcia-Alonso L, Dopazo J, Huerta-Cepas J, et al. PTMcode v2: a resource for functional associations of post-translational modifications within and between proteins. Nucleic Acids Res. 2015;43: D494–D502. doi: 10.1093/nar/gku1081
6. Stephenson JD, Totoo P, Burke DF, Jänes J, Beltrao P, Martin MJ. ProtVar: mapping and contextualizing human missense variation. Nucleic Acids Res. 2024;52: W140–W147. doi: 10.1093/nar/gkae413
7. Niu B, Scott AD, Sengupta S, Bailey MH, Batra P, Ning J, et al. Protein-structure-guided discovery of functional mutations across 19 cancer types. Nat Genet. 2016;48: 827–837. doi: 10.1038/ng.3586
8. Beltrao P, Albanèse V, Kenner LR, Swaney DL, Burlingame A, Villén J, et al. Systematic functional prioritization of protein posttranslational modifications. Cell. 2012;150: 413–425. doi: 10.1016/j.cell.2012.05.036
9. Nishi H, Hashimoto K, Panchenko AR. Phosphorylation in protein-protein binding: effect on stability and function. Structure. 2011;19: 1807–1815. doi: 10.1016/j.str.2011.09.021
10. Evans R, O'Neill M, Pritzel A, Antropova N, Senior A, Green T, et al. Protein complex prediction with AlphaFold-Multimer. bioRxiv 463034 [Preprint]. 2021 Oct 4 [revised 2022 Mar 10; cited 2026 Aug 14]. Available from: https://doi.org/10.1101/2021.10.04.463034
11. Ng PC, Henikoff S. SIFT: predicting amino acid changes that affect protein function. Nucleic Acids Res. 2003;31: 3812–3814. doi: 10.1093/nar/gkg509
12. UniProt Consortium. UniProt: the Universal Protein Knowledgebase in 2023. Nucleic Acids Res. 2023;51: D523–D531. doi: 10.1093/nar/gkac1052
13. Jumper J, Evans R, Pritzel A, Green T, Figurnov M, Ronneberger O, et al. Highly accurate protein structure prediction with AlphaFold. Nature. 2021;596: 583–589. doi: 10.1038/s41586-021-03819-2
14. Varadi M, Bertoni D, Magana P, Paramval U, Pidruchna I, Radhakrishnan M, et al. AlphaFold Protein Structure Database in 2024: providing structure coverage for over 214 million protein sequences. Nucleic Acids Res. 2024;52: D368–D375. doi: 10.1093/nar/gkad1011
15. Terwilliger TC, Liebschner D, Croll TI, Williams CJ, McCoy AJ, Poon BK, et al. AlphaFold predictions are valuable hypotheses and accelerate but do not replace experimental structure determination. Nat Methods. 2024;21: 110–116. doi: 10.1038/s41592-023-02087-4
16. Ruff KM, Pappu RV. AlphaFold and implications for intrinsically disordered proteins. J Mol Biol. 2021;433: 167208. doi: 10.1016/j.jmb.2021.167208
17. Shrake A, Rupley JA. Environment and exposure to solvent of protein atoms. Lysozyme and insulin. J Mol Biol. 1973;79: 351–371. doi: 10.1016/0022-2836(73)90011-9
18. Tien MZ, Meyer AG, Sydykova DK, Spielman SJ, Wilke CO. Maximum allowed solvent accessibilities of residues in proteins. PLoS One. 2013;8: e80635. doi: 10.1371/journal.pone.0080635
19. Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, et al. Scikit-learn: machine learning in Python. J Mach Learn Res. 2011;12: 2825–2830.
20. Kennedy PH, Alborzian Deh Sheikh A, Balakar M, Jones AC, Olive ME, Hegde M, et al. Post-translational modification-centric base editor screens to assess phosphorylation site functionality in high throughput. Nat Methods. 2024;21: 1033–1043. doi: 10.1038/s41592-024-02256-z
21. Correa Marrero M, Mello VH, Sartori P, Beltrao P. Global comparative structural analysis of responses to protein phosphorylation. Nat Commun. 2025;16: 9407. doi: 10.1038/s41467-025-64116-4
22. Li Y, Xu T, Ma H, Yue D, Lamao Q, Liu Y, et al. Functional profiling of serine, threonine and tyrosine sites. Nat Chem Biol. 2025;21: 532–543. doi: 10.1038/s41589-024-01731-0

## Supporting information

Captions only. Each item is uploaded as its own file, as PLOS ONE requires.

**S1 Appendix.** Annotation records, residue expansion, and a withdrawn count. The record-to-residue expansion behind the 560-residue target set, the duplicate-removal rules giving 565 and 566 rows, the source of the excess over 560, and an earlier expanded row count that does not reproduce and is withdrawn.

**S1 Fig.** The eleven-stratum confidence family, drawn. Primary and inclusive arms across eleven model-confidence strata, from 163 sites down to 27. All post hoc.

**S2 Fig.** Cohort, residue-class and feature-definition checks. Cohort versions, residue classes, alternative distance-feature definitions, and the post hoc SIFT comparator on common support, on one scale. All post hoc.

**S1 Table.** The eleven-stratum confidence family, tabulated. Both cohort versions across every stratum, with sites and intervals. All post hoc.

**S2 Appendix.** The simulated reviews. What was run, what it produced, and the statement that none of it is peer review.

**S2 Table.** The 72-cell confidence-by-predicted-aligned-error grids. Four summaries at 10 Å; the 72 primary-cohort cells run from 0.416 to 0.569.
