"""Distance from the phospho-accepting oxygen, for both cohorts.

David Chang's first review point, 2026-08-18. The declared predictor is the shortest heavy-atom
separation between the modified residue and the nearest annotated target, backbone included. The
phosphate attaches to the side-chain tip — OG in serine, OG1 in threonine, OH in tyrosine — and the
backbone is identical in every residue whether or not it is a phosphosite. Two consecutive residues are
covalently bonded backbone-to-backbone at a fixed ~1.33 Angstrom, so under the declared definition any
adjacent pair returns that constant. The peptide-bond band the paper reports is therefore a property of
the measurement, not of the data.

This computes the alternative: from the tip oxygen of the modified residue to any non-hydrogen atom of
the target residue. Everything else — target set, structures, exclusion rules — is unchanged, so the two
predictors are comparable on the same rows.

Outputs `tip_distance_yeast.csv` and `tip_distance_human.csv`. Nothing here may enter a manuscript, wiki
page or email until it is registered in NUMBERS.md.
"""
from __future__ import annotations
import os, sys, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
YEAST_AF = os.path.join(RESEARCH, "phase0_calibration", "data", "af")
HUMAN_AF = os.path.join(RESEARCH, "kennedy_replication", "cache", "af")
TIP = {"S": "OG", "T": "OG1", "Y": "OH"}


def tip_distances(cohort, af_dir, targets_by_acc, label):
    """Per site: distance from its tip oxygen to the nearest heavy atom of any eligible target."""
    from Bio.PDB import MMCIFParser
    from Bio.Data.IUPACData import protein_letters_3to1_extended as three_to_one
    parser = MMCIFParser(QUIET=True)
    out = []
    for acc, sites in cohort.groupby("acc"):
        path = os.path.join(af_dir, f"{acc}.cif")
        tgt = sorted(targets_by_acc.get(acc, []))
        if not os.path.exists(path) or not tgt:
            continue
        try:
            st = parser.get_structure(acc, path)
        except Exception:
            continue
        res = {}
        for r in st[0].get_residues():
            if r.id[0] != " ":
                continue
            try:
                aa1 = three_to_one[r.get_resname().capitalize()]
            except KeyError:
                continue
            res[r.id[1]] = (aa1, [a for a in r if a.element != "H"])
        for row in sites.itertuples():
            if row.pos not in res:
                continue
            aa1, atoms = res[row.pos]
            if aa1 != row.aa:
                continue
            want = TIP.get(row.aa)
            tip = next((a for a in atoms if a.get_id() == want), None)
            rec = {"acc": acc, "pos": row.pos, "aa": row.aa,
                   "tip_atom": want, "tip_present": tip is not None}
            best, at = np.inf, np.nan
            if tip is not None:
                for t in tgt:
                    if t not in res or t == row.pos:
                        continue
                    for a2 in res[t][1]:
                        d = tip - a2
                        if d < best:
                            best, at = d, t
            rec["tip_dist_A"] = float(best) if np.isfinite(best) else np.nan
            rec["tip_nearest_feat_pos"] = at
            out.append(rec)
    df = pd.DataFrame(out)
    got = set(zip(df.acc, df.pos)); want = set(zip(cohort.acc, cohort.pos))
    if want - got:
        raise RuntimeError(f"{len(want - got)} cohort sites produced no row, e.g. {sorted(want - got)[:5]}")
    print(f"  {label}: {len(df)} rows, tip atom present on {int(df.tip_present.sum())}, "
          f"distance on {int(df.tip_dist_A.notna().sum())}", flush=True)
    return df


def yeast():
    coh = pd.read_csv(os.path.join(RESEARCH, "phase0_calibration", "phase0_5", "results",
                                   "phase0_5_primary_analysis.csv"))
    # the "core" target set is ACT_SITE + BINDING, matching the declared predictor
    feat = pd.read_csv(os.path.join(RESEARCH, "phase0_calibration", "results",
                                    "uniprot_features_core.csv"))
    tg = {a: set(g["feat_pos"]) for a, g in feat.groupby("acc")}
    return tip_distances(coh, YEAST_AF, tg, "yeast")


def human():
    coh = pd.read_csv(os.path.join(RESEARCH, "kennedy_replication", "kennedy_analysis_corrected.csv"))
    coh = coh[coh.min_dist_A.notna()]
    # The corrected target file, not the pre-rebuild one. `uniprot_targets.csv` holds the 818 accessions
    # of the superseded cohort and lacks Q2Y0W8, which entered in the 2026-08-14 rebuild; using it
    # silently dropped that protein and its site.
    feat = pd.read_csv(os.path.join(RESEARCH, "kennedy_replication", "uniprot_targets_corrected.csv"))
    tg = {a: set(g["res"]) for a, g in feat.groupby("acc")}
    missing = sorted(set(coh.acc) - set(tg))
    if missing:
        raise RuntimeError(f"target file does not cover {len(missing)} cohort accessions: {missing[:5]}")
    return tip_distances(coh, HUMAN_AF, tg, "human")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("yeast", "both"):
        yeast().to_csv(os.path.join(HERE, "tip_distance_yeast.csv"), index=False)
    if which in ("human", "both"):
        human().to_csv(os.path.join(HERE, "tip_distance_human.csv"), index=False)
    print("done")
