"""Does the Kennedy endpoint detect anything already known to be functional?

Two candidate positive controls, both external to this work:

1. PhosphoSitePlus curated regulatory sites, as distributed in Ochoa et al. 2020
   Supplementary Data. These are sites with an established regulatory role in the literature.
   If the screen's hits are not enriched for them, the endpoint is the limiting factor.

2. Individual published features from the Ochoa 59-feature set — conservation (SIFT),
   disorder, interface and hotspot flags, kinase-motif scores. Each is tested as a predictor
   of the screen outcome with the same estimator used everywhere else.

A feature that separates the classes here is a positive control. If none does, the honest
reading is that this endpoint cannot support a calibration of any site-level feature.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _paths  # noqa: E402  — resolves the vault and repository layouts

p05 = _paths.analysis_module()
DRAWS, SEED = 20000, 20260728
XL = os.path.join(HERE, "cache", "ochoa_functional_score.xlsx")

FEATURES = [
    ("sift_ala_score", -1, "SIFT score for the alanine substitution (lower = more damaging)"),
    ("sift_min_score", -1, "SIFT minimum score across substitutions"),
    ("disopred_score", -1, "predicted disorder (lower = more ordered)"),
    ("isHotspot", 1, "phosphorylation hotspot flag"),
    ("isInterface", 1, "protein-interface flag"),
    ("log10_hotspot_pval_min", -1, "hotspot p-value"),
    ("PWM_max_mss", 1, "best kinase-motif match score"),
    ("netpho_max_all", 1, "NetPhos maximum prediction"),
    ("EV_ala_prediction_epistatic", -1, "evolutionary-coupling prediction for the alanine mutant"),
    ("prot_length", 1, "protein length"),
    ("paxdb_abundance_log10", 1, "protein abundance"),
    ("adj_ptms_w21", 1, "neighbouring PTMs within 21 residues"),
]


def interval(y, score, groups, label):
    keep = ~pd.isna(score)
    y, score, groups = np.asarray(y)[keep], np.asarray(score, float)[keep], np.asarray(groups)[keep]
    if len(y) < 40 or y.sum() < 10 or (1 - y).sum() < 10:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
                "auc": None, "note": "too small to estimate"}
    r = p05.bootstrap_auc(y.astype(int), score, groups=groups, n=DRAWS, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6),
            "ci_low": None if touching else round(r["ci_low"], 6),
            "ci_high": None if touching else round(r["ci_high"], 6),
            "excludes_half": bool((not touching) and (r["ci_low"] > 0.5 or r["ci_high"] < 0.5)),
            "draws_retained": int(r["draws"])}


def main():
    coh = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    coh = coh[coh.min_dist_A.notna()].copy()
    coh["y"] = ((coh.p3 < 0.05) | (coh.p4 < 0.05)).astype(int)
    print(f"cohort: {len(coh)} sites, {coh.acc.nunique()} proteins, {coh.y.sum()} positive", flush=True)

    # ---- 1. PhosphoSitePlus known regulatory sites -------------------------
    psp = pd.read_excel(XL, sheet_name="known_regulatory_PSP", skiprows=1)
    psp.columns = [str(c).strip() for c in psp.columns]
    psp = psp.rename(columns={psp.columns[0]: "acc", psp.columns[1]: "position"})
    psp["position"] = pd.to_numeric(psp["position"], errors="coerce")
    known = set(zip(psp.acc.astype(str), psp.position.astype("Int64")))
    coh["is_known_regulatory"] = [
        (a, p) in known for a, p in zip(coh.acc.astype(str), coh.pos.astype("Int64"))]
    k = int(coh.is_known_regulatory.sum())
    print(f"\nPhosphoSitePlus regulatory sites in the cohort: {k} of {len(coh)}", flush=True)

    out = {"cohort": {"sites": int(len(coh)), "positives": int(coh.y.sum()),
                      "known_regulatory_in_cohort": k}}
    if k >= 10:
        hit_known = coh.loc[coh.is_known_regulatory, "y"].mean()
        hit_other = coh.loc[~coh.is_known_regulatory, "y"].mean()
        out["known_regulatory_enrichment"] = {
            "n_known": k, "hit_rate_known": round(float(hit_known), 4),
            "n_other": int((~coh.is_known_regulatory).sum()),
            "hit_rate_other": round(float(hit_other), 4),
            "difference_points": round(100 * float(hit_known - hit_other), 2),
        }
        out["known_regulatory_as_predictor"] = interval(
            coh.y, coh.is_known_regulatory.astype(float), coh.acc,
            "PhosphoSitePlus known-regulatory flag")
        print("  hit rate, known regulatory: %.1f%%  vs other: %.1f%%"
              % (100 * hit_known, 100 * hit_other), flush=True)

    # ---- 2. published features as candidate positive controls -------------
    cols = ["uniprot", "position"] + [f for f, _, _ in FEATURES]
    feat = pd.read_excel(XL, sheet_name="annotated_phosphoproteome", usecols=cols)
    feat = feat.rename(columns={"uniprot": "acc", "position": "pos"})
    feat["pos"] = pd.to_numeric(feat["pos"], errors="coerce")
    m = coh.merge(feat, on=["acc", "pos"], how="left")
    matched = m[[f for f, _, _ in FEATURES]].notna().any(axis=1).sum()
    print(f"\ncohort sites matched into the Ochoa phosphoproteome: {matched} of {len(m)}", flush=True)
    out["ochoa_match"] = {"matched": int(matched), "of": int(len(m))}

    rows = [interval(m.y, -m.min_dist_A, m.acc, "distance (reference)")]
    for col, sign, desc in FEATURES:
        if col not in m:
            continue
        v = pd.to_numeric(m[col], errors="coerce")
        if v.notna().sum() < 40:
            continue
        rows.append(interval(m.y, sign * v, m.acc, desc))
    out["features"] = rows

    print()
    print(pd.DataFrame(rows).to_string(index=False))
    winners = [r for r in rows if r.get("excludes_half")]
    print()
    print("features whose interval excludes 0.5:",
          [r["label"] for r in winners] if winners else "NONE")
    out["any_positive_control"] = bool(winners)

    with open(os.path.join(HERE, "positive_control.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    m.to_csv(os.path.join(HERE, "kennedy_with_ochoa_features.csv"), index=False)


if __name__ == "__main__":
    main()
