"""Panel 2C - AUC by declared confidence stratum, both cohorts.

Three things guard against reading a dose-response into the row order, which is nested
subsets rather than a trend (Results: the pattern is nonmonotonic, and NUMBERS.md §13
disallows implying otherwise):
  - marker area scales with n, so the 27- and 28-substitution strata are visibly the
    smallest points on the panel;
  - hairlines separate the four declared families {all}, {pLDDT}, {PAE}, {joint};
  - a second faint vertical sits at the primary all-substitutions estimate, so each
    stratum reads against its parent rather than against chance alone.
None of the three prints a statistic inside the data area.

Cohort keys are matched by exact equality. The previous substring match on "exclude"
worked only for this file's values; the sibling cohort_sensitivity.csv uses
"primary_excluding_..." and would have raised IndexError.
"""
import numpy as np
import pandas as pd

from _style import *

W, H = FOREST_W_MM, 62

PRI = "exclude_annotation_coincident"
INC = "include_annotation_coincident"

ORDER = ["all", "site_plddt_ge_50", "site_plddt_ge_70", "site_and_target_plddt_ge_70",
         "site_plddt_ge_90", "site_and_target_plddt_ge_90",
         "pair_pae_max_le_5", "pair_pae_max_le_10", "pair_pae_max_le_15",
         "high_confidence_joint", "very_high_confidence_joint"]
NICE = {"all": "All substitutions", "site_plddt_ge_50": "Site pLDDT ≥50",
        "site_plddt_ge_70": "Site pLDDT ≥70",
        "site_and_target_plddt_ge_70": "Site and target pLDDT ≥70",
        "site_plddt_ge_90": "Site pLDDT ≥90",
        "site_and_target_plddt_ge_90": "Site and target pLDDT ≥90",
        "pair_pae_max_le_5": "Max PAE ≤5 Å", "pair_pae_max_le_10": "Max PAE ≤10 Å",
        "pair_pae_max_le_15": "Max PAE ≤15 Å",
        "high_confidence_joint": "Both ≥70; PAE ≤10 Å",
        "very_high_confidence_joint": "Both ≥90; PAE ≤10 Å"}
# Family boundaries: draw a hairline ABOVE these strata.
BREAKS = {"site_plddt_ge_50", "pair_pae_max_le_5", "high_confidence_joint"}

def build():
    s = pd.read_csv(f"{P5}/confidence_strata.csv")
    arms = {c: s[s.cohort == c].set_index("stratum") for c in s.cohort.unique()}
    assert PRI in arms and INC in arms, "cohort keys changed: %s" % list(arms)
    # The caption claims EVERY declared stratum; a silent filter would make that false.
    assert set(arms[PRI].index) == set(ORDER), \
        "confidence strata changed: %s" % sorted(set(arms[PRI].index) ^ set(ORDER))

    n_pri = arms[PRI].loc[ORDER, "n_sites"].astype(int)
    n_inc = arms[INC].reindex(ORDER)["n_sites"]
    parent = float(arms[PRI].loc["all", "estimate"])

    # Marker area proportional to n, floored so the smallest stratum stays visible.
    area = 5.0 + 34.0 * (n_pri / n_pri.max())

    fig = panel(W, H)
    # x geometry comes from _style so panels C and D share one AUC scale. The left band
    # is sized to "Site and target pLDDT ≥90  (28/31)" at 6.8 pt = 48.9 mm on 177 mm.
    ax = fig.add_axes([FOREST_L, 0.155, FOREST_W, 0.765])
    ax.axvline(0.5, color=INK3, ls=(0, (3, 3)), lw=0.8, zorder=1)
    ax.axvline(parent, color=BLUE, ls=(0, (1, 2)), lw=0.8, alpha=0.55, zorder=1)

    for i, k in enumerate(ORDER):
        yy = len(ORDER) - 1 - i
        if k in BREAKS:
            ax.axhline(yy + 0.5, color="#e0e3e6", lw=0.5, zorder=0)
        for arm, col, off, mk in [(PRI, BLUE, 0.17, "o"), (INC, ORANGE, -0.17, "s")]:
            if k not in arms[arm].index:
                continue
            r = arms[arm].loc[k]
            ax.plot([r.ci_low, r.ci_high], [yy + off] * 2, color=col, lw=1.1, zorder=3,
                    solid_capstyle="butt")
            for x in (r.ci_low, r.ci_high):
                ax.plot([x, x], [yy + off - .11, yy + off + .11], color=col, lw=1.1,
                        zorder=3)
            ax.scatter([r.estimate], [yy + off], s=area[k], marker=mk, color=col,
                       edgecolors="white", linewidths=0.5, zorder=4)

    labels = ["%s  (%d/%d)" % (NICE[k], n_pri[k], int(n_inc[k]))
              if pd.notna(n_inc[k]) else "%s  (%d/–)" % (NICE[k], n_pri[k])
              for k in ORDER]
    ax.set_yticks(range(len(ORDER)))
    ax.set_yticklabels(labels[::-1])
    ax.set_ylim(-0.6, len(ORDER) - 0.4)
    ax.set_xlim(*FOREST_XLIM)
    ax.set_xticks(FOREST_XTICKS)
    ax.set_xlabel("AUC (protein-cluster 95% CI)")
    grid(ax, axis="x")
    ax.tick_params(axis="y", length=0)

    h = [plt.Line2D([], [], color=BLUE, marker="o", ms=3.4, lw=1.1, mec="white", mew=0.5),
         plt.Line2D([], [], color=ORANGE, marker="s", ms=3.4, lw=1.1, mec="white", mew=0.5),
         plt.Line2D([], [], color=BLUE, ls=(0, (1, 2)), lw=0.8, alpha=0.55)]
    ax.legend(h, ["Primary", "Inclusive 0 Å", "Primary all-substitutions estimate"],
              frameon=False, loc="lower left", bbox_to_anchor=(-0.004, 1.002), ncol=3,
              handlelength=1.6, handletextpad=0.5, columnspacing=2.0,
              fontsize=6.5, labelcolor=INK2, borderpad=0)
    save(fig, "p2c_confidence_forest")


if __name__ == "__main__":
    build()
