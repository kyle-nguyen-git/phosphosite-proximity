"""RR-28: characterize the annotation target set behind the phospho-distance calibration.

Read-only against the frozen tree. Writes only into rr28/.

Estimators are loaded from the frozen phase-0.5 analysis module (guarded by
__main__, so importing it does not run main()).
"""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "rr28"
OUT.mkdir(exist_ok=True)

FROZEN = {
    "results/statistics.json": "57d02d5b4eae6a7d5f18b78b20ffebe491cc4e5f6e23e49710aba71d448a0401",
    "results/analysis_final.csv": "e666827da317fd963074e91613748ba449fb7005c207bdf0b389bd8451ac4dd4",
    "robustness/results/robustness_statistics.json": "3ea01c7b0a8b8f80304e574753d24c07ee7d542975e4f4603443b07bf050d02b",
}
for rel, want in FROZEN.items():
    got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    if got != want:
        raise SystemExit(f"ABORT: hash mismatch for {rel}: {got} != {want}")
print("frozen hashes verified")

spec = importlib.util.spec_from_file_location(
    "p05", str(ROOT / "robustness/src/02_robustness_analysis.py")
)
p05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p05)
SEED = p05.SEED           # 20260728
NBOOT = 20000             # declared post hoc sensitivity convention

CORE_FEATURES = ("Active site", "Binding site")
EXPERIMENTAL = {"ECO:0000269", "ECO:0007744"}

det = pd.read_csv(ROOT / "results/uniprot_features_detailed.csv")
det["evidence_codes"] = det["evidence_codes"].fillna("")
core_rec = det[det.feat_type.isin(CORE_FEATURES)].copy()
core_rec["width"] = core_rec["end"] - core_rec["start"] + 1
core_rec["codes"] = core_rec.evidence_codes.apply(
    lambda s: frozenset(c for c in s.split(";") if c)
)
core_rec["is_exp"] = core_rec.codes.apply(lambda s: bool(s & EXPERIMENTAL))

prim = pd.read_csv(ROOT / "results/analysis_final.csv")
assert len(prim) == 163
accs = sorted(prim.acc.unique())

report = {}
report["conventions"] = {
    "experimental_definition": "evidence code set intersects {ECO:0000269, ECO:0007744}",
    "non_experimental": "ECO:0000255, ECO:0000250, ECO:0000305, or no evidence code",
    "core_feature_types": list(CORE_FEATURES),
    "bootstrap": f"protein-cluster, n={NBOOT} nominal draws, seed={SEED}",
    "score": "-min_dist_A (shorter distance scored toward screen-positive)",
}

# ---------------------------------------------------------------- structures
parser = MMCIFParser(QUIET=True)


def residue_atoms(structure):
    """Copied in spirit from src/02_structures.py: position -> (aa, atoms)."""
    from Bio.PDB.Polypeptide import protein_letters_3to1
    out = {}
    for residue in structure[0].get_residues():
        if residue.id[0] != " ":
            continue
        try:
            aa = protein_letters_3to1[residue.get_resname()]
        except KeyError:
            continue
        out[residue.id[1]] = (aa, [a for a in residue])
    return out


struct_res = {}
for acc in accs:
    path = ROOT / "data/af" / f"{acc}.cif"
    struct_res[acc] = residue_atoms(parser.get_structure(acc, str(path)))


def min_dist(res, pos, targets):
    if pos in targets:
        return 0.0, pos
    best, nearest = np.inf, np.nan
    for t in targets:
        for a1 in res[pos][1]:
            for a2 in res[t][1]:
                d = a1 - a2
                if d < best:
                    best, nearest = d, t
    return (float(best), nearest) if np.isfinite(best) else (np.nan, np.nan)


# expanded eligible target set per protein (all core records), as in the pipeline
core_pos = ROOT / "results/uniprot_features_core.csv"
core_expanded = pd.read_csv(core_pos)
targets_all = {
    acc: sorted({p for p in core_expanded.loc[core_expanded.acc == acc, "feat_pos"]
                 if p in struct_res[acc]})
    for acc in accs
}

# sanity: reproduce frozen min_dist_A with the full target set
chk = []
for _, r in prim.iterrows():
    d, nf = min_dist(struct_res[r.acc], int(r.pos), targets_all[r.acc])
    chk.append((d, nf))
chk_d = np.array([c[0] for c in chk])
max_abs_diff = float(np.nanmax(np.abs(chk_d - prim.min_dist_A.to_numpy())))
nearest_match = int(sum(int(c[1]) == int(p) for c, p in zip(chk, prim.nearest_feat_pos)))
report["recomputation_check"] = {
    "max_abs_distance_diff_A": max_abs_diff,
    "nearest_feat_pos_agreements": nearest_match,
    "n": len(prim),
}
print("recompute check:", report["recomputation_check"])

# ------------------------------------------------- 1. evidence of NEAREST target


