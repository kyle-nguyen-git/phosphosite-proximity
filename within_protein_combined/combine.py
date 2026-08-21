"""Combine the within-protein estimates, and estimate the within-protein effect directly.

David Chang's fourth review point, 2026-08-18. The paper isolates the within-protein comparison three
times — yeast, human fitness, human reporter — reports three imprecise answers pointing in different
directions, and stops. The quantity a working scientist wants is the combined one.

Two things are done here.

  1. A fixed-effect and a random-effects combination of the yeast and human within-protein AUCs. The two
     human screens share all 1,470 sites and are NOT independent of each other, so only ONE human screen
     enters the combination. The fitness screen is designated, because it is the proliferation/survival
     readout the source experiment leads with; the reporter substitution is reported as a sensitivity
     arm, not added to it.

  2. A conditional logistic regression stratified on protein. The model in Section 2.2 is marginal with
     cluster-robust errors, which corrects the uncertainty for clustering but still estimates a mixed
     within-and-between effect. The conditional model estimates the within-protein effect directly and
     uses every protein carrying both outcome classes rather than only sites that form pairs.

Nothing here may enter a manuscript, wiki page or email until it is registered in NUMBERS.md.
"""
import json, os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RESEARCH, "kennedy_replication"))
import _paths                                     # noqa: E402
p05 = _paths.analysis_module()
DRAWS, SEED = 20000, 20260728


def within(d, y, tag):
    """Equal-protein-weight within-protein AUC with its protein-cluster interval, via the frozen estimator."""
    frame = pd.DataFrame({"acc": d.acc, "y": np.asarray(y, int), "dist_core_A": d.min_dist_A})
    _, w = p05.within_protein_discrimination(frame, n=DRAWS, seed=SEED)
    est = float(w["equal_protein_weight_auc"])
    lo, hi = float(w["equal_protein_weight_ci_low"]), float(w["equal_protein_weight_ci_high"])
    se = (hi - lo) / 3.919927969080108           # normal-approximation SE from a 95% interval
    return {"cohort": tag, "estimate": round(est, 6), "ci_low": round(lo, 6), "ci_high": round(hi, 6),
            "se": round(se, 6), "informative_proteins": int(w["informative_proteins"]),
            "informative_sites": int(w["informative_sites"]),
            "pair_weighted": round(float(w["pair_weighted_auc"]), 6)}


def combine(arms):
    """Inverse-variance fixed effect, DerSimonian-Laird random effects, Cochran Q and I-squared."""
    e = np.array([a["estimate"] for a in arms]); se = np.array([a["se"] for a in arms])
    w = 1 / se ** 2
    fe = float((w * e).sum() / w.sum()); fe_se = float(np.sqrt(1 / w.sum()))
    Q = float((w * (e - fe) ** 2).sum()); dfree = len(e) - 1
    C = float(w.sum() - (w ** 2).sum() / w.sum())
    tau2 = max(0.0, (Q - dfree) / C) if C > 0 else 0.0
    wr = 1 / (se ** 2 + tau2)
    re = float((wr * e).sum() / wr.sum()); re_se = float(np.sqrt(1 / wr.sum()))
    I2 = max(0.0, (Q - dfree) / Q) * 100 if Q > 0 else 0.0
    z = 1.959963984540054
    return {"cohorts": [a["cohort"] for a in arms],
            "fixed_effect": {"estimate": round(fe, 6), "ci_low": round(fe - z * fe_se, 6),
                             "ci_high": round(fe + z * fe_se, 6), "se": round(fe_se, 6),
                             "contains_half": bool(fe - z * fe_se <= 0.5 <= fe + z * fe_se)},
            "random_effects": {"estimate": round(re, 6), "ci_low": round(re - z * re_se, 6),
                               "ci_high": round(re + z * re_se, 6), "se": round(re_se, 6),
                               "tau2": round(tau2, 8),
                               "contains_half": bool(re - z * re_se <= 0.5 <= re + z * re_se)},
            "Q": round(Q, 4), "df": dfree, "I2_percent": round(I2, 2),
            "total_informative_proteins": int(sum(a["informative_proteins"] for a in arms)),
            "total_informative_sites": int(sum(a["informative_sites"] for a in arms))}


