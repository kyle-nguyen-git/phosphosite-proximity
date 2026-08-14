"""Rebuild both human endpoints from the two MAGeCK directional columns, and regenerate everything.

The declared endpoints doubled the screens' *released* per-site column. Section 22.2 records that the
released column reproduces `min(neg|p-value, pos|p-value)` on only 1,428 of 1,475 rows for the fitness
screen and 1,372 of 1,475 for the reporter screen, so a doubled released column is not the same
quantity as a doubled reconstruction from the two directions.

It matters for the reporter screen. Reconstructing moves it from 80 to 83 positives — TBKBP1_S335,
PDE4A_S13 and BRSK2_S367 change classification — and the fitness screen does not move at all, because
none of its 47 mismatched rows crosses the threshold.

The consequence that has to be reported: under the released column the reporter's equal-protein
within-protein interval ended at 0.498044, below 0.5. Reconstructed, it ends at 0.501814. **The only
interval in the paper that excluded 0.5 from below does not survive the correct endpoint.**

This script defines the endpoint once, from source, and regenerates every dependent quantity so nothing
downstream is left describing the old label.

Outputs `rebuilt_endpoints.json`. Nothing here may enter a manuscript, wiki page or email until it is
registered in `NUMBERS.md`.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _paths  # noqa: E402

p05 = _paths.analysis_module()
DRAWS, SEED = 20000, 20260728
XL = os.path.join(HERE, "cache", "kennedy_supplement.xlsx")
OCHOA = os.path.join(HERE, "cache", "ochoa_functional_score.xlsx")
SHEETS = [("SuppTable 3 MAGeCK gene_summary", "fitness"),
          ("SuppTable4 MAGeCK gene_summary", "reporter")]


def interval(y, score, groups, label):
    y = np.asarray(y, int)
    if y.sum() < 10 or (1 - y).sum() < 10:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()), "auc": None,
                "note": "too few in one class"}
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups), n=DRAWS, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6),
            "ci_low": None if touching else round(r["ci_low"], 6),
            "ci_high": None if touching else round(r["ci_high"], 6),
            "half_width": None if touching else round((r["ci_high"] - r["ci_low"]) / 2, 6),
            "contains_half": bool(touching or (r["ci_low"] <= 0.5 <= r["ci_high"])),
            "draws_retained": int(r["draws"])}


def reconstruct(coh):
    """Directional minimum per site, taken from the source gene_summary sheets."""
    out = {}
    for sheet, tag in SHEETS:
        g = pd.read_excel(XL, sheet_name=sheet)
        key = g.set_index(g["id"].astype(str))
        vals, missing = [], 0
        for r in coh.itertuples():
            k = f"{r.gene}_{r.aa}{r.pos}"
            if k in key.index:
                row = key.loc[k]
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                vals.append(min(float(row["neg|p-value"]), float(row["pos|p-value"])))
            else:
                vals.append(np.nan)
                missing += 1
        out[tag] = (np.asarray(vals, float), missing)
    return out


def main():
    coh = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    coh = coh[coh.min_dist_A.notna()].reset_index(drop=True)
    rec = reconstruct(coh)
    out = {"cohort_sites": int(len(coh)), "proteins": int(coh.acc.nunique()), "screens": {}}

    feat = None
    if os.path.exists(OCHOA):
        f = pd.read_excel(OCHOA, sheet_name="annotated_phosphoproteome",
                          usecols=["uniprot", "position", "sift_min_score", "sift_ala_score"])
        f = f.rename(columns={"uniprot": "acc", "position": "pos"})
        f["pos"] = pd.to_numeric(f["pos"], errors="coerce")
        feat = coh.merge(f, on=["acc", "pos"], how="left")

    cls = None
    p = os.path.join(HERE, "kennedy_analysis_with_class.csv")
    if os.path.exists(p):
        cls = pd.read_csv(p)
        cls = cls[cls.min_dist_A.notna()]

    for tag, released_col in [("fitness", "p3"), ("reporter", "p4")]:
        vals, missing = rec[tag]
        y_rel = (2 * coh[released_col] < 0.05).astype(int)
        y = pd.Series((2 * vals < 0.05).astype(int))
        changed = coh[y_rel.to_numpy() != y.to_numpy()]
        rr = {"unmatched_ids": missing,
              "positives_released_column": int(y_rel.sum()),
              "positives_reconstructed": int(y.sum()),
              "sites_changing_classification": [f"{r.gene}_{r.aa}{r.pos}" for r in changed.itertuples()]}

        score, groups = -coh.min_dist_A, coh.acc
        rr["primary"] = interval(y, score, groups, f"{tag}: distance, reconstructed primary")

        e = coh.min_dist_exp_A.notna()
        rr["experimental_evidence_only"] = interval(y[e.to_numpy()], -coh.min_dist_exp_A[e], groups[e],
                                                    f"{tag}: experimentally-evidenced targets only")

        seqsep = (coh.pos - coh.nearest_feat_pos).abs()
        comps, diffs = [], {}
        for label, s in [("minimum sequence separation", -seqsep), ("site pLDDT", coh.plddt),
                         ("inverse relative solvent accessibility", -coh.rsa),
                         ("annotated target count", coh.n_annot_residues)]:
            comps.append(interval(y, s, groups, f"{tag}: {label}"))
            d = p05.paired_auc_difference(y.to_numpy(int), np.asarray(s, float),
                                          -coh.min_dist_A.to_numpy(float), coh.acc.to_numpy(),
                                          n=DRAWS, seed=SEED)
            diffs[label] = {"estimate": round(d["estimate"], 6), "ci_low": round(d["ci_low"], 6),
                            "ci_high": round(d["ci_high"], 6),
                            "excludes_zero": bool(d["ci_low"] > 0 or d["ci_high"] < 0)}
        rr["comparators"] = comps
        rr["paired_differences_vs_distance"] = diffs

        rng = np.random.default_rng(SEED)
        yv = y.to_numpy(int)
        obs = p05.auc_from_ranks(yv, -coh.min_dist_A.to_numpy(float))
        null = np.array([p05.auc_from_ranks(rng.permutation(yv), -coh.min_dist_A.to_numpy(float))
                         for _ in range(DRAWS)])
        rr["permutation_null"] = {
            "observed": round(float(obs), 6), "null_mean": round(float(null.mean()), 6),
            "null_sd": round(float(null.std(ddof=1)), 6),
            "sd_from_centre": round(float(abs(obs - null.mean()) / null.std(ddof=1)), 3),
            "two_sided_p": round(float((np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean())) + 1)
                                       / (DRAWS + 1)), 4)}

        pos, neg = int(yv.sum()), int((1 - yv).sum())
        tmp = coh.assign(_y=yv)
        within = sum(int(g._y.sum()) * int((1 - g._y).sum()) for _, g in tmp.groupby("acc"))
        rr["pair_decomposition"] = {
            "ranked_pairs": pos * neg, "within_protein": within,
            "within_protein_pct": round(100 * within / max(1, pos * neg), 4),
            "across_protein_pct": round(100 * (1 - within / max(1, pos * neg)), 4),
            "informative_proteins": int(sum(1 for _, g in tmp.groupby("acc")
                                            if g._y.sum() and (1 - g._y).sum()))}

        frame = pd.DataFrame({"acc": coh.acc, "y": yv, "dist_core_A": coh.min_dist_A})
        _, w = p05.within_protein_discrimination(frame, n=DRAWS, seed=SEED)
        rr["within_protein"] = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in w.items()}
        rr["within_protein"]["equal_protein_excludes_half_below"] = bool(
            w["equal_protein_weight_ci_high"] < 0.5)

        if feat is not None:
            rr["positive_control"] = []
            for col, lab in [("sift_min_score", "SIFT minimum score"),
                             ("sift_ala_score", "SIFT alanine score")]:
                v = pd.to_numeric(feat[col], errors="coerce")
                k = v.notna().to_numpy()
                rr["positive_control"].append(interval(yv[k], (-v)[k], feat.acc[k], f"{tag}: {lab}"))

        if cls is not None:
            single = cls[cls.max_edits == 1]
            sv, _ = rec[tag]
            idx = coh.set_index(["acc", "pos"]).index
            m = single.set_index(["acc", "pos"]).index
            sel = [i for i, key in enumerate(idx) if key in set(m)]
            ys = (2 * sv[sel] < 0.05).astype(int)
            rr["single_edit_no_bystander"] = interval(ys, -coh.min_dist_A.iloc[sel],
                                                      coh.acc.iloc[sel],
                                                      f"{tag}: single-edit guides only")
        out["screens"][tag] = rr
        print(f"--- {tag} ---")
        print(f"  positives {rr['positives_released_column']} -> {rr['positives_reconstructed']}"
              f"  ({len(rr['sites_changing_classification'])} changed)")
        print(f"  primary {rr['primary']['auc']} [{rr['primary']['ci_low']}, {rr['primary']['ci_high']}]")
        wp = rr["within_protein"]
        print(f"  within-protein equal {wp['equal_protein_weight_auc']} "
              f"[{wp['equal_protein_weight_ci_low']}, {wp['equal_protein_weight_ci_high']}]"
              f"  excludes 0.5 below: {wp['equal_protein_excludes_half_below']}", flush=True)

    with open(os.path.join(HERE, "rebuilt_endpoints.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote rebuilt_endpoints.json")


if __name__ == "__main__":
    main()
