"""
Step 1 — build the site-level analysis set from primary public sources.

Downloads (or reuses cached copies of):
  - Viéitez et al., Nat Biotechnol 2022;40:382-390 supplementary data (Europe PMC, PMC7612524)
  - the reviewed S. cerevisiae proteome with sequences (UniProt REST)
  - UniProt ACT_SITE / BINDING / SITE / DNA_BIND feature residues for the proteins involved

Then:
  1. keeps point-mutant strains only (Supplementary Data 1, "Sup Table 1")
  2. maps yeast systematic names to UniProt accessions via ordered-locus names
  3. validates that the residue at each reported position is the claimed S/T/Y
  4. reconstructs outcomes from the raw 102-condition screen (Supplementary Data 3)
  5. applies the strain-specific WGS and scar-correlation flags (Supplementary Data 8)
  6. uses Supplementary Data 6 only for optional biological annotations
  7. restricts to proteins carrying >=1 ACT_SITE or BINDING annotation
  8. aggregates replicate strains to one row per amino-acid substitution

Outputs
  results/cohort_disposition.csv     every point mutant with an inclusion/exclusion reason
  results/sites_validated.csv        compatibility copy of the full disposition table
  results/sites_with_phenotype.csv   eligible strain records with raw-screen outcomes
  results/analysis_site_members.csv  strains represented by each core substitution
  results/uniprot_features.csv       all retrieved feature residues
  results/uniprot_features_core.csv  ACT_SITE / BINDING only
  results/analysis_set.csv           the set carried into 02_structures.py

Deterministic: no sampling in this step.
"""
import io
import json
import os
import time
import zipfile

import pandas as pd
import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
RES = os.path.join(HERE, "results")
os.makedirs(DATA, exist_ok=True)
os.makedirs(RES, exist_ok=True)

PMCID = "PMC7612524"                       # Viéitez et al. 2022, PMID 34663920
YEAST_PROTEOME = "559292"                  # S. cerevisiae S288C
SUPPL_URL = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles"
UNIPROT_STREAM = "https://rest.uniprot.org/uniprotkb/stream"
UNIPROT_SEARCH = "https://rest.uniprot.org/uniprotkb/search"
CORE_FEATURES = ("Active site", "Binding site")
ALL_FEATURES = ("Active site", "Binding site", "Site", "DNA binding")


def fetch_supplementary() -> None:
    """Pull the Viéitez supplementary bundle and unpack the .xlsx files."""
    target = os.path.join(DATA, "EMS132528-supplement-Supplementary_Data_1.xlsx")
    if os.path.exists(target):
        return
    zpath = os.path.join(DATA, f"{PMCID}_supplementary.zip")
    if not os.path.exists(zpath) or os.path.getsize(zpath) < 10_000:
        r = requests.get(SUPPL_URL, timeout=300)
        r.raise_for_status()
        with open(zpath, "wb") as fh:
            fh.write(r.content)
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            if name.endswith(".xlsx"):
                z.extract(name, DATA)


def fetch_proteome() -> pd.DataFrame:
    """Reviewed yeast proteome: accession, ordered-locus names, sequence."""
    path = os.path.join(DATA, "yeast_sgd_uniprot.tsv")
    if not os.path.exists(path) or os.path.getsize(path) < 100_000:
        r = requests.get(
            UNIPROT_STREAM,
            params={
                "query": f"organism_id:{YEAST_PROTEOME} AND reviewed:true",
                "fields": "accession,id,gene_oln,gene_primary,protein_name,sequence,length",
                "format": "tsv",
            },
            timeout=300,
        )
        r.raise_for_status()
        with open(path, "wb") as fh:
            fh.write(r.content)
    up = pd.read_csv(path, sep="\t")
    up.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "length"]
    return up