def conditional_logit(d, y, tag):
    """Within-protein effect of distance, stratified on protein. Proteins with one outcome class drop out
    of the conditional likelihood by construction, which is the point of the model."""
    from statsmodels.discrete.conditional_models import ConditionalLogit
    df = pd.DataFrame({"y": np.asarray(y, int), "acc": d.acc.values,
                       "d10": d.min_dist_A.values / 10.0})          # per 10 angstroms
    keep = df.groupby("acc").y.transform(lambda s: 0 < s.sum() < len(s))
    df = df[keep]
    if df.empty or df.acc.nunique() < 2:
        return {"cohort": tag, "note": "no informative stratum"}
    try:
        res = ConditionalLogit(df.y.values, df[["d10"]].values, groups=df.acc.values).fit(disp=0)
        b = float(res.params[0]); se = float(res.bse[0]); z = 1.959963984540054
        return {"cohort": tag, "beta_per_10A": round(b, 6), "se": round(se, 6),
                "odds_ratio_per_10A": round(float(np.exp(b)), 6),
                "or_ci_low": round(float(np.exp(b - z * se)), 6),
                "or_ci_high": round(float(np.exp(b + z * se)), 6),
                "p_value": round(float(res.pvalues[0]), 4),
                "informative_strata": int(df.acc.nunique()), "sites_used": int(len(df)),
                "contains_one": bool(np.exp(b - z * se) <= 1.0 <= np.exp(b + z * se))}
    except Exception as exc:
        return {"cohort": tag, "note": f"model did not converge: {exc}"}


if __name__ == "__main__":
    out = {}
    y_ = pd.read_csv(os.path.join(RESEARCH, "phase0_calibration", "phase0_5", "results",
                                  "phase0_5_primary_analysis.csv"))
    y_ = y_.rename(columns={"dist_core_A": "min_dist_A"}) if "min_dist_A" not in y_ else y_
    arms = {"yeast": within(y_, y_.y, "yeast")}
    cl = {"yeast": conditional_logit(y_, y_.y, "yeast")}

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "re_", os.path.join(RESEARCH, "kennedy_replication", "rebuild_endpoints.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    h = pd.read_csv(os.path.join(RESEARCH, "kennedy_replication", "kennedy_analysis_corrected.csv"))
    h = h[h.min_dist_A.notna()].reset_index(drop=True)
    rec = m.reconstruct(h)
    for tag, key in (("human_fitness", "fitness"), ("human_reporter", "reporter")):
        yy = (2 * rec[key][0] < 0.05).astype(int)
        arms[tag] = within(h, yy, tag)
        cl[tag] = conditional_logit(h, yy, tag)

    out["per_cohort"] = arms
    out["conditional_logistic"] = cl
    out["combined_designated"] = combine([arms["yeast"], arms["human_fitness"]])
    out["combined_reporter_substituted_sensitivity"] = combine([arms["yeast"], arms["human_reporter"]])
    out["designation_note"] = ("The two human screens share all 1,470 sites and are not independent, so "
                               "only one enters the combination. The fitness screen is designated; the "
                               "reporter substitution is a sensitivity arm and is not pooled with it.")
    json.dump(out, open(os.path.join(HERE, "combined_results.json"), "w"), indent=2)

    for k, a in arms.items():
        print(f"  {k:15s} {a['estimate']} [{a['ci_low']}, {a['ci_high']}]  "
              f"{a['informative_proteins']} proteins, {a['informative_sites']} sites")
    for name in ("combined_designated", "combined_reporter_substituted_sensitivity"):
        c = out[name]; fe, re = c["fixed_effect"], c["random_effects"]
        print(f"\n{name}  ({' + '.join(c['cohorts'])})")
        print(f"  fixed  {fe['estimate']} [{fe['ci_low']}, {fe['ci_high']}]  contains 0.5: {fe['contains_half']}")
        print(f"  random {re['estimate']} [{re['ci_low']}, {re['ci_high']}]  contains 0.5: {re['contains_half']}")
        print(f"  Q={c['Q']} df={c['df']} I2={c['I2_percent']}%  proteins={c['total_informative_proteins']} sites={c['total_informative_sites']}")
    print("\nconditional logistic (per 10 A):")
    for k, v in cl.items():
        if "beta_per_10A" in v:
            print(f"  {k:15s} OR {v['odds_ratio_per_10A']} [{v['or_ci_low']}, {v['or_ci_high']}] "
                  f"p={v['p_value']}  strata={v['informative_strata']} sites={v['sites_used']} contains 1: {v['contains_one']}")
        else:
            print(f"  {k:15s} {v.get('note')}")
    print("\nwrote combined_results.json")
