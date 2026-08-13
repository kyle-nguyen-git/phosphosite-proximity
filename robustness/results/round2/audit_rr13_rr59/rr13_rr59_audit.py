"""RR-13 (bootstrap draw-retention audit) and RR-59 (predictor benchmark dual summary).

Read-only with respect to the frozen tree. Writes only into audit_rr13_rr59/.

RR-13 walks every stored interval in results/ and robustness/results/ (JSON + CSV) and records
nominal draws, retained draws, shortfall, and whether either endpoint touches exactly 0 or 1.
RR-59 reads robustness/results/predictor_benchmark.csv verbatim and re-derives the pooled
out-of-fold AUC from the stored out-of-fold predictions using the frozen module's own
auc_from_ranks, as a check on the stored pooled column.

The frozen module robustness/src/02_robustness_analysis.py guards main() behind
`if __name__ == "__main__":`, so importing it by spec executes definitions only. Verified
before running; functions are loaded from it, not reimplemented.
"""

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

FROZEN_HASHES = {
    "results/statistics.json":
        "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv":
        "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "robustness/results/robustness_statistics.json":
        "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}


def verify_frozen():
    for rel, expected in FROZEN_HASHES.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if got != expected:
            sys.exit(f"ABORT: hash mismatch for {rel}\n  expected {expected}\n  got      {got}")
    print("frozen hashes verified: 3/3")


def load_module():
    path = ROOT / "robustness/src/02_robustness_analysis.py"
    text = path.read_text()
    if '__name__ == "__main__"' not in text:
        sys.exit("ABORT: module is not main-guarded; do not import it")
    spec = importlib.util.spec_from_file_location("p05", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- RR-13

# Nominal draw counts as declared in the frozen module.
N_PRIMARY = 200000
N_SENS = 20000
N_CORR = 4000
N_WILD = 9999


def touches_bound(lo, hi):
    flags = []
    for name, v in (("low", lo), ("high", hi)):
        if v is None:
            continue
        if v == 0.0:
            flags.append(f"{name}=0")
        elif v == 1.0:
            flags.append(f"{name}=1")
    return ";".join(flags)


def classify(path, keys):
    """Return (method, nominal) for an interval record."""
    p = path.lower()
    if "logistic" in p or "regression_models" in p:
        return "logistic Wald / cluster-robust (analytic, no resampling)", None
    if "spearman" in p or "correlation" in p or "continuous_outcomes" in p:
        return "cluster_boot_spearman (retained count not stored)", N_CORR
    if "wild" in p:
        return "wild_cluster_lpm", N_WILD
    if "difference" in p or "minus" in p:
        return "paired_auc_difference (protein cluster)", None
    return "bootstrap_auc (protein cluster)", None


def walk_json(obj, path, rows, source):
    if isinstance(obj, dict):
        if "ci_low" in obj and "ci_high" in obj:
            draws = obj.get("draws")
            method, nominal = classify(path, obj.keys())
            if nominal is None:
                nominal = draws if draws in (N_PRIMARY, N_SENS) else (
                    N_PRIMARY if (draws or 0) > 100000 else N_SENS)
            lo, hi = obj.get("ci_low"), obj.get("ci_high")
            est = obj.get("estimate", obj.get("auc", obj.get("rho",
                  obj.get("or_per_10x_distance_plus_1A"))))
            rows.append({
                "source_file": source,
                "record_path": path,
                "quantity": path.rsplit("/", 1)[-1] or path,
                "method": method,
                "point_estimate": est,
                "ci_low": lo,
                "ci_high": hi,
                "n_sites": obj.get("n_sites", obj.get("n")),
                "nominal_draws": nominal if method.startswith(("bootstrap", "paired", "cluster", "wild")) else "",
                "retained_draws": draws if draws is not None else "not stored",
                "shortfall": (nominal - draws) if (draws is not None and isinstance(nominal, int)) else "",
                "endpoint_touches_0_or_1": touches_bound(lo, hi),
            })
        for k, v in obj.items():
            walk_json(v, f"{path}/{k}", rows, source)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_json(v, f"{path}[{i}]", rows, source)


def scan_csvs(rows):
    files = sorted(list((ROOT / "results").glob("*.csv")) +
                   list((ROOT / "robustness/results").glob("*.csv")))
    for f in files:
        with f.open() as fh:
            reader = csv.DictReader(fh)
            cols = reader.fieldnames or []
            pairs = []
            for c in cols:
                if c.endswith("ci_low"):
                    hi = c[:-len("ci_low")] + "ci_high"
                    if hi in cols:
                        pairs.append((c[:-len("ci_low")].rstrip("_"), c, hi))
            if not pairs:
                continue
            src = str(f.relative_to(ROOT))
            for i, row in enumerate(reader):
                label = " | ".join(str(row[k]) for k in cols[:2] if k in row)
                for prefix, clo, chi in pairs:
                    lo = row.get(clo)
                    hi = row.get(chi)
                    if lo in (None, "") or hi in (None, ""):
                        continue
                    lo, hi = float(lo), float(hi)
                    draws = row.get("draws") or row.get(f"{prefix}_draws") or ""
                    draws = int(draws) if draws not in ("", None) else None
                    method, nominal = classify(src + "/" + prefix, row.keys())
                    if nominal is None:
                        nominal = N_PRIMARY if (draws or 0) > 100000 else N_SENS
                    est = row.get("estimate") or row.get("auc") or row.get(f"{prefix}_auc") \
                        or row.get("rho") or row.get("or_per_10x_distance_plus_1A") or ""
                    rows.append({
                        "source_file": src,
                        "record_path": f"row {i}: {label}" + (f" [{prefix}]" if prefix else ""),
                        "quantity": prefix or "estimate",
                        "method": method,
                        "point_estimate": est,
                        "ci_low": lo,
                        "ci_high": hi,
                        "n_sites": row.get("n_sites", ""),
                        "nominal_draws": nominal if "analytic" not in method else "",
                        "retained_draws": draws if draws is not None else "not stored",
                        "shortfall": (nominal - draws) if draws is not None else "",
                        "endpoint_touches_0_or_1": touches_bound(lo, hi),
                    })


def rr13():
    rows = []
    for rel in ["results/statistics.json", "results/cohort_arm_statistics.json",
                "robustness/results/robustness_statistics.json"]:
        walk_json(json.loads((ROOT / rel).read_text()), "", rows, rel)
    scan_csvs(rows)
    return rows


# ---------------------------------------------------------------- RR-59

def rr59(p05):
    import pandas as pd
    bench = pd.read_csv(ROOT / "robustness/results/predictor_benchmark.csv")
    oof = pd.read_csv(ROOT / "robustness/results/robustness_analysis_with_oof_predictions.csv")
    y = oof["has_pheno"].astype(int).to_numpy()
    out = []
    for _, r in bench.iterrows():
        col = f"oof_{r['model']}"
        recomputed = (p05.auc_from_ranks(y, oof[col].to_numpy())
                      if col in oof.columns else None)
        out.append({
            "model": r["model"],
            "features": r["features"],
            "n_features": 0 if r["features"] == "none" else len(str(r["features"]).split(";")),
            "split_averaged_estimate": float(r["estimate"]),
            "split_low_2.5pct": float(r["split_low"]),
            "split_high_97.5pct": float(r["split_high"]),
            "pooled_oof_auc_stored": float(r["pooled_oof_auc"]),
            "pooled_oof_auc_recomputed_frozen_estimator": recomputed,
            "pooled_minus_split_averaged": float(r["pooled_oof_auc"]) - float(r["estimate"]),
            "brier": float(r["brier"]),
        })
    return out, int(len(oof)), int(y.sum())


def main():
    verify_frozen()
    p05 = load_module()
    rr13_rows = rr13()
    rr59_rows, n_oof, n_pos = rr59(p05)

    fields = ["source_file", "record_path", "quantity", "method", "point_estimate",
              "ci_low", "ci_high", "n_sites", "nominal_draws", "retained_draws",
              "shortfall", "endpoint_touches_0_or_1"]
    with (OUT / "rr13_bootstrap_draw_audit.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rr13_rows)

    with (OUT / "rr59_predictor_benchmark_dual_summary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rr59_rows[0].keys()))
        w.writeheader()
        w.writerows(rr59_rows)

    shortfalls = [r for r in rr13_rows if isinstance(r["shortfall"], int) and r["shortfall"] > 0]
    touching = [r for r in rr13_rows if r["endpoint_touches_0_or_1"]]
    not_stored = [r for r in rr13_rows if r["retained_draws"] == "not stored"
                  and "analytic" not in r["method"]]
    canonical = [r for r in rr13_rows if r["retained_draws"] == 200000]

    summary = {
        "frozen_hashes_verified": True,
        "seed_base": p05.SEED,
        "n_primary_boot": p05.N_PRIMARY_BOOT,
        "n_sensitivity_boot": p05.N_SENSITIVITY_BOOT,
        "n_corr_boot": p05.N_CORR_BOOT,
        "n_wild": p05.N_WILD,
        "rr13_total_interval_records": len(rr13_rows),
        "rr13_records_with_shortfall": len(shortfalls),
        "rr13_records_touching_0_or_1": len(touching),
        "rr13_resampling_records_without_stored_retained_count": len(not_stored),
        "rr13_records_retaining_full_200000": len(canonical),
        "rr13_shortfall_detail": [
            {k: r[k] for k in ("source_file", "record_path", "quantity", "nominal_draws",
                               "retained_draws", "shortfall", "ci_low", "ci_high",
                               "endpoint_touches_0_or_1")} for r in shortfalls],
        "rr13_endpoint_detail": [
            {k: r[k] for k in ("source_file", "record_path", "point_estimate", "n_sites",
                               "ci_low", "ci_high", "retained_draws")} for r in touching],
        "rr59": {"n_rows_oof": n_oof, "n_positive": n_pos, "models": rr59_rows},
        "notes": [
            "robustness/src/02_robustness_analysis.py bootstrap_auc returns draws=len(draws), the "
            "retained count after discarding single-class resamples. Every 'draws' value in "
            "robustness/results/ is therefore a genuine retained count.",
            "src/03_analysis.py boot_auc returns only (point, lo, hi); results/statistics.json "
            "and results/cohort_arm_primary_estimates.csv write 'draws': N_PRIMARY_BOOT and "
            "'naive_site_draws': N_PRIMARY_BOOT as literal constants (src/03_analysis.py lines "
            "124, 129). Those 200000 entries are nominal, not measured retention.",
            "src/03_analysis.py auc_other_predictors and sift_comparator store no draw count at "
            "all; their nominal count is N_SENSITIVITY_BOOT = 20000 by the boot_auc default.",
            "robustness/results/sift_comparator_sensitivity.csv omits a draws column, but the same "
            "intervals in robustness_statistics.json carry draws=20000.",
            "results/cohort_arm_statistics.json is byte-identical to results/statistics.json "
            "(sha256 57d02d5b...); its records are duplicates, not independent estimates.",
        ],
    }
    (OUT / "rr13_rr59_audit.json").write_text(json.dumps(summary, indent=2))

    print(f"RR-13 interval records: {len(rr13_rows)}")
    print(f"  with shortfall: {len(shortfalls)}")
    print(f"  touching 0 or 1: {len(touching)}")
    print(f"  resampling records with no stored retained count: {len(not_stored)}")
    for r in shortfalls:
        print("  SHORTFALL", r["source_file"], r["record_path"], r["retained_draws"],
              "/", r["nominal_draws"])
    for r in touching:
        print("  ENDPOINT", r["source_file"], r["record_path"], r["ci_low"], r["ci_high"])
    print("\nRR-59")
    for r in rr59_rows:
        print(f"  {r['model']:<22} split-avg {r['split_averaged_estimate']:.6f} "
              f"pooled {r['pooled_oof_auc_stored']:.6f} "
              f"recomputed {r['pooled_oof_auc_recomputed_frozen_estimator']}")


if __name__ == "__main__":
    main()
