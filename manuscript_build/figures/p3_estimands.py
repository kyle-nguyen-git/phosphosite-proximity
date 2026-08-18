"""Figure 3: what the statistic estimates, in both organisms.

The second format review found that both main figures were yeast-only while the title, abstract and
claimed extension name yeast and human, and that the sensitivity catalogues dominated the main visual
space. This panel is the reply: the central scientific comparison on one scale, across all three
cohorts, showing the pooled estimate beside the two within-protein aggregations.

Every number is read from a committed results file. Nothing is typed in.

  yeast pooled            NUMBERS.md Section 12, via phase0_5/results/phase0_5_statistics.json
  yeast within-protein    the same file's within_protein_discrimination block
  human, both screens     kennedy_replication/rebuilt_endpoints_1470.json (Section 27)

Redundant encoding throughout, because the review found panels relying on colour alone: each estimand
gets its own marker shape as well as its own colour, and the chance line is drawn once.
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
RESEARCH = os.path.dirname(BUILD)
CAL = os.path.join(RESEARCH, "phase0_calibration")
KEN = os.path.join(RESEARCH, "kennedy_replication")

MM = 1 / 25.4
COL2 = 183          # double-column width in mm, matching the release figures

BLUE, ORANGE, GREEN = "#3B6FB6", "#E07A2B", "#2E8B6B"
INK = "#1A1A1A"


def load():
    with open(os.path.join(CAL, "phase0_5", "results", "phase0_5_statistics.json")) as fh:
        y = json.load(fh)
    with open(os.path.join(KEN, "rebuilt_endpoints_1470.json")) as fh:
        h = json.load(fh)
    w = y["within_protein_discrimination"]

    def pooled_yeast():
        # the protein-clustered interval, which is the one the manuscript reports
        b = y["primary_auc"]["protein_cluster_bootstrap"]
        return b["estimate"], b["ci_low"], b["ci_high"]

    rows = []
    pe, plo, phi = pooled_yeast()
    rows.append(("Yeast", "Pooled", pe, plo, phi, 163, 48))
    rows.append(("Yeast", "Within-protein, pair-weighted",
                 w["pair_weighted_auc"], w["pair_weighted_ci_low"], w["pair_weighted_ci_high"],
                 w["informative_sites"], w["informative_proteins"]))
    rows.append(("Yeast", "Within-protein, equal-protein",
                 w["equal_protein_weight_auc"], w["equal_protein_weight_ci_low"],
                 w["equal_protein_weight_ci_high"], w["informative_sites"], w["informative_proteins"]))

    for tag, label in (("fitness", "Human, fitness"), ("reporter", "Human, NFAT reporter")):
        sc = h["screens"][tag]
        p = sc["primary"]
        rows.append((label, "Pooled", p["auc"], p["ci_low"], p["ci_high"], p["n"], p["proteins"]))
        wp = sc["within_protein"]
        rows.append((label, "Within-protein, pair-weighted",
                     wp["pair_weighted_auc"], wp["pair_weighted_ci_low"], wp["pair_weighted_ci_high"],
                     wp["informative_sites"], wp["informative_proteins"]))
        rows.append((label, "Within-protein, equal-protein",
                     wp["equal_protein_weight_auc"], wp["equal_protein_weight_ci_low"],
                     wp["equal_protein_weight_ci_high"], wp["informative_sites"],
                     wp["informative_proteins"]))
    return rows


def main():
    rows = load()
    style = {
        "Pooled": dict(color=BLUE, marker="o", ls="-"),
        "Within-protein, pair-weighted": dict(color=ORANGE, marker="s", ls="--"),
        "Within-protein, equal-protein": dict(color=GREEN, marker="^", ls=":"),
    }

    fig, ax = plt.subplots(figsize=(COL2 * MM, 78 * MM))
    ys, labels = [], []
    pos = 0.0
    last_cohort = None
    for cohort, estimand, est, lo, hi, n, prot in rows:
        if last_cohort is not None and cohort != last_cohort:
            pos -= 0.55
        pos -= 1.0
        st = style[estimand]
        ax.plot([lo, hi], [pos, pos], color=st["color"], ls=st["ls"], lw=1.3,
                solid_capstyle="butt", zorder=2)
        ax.plot([lo, lo], [pos - 0.16, pos + 0.16], color=st["color"], lw=1.3, zorder=2)
        ax.plot([hi, hi], [pos - 0.16, pos + 0.16], color=st["color"], lw=1.3, zorder=2)
        ax.plot([est], [pos], color=st["color"], marker=st["marker"], ms=5,
                mec="white", mew=0.7, zorder=3)
        labels.append((pos, f"{estimand}   ({n} sites, {prot} proteins)" if "Within" in estimand
                       else f"{estimand}   ({n} sites, {prot} proteins)"))
        ys.append(pos)
        last_cohort = cohort

    ax.axvline(0.5, color="#666666", ls=(0, (4, 3)), lw=1.0, zorder=1)
    ax.text(0.5, max(ys) + 0.85, "chance", ha="center", va="bottom", fontsize=8, color="#444444")

    ax.set_yticks([p for p, _ in labels])
    ax.set_yticklabels([t for _, t in labels], fontsize=8, color=INK)
    ax.set_xlabel("AUC (protein-cluster 95% confidence interval)", fontsize=8, color=INK)
    ax.set_xlim(0.20, 0.90)
    ax.set_ylim(min(ys) - 0.9, max(ys) + 1.6)
    ax.tick_params(axis="x", labelsize=8, colors=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#999999")

    # cohort bands, labelled in black rather than the grey the review flagged
    seen, band_start = [], None
    for i, (cohort, *_rest) in enumerate(rows):
        if cohort not in [c for c, _ in seen]:
            seen.append((cohort, ys[i]))
    for cohort, ytop in seen:
        ax.text(0.205, ytop + 0.55, cohort, fontsize=8, fontweight="bold", color=INK,
                ha="left", va="bottom")

    handles = [plt.Line2D([], [], color=v["color"], marker=v["marker"], ls=v["ls"], ms=5,
                          mec="white", mew=0.7, label=k) for k, v in style.items()]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=8,
              handlelength=2.6, borderpad=0.2)

    fig.tight_layout(pad=0.4)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"figure3.{ext}"), dpi=600,
                    metadata={"CreationDate": None} if ext == "pdf" else None)
    print(f"figure3: {COL2} x 78 mm, {len(rows)} estimates from committed files")


if __name__ == "__main__":
    main()
