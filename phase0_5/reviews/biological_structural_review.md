# Biological and Structural Adversarial Review

> **Review status:** AI-assisted internal adversarial review. This is **not independent peer review**, external methods review, or biological validation.

> **Post-review serialization addendum:** A later clean-environment run canonicalized last-bit
> continuous-model fields and refroze the Phase 0.5 JSON without changing any reported value. Use the
> current `NUMBERS.md` header, not the historical hash quoted below; see `RESPONSE_LOG.md`.

## Scope and Numerical Authority

This review is confined to the public-data Fulbright project in `outputs/fulbright/research/phase0_calibration`. It does not use Einstein or NYU evidence. It audits biological construct validity, annotation-coincident substitutions, the UniProt target definition, AlphaFold monomer geometry, pLDDT/PAE interpretation, residue and feature sensitivities, the growth-phenotype proxy, and mechanistic claim scope.

`NUMBERS.md` was read before numerical review and is the sole numerical authority. Its three frozen hashes were recomputed before any project number was used:

| Frozen file | SHA-256 in `NUMBERS.md` | Recomputed status |
|---|---|---|
| `results/statistics.json` | `57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401` | Match |
| `results/analysis_final.csv` | `e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4` | Match |
| `phase0_5/results/phase0_5_statistics.json` | `569a3c5eab309e3ac3572d84718ce8b59ad3bd0762ed9d085aeafb6584f2e3e9` | Match |

The audited numerical baseline is therefore the exclusion-primary cohort, **n=163, AUC 0.527 [0.417, 0.632]**, with the named inclusive sensitivity, **n=166, AUC 0.544 [0.436, 0.649]**, exactly as specified in `NUMBERS.md` sections 1–3.

## Overall Assessment

No surviving biological or structural error was found that makes the narrow reported estimand internally uninterpretable. The manuscript is explicit that it evaluates one retrospective, annotation-selected, monomeric residue-distance heuristic against a direction-agnostic mutant-growth label. It does not establish phosphorylation dependence, causal mechanism, a universal distance cutoff, or lack of information in distance.

Important construct limitations remain. They do not reverse the frozen result, but they should be resolved or made more explicit before the work is represented as a biological calibration rather than a calibration to a particular computational annotation definition.

Severity in this report is defined as follows: **blocking** means that the implemented estimand or central claim is biologically invalid without correction or new analysis; **major** means that a central construct or release claim needs revision while the frozen estimate remains interpretable for the implemented estimand; **minor** means a bounded terminology or secondary-method issue; **passed** means the relevant claim is supported and appropriately scoped.

## Blocking Findings

**None identified.**

This conclusion is conditional on retaining the current narrow claims. Promoting the result to a statement about phosphosite mechanism, experimentally verified functional residues, native complexes, or phosphorylation-dependent function would create a blocker unsupported by the present design.

## Major Findings

### M1 — The UniProt target is a heterogeneous coordinate union, not a uniform set of experimentally established functional residues

**Finding.** The primary target includes every expanded coordinate from UniProt `Active site` and `Binding site` features without filtering by evidence code, evidence source, ligand class, point-versus-range status, or experimental support. Range features are expanded into individual target residues. The distance calculation then treats all resulting coordinates equivalently.

**Why it matters.** “Distance to an annotated functional residue” can be read more strongly than the implemented construct. A point catalytic residue supported by direct structural evidence, a motif-like binding interval transferred from another protein, and a feature with blank evidence fields all enter the same target union. This heterogeneity can change both cohort eligibility and nearest-target rank. It also affects what “annotation-coincident” means: the TDH3 overlaps arise from expansion of a binding interval, whereas PRM15 S158 has both point and interval annotations. `NUMBERS.md` section 2 records that all three coincident substitutions carry ECO:0000250 evidence.

**Exact file evidence.**

- `src/01_build_sites.py:50-51` defines the core set as all `Active site` and `Binding site` records.
- `src/01_build_sites.py:129-170` preserves evidence metadata but expands every start-to-end interval without an evidence filter.
- `src/01_build_sites.py:326-375` creates eligibility and `is_itself_annot` from that expanded coordinate set.
- `results/uniprot_features_detailed.csv:7` is the TDH3 binding interval underlying TDH3 S149 and T151; rows `260`, `263`, and `264` contain the PRM15 S158 point/range records. These rows carry ECO:0000250.
- `results/uniprot_features_detailed.csv:154` contains a core active-site record for `KAPA_YEAST` with blank evidence fields, confirming that evidence presence is not an eligibility requirement.
- `manuscript/preprint_draft_v1.md:85` acknowledges ligand/evidence heterogeneity and interval features, but the abstract at line `11` still uses the more biological phrase “annotated functional residue.”

**Required resolution.** At minimum, define the predictor everywhere as distance to an **expanded UniProt ACT_SITE/BINDING coordinate** and state that reviewed entry status does not imply direct experimental support for every feature. For a stronger biological claim, add a feature-evidence table and sensitivities separating point from interval features and direct PDB/PubMed-supported annotations from transferred or missing-evidence annotations. The broader SITE/DNA-binding sensitivity should also be described as conditional on the original core-eligible cohort: `phase0_5/src/01_build_phase0_5_dataset.py:212-218` starts from the already core-selected inclusive table, so it does not test re-eligibility of proteins lacking ACT_SITE/BINDING.

