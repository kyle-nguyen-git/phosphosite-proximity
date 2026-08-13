"""RR-29: sequence-adjacency sensitivity and short-range composition.

Reads the frozen phase 0.5 analysis table, tabulates every substitution within 15 A
of its nearest target, and recomputes the primary/inclusive AUCs and the descriptive
cutoff table with sequence-adjacent (|pos - nearest_feat_pos| <= 2) substitutions removed.

Estimators are loaded from the frozen module phase0_5/src/02_phase0_5_analysis.py
(guarded by `if __name__ == "__main__"`, so importing does not run main()).

Writes only into rr29_sequence_adjacency/.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE

FROZEN = {
    "results/statistics.json":
        "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv":
        "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "phase0_5/results/phase0_5_statistics.json":
        "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}

for rel, expected in FROZEN.items():
    digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if digest != expected:
        raise SystemExit(f"ABORT: hash mismatch for {rel}: {digest} != {expected}")
print("frozen hashes verified")

spec = importlib.util.spec_from_file_location(
    "p05", ROOT / "phase0_5" / "src" / "02_phase0_5_analysis.py"
)
p05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p05)

SEED = p05.SEED            # 20260728
N_BOOT = 20000             # declared post hoc sensitivity draw count
assert SEED == 20260728

# ---------------------------------------------------------------- load cohort
d = pd.read_csv(ROOT / "phase0_5" / "results" / "phase0_5_analysis.csv")
d["y"] = d["has_pheno"].astype(int)
d["cohort_primary_exclude_annotation_coincident"] = ~d.is_itself_annot.astype(bool)
d["cohort_inclusive_sensitivity"] = True

# min_dist_A and dist_core_A are identical on all 166 rows, as are
# nearest_feat_pos and nearest_core_pos; the published score is -dist_core_A.
assert np.allclose(d.min_dist_A, d.dist_core_A)
assert (d.nearest_feat_pos == d.nearest_core_pos).all()

d["dpos"] = (d["pos"] - d["nearest_feat_pos"]).abs()
d["seq_adjacent"] = d["dpos"] <= 2

primary = d.loc[d.cohort_primary_exclude_annotation_coincident].copy()
inclusive = d.copy()

# ------------------------------------------- Part 1: within-15 A tabulation
within15 = primary.loc[primary.dist_core_A <= 15].copy()
within15 = within15.sort_values("dist_core_A")
tab = within15[[
    "acc", "Gene name", "pos", "pmt_aa_wt", "pmt_aa_mutant",
    "dist_core_A", "nearest_feat_pos", "dpos", "seq_adjacent", "y",
]].rename(columns={"dist_core_A": "distance_A", "y": "outcome_has_pheno"})
tab.to_csv(OUT / "rr29_within15A_primary.csv", index=False)

sub5 = tab.loc[tab.distance_A < 5]

# ------------------------------------------------------ Part 2: AUC sensitivity
def arm(frame, label):
    keep = frame.loc[~frame.seq_adjacent]
    res_full = p05.bootstrap_auc(
        frame.y, -frame.dist_core_A, groups=frame.acc, n=N_BOOT, seed=SEED
    )
    res_keep = p05.bootstrap_auc(
        keep.y, -keep.dist_core_A, groups=keep.acc, n=N_BOOT, seed=SEED
    )
    return [
        {
            "arm": label, "filter": "all substitutions",
            "n_sites": int(len(frame)), "n_proteins": int(frame.acc.nunique()),
            "n_positive": int(frame.y.sum()), "n_negative": int((frame.y == 0).sum()),
            "auc": res_full["estimate"], "ci_low": res_full["ci_low"],
            "ci_high": res_full["ci_high"],
            "nominal_draws": N_BOOT, "retained_draws": res_full["draws"],
            "seed": SEED,
        },
        {
            "arm": label, "filter": "|dpos| <= 2 excluded",
            "n_sites": int(len(keep)), "n_proteins": int(keep.acc.nunique()),
            "n_positive": int(keep.y.sum()), "n_negative": int((keep.y == 0).sum()),
            "auc": res_keep["estimate"], "ci_low": res_keep["ci_low"],
            "ci_high": res_keep["ci_high"],
            "nominal_draws": N_BOOT, "retained_draws": res_keep["draws"],
            "seed": SEED,
        },
    ]


auc_rows = arm(primary, "primary_exclude_annotation_coincident")
auc_rows += arm(inclusive, "inclusive_sensitivity")
auc_table = pd.DataFrame(auc_rows)
auc_table.to_csv(OUT / "rr29_auc_sensitivity.csv", index=False)

# ------------------------------------------- Part 3: descriptive cutoff table
cut_rows = []
for cohort_name, frame in (
    ("primary_exclude_annotation_coincident", primary),
    ("inclusive_sensitivity", inclusive),
):
    for filt, sub in (
        ("all substitutions", frame),
        ("|dpos| <= 2 excluded", frame.loc[~frame.seq_adjacent]),
    ):
        for cutoff in (5, 8, 10, 15):
            near = sub.dist_core_A <= cutoff
            np_ = int(sub.loc[near, "y"].sum())
            nn = int(near.sum() - np_)
            fp = int(sub.loc[~near, "y"].sum())
            fn = int((~near).sum() - fp)
            odds = (np_ * fn) / (nn * fp) if nn and fp else np.nan
            cut_rows.append({
                "cohort": cohort_name, "filter": filt, "cutoff_A": cutoff,
                "n_within": int(near.sum()), "n_positive_within": np_,
                "rate_within": float(sub.loc[near, "y"].mean()) if near.sum() else np.nan,
                "n_beyond": int((~near).sum()), "n_positive_beyond": fp,
                "rate_beyond": float(sub.loc[~near, "y"].mean()),
                "odds_ratio_descriptive": float(odds),
            })
cut_table = pd.DataFrame(cut_rows)
cut_table.to_csv(OUT / "rr29_cutoffs.csv", index=False)

# ------------------------------------------------------------------- JSON dump
summary = {
    "roadmap_item": "RR-29",
    "seed": SEED,
    "nominal_draws": N_BOOT,
    "resampling_unit": "UniProt accession (acc)",
    "score": "-dist_core_A (shorter distance scored toward screen-positive)",
    "distance_column_note": (
        "min_dist_A == dist_core_A on all 166 rows; "
        "nearest_feat_pos == nearest_core_pos on all 166 rows"
    ),
    "sub5A_primary": {
        "n": int(len(sub5)),
        "n_seq_adjacent_dpos_le_2": int(sub5.seq_adjacent.sum()),
        "n_dpos_eq_1": int((sub5.dpos == 1).sum()),
        "distance_range_dpos_eq_1": [
            float(sub5.loc[sub5.dpos == 1, "distance_A"].min()),
            float(sub5.loc[sub5.dpos == 1, "distance_A"].max()),
        ] if (sub5.dpos == 1).any() else None,
        "rows": sub5.to_dict(orient="records"),
    },
    "within15A_primary_n": int(len(tab)),
    "auc_sensitivity": auc_rows,
    "cutoffs": cut_rows,
    "dpos_distribution_primary": {
        str(k): int(v) for k, v in primary.dpos.value_counts().sort_index().items()
    },
}
with (OUT / "rr29_results.json").open("w") as fh:
    json.dump(summary, fh, indent=2, default=p05.to_builtin)
    fh.write("\n")

pd.set_option("display.width", 200)
print("\n--- sub-5 A bin, primary ---")
print(sub5.to_string(index=False))
print("\n--- AUC sensitivity ---")
print(auc_table.to_string(index=False))
print("\n--- cutoffs ---")
print(cut_table.to_string(index=False))
print("\n--- dpos distribution (primary) ---")
print(primary.dpos.value_counts().sort_index().to_string())
print("\nwithin 15 A (primary): n =", len(tab),
      "| seq-adjacent within 15 A:", int(tab.seq_adjacent.sum()))
