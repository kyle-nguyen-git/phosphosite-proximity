"""RR-44: direction-specific screen endpoints (growth defect vs growth enhancement).

Every published outcome in this project is direction-agnostic: a substitution is
outcome-positive if its replicate-averaged count of called conditions (qvalue < 0.05)
exceeds zero, regardless of the sign of the S-score. This script builds the two
direction-specific endpoints from the condition-level source table and re-runs the
published discrimination estimator on each.

Frozen-tree rules honoured here:
  * nothing under the project tree is written except this directory;
  * the three frozen hashes are checked before any computation and the run aborts on
    mismatch;
  * AUC and the bootstrap are loaded from robustness/src/02_robustness_analysis.py, not
    reimplemented. That module guards its entry point with
    `if __name__ == "__main__": main()`, and importlib sets __name__ to the spec name,
    so exec_module does not run main(). Verified before use.

Replicate aggregation follows robustness/src/01_build_robustness_dataset.py
aggregate_raw_scores() (lines 133-175): Supplementary Data 3 is inner-joined to
results/analysis_site_members.csv on PBY ID (validate="many_to_one"), the per-strain
count of called conditions is taken, and those per-strain counts are averaged over the
replicate strains of a substitution. That is the same per-strain-then-mean rule the
outcome ledger in src/01_build_sites.py uses to build `phenotypes` and `has_pheno`
(raw_n_q05 aggregated with "mean", label = mean > 0). The direction-specific endpoints
change only the per-strain counting predicate.

Usage:  python3 rr44_direction_specific_endpoint.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE
# phosphosite-proximity/ is the nearest ancestor holding NUMBERS.md, so this script keeps
# working wherever under the tree it is placed.
ROOT = next(p for p in HERE.parents if (p / "NUMBERS.md").exists())

FROZEN = {
    "results/statistics.json":
        "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv":
        "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "robustness/results/robustness_statistics.json":
        "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}

# Declared post hoc sensitivity convention (RR conventions block).
N_BOOT = 20_000


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def verify_frozen() -> dict:
    observed = {}
    for rel, expected in FROZEN.items():
        got = sha256(ROOT / rel)
        observed[rel] = got
        if got != expected:
            sys.exit(f"ABORT: hash mismatch for {rel}\n  expected {expected}\n  observed {got}")
    return observed


def load_frozen_module():
    path = ROOT / "robustness" / "src" / "02_robustness_analysis.py"
    text = path.read_text()
    if 'if __name__ == "__main__"' not in text:
        sys.exit("ABORT: analysis module is not entry-point guarded; refusing to exec it.")
    spec = importlib.util.spec_from_file_location("p05", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.__name__ == "p05"
    return module


def interval_or_point(res: dict, n: int, label: str) -> dict:
    """Apply the 'no interval touching exactly 0 or 1' rule."""
    out = {
        "endpoint": label,
        "n": int(n),
        "auc": float(res["estimate"]),
        "nominal_draws": N_BOOT,
        "retained_draws": int(res["draws"]),
        "ci_low": float(res["ci_low"]),
        "ci_high": float(res["ci_high"]),
        "ci_reportable": True,
        "ci_suppressed_reason": "",
    }
    if res["ci_low"] == 0.0 or res["ci_high"] == 1.0:
        out["ci_reportable"] = False
        out["ci_suppressed_reason"] = (
            "percentile endpoint sits exactly at the AUC boundary; the interval is a "
            "resampling artefact of a degenerate draw, so only the point estimate and n "
            "are reportable"
        )
    return out


def main() -> None:
    warnings.filterwarnings("ignore", message="Unknown extension is not supported")

    observed_hashes = verify_frozen()
    p05 = load_frozen_module()
    seed = p05.SEED
    print(f"frozen hashes verified; module SEED = {seed}; nominal draws = {N_BOOT}")

    # ---- source tables -------------------------------------------------------
    scores = pd.read_excel(
        ROOT / "data" / "EMS132528-supplement-Supplementary_Data_3.xlsx",
        sheet_name="Table S3 – S_Scores of chemical",
    )
    scores["PBY ID"] = scores["PBY ID"].astype(str)

    enriched = pd.read_csv(ROOT / "robustness" / "results" / "robustness_analysis.csv")
    base = pd.read_csv(ROOT / "results" / "analysis_inclusive_sensitivity.csv")
    base["Strain ID"] = base["Strain ID"].astype(str)

    # Member-strain table, restricted exactly as the phase 0.5 build script does.
    members = pd.read_csv(ROOT / "results" / "analysis_site_members.csv")
    members["Strain ID"] = members["Strain ID"].astype(str)
    members = members.merge(
        base[["acc", "pos"]], on=["acc", "pos"], how="inner", validate="many_to_one"
    )[["acc", "pos", "Strain ID"]].drop_duplicates()
    members = members.rename(columns={"Strain ID": "PBY ID"})
    members["PBY ID"] = members["PBY ID"].astype(str)

    joined = scores.merge(members, on="PBY ID", how="inner", validate="many_to_one")
    print(
        f"join: {len(joined)} strain-condition rows / {joined['PBY ID'].nunique()} strains "
        f"/ {joined.groupby(['acc','pos']).ngroups} substitutions"
    )

    called = joined["qvalue"] < 0.05
    joined["called_any"] = called.astype(int)
    joined["called_defect"] = (called & (joined["Score"] < 0)).astype(int)
    joined["called_enhance"] = (called & (joined["Score"] > 0)).astype(int)
    n_called_zero_score = int((called & (joined["Score"] == 0)).sum())

    # Per strain: count conditions. Then average over replicate strains of the
    # substitution (the published rule).
    per_strain = joined.groupby(["acc", "pos", "PBY ID"], sort=False, as_index=False).agg(
        n_called_any=("called_any", "sum"),
        n_called_defect=("called_defect", "sum"),
        n_called_enhance=("called_enhance", "sum"),
    )
    per_site = per_strain.groupby(["acc", "pos"], sort=False, as_index=False).agg(
        replicate_strains=("PBY ID", "nunique"),
        mean_called_any=("n_called_any", "mean"),
        mean_called_defect=("n_called_defect", "mean"),
        mean_called_enhance=("n_called_enhance", "mean"),
    )
    per_site["y_any_recon"] = (per_site["mean_called_any"] > 0).astype(int)
    per_site["y_defect"] = (per_site["mean_called_defect"] > 0).astype(int)
    per_site["y_enhance"] = (per_site["mean_called_enhance"] > 0).astype(int)

    data = enriched.merge(per_site, on=["acc", "pos"], how="left", validate="one_to_one")
    if data[["mean_called_any", "dist_core_A"]].isna().any().any():
        sys.exit("ABORT: missing raw profile or distance after join.")

    data["y_published"] = data["has_pheno"].astype(int)
    data["cohort_primary"] = ~data["is_itself_annot"].astype(bool)

    # Reconstruction check against the published direction-agnostic label.
    mismatch = int((data["y_any_recon"] != data["y_published"]).sum())
    corr_check = float(
        np.max(np.abs(data["mean_called_any"] - data["raw_q05_mean_per_strain"]))
    )
    print(f"direction-agnostic label reconstruction mismatches: {mismatch}")
    print(f"max |reconstructed mean count - published raw_q05_mean_per_strain| = {corr_check:.3g}")
    if mismatch != 0 or corr_check > 1e-9:
        sys.exit("ABORT: replicate aggregation does not reproduce the published ledger.")

    # ---- endpoints -----------------------------------------------------------
    arms = {
        "primary_exclude_annotation_coincident": data.loc[data["cohort_primary"]].copy(),
        "inclusive_sensitivity": data.copy(),
    }
    endpoints = {
        "direction_agnostic_published": "y_published",
        "defect_specific": "y_defect",
        "enhancement_specific": "y_enhance",
    }

    rows = []
    for arm_name, frame in arms.items():
        score = -frame["dist_core_A"].to_numpy(float)   # shorter distance -> positive
        groups = frame["acc"].to_numpy()
        for ep_name, column in endpoints.items():
            y = frame[column].to_numpy(int)
            res = p05.bootstrap_auc(y, score, groups=groups, n=N_BOOT, seed=seed)
            point_only = p05.auc_from_ranks(y, score)
            assert abs(point_only - res["estimate"]) < 1e-12
            record = interval_or_point(res, len(frame), ep_name)
            record.update(
                {
                    "arm": arm_name,
                    "proteins": int(frame["acc"].nunique()),
                    "positives": int(y.sum()),
                    "negatives": int(len(y) - y.sum()),
                    "positive_rate": float(y.mean()),
                    "bootstrap_seed": seed,
                    "resampling_unit": "UniProt accession",
                }
            )
            rows.append(record)
            print(
                f"{arm_name:42s} {ep_name:28s} n={record['n']:3d} pos={record['positives']:3d} "
                f"AUC={record['auc']:.7f} CI=[{record['ci_low']:.6f}, {record['ci_high']:.6f}] "
                f"retained={record['retained_draws']}/{N_BOOT}"
            )

    results = pd.DataFrame(rows)[
        [
            "arm", "endpoint", "n", "proteins", "positives", "negatives", "positive_rate",
            "auc", "ci_low", "ci_high", "ci_reportable", "ci_suppressed_reason",
            "nominal_draws", "retained_draws", "bootstrap_seed", "resampling_unit",
        ]
    ]
    results.to_csv(OUT / "rr44_direction_specific_results.csv", index=False)

    # ---- dominance among primary-cohort direction-agnostic positives ---------
    primary = arms["primary_exclude_annotation_coincident"]
    pos = primary.loc[primary["y_published"] == 1].copy()
    pos["dominance"] = np.select(
        [
            pos["mean_called_defect"] > pos["mean_called_enhance"],
            pos["mean_called_enhance"] > pos["mean_called_defect"],
        ],
        ["defect_dominant", "enhancement_dominant"],
        default="tied",
    )
    dominance = pos["dominance"].value_counts().to_dict()
    pure = {
        "defect_only": int(((pos["mean_called_defect"] > 0) & (pos["mean_called_enhance"] == 0)).sum()),
        "enhancement_only": int(((pos["mean_called_enhance"] > 0) & (pos["mean_called_defect"] == 0)).sum()),
        "mixed_both_directions": int(((pos["mean_called_defect"] > 0) & (pos["mean_called_enhance"] > 0)).sum()),
    }
    print("\nprimary-cohort positives, dominance under called conditions only:")
    print(f"  {dominance}")
    print(f"  {pure}")

    # R3 reported "18 of 79 enhancement-dominant" from profile extremes. Reproduce that
    # rule explicitly (largest |S-score| over the 102-condition profile falls on the
    # positive side, ignoring whether the condition was called) and cross-tabulate it
    # against the proper called-condition computation.
    pos["r3_profile_extreme"] = np.where(
        pos["sscore_max"] > -pos["sscore_min"], "enhancement", "defect"
    )
    r3_counts = pos["r3_profile_extreme"].value_counts().to_dict()
    r3_cross = (
        pd.crosstab(pos["r3_profile_extreme"], pos["dominance"])
        .astype(int).to_dict(orient="index")
    )
    print("\nR3 profile-extreme rule reproduced:", r3_counts)
    print("cross-tabulation vs called-condition dominance:", r3_cross)

    pos_out = pos[
        [
            "acc", "pos", "Gene name", "dist_core_A", "replicate_strains",
            "mean_called_any", "mean_called_defect", "mean_called_enhance", "dominance",
            "sscore_min", "sscore_max", "r3_profile_extreme",
        ]
    ].sort_values(["dominance", "acc", "pos"])
    pos_out.to_csv(OUT / "rr44_primary_positive_dominance.csv", index=False)

    # ---- cross-tabulation of the two direction-specific labels ---------------
    cross = {}
    for arm_name, frame in arms.items():
        cross[arm_name] = {
            "defect_pos_enhance_pos": int(((frame.y_defect == 1) & (frame.y_enhance == 1)).sum()),
            "defect_pos_enhance_neg": int(((frame.y_defect == 1) & (frame.y_enhance == 0)).sum()),
            "defect_neg_enhance_pos": int(((frame.y_defect == 0) & (frame.y_enhance == 1)).sum()),
            "defect_neg_enhance_neg": int(((frame.y_defect == 0) & (frame.y_enhance == 0)).sum()),
        }

    summary = {
        "roadmap_item": "RR-44",
        "frozen_hashes_verified": observed_hashes,
        "conventions": {
            "nominal_protein_cluster_draws": N_BOOT,
            "base_seed": seed,
            "resampling_unit": "UniProt accession; every substitution of a sampled protein retained",
            "discarded_draws_rule": "bootstrap_auc discards resamples drawing a single outcome class",
            "scoring_orientation": "score = -dist_core_A; shorter distance scored toward screen-positive",
            "called_condition": "qvalue < 0.05",
            "replicate_aggregation": (
                "per-strain count of called conditions, then arithmetic mean over the "
                "replicate strains of a substitution; label = mean > 0 "
                "(robustness/src/01_build_robustness_dataset.py aggregate_raw_scores; "
                "src/01_build_sites.py phenotypes/has_pheno)"
            ),
        },
        "source_join": {
            "strain_condition_rows": int(len(joined)),
            "strains": int(joined["PBY ID"].nunique()),
            "substitutions": int(joined.groupby(["acc", "pos"]).ngroups),
            "conditions": int(joined["Condition"].nunique()),
            "called_rows_total": int(joined["called_any"].sum()),
            "called_rows_defect": int(joined["called_defect"].sum()),
            "called_rows_enhance": int(joined["called_enhance"].sum()),
            "called_rows_score_exactly_zero": n_called_zero_score,
        },
        "reconstruction_check": {
            "direction_agnostic_label_mismatches": mismatch,
            "max_abs_delta_vs_raw_q05_mean_per_strain": corr_check,
        },
        "estimates": rows,
        "primary_positive_dominance": {
            "n_positives": int(len(pos)),
            "counts": dominance,
            "pure_and_mixed": pure,
            "r3_profile_extreme_rule": {
                "definition": "sscore_max > -sscore_min over all 102 conditions, called or not",
                "counts": r3_counts,
                "cross_tabulation_vs_called_condition_dominance": r3_cross,
            },
        },
        "label_cross_tabulation": cross,
    }
    (OUT / "rr44_direction_specific_results.json").write_text(
        json.dumps(summary, indent=2, default=p05.to_builtin) + "\n"
    )
    print(f"\nwrote {OUT/'rr44_direction_specific_results.csv'}")
    print(f"wrote {OUT/'rr44_direction_specific_results.json'}")
    print(f"wrote {OUT/'rr44_primary_positive_dominance.csv'}")


if __name__ == "__main__":
    main()
