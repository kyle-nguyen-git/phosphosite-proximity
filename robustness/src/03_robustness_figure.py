"""Build the the robustness analysis robustness summary figure (PDF and PNG)."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parents[1]
RESULTS = HERE / "results"
INK = "#171717"
MUTED = "#626262"
GRID = "#dddddd"
BLUE = "#276FBF"
ORANGE = "#D95F02"
GREEN = "#1B9E77"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#999999",
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def forest(
    ax, frame, label_col, estimate_col, low_col, high_col, labels, color, reference,
    y_offset=0.0, set_labels=True, marker="o", label=None,
):
    plot = frame.set_index(label_col).loc[list(labels.keys())].copy()
    plot["display"] = [labels[index] for index in plot.index]
    y = np.arange(len(plot))[::-1].astype(float)
    estimate = plot[estimate_col].to_numpy(float)
    low = plot[low_col].to_numpy(float)
    high = plot[high_col].to_numpy(float)
    ax.axvline(reference, color="#999999", lw=1, ls=(0, (4, 3)))
    ax.errorbar(
        estimate, y + y_offset,
        xerr=np.vstack([estimate - low, high - estimate]),
        fmt=marker, color=color, ecolor=color, capsize=3, lw=1.5, ms=5.5,
        label=label,
    )
    if set_labels:
        ax.set_yticks(y)
        ax.set_yticklabels(plot["display"])
    ax.grid(axis="x", color=GRID, lw=0.6, alpha=0.7)
    return plot


def main() -> None:
    d = pd.read_csv(RESULTS / "robustness_primary_analysis.csv")
    confidence_all = pd.read_csv(RESULTS / "confidence_strata.csv")
    confidence = confidence_all.loc[
        confidence_all.cohort == "exclude_annotation_coincident"
    ].copy()
    confidence_inclusive = confidence_all.loc[
        confidence_all.cohort == "include_annotation_coincident"
    ].copy()
    cohorts = pd.read_csv(RESULTS / "cohort_sensitivity.csv")
    statistics = json.loads((RESULTS / "robustness_statistics.json").read_text())

    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
    fig.subplots_adjust(left=0.10, right=0.95, top=0.84, bottom=0.12, hspace=0.52, wspace=0.40)
    fig.suptitle(
        "Structural confidence and sensitivity analyses",
        x=0.10, y=0.955, ha="left", fontsize=16, fontweight="bold", color=INK,
    )
    fig.text(
        0.10, 0.905,
        f"Primary: {len(d)} S/T/Y-to-A substitutions across {d.acc.nunique()} yeast proteins · "
        "UniProt-annotated active and binding residues · AlphaFold DB monomer models",
        ha="left", fontsize=9.5, color=MUTED,
    )

    cluster_ci = statistics["primary_auc"]["protein_cluster_bootstrap"]

    # A: raw distance distributions.
    ax = axes[0, 0]
    for value, label, color in (
        (0, "Screen-negative", BLUE),
        (1, "Screen-positive", ORANGE),
    ):
        values = np.sort(d.loc[d.has_pheno.astype(int) == value, "dist_core_A"].to_numpy(float))
        ecdf = np.arange(1, len(values) + 1) / len(values)
        ax.step(values, ecdf, where="post", lw=2, color=color, label=f"{label} (n={len(values)})")
    ax.set_xlabel("Distance to nearest annotated active or binding residue (Å)")
    ax.set_ylabel("Empirical cumulative fraction")
    ax.set_xlim(-1, max(95, float(d.dist_core_A.max()) + 3))
    ax.set_ylim(0, 1.02)
    ax.grid(color=GRID, lw=0.6, alpha=0.7)
    ax.legend(frameon=False, fontsize=8.0, loc="lower right")
    ax.text(
        0.04, 0.94,
        f"AUC {cluster_ci['estimate']:.3f}\n95% CI {cluster_ci['ci_low']:.3f}–{cluster_ci['ci_high']:.3f}",
        transform=ax.transAxes, ha="left", va="top", color=INK, fontweight="bold",
    )
    ax.set_title("A   Observed distance distributions", loc="left", fontweight="bold", color=INK)

    # B: confidence-restricted primary AUC.
    ax = axes[0, 1]
    conf_index = confidence.set_index("stratum")
    conf_inclusive_index = confidence_inclusive.set_index("stratum")
    def conf_label(name, text):
        return (
            f"{text} (n={int(conf_index.loc[name, 'n_sites'])}/"
            f"{int(conf_inclusive_index.loc[name, 'n_sites'])})"
        )
    conf_labels = {
        "all": conf_label("all", "All substitutions"),
        "site_plddt_ge_50": conf_label("site_plddt_ge_50", "Site pLDDT ≥50"),
        "site_plddt_ge_70": conf_label("site_plddt_ge_70", "Site pLDDT ≥70"),
        "site_and_target_plddt_ge_70": conf_label("site_and_target_plddt_ge_70", "Both pLDDT ≥70"),
        "pair_pae_max_le_5": conf_label("pair_pae_max_le_5", "Maximum PAE ≤5 Å"),
        "pair_pae_max_le_10": conf_label("pair_pae_max_le_10", "Maximum PAE ≤10 Å"),
        "pair_pae_max_le_15": conf_label("pair_pae_max_le_15", "Maximum PAE ≤15 Å"),
        "high_confidence_joint": conf_label("high_confidence_joint", "Both pLDDT ≥70; max PAE ≤10"),
        "site_plddt_ge_90": conf_label("site_plddt_ge_90", "Site pLDDT ≥90"),
        "site_and_target_plddt_ge_90": conf_label("site_and_target_plddt_ge_90", "Both pLDDT ≥90"),
        "very_high_confidence_joint": conf_label("very_high_confidence_joint", "Both pLDDT ≥90; max PAE ≤10"),
    }
    forest(
        ax, confidence, "stratum", "estimate", "ci_low", "ci_high", conf_labels,
        BLUE, 0.5, y_offset=0.13, label="Primary cohort",
    )
    forest(
        ax, confidence_inclusive, "stratum", "estimate", "ci_low", "ci_high", conf_labels,
        ORANGE, 0.5, y_offset=-0.13, set_labels=False, marker="s",
        label="Inclusive sensitivity",
    )
    ax.set_xlim(0.05, 0.95)
    ax.set_xlabel("AUC for closer distance → screen-positive label (protein-cluster 95% CI)")
    ax.tick_params(axis="y", labelsize=7.8)
    ax.set_ylim(-0.6, 12.2)
    ax.legend(
        frameon=False, fontsize=7.6, ncol=2,
        loc="upper center", bbox_to_anchor=(0.5, 0.99),
    )
    ax.set_title("B   Structural-confidence sensitivity", loc="left", fontweight="bold", color=INK)

    # C: cohort-definition sensitivities.
    ax = axes[1, 0]
    cohort_index = cohorts.set_index("cohort")
    def cohort_label(name, text):
        return f"{text} (n={int(cohort_index.loc[name, 'n_sites'])})"
    cohort_labels = {
        "primary_excluding_annotation_coincident": cohort_label(
            "primary_excluding_annotation_coincident", "Primary: target-coincident sites excluded"
        ),
        "inclusive_exact_overlaps_at_0A": cohort_label(
            "inclusive_exact_overlaps_at_0A", "Inclusive sensitivity: coincident sites at 0 Å"
        ),
        "inclusive_exclude_hog1_pby107_position_resolution": cohort_label(
            "inclusive_exclude_hog1_pby107_position_resolution", "Inclusive, exclude resolved HOG1"
        ),
        "legacy_phase0_supp6_selected_excluding_overlaps": cohort_label(
            "legacy_phase0_supp6_selected_excluding_overlaps", "Legacy 158-site cohort"
        ),
        "primary_serine_threonine_only": cohort_label(
            "primary_serine_threonine_only", "Primary serine/threonine only"
        ),
        "primary_tyrosine_only": cohort_label(
            "primary_tyrosine_only", "Primary tyrosine only"
        ),
        "inclusive_exclude_prm15_s158_phosphointermediate": cohort_label(
            "inclusive_exclude_prm15_s158_phosphointermediate", "Inclusive, exclude PRM15"
        ),
    }
    forest(
        ax, cohorts, "cohort", "estimate", "ci_low", "ci_high",
        cohort_labels, GREEN, 0.5,
    )
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("AUC for closer distance → screen-positive label (protein-cluster 95% CI)")
    ax.tick_params(axis="y", labelsize=7.4)
    ax.set_title("C   Cohort and residue-class sensitivities", loc="left", fontweight="bold", color=INK)

    # D: pairwise confidence is strongly coupled to the measured distance.
    ax = axes[1, 1]
    scatter = ax.scatter(
        d["dist_core_A"], d["pae_pair_max"], c=d["plddt"], cmap="viridis",
        s=30, alpha=0.78, edgecolor="white", linewidth=0.4,
    )
    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlabel("Distance to nearest annotated active or binding residue (Å, symlog scale)")
    ax.set_ylabel("Maximum directional site–target PAE (Å)")
    ax.grid(color=GRID, lw=0.6, alpha=0.7)
    rho = statistics["confidence_correlations"]["spearman_distance_vs_pair_pae"]["rho"]
    ax.text(
        0.04, 0.94, f"Spearman ρ = {rho:.3f}", transform=ax.transAxes,
        ha="left", va="top", color=INK, fontweight="bold",
    )
    colorbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Site pLDDT", color=MUTED)
    ax.set_title("D   Distance is associated with relative-position uncertainty", loc="left", fontweight="bold", color=INK)

    wild = statistics["wild_cluster_lpm"]
    fig.text(
        0.10, 0.055,
        f"Primary AUC {cluster_ci['estimate']:.3f} [{cluster_ci['ci_low']:.3f}, {cluster_ci['ci_high']:.3f}]. "
        f"Adjusted linear-probability wild-cluster p={wild['wild_cluster_p']:.3f}. "
        "Three target-coincident substitutions are excluded from primary and retained at 0 Å only in the named sensitivity.",
        ha="left", fontsize=8.6, color=MUTED,
    )
    fig.text(
        0.10, 0.025,
        "All PAE strata use the maximum of the two directional site–target values. Analyses are exploratory; intervals resample proteins, and threshold families were examined after the outcome.",
        ha="left", fontsize=8.2, color="#777777",
    )

    for extension in ("png", "pdf"):
        for stem in ("robustness_robustness_summary", "robustness_two_arm_robustness_summary"):
            fig.savefig(
                RESULTS / f"{stem}.{extension}",
                dpi=300, bbox_inches="tight",
            )
    print("wrote robustness_robustness_summary.{png,pdf}")


if __name__ == "__main__":
    main()
