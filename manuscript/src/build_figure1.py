"""Build Figure 1: cohort reconstruction, estimand, and primary ROC."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Ellipse
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "manuscript"
INK = "#171717"
MUTED = "#666666"
GRID = "#dedede"
BLUE = "#276FBF"
ORANGE = "#D95F02"
GREEN = "#1B9E77"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#999999",
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
})


def roc_curve(y_true, y_score):
    """Return empirical ROC coordinates without a plotting-time sklearn dependency."""
    y = np.asarray(y_true, dtype=int)
    score = np.asarray(y_score, dtype=float)
    order = np.argsort(-score, kind="mergesort")
    y = y[order]
    score = score[order]
    threshold_indices = np.r_[np.where(np.diff(score))[0], y.size - 1]
    true_positives = np.cumsum(y)[threshold_indices]
    false_positives = 1 + threshold_indices - true_positives
    true_positives = np.r_[0, true_positives]
    false_positives = np.r_[0, false_positives]
    thresholds = np.r_[np.inf, score[threshold_indices]]
    return (
        false_positives / false_positives[-1],
        true_positives / true_positives[-1],
        thresholds,
    )


def rounded_box(ax, xy, width, height, text, face, edge, fontsize=8.3):
    patch = FancyBboxPatch(
        xy, width, height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.2, edgecolor=edge, facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2, xy[1] + height / 2, text,
        ha="center", va="center", fontsize=fontsize, color=INK, linespacing=1.25,
    )


def main() -> None:
    disposition = pd.read_csv(ROOT / "results" / "cohort_disposition.csv")
    d = pd.read_csv(ROOT / "phase0_5" / "results" / "phase0_5_primary_analysis.csv")
    inclusive = pd.read_csv(
        ROOT / "phase0_5" / "results" / "phase0_5_inclusive_sensitivity_analysis.csv"
    )
    stats = json.loads((ROOT / "phase0_5" / "results" / "phase0_5_statistics.json").read_text())
    primary = stats["primary_auc"]["protein_cluster_bootstrap"]
    sensitivity = stats["inclusive_sensitivity_auc"]["protein_cluster_bootstrap"]

    if not (
        len(disposition) == 497
        and len(d) == 163
        and int(d.has_pheno.sum()) == 79
        and len(inclusive) == 166
        and int(inclusive.has_pheno.sum()) == 82
    ):
        raise RuntimeError("Figure 1 inputs do not match the declared two-arm cohorts")

    fig = plt.figure(figsize=(12, 6.9), facecolor="white")
    grid = fig.add_gridspec(1, 3, width_ratios=[1.06, 1.02, 1.08])
    fig.subplots_adjust(left=0.055, right=0.97, top=0.82, bottom=0.14, wspace=0.31)
    fig.suptitle(
        "Cohort reconstruction and primary structural-proximity analysis",
        x=0.055, y=0.955, ha="left", fontsize=17, fontweight="bold", color=INK,
    )
    fig.text(
        0.055, 0.905,
        "Public yeast phosphosite-to-alanine growth screen · reviewed UniProt annotations · AlphaFold DB monomer models",
        ha="left", fontsize=10, color=MUTED,
    )

    # A: cohort flow.
    ax = fig.add_subplot(grid[0, 0])
    ax.set_title("A   Cohort reconstruction", loc="left", fontweight="bold", fontsize=11, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    boxes = [
        (0.86, "497 point-mutant records\n490 source substitutions · 116 genes"),
        (0.69, "487 sequence-matched records\nHOG1 T174 resolved · 10 mismatches"),
        (0.52, "465 sequence-matched records with raw profiles\n22 lacked a raw screen profile"),
        (0.35, "427 records after source QC\n18 WGS + 20 scar-correlation flags excluded"),
        (0.18, "423 unique eligible substitutions\n107 proteins"),
        (0.01, "Primary: 163 substitutions · 48 proteins · 79 screen-positive\nInclusive: 166 substitutions · 50 proteins · 82 screen-positive"),
    ]
    for index, (y, label) in enumerate(boxes):
        final = index == len(boxes) - 1
        rounded_box(
            ax, (0.04 if final else 0.06, y), 0.92 if final else 0.88, 0.115, label,
            "#EAF4F1" if final else "#F4F6F8",
            GREEN if final else "#B9C2CC",
            fontsize=8.0 if not final else 7.0,
        )
        if index < len(boxes) - 1:
            ax.add_patch(FancyArrowPatch(
                (0.50, y - 0.003), (0.50, boxes[index + 1][0] + 0.119),
                arrowstyle="-|>", mutation_scale=10, color="#8D98A4", lw=1.0,
            ))

    # B: declared estimand.
    ax = fig.add_subplot(grid[0, 1])
    ax.set_title("B   Analysis definition", loc="left", fontweight="bold", fontsize=11, color=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Ellipse((0.50, 0.61), 0.83, 0.45, angle=-8, facecolor="#F1F3F5", edgecolor="#B8C0C7", lw=1.2))
    ax.plot(
        [0.14, 0.24, 0.33, 0.43, 0.55, 0.67, 0.80, 0.86],
        [0.62, 0.72, 0.56, 0.66, 0.52, 0.68, 0.58, 0.65],
        color="#929CA5", lw=5, alpha=0.55, solid_capstyle="round",
    )
    site = (0.31, 0.57)
    target = (0.71, 0.65)
    ax.add_patch(Circle(site, 0.035, color=ORANGE, ec="white", lw=1.2, zorder=5))
    ax.add_patch(Circle(target, 0.035, color=BLUE, ec="white", lw=1.2, zorder=5))
    ax.text(site[0], site[1] - 0.085, "S/T/Y→A site", ha="center", color=ORANGE, fontsize=8.3, fontweight="bold")
    ax.text(target[0], target[1] + 0.075, "UniProt-annotated active\nor binding residue", ha="center", color=BLUE, fontsize=8.3, fontweight="bold")
    ax.add_patch(FancyArrowPatch(site, target, arrowstyle="<->", mutation_scale=11, color=INK, lw=1.4))
    ax.text(0.51, 0.67, "minimum heavy-atom\ndistance, Å", ha="center", va="bottom", fontsize=8.2, color=INK)
    rounded_box(
        ax, (0.10, 0.18), 0.80, 0.12,
        "Predictor: shorter distance\nOutcome: direction-agnostic screen-positive label",
        "#FFF4EC", "#E6AA79", fontsize=8.5,
    )
    ax.add_patch(Circle((0.17, 0.08), 0.025, color="white", ec=ORANGE, lw=2))
    ax.text(
        0.22, 0.08,
        "Three target-coincident substitutions excluded from primary;\nretained at 0 Å in sensitivity",
        va="center", fontsize=7.4, color=MUTED, linespacing=1.15,
    )
    ax.text(
        0.50, 0.37,
        "One coordinate feature; no ligand, complex,\nphosphorylated state, or conformational ensemble",
        ha="center", va="center", fontsize=8.0, color=MUTED, linespacing=1.35,
    )

    # C: primary ROC and sparse 5 Å regime.
    ax = fig.add_subplot(grid[0, 2])
    y = d.has_pheno.astype(int).to_numpy()
    distance = d.dist_core_A.to_numpy(float)
    fpr, tpr, _ = roc_curve(y, -distance)
    inclusive_y = inclusive.has_pheno.astype(int).to_numpy()
    inclusive_distance = inclusive.dist_core_A.to_numpy(float)
    sensitivity_fpr, sensitivity_tpr, _ = roc_curve(inclusive_y, -inclusive_distance)
    ax.plot([0, 1], [0, 1], color="#999999", lw=1.2, ls=(0, (4, 3)))
    ax.plot(fpr, tpr, color=BLUE, lw=2.4, label="Primary cohort")
    ax.plot(
        sensitivity_fpr, sensitivity_tpr, color=ORANGE, lw=1.8,
        ls=(0, (4, 2)), label="Inclusive 0 Å sensitivity",
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("False-positive rate")
    ax.set_ylabel("True-positive rate")
    ax.grid(color=GRID, lw=0.6, alpha=0.8)
    ax.set_title("C   Primary discrimination", loc="left", fontweight="bold", fontsize=11, color=INK)
    ax.text(
        0.05, 0.94,
        f"AUC {primary['estimate']:.3f}\nprotein-cluster 95% CI\n{primary['ci_low']:.3f}–{primary['ci_high']:.3f}",
        transform=ax.transAxes, va="top", ha="left", fontsize=9.7, color=INK, fontweight="bold",
    )
    ax.text(
        0.05, 0.72,
        f"Inclusive sensitivity\nAUC {sensitivity['estimate']:.3f}\n"
        f"{sensitivity['ci_low']:.3f}–{sensitivity['ci_high']:.3f}",
        transform=ax.transAxes, va="top", ha="left", fontsize=8.2, color=ORANGE,
    )
    near = distance <= 5
    ax.text(
        0.95, 0.08,
        f"≤5 Å: {int(near.sum())} substitutions\n{int(y[near].sum())}/{int(near.sum())} positive ({y[near].mean():.1%})\n"
        f">5 Å: {int(y[~near].sum())}/{int((~near).sum())} positive ({y[~near].mean():.1%})",
        transform=ax.transAxes, va="bottom", ha="right", fontsize=8.1, color=MUTED,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#D1D5D9", "alpha": 0.95},
    )
    ax.legend(frameon=False, fontsize=7.7, loc="upper right")

    fig.text(
        0.055, 0.055,
        "Data-source roles were fixed during reviewer-driven reconstruction: Supplement 1 constructs; Supplement 3 outcome ledger; "
        "Supplement 8 QC; Supplement 6 annotations only. Counts distinguish strain records from unique substitutions.",
        ha="left", fontsize=8.4, color=MUTED,
    )
    for extension in ("png", "pdf"):
        fig.savefig(OUT / f"figure1_cohort_estimand_primary.{extension}", dpi=300, bbox_inches="tight")
    print("wrote manuscript/figure1_cohort_estimand_primary.{png,pdf}")


if __name__ == "__main__":
    main()
