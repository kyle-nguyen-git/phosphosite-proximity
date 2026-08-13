"""RR-30 / RR-58: comparator predictor table on the primary cohort.

Read-only with respect to the frozen tree. Writes only into notes/rr30_rr58/.

Estimators are loaded from the frozen module robustness/src/02_robustness_analysis.py
(auc_from_ranks, bootstrap_auc, paired_auc_difference). That module is guarded by
`if __name__ == "__main__": main()`, so importing it under the name "p05" does not
run main(); verified before use.

Conventions (declared, enforced here):
  - 20,000 protein-cluster bootstrap draws, base seed = module SEED (20260728).
  - Resampling unit is the UniProt accession (`acc`).
  - bootstrap_auc / paired_auc_difference discard resamples with a single outcome
    class; the retained draw count is reported alongside the nominal count (RR-13).
  - Scoring orientation: each predictor is signed so that the direction hypothesised
    to favour a screen-positive label is the direction of increasing score.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

FROZEN_HASHES = {
    "results/statistics.json":
        "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv":
        "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "robustness/results/robustness_statistics.json":
        "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_frozen() -> None:
    for rel, expected in FROZEN_HASHES.items():
        got = sha256(ROOT / rel)
        if got != expected:
            raise SystemExit(f"ABORT: hash mismatch for {rel}\n  expected {expected}\n  got      {got}")
    print("frozen hashes verified (3/3)")


def load_estimators():
    src = ROOT / "robustness" / "src" / "02_robustness_analysis.py"
    text = src.read_text()
    if 'if __name__ == "__main__":' not in text:
        raise SystemExit("ABORT: frozen analysis module is not __main__-guarded; refusing to import.")
    spec = importlib.util.spec_from_file_location("p05", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- data

def eligible_targets(features_csv: Path):
    """ACT_SITE + BINDING records only, intervals expanded to each covered residue."""
    f = pd.read_csv(features_csv)
    elig = f[f["feat_type"].isin(["Active site", "Binding site"])].copy()
    per_acc: dict[str, set[int]] = {}
    n_rows = 0
    for _, r in elig.iterrows():
        s, e = int(r["start"]), int(r["end"])
        for p in range(s, e + 1):
            per_acc.setdefault(r["acc"], set()).add(p)
            n_rows += 1
    n_unique = sum(len(v) for v in per_acc.values())
    return per_acc, {
        "records_total": int(len(f)),
        "records_eligible": int(len(elig)),
        "records_active_site": int((elig["feat_type"] == "Active site").sum()),
        "records_binding_site": int((elig["feat_type"] == "Binding site").sum()),
        "feature_residue_rows": int(n_rows),
        "unique_target_residues": int(n_unique),
        "accessions_with_targets": int(len(per_acc)),
    }


def min_seq_sep_to_eligible(d: pd.DataFrame, per_acc: dict[str, set[int]]) -> np.ndarray:
    vals = []
    for acc, pos in zip(d["acc"], d["pos"]):
        tgt = per_acc.get(acc)
        if not tgt:
            vals.append(np.nan)
        else:
            vals.append(min(abs(int(pos) - t) for t in tgt))
    return np.asarray(vals, dtype=float)


# ---------------------------------------------------------------- main

def main() -> None:
    verify_frozen()
    p05 = load_estimators()
    print(f"estimators loaded from frozen module; SEED={p05.SEED}, "
          f"N_SENSITIVITY_BOOT={p05.N_SENSITIVITY_BOOT}")
    n_boot = p05.N_SENSITIVITY_BOOT
    seed = p05.SEED
    assert n_boot == 20000 and seed == 20260728

    d = pd.read_csv(ROOT / "robustness" / "results" / "robustness_analysis.csv")
    d = d[d["cohort_primary_exclude_annotation_coincident"].astype(bool)].reset_index(drop=True)

    # cross-check the cohort against the frozen primary file
    fin = pd.read_csv(ROOT / "results" / "analysis_final.csv")
    assert set(zip(d["acc"], d["pos"])) == set(zip(fin["acc"], fin["pos"])), "cohort mismatch"
    assert len(d) == 163, len(d)

    per_acc, tgt_stats = eligible_targets(ROOT / "results" / "uniprot_features_detailed.csv")
    print("eligible target set:", json.dumps(tgt_stats))
    missing = sorted(set(d["acc"]) - set(per_acc))
    print(f"cohort accessions without an eligible target: {len(missing)} {missing}")

    d["min_seq_sep_eligible"] = min_seq_sep_to_eligible(d, per_acc)
    d["seq_sep_to_nearest3d"] = (d["pos"] - d["nearest_feat_pos"]).abs().astype(float)

    y = d["y"].to_numpy(dtype=int)
    groups = d["acc"].to_numpy()

    # Each entry: (key, label, raw column, sign). sign=-1 means smaller values are
    # scored toward a screen-positive label.
    spec = [
        ("min_seq_sep_eligible", "min |pos - target pos|, eligible ACT_SITE+BINDING set",
         "min_seq_sep_eligible", -1),
        ("seq_sep_to_nearest3d", "|pos - nearest_feat_pos| (seq sep to 3D-nearest target)",
         "seq_sep_to_nearest3d", -1),
        ("protein_length", "protein_length", "protein_length", +1),
        ("plddt", "site pLDDT", "plddt", +1),
        ("rsa_inv", "inverse relative solvent accessibility", "rsa", -1),
        ("n_annot_residues", "n_annot_residues (annotated-target count)",
         "n_annot_residues", +1),
        ("raw_conditions", "raw_conditions (bookkeeping negative control)",
         "raw_conditions", +1),
        ("min_dist_A", "min heavy-atom distance (declared predictor)", "min_dist_A", -1),
    ]

    ref_key = "min_dist_A"
    ref_score = -d["min_dist_A"].to_numpy(dtype=float)

    rows = []
    for key, label, col, sign in spec:
        raw = d[col].to_numpy(dtype=float)
        ok = np.isfinite(raw)
        score = sign * raw
        n = int(ok.sum())
        # both orientations, for the record
        auc_pos = p05.auc_from_ranks(y[ok], raw[ok])
        auc_signed = p05.auc_from_ranks(y[ok], score[ok])
        boot = p05.bootstrap_auc(y[ok], score[ok], groups=groups[ok], n=n_boot, seed=seed)
        n_uniq_vals = int(np.unique(raw[ok]).size)

        row = {
            "key": key,
            "predictor": label,
            "orientation": ("smaller -> screen-positive" if sign < 0
                            else "larger -> screen-positive"),
            "n": n,
            "n_proteins": int(pd.unique(groups[ok]).size),
            "n_distinct_values": n_uniq_vals,
            "auc": boot["estimate"],
            "auc_as_stored_ascending": auc_pos,
            "auc_signed_check": auc_signed,
            "ci_low": boot["ci_low"],
            "ci_high": boot["ci_high"],
            "boot_nominal": n_boot,
            "boot_retained": boot["draws"],
        }

        if key == ref_key:
            row.update({
                "diff_vs_distance": 0.0,
                "diff_ci_low": None,
                "diff_ci_high": None,
                "diff_boot_nominal": None,
                "diff_boot_retained": None,
                "diff_note": "reference predictor; difference against itself is identically 0",
            })
        else:
            common = ok & np.isfinite(ref_score)
            diff = p05.paired_auc_difference(
                y[common], score[common], ref_score[common], groups[common],
                n=n_boot, seed=seed,
            )
            row.update({
                "diff_n_common": int(common.sum()),
                "diff_vs_distance": diff["estimate"],
                "diff_ci_low": diff["ci_low"],
                "diff_ci_high": diff["ci_high"],
                "diff_boot_nominal": n_boot,
                "diff_boot_retained": diff["draws"],
                "diff_note": "",
            })
        rows.append(row)
        print(f"  {key:24s} n={n:3d} AUC={row['auc']:.6f} "
              f"[{row['ci_low']:.6f}, {row['ci_high']:.6f}] retained={boot['draws']}")

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "rr30_rr58_comparator_table.csv", index=False)
    with open(OUT / "rr30_rr58_comparator_table.json", "w") as fh:
        json.dump(
            {
                "cohort": "primary (exclude_annotation_coincident)",
                "n_sites": int(len(d)),
                "n_positives": int(y.sum()),
                "n_proteins": int(pd.unique(groups).size),
                "seed": int(seed),
                "bootstrap_nominal_draws": int(n_boot),
                "resampling_unit": "UniProt accession",
                "eligible_target_set": tgt_stats,
                "rows": rows,
            },
            fh,
            indent=2,
            default=p05.to_builtin,
        )
    print(f"\nwrote {OUT/'rr30_rr58_comparator_table.csv'}")
    print(f"wrote {OUT/'rr30_rr58_comparator_table.json'}")


if __name__ == "__main__":
    main()
