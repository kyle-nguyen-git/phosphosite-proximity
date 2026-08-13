"""Run the yeast analysis against the Kennedy 2024 human cohort.

Estimators are imported from the frozen yeast module rather than reimplemented, so the two
cohorts are computed by the same code and the comparison means something.

Conventions carried over: accession is the resampling unit, 20,000 draws, seed 20260728,
retained draws reported for every interval, no interval printed whose endpoint touches 0 or 1.
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


def interval(y, score, groups, label, n_draws=DRAWS):
    """Protein-clustered AUC with retained-draw disclosure."""
    r = p05.bootstrap_auc(np.asarray(y, int), np.asarray(score, float),
                          groups=np.asarray(groups), n=n_draws, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {
        "label": label, "n": int(len(y)), "positive": int(np.sum(y)),
        "proteins": int(pd.Series(groups).nunique()),
        "auc": round(r["estimate"], 6),
        "ci_low": None if touching else round(r["ci_low"], 6),
        "ci_high": None if touching else round(r["ci_high"], 6),
        "draws_nominal": n_draws, "draws_retained": int(r["draws"]),
        "interval_withheld_boundary": bool(touching),
    }


def main():
    d = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    d = d[d.min_dist_A.notna()].copy()

    # Primary endpoint: called in either screen at raw p < 0.05. Stated in advance of the
    # estimate, and co-reported with the stricter FDR arm below.
    d["y"] = ((d.p3 < 0.05) | (d.p4 < 0.05)).astype(int)
    d["y_fdr"] = ((d.f3 < 0.25) | (d.f4 < 0.25)).astype(int)
    d["seqsep"] = (d.pos - d.nearest_feat_pos).abs()

    results, notes = [], {}

    # ---- primary and its endpoint sensitivity ----------------------------
    results.append(interval(d.y, -d.min_dist_A, d.acc, "distance, primary endpoint (p<0.05 either screen)"))
    results.append(interval(d.y_fdr, -d.min_dist_A, d.acc, "distance, FDR<0.25 either screen"))

    # ---- experimental-evidence-only target set ---------------------------
    e = d[d.min_dist_exp_A.notna()]
    results.append(interval(e.y, -e.min_dist_exp_A, e.acc, "distance to experimentally-evidenced targets only"))

    # ---- comparators, all on the primary endpoint ------------------------
    comparators = [
        ("minimum sequence separation to an eligible target", -d.seqsep),
        ("site pLDDT", d.plddt),
        ("inverse relative solvent accessibility", -d.rsa),
        ("annotated target count in the protein", d.n_annot_residues),
    ]
    for label, score in comparators:
        results.append(interval(d.y, score, d.acc, label))
        diff = p05.paired_auc_difference(d.y.to_numpy(), np.asarray(score, float),
                                         -d.min_dist_A.to_numpy(float), d.acc.to_numpy(),
                                         n=DRAWS, seed=SEED)
        notes[f"paired difference vs distance: {label}"] = {
            "estimate": round(diff["estimate"], 6),
            "ci_low": round(diff["ci_low"], 6), "ci_high": round(diff["ci_high"], 6),
            "excludes_zero": bool(diff["ci_low"] > 0 or diff["ci_high"] < 0),
        }

    # ---- permutation null -------------------------------------------------
    rng = np.random.default_rng(SEED)
    obs = p05.auc_from_ranks(d.y.to_numpy(), -d.min_dist_A.to_numpy(float))
    null = np.array([p05.auc_from_ranks(rng.permutation(d.y.to_numpy()),
                                        -d.min_dist_A.to_numpy(float)) for _ in range(DRAWS)])
    notes["permutation null"] = {
        "observed": round(float(obs), 6), "null_mean": round(float(null.mean()), 6),
        "null_sd": round(float(null.std(ddof=1)), 6),
        "two_sided_p": round(float((np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean())) + 1) / (DRAWS + 1)), 4),
        "permutations": DRAWS,
    }

    # ---- ranked-pair decomposition ---------------------------------------
    pos, neg = int(d.y.sum()), int((1 - d.y).sum())
    within = sum(int(g.y.sum()) * int((1 - g.y).sum()) for _, g in d.groupby("acc"))
    notes["pair decomposition"] = {
        "ranked_pairs": pos * neg, "within_protein": within,
        "within_protein_pct": round(100 * within / (pos * neg), 2),
        "informative_proteins": int(sum(1 for _, g in d.groupby("acc") if g.y.sum() and (1 - g.y).sum())),
    }

    # ---- short range ------------------------------------------------------
    sub5 = d[d.min_dist_A <= 5]
    notes["short range"] = {
        "sites_within_5A": int(len(sub5)),
        "of_which_sequence_adjacent_dpos_le_2": int((sub5.seqsep <= 2).sum()),
        "peptide_bond_band_1.30_1.35A": int(((sub5.min_dist_A >= 1.30) & (sub5.min_dist_A <= 1.35)).sum()),
    }
    f = d[d.seqsep > 2]
    results.append(interval(f.y, -f.min_dist_A, f.acc, "distance, sequence-adjacent pairs excluded"))

    out = {"cohort": {"sites": int(len(d)), "proteins": int(d.acc.nunique()),
                      "positives_primary": pos, "positive_rate": round(pos / len(d), 4)},
           "estimates": results, "notes": notes}
    with open(os.path.join(HERE, "kennedy_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    print(json.dumps(out["cohort"], indent=2))
    print()
    print(pd.DataFrame(results).to_string(index=False))
    print()
    for k, v in notes.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