### M2 — The distance is an any-heavy-atom residue distance, not a phosphoacceptor- or phosphate-specific geometry

**Finding.** The structural predictor is the minimum over every heavy atom in the wild-type S/T/Y residue and every heavy atom in a target residue. It does not use the phosphoacceptor oxygen, model a phosphate, distinguish backbone from side-chain contact, or separate tertiary proximity from trivial local sequence adjacency.

**Why it matters.** A short minimum can be driven by backbone packing or by residues neighboring an expanded annotation interval in primary sequence. That is a legitimate residue-proximity metric, but it is not a direct measure of phosphate-to-active-site geometry or a mechanism-specific interaction. The current feature-definition sensitivities change annotation classes, not the atom definition or sequence-separation contribution.

**Exact file evidence.**

- `src/02_structures.py:105-120` minimizes over all heavy-atom pairs.
- `phase0_5/src/01_build_phase0_5_dataset.py:83-103` independently implements the same rule.
- `manuscript/preprint_draft_v1.md:115` accurately discloses “any heavy atom,” while lines `21` and `79` disclose absence of phosphorylation and other native-state components.
- `phase0_5/src/02_phase0_5_analysis.py:723-751` varies feature classes but contains no phosphoacceptor-atom, Cα, or sequence-neighbor sensitivity.

**Required resolution.** Keep conclusions explicitly attached to “minimum residue–residue heavy-atom distance.” If the manuscript is to discuss phosphosite geometry more generally, add oxygen-specific or Cα sensitivity and a sequence-separation analysis. Otherwise, add a direct limitation that small values need not represent phosphate-mediated contact.

### M3 — The growth label pools effect direction, condition, and replicate consistency

**Finding.** Outcome positivity is based on whether any source q-value crosses the threshold, independent of the sign of the associated growth score. Counts are averaged across replicate strains and then thresholded above zero; because the counts are nonnegative, this is logically an “at least one replicate has at least one called condition” rule rather than a replicate-consistency rule. The continuous sensitivity family uses significance strength or unsigned score magnitude and therefore does not recover growth direction.

**Why it matters.** Growth-enhancing and growth-impairing responses can arise through different biology but receive the same positive label. A call confined to one condition or one replicate is also treated as evidence of detectable perturbation. The estimand is valid as a screen-detectability endpoint, but it is not a homogeneous functional mechanism and cannot be interpreted as loss of phosphorylation-dependent activity.

**Exact file evidence.**

- `src/01_build_sites.py:236-253` counts calls at the configured source `qvalue` threshold without using the sign of `Score`.
- `src/01_build_sites.py:321-323` creates `has_pheno` from a positive count.
- `src/01_build_sites.py:342-371` averages replicate counts and then thresholds the mean above zero.
- `phase0_5/src/01_build_phase0_5_dataset.py:137-181` preserves signed condition scores, but `phase0_5/src/02_phase0_5_analysis.py:828-835` analyzes phenotype count, minimum-q evidence, RMS, mean absolute score, and maximum absolute score rather than signed gain/loss outcomes.
- `manuscript/preprint_draft_v1.md:83` correctly calls the outcome a proxy and rejects direct phosphorylation-function interpretation, but it does not explicitly say that opposing growth directions are pooled.

**Required resolution.** Name the endpoint “direction-agnostic any-condition screen phenotype” in the abstract and Methods. A signed gain/loss analysis and a replicate-consistency sensitivity would strengthen biological interpretation, but they should remain post-result exploratory analyses.

### M4 — Current AlphaFold artifacts support the v6-monomer claim, but the retrieval and mapping checks do not fail closed

**Finding.** The current local manifest and mmCIF metadata support the stated AlphaFold DB v6 monomer provenance. The rerun code, however, accepts any existing unversioned CIF above a size threshold and otherwise follows the API’s current `cifUrl`. PAE retrieval similarly uses `latestVersion`. The PAE matrix is indexed as UniProt position minus one. The manuscript says sequence identity and numbering were checked, but the coordinate code checks the substituted residue rather than implementing a full model-to-UniProt sequence equality assertion.

**Why it matters.** A future clean-room run after an AlphaFold update, or a mismatched cached CIF/PAE pair, could silently change geometry while still appearing complete. This does not invalidate the present frozen artifacts, but it is a structural provenance gap for reproducible release.

**Exact file evidence.**

- `src/02_structures.py:30-49` uses an unversioned cache path and the current API URL.
- `src/02_structures.py:96-103` checks target availability and the substituted residue identity, not full sequence equality.
- `phase0_5/src/01_build_phase0_5_dataset.py:106-134` obtains `latestVersion`; lines `335-345` index PAE directly by sequence position.
- `phase0_5/results/alphafold_pae_manifest.csv` records current model version, monomer status, sequence bounds, URLs, and cached hashes; representative mmCIF file `data/af/P00359.cif` contains the v6 repository history.
- `phase0_5/src/04_verify_release.py:262-270` checks completeness and the stored version column but does not parse the CIF version, compare full sequences, or validate PAE dimensions against the model sequence.
- `manuscript/preprint_draft_v1.md:113` makes the broader sequence-identity claim.

