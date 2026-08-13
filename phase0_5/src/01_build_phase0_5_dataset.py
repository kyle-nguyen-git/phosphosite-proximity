"""Build the enriched Phase 0.5 analysis table.

This script starts from the full inclusive Phase 0 sensitivity table so both the
exclude-primary and inclusive-sensitivity cohorts can be emitted from one enriched dataset. It adds:

* raw 102-condition S-score summaries from Viéitez Supplementary Data 3;
* independent annotations from Supplementary Data 6;
* the paper's WGS and scar-control quality flags from Supplementary Data 8;
* distances under five pre-specified UniProt feature definitions;
* pLDDT at the nearest core target and AlphaFold pairwise PAE.

AlphaFold metadata and PAE documents are cached as versioned, gzip-compressed JSON.
No Einstein, NYU, or unpublished laboratory data are read.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from Bio.PDB import MMCIFParser
from Bio.PDB.Polypeptide import protein_letters_3to1


HERE = Path(__file__).resolve().parents[1]
PARENT = HERE.parent
DATA = HERE / "data"
PAE_DIR = DATA / "pae"
RESULTS = HERE / "results"
PARENT_DATA = PARENT / "data"
PARENT_RESULTS = PARENT / "results"

PAE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api/prediction/{acc}"
FEATURE_SETS = {
    "act_site": {"Active site"},
    "binding": {"Binding site"},
    "core": {"Active site", "Binding site"},
    "core_plus_site": {"Active site", "Binding site", "Site"},
    "all_with_dna_bind": {"Active site", "Binding site", "Site", "DNA binding"},
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def residue_atoms(structure):
    """Map sequence position to one-letter residue, heavy atoms, and mean pLDDT."""
    out = {}
    for residue in structure[0].get_residues():
        if residue.id[0] != " ":
            continue
        atoms = [atom for atom in residue if atom.element != "H"]
        if not atoms:
            continue
        try:
            aa = protein_letters_3to1[residue.get_resname()]
        except KeyError:
            continue
        out[int(residue.id[1])] = (
            aa,
            atoms,
            float(np.mean([atom.get_bfactor() for atom in atoms])),
        )
    return out


def closest_target(site_pos: int, residues: dict, targets: list[int]):
    """Return minimum heavy-atom distance and nearest target position."""
    if site_pos not in residues:
        return np.nan, np.nan
    if site_pos in targets:
        return 0.0, int(site_pos)
    site_atoms = residues[site_pos][1]
    best = np.inf
    nearest = np.nan
    for target in targets:
        if target not in residues:
            continue
        for atom_site in site_atoms:
            for atom_target in residues[target][1]:
                distance = atom_site - atom_target
                if distance < best:
                    best = distance
                    nearest = target
    if not np.isfinite(best):
        return np.nan, np.nan
    return float(best), int(nearest)


def fetch_alphafold_pair_data(acc: str):
    """Return the checksum-pinned AlphaFold DB v6 metadata and PAE matrix."""
    meta_path = PAE_DIR / f"{acc}_metadata.json"
    if not meta_path.exists():
        raise RuntimeError(f"pinned AlphaFold metadata missing for {acc}")
    metadata = json.loads(meta_path.read_text())

    version = int(metadata["latestVersion"])
    if version != 6 or metadata.get("isComplex"):
        raise RuntimeError(f"unexpected AlphaFold model contract for {acc}")
    if not str(metadata.get("cifUrl", "")).endswith("model_v6.cif"):
        raise RuntimeError(f"AlphaFold CIF URL is not pinned to v6 for {acc}")
    if not str(metadata.get("paeDocUrl", "")).endswith("error_v6.json"):
        raise RuntimeError(f"AlphaFold PAE URL is not pinned to v6 for {acc}")
    pae_path = PAE_DIR / f"{acc}_v{version}_pae.json.gz"
    if not pae_path.exists():
        raise RuntimeError(f"pinned AlphaFold PAE cache missing for {acc}")
    with gzip.open(pae_path, "rt") as handle:
        pae_document = json.load(handle)

    payload = pae_document[0] if isinstance(pae_document, list) else pae_document
    matrix = np.asarray(payload["predicted_aligned_error"], dtype=np.float32)
    return metadata, matrix, pae_path


def aggregate_raw_scores(site_members: pd.DataFrame) -> pd.DataFrame:
    """Average replicate-strain profiles within condition, then summarize each substitution."""
    source = PARENT_DATA / "EMS132528-supplement-Supplementary_Data_3.xlsx"
    scores = pd.read_excel(source, sheet_name="Table S3 – S_Scores of chemical")
    scores["PBY ID"] = scores["PBY ID"].astype(str)
    members = site_members.rename(columns={"Strain ID": "PBY ID"}).copy()
    members["PBY ID"] = members["PBY ID"].astype(str)
    scores = scores.merge(members, on="PBY ID", how="inner", validate="many_to_one")
    condition_scores = (
        scores.groupby(["acc", "pos", "Condition"], sort=False, as_index=False)
        .agg(Score=("Score", "mean"))
    )
    replicate_counts = (
        members.groupby(["acc", "pos"], sort=False)["PBY ID"]
        .nunique().rename("raw_profile_member_count")
    )
    per_strain_q05 = (
        scores.groupby(["acc", "pos", "PBY ID"], sort=False)["qvalue"]
        .apply(lambda x: int((x < 0.05).sum()))
        .rename("raw_q05_per_strain")
        .reset_index()
        .groupby(["acc", "pos"], sort=False)["raw_q05_per_strain"]
        .mean()
        .rename("raw_q05_mean_per_strain")
    )
    source_rows = (
        scores.groupby(["acc", "pos"], sort=False)
        .agg(
            raw_source_rows=("Score", "size"),
            raw_q05_strain_condition_rows=("qvalue", lambda x: int((x < 0.05).sum())),
            raw_min_q=("qvalue", "min"),
        )
    )
    grouped = condition_scores.groupby(["acc", "pos"], sort=False)
    out = grouped.agg(
        sscore_rows=("Score", "size"),
        sscore_conditions=("Condition", "nunique"),
        sscore_mean=("Score", "mean"),
        sscore_sd=("Score", "std"),
        sscore_rms=("Score", lambda x: float(np.sqrt(np.mean(np.square(x))))),
        sscore_mean_abs=("Score", lambda x: float(np.mean(np.abs(x)))),
        sscore_max_abs=("Score", lambda x: float(np.max(np.abs(x)))),
        sscore_min=("Score", "min"),
        sscore_max=("Score", "max"),
    ).join(replicate_counts).join(per_strain_q05).join(source_rows).reset_index()
    return out


def build_mismatch_audit() -> None:
    """Document every point-mutant position excluded by sequence validation."""
    sites = pd.read_csv(PARENT_RESULTS / "sites_validated.csv")
    sites = sites[sites["check"] != "MATCH"].copy()
    proteome = pd.read_csv(PARENT_DATA / "yeast_sgd_uniprot.tsv", sep="\t")
    proteome.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "length"]
    sequences = dict(zip(proteome.acc, proteome.seq))

    nearest_matches = []
    categories = []
    for row in sites.itertuples():
        seq = sequences.get(row.acc, "")
        positions = []
        for offset in range(-3, 4):
            candidate = int(row.pos) + offset
            if candidate >= 1 and candidate <= len(seq) and seq[candidate - 1] == row.pmt_aa_wt:
                positions.append(candidate)
        nearest_matches.append(";".join(map(str, positions)))
        categories.append("nearby_same_residue" if positions else "unresolved")
    sites["same_residue_within_3_positions"] = nearest_matches
    sites["audit_category"] = categories
    sites.to_csv(RESULTS / "residue_mismatch_audit.csv", index=False)


def main() -> None:
    warnings.filterwarnings("ignore", message="Unknown extension is not supported")

    base = pd.read_csv(PARENT_RESULTS / "analysis_inclusive_sensitivity.csv")
    base["Strain ID"] = base["Strain ID"].astype(str)
    all_members = pd.read_csv(PARENT_RESULTS / "analysis_site_members.csv")
    all_members["Strain ID"] = all_members["Strain ID"].astype(str)
    all_members = all_members.merge(
        base[["acc", "pos"]], on=["acc", "pos"], how="inner", validate="many_to_one"
    )[["acc", "pos", "Strain ID"]].drop_duplicates()

    # Supplementary Data 6: annotations and deletion-profile correlation.
    functional_path = PARENT_DATA / "EMS132528-supplement-Supplementary_Data_6.xlsx"
    functional = pd.read_excel(functional_path, sheet_name="Functional information")
    functional = functional.rename(
        columns={
            "refpby": "Strain ID",
            "group": "phenotype_group",
            "label": "supplement_label",
            "is_disopred": "supp_is_disopred",
            "disopred_score_inv": "supp_disopred_score_inv",
        }
    )
    keep = [
        "Strain ID", "cor_estimate", "cor_pvalue", "cor_fdr", "age_w0_group",
        "supp_is_disopred", "supp_disopred_score_inv", "domain_uniprot",
        "pgrid_pubmed_count", "quant_top1", "ptmfunc_counts", "PWM_nkinTop01",
        "sift_ala_score_inv", "phenotype_group", "supplement_label",
    ]
    # Phase 0 may already carry publication-oriented annotations (currently SIFT). Add only
    # genuinely new columns so reruns remain stable as the upstream package matures.
    add_columns = ["Strain ID"] + [column for column in keep[1:] if column not in base.columns]
    enriched = base.merge(
        functional[add_columns], on="Strain ID", how="left", validate="one_to_one"
    )

    # Supplementary Data 3: use the raw profile without inventing a new significance threshold.
    score_summary = aggregate_raw_scores(all_members)
    enriched = enriched.merge(
        score_summary, on=["acc", "pos"], how="left", validate="one_to_one"
    )

    # Supplementary Data 8: verify that no retained member strain carries either
    # of the two explicit source QC flags. The scar table is strain-specific.
    quality_path = PARENT_DATA / "EMS132528-supplement-Supplementary_Data_8.xlsx"
    wgs = pd.read_excel(quality_path, sheet_name="WGS")
    wgs_flagged = set(
        wgs.loc[wgs["Quality Control Note WGS"].notna(), "PBY Number"].astype(str)
    )
    scar = pd.read_excel(quality_path, sheet_name="Corr with control")
    scar_flagged = set(
        scar.loc[
            scar["Correlation with scar control gene"].fillna(False).astype(bool),
            "PBY Number",
        ].astype(str)
    )
    member_qc = all_members.copy()
    member_qc["wgs_additional_mutation_flag"] = member_qc["Strain ID"].isin(wgs_flagged)
    member_qc["scar_control_correlation_flag"] = member_qc["Strain ID"].isin(scar_flagged)
    member_qc = member_qc.groupby(["acc", "pos"], as_index=False).agg(
        wgs_additional_mutation_flag=("wgs_additional_mutation_flag", "any"),
        scar_control_correlation_flag=("scar_control_correlation_flag", "any"),
    )
    for column in ("wgs_additional_mutation_flag", "scar_control_correlation_flag"):
        if column in enriched.columns:
            enriched = enriched.drop(columns=column)
    enriched = enriched.merge(member_qc, on=["acc", "pos"], how="left", validate="one_to_one")

    proteome = pd.read_csv(PARENT_DATA / "yeast_sgd_uniprot.tsv", sep="\t")
    proteome.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "protein_length"]
    enriched = enriched.merge(
        proteome[["acc", "protein_length"]], on="acc", how="left", validate="many_to_one"
    )

    # Recompute distances under alternative annotation definitions and obtain target pLDDT.
    all_features = pd.read_csv(PARENT_RESULTS / "uniprot_features.csv")
    parser = MMCIFParser(QUIET=True)
    feature_rows = []
    pae_manifest = []
    for acc, subset in enriched.groupby("acc", sort=True):
        cif_path = PARENT_DATA / "af" / f"{acc}.cif"
        structure = parser.get_structure(acc, str(cif_path))
        residues = residue_atoms(structure)
        expected_sequence = str(
            proteome.loc[proteome["acc"].astype(str) == str(acc), "seq"].iloc[0]
        )
        metadata, pae_matrix, pae_path = fetch_alphafold_pair_data(acc)
        positions = sorted(residues)
        observed_sequence = "".join(residues[position][0] for position in positions)
        metadata_sequence = str(metadata["sequence"])
        if (
            positions != list(range(1, len(expected_sequence) + 1))
            or observed_sequence != expected_sequence
            or metadata_sequence != expected_sequence
            or str(metadata.get("uniprotSequence")) != expected_sequence
        ):
            raise RuntimeError(f"AlphaFold/UniProt sequence or numbering mismatch for {acc}")
        acc_features = all_features[all_features["acc"] == acc]
        positions_by_set = {
            name: sorted(
                set(acc_features.loc[acc_features["feat_type"].isin(types), "feat_pos"].astype(int))
            )
            for name, types in FEATURE_SETS.items()
        }

        if pae_matrix.shape != (len(expected_sequence), len(expected_sequence)):
            raise RuntimeError(f"AlphaFold PAE dimensions do not match sequence for {acc}")
        pae_manifest.append(
            {
                "acc": acc,
                "entry_id": metadata.get("entryId"),
                "latest_version": metadata.get("latestVersion"),
                "model_created_date": metadata.get("modelCreatedDate"),
                "sequence_checksum": metadata.get("sequenceChecksum"),
                "sequence_start": metadata.get("sequenceStart"),
                "sequence_end": metadata.get("sequenceEnd"),
                "uniprot_start": metadata.get("uniprotStart"),
                "uniprot_end": metadata.get("uniprotEnd"),
                "chain_id": metadata.get("chainId"),
                "tool_used": metadata.get("toolUsed"),
                "is_complex": metadata.get("isComplex"),
                "cif_url": metadata.get("cifUrl"),
                "cif_cached_file": str(cif_path.relative_to(PARENT)),
                "cif_cached_sha256": sha256(cif_path),
                "pae_url": metadata.get("paeDocUrl"),
                "cached_file": str(pae_path.relative_to(HERE)),
                "cached_sha256": sha256(pae_path),
            }
        )

        for row in subset.itertuples():
            result = {"acc": acc, "pos": int(row.pos)}
            nearest_core = np.nan
            for set_name, targets in positions_by_set.items():
                distance, nearest = closest_target(int(row.pos), residues, targets)
                result[f"dist_{set_name}_A"] = distance
                result[f"nearest_{set_name}_pos"] = nearest
                result[f"n_{set_name}_residues"] = len([p for p in targets if p in residues])
                if set_name == "core":
                    nearest_core = nearest

            if pd.notna(nearest_core):
                target_pos = int(nearest_core)
                result["nearest_core_plddt"] = residues[target_pos][2]
                i, j = int(row.pos) - 1, target_pos - 1
                if i < pae_matrix.shape[0] and j < pae_matrix.shape[1]:
                    directed_ij = float(pae_matrix[i, j])
                    directed_ji = float(pae_matrix[j, i])
                    result["pae_site_to_target"] = directed_ij
                    result["pae_target_to_site"] = directed_ji
                    result["pae_pair_mean"] = (directed_ij + directed_ji) / 2
                    result["pae_pair_max"] = max(directed_ij, directed_ji)
                else:
                    result["pae_site_to_target"] = np.nan
                    result["pae_target_to_site"] = np.nan
                    result["pae_pair_mean"] = np.nan
                    result["pae_pair_max"] = np.nan
            else:
                result["nearest_core_plddt"] = np.nan
                result["pae_site_to_target"] = np.nan
                result["pae_target_to_site"] = np.nan
                result["pae_pair_mean"] = np.nan
                result["pae_pair_max"] = np.nan
            result["alphafold_version"] = int(metadata["latestVersion"])
            feature_rows.append(result)
        time.sleep(0.05)

    structural = pd.DataFrame(feature_rows)
    enriched = enriched.merge(structural, on=["acc", "pos"], how="left", validate="one_to_one")
    enriched["core_distance_recompute_delta_A"] = (
        enriched["min_dist_A"] - enriched["dist_core_A"]
    )
    enriched["logd"] = np.log10(enriched["dist_core_A"] + 1.0)
    enriched["neglog10_min_raw_q"] = -np.log10(
        enriched["extremePheno"].clip(lower=1e-300)
    )
    enriched["phenotype_count_reconstruction_mismatch"] = ~np.isclose(
        enriched["phenotypes"], enriched["raw_q05_mean_per_strain"], equal_nan=False
    )
    enriched["has_uniprot_domain"] = enriched["domain_uniprot"].notna().astype(int)
    enriched["age_ordinal"] = enriched["age_w0_group"].map({"S1": 0, "Y2": 1, "Y1": 2, "Y0": 3})

    output_path = RESULTS / "phase0_5_analysis.csv"
    enriched.to_csv(output_path, index=False)
    pd.DataFrame(pae_manifest).to_csv(RESULTS / "alphafold_pae_manifest.csv", index=False)
    build_mismatch_audit()

    source_paths = [
        PARENT_RESULTS / "analysis_final.csv",
        PARENT_RESULTS / "analysis_inclusive_sensitivity.csv",
        PARENT_RESULTS / "analysis_all_eligible.csv",
        PARENT_RESULTS / "analysis_site_members.csv",
        PARENT_RESULTS / "cohort_disposition.csv",
        PARENT_RESULTS / "uniprot_features.csv",
        PARENT_RESULTS / "uniprot_features_detailed.csv",
        PARENT_DATA / "uniprot_entries_raw.json",
        PARENT_DATA / "EMS132528-supplement-Supplementary_Data_3.xlsx",
        functional_path,
        quality_path,
        PARENT_DATA / "yeast_sgd_uniprot.tsv",
    ]
    manifest = {
        "inputs": [
            {"path": str(path.relative_to(PARENT)), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in source_paths
        ],
        "output": {
            "path": str(output_path.relative_to(HERE)),
            "bytes": output_path.stat().st_size,
            "sha256": sha256(output_path),
        },
    }
    (RESULTS / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    max_delta = float(enriched["core_distance_recompute_delta_A"].abs().max())
    print(f"Phase 0.5 table: {len(enriched)} sites / {enriched.acc.nunique()} proteins")
    print(f"raw S-score coverage: {int(enriched.sscore_rms.notna().sum())}/{len(enriched)}")
    print(f"PAE coverage: {int(enriched.pae_pair_max.notna().sum())}/{len(enriched)}")
    print(f"AlphaFold versions: {sorted(enriched.alphafold_version.dropna().unique().astype(int))}")
    print(f"max core-distance recomputation delta: {max_delta:.3g} A")
    print(f"WGS flags in analysis set: {int(enriched.wgs_additional_mutation_flag.sum())}")
    print(
        "scar-control correlation flags in analysis set: "
        f"{int(enriched.scar_control_correlation_flag.sum())}"
    )
    print(
        "phenotype-count reconstruction mismatches: "
        f"{int(enriched.phenotype_count_reconstruction_mismatch.sum())}"
    )


if __name__ == "__main__":
    main()
