"""AUC for the tip-oxygen predictor, and its paired difference against the declared predictor.

Same estimator, same protein-cluster bootstrap, same seed as everything else, so the two predictors are
compared on identical rows.
"""
import json, os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RESEARCH, "kennedy_replication"))
import _paths                                    # noqa: E402
p05 = _paths.analysis_module()
DRAWS, SEED = 20000, 20260728


def interval(y, score, groups, label):
    y = np.asarray(y, int)
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups), n=DRAWS, seed=SEED)
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6), "ci_low": round(r["ci_low"], 6),
            "ci_high": round(r["ci_high"], 6), "draws_retained": int(r["draws"]),
            "contains_half": bool(r["ci_low"] <= 0.5 <= r["ci_high"])}


def paired(y, a, b, groups):
    d = p05.paired_auc_difference(np.asarray(y, int), np.asarray(a, float), np.asarray(b, float),
                                  np.asarray(groups), n=DRAWS, seed=SEED)
    return {"estimate": round(d["estimate"], 6), "ci_low": round(d["ci_low"], 6),
            "ci_high": round(d["ci_high"], 6),
            "excludes_zero": bool(d["ci_low"] > 0 or d["ci_high"] < 0)}


def arm(coh, y, tag, out):
    k = coh.tip_dist_A.notna() & coh.min_dist_A.notna()
    c, yy = coh[k], np.asarray(y, int)[k.to_numpy()]
    out[tag] = {
        "declared": interval(yy, -c.min_dist_A, c.acc, f"{tag}: declared minimum heavy-atom distance"),
        "tip":      interval(yy, -c.tip_dist_A, c.acc, f"{tag}: distance from the phospho-accepting oxygen"),
        "paired_tip_minus_declared": paired(yy, -c.tip_dist_A, -c.min_dist_A, c.acc),
        "spearman_between_predictors": round(float(c[["min_dist_A", "tip_dist_A"]]
                                                   .corr(method="spearman").iloc[0, 1]), 4),
        "declared_within_5A": int((c.min_dist_A < 5).sum()),
        "tip_within_5A": int((c.tip_dist_A < 5).sum()),
        "declared_peptide_band_1_30_1_35": int(((c.min_dist_A >= 1.30) & (c.min_dist_A <= 1.35)).sum()),
        "tip_peptide_band_1_30_1_35": int(((c.tip_dist_A >= 1.30) & (c.tip_dist_A <= 1.35)).sum()),
        "tip_min_A": round(float(c.tip_dist_A.min()), 4),
    }
    r = out[tag]
    print(f"--- {tag} ---")
    print(f"  declared {r['declared']['auc']} [{r['declared']['ci_low']}, {r['declared']['ci_high']}]")
    print(f"  tip      {r['tip']['auc']} [{r['tip']['ci_low']}, {r['tip']['ci_high']}]")
    d = r["paired_tip_minus_declared"]
    print(f"  paired tip - declared {d['estimate']:+f} [{d['ci_low']:+f}, {d['ci_high']:+f}] excludes0={d['excludes_zero']}")
    print(f"  peptide band: declared {r['declared_peptide_band_1_30_1_35']} -> tip {r['tip_peptide_band_1_30_1_35']}; min tip {r['tip_min_A']} A", flush=True)


if __name__ == "__main__":
    out = {}
    y_ = pd.read_csv(os.path.join(RESEARCH, "phase0_calibration", "phase0_5", "results",
                                  "phase0_5_primary_analysis.csv"))
    t_ = pd.read_csv(os.path.join(HERE, "tip_distance_yeast.csv"))
    coh = y_.merge(t_[["acc", "pos", "tip_dist_A", "tip_nearest_feat_pos"]], on=["acc", "pos"], how="left")
    arm(coh, coh.y, "yeast", out)

    hp = os.path.join(HERE, "tip_distance_human.csv")
    if os.path.exists(hp):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "re_", os.path.join(RESEARCH, "kennedy_replication", "rebuild_endpoints.py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        h = pd.read_csv(os.path.join(RESEARCH, "kennedy_replication", "kennedy_analysis_corrected.csv"))
        h = h[h.min_dist_A.notna()].reset_index(drop=True)
        rec = m.reconstruct(h)
        th = pd.read_csv(hp)
        h = h.merge(th[["acc", "pos", "tip_dist_A", "tip_nearest_feat_pos"]], on=["acc", "pos"], how="left")
        for tag, key in (("human_fitness", "fitness"), ("human_reporter", "reporter")):
            arm(h, (2 * rec[key][0] < 0.05).astype(int), tag, out)
    json.dump(out, open(os.path.join(HERE, "tip_results.json"), "w"), indent=2)
    print("\nwrote tip_results.json")