**Required resolution.** Pin exact v6 URLs and hashes, verify the cached CIF’s internal release/version against the manifest, compare full UniProt/metadata/model sequences and bounds, validate PAE dimensions, and make these fail-closed verifier checks. Until then, narrow the Methods wording to the checks actually executed.

## Minor Findings

### m1 — pLDDT should not be labeled a disorder proxy

`src/02_structures.py:4-5` calls site pLDDT an “AlphaFold confidence, used as the disorder proxy.” Low pLDDT can arise for several reasons and is not equivalent to experimentally established disorder. The manuscript is more careful at lines `21`, `45-51`, and `81`, and the separate source DISOPRED annotation is available in Phase 0.5. Keep pLDDT labeled as model-local confidence only.

### m2 — Pair-confidence strata are conditional on the coordinate-selected nearest target

`phase0_5/src/01_build_phase0_5_dataset.py:324-345` first selects the nearest target by the predicted coordinates and then assigns that pair’s PAE. Confidence filtering does not reselect among alternative annotated targets. This is acceptable for a sensitivity of the declared predictor, but the strata should not be described as finding the nearest well-supported biological target.

### m3 — Monomer RSA is an apo-prediction covariate

`src/02_structures.py:89-127` computes solvent exposure on the isolated AlphaFold monomer. Interfaces, ligands, membranes, and conformational states can change exposure. RSA is used only as an adjustment/predictive feature, so this is not a primary-result blocker, but it should inherit the same monomer-state caveat as distance.

## Passed Checks

- **Annotation-coincident estimand:** PASS. `NUMBERS.md` sections 1–3, `src/03_analysis.py:29-30` and `74-95`, `phase0_5/ANALYSIS_PROVENANCE.md:34-40`, and the manuscript abstract/results/methods consistently define exclusion-primary and inclusive-at-zero sensitivity arms. The post-outcome decision and the fact that all coincident substitutions are outcome-positive are disclosed.
- **AlphaFold monomer limitations:** PASS. `manuscript/preprint_draft_v1.md:21`, `79`, `89`, `113-115`, and `196-198` state that ligands, complexes/partners, phosphorylation, alternative conformations, interfaces, and cellular context are absent or outside the predictor.
- **pLDDT/PAE interpretation:** PASS with the minor terminology note above. `phase0_5/ANALYSIS_PROVENANCE.md:48-54`, `phase0_5/RESULTS.md:9-39`, and `manuscript/preprint_draft_v1.md:45-53`, `81`, and `125` name `pae_pair_max`, display the full sensitivity family, reject a monotonic confidence trend, and do not promote the most favorable or least favorable cell as a result.
- **Residue sensitivity:** PASS. `NUMBERS.md` section 12 and `manuscript/preprint_draft_v1.md:55-59`, `83`, and `125` report the residue-class analyses as post-result and explicitly warn that tyrosine-to-alanine chemistry and sparse support prevent a mechanistic interpretation.
- **Feature sensitivity:** PASS for transparency, subject to M1. The ACT_SITE, BINDING, union, SITE, and DNA-binding definitions are emitted and described as post-result; no definition is promoted as preferred.
- **Growth proxy boundary:** PASS, subject to M3. `manuscript/preprint_draft_v1.md:11`, `83`, `103-105`, and `196` state that the label is a source q-value-based alanine-mutant growth proxy and not direct measurement of occupancy, catalysis, or phosphorylation-dependent function.
- **Mechanistic restraint:** PASS. The abstract and Discussion repeatedly limit inference to one monomeric distance heuristic. The manuscript explicitly rejects “distance is uninformative,” SIFT superiority, causal phosphorylation claims, and universal cutoff validity (`manuscript/preprint_draft_v1.md:11`, `75-89`).
- **Annotation-selected generalizability:** PASS. `manuscript/preprint_draft_v1.md:85` states that proteins lacking eligible annotations cannot enter and that the analysis does not establish external representativeness.
- **Current structural artifact provenance:** PASS for the frozen local state. The AlphaFold manifest retains version, monomer flag, bounds, URLs, and hashes, while `NUMBERS.md` and the release verifier bind the numerical artifacts. M4 concerns future fail-closed reproduction, not evidence that the current files are from a different model class.

## Release Interpretation

The biological result can be presented as a transparent weak-and-imprecise calibration of one explicitly defined computational heuristic. It should not be presented as validation or refutation of structural regulation in general. M1–M3 warrant manuscript-level clarification; M4 should be resolved as part of the clean-room release work. Evidence- and atom-definition sensitivities would materially strengthen a journal submission.

This report may be supplied to an external reviewer as an internal checklist, but it does not satisfy the manuscript’s requirement for independent methods or peer review.
