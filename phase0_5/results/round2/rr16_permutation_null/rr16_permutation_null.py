"""RR-16: permutation null for the primary estimand (AUC of -min_dist_A for the
screen-positive label), primary cohort, n=163 substitutions, 48 proteins.

Estimators are loaded from the frozen phase 0.5 analysis module; nothing here
reimplements AUC or the bootstrap. Reads only; writes only into this directory.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

FROZEN = {
    "results/statistics.json": "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv": "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "phase0_5/results/phase0_5_statistics.json": "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}
for rel, want in FROZEN.items():
    got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if got != want:
        raise SystemExit(f"ABORT: hash mismatch for {rel}\n  expected {want}\n  got      {got}")
print("frozen hashes verified")

spec = importlib.util.spec_from_file_location(
    "p05", str(ROOT / "phase0_5" / "src" / "02_phase0_5_analysis.py")
)
p05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p05)  # module is __main__-guarded; import runs defs/constants only

SEED = p05.SEED  # 20260728
N_PERM = 20_000
N_BOOT = p05.N_SENSITIVITY_BOOT  # 20000

d = pd.read_csv(ROOT / "results" / "analysis_final.csv")
assert len(d) == 163, len(d)
y = d.y.to_numpy(int)
score = -d.min_dist_A.to_numpy(float)  # shorter distance scored toward screen-positive
acc = d.acc.to_numpy()

observed = p05.auc_from_ranks(y, score)
OBS_REF = 0.5268234

boot = p05.bootstrap_auc(y, score, groups=acc, n=N_BOOT, seed=SEED)


def perm_stats(draws, observed, label):
    draws = np.asarray(draws, dtype=float)
    mean = float(draws.mean())
    sd = float(draws.std(ddof=1))
    lo, hi = (float(v) for v in np.percentile(draws, [2.5, 97.5]))
    dev_obs_half = abs(observed - 0.5)
    dev_obs_mean = abs(observed - mean)
    n = draws.size
    ge_half = int((np.abs(draws - 0.5) >= dev_obs_half - 1e-12).sum())
    ge_mean = int((np.abs(draws - mean) >= dev_obs_mean - 1e-12).sum())
    return {
        "scheme": label,
        "n_permutations": n,
        "null_mean": mean,
        "null_sd": sd,
        "null_p2_5": lo,
        "null_p97_5": hi,
        "null_min": float(draws.min()),
        "null_max": float(draws.max()),
        "observed_auc": float(observed),
        "p_two_sided_about_0.5_addone": (ge_half + 1) / (n + 1),
        "p_two_sided_about_0.5_raw": ge_half / n,
        "n_ge_about_0.5": ge_half,
        "p_two_sided_about_null_mean_addone": (ge_mean + 1) / (n + 1),
        "p_two_sided_about_null_mean_raw": ge_mean / n,
        "n_ge_about_null_mean": ge_mean,
        "z_about_null_mean": float((observed - mean) / sd),
    }


# (a) unrestricted permutation of the 163 labels
rng = np.random.default_rng(SEED)
yy = y.copy()
draws_a = np.empty(N_PERM)
for i in range(N_PERM):
    rng.shuffle(yy)
    draws_a[i] = p05.auc_from_ranks(yy, score)

# (b) permutation within protein (protein-level outcome structure preserved)
rng_b = np.random.default_rng(SEED)
blocks = [np.flatnonzero(acc == a) for a in np.unique(acc)]
var_blocks = [b for b in blocks if len(np.unique(y[b])) == 2]
const_blocks = len(blocks) - len(var_blocks)
yb = y.copy()
draws_b = np.empty(N_PERM)
for i in range(N_PERM):
    for b in var_blocks:
        yb[b] = rng_b.permutation(y[b])
    draws_b[i] = p05.auc_from_ranks(yb, score)

res_a = perm_stats(draws_a, observed, "unrestricted_across_163_substitutions")
res_b = perm_stats(draws_b, observed, "within_protein_48_clusters")
res_b["n_protein_clusters"] = len(blocks)
res_b["n_clusters_with_both_labels"] = len(var_blocks)
res_b["n_clusters_single_label_fixed"] = const_blocks
res_b["n_sites_in_variable_clusters"] = int(sum(len(b) for b in var_blocks))

# declared post hoc families
families = [
    ("confidence strata x cohorts", 11 * 2),
    ("PAE grids x cohorts", 72 * 3),
    ("feature definitions", 5),
    ("cohort/residue sensitivities", 7),
    ("continuous outcomes", 5),
]
total_estimates = sum(v for _, v in families)

fam = {}
for res, key in ((res_a, "unrestricted"), (res_b, "within_protein")):
    draws = draws_a if key == "unrestricted" else draws_b
    mean = res["null_mean"]
    dev = np.abs(draws - mean)
    # expected max |AUC - null mean| over k independent null estimates
    k = total_estimates
    q = float(np.quantile(dev, (0.5) ** (1.0 / k)))  # median of the max of k draws
    q95 = float(np.quantile(dev, (0.95) ** (1.0 / k)))
    fam[key] = {
        "expected_false_positives_at_p_lt_0.05": 0.05 * k,
        "expected_count_as_extreme_as_observed": res["p_two_sided_about_null_mean_raw"] * k,
        "median_max_abs_deviation_over_k_independent_nulls": q,
        "p95_max_abs_deviation_over_k_independent_nulls": q95,
        "implied_max_auc_median": mean + q,
        "implied_max_auc_p95": mean + q95,
    }

out = {
    "roadmap_item": "RR-16",
    "estimand": "AUC(-min_dist_A -> screen-positive label), primary cohort exclude_annotation_coincident",
    "n_sites": int(len(d)),
    "n_proteins": int(d.acc.nunique()),
    "n_positive": int(y.sum()),
    "n_negative": int(len(y) - y.sum()),
    "seed": SEED,
    "n_permutations": N_PERM,
    "observed_auc_recomputed": float(observed),
    "observed_auc_frozen_statistics_json": 0.5268233875828813,
    "observed_auc_as_quoted_in_task": OBS_REF,
    "observed_auc_protein_cluster_ci": {
        "estimate": boot["estimate"],
        "ci_low": boot["ci_low"],
        "ci_high": boot["ci_high"],
        "retained_draws": boot["draws"],
        "nominal_draws": N_BOOT,
        "seed": SEED,
        "unit": "UniProt accession",
    },
    "permutation_a_unrestricted": res_a,
    "permutation_b_within_protein": res_b,
    "declared_post_hoc_families": {
        "components": {name: count for name, count in families},
        "total_estimates": total_estimates,
    },
    "family_scale_vs_null": fam,
    "r1_reported_unverified": {"sd": 0.045, "range": [0.410, 0.588], "p": 0.55},
}

(OUT / "rr16_permutation_null.json").write_text(json.dumps(out, indent=2))

rows = []
for res in (res_a, res_b):
    rows.append({k: res.get(k) for k in [
        "scheme", "n_permutations", "observed_auc", "null_mean", "null_sd",
        "null_p2_5", "null_p97_5", "null_min", "null_max",
        "p_two_sided_about_0.5_addone", "p_two_sided_about_0.5_raw",
        "p_two_sided_about_null_mean_addone", "p_two_sided_about_null_mean_raw",
        "z_about_null_mean",
    ]})
pd.DataFrame(rows).to_csv(OUT / "rr16_permutation_null.csv", index=False)
np.save(OUT / "rr16_null_draws_unrestricted.npy", draws_a)
np.save(OUT / "rr16_null_draws_within_protein.npy", draws_b)
print(json.dumps(out, indent=2))
