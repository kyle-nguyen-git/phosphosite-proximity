"""Split the human cohort by what the base editor actually did to the target residue.

Only threonine-to-alanine is a clean phospho-null. Serine-to-proline removes the phosphoacceptor
and disrupts the backbone, so it confounds exactly the structural claim under test. This script
classifies each guide's edit at its intended site and re-runs the analysis per class.
"""
import json
import os
import sys
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _paths  # noqa: E402  — resolves the vault and repository layouts

p05 = _paths.analysis_module()
DRAWS, SEED = 20000, 20260728

THREE = {"Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q", "Glu": "E",
         "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F",
         "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V", "Ter": "*"}
EDIT = re.compile(r"([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2})")


def edits_at_target(row):
    """Return (from, to, n_edits, n_silent) for the edit at the guide's intended target position."""
    target = str(row.get("Target site") or "").strip()
    m = re.match(r"([STY])(\d+)$", target)
    if not m:
        return None
    pos = int(m.group(2))
    for a3, p, b3 in EDIT.findall(str(row.get("Amino acid edits") or "")):
        if int(p) == pos:
            return (THREE.get(a3, "?"), THREE.get(b3, "?"), pos, row.get("Gene Symbol"))
    return None


def interval(y, score, groups, label):
    y = np.asarray(y, int)
    if y.sum() < 5 or (1 - y).sum() < 5:
        return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
                "auc": None, "note": "too few in one class to estimate"}
    r = p05.bootstrap_auc(y, np.asarray(score, float), groups=np.asarray(groups),
                          n=DRAWS, seed=SEED)
    touching = r["ci_low"] <= 0.0 or r["ci_high"] >= 1.0
    return {"label": label, "n": int(len(y)), "positive": int(y.sum()),
            "proteins": int(pd.Series(groups).nunique()),
            "auc": round(r["estimate"], 6),
            "ci_low": None if touching else round(r["ci_low"], 6),
            "ci_high": None if touching else round(r["ci_high"], 6),
            "draws_retained": int(r["draws"]), "draws_nominal": DRAWS}


def main():
    xl = os.path.join(HERE, "cache", "kennedy_supplement.xlsx")
    frames = []
    for sheet, editor in [("SuppTable 2 AG_exact_v1", "ABE8e"), ("SuppTable 2 CT_picks_v1", "BE4")]:
        g = pd.read_excel(xl, sheet_name=sheet)
        g["editor"] = editor
        frames.append(g)
    guides = pd.concat(frames, ignore_index=True)
    print(f"guides in Supplementary Table 2: {len(guides)}", flush=True)

    rows = []
    for r in guides.to_dict("records"):
        parsed = edits_at_target(r)
        if not parsed:
            continue
        frm, to, pos, gene = parsed
        rows.append({"gene": gene, "pos": pos, "frm": frm, "to": to,
                     "editor": r["editor"], "n_edits": r.get("# edits"),
                     "n_silent": r.get("#silent edits")})
    ed = pd.DataFrame(rows)
    print(f"guides with a parsable edit at their intended site: {len(ed)}", flush=True)

    for editor, g in ed.groupby("editor"):
        counts = (g.frm + "→" + g.to).value_counts()
        print(f"\n{editor}: substitution at the target residue, top 8 of {len(g)}")
        for k, v in counts.head(8).items():
            print("   %-8s %5d  %5.1f%%" % (k, v, 100 * v / len(g)))

    # one class per (gene, pos): a site is clean only if every guide hitting it agrees
    cls = (ed.assign(sub=ed.frm + "→" + ed.to)
             .groupby(["gene", "pos"])
             .agg(subs=("sub", lambda s: ";".join(sorted(set(s)))),
                  max_edits=("n_edits", "max"))
             .reset_index())

    d = pd.read_csv(os.path.join(HERE, "kennedy_analysis.csv"))
    d = d[d.min_dist_A.notna()].copy()
    d["y"] = ((d.p3 < 0.05) | (d.p4 < 0.05)).astype(int)
    d = d.merge(cls, on=["gene", "pos"], how="left")
    print(f"\ncohort sites matched to a guide class: {d.subs.notna().sum()} of {len(d)}", flush=True)

    results = [interval(d.y, -d.min_dist_A, d.acc, "all sites (reference)")]
    for label, mask in [
        ("threonine to alanine only (clean phospho-null)", d.subs == "T→A"),
        ("serine to proline only (backbone-disruptive)", d.subs == "S→P"),
        ("serine to glycine only", d.subs == "S→G"),
        ("any silent edit at the target site", d.subs.fillna("").str.contains("→")
            & d.subs.fillna("").apply(lambda s: any(a == b for a, b in
              [(x.split("→")[0], x.split("→")[-1]) for x in s.split(";") if "→" in x]))),
        ("single-edit guides only (no bystander)", d.max_edits == 1),
    ]:
        sub = d[mask.fillna(False)]
        if len(sub) >= 20:
            results.append(interval(sub.y, -sub.min_dist_A, sub.acc, label))
        else:
            results.append({"label": label, "n": int(len(sub)), "auc": None,
                            "note": "fewer than 20 sites"})

    print()
    print(pd.DataFrame(results).to_string(index=False))
    with open(os.path.join(HERE, "perturbation_arms.json"), "w") as fh:
        json.dump(results, fh, indent=2)
    d.to_csv(os.path.join(HERE, "kennedy_analysis_with_class.csv"), index=False)


if __name__ == "__main__":
    main()
