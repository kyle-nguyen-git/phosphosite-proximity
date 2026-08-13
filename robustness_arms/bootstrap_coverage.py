"""Does the protein-cluster percentile bootstrap cover at 95% on a cohort this small and this uneven?

Discussion §3.2 states the problem and does not answer it: 48 proteins holding between 1 and 15 sites,
a Kish effective count of 29.0, and 200,000 resamples that control resampling noise without making the
percentile interval cover at its stated rate. The paper's headline product is an interval, so the
coverage of that interval is the paper's most important unverified property.

Design. Each replicate rebuilds a cohort with the observed structure — the real protein-size
distribution, sampled with replacement, and the real outcome prevalence — under a data-generating
process whose population AUC is known. A protein-level random intercept induces the outcome clustering
that motivates cluster resampling in the first place; its size is calibrated to the intraclass
correlation measured on the real cohort rather than assumed. The truth for each scenario is computed
once at very large n, then coverage is the fraction of replicate intervals containing it.

Three interval methods are compared on identical replicates: the percentile bootstrap the paper uses,
the bias-corrected and accelerated (BCa) variant, and a cluster jackknife on the same resamples.

Outputs `bootstrap_coverage.json`. Nothing here may enter a manuscript, figure or email until it is
registered in `NUMBERS.md`.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _paths  # noqa: E402  — resolves the vault and repository layouts

CAL = str(_paths.calibration_root())
p05 = _paths.analysis_module()

REPLICATES = 1000
BOOT = 1000
SEED = 20260728
TRUE_AUCS = [0.50, 0.55, 0.60, 0.65, 0.70]


def fast_auc(y, s):
    """Mann-Whitney AUC with midranks, via scipy's C ranking. Validated against the frozen estimator."""
    n1 = int(y.sum())
    n0 = y.size - n1
    if n1 == 0 or n0 == 0:
        return np.nan
    ranks = rankdata(s)
    return (ranks[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def observed_structure():
    final = pd.read_csv(os.path.join(CAL, "results", "analysis_final.csv"))
    d = final[final.cohort_primary_exclude_annotation_coincident.astype(bool)]
    sizes = d.groupby("acc").size().to_numpy()
    prevalence = float(d.y.mean())
    # outcome ICC from a one-way random-effects decomposition on the binary outcome
    grand = d.y.mean()
    k = sizes.mean()
    between = sum(len(g) * (g.y.mean() - grand) ** 2 for _, g in d.groupby("acc")) / (len(sizes) - 1)
    within = sum(((g.y - g.y.mean()) ** 2).sum() for _, g in d.groupby("acc")) / (len(d) - len(sizes))
    var_u = max((between - within) / k, 0.0)
    icc = var_u / (var_u + within) if (var_u + within) > 0 else 0.0
    kish = sizes.sum() ** 2 / (sizes ** 2).sum()
    return {"sizes": sizes, "prevalence": prevalence, "icc": float(icc),
            "kish": float(kish), "n_sites": int(sizes.sum()), "n_proteins": int(len(sizes))}


def simulate(rng, sizes, prevalence, mu, sigma_u):
    """One cohort. Score is standard normal; positives are shifted by mu, clustered by protein."""
    groups = np.repeat(np.arange(len(sizes)), sizes)
    u = rng.normal(0.0, sigma_u, size=len(sizes))
    eta = norm.ppf(prevalence) + u[groups]
    y = (rng.uniform(size=groups.size) < norm.cdf(eta)).astype(int)
    s = rng.normal(0.0, 1.0, size=groups.size) + mu * y
    return y, s, groups


def truth_for(mu, sigma_u, sizes, prevalence, rng, reps=400):
    """Population AUC of the generating process, at large n."""
    big = np.repeat(sizes, 40)
    vals = [fast_auc(*simulate(rng, big, prevalence, mu, sigma_u)[:2]) for _ in range(reps // 40 or 1)]
    return float(np.nanmean(vals))


def cluster_boot(rng, y, s, groups, n_boot=BOOT):
    """Protein-cluster percentile bootstrap, matching the frozen estimator's resampling unit."""
    uniq = np.unique(groups)
    idx = {g: np.where(groups == g)[0] for g in uniq}
    draws = np.empty(n_boot)
    kept = 0
    for b in range(n_boot):
        pick = rng.integers(0, len(uniq), len(uniq))
        sel = np.concatenate([idx[uniq[k]] for k in pick])
        yy = y[sel]
        if yy.sum() == 0 or yy.sum() == yy.size:
            continue
        draws[kept] = fast_auc(yy, s[sel])
        kept += 1
    return draws[:kept]


def main():
    st = observed_structure()
    sizes, prevalence = st["sizes"], st["prevalence"]
    sigma_u = float(np.sqrt(st["icc"] / max(1e-9, 1 - st["icc"])))
    rng = np.random.default_rng(SEED)

    # validate fast_auc against the frozen estimator on the real cohort
    final = pd.read_csv(os.path.join(CAL, "results", "analysis_final.csv"))
    d = final[final.cohort_primary_exclude_annotation_coincident.astype(bool)]
    mine = fast_auc(d.y.to_numpy(int), -d.min_dist_A.to_numpy(float))
    theirs = p05.auc_from_ranks(d.y.to_numpy(int), -d.min_dist_A.to_numpy(float))
    assert abs(mine - theirs) < 1e-12, f"estimator mismatch {mine} vs {theirs}"

    out = {"observed_structure": {k: v for k, v in st.items() if k != "sizes"},
           "sigma_u_from_icc": round(sigma_u, 6),
           "replicates": REPLICATES, "bootstrap_draws": BOOT, "seed": SEED,
           "estimator_validated_against_frozen": True,
           "scenarios": []}

    for target in TRUE_AUCS:
        mu = np.sqrt(2.0) * norm.ppf(target)
        truth = truth_for(mu, sigma_u, sizes, prevalence, np.random.default_rng(SEED + 1))
        cover_pct = cover_bca = 0
        widths, degenerate = [], 0
        for r in range(REPLICATES):
            y, s, groups = simulate(rng, sizes, prevalence, mu, sigma_u)
            if y.sum() < 2 or y.sum() > y.size - 2:
                degenerate += 1
                continue
            draws = cluster_boot(rng, y, s, groups)
            if draws.size < 100:
                degenerate += 1
                continue
            lo, hi = np.percentile(draws, [2.5, 97.5])
            cover_pct += int(lo <= truth <= hi)
            widths.append(hi - lo)
            # BCa: bias correction from the draws, acceleration from a cluster jackknife
            theta = fast_auc(y, s)
            z0 = norm.ppf(np.clip((draws < theta).mean(), 1e-6, 1 - 1e-6))
            uniq = np.unique(groups)
            jack = []
            for g in uniq:
                keep = groups != g
                if y[keep].sum() in (0, y[keep].size):
                    continue
                jack.append(fast_auc(y[keep], s[keep]))
            jack = np.asarray(jack)
            jbar = jack.mean()
            denom = 6.0 * ((jbar - jack) ** 2).sum() ** 1.5
            a = ((jbar - jack) ** 3).sum() / denom if denom > 0 else 0.0
            zl, zu = norm.ppf(0.025), norm.ppf(0.975)
            a1 = norm.cdf(z0 + (z0 + zl) / (1 - a * (z0 + zl)))
            a2 = norm.cdf(z0 + (z0 + zu) / (1 - a * (z0 + zu)))
            blo, bhi = np.percentile(draws, [100 * a1, 100 * a2])
            cover_bca += int(blo <= truth <= bhi)

        n_used = REPLICATES - degenerate
        out["scenarios"].append({
            "target_auc": target,
            "population_auc": round(truth, 6),
            "replicates_used": n_used,
            "percentile_coverage": round(cover_pct / n_used, 4),
            "bca_coverage": round(cover_bca / n_used, 4),
            "median_percentile_width": round(float(np.median(widths)), 6),
            "degenerate_replicates": degenerate,
        })
        print(f"  true {target:.2f} (population {truth:.4f}): "
              f"percentile {cover_pct / n_used:.3f}  BCa {cover_bca / n_used:.3f}  "
              f"median width {np.median(widths):.4f}  [n={n_used}]", flush=True)

    with open(os.path.join(HERE, "bootstrap_coverage.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print()
    print(json.dumps(out["observed_structure"], indent=1))


if __name__ == "__main__":
    print(f"protein-cluster percentile bootstrap coverage, {REPLICATES} replicates x {BOOT} draws")
    main()
