"""Characterise the Kennedy 2024 outcome variable, and re-run the primary estimate against it.

`analyse.py` calls a site affected at `p3 < 0.05 or p4 < 0.05`, treating those columns as p-values.
They are not. Each is the minimum of MAGeCK's two one-sided gene-level p-values, `neg|p-value` and
`pos|p-value`. A minimum of two one-sided tests is not a two-sided p-value: under the null it is
distributed roughly U(0, 0.5), so a 0.05 cut-off admits about twice the nominal rate.

This matters in the direction that flatters the paper's conclusion. Non-differential label noise
attenuates AUC toward 0.5, so an inflated false-positive rate among "affected" sites makes a null
result easier to obtain. The near-chance human estimate must not be read without this.

The script does three things:

1. Characterises the outcome: the distribution of each p column, the rate below 0.05, and how often
   the cohort's `p3` equals `min(neg, pos)`.
2. Measures endpoint sensitivity on the screen's own 208 essential-splice-site guides, which should
   deplete. This is a positive control for the *endpoint*, distinct from the Ochoa-feature positive
   control for the *predictor* in `positive_control.py`.
3. Re-runs the primary distance AUC under three repaired outcome definitions and reports whether the
   near-chance reading survives.

Outputs `endpoint_characterisation.json`. Nothing here may enter a manuscript, wiki page or email
until it is registered in `NUMBERS.md`.
"""
import importlib.util
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "p05", os.path.join(HERE, "..", "phase0_calibration", "phase0_5", "src", "02_phase0_5_analysis.py"))
p05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p05)
DRAWS, SEED = 20000, 20260728
XL = os.path.join(HERE, "cache", "kennedy_supplement.xlsx")
SHEETS = [("SuppTable 3 MAGeCK gene_summary", "screen3"),
          ("SuppTable4 MAGeCK gene_summary", "screen4")]


def interval(y, score, groups, label):
    y = np.asarray(y, int)
    if y.sum() < 10 or (1 - y).sum() < 10:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
                "auc": None, "note": "too few in one class"}
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups),
                          n=DRAWS, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6),
            "ci_low": None if touching else round(r["ci_low"], 6),
            "ci_high": None if touching else round(r["ci_high"], 6),
            "contains_half": bool(touching or (r["ci_low"] <= 0.5 <= r["ci_high"])),
            "draws_retained": int(r["draws"])}


def main():
    out = {}

    # ---- 1. the outcome variable ------------------------------------------
    dist = {}
    for sheet, tag in SHEETS:
        try:
            g = pd.read_excel(XL, sheet_name=sheet)
        except Exception as exc:
            dist[tag] = {"error": str(exc)}
            continue
        n = g["neg|p-value"].astype(float)
        p = g["pos|p-value"].astype(float)
        mn = np.minimum(n, p)
        ids = g["id"].astype(str)
        is_ctrl = ids.str.contains("Essentialsplicesite", case=False, na=False)
        rec = {"rows": int(len(g))}
        for lab, v in [("neg_p", n), ("pos_p", p), ("min_p", mn)]:
            rec[lab] = {"median": round(float(np.median(v)), 6),
                        "max": round(float(v.max()), 6),
                        "frac_below_0.05": round(float((v < 0.05).mean()), 6)}
        nc = mn[~is_ctrl]
        rec["non_control"] = {
            "rows": int((~is_ctrl).sum()),
            "median_min_p": round(float(np.median(nc)), 6),
            "frac_below_0.05": round(float((nc < 0.05).mean()), 6),
            "expected_under_uniform_two_sided": 0.05,
            "inflation_factor": round(float((nc < 0.05).mean() / 0.05), 3),
        }
        # 2. endpoint sensitivity on the screen's own lethal controls
        if is_ctrl.any():
            cm = mn[is_ctrl]
            rec["essential_splice_controls"] = {
                "rows": int(is_ctrl.sum()),
                "median_min_p": round(float(np.median(cm)), 6),
                "detected_at_0.05": round(float((cm < 0.05).mean()), 6),
                "median_neg_lfc": round(float(g.loc[is_ctrl, "neg|lfc"].astype(float).median()), 6),
            }
        dist[tag] = rec
    out["outcome_distribution"] = dist

    # how often does the cohort's p3 reproduce min(neg, pos)?
    coh = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    coh = coh[coh.min_dist_A.notna()].copy()
    g3 = pd.read_excel(XL, sheet_name="SuppTable 3 MAGeCK gene_summary")
    key = g3.set_index(g3["id"].astype(str))
    hit = miss = unmatched = 0
    for r in coh.itertuples():
        k = f"{r.gene}_{r.aa}{r.pos}"
        if k not in key.index:
            unmatched += 1
            continue
        row = key.loc[k]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        want = min(float(row["neg|p-value"]), float(row["pos|p-value"]))
        hit, miss = (hit + 1, miss) if abs(float(r.p3) - want) < 1e-9 else (hit, miss + 1)
    out["p3_is_min_of_one_sided"] = {"matched": hit, "mismatched": miss,
                                     "unmatched_ids": unmatched, "cohort_rows": int(len(coh))}

    # ---- 3. repaired outcome definitions ----------------------------------
    coh["y_asused"] = ((coh.p3 < 0.05) | (coh.p4 < 0.05)).astype(int)
    # Treating p3/p4 as min of two one-sided tests, a valid two-sided p is 2*min, capped at 1.
    coh["y_twosided"] = ((2 * coh.p3 < 0.05) | (2 * coh.p4 < 0.05)).astype(int)
    coh["y_fdr25"] = ((coh.f3 < 0.25) | (coh.f4 < 0.25)).astype(int)
    # Continuous magnitude, which does not depend on any p-value construction at all.
    mag = np.maximum(coh[["l3", "l4"]].abs().max(axis=1).fillna(0), 0)
    coh["y_topdecile"] = (mag >= mag.quantile(0.90)).astype(int)

    rows = []
    for col, label in [("y_asused", "as used: min(neg,pos) < 0.05 either screen"),
                       ("y_twosided", "repaired: 2 x min(neg,pos) < 0.05 either screen"),
                       ("y_fdr25", "MAGeCK FDR < 0.25 either screen"),
                       ("y_topdecile", "top decile of |log2 fold change|")]:
        rows.append(interval(coh[col], -coh.min_dist_A, coh.acc, label))
    out["distance_under_repaired_outcomes"] = rows

    print(json.dumps(out["outcome_distribution"], indent=1))
    print()
    print(json.dumps(out["p3_is_min_of_one_sided"], indent=1))
    print()
    print(pd.DataFrame(rows).to_string(index=False))

    with open(os.path.join(HERE, "endpoint_characterisation.json"), "w") as fh:
        json.dump(out, fh, indent=2)


if __name__ == "__main__":
    main()
