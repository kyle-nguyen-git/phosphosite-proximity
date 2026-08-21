"""Discrimination restricted to the range the heuristic actually claims, and the cut-off contrast.

David Chang's second review point, 2026-08-18. The folk claim is local: a site a few angstroms from a
catalytic residue is worth testing first. The pooled AUC instead ranks every affected site against every
unaffected site at every distance, and in these cohorts most pairs are tens of angstroms apart, where no
one has claimed an effect. Those pairs can only pull the estimate toward 0.5.

Two things are computed here:

  1. AUC restricted to sites within 15 A and within 10 A of their nearest target. 15 A is the radius
     Strumillo et al. use, so it is not a new arbitrary cut.
  2. The cut-off contrast as a rate with a protein-cluster interval and its n, because a threshold is the
     form the heuristic is actually used in. The paper currently reports 40.0% against 49.0% with no
     interval. Methods 4.5 declares four descriptive cut-offs — 5, 8, 10 and 15 angstroms — and all four
     are run here. An earlier version of this script ran only three and dropped 8 without comment, which
     made the reported grid a selected subset of an already-declared grid.

Restriction is on the predictor, so the restricted estimand is conditional on being inside the window and
is not the pooled estimand. That is the point: it is the estimand the claim is about.

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


def auc_ci(y, score, groups, label):
    y = np.asarray(y, int)
    if y.sum() < 3 or (1 - y).sum() < 3:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
                "proteins": int(pd.Series(groups).nunique()), "auc": None,
                "note": "fewer than three sites in one class; no interval computed"}
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups), n=DRAWS, seed=SEED)
    touch = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()), "auc": round(r["estimate"], 6),
            "ci_low": None if touch else round(r["ci_low"], 6),
            "ci_high": None if touch else round(r["ci_high"], 6),
            "contains_half": bool(touch or (r["ci_low"] <= 0.5 <= r["ci_high"])),
            "draws_retained": int(r["draws"])}


def rate_diff(inside, outside, g_in, g_out, seed=SEED, n=DRAWS):
    """Affected-rate inside a cut-off minus outside, resampling whole proteins."""
    rng = np.random.default_rng(seed)
    allg = np.concatenate([np.asarray(g_in), np.asarray(g_out)])
    y = np.concatenate([np.asarray(inside, int), np.asarray(outside, int)])
    isin = np.concatenate([np.ones(len(inside), bool), np.zeros(len(outside), bool)])
    uniq = pd.unique(allg)
    idx = {u: np.flatnonzero(allg == u) for u in uniq}
    obs_in = y[isin].mean() if isin.any() else np.nan
    obs_out = y[~isin].mean() if (~isin).any() else np.nan
    draws = []
    for _ in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        rows = np.concatenate([idx[u] for u in pick])
        yi, ii = y[rows], isin[rows]
        if ii.sum() == 0 or (~ii).sum() == 0:
            continue
        draws.append(yi[ii].mean() - yi[~ii].mean())
    draws = np.asarray(draws)
    lo, hi = (np.percentile(draws, [2.5, 97.5]) if len(draws) else (np.nan, np.nan))
    return {"n_inside": int(len(inside)), "n_outside": int(len(outside)),
            "affected_inside": int(np.sum(inside)), "affected_outside": int(np.sum(outside)),
            "rate_inside": round(float(obs_in), 6), "rate_outside": round(float(obs_out), 6),
            "difference": round(float(obs_in - obs_out), 6),
            "ci_low": round(float(lo), 6), "ci_high": round(float(hi), 6),
            "excludes_zero": bool(lo > 0 or hi < 0), "draws_retained": int(len(draws)),
            "proteins": int(len(uniq))}


def cohort_arms(d, y, dist_col, tag, out):
    y = np.asarray(y, int)
    res = {"all_range": auc_ci(y, -d[dist_col], d.acc, f"{tag}: all range")}
    for cut in (15.0, 10.0, 8.0, 5.0):
        k = (d[dist_col] < cut).to_numpy()
        res[f"within_{int(cut)}A"] = auc_ci(y[k], -d[dist_col][k], d.acc[k],
                                            f"{tag}: sites within {int(cut)} A")
        res[f"cutoff_{int(cut)}A_rate"] = rate_diff(y[k], y[~k], d.acc[k], d.acc[~k])
    out[tag] = res
    print(f"--- {tag} ---")
    for cut in ("all_range", "within_15A", "within_10A", "within_8A", "within_5A"):
        r = res[cut]
        s = f"{r['auc']} [{r.get('ci_low')}, {r.get('ci_high')}]" if r.get("auc") is not None else r.get("note")
        print(f"  {cut:12s} n={r['n']:>5} pos={r['positive']:>4} prot={r['proteins']:>4}  {s}")
    for cut in (15, 10, 8, 5):
        r = res[f"cutoff_{cut}A_rate"]
        print(f"  cutoff {cut:>2} A: inside {r['affected_inside']}/{r['n_inside']} = {r['rate_inside']:.3f}"
              f" vs outside {r['rate_outside']:.3f}; difference {r['difference']:+.3f}"
              f" [{r['ci_low']:+.3f}, {r['ci_high']:+.3f}] excl0={r['excludes_zero']}")
    print(flush=True)


if __name__ == "__main__":
    out = {}
    y_ = pd.read_csv(os.path.join(RESEARCH, "phase0_calibration", "phase0_5", "results",
                                  "phase0_5_primary_analysis.csv"))
    cohort_arms(y_, y_.y, "min_dist_A", "yeast", out)

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "re_", os.path.join(RESEARCH, "kennedy_replication", "rebuild_endpoints.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    h = pd.read_csv(os.path.join(RESEARCH, "kennedy_replication", "kennedy_analysis_corrected.csv"))
    h = h[h.min_dist_A.notna()].reset_index(drop=True)
    rec = m.reconstruct(h)
    for tag, key in (("human_fitness", "fitness"), ("human_reporter", "reporter")):
        cohort_arms(h, (2 * rec[key][0] < 0.05).astype(int), "min_dist_A", tag, out)
    json.dump(out, open(os.path.join(HERE, "range_results.json"), "w"), indent=2)
    print("wrote range_results.json")
