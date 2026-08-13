"""Retain the source quality-control exclusions and re-estimate.

`NUMBERS.md` §19.5 records that the two source QC filters removed 38 strain records of which 34 (89.5%)
are screen-positive, against 39.6% among the 427 retained, and that the scar-correlation filter is
defined on phenotype similarity to a marker control — so for those records the exclusion is conditioned
on the outcome by construction. No arm retained them and no distances were ever computed for them.

Excluding outcome-associated records and then reporting a near-chance estimate is the objection this
script exists to answer. Of the 38, ten sit in a protein carrying an eligible ACT_SITE or BINDING
annotation with a cached AlphaFold model, so ten can be given a distance under the declared estimand.
All ten are sequencing-flagged; none of the twenty scar-flagged records lands in an annotated protein,
which is itself worth reporting because the scar filter is the one conditioned on the outcome.

Distance is computed by the frozen definition in `src/02_structures.py`: minimum heavy-atom separation
to the nearest eligible annotated residue in the AlphaFold monomer, exact overlap scored 0 Å. That
module is imported rather than reimplemented so the two arms cannot drift.

Outputs `qc_inclusive_arm.json` and `qc_inclusive_cohort.csv`. Nothing here may enter a manuscript,
figure or email until it is registered in `NUMBERS.md`.
"""
import importlib.util
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CAL = os.path.join(HERE, "..", "phase0_calibration")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p05 = load("p05", os.path.join(CAL, "phase0_5", "src", "02_phase0_5_analysis.py"))
struct = load("structures", os.path.join(CAL, "src", "02_structures.py"))
DRAWS, SEED = 200000, 20260728


def interval(y, score, groups, label, draws=DRAWS):
    y = np.asarray(y, int)
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups),
                          n=draws, seed=SEED)
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6),
            "ci_low": round(r["ci_low"], 6), "ci_high": round(r["ci_high"], 6),
            "half_width": round((r["ci_high"] - r["ci_low"]) / 2, 6),
            "draws_nominal": draws, "draws_retained": int(r["draws"])}


def main():
    from Bio.PDB import MMCIFParser, ShrakeRupley

    disp = pd.read_csv(os.path.join(CAL, "results", "cohort_disposition.csv"))
    feats = pd.read_csv(os.path.join(CAL, "results", "uniprot_features_core.csv"))
    final = pd.read_csv(os.path.join(CAL, "results", "analysis_final.csv"))

    excluded = disp[(disp.wgs_quality_flag) | (disp.scar_control_correlation_flag)].copy()
    feat_by_acc = feats.groupby("acc")["feat_pos"].apply(lambda s: sorted(set(s))).to_dict()

    out = {"excluded_records": {
        "total": int(len(excluded)),
        "sequencing_flagged": int(disp.wgs_quality_flag.sum()),
        "scar_flagged": int(disp.scar_control_correlation_flag.sum()),
        "proteins": int(excluded.acc.nunique()),
        "screen_positive": int((excluded.raw_n_q05.fillna(0) > 0).sum()),
    }}

    parser, sr = MMCIFParser(QUIET=True), ShrakeRupley()
    rows, skipped = [], {"no_annotation": 0, "no_model": 0, "not_in_model": 0, "aa_mismatch": 0}
    for acc, grp in excluded.groupby("acc"):
        targets_all = feat_by_acc.get(acc, [])
        if not targets_all:
            skipped["no_annotation"] += len(grp)
            continue
        path = os.path.join(CAL, "data", "af", f"{acc}.cif")
        if not os.path.exists(path):
            skipped["no_model"] += len(grp)
            continue
        res = struct.residue_atoms(parser.get_structure(acc, path))
        try:
            sr.compute(parser.get_structure(acc, path)[0], level="R")
        except Exception:
            pass
        targets = [p for p in targets_all if p in res]
        for _, r in grp.iterrows():
            pos = int(r["pos"])
            if pos not in res:
                skipped["not_in_model"] += 1
                continue
            aa, atoms, plddt = res[pos]
            if aa != r["pmt_aa_wt"]:
                skipped["aa_mismatch"] += 1
                continue
            if pos in targets:
                dmin, nearest = 0.0, pos
            else:
                best, nearest = np.inf, np.nan
                for t in targets:
                    for a1 in atoms:
                        for a2 in res[t][1]:
                            d = a1 - a2
                            if d < best:
                                best, nearest = d, t
                dmin = best if np.isfinite(best) else np.nan
            rows.append({"acc": acc, "pos": pos, "aa": aa, "gene": r["Gene name"],
                         "strain": r["Strain ID"], "min_dist_A": dmin,
                         "nearest_feat_pos": nearest, "plddt": plddt,
                         "n_annot_residues": len(targets),
                         "raw_n_q05": r["raw_n_q05"],
                         "y": int((r["raw_n_q05"] or 0) > 0),
                         "wgs_quality_flag": bool(r["wgs_quality_flag"]),
                         "scar_control_correlation_flag": bool(r["scar_control_correlation_flag"])})
    add = pd.DataFrame(rows)
    out["restored"] = {
        "records": int(len(add)),
        "proteins": int(add.acc.nunique()) if len(add) else 0,
        "screen_positive": int(add.y.sum()) if len(add) else 0,
        "sequencing_flagged": int(add.wgs_quality_flag.sum()) if len(add) else 0,
        "scar_flagged": int(add.scar_control_correlation_flag.sum()) if len(add) else 0,
        "median_distance_A": round(float(add.min_dist_A.median()), 4) if len(add) else None,
        "not_restorable": skipped,
    }

    # ---- combine with the primary arm --------------------------------------
    base = final[["acc", "pos", "min_dist_A", "y"]].copy()
    base = base[final.cohort_primary_exclude_annotation_coincident.astype(bool)]
    add_sites = (add.groupby(["acc", "pos"])
                    .agg(min_dist_A=("min_dist_A", "first"), y=("y", "max"))
                    .reset_index())
    # a restored record may name a site already in the primary cohort; keep the primary row
    dup = add_sites.merge(base[["acc", "pos"]], on=["acc", "pos"], how="inner")
    add_new = add_sites.merge(base[["acc", "pos"]], on=["acc", "pos"], how="left", indicator=True)
    add_new = add_new[add_new._merge == "left_only"].drop(columns="_merge")
    out["restored"]["distinct_sites"] = int(len(add_sites))
    out["restored"]["already_in_primary_cohort"] = int(len(dup))
    out["restored"]["new_sites_added"] = int(len(add_new))

    combined = pd.concat([base, add_new[["acc", "pos", "min_dist_A", "y"]]], ignore_index=True)
    combined = combined[combined.min_dist_A.notna()]

    est = [
        interval(base.y, -base.min_dist_A, base.acc, "primary arm as published"),
        interval(combined.y, -combined.min_dist_A, combined.acc,
                 "QC-inclusive arm: source quality-control exclusions restored"),
    ]
    out["estimates"] = est
    out["difference_in_point_estimate"] = round(est[1]["auc"] - est[0]["auc"], 6)

    combined.to_csv(os.path.join(HERE, "qc_inclusive_cohort.csv"), index=False)
    with open(os.path.join(HERE, "qc_inclusive_arm.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out["excluded_records"], indent=1))
    print(json.dumps(out["restored"], indent=1))
    print()
    print(pd.DataFrame(est).to_string(index=False))


if __name__ == "__main__":
    main()
