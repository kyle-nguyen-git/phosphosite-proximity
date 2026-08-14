"""Recompute the Section 20 family under the declared primary endpoints.

Section 20 was computed on the union `p3 < 0.05 or p4 < 0.05`. That endpoint is withdrawn: it pools two
different phenotypes that agree on 6 sites out of ~145, and it leaves two multiplicity layers
uncorrected. The declared primaries are now the two screens separately, each corrected for the two
MAGeCK directions:

  A1  fitness screen, Supplementary Table 3   2 * p3 < 0.05
  A2  NFAT reporter screen, Supplementary Table 4   2 * p4 < 0.05

Everything that depends on which sites are positive has to move with them: the experimental-evidence
arm, every comparator and paired difference, the permutation null, the ranked-pair decomposition, and
the positive control. This recomputes all of it for both, plus the continuous arms that use no p-value.

Quantities that depend only on the predictor — the short-range counts, the peptide-bond band — do not
move and are recomputed once as a check that they have not.

Outputs `primary_recompute.json`. Nothing here may enter a manuscript, wiki page or email until it is
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
XL = os.path.join(HERE, "cache", "ochoa_functional_score.xlsx")


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
            "half_width": None if touching else round((r["ci_high"] - r["ci_low"]) / 2, 6),
            "contains_half": bool(touching or (r["ci_low"] <= 0.5 <= r["ci_high"])),
            "draws_retained": int(r["draws"])}


def family(d, y, tag, feat=None):
    """Everything in the Section 20 family, for one declared endpoint."""
    score, groups = -d.min_dist_A, d.acc
    out = {"positives": int(y.sum()), "positive_rate": round(float(y.mean()), 4)}

    out["primary"] = interval(y, score, groups, f"{tag}: distance, primary")

    e = d.min_dist_exp_A.notna()
    out["experimental_evidence_only"] = interval(
        y[e], -d.min_dist_exp_A[e], groups[e], f"{tag}: experimentally-evidenced targets only")

    seqsep = (d.pos - d.nearest_feat_pos).abs()
    comparators, diffs = [], {}
    for label, s in [("minimum sequence separation", -seqsep), ("site pLDDT", d.plddt),
                     ("inverse relative solvent accessibility", -d.rsa),
                     ("annotated target count", d.n_annot_residues)]:
        comparators.append(interval(y, s, groups, f"{tag}: {label}"))
        dif = p05.paired_auc_difference(np.asarray(y, int), np.asarray(s, float),
                                        -d.min_dist_A.to_numpy(float), d.acc.to_numpy(),
                                        n=DRAWS, seed=SEED)
        diffs[label] = {"estimate": round(dif["estimate"], 6),
                        "ci_low": round(dif["ci_low"], 6), "ci_high": round(dif["ci_high"], 6),
                        "excludes_zero": bool(dif["ci_low"] > 0 or dif["ci_high"] < 0)}
    out["comparators"] = comparators
    out["paired_differences_vs_distance"] = diffs

    rng = np.random.default_rng(SEED)
    yv = np.asarray(y, int)
    obs = p05.auc_from_ranks(yv, -d.min_dist_A.to_numpy(float))
    null = np.array([p05.auc_from_ranks(rng.permutation(yv), -d.min_dist_A.to_numpy(float))
                     for _ in range(DRAWS)])
    out["permutation_null"] = {
        "observed": round(float(obs), 6), "null_mean": round(float(null.mean()), 6),
        "null_sd": round(float(null.std(ddof=1)), 6),
        "sd_from_centre": round(float(abs(obs - null.mean()) / null.std(ddof=1)), 3),
        "two_sided_p": round(float((np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean())) + 1)
                                   / (DRAWS + 1)), 4)}

    pos, neg = int(yv.sum()), int((1 - yv).sum())
    tmp = d.assign(_y=yv)
    within = sum(int(g._y.sum()) * int((1 - g._y).sum()) for _, g in tmp.groupby("acc"))
    out["pair_decomposition"] = {
        "ranked_pairs": pos * neg, "within_protein": within,
        "within_protein_pct": round(100 * within / max(1, pos * neg), 4),
        "across_protein_pct": round(100 * (1 - within / max(1, pos * neg)), 4),
        "informative_proteins": int(sum(1 for _, g in tmp.groupby("acc")
                                        if g._y.sum() and (1 - g._y).sum()))}

    if feat is not None:
        m = feat
        for col, sign, lab in [("sift_min_score", -1, "SIFT minimum score"),
                               ("sift_ala_score", -1, "SIFT alanine score")]:
            v = pd.to_numeric(m[col], errors="coerce")
            k = v.notna()
            out.setdefault("positive_control", []).append(
                interval(np.asarray(y)[k.to_numpy()], (sign * v)[k], m.acc[k], f"{tag}: {lab}"))
    return out


def main():
    d = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    d = d[d.min_dist_A.notna()].reset_index(drop=True)

    feat = None
    if os.path.exists(XL):
        cols = ["uniprot", "position", "sift_min_score", "sift_ala_score"]
        f = pd.read_excel(XL, sheet_name="annotated_phosphoproteome", usecols=cols)
        f = f.rename(columns={"uniprot": "acc", "position": "pos"})
        f["pos"] = pd.to_numeric(f["pos"], errors="coerce")
        feat = d.merge(f, on=["acc", "pos"], how="left")

    out = {"cohort_sites": int(len(d)), "proteins": int(d.acc.nunique())}

    # predictor-only quantities, which must not move
    seqsep = (d.pos - d.nearest_feat_pos).abs()
    sub5 = d[d.min_dist_A <= 5]
    out["predictor_only"] = {
        "sites_within_5A": int(len(sub5)),
        "sequence_adjacent_dpos_le_2": int((seqsep[d.min_dist_A <= 5] <= 2).sum()),
        "peptide_bond_band_1.30_1.35A": int(((sub5.min_dist_A >= 1.30) & (sub5.min_dist_A <= 1.35)).sum()),
        "median_distance_A": round(float(d.min_dist_A.median()), 4),
        "median_plddt": round(float(d.plddt.median()), 4)}

    for tag, y in [("A1 fitness", (2 * d.p3 < 0.05).astype(int)),
                   ("A2 reporter", (2 * d.p4 < 0.05).astype(int))]:
        print(f"--- {tag} ---", flush=True)
        out[tag] = family(d, y, tag, feat)
        print(json.dumps({k: v for k, v in out[tag].items()
                          if k in ("positives", "primary", "pair_decomposition")}, indent=1), flush=True)

    with open(os.path.join(HERE, "primary_recompute.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote primary_recompute.json")


if __name__ == "__main__":
    main()
