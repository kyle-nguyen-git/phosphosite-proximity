"""Phase 0.5 robustness, continuous-outcome, and predictor-benchmark analyses."""

from __future__ import annotations

import json
import os
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
import sklearn
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import rankdata, spearmanr
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


SEED = 20260728
N_PRIMARY_BOOT = 200000
N_SENSITIVITY_BOOT = 20000
N_CORR_BOOT = 4000
N_WILD = 9999
PRIMARY_COHORT = "exclude_annotation_coincident"
INCLUSIVE_COHORT = "include_annotation_coincident"
HERE = Path(__file__).resolve().parents[1]
RESULTS = HERE / "results"


def to_builtin(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    raise TypeError(f"cannot serialize {type(value)}")


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


def bootstrap_auc(y, score, groups=None, n=N_SENSITIVITY_BOOT, seed=SEED):
    """AUC and percentile CI using either sites or proteins as resampling units."""
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    point = auc_from_ranks(y, score)
    rng = np.random.default_rng(seed)
    draws = []
    if groups is None:
        for _ in range(n):
            idx = rng.choice(len(y), len(y), replace=True)
            if np.unique(y[idx]).size == 2:
                draws.append(auc_from_ranks(y[idx], score[idx]))
    else:
        groups = np.asarray(groups)
        unique_groups = np.unique(groups)
        indices = {group: np.flatnonzero(groups == group) for group in unique_groups}
        for _ in range(n):
            sampled = rng.choice(unique_groups, len(unique_groups), replace=True)
            idx = np.concatenate([indices[group] for group in sampled])
            if np.unique(y[idx]).size == 2:
                draws.append(auc_from_ranks(y[idx], score[idx]))
    low, high = np.percentile(draws, [2.5, 97.5])
    return {"estimate": point, "ci_low": float(low), "ci_high": float(high), "draws": len(draws)}


def paired_auc_difference(y, score_a, score_b, groups, n=N_SENSITIVITY_BOOT, seed=SEED):
    """Protein-bootstrap interval for AUC(score_a) minus AUC(score_b)."""
    y = np.asarray(y, dtype=int)
    score_a = np.asarray(score_a, dtype=float)
    score_b = np.asarray(score_b, dtype=float)
    groups = np.asarray(groups)
    point = auc_from_ranks(y, score_a) - auc_from_ranks(y, score_b)
    rng = np.random.default_rng(seed)
    unique_groups = np.unique(groups)
    indices = {group: np.flatnonzero(groups == group) for group in unique_groups}
    draws = []
    for _ in range(n):
        sampled = rng.choice(unique_groups, len(unique_groups), replace=True)
        idx = np.concatenate([indices[group] for group in sampled])
        if np.unique(y[idx]).size == 2:
            draws.append(
                auc_from_ranks(y[idx], score_a[idx]) - auc_from_ranks(y[idx], score_b[idx])
            )
    low, high = np.percentile(draws, [2.5, 97.5])
    return {"estimate": float(point), "ci_low": float(low), "ci_high": float(high), "draws": len(draws)}


def cluster_boot_spearman(x, y, groups, n=N_CORR_BOOT, seed=SEED):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    groups = np.asarray(groups)
    point, _ = spearmanr(x, y)
    rng = np.random.default_rng(seed)
    unique_groups = np.unique(groups)
    indices = {group: np.flatnonzero(groups == group) for group in unique_groups}
    draws = []
    for _ in range(n):
        sampled = rng.choice(unique_groups, len(unique_groups), replace=True)
        idx = np.concatenate([indices[group] for group in sampled])
        rho, _ = spearmanr(x[idx], y[idx])
        if np.isfinite(rho):
            draws.append(rho)
    low, high = np.percentile(draws, [2.5, 97.5])
    return {
        "rho": float(point),
        "ci_low": float(low),
        "ci_high": float(high),
    }


def within_protein_discrimination(d, n=N_SENSITIVITY_BOOT, seed=SEED):
    """AUC using only positive-negative comparisons within the same protein."""
    rows = []
    for acc, subset in d.groupby("acc", sort=True):
        if subset.y.nunique() != 2:
            continue
        n_positive = int(subset.y.sum())
        n_negative = int(len(subset) - n_positive)
        rows.append(
            {
                "acc": acc,
                "n_sites": int(len(subset)),
                "n_positive": n_positive,
                "n_negative": n_negative,
                "positive_negative_pairs": n_positive * n_negative,
                "within_protein_auc": auc_from_ranks(subset.y, -subset.dist_core_A),
            }
        )
    detail = pd.DataFrame(rows)
    if detail.empty:
        raise RuntimeError("no proteins contain both outcome classes")
    pair_weighted = float(
        np.average(detail.within_protein_auc, weights=detail.positive_negative_pairs)
    )
    equal_weighted = float(detail.within_protein_auc.mean())
    rng = np.random.default_rng(seed)
    pair_draws, equal_draws = [], []
    for _ in range(n):
        sampled = detail.iloc[rng.integers(0, len(detail), len(detail))]
        pair_draws.append(
            np.average(sampled.within_protein_auc, weights=sampled.positive_negative_pairs)
        )
        equal_draws.append(sampled.within_protein_auc.mean())
    all_positive = int(sum((subset.y == 1).all() for _, subset in d.groupby("acc")))
    all_negative = int(sum((subset.y == 0).all() for _, subset in d.groupby("acc")))
    return detail, {
        "informative_proteins": int(len(detail)),
        "informative_sites": int(detail.n_sites.sum()),
        "within_protein_positive_negative_pairs": int(detail.positive_negative_pairs.sum()),
        "all_positive_proteins": all_positive,
        "all_negative_proteins": all_negative,
        "pair_weighted_auc": pair_weighted,
        "pair_weighted_ci_low": float(np.percentile(pair_draws, 2.5)),
        "pair_weighted_ci_high": float(np.percentile(pair_draws, 97.5)),
        "equal_protein_weight_auc": equal_weighted,
        "equal_protein_weight_ci_low": float(np.percentile(equal_draws, 2.5)),
        "equal_protein_weight_ci_high": float(np.percentile(equal_draws, 97.5)),
    }


def cluster_covariance(x, residual, groups):
    """CR1 covariance for OLS, used by the wild-cluster bootstrap."""
    x = np.asarray(x, dtype=float)
    residual = np.asarray(residual, dtype=float)
    groups = np.asarray(groups)
    n, k = x.shape
    unique_groups = np.unique(groups)
    xtx_inv = np.linalg.inv(x.T @ x)
    meat = np.zeros((k, k), dtype=float)
    for group in unique_groups:
        mask = groups == group
        score = x[mask].T @ residual[mask]
        meat += np.outer(score, score)
    g = len(unique_groups)
    correction = (g / (g - 1)) * ((n - 1) / (n - k))
    return correction * xtx_inv @ meat @ xtx_inv


def wild_cluster_lpm(d, n=N_WILD, seed=SEED):
    """Rademacher wild-cluster bootstrap-t for an adjusted linear probability model."""
    y = d["y"].to_numpy(float)
    groups = d["acc"].to_numpy()
    x = sm.add_constant(d[["logd", "plddt", "rsa"]], has_constant="add").to_numpy(float)
    z = sm.add_constant(d[["plddt", "rsa"]], has_constant="add").to_numpy(float)

    beta_full = np.linalg.solve(x.T @ x, x.T @ y)
    residual_full = y - x @ beta_full
    covariance_full = cluster_covariance(x, residual_full, groups)
    t_observed = beta_full[1] / np.sqrt(covariance_full[1, 1])

    beta_restricted = np.linalg.solve(z.T @ z, z.T @ y)
    fitted_restricted = z @ beta_restricted
    residual_restricted = y - fitted_restricted
    unique_groups = np.unique(groups)
    group_index = {group: index for index, group in enumerate(unique_groups)}
    row_group = np.array([group_index[group] for group in groups])

    rng = np.random.default_rng(seed)
    exceed = 0
    finite = 0
    xtx_inv = np.linalg.inv(x.T @ x)
    for _ in range(n):
        weights = rng.choice((-1.0, 1.0), size=len(unique_groups))
        y_star = fitted_restricted + residual_restricted * weights[row_group]
        beta_star = xtx_inv @ x.T @ y_star
        residual_star = y_star - x @ beta_star
        covariance_star = cluster_covariance(x, residual_star, groups)
        variance = covariance_star[1, 1]
        if variance <= 0 or not np.isfinite(variance):
            continue
        t_star = beta_star[1] / np.sqrt(variance)
        finite += 1
        exceed += int(abs(t_star) >= abs(t_observed))
    p_value = (exceed + 1) / (finite + 1)
    return {
        "model": "linear probability: y ~ log10(distance_A + 1) + pLDDT + RSA",
        "coefficient_log10_distance_plus_1A": float(beta_full[1]),
        "cluster_robust_se": float(np.sqrt(covariance_full[1, 1])),
        "t_observed": float(t_observed),
        "wild_cluster_p": float(p_value),
        "bootstrap_draws": int(finite),
        "weight": "Rademacher",
        "clusters": int(len(unique_groups)),
    }


def repeated_grouped_predictions(d, features, repeats=10, folds=5):
    """Average probabilities from repeated stratified group five-fold splits.

    Leaving out one protein at a time makes each fold's training prevalence a deterministic inverse
    function of that protein's labels. That creates a mechanically anti-predictive intercept. Five-fold
    grouped splits preserve protein isolation without that one-cluster prevalence artifact.
    """
    x = d[features].copy()
    y = d["y"].to_numpy(int)
    groups = d["acc"].to_numpy()
    prediction_sum = np.zeros(len(d), dtype=float)
    prediction_count = np.zeros(len(d), dtype=int)
    repeat_auc = []
    repeat_brier = []
    for repeat in range(repeats):
        splitter = StratifiedGroupKFold(
            n_splits=folds, shuffle=True, random_state=SEED + repeat
        )
        repeat_predictions = np.full(len(d), np.nan)
        fold_auc_weighted_sum = 0.0
        fold_pair_weight_sum = 0
        for train, test in splitter.split(x, y, groups):
            transformer = ColumnTransformer(
                [("numeric", Pipeline([
                    ("impute", SimpleImputer(strategy="median", add_indicator=True)),
                    ("scale", StandardScaler()),
                ]), features)],
                remainder="drop",
            )
            model = Pipeline([
                ("prepare", transformer),
                ("logistic", LogisticRegression(
                    penalty="l2", C=1.0, solver="liblinear", random_state=SEED, max_iter=5000
                )),
            ])
            model.fit(x.iloc[train], y[train])
            fold_predictions = model.predict_proba(x.iloc[test])[:, 1]
            prediction_sum[test] += fold_predictions
            prediction_count[test] += 1
            repeat_predictions[test] = fold_predictions
            n_positive = int(y[test].sum())
            n_negative = int(len(test) - n_positive)
            if n_positive and n_negative:
                pair_weight = n_positive * n_negative
                fold_auc_weighted_sum += roc_auc_score(y[test], fold_predictions) * pair_weight
                fold_pair_weight_sum += pair_weight
        repeat_auc.append(fold_auc_weighted_sum / fold_pair_weight_sum)
        repeat_brier.append(brier_score_loss(y, repeat_predictions))
    if not np.all(prediction_count == repeats):
        raise RuntimeError("grouped cross-validation did not predict every row once per repeat")
    return {
        "predictions": prediction_sum / prediction_count,
        "repeat_auc": np.asarray(repeat_auc),
        "repeat_brier": np.asarray(repeat_brier),
    }


def main() -> None:
    all_data = pd.read_csv(RESULTS / "phase0_5_analysis.csv")
    all_data["y"] = all_data["has_pheno"].astype(int)
    all_data["logd"] = np.log10(all_data["dist_core_A"] + 1.0)
    all_data["log_n_annot"] = np.log1p(all_data["n_core_residues"])
    all_data["log_protein_length"] = np.log10(all_data["protein_length"])
    all_data["supp_is_disopred"] = all_data["supp_is_disopred"].astype(float)
    all_data["cohort_primary_exclude_annotation_coincident"] = (
        ~all_data.is_itself_annot.astype(bool)
    )
    all_data["cohort_inclusive_sensitivity"] = True

    primary_data = all_data.loc[
        all_data.cohort_primary_exclude_annotation_coincident
    ].copy()
    inclusive_data = all_data.copy()
    legacy_data = all_data.loc[
        all_data.in_supplementary_data_6.astype(bool)
        & ~all_data.is_itself_annot.astype(bool)
        & ~all_data.position_resolution.str.contains("resolved", na=False)
    ].copy()
    d = primary_data
    primary_data.to_csv(RESULTS / "phase0_5_primary_analysis.csv", index=False)
    inclusive_data.to_csv(
        RESULTS / "phase0_5_inclusive_sensitivity_analysis.csv", index=False
    )

    summary = {
        "seed": SEED,
        "n_primary_bootstrap": N_PRIMARY_BOOT,
        "n_sensitivity_bootstrap": N_SENSITIVITY_BOOT,
        "n_correlation_bootstrap": N_CORR_BOOT,
        "n_wild_cluster": N_WILD,
        "distance_transform": "log10(distance_A + 1)",
        "primary_cohort": PRIMARY_COHORT,
        "inclusive_sensitivity_cohort": INCLUSIVE_COHORT,
        "n_sites": int(len(d)),
        "n_proteins": int(d.acc.nunique()),
        "n_positive": int(d.y.sum()),
        "cohort_counts": {
            PRIMARY_COHORT: {
                "n_sites": int(len(primary_data)),
                "n_proteins": int(primary_data.acc.nunique()),
                "n_positive": int(primary_data.y.sum()),
            },
            INCLUSIVE_COHORT: {
                "n_sites": int(len(inclusive_data)),
                "n_proteins": int(inclusive_data.acc.nunique()),
                "n_positive": int(inclusive_data.y.sum()),
            },
        },
    }

    # Primary estimate and inclusive sensitivity use the same seed schedule.
    summary["primary_auc"] = {
        "site_bootstrap": bootstrap_auc(
            d.y, -d.dist_core_A, n=N_PRIMARY_BOOT, seed=SEED
        ),
        "protein_cluster_bootstrap": bootstrap_auc(
            d.y, -d.dist_core_A, groups=d.acc, n=N_PRIMARY_BOOT, seed=SEED + 1
        ),
    }
    summary["inclusive_sensitivity_auc"] = {
        "site_bootstrap": bootstrap_auc(
            inclusive_data.y,
            -inclusive_data.dist_core_A,
            n=N_PRIMARY_BOOT,
            seed=SEED,
        ),
        "protein_cluster_bootstrap": bootstrap_auc(
            inclusive_data.y,
            -inclusive_data.dist_core_A,
            groups=inclusive_data.acc,
            n=N_PRIMARY_BOOT,
            seed=SEED + 1,
        ),
    }

    arm_estimates = pd.DataFrame([
        {
            "cohort": PRIMARY_COHORT,
            "role": "primary",
            "n_sites": int(len(primary_data)),
            "n_proteins": int(primary_data.acc.nunique()),
            "n_positive": int(primary_data.y.sum()),
            **summary["primary_auc"]["protein_cluster_bootstrap"],
        },
        {
            "cohort": INCLUSIVE_COHORT,
            "role": "inclusive_sensitivity",
            "n_sites": int(len(inclusive_data)),
            "n_proteins": int(inclusive_data.acc.nunique()),
            "n_positive": int(inclusive_data.y.sum()),
            **summary["inclusive_sensitivity_auc"]["protein_cluster_bootstrap"],
        },
    ])
    arm_estimates.to_csv(RESULTS / "cohort_arm_primary_estimates.csv", index=False)

    cutoff_rows = []
    descriptive_rows = []
    for cohort_name, frame in (
        (PRIMARY_COHORT, primary_data),
        (INCLUSIVE_COHORT, inclusive_data),
    ):
        for cutoff in (5, 8, 10, 15):
            near = frame.dist_core_A <= cutoff
            near_positive = int(frame.loc[near, "y"].sum())
            near_negative = int(near.sum() - near_positive)
            far_positive = int(frame.loc[~near, "y"].sum())
            far_negative = int((~near).sum() - far_positive)
            odds = (
                (near_positive * far_negative) / (near_negative * far_positive)
                if near_negative and far_positive else np.nan
            )
            cutoff_rows.append({
                "cohort": cohort_name,
                "cutoff_A": cutoff,
                "n_within": int(near.sum()),
                "n_positive_within": near_positive,
                "rate_within": float(frame.loc[near, "y"].mean()),
                "n_beyond": int((~near).sum()),
                "n_positive_beyond": far_positive,
                "rate_beyond": float(frame.loc[~near, "y"].mean()),
                "odds_ratio_descriptive": float(odds),
            })
        composition = frame.pmt_aa_wt.value_counts()
        descriptive_rows.append({
            "cohort": cohort_name,
            "n_sites": int(len(frame)),
            "n_proteins": int(frame.acc.nunique()),
            "n_positive": int(frame.y.sum()),
            "positive_rate": float(frame.y.mean()),
            "median_distance_positive": float(frame.loc[frame.y == 1, "dist_core_A"].median()),
            "median_distance_negative": float(frame.loc[frame.y == 0, "dist_core_A"].median()),
            "median_distance": float(frame.dist_core_A.median()),
            "median_plddt": float(frame.plddt.median()),
            "median_rsa": float(frame.rsa.median()),
            "serine_n": int(composition.get("S", 0)),
            "threonine_n": int(composition.get("T", 0)),
            "tyrosine_n": int(composition.get("Y", 0)),
            "corr_logdistance_plddt": float(
                np.corrcoef(np.log10(frame.dist_core_A + 1.0), frame.plddt)[0, 1]
            ),
        })
    cutoff_table = pd.DataFrame(cutoff_rows)
    descriptive_table = pd.DataFrame(descriptive_rows)
    cutoff_table.to_csv(RESULTS / "cohort_arm_cutoffs.csv", index=False)
    descriptive_table.to_csv(RESULTS / "cohort_arm_descriptives.csv", index=False)
    summary["cohort_arm_cutoffs"] = cutoff_rows
    summary["cohort_arm_descriptives"] = descriptive_rows

    # Identification checks: remove across-protein distance-scale comparisons,
    # and separately normalize distances to each protein's empirical scale.
    within_detail, within_summary = within_protein_discrimination(d, seed=SEED + 2)
    within_detail.to_csv(RESULTS / "within_protein_auc.csv", index=False)
    summary["within_protein_discrimination"] = within_summary
    d["within_protein_distance_percentile"] = d.groupby("acc")["dist_core_A"].rank(
        method="average", pct=True
    )
    summary["within_protein_distance_percentile_auc"] = bootstrap_auc(
        d.y,
        -d.within_protein_distance_percentile,
        groups=d.acc,
        seed=SEED + 3,
    )

    # Cluster-robust regression sequence for both declared cohort arms.
    regression_rows = []
    for cohort_name, frame in (
        (PRIMARY_COHORT, primary_data),
        (INCLUSIVE_COHORT, inclusive_data),
    ):
        for formula in (
            "y ~ logd",
            "y ~ logd + plddt + rsa",
            "y ~ logd + plddt + rsa + pae_pair_max",
            "y ~ logd + plddt + rsa + C(pmt_aa_wt)",
            "y ~ logd + plddt + rsa + log_n_annot + log_protein_length + C(pmt_aa_wt)",
        ):
            model = smf.logit(formula, data=frame).fit(
                disp=0, cov_type="cluster", cov_kwds={"groups": frame.acc}
            )
            coefficient = model.params["logd"]
            se = model.bse["logd"]
            regression_rows.append(
                {
                    "cohort": cohort_name,
                    "formula": formula,
                    "or_per_10x_distance_plus_1A": float(np.exp(coefficient)),
                    "ci_low": float(np.exp(coefficient - 1.96 * se)),
                    "ci_high": float(np.exp(coefficient + 1.96 * se)),
                    "cluster_p": float(model.pvalues["logd"]),
                }
            )
    regression = pd.DataFrame(regression_rows)
    regression.to_csv(RESULTS / "regression_models.csv", index=False)
    summary["regression_models"] = regression_rows

    # Post-result sequence-constraint comparator on common support for both arms.
    sift_rows = []
    sift_results = {}
    for cohort_name, frame, seed_offset in (
        (PRIMARY_COHORT, primary_data, 0),
        (INCLUSIVE_COHORT, inclusive_data, 0),
        ("legacy_158", legacy_data, 4),
    ):
        common = frame.loc[frame.sift_ala_score_inv.notna()].copy()
        sift_auc = bootstrap_auc(
            common.y,
            common.sift_ala_score_inv,
            groups=common.acc,
            seed=SEED + 10 + seed_offset,
        )
        distance_auc = bootstrap_auc(
            common.y,
            -common.dist_core_A,
            groups=common.acc,
            seed=SEED + 11 + seed_offset,
        )
        difference = paired_auc_difference(
            common.y,
            common.sift_ala_score_inv,
            -common.dist_core_A,
            common.acc,
            seed=SEED + 12 + seed_offset,
        )
        correlation = cluster_boot_spearman(
            common.logd,
            common.sift_ala_score_inv,
            common.acc,
            seed=SEED + 13 + seed_offset,
        )
        sift_results[cohort_name] = {
            "n_sites": int(len(common)),
            "n_proteins": int(common.acc.nunique()),
            "n_positive": int(common.y.sum()),
            "sift_auc": sift_auc,
            "distance_auc": distance_auc,
            "sift_minus_distance_auc": difference,
            "correlation_log10_distance_plus_1A_vs_sift": correlation,
        }
        sift_rows.append({
            "cohort": cohort_name,
            "n_sites": int(len(common)),
            "n_proteins": int(common.acc.nunique()),
            "n_positive": int(common.y.sum()),
            "sift_auc": sift_auc["estimate"],
            "sift_ci_low": sift_auc["ci_low"],
            "sift_ci_high": sift_auc["ci_high"],
            "distance_auc": distance_auc["estimate"],
            "distance_ci_low": distance_auc["ci_low"],
            "distance_ci_high": distance_auc["ci_high"],
            "sift_minus_distance": difference["estimate"],
            "difference_ci_low": difference["ci_low"],
            "difference_ci_high": difference["ci_high"],
        })
    summary["sift_sequence_constraint_diagnostic"] = {
        "timing": "post-result diagnostic",
        "cohorts": sift_results,
        **sift_results[PRIMARY_COHORT],
    }
    pd.DataFrame(sift_rows).to_csv(
        RESULTS / "sift_comparator_sensitivity.csv", index=False
    )

    # Confidence strata: the PAE restriction directly addresses uncertainty in pairwise geometry.
    strata = {
        "all": np.ones(len(d), dtype=bool),
        "site_plddt_ge_50": d.plddt >= 50,
        "site_plddt_ge_70": d.plddt >= 70,
        "site_and_target_plddt_ge_70": (d.plddt >= 70) & (d.nearest_core_plddt >= 70),
        "site_plddt_ge_90": d.plddt >= 90,
        "site_and_target_plddt_ge_90": (d.plddt >= 90) & (d.nearest_core_plddt >= 90),
        "pair_pae_max_le_5": d.pae_pair_max <= 5,
        "pair_pae_max_le_10": d.pae_pair_max <= 10,
        "pair_pae_max_le_15": d.pae_pair_max <= 15,
        "high_confidence_joint": (
            (d.plddt >= 70) & (d.nearest_core_plddt >= 70) & (d.pae_pair_max <= 10)
        ),
        "very_high_confidence_joint": (
            (d.plddt >= 90) & (d.nearest_core_plddt >= 90) & (d.pae_pair_max <= 10)
        ),
    }
    confidence_rows = []
    for cohort_name, frame, all_interval, confidence_seed_base in (
        (
            PRIMARY_COHORT,
            primary_data,
            summary["primary_auc"]["protein_cluster_bootstrap"],
            30,
        ),
        (
            INCLUSIVE_COHORT,
            inclusive_data,
            summary["inclusive_sensitivity_auc"]["protein_cluster_bootstrap"],
            20,
        ),
    ):
        cohort_strata = {
            "all": np.ones(len(frame), dtype=bool),
            "site_plddt_ge_50": frame.plddt >= 50,
            "site_plddt_ge_70": frame.plddt >= 70,
            "site_and_target_plddt_ge_70": (
                (frame.plddt >= 70) & (frame.nearest_core_plddt >= 70)
            ),
            "site_plddt_ge_90": frame.plddt >= 90,
            "site_and_target_plddt_ge_90": (
                (frame.plddt >= 90) & (frame.nearest_core_plddt >= 90)
            ),
            "pair_pae_max_le_5": frame.pae_pair_max <= 5,
            "pair_pae_max_le_10": frame.pae_pair_max <= 10,
            "pair_pae_max_le_15": frame.pae_pair_max <= 15,
            "high_confidence_joint": (
                (frame.plddt >= 70)
                & (frame.nearest_core_plddt >= 70)
                & (frame.pae_pair_max <= 10)
            ),
            "very_high_confidence_joint": (
                (frame.plddt >= 90)
                & (frame.nearest_core_plddt >= 90)
                & (frame.pae_pair_max <= 10)
            ),
        }
        for index, (name, mask) in enumerate(cohort_strata.items()):
            subset = frame.loc[mask].copy()
            row = {
                "cohort": cohort_name,
                "stratum": name,
                "n_sites": len(subset),
                "n_proteins": subset.acc.nunique(),
                "n_positive": int(subset.y.sum()),
            }
            if name == "all":
                row.update(all_interval)
            elif len(subset) >= 4 and subset.y.nunique() == 2:
                row.update(
                    bootstrap_auc(
                        subset.y,
                        -subset.dist_core_A,
                        groups=subset.acc,
                        seed=SEED + confidence_seed_base + index,
                    )
                )
            confidence_rows.append(row)
    confidence = pd.DataFrame(confidence_rows)
    confidence.to_csv(RESULTS / "confidence_strata.csv", index=False)
    summary["confidence_strata"] = {
        cohort_name: confidence.loc[confidence.cohort == cohort_name]
        .drop(columns="cohort")
        .to_dict(orient="records")
        for cohort_name in (PRIMARY_COHORT, INCLUSIVE_COHORT)
    }

    # PAE-definition multiverse. The primary sensitivity uses the maximum of
    # the two directed PAE entries; all four available summaries are shown so
    # that this conservative, outcome-known choice cannot be mistaken for a
    # uniquely defined measurement.
    pae_columns = {
        "pae_pair_max": "maximum of both directed entries",
        "pae_site_to_target": "site to target",
        "pae_pair_mean": "mean of both directed entries",
        "pae_target_to_site": "target to site",
    }
    pae_at10_rows = []
    pae_grid_rows = []
    for cohort_name, cohort in (
        (PRIMARY_COHORT, primary_data),
        (INCLUSIVE_COHORT, inclusive_data),
        ("legacy_158", legacy_data),
    ):
        for column, definition in pae_columns.items():
            at10 = cohort[cohort[column] <= 10]
            pae_at10_rows.append({
                "cohort": cohort_name,
                "pae_column": column,
                "definition": definition,
                "threshold_A": 10,
                "n_sites": int(len(at10)),
                "n_proteins": int(at10.acc.nunique()),
                "n_positive": int(at10.y.sum()),
                "auc": auc_from_ranks(at10.y, -at10.dist_core_A),
            })
            for threshold in (5, 10, 15, 20, 25, 30):
                for site_plddt_floor in (0, 50, 70):
                    subset = cohort[
                        (cohort[column] <= threshold)
                        & (cohort.plddt >= site_plddt_floor)
                    ]
                    estimate = np.nan
                    if len(subset) and subset.y.nunique() == 2:
                        estimate = auc_from_ranks(subset.y, -subset.dist_core_A)
                    pae_grid_rows.append({
                        "cohort": cohort_name,
                        "pae_column": column,
                        "pae_threshold_A": threshold,
                        "site_plddt_floor": site_plddt_floor,
                        "n_sites": int(len(subset)),
                        "n_proteins": int(subset.acc.nunique()),
                        "n_positive": int(subset.y.sum()),
                        "auc": estimate,
                    })
    pae_at10 = pd.DataFrame(pae_at10_rows)
    pae_at10.to_csv(RESULTS / "pae_column_sensitivity_at_10A.csv", index=False)
    pae_grid = pd.DataFrame(pae_grid_rows)
    pae_grid["auc_rank_low_to_high_within_cohort"] = pae_grid.groupby("cohort")["auc"].rank(
        method="min", ascending=True
    )
    pae_grid.to_csv(RESULTS / "pae_filter_grid_72x3.csv", index=False)
    summary["pae_column_sensitivity_at_10A"] = pae_at10.to_dict(orient="records")
    summary["pae_filter_grid"] = {
        cohort_name: {
            "n_cells": int(len(frame)),
            "auc_min": float(frame.auc.min()),
            "auc_max": float(frame.auc.max()),
            "minimum_cell": frame.loc[frame.auc.idxmin()].to_dict(),
            "maximum_cell": frame.loc[frame.auc.idxmax()].to_dict(),
        }
        for cohort_name, frame in pae_grid.groupby("cohort")
    }

    # Alternative feature definitions are sensitivities, not competing primary analyses.
    definition_rows = []
    for index, column in enumerate(
        ["dist_act_site_A", "dist_binding_A", "dist_core_A", "dist_core_plus_site_A", "dist_all_with_dna_bind_A"]
    ):
        subset = d[d[column].notna()].copy()
        row = {
            "distance_definition": column,
            "n_sites": len(subset),
            "n_proteins": subset.acc.nunique(),
            "n_positive": int(subset.y.sum()),
        }
        if column == "dist_core_A":
            # This row is the identical primary estimand. Reuse the canonical
            # 200,000-draw interval rather than simulating a sensitivity-sized
            # interval that can disagree through Monte Carlo error.
            row.update(summary["primary_auc"]["protein_cluster_bootstrap"])
        elif len(subset) >= 4 and subset.y.nunique() == 2:
            row.update(
                bootstrap_auc(
                    subset.y,
                    -subset[column],
                    groups=subset.acc,
                    seed=SEED + 40 + index,
                )
            )
        definition_rows.append(row)
    definitions = pd.DataFrame(definition_rows)
    definitions.to_csv(RESULTS / "feature_definition_sensitivity.csv", index=False)
    summary["feature_definition_sensitivity"] = definition_rows

    # Reviewer-driven cohort sensitivities. Exact-overlap exclusion is primary;
    # the 166-site 0 Å arm is the named inclusive sensitivity.
    cohort_masks = {
        "primary_excluding_annotation_coincident": (
            ~inclusive_data.is_itself_annot.astype(bool)
        ),
        "inclusive_exact_overlaps_at_0A": np.ones(len(inclusive_data), dtype=bool),
        "inclusive_exclude_hog1_pby107_position_resolution": (
            ~inclusive_data["Strain ID"].astype(str).eq("PBY107")
        ),
        "legacy_phase0_supp6_selected_excluding_overlaps": (
            inclusive_data.index.isin(legacy_data.index)
        ),
        "primary_serine_threonine_only": (
            ~inclusive_data.is_itself_annot.astype(bool)
            & inclusive_data.pmt_aa_wt.isin(["S", "T"])
        ),
        "primary_tyrosine_only": (
            ~inclusive_data.is_itself_annot.astype(bool)
            & inclusive_data.pmt_aa_wt.eq("Y")
        ),
        "inclusive_exclude_prm15_s158_phosphointermediate": ~(
            (inclusive_data.acc == "Q03262") & (inclusive_data.pos == 158)
        ),
    }
    cohort_rows = []
    for index, (name, mask) in enumerate(cohort_masks.items()):
        subset = inclusive_data.loc[mask].copy()
        row = {
            "cohort": name,
            "n_sites": len(subset),
            "n_proteins": subset.acc.nunique(),
            "n_positive": int(subset.y.sum()),
        }
        if name == "primary_excluding_annotation_coincident":
            row.update(summary["primary_auc"]["protein_cluster_bootstrap"])
        elif name == "inclusive_exact_overlaps_at_0A":
            row.update(summary["inclusive_sensitivity_auc"]["protein_cluster_bootstrap"])
        elif len(subset) >= 4 and subset.y.nunique() == 2:
            row.update(
                bootstrap_auc(
                    subset.y,
                    -subset.dist_core_A,
                    groups=subset.acc,
                    seed=SEED + 50 + index,
                )
            )
        cohort_rows.append(row)
    cohorts = pd.DataFrame(cohort_rows)
    cohorts.to_csv(RESULTS / "cohort_sensitivity.csv", index=False)
    summary["cohort_sensitivity"] = cohort_rows

    residue_rows = []
    for index, residue in enumerate(("S", "T", "Y")):
        subset = d[d.pmt_aa_wt.eq(residue)].copy()
        row = {
            "residue": residue,
            "n_sites": int(len(subset)),
            "n_proteins": int(subset.acc.nunique()),
            "n_positive": int(subset.y.sum()),
        }
        if len(subset) >= 4 and subset.y.nunique() == 2:
            row.update(
                bootstrap_auc(
                    subset.y,
                    -subset.dist_core_A,
                    groups=subset.acc,
                    seed=SEED + 56 + index,
                )
            )
        residue_rows.append(row)
    pd.DataFrame(residue_rows).to_csv(RESULTS / "residue_class_sensitivity.csv", index=False)
    summary["residue_class_sensitivity"] = residue_rows

    # Continuous growth-profile outcomes.
    outcomes = [
        "phenotypes",
        "neglog10_min_raw_q",
        "sscore_rms",
        "sscore_mean_abs",
        "sscore_max_abs",
    ]
    continuous_rows = []
    for index, outcome in enumerate(outcomes):
        subset = d[["acc", "dist_core_A", outcome, "logd", "plddt", "rsa"]].dropna()
        corr = cluster_boot_spearman(
            subset.dist_core_A,
            subset[outcome],
            subset.acc,
            seed=SEED + 60 + index,
        )
        model_data = subset.copy()
        model_data["log_outcome"] = np.log1p(model_data[outcome])
        fit = smf.ols("log_outcome ~ logd + plddt + rsa", data=model_data).fit(
            cov_type="cluster", cov_kwds={"groups": model_data.acc}
        )
        coefficient = fit.params["logd"]
        se = fit.bse["logd"]
        continuous_rows.append(
            {
                "outcome": outcome,
                "n_sites": len(subset),
                "n_proteins": subset.acc.nunique(),
                **corr,
                "adjusted_log_outcome_beta_per_10x_distance_plus_1A": float(coefficient),
                "adjusted_ci_low": float(coefficient - 1.96 * se),
                "adjusted_ci_high": float(coefficient + 1.96 * se),
                "adjusted_cluster_p": float(fit.pvalues["logd"]),
            }
        )
    continuous = pd.DataFrame(continuous_rows)
    # BLAS implementations can differ in the last few machine-precision digits for the
    # clustered OLS sensitivity. Canonicalize the release serialization well below the
    # manuscript's reporting precision so a clean-room wheel environment is byte-stable.
    continuous_numeric = continuous.select_dtypes(include=[np.number]).columns
    continuous[continuous_numeric] = continuous[continuous_numeric].round(12)
    continuous_rows = continuous.to_dict(orient="records")
    continuous.to_csv(RESULTS / "continuous_outcomes.csv", index=False)
    summary["continuous_outcomes"] = continuous_rows

    # Protein-isolated out-of-sample benchmark. Outcome-derived fields are deliberately excluded.
    model_specs = {
        "distance_only": ["logd"],
        "structural": ["logd", "plddt", "rsa", "pae_pair_max", "log_n_annot"],
        "published_annotations": [
            "supp_is_disopred", "age_ordinal", "has_uniprot_domain",
            "sift_ala_score_inv", "PWM_nkinTop01",
        ],
        "combined": [
            "logd", "plddt", "rsa", "pae_pair_max", "log_n_annot",
            "supp_is_disopred", "age_ordinal", "has_uniprot_domain",
            "sift_ala_score_inv", "PWM_nkinTop01",
        ],
    }
    benchmark_rows = []
    repeat_auc_by_model = {}
    # A constant benchmark has AUC 0.5 by construction and does not inherit fold-prevalence artifacts.
    null_predictions = np.full(len(d), d.y.mean(), dtype=float)
    benchmark_rows.append(
        {
            "model": "constant_prevalence",
            "features": "none",
            "estimate": 0.5,
            "split_low": 0.5,
            "split_high": 0.5,
            "pooled_oof_auc": 0.5,
            "brier": float(brier_score_loss(d.y, null_predictions)),
        }
    )
    d["oof_constant_prevalence"] = null_predictions

    for index, (name, features) in enumerate(model_specs.items()):
        cv = repeated_grouped_predictions(d, features)
        repeat_auc_by_model[name] = cv["repeat_auc"]
        predictions = cv["predictions"]
        d[f"oof_{name}"] = predictions
        benchmark_rows.append(
            {
                "model": name,
                "features": ";".join(features),
                "estimate": float(np.mean(cv["repeat_auc"])),
                "split_low": float(np.percentile(cv["repeat_auc"], 2.5)),
                "split_high": float(np.percentile(cv["repeat_auc"], 97.5)),
                "pooled_oof_auc": float(roc_auc_score(d.y, predictions)),
                "brier": float(np.mean(cv["repeat_brier"])),
            }
        )
    benchmark = pd.DataFrame(benchmark_rows)
    benchmark.to_csv(RESULTS / "predictor_benchmark.csv", index=False)
    d.to_csv(RESULTS / "phase0_5_analysis_with_oof_predictions.csv", index=False)
    publication_columns = [
        "Strain ID", "Gene name", "Systematic name", "acc", "pos", "aa", "pmt_aa_wt",
        "has_pheno", "phenotypes", "extremePheno", "neglog10_min_raw_q",
        "source_replicate_strain_count", "raw_source_rows",
        "sscore_rms", "sscore_mean_abs", "sscore_max_abs", "phenotype_group",
        "dist_core_A", "nearest_core_pos", "plddt", "nearest_core_plddt", "rsa",
        "pae_pair_mean", "pae_pair_max", "n_core_residues", "protein_length",
        "dist_act_site_A", "dist_binding_A", "dist_core_plus_site_A",
        "dist_all_with_dna_bind_A", "age_w0_group", "supp_is_disopred",
        "domain_uniprot", "sift_ala_score_inv", "PWM_nkinTop01",
        "wgs_additional_mutation_flag", "scar_control_correlation_flag", "is_itself_annot",
        "cohort_primary_exclude_annotation_coincident", "cohort_inclusive_sensitivity",
        "alphafold_version",
        "oof_distance_only", "oof_structural", "oof_published_annotations", "oof_combined",
    ]
    d[publication_columns].to_csv(RESULTS / "phase0_5_publication_data.csv", index=False)
    summary["predictor_benchmark"] = benchmark_rows
    incremental = repeat_auc_by_model["combined"] - repeat_auc_by_model["published_annotations"]
    summary["incremental_structural_value_over_published_annotations"] = {
        "mean_auc_difference": float(np.mean(incremental)),
        "split_low": float(np.percentile(incremental, 2.5)),
        "split_high": float(np.percentile(incremental, 97.5)),
        "repeat_differences": incremental.tolist(),
    }

    # Small-cluster sensitivity for the adjusted binary model.
    summary["wild_cluster_lpm"] = wild_cluster_lpm(d)

    distance_pae = cluster_boot_spearman(
        d.dist_core_A, d.pae_pair_max, d.acc, seed=SEED + 90
    )
    site_plddt_pae = cluster_boot_spearman(
        d.plddt, d.pae_pair_max, d.acc, seed=SEED + 91
    )
    summary["confidence_correlations"] = {
        "spearman_distance_vs_pair_pae": distance_pae,
        "spearman_site_plddt_vs_pair_pae": site_plddt_pae,
    }

    summary["qc"] = {
        "pae_complete_primary": int(primary_data.pae_pair_max.notna().sum()),
        "pae_complete_inclusive": int(inclusive_data.pae_pair_max.notna().sum()),
        "raw_s_scores_complete_primary": int(primary_data.sscore_rms.notna().sum()),
        "raw_s_scores_complete_inclusive": int(inclusive_data.sscore_rms.notna().sum()),
        "wgs_flags_in_primary": int(primary_data.wgs_additional_mutation_flag.sum()),
        "wgs_flags_in_inclusive": int(inclusive_data.wgs_additional_mutation_flag.sum()),
        "scar_control_correlation_flags_in_primary": int(
            primary_data.scar_control_correlation_flag.sum()
        ),
        "scar_control_correlation_flags_in_inclusive": int(
            inclusive_data.scar_control_correlation_flag.sum()
        ),
        "substitutions_with_replicate_strains_inclusive": int(
            (inclusive_data.source_replicate_strain_count > 1).sum()
        ),
        "exact_annotation_overlaps_primary": int(
            primary_data.is_itself_annot.astype(bool).sum()
        ),
        "exact_annotation_overlaps_inclusive": int(
            inclusive_data.is_itself_annot.astype(bool).sum()
        ),
        "max_core_distance_recompute_delta_A": float(
            inclusive_data.core_distance_recompute_delta_A.abs().max()
        ),
        "alphafold_versions": sorted(
            inclusive_data.alphafold_version.dropna().astype(int).unique().tolist()
        ),
    }
    summary["environment"] = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scipy": scipy.__version__,
        "scikit_learn": sklearn.__version__,
        "statsmodels": statsmodels.__version__,
    }

    with (RESULTS / "phase0_5_statistics.json").open("w") as handle:
        json.dump(summary, handle, indent=2, default=to_builtin)
        handle.write("\n")

    print(
        "primary AUC (protein-cluster bootstrap): "
        f"{summary['primary_auc']['protein_cluster_bootstrap']['estimate']:.3f} "
        f"[{summary['primary_auc']['protein_cluster_bootstrap']['ci_low']:.3f}, "
        f"{summary['primary_auc']['protein_cluster_bootstrap']['ci_high']:.3f}]"
    )
    print(
        "inclusive sensitivity AUC (protein-cluster bootstrap): "
        f"{summary['inclusive_sensitivity_auc']['protein_cluster_bootstrap']['estimate']:.3f} "
        f"[{summary['inclusive_sensitivity_auc']['protein_cluster_bootstrap']['ci_low']:.3f}, "
        f"{summary['inclusive_sensitivity_auc']['protein_cluster_bootstrap']['ci_high']:.3f}]"
    )
    print("\nconfidence strata")
    print(confidence.to_string(index=False))
    print("\ncontinuous outcomes")
    print(continuous.to_string(index=False))
    print("\npredictor benchmark")
    print(benchmark.to_string(index=False))
    print("\nwild cluster LPM")
    print(summary["wild_cluster_lpm"])


if __name__ == "__main__":
    main()