def covering(acc, pos):
    m = core_rec[(core_rec.acc == acc) & (core_rec.start <= pos) & (core_rec.end >= pos)]
    return m


rows = []
for _, r in prim.iterrows():
    nf = int(r.nearest_feat_pos)
    m = covering(r.acc, nf)
    codes = frozenset().union(*m.codes) if len(m) else frozenset()
    rows.append({
        "acc": r.acc, "pos": int(r.pos), "nearest_feat_pos": nf,
        "n_covering_records": len(m),
        "codes": ";".join(sorted(codes)) if codes else "(none)",
        "is_experimental": bool(codes & EXPERIMENTAL),
        "feat_types": ";".join(sorted(set(m.feat_type))),
        "ligands": ";".join(sorted({x for x in m.ligand_name.fillna("") if x})),
        "min_dist_A": float(r.min_dist_A), "y": int(r.y),
    })
sub = pd.DataFrame(rows)
sub.to_csv(OUT / "rr28_substitution_target_evidence.csv", index=False)

report["item1_nearest_target_evidence_substitution_level"] = {
    "n_substitutions": len(sub),
    "code_set_counts": sub.codes.value_counts().to_dict(),
    "experimental": int(sub.is_experimental.sum()),
    "non_experimental": int((~sub.is_experimental).sum()),
    "substitutions_whose_nearest_residue_is_covered_by_more_than_one_record":
        int((sub.n_covering_records > 1).sum()),
    "max_covering_records": int(sub.n_covering_records.max()),
}

# ------------------------------------------- 2. evidence over expanded target set
exp_rows = []
for acc in accs:
    for pos in targets_all[acc]:
        m = covering(acc, pos)
        codes = frozenset().union(*m.codes) if len(m) else frozenset()
        exp_rows.append({
            "acc": acc, "feat_pos": pos, "n_covering_records": len(m),
            "codes": ";".join(sorted(codes)) if codes else "(none)",
            "is_experimental": bool(codes & EXPERIMENTAL),
        })
expanded = pd.DataFrame(exp_rows)
expanded.to_csv(OUT / "rr28_expanded_target_residues.csv", index=False)
report["item2_expanded_residue_level"] = {
    "n_target_residues_48_proteins": len(expanded),
    "n_proteins": int(expanded.acc.nunique()),
    "code_set_counts": expanded.codes.value_counts().to_dict(),
    "experimental": int(expanded.is_experimental.sum()),
    "non_experimental": int((~expanded.is_experimental).sum()),
    "residues_covered_by_more_than_one_record": int((expanded.n_covering_records > 1).sum()),
}

# --------------------------------------------------------- 3. ligand composition
lig = sub.ligands.replace("", "(none)")
report["item3_ligand_of_nearest_target"] = {
    "n_substitutions": len(sub),
    "distribution": lig.value_counts().to_dict(),
    "ATP": int((lig == "ATP").sum()),
    "ATP_containing": int(lig.str.contains("ATP").sum()),
}
report["item3_ligand_over_expanded_binding_residues"] = (
    core_rec[core_rec.feat_type == "Binding site"]
    .assign(n=lambda d: d.width)
    .groupby(core_rec.ligand_name.fillna("(none)"))["width"].sum().sort_values(ascending=False).to_dict()
)

# ------------------------------------------------- 4. interval widths of BINDING
bind = core_rec[core_rec.feat_type == "Binding site"].copy()
bind_all = det[det.feat_type == "Binding site"].copy()
bind_all["width"] = bind_all["end"] - bind_all["start"] + 1
w = bind.width
report["item4_binding_interval_widths"] = {
    "n_binding_records_all_57_proteins": int(len(bind_all)),
    "n_binding_records": int(len(bind)),
    "width_counts": w.value_counts().sort_index().to_dict(),
    "sum_of_widths_all_binding_records": int(w.sum()),
    "records_width_ge_8": int((w >= 8).sum()),
    "residues_from_records_width_ge_8": int(w[w >= 8].sum()),
    "median_width": float(w.median()),
    "max_width": int(w.max()),
}
# restricted to the 48 primary-cohort proteins
b48 = bind[bind.acc.isin(accs)]
report["item4_binding_interval_widths_48_proteins"] = {
    "n_binding_records": int(len(b48)),
    "sum_of_widths": int(b48.width.sum()),
    "records_width_ge_8": int((b48.width >= 8).sum()),
    "residues_from_records_width_ge_8": int(b48.width[b48.width >= 8].sum()),
}
# and how many *deduplicated eligible* residues are touched by a wide record
wide_pos = set()
for _, r in bind[bind.width >= 8].iterrows():
    for p in range(int(r.start), int(r.end) + 1):
        wide_pos.add((r.acc, p))
