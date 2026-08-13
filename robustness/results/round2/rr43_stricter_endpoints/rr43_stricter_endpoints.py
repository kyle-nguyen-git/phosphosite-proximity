#!/usr/bin/env python3
"""
RR-43: stricter outcome endpoints for the phosphosite-distance calibration.

Published endpoint: "at least one condition with source qvalue < 0.05", operationalised as
raw_q05_mean_per_strain > 0 (the replicate-averaged called-condition count). This script
recomputes the primary and inclusive-sensitivity AUCs under >= 2 and >= 3 called-condition
endpoints, using the project's own estimators loaded from the frozen phase 0.5 module.

Read-only with respect to the frozen tree. All outputs land in this directory.
"""

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

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


def verify_hashes():
    for rel, expected in FROZEN_HASHES.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if got != expected:
            raise SystemExit(f"ABORT: hash mismatch for {rel}\n  expected {expected}\n  got      {got}")
        print(f"[hash ok] {rel}")


# ---------------------------------------------------------------- estimators
# 02_robustness_analysis.py guards its main() behind `if __name__ == "__main__"`,
# so importing it executes definitions only and writes nothing.
def load_module():
    spec = importlib.util.spec_from_file_location(
        "p05", str(ROOT / "robustness" / "src" / "02_robustness_analysis.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- conventions
N_BOOT = 20000          # declared post hoc sensitivity draws
# base seed = module SEED, set after import


def interval_is_degenerate(lo, hi):
    """Declared rule: report no interval whose endpoint touches exactly 0 or 1."""
    return lo == 0.0 or hi == 1.0 or lo == 1.0 or hi == 0.0


def main():
    verify_hashes()
    p05 = load_module()
    SEED = p05.SEED
    print(f"[module] SEED={SEED}  N_PRIMARY_BOOT={p05.N_PRIMARY_BOOT}  "
          f"N_SENSITIVITY_BOOT={p05.N_SENSITIVITY_BOOT}")

    d = pd.read_csv(ROOT / "robustness" / "results" / "robustness_analysis.csv")
    assert len(d) == 166, len(d)

    # cohort flags, reconstructed exactly as the frozen module does
    d["cohort_primary_exclude_annotation_coincident"] = ~d.is_itself_annot.astype(bool)
    d["cohort_inclusive_sensitivity"] = True

    # ---------------------------------------------------------- replicate rule
    # Per-strain called-condition counts from the source supplement, so the
    # averaged rule and the per-strain rule can be compared directly.
    supp = pd.read_excel(ROOT / "data" / "EMS132528-supplement-Supplementary_Data_3.xlsx")
    supp["_pby"] = supp["PBY ID"].astype(str)
    per_strain_called = supp.groupby("_pby").apply(
        lambda t: int((t.qvalue < 0.05).sum()), include_groups=False
    ).to_dict()

    def strain_counts(row):
        ids = [s for s in str(row.member_strain_ids).split(";") if s and s != "nan"]
        return [per_strain_called.get(s, np.nan) for s in ids]

    d["sc_counts"] = [strain_counts(r) for r in d.itertuples()]
    d["sc_n_strains"] = d["sc_counts"].apply(len)
    d["sc_sum"] = d["sc_counts"].apply(lambda v: float(np.sum(v)) if len(v) else np.nan)
    d["sc_max"] = d["sc_counts"].apply(lambda v: float(np.max(v)) if len(v) else np.nan)
    d["sc_min"] = d["sc_counts"].apply(lambda v: float(np.min(v)) if len(v) else np.nan)
    d["sc_mean"] = d["sc_sum"] / d["sc_n_strains"]

    # consistency check against the frozen column
    delta = (d["sc_mean"] - d["raw_q05_mean_per_strain"]).abs()
    print(f"[check] max |recomputed mean - raw_q05_mean_per_strain| = {delta.max():.12g}")
    print(f"[check] published has_pheno == (raw_q05_mean_per_strain > 0): "
          f"{bool((d.has_pheno.astype(int) == (d.raw_q05_mean_per_strain > 0).astype(int)).all())}")
    print(f"[check] substitutions with >1 member strain: {int((d.sc_n_strains > 1).sum())}")

    replicated = d[d.sc_n_strains > 1]
    rep_rows = []
    for r in replicated.itertuples():
        rep_rows.append({
            "acc": r.acc, "pos": int(r.pos),
            "substitution": f"{r.pmt_aa_wt}{int(r.pos)}{r.pmt_aa_mutant}",
            "member_strain_ids": r.member_strain_ids,
            "per_strain_counts": ";".join(str(int(v)) for v in r.sc_counts),
            "mean": r.sc_mean, "min": r.sc_min, "max": r.sc_max,
        })
        print(f"[replicate] {r.acc} {int(r.pos)} strains={r.member_strain_ids} "
              f"counts={r.sc_counts} mean={r.sc_mean}")

    # Three candidate replicate rules:
    #   AVG  : threshold on the replicate-averaged count      (mean >= k)
    #   ANY  : threshold per strain, positive if any strain qualifies (max >= k)
    #   ALL  : threshold per strain, positive only if every strain qualifies (min >= k)
    # At k=1, AVG and ANY are algebraically identical to the published mean>0 rule.
    rules = {
        "avg": lambda k: (d["sc_mean"] >= k),
        "any": lambda k: (d["sc_max"] >= k),
        "all": lambda k: (d["sc_min"] >= k),
    }

    # ------------------------------------------------- class-change reporting
    rule_diffs = []
    for k in (1, 2, 3):
        lab = {name: fn(k).astype(int) for name, fn in rules.items()}
        for a, b in (("avg", "any"), ("avg", "all")):
            diff = d[lab[a] != lab[b]]
            for r in diff.itertuples():
                rule_diffs.append({
                    "threshold": k, "rule_a": a, "rule_b": b,
                    "acc": r.acc, "pos": int(r.pos),
                    "substitution": f"{r.pmt_aa_wt}{int(r.pos)}{r.pmt_aa_mutant}",
                    "per_strain_counts": ";".join(str(int(v)) for v in r.sc_counts),
                    f"label_{a}": int(lab[a].loc[r.Index]), f"label_{b}": int(lab[b].loc[r.Index]),
                })
    print(f"[rules] substitution-level class disagreements between rules: {len(rule_diffs)}")

    # verify k=1 avg rule reproduces the published label exactly
    assert (rules["avg"](1).astype(int).values == d.has_pheno.astype(int).values).all(), \
        "avg>=1 does not reproduce published has_pheno"
    assert (rules["any"](1).astype(int).values == d.has_pheno.astype(int).values).all(), \
        "any>=1 does not reproduce published has_pheno"
    print("[check] both avg>=1 and any>=1 reproduce published has_pheno exactly")

    # ------------------------------------------------------------- estimation
    arms = {
        "primary_exclude_annotation_coincident": d.cohort_primary_exclude_annotation_coincident.values,
        "inclusive_sensitivity": d.cohort_inclusive_sensitivity.values,
    }

    records = []
    for rule_name in ("avg", "any", "all"):
        for k in (1, 2, 3):
            y_full = rules[rule_name](k).astype(int).values
            for arm, mask in arms.items():
                sub = d.loc[mask]
                y = y_full[mask]
                score = -sub.dist_core_A.values      # shorter distance -> screen-positive
                groups = sub.acc.values
                n = int(len(sub))
                pos = int(y.sum())
                rec = {
                    "rule": rule_name, "threshold_k": k, "arm": arm,
                    "n": n, "positives": pos, "negatives": n - pos,
                    "n_proteins": int(sub.acc.nunique()),
                    "n_proteins_with_positive": int(sub.loc[y == 1, "acc"].nunique()),
                    "nominal_draws": N_BOOT, "seed": SEED,
                }
                if pos == 0 or pos == n:
                    rec.update({"auc": np.nan, "ci_low": np.nan, "ci_high": np.nan,
                                "retained_draws": 0, "interval_reported": False,
                                "note": "single outcome class; AUC undefined"})
                else:
                    b = p05.bootstrap_auc(y, score, groups=groups, n=N_BOOT, seed=SEED)
                    degen = interval_is_degenerate(b["ci_low"], b["ci_high"])
                    rec.update({
                        "auc": b["estimate"], "ci_low": b["ci_low"], "ci_high": b["ci_high"],
                        "retained_draws": b["draws"],
                        "interval_reported": not degen,
                        "note": ("interval endpoint touches 0 or 1; point estimate with n only"
                                 if degen else ""),
                    })
                records.append(rec)
                print(f"  {rule_name} k>={k} {arm:42s} n={n:3d} pos={pos:3d} "
                      f"AUC={rec['auc']:.6f} CI=[{rec['ci_low']:.6f},{rec['ci_high']:.6f}] "
                      f"retained={rec['retained_draws']}/{N_BOOT}")

    res = pd.DataFrame(records)
    res.to_csv(OUT / "rr43_endpoint_results.csv", index=False)

    # ------------------------------- reproduce published k>=1 at published settings
    repro = {}
    for arm, mask in arms.items():
        sub = d.loc[mask]
        y = d.has_pheno.astype(int).values[mask]
        b = p05.bootstrap_auc(y, -sub.dist_core_A.values, groups=sub.acc.values,
                              n=p05.N_PRIMARY_BOOT, seed=SEED + 1)
        repro[arm] = b
        print(f"[repro published] {arm}: AUC={b['estimate']:.16f} "
              f"CI=[{b['ci_low']:.16f},{b['ci_high']:.16f}] draws={b['draws']}")

    # ------------------------------------------- survival of the 79 primary positives
    prim = d.loc[arms["primary_exclude_annotation_coincident"]].copy()
    pos79 = prim[prim.has_pheno.astype(bool)].copy()
    survival = {}
    for k in (1, 2, 3):
        survival[k] = int((pos79["sc_mean"] >= k).sum())
    print(f"[survival] of {len(pos79)} primary positives: "
          f">=1 {survival[1]}, >=2 {survival[2]}, >=3 {survival[3]}")

    drops2 = pos79[pos79["sc_mean"] < 2].copy()
    drops3 = pos79[(pos79["sc_mean"] >= 2) & (pos79["sc_mean"] < 3)].copy()

    def droplist(frame):
        out = []
        for _, r in frame.sort_values(["acc", "pos"]).iterrows():
            out.append({
                "acc": r["acc"], "pos": int(r["pos"]),
                "substitution": f"{r['pmt_aa_wt']}{int(r['pos'])}{r['pmt_aa_mutant']}",
                "gene": r.get("Gene name", ""),
                "called_conditions_mean_per_strain": float(r["sc_mean"]),
                "n_member_strains": int(r["sc_n_strains"]),
                "dist_core_A": float(r["dist_core_A"]),
            })
        return out

    drop_at_2 = droplist(drops2)
    drop_at_3_additional = droplist(drops3)

    payload = {
        "roadmap_item": "RR-43",
        "frozen_hashes_verified": True,
        "conventions": {
            "resampling_unit": "UniProt accession (acc); all substitutions of a sampled protein retained",
            "nominal_draws": N_BOOT,
            "seed": SEED,
            "bootstrap": "p05.bootstrap_auc from robustness/src/02_robustness_analysis.py (frozen)",
            "auc": "p05.auc_from_ranks (average ranks for ties)",
            "score": "-dist_core_A (shorter distance scored toward screen-positive)",
            "note_vs_published": ("published primary/inclusive intervals use n=200000, seed=SEED+1; "
                                  "post hoc sensitivity here uses n=20000, seed=SEED as declared"),
            "endpoint_handling": ("raising the threshold reclassifies former positives as negatives; "
                                  "cohort n is unchanged at 163 / 166"),
        },
        "replicate_structure": {
            "n_substitutions_single_strain": int((d.sc_n_strains == 1).sum()),
            "n_substitutions_multi_strain": int((d.sc_n_strains > 1).sum()),
            "replicated_substitutions": rep_rows,
            "rule_disagreements": rule_diffs,
        },
        "published_reproduction": repro,
        "primary_positive_survival": {
            "n_primary_positives": int(len(pos79)),
            "surviving_ge1": survival[1],
            "surviving_ge2": survival[2],
            "surviving_ge3": survival[3],
            "dropped_at_ge2": drop_at_2,
            "dropped_additionally_at_ge3": drop_at_3_additional,
        },
        "results": records,
    }
    with (OUT / "rr43_endpoint_results.json").open("w") as fh:
        json.dump(payload, fh, indent=2, default=p05.to_builtin)
        fh.write("\n")
    print(f"[write] {OUT/'rr43_endpoint_results.csv'}")
    print(f"[write] {OUT/'rr43_endpoint_results.json'}")


if __name__ == "__main__":
    main()