def fetch_features(accessions) -> pd.DataFrame:
    """Retrieve functional-site features and preserve auditable UniProt metadata."""
    path = os.path.join(RES, "uniprot_features.csv")
    detailed_path = os.path.join(RES, "uniprot_features_detailed.csv")
    raw_path = os.path.join(DATA, "uniprot_entries_raw.json")
    accession_path = os.path.join(DATA, "uniprot_feature_accessions.txt")
    requested = sorted(set(accessions))
    cached_accessions = []
    if os.path.exists(accession_path):
        with open(accession_path) as handle:
            cached_accessions = [line.strip() for line in handle if line.strip()]
    if (
        all(os.path.exists(p) for p in (path, detailed_path, raw_path, accession_path))
        and cached_accessions == requested
    ):
        return pd.read_csv(path)
    rows, detailed, raw_entries, batch = [], [], [], 40
    releases, release_dates = set(), set()
    for i in range(0, len(accessions), batch):
        query = " OR ".join(f"accession:{a}" for a in accessions[i:i + batch])
        r = requests.get(
            UNIPROT_SEARCH,
            params={
                "query": query, "format": "json", "size": 500,
            },
            timeout=180,
        )
        r.raise_for_status()
        if r.headers.get("x-uniprot-release"):
            releases.add(r.headers["x-uniprot-release"])
        if r.headers.get("x-uniprot-release-date"):
            release_dates.add(r.headers["x-uniprot-release-date"])
        batch_entries = r.json().get("results", [])
        raw_entries.extend(batch_entries)
        for entry in batch_entries:
            acc = entry["primaryAccession"]
            audit = entry.get("entryAudit", {})
            for feat in entry.get("features", []):
                ftype = feat.get("type")
                if ftype not in ALL_FEATURES:
                    continue
                loc = feat.get("location", {})
                start = loc.get("start", {}).get("value")
                end = loc.get("end", {}).get("value")
                if start is None:
                    continue
                end = int(end or start)
                evidences = feat.get("evidences", [])
                ligand = feat.get("ligand") or {}
                ligand_part = feat.get("ligandPart") or {}
                detailed.append({
                    "acc": acc,
                    "entry_id": entry.get("uniProtkbId", ""),
                    "entry_version": audit.get("entryVersion"),
                    "sequence_version": audit.get("sequenceVersion"),
                    "annotation_update_date": audit.get("lastAnnotationUpdateDate", ""),
                    "feat_type": ftype,
                    "feature_id": feat.get("featureId", ""),
                    "start": int(start),
                    "end": end,
                    "start_modifier": loc.get("start", {}).get("modifier", ""),
                    "end_modifier": loc.get("end", {}).get("modifier", ""),
                    "is_range": int(start) != end,
                    "description": feat.get("description") or "",
                    "ligand_name": ligand.get("name", ""),
                    "ligand_id": ligand.get("id", ""),
                    "ligand_part_name": ligand_part.get("name", ""),
                    "ligand_part_id": ligand_part.get("id", ""),
                    "evidence_codes": ";".join(sorted({e.get("evidenceCode", "") for e in evidences if e.get("evidenceCode")})),
                    "evidence_sources": ";".join(sorted({e.get("source", "") for e in evidences if e.get("source")})),
                    "evidence_ids": ";".join(sorted({e.get("id", "") for e in evidences if e.get("id")})),
                    "evidence_json": json.dumps(evidences, sort_keys=True, separators=(",", ":")),
                    "cross_references_json": json.dumps(feat.get("featureCrossReferences", []), sort_keys=True, separators=(",", ":")),
                })
                for pos in range(int(start), end + 1):
                    rows.append({
                        "acc": acc, "feat_type": ftype, "feat_pos": pos,
                        "desc": feat.get("description") or "",
                    })
        time.sleep(0.3)
    feats = pd.DataFrame(rows).drop_duplicates(subset=["acc", "feat_type", "feat_pos"])
    feats.to_csv(path, index=False)
    pd.DataFrame(detailed).drop_duplicates().to_csv(detailed_path, index=False)
    with open(raw_path, "w") as handle:
        json.dump({
            "uniprot_release": sorted(releases),
            "uniprot_release_date": sorted(release_dates),
            "retrieved_entries": raw_entries,
        }, handle, indent=2)
    with open(accession_path, "w") as handle:
        handle.write("\n".join(requested) + "\n")
    return feats


