"""Step 3 — seeded two-arm statistics for the calibration analysis.

The declared primary cohort excludes substitutions that coincide with an eligible
ACT_SITE or BINDING residue. The inclusive 0 Å arm is emitted as a named sensitivity.
Both arms are produced from the same reconstructed 166-site table and seed schedule.

Outputs
  results/analysis_all_eligible.csv            full 166-site reconstructed table
  results/analysis_final.csv                   primary 163-site exclude arm
  results/analysis_inclusive_sensitivity.csv   inclusive 166-site sensitivity arm
  results/statistics.json                      both arms plus primary-compatible keys
  results/cohort_arm_*.csv                     complete arm comparison tables
"""

import json
import os
import platform

import numpy as np
import pandas as pd
import statsmodels
import statsmodels.formula.api as smf
from scipy.stats import rankdata, spearmanr


SEED = 20260728
N_PRIMARY_BOOT = 200000
N_SENSITIVITY_BOOT = 20000
PRIMARY_COHORT = "exclude_annotation_coincident"
INCLUSIVE_COHORT = "include_annotation_coincident"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(HERE, "results")


def auc_from_ranks(y, score):
    """AUC for a binary label, with average ranks for tied scores."""
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    n1 = int(y.sum())
    n0 = int(len(y) - n1)
    if n1 == 0 or n0 == 0:
        return np.nan
    ranks = rankdata(score, method="average")
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot_auc(y, score, clusters=None, n=N_SENSITIVITY_BOOT, seed=SEED):
    """AUC with a percentile bootstrap interval."""
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    point = auc_from_ranks(y, score)
    local_rng = np.random.default_rng(seed)
    draws = []
    if clusters is None:
        for _ in range(n):
            idx = local_rng.choice(len(y), len(y), replace=True)
            if len(np.unique(y[idx])) > 1:
                draws.append(auc_from_ranks(y[idx], score[idx]))
    else:
        groups = {}
        for index, cluster in enumerate(clusters):
            groups.setdefault(cluster, []).append(index)
        keys = list(groups)
        members = {key: np.asarray(value) for key, value in groups.items()}
        for _ in range(n):
            sampled = local_rng.choice(keys, len(keys), replace=True)
            idx = np.concatenate([members[key] for key in sampled])
            if len(np.unique(y[idx])) > 1:
                draws.append(auc_from_ranks(y[idx], score[idx]))
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return float(point), float(lo), float(hi)


def build_analysis_sets():
    """Build the common table, then materialize both named cohorts."""
    sites = pd.read_csv(os.path.join(RES, "analysis_set.csv")).drop_duplicates(
        subset=["acc", "pos"]
    )
    features = pd.read_csv(os.path.join(RES, "structural_features.csv")).drop_duplicates(
        subset=["acc", "pos"]
    )
    full = sites.merge(features, on=["acc", "pos"], how="inner")
    full["y"] = full.has_pheno.astype(int)
    full["logd"] = np.log10(full.min_dist_A + 1.0)
    full["ordered"] = (full.plddt >= 70).astype(int)
    full["n_pheno"] = full.phenotypes.fillna(0)
    full["cohort_primary_exclude_annotation_coincident"] = ~full.is_itself_annot.astype(bool)
    full["cohort_inclusive_sensitivity"] = True

    primary = full.loc[full.cohort_primary_exclude_annotation_coincident].copy()
    inclusive = full.copy()
    full.to_csv(os.path.join(RES, "analysis_all_eligible.csv"), index=False)
    primary.to_csv(os.path.join(RES, "analysis_final.csv"), index=False)
    inclusive.to_csv(os.path.join(RES, "analysis_inclusive_sensitivity.csv"), index=False)
    return {PRIMARY_COHORT: primary, INCLUSIVE_COHORT: inclusive}


