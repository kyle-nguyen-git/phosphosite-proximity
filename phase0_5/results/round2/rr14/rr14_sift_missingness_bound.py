"""RR-14: SIFT missingness disclosure and worst/best-case bound on the paired
SIFT-minus-distance AUC difference.

Read-only with respect to the frozen tree. Everything is written under rr14/.

Estimators are loaded from the frozen module phase0_5/src/02_phase0_5_analysis.py
(guarded by `if __name__ == "__main__"`, so importing it does not run main()).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "rr14"

FROZEN = {
    "results/statistics.json":
        "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv":
        "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "phase0_5/results/phase0_5_statistics.json":
        "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}

for rel, expected in FROZEN.items():
    got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if got != expected:
        raise SystemExit(f"ABORT: hash mismatch for {rel}\n  expected {expected}\n  got      {got}")
print("frozen hashes verified")

spec = importlib.util.spec_from_file_location(
    "p05", ROOT / "phase0_5" / "src" / "02_phase0_5_analysis.py"
)
p05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p05)

SEED = p05.SEED            # 20260728
N_BOOT = 20000             # declared post hoc sensitivity draw count

# --- cohort construction, identical to main() -------------------------------
all_data = pd.read_csv(ROOT / "phase0_5" / "results" / "phase0_5_analysis.csv")
all_data["y"] = all_data["has_pheno"].astype(int)
all_data["logd"] = np.log10(all_data["dist_core_A"] + 1.0)
d = all_data.loc[~all_data.is_itself_annot.astype(bool)].copy()
assert len(d) == 163, len(d)
assert d.dist_core_A.notna().all()

observed = d.sift_ala_score_inv.notna()
n_missing = int((~observed).sum())
assert n_missing == 11, n_missing

results = {
    "item": "RR-14",
    "seed_base": SEED,
    "n_bootstrap_nominal": N_BOOT,
    "resampling_unit": "UniProt accession (acc); all substitutions of a sampled protein retained",
    "scoring_orientation": "shorter distance scored toward screen-positive (score = -dist_core_A); "
                           "sift_ala_score_inv already oriented so higher = more screen-positive",
}

# --- 1. missingness comparison ---------------------------------------------
def describe(frame, label):
    q1, med, q3 = np.percentile(frame.dist_core_A, [25, 50, 75])
    return {
        "group": label,
        "n": int(len(frame)),
        "n_proteins": int(frame.acc.nunique()),
        "n_positive": int(frame.y.sum()),
        "outcome_rate": float(frame.y.mean()),
        "dist_median_A": float(med),
        "dist_q1_A": float(q1),
        "dist_q3_A": float(q3),
        "dist_iqr_A": float(q3 - q1),
        "dist_min_A": float(frame.dist_core_A.min()),
        "dist_max_A": float(frame.dist_core_A.max()),
    }

miss_rows = [
    describe(d.loc[observed], "sift_observed"),
    describe(d.loc[~observed], "sift_missing"),
    describe(d, "all_primary"),
]
results["missingness"] = miss_rows
results["missing_records"] = d.loc[~observed, [
    "acc", "pmt_aa_wt", "pos", "dist_core_A", "y", "position_resolution"
]].to_dict(orient="records")

# Mann-Whitney style rank comparison of distance between the two groups,
# expressed as the project's own rank AUC (no new estimator introduced):
# P(missing site is farther than observed site), ties at 0.5.
results["distance_rank_auc_missing_vs_observed"] = float(
    p05.auc_from_ranks((~observed).astype(int).values, d.dist_core_A.values)
)

# --- 2. bound on the paired SIFT-minus-distance difference ------------------
lo = float(d.sift_ala_score_inv.min(skipna=True))
hi = float(d.sift_ala_score_inv.max(skipna=True))
span = hi - lo if hi > lo else 1.0
BELOW = lo - span          # strictly below every observed value
ABOVE = hi + span          # strictly above every observed value

def imputed(direction):
    """direction 'least': missing positives ranked lowest, missing negatives highest
       (minimises SIFT AUC). 'most': the reverse (maximises SIFT AUC)."""
    s = d.sift_ala_score_inv.to_numpy(dtype=float).copy()
    y = d.y.to_numpy(dtype=int)
    miss = ~observed.to_numpy()
    if direction == "least":
        s[miss & (y == 1)] = BELOW
        s[miss & (y == 0)] = ABOVE
    else:
        s[miss & (y == 1)] = ABOVE
        s[miss & (y == 0)] = BELOW
    return s

dist_score = -d.dist_core_A.to_numpy(dtype=float)
y = d.y.to_numpy(dtype=int)
groups = d.acc.to_numpy()

bounds = {}
for direction in ("least", "most"):
    s = imputed(direction)
    sift_auc = p05.bootstrap_auc(y, s, groups=groups, n=N_BOOT, seed=SEED)
    diff = p05.paired_auc_difference(y, s, dist_score, groups, n=N_BOOT, seed=SEED)
    bounds[direction] = {
        "imputation": ("missing positives at the lowest rank, missing negatives at the highest"
                       if direction == "least" else
                       "missing positives at the highest rank, missing negatives at the lowest"),
        "n_sites": int(len(d)),
        "n_proteins": int(d.acc.nunique()),
        "n_positive": int(y.sum()),
        "sift_auc": sift_auc,
        "sift_minus_distance_auc": diff,
        "seed": SEED,
        "draws_nominal": N_BOOT,
        "draws_retained_sift_auc": sift_auc["draws"],
        "draws_retained_difference": diff["draws"],
    }
results["bounds"] = bounds

# distance-only AUC on the full 163 (the comparator arm of the paired difference)
dist_auc_163 = p05.bootstrap_auc(y, dist_score, groups=groups, n=N_BOOT, seed=SEED)
results["distance_auc_full_163"] = dist_auc_163 | {"draws_nominal": N_BOOT, "seed": SEED}

# published common-support values, read from the frozen file (not retyped)
frozen = json.loads((ROOT / "phase0_5" / "results" / "phase0_5_statistics.json").read_text())
pub = frozen["sift_sequence_constraint_diagnostic"]["cohorts"]["exclude_annotation_coincident"]
results["published_common_support"] = {
    "n_sites": pub["n_sites"], "n_proteins": pub["n_proteins"], "n_positive": pub["n_positive"],
    "sift_auc": pub["sift_auc"], "distance_auc": pub["distance_auc"],
    "sift_minus_distance_auc": pub["sift_minus_distance_auc"],
}

OUT.mkdir(exist_ok=True)
(OUT / "rr14_results.json").write_text(json.dumps(results, indent=2) + "\n")

rows = []
for r in miss_rows:
    rows.append({"block": "missingness", **r})
tab = pd.DataFrame(rows)
tab.to_csv(OUT / "rr14_missingness.csv", index=False)

brows = []
p = results["published_common_support"]
brows.append({
    "arm": "published_common_support", "n_sites": p["n_sites"], "n_positive": p["n_positive"],
    "sift_auc": p["sift_auc"]["estimate"],
    "diff_estimate": p["sift_minus_distance_auc"]["estimate"],
    "diff_ci_low": p["sift_minus_distance_auc"]["ci_low"],
    "diff_ci_high": p["sift_minus_distance_auc"]["ci_high"],
    "draws_nominal": 20000, "draws_retained": p["sift_minus_distance_auc"]["draws"],
})
for k, b in bounds.items():
    brows.append({
        "arm": f"imputed_{k}_favourable_for_sift", "n_sites": b["n_sites"],
        "n_positive": b["n_positive"], "sift_auc": b["sift_auc"]["estimate"],
        "diff_estimate": b["sift_minus_distance_auc"]["estimate"],
        "diff_ci_low": b["sift_minus_distance_auc"]["ci_low"],
        "diff_ci_high": b["sift_minus_distance_auc"]["ci_high"],
        "draws_nominal": N_BOOT, "draws_retained": b["sift_minus_distance_auc"]["draws"],
    })
pd.DataFrame(brows).to_csv(OUT / "rr14_bounds.csv", index=False)

print(json.dumps(results["missingness"], indent=2))
print("distance rank AUC (missing vs observed):",
      results["distance_rank_auc_missing_vs_observed"])
print(json.dumps({k: {"sift_auc": v["sift_auc"],
                      "diff": v["sift_minus_distance_auc"]} for k, v in bounds.items()}, indent=2))
print("distance AUC full 163:", dist_auc_163)