def main() -> None:
    fetch_supplementary()
    up = fetch_proteome()
    seqs = dict(zip(up.acc, up.seq))

    # ordered-locus name (e.g. YMR037C) -> accession; the column may hold several
    oln2acc = {}
    for _, row in up.iterrows():
        if pd.isna(row.oln):
            continue
        for token in str(row.oln).replace(";", " ").split():
            oln2acc.setdefault(token.strip().upper(), row.acc)

    strains = pd.read_excel(
        os.path.join(DATA, "EMS132528-supplement-Supplementary_Data_1.xlsx"),
        sheet_name="Sup Table 1",
    ).dropna(how="all")
    pm = strains[strains.is_point_mutant.fillna(False).astype(bool)].copy()
    pm["Strain ID"] = pm["Strain ID"].astype(str)
    pm["source_pos"] = pm.pmt_position.astype(int)
    pm["pos"] = pm.source_pos
    pm["position_resolution"] = "source workbook coordinate"

    # Supplementary Data 1/6 label this construct HOG1 T178A, but the source
    # article and Supplementary Data 8 identify the screened control as
    # HOG1 T174A. T174 also matches the reviewed UniProt sequence; T178 does not.
    hog1 = pm["Strain ID"].eq("PBY107")
    pm.loc[hog1, "pos"] = 174
    pm.loc[hog1, "position_resolution"] = (
        "resolved HOG1 T178A workbook label to T174A from source article and Supplementary Data 8"
    )
    pm["acc"] = pm["Systematic name"].str.upper().map(oln2acc)
    print(
        f"point-mutant strain records: {len(pm)} / "
        f"{pm[['Systematic name', 'source_pos', 'pmt_aa_wt', 'pmt_aa_mutant']].drop_duplicates().shape[0]} "
        f"source substitutions / {pm['Systematic name'].nunique()} genes"
    )
    unmapped = sorted(pm.loc[pm.acc.isna(), "Systematic name"].unique())
    if unmapped:
        print(f"  unmapped systematic names: {unmapped}")

    def validate(row):
        seq = seqs.get(row.acc)
        if not isinstance(seq, str) or row.pos > len(seq):
            return "OUT_OF_RANGE"
        observed = seq[row.pos - 1]
        return "MATCH" if observed == row.pmt_aa_wt else f"MISMATCH:{observed}"

    pm["check"] = pm.apply(validate, axis=1)

    # Reconstruct the outcome from the full raw screening table. This is the
    # outcome ledger; Supplementary Data 6 is a Figure 2 annotation table and
    # must not determine cohort membership.
    raw = pd.read_excel(
        os.path.join(DATA, "EMS132528-supplement-Supplementary_Data_3.xlsx"),
        sheet_name="Table S3 – S_Scores of chemical",
    ).dropna(how="all")
    raw["PBY ID"] = raw["PBY ID"].astype(str)
    per_strain = (
        raw.groupby("PBY ID", sort=False)
        .agg(
            raw_profile_rows=("Score", "size"),
            raw_conditions=("Condition", "nunique"),
            raw_n_q05=("qvalue", lambda x: int((x < 0.05).sum())),
            raw_min_q=("qvalue", "min"),
        )
        .reset_index()
        .rename(columns={"PBY ID": "Strain ID"})
    )
    pm = pm.merge(per_strain, on="Strain ID", how="left", validate="one_to_one")
    pm["raw_profile_available"] = pm.raw_profile_rows.notna()

    quality_path = os.path.join(DATA, "EMS132528-supplement-Supplementary_Data_8.xlsx")
    wgs = pd.read_excel(quality_path, sheet_name="WGS").dropna(how="all")
    wgs_ids = set(
        wgs.loc[wgs["Quality Control Note WGS"].notna(), "PBY Number"].astype(str)
    )
    scar = pd.read_excel(quality_path, sheet_name="Corr with control").dropna(how="all")
    scar_ids = set(
        scar.loc[
            scar["Correlation with scar control gene"].fillna(False).astype(bool),
            "PBY Number",
        ].astype(str)
    )
    pm["wgs_quality_flag"] = pm["Strain ID"].isin(wgs_ids)
    pm["scar_control_correlation_flag"] = pm["Strain ID"].isin(scar_ids)

    def disposition(row):
        if pd.isna(row.acc):
            return "exclude: no reviewed UniProt mapping"
        if row.check != "MATCH":
            return f"exclude: {row.check.lower()} at resolved coordinate"
        if not row.raw_profile_available:
            return "exclude: no raw screening profile"
        if row.wgs_quality_flag:
            return "exclude: Supplementary Data 8 WGS quality flag"
        if row.scar_control_correlation_flag:
            return "exclude: Supplementary Data 8 scar-control correlation"
        return "include: sequence-validated raw-screen strain"

    pm["cohort_disposition"] = pm.apply(disposition, axis=1)
    pm["eligible_raw_cohort"] = pm.cohort_disposition.str.startswith("include:")
    pm.to_csv(os.path.join(RES, "cohort_disposition.csv"), index=False)
    pm.to_csv(os.path.join(RES, "sites_validated.csv"), index=False)

    eligible = pm[pm.eligible_raw_cohort].copy()
    print(
        f"raw screen: {int(pm.raw_profile_available.sum())}/{len(pm)} point-mutant records; "
        f"sequence/QC eligible: {len(eligible)} records / "
        f"{eligible[['acc', 'pos', 'pmt_aa_wt', 'pmt_aa_mutant']].drop_duplicates().shape[0]} "
        f"substitutions / {eligible.acc.nunique()} proteins"
    )

    # Supplementary Data 6 contributes annotations only. Prefix source fields
    # that would otherwise be mistaken for the reconstructed outcome.
    func = pd.read_excel(
        os.path.join(DATA, "EMS132528-supplement-Supplementary_Data_6.xlsx"),
        sheet_name="Functional information",
    ).dropna(how="all")
    annotation_cols = [
        "refpby", "cor_estimate", "cor_pvalue", "cor_fdr", "label",
        "isPhosphogrid", "age_w0_group", "is_disopred", "disopred_score_inv",
        "domain_uniprot", "pgrid_pubmed_count", "quant_top1", "ptmfunc_counts",
        "PWM_nkinTop01", "sift_ala_score_inv", "group", "phenotypes", "extremePheno",
    ]
    ann = func[[c for c in annotation_cols if c in func.columns]].copy()
    ann = ann.rename(
        columns={
            "phenotypes": "supp6_phenotypes",
            "extremePheno": "supp6_extremePheno",
        }
    )
    eligible = eligible.merge(
        ann, left_on="Strain ID", right_on="refpby", how="left", validate="one_to_one"
    )
    eligible["phenotypes"] = eligible.raw_n_q05.astype(float)
    eligible["extremePheno"] = eligible.raw_min_q.astype(float)
    eligible["has_pheno"] = eligible.phenotypes > 0
    eligible["in_supplementary_data_6"] = eligible.refpby.notna()

    feats = fetch_features(sorted(eligible.acc.unique()))
    core = feats[feats.feat_type.isin(CORE_FEATURES)]
    core.to_csv(os.path.join(RES, "uniprot_features_core.csv"), index=False)
    print(f"features: {len(feats)} residues, {len(core)} ACT_SITE/BINDING "
          f"across {core.acc.nunique()} proteins")

    annotated_positions = set(zip(core.acc, core.feat_pos))
    eligible["has_annot"] = eligible.acc.isin(set(core.acc.unique()))
    eligible["is_itself_annot"] = [
        (a, p) in annotated_positions for a, p in zip(eligible.acc, eligible.pos)
    ]
    eligible.to_csv(os.path.join(RES, "sites_with_phenotype.csv"), index=False)

    members = eligible[eligible.acc.isin(set(core.acc.unique()))].copy()
    members.to_csv(os.path.join(RES, "analysis_site_members.csv"), index=False)

    # Collapse technical/biological replicate strains to the prespecified unit:
    # one amino-acid substitution. Counts are averaged as in the source Figure 2
    # table; the binary label is whether that mean is greater than zero.
    key = ["acc", "pos", "pmt_aa_wt", "pmt_aa_mutant"]

    def first_observed(series):
        observed = series.dropna()
        return observed.iloc[0] if len(observed) else pd.NA

    first_cols = [
        "Gene name", "Systematic name", "source_pos", "position_resolution", "Strain name",
        "label", "group", "is_disopred", "disopred_score_inv", "sift_ala_score_inv",
        "cor_estimate", "cor_pvalue", "cor_fdr", "isPhosphogrid", "age_w0_group",
        "domain_uniprot", "pgrid_pubmed_count", "quant_top1", "ptmfunc_counts",
        "PWM_nkinTop01", "supp6_phenotypes", "supp6_extremePheno",
    ]
    aggregations = {
        "Strain ID": lambda s: ";".join(sorted(set(s.astype(str)))),
        "phenotypes": "mean",
        "extremePheno": "min",
        "raw_profile_rows": "sum",
        "raw_conditions": "max",
        "in_supplementary_data_6": "all",
        **{c: first_observed for c in first_cols if c in members.columns},
    }
    analysis = members.groupby(key, as_index=False, sort=True).agg(aggregations)
    analysis = analysis.rename(columns={"Strain ID": "member_strain_ids"})
    analysis["Strain ID"] = analysis.member_strain_ids.str.split(";").str[0]
    analysis["source_replicate_strain_count"] = analysis.member_strain_ids.str.count(";") + 1
    analysis["has_pheno"] = analysis.phenotypes > 0
    analysis["has_annot"] = True
    analysis["is_itself_annot"] = [
        (a, p) in annotated_positions for a, p in zip(analysis.acc, analysis.pos)
    ]
    analysis["wgs_quality_flag"] = False
    analysis["scar_control_correlation_flag"] = False
    analysis.to_csv(os.path.join(RES, "analysis_set.csv"), index=False)

    print(
        f"ANALYSIS SET: {len(analysis)} unique substitutions / {analysis.acc.nunique()} proteins / "
        f"{int(analysis.has_pheno.sum())} outcome-positive"
    )
    print(f"  sites that are themselves annotated: {int(analysis.is_itself_annot.sum())}")
    print("\nnext: src/02_structures.py")


if __name__ == "__main__":
    main()
