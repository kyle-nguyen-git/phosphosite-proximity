"""Within-protein discrimination in the human cohort, under both declared primaries.

The second independent review's central design objection is that the headline AUC is dominated by
comparisons between different proteins — 102 of 99,684 ranked pairs on the fitness screen and 180 of
111,600 on the reporter screen — while the use case the paper names is choosing among sites inside one
protein. Pair counts state the problem; they do not estimate the quantity. This estimates it.

The estimator is the frozen `within_protein_discrimination` from the yeast analysis module, imported
rather than reimplemented, so the yeast and human within-protein numbers are computed the same way. It
restricts to proteins carrying both outcome classes, computes an AUC inside each, and aggregates two
ways: weighted by the positive-negative pairs each protein contributes, and weighting every informative
protein equally. Uncertainty resamples proteins.

Also computed here: the single-edit / no-bystander sensitivity under both declared primaries, which
`NUMBERS.md` §20.6 has under the withdrawn union endpoint only.

Outputs `within_protein.json`. Nothing here may enter a manuscript, wiki page or email until it is
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


def main():
    d = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    d = d[d.min_dist_A.notna()].reset_index(drop=True)

    # the frozen estimator reads columns named `y` and `dist_core_A`
    out = {"cohort_sites": int(len(d)), "proteins": int(d.acc.nunique())}

    for tag, y in [("A1 fitness", (2 * d.p3 < 0.05).astype(int)),
                   ("A2 reporter", (2 * d.p4 < 0.05).astype(int))]:
        frame = pd.DataFrame({"acc": d.acc, "y": y, "dist_core_A": d.min_dist_A})
        detail, summary = p05.within_protein_discrimination(frame, n=DRAWS, seed=SEED)
        detail.to_csv(os.path.join(HERE, f"within_protein_{tag.split()[0]}.csv"), index=False)
        out[tag] = {k: (round(v, 6) if isinstance(v, float) else v) for k, v in summary.items()}
        print(f"--- {tag} ---")
        print(f"  informative proteins {summary['informative_proteins']}, "
              f"sites {summary['informative_sites']}, "
              f"pairs {summary['within_protein_positive_negative_pairs']}")
        print(f"  pair-weighted        {summary['pair_weighted_auc']:.6f} "
              f"[{summary['pair_weighted_ci_low']:.6f}, {summary['pair_weighted_ci_high']:.6f}]")
        print(f"  equal-protein-weight {summary['equal_protein_weight_auc']:.6f} "
              f"[{summary['equal_protein_weight_ci_low']:.6f}, {summary['equal_protein_weight_ci_high']:.6f}]",
              flush=True)

    # ---- single-edit / no-bystander arm under both declared primaries ----
    cls_path = os.path.join(HERE, "kennedy_analysis_with_class.csv")
    if os.path.exists(cls_path):
        c = pd.read_csv(cls_path)
        c = c[c.min_dist_A.notna()]
        single = c[c.max_edits == 1]
        arms = {}
        for tag, col in [("A1 fitness", "p3"), ("A2 reporter", "p4")]:
            yy = (2 * single[col] < 0.05).astype(int)
            if yy.sum() >= 10 and (1 - yy).sum() >= 10:
                r = p05.bootstrap_auc(yy.to_numpy(int), -single.min_dist_A.to_numpy(float),
                                      groups=single.acc.to_numpy(), n=DRAWS, seed=SEED)
                arms[tag] = {"n": int(len(single)), "positive": int(yy.sum()),
                             "proteins": int(single.acc.nunique()),
                             "auc": round(r["estimate"], 6),
                             "ci_low": round(r["ci_low"], 6), "ci_high": round(r["ci_high"], 6),
                             "draws_retained": int(r["draws"])}
            else:
                arms[tag] = {"n": int(len(single)), "positive": int(yy.sum()),
                             "auc": None, "note": "too few in one class"}
        out["single_edit_no_bystander"] = arms
        print("\nsingle-edit / no-bystander:")
        print(json.dumps(arms, indent=1))

    with open(os.path.join(HERE, "within_protein.json"), "w") as fh:
        json.dump(out, fh, indent=2)


if __name__ == "__main__":
    main()
