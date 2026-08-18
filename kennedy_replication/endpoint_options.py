"""What each candidate human endpoint gives, so the choice is made on numbers.

The current endpoint is `p3 < 0.05 or p4 < 0.05`. It has two uncorrected multiplicity layers — the two
MAGeCK directions inside each screen, and the union across two screens — and it pools two different
phenotypes: Supplementary Table 3 is a fitness readout, Supplementary Table 4 an NFAT reporter readout.

This enumerates the options rather than picking one:

  A  each screen separately, direction-corrected      2*min(p_neg,p_pos) < 0.05
  B  union across screens, fully corrected            min of four directional p-values < 0.0125
  C  continuous, no p-value at all                    |log2 fold change|, per screen and pooled
  D  the screens' own FDR                             MAGeCK FDR, reported for completeness

Every arm is scored with the same frozen estimator and the same protein-cluster bootstrap. Arms A and
B are reconstructed from the four source MAGeCK directional columns. The released per-site columns are
retained only for the explicitly withdrawn uncorrected union and the source FDR arm.

Outputs `endpoint_options_source_corrected.json`. Nothing here may enter a manuscript, wiki page or
email until it is registered in `NUMBERS.md`.
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
SHEETS = [("gs_SuppTable_3_MAGeCK_gene_summary.csv", "fitness"),
          ("gs_SuppTable4_MAGeCK_gene_summary.csv", "reporter")]


def directional_minima(d):
    """Reconstruct each screen from its source MAGeCK negative/positive p-value columns."""
    out = {}
    for filename, tag in SHEETS:
        g = pd.read_csv(os.path.join(HERE, "cache", filename)).set_index("id")
        vals = []
        for r in d.itertuples():
            row = g.loc[f"{r.gene}_{r.aa}{r.pos}"]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            vals.append(min(float(row["neg|p-value"]), float(row["pos|p-value"])))
        out[tag] = np.asarray(vals, float)
    return out


def interval(y, score, groups, label, note=""):
    y = np.asarray(y, int)
    if y.sum() < 10 or (1 - y).sum() < 10:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
                "auc": None, "note": "too few in one class to estimate"}
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups),
                          n=DRAWS, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    lo, hi = (None, None) if touching else (round(r["ci_low"], 6), round(r["ci_high"], 6))
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "positive_rate": round(float(y.mean()), 4),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6), "ci_low": lo, "ci_high": hi,
            "half_width": None if touching else round((r["ci_high"] - r["ci_low"]) / 2, 6),
            "contains_half": bool(touching or (r["ci_low"] <= 0.5 <= r["ci_high"])),
            "draws_retained": int(r["draws"]), "note": note}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohort", default=os.path.join(HERE, "kennedy_analysis_corrected.csv"))
    ap.add_argument("--out", default=os.path.join(HERE, "endpoint_options_source_corrected.json"))
    opts = ap.parse_args()
    d = pd.read_csv(opts.cohort)
    d = d[d.min_dist_A.notna()].copy()
    score, groups = -d.min_dist_A, d.acc
    rows = []
    rec = directional_minima(d)

    # ---- current, for reference -------------------------------------------
    rows.append(interval((d.p3 < 0.05) | (d.p4 < 0.05), score, groups,
                         "CURRENT: p3<0.05 or p4<0.05",
                         "two uncorrected layers; unions two phenotypes"))

    # ---- A: each screen separately, direction-corrected --------------------
    rows.append(interval(2 * rec["fitness"] < 0.05, score, groups,
                         "A1: fitness screen, 2*min(p_neg,p_pos) < 0.05",
                         "Supplementary Table 3, abundance before vs after ABE8e"))
    rows.append(interval(2 * rec["reporter"] < 0.05, score, groups,
                         "A2: NFAT reporter, 2*min(p_neg,p_pos) < 0.05",
                         "Supplementary Table 4, GFP-high vs GFP-low"))

    # ---- B: union, corrected for direction and screen ----------------------
    rows.append(interval((rec["fitness"] < 0.0125) | (rec["reporter"] < 0.0125), score, groups,
                         "B: union, Bonferroni over four directional p-values",
                         "declared composite; a site is affected in either phenotype"))

    # ---- C: continuous, no p-value ----------------------------------------
    for col, lab in [("l3", "C1: |log2 FC|, fitness screen"),
                     ("l4", "C2: |log2 FC|, NFAT reporter screen")]:
        mag = d[col].abs()
        keep = mag.notna()
        rows.append(interval((mag[keep] >= mag[keep].quantile(0.90)).astype(int),
                             score[keep], groups[keep], lab + ", top decile",
                             "no p-value used"))
    mag = d[["l3", "l4"]].abs().max(axis=1)
    rows.append(interval((mag >= mag.quantile(0.90)).astype(int), score, groups,
                         "C3: |log2 FC|, larger of the two screens, top decile",
                         "no p-value used; still pools two phenotypes"))

    # ---- D: the screens' own FDR ------------------------------------------
    rows.append(interval((d.f3 < 0.25) | (d.f4 < 0.25), score, groups,
                         "D: MAGeCK FDR < 0.25 either screen",
                         "the screens' own multiplicity control"))

    # ---- how much do the two screens even agree? ---------------------------
    a = (2 * rec["fitness"] < 0.05)
    b = (2 * rec["reporter"] < 0.05)
    agreement = {
        "called_in_fitness_only": int((a & ~b).sum()),
        "called_in_reporter_only": int((~a & b).sum()),
        "called_in_both": int((a & b).sum()),
        "called_in_neither": int((~a & ~b).sum()),
        "jaccard": round(float((a & b).sum() / max(1, (a | b).sum())), 4),
        "spearman_l3_l4": round(float(d[["l3", "l4"]].corr(method="spearman").iloc[0, 1]), 4),
    }

    out = {"cohort_sites": int(len(d)), "proteins": int(d.acc.nunique()),
           "arms": rows, "screen_agreement": agreement}
    with open(opts.out, "w") as fh:
        json.dump(out, fh, indent=2)

    print(pd.DataFrame(rows)[["label", "positive", "positive_rate", "auc",
                              "ci_low", "ci_high", "half_width", "contains_half"]]
          .to_string(index=False))
    print()
    print(json.dumps(agreement, indent=1))


if __name__ == "__main__":
    main()