expanded["from_wide_record"] = [
    (a, p) in wide_pos for a, p in zip(expanded.acc, expanded.feat_pos)
]
report["item4_dedup_eligible_residues_from_wide_records"] = {
    "n_eligible_residues": len(expanded),
    "from_records_width_ge_8": int(expanded.from_wide_record.sum()),
}

# ------------------------------------------------------------- 5. kinase status
prot = pd.read_csv(ROOT / "data/yeast_sgd_uniprot.tsv", sep="\t")
prot.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "length"]
p48 = prot[prot.acc.isin(accs)][["acc", "entry", "gene", "pname"]].copy()
p48["any_kinase_in_name"] = p48.pname.str.contains("kinase", case=False, na=False)
p48["protein_kinase"] = p48.pname.str.contains(
    r"protein kinase|protein-serine|serine/threonine|tyrosine-protein kinase|kinase [A-Z]* ?catalytic",
    case=False, regex=True, na=False)
p48.to_csv(OUT / "rr28_primary_cohort_proteins.csv", index=False)
report["item5_kinases"] = {
    "n_proteins": len(p48),
    "name_contains_kinase": int(p48.any_kinase_in_name.sum()),
    "protein_kinase_by_name_regex": int(p48.protein_kinase.sum()),
    "kinase_named_entries": p48[p48.any_kinase_in_name][["acc", "gene", "pname"]].to_dict("records"),
}

# ------------------------------------ 6. experimental-only eligible target set
targets_exp = {}
for acc in accs:
    pos = set()
    for _, r in core_rec[(core_rec.acc == acc) & (core_rec.is_exp)].iterrows():
        pos.update(range(int(r.start), int(r.end) + 1))
    targets_exp[acc] = sorted(p for p in pos if p in struct_res[acc])

rec2 = []
for _, r in prim.iterrows():
    t = targets_exp[r.acc]
    if not t:
        rec2.append({"acc": r.acc, "pos": int(r.pos), "y": int(r.y),
                     "min_dist_exp_A": np.nan, "nearest_exp_pos": np.nan,
                     "n_exp_targets": 0})
        continue
    d, nf = min_dist(struct_res[r.acc], int(r.pos), t)
    rec2.append({"acc": r.acc, "pos": int(r.pos), "y": int(r.y),
                 "min_dist_exp_A": d, "nearest_exp_pos": nf, "n_exp_targets": len(t)})
expsub = pd.DataFrame(rec2)
expsub = expsub.merge(prim[["acc", "pos", "min_dist_A"]], on=["acc", "pos"], how="left")
expsub.to_csv(OUT / "rr28_experimental_only_distances.csv", index=False)

keep = expsub[expsub.min_dist_exp_A.notna()].copy()
res6 = {
    "n_substitutions_total": len(expsub),
    "n_retaining_an_experimental_target": int(len(keep)),
    "n_losing_all_targets": int(len(expsub) - len(keep)),
    "n_proteins_total": len(accs),
    "n_proteins_with_experimental_target": int((keep.acc.nunique())),
    "n_positive_retained": int(keep.y.sum()),
    "n_negative_retained": int((keep.y == 0).sum()),
    "any_zero_distance_after_restriction": int((keep.min_dist_exp_A == 0).sum()),
    "median_dist_exp_positive": float(np.median(keep.min_dist_exp_A[keep.y == 1])) if keep.y.sum() else None,
    "median_dist_exp_negative": float(np.median(keep.min_dist_exp_A[keep.y == 0])) if (keep.y == 0).sum() else None,
}
if len(keep) and keep.y.nunique() == 2:
    b = p05.bootstrap_auc(keep.y.to_numpy(), -keep.min_dist_exp_A.to_numpy(),
                          groups=keep.acc.to_numpy(), n=NBOOT, seed=SEED)
    res6["auc_experimental_only_targets"] = {**b, "nominal_draws": NBOOT, "seed": SEED}
    # same substitutions, but scored with the ORIGINAL full-annotation distance
    b2 = p05.bootstrap_auc(keep.y.to_numpy(), -keep.min_dist_A.to_numpy(),
                           groups=keep.acc.to_numpy(), n=NBOOT, seed=SEED)
    res6["auc_same_subset_full_annotation_distance"] = {**b2, "nominal_draws": NBOOT, "seed": SEED}
    pd_ = p05.paired_auc_difference(keep.y.to_numpy(), -keep.min_dist_exp_A.to_numpy(),
                                    -keep.min_dist_A.to_numpy(), keep.acc.to_numpy(),
                                    n=NBOOT, seed=SEED)
    res6["paired_difference_exp_minus_full_on_retained_subset"] = {
        **pd_, "nominal_draws": NBOOT, "seed": SEED}
report["item6_experimental_only_restriction"] = res6

with open(OUT / "rr28_results.json", "w") as fh:
    json.dump(report, fh, indent=1, default=str)
print(json.dumps(report, indent=1, default=str)[:4000])