def analyze_cohort(data, cohort_name):
    """Run the complete parent analysis for one explicitly named cohort."""
    d = data.copy()
    y = d.y.to_numpy(int)
    dist = d.min_dist_A.to_numpy(float)
    plddt = d.plddt.to_numpy(float)
    rsa = d.rsa.to_numpy(float)

    out = {
        "cohort": cohort_name,
        "n_sites": int(len(d)),
        "n_proteins": int(d.acc.nunique()),
        "n_positive": int(y.sum()),
        "positive_rate": float(y.mean()),
    }

    auc, lo, hi = boot_auc(
        y, -dist, clusters=d.acc.to_numpy(), n=N_PRIMARY_BOOT, seed=SEED + 1
    )
    _, naive_lo, naive_hi = boot_auc(
        y, -dist, clusters=None, n=N_PRIMARY_BOOT, seed=SEED
    )
    out["auc_distance"] = {
        "auc": auc,
        "ci_low": lo,
        "ci_high": hi,
        "draws": N_PRIMARY_BOOT,
        "seed": SEED + 1,
        "bootstrap": "protein-clustered",
        "naive_site_ci_low": naive_lo,
        "naive_site_ci_high": naive_hi,
        "naive_site_draws": N_PRIMARY_BOOT,
        "naive_site_seed": SEED,
    }
    out["median_distance_positive"] = float(np.median(dist[y == 1]))
    out["median_distance_negative"] = float(np.median(dist[y == 0]))

    cutoff_rows = []
    for cutoff in (5, 8, 10, 15):
        near = dist <= cutoff
        near_positive = int((near & (y == 1)).sum())
        near_negative = int((near & (y == 0)).sum())
        far_positive = int((~near & (y == 1)).sum())
        far_negative = int((~near & (y == 0)).sum())
        odds = (
            (near_positive * far_negative) / (near_negative * far_positive)
            if near_negative and far_positive else np.nan
        )
        cutoff_rows.append({
            "cutoff_A": cutoff,
            "n_within": int(near.sum()),
            "n_positive_within": near_positive,
            "rate_within": float(y[near].mean()),
            "n_beyond": int((~near).sum()),
            "n_positive_beyond": far_positive,
            "rate_beyond": float(y[~near].mean()),
            "odds_ratio_descriptive": float(odds),
        })
    out["cutoffs"] = cutoff_rows

    logistic_rows = []
    for formula in ("y ~ logd", "y ~ logd + plddt", "y ~ logd + plddt + rsa"):
        model = smf.logit(formula, data=d).fit(
            disp=0, cov_type="cluster", cov_kwds={"groups": d.acc}
        )
        coefficient = model.params["logd"]
        se = model.bse["logd"]
        logistic_rows.append({
            "formula": formula,
            "or_per_10x_distance_plus_1A": float(np.exp(coefficient)),
            "ci_low": float(np.exp(coefficient - 1.96 * se)),
            "ci_high": float(np.exp(coefficient + 1.96 * se)),
            "p": float(model.pvalues["logd"]),
        })
    out["logistic"] = logistic_rows

    d["negloge"] = -np.log10(d.extremePheno.clip(lower=1e-12))
    out["continuous"] = {}
    for name, target in (("n_phenotypes", d.n_pheno), ("neglog_extremePheno", d.negloge)):
        rho, _ = spearmanr(dist, target)
        out["continuous"][name] = {"spearman_rho_descriptive": float(rho)}

    out["auc_other_predictors"] = {}
    for index, (name, values) in enumerate((
        ("plddt", plddt),
        ("rsa", rsa),
        ("n_annot_residues", d.n_annot_residues.to_numpy()),
    )):
        estimate, lower, upper = boot_auc(
            y, values, clusters=d.acc.to_numpy(), seed=SEED + 20 + index
        )
        out["auc_other_predictors"][name] = {
            "auc": estimate, "ci_low": lower, "ci_high": upper,
        }

    if "sift_ala_score_inv" in d.columns:
        support = d.sift_ala_score_inv.notna().to_numpy()
        support_y = y[support]
        support_score = d.sift_ala_score_inv.to_numpy()[support]
        estimate, lower, upper = boot_auc(
            support_y,
            support_score,
            clusters=d.acc.to_numpy()[support],
            seed=SEED + 10,
        )
        correlation, _ = spearmanr(np.log10(dist[support] + 1.0), support_score)
        out["sift_comparator"] = {
            "auc": estimate,
            "ci_low": lower,
            "ci_high": upper,
            "n": int(support.sum()),
            "n_positive": int(support_y.sum()),
            "spearman_logdistance_vs_sift_descriptive": {"rho": float(correlation)},
            "note": "post-result comparator; not independent validation",
        }

    out["descriptives"] = {
        "median_distance": float(np.median(dist)),
        "median_plddt": float(np.median(plddt)),
        "median_rsa": float(np.median(rsa)),
        "max_sites_per_protein": int(d.acc.value_counts().max()),
        "residue_composition": {key: int(value) for key, value in d.pmt_aa_wt.value_counts().items()},
    }
    ordered = d.plddt >= 70
    out["disorder_split_plddt70"] = {
        "ordered_n": int(ordered.sum()),
        "ordered_rate": float(y[ordered.to_numpy()].mean()),
        "disordered_n": int((~ordered).sum()),
        "disordered_rate": float(y[(~ordered).to_numpy()].mean()),
    }
    out["corr_logdistance_plddt"] = float(
        np.corrcoef(np.log10(dist + 1.0), plddt)[0, 1]
    )
    return out


def write_arm_tables(cohorts):
    estimate_rows = []
    cutoff_rows = []
    logistic_rows = []
    descriptive_rows = []
    for cohort_name, result in cohorts.items():
        estimate_rows.append({
            "cohort": cohort_name,
            "role": "primary" if cohort_name == PRIMARY_COHORT else "inclusive_sensitivity",
            "n_sites": result["n_sites"],
            "n_proteins": result["n_proteins"],
            "n_positive": result["n_positive"],
            **result["auc_distance"],
        })
        cutoff_rows.extend({"cohort": cohort_name, **row} for row in result["cutoffs"])
        logistic_rows.extend({"cohort": cohort_name, **row} for row in result["logistic"])
        composition = result["descriptives"]["residue_composition"]
        descriptive_rows.append({
            "cohort": cohort_name,
            "n_sites": result["n_sites"],
            "n_proteins": result["n_proteins"],
            "n_positive": result["n_positive"],
            "positive_rate": result["positive_rate"],
            "median_distance_positive": result["median_distance_positive"],
            "median_distance_negative": result["median_distance_negative"],
            "median_distance": result["descriptives"]["median_distance"],
            "median_plddt": result["descriptives"]["median_plddt"],
            "median_rsa": result["descriptives"]["median_rsa"],
            "serine_n": composition.get("S", 0),
            "threonine_n": composition.get("T", 0),
            "tyrosine_n": composition.get("Y", 0),
            "corr_logdistance_plddt": result["corr_logdistance_plddt"],
        })
    pd.DataFrame(estimate_rows).to_csv(os.path.join(RES, "cohort_arm_primary_estimates.csv"), index=False)
    pd.DataFrame(cutoff_rows).to_csv(os.path.join(RES, "cohort_arm_cutoffs.csv"), index=False)
    pd.DataFrame(logistic_rows).to_csv(os.path.join(RES, "cohort_arm_logistic.csv"), index=False)
    pd.DataFrame(descriptive_rows).to_csv(os.path.join(RES, "cohort_arm_descriptives.csv"), index=False)


def main():
    frames = build_analysis_sets()
    cohort_results = {
        cohort_name: analyze_cohort(frame, cohort_name)
        for cohort_name, frame in frames.items()
    }
    write_arm_tables(cohort_results)

    import Bio, scipy, sklearn
    primary = cohort_results[PRIMARY_COHORT]
    document = {
        "seed": SEED,
        "n_primary_bootstrap": N_PRIMARY_BOOT,
        "n_sensitivity_bootstrap": N_SENSITIVITY_BOOT,
        "distance_transform": "log10(distance_A + 1)",
        "primary_cohort": PRIMARY_COHORT,
        "inclusive_sensitivity_cohort": INCLUSIVE_COHORT,
        "cohorts": cohort_results,
        "inclusive_sensitivity": cohort_results[INCLUSIVE_COHORT],
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "statsmodels": statsmodels.__version__,
            "scipy": scipy.__version__,
            "scikit-learn": sklearn.__version__,
            "biopython": Bio.__version__,
        },
    }
    # Primary-compatible aliases keep downstream consumers explicit and simple.
    document.update(primary)
    for name in ("statistics.json", "cohort_arm_statistics.json"):
        with open(os.path.join(RES, name), "w") as handle:
            json.dump(document, handle, indent=1)
            handle.write("\n")

    for cohort_name, result in cohort_results.items():
        interval = result["auc_distance"]
        print(
            f"{cohort_name}: n={result['n_sites']} / proteins={result['n_proteins']} / "
            f"positive={result['n_positive']} / AUC={interval['auc']:.3f} "
            f"[{interval['ci_low']:.3f}, {interval['ci_high']:.3f}]"
        )
    print("wrote both cohort arms to results/statistics.json and cohort_arm_*.csv")


if __name__ == "__main__":
    main()
