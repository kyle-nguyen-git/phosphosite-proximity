"""Panel 2D - all three declared sensitivity families, plus the SIFT comparator.

Displays every family NUMBERS.md §12 declares. The earlier panel plotted the cohort and
residue-class family and dropped the feature-definition family, which happens to contain
the highest non-tyrosine estimate in the paper (ACT_SITE only, 0.570) - selective display
of exactly the kind §13 warns against, in the direction favourable to the hypothesis.

The SIFT rows are the paper's calibration anchor: the same 152 substitutions score 0.606
for SIFT against 0.532 for distance, and the distance interval CONTAINS the SIFT point
estimate. Without them two figures of chance-straddling intervals push a reader toward the
demonstrated-null reading the paper explicitly disclaims. SIFT is post hoc, not
independent validation; the caption says so.

Rows are coloured by cohort arm using the same BLUE/ORANGE the rest of the paper uses, so
the primary/inclusive distinction stays legible here as well as in panel C.

The tyrosine row is taken from residue_class_sensitivity.csv, not cohort_sensitivity.csv.
Both describe the same 16-site subset and differ only by Monte Carlo draw
(0.2719 against 0.2667 at the lower bound); NUMBERS.md §12 makes the residue-class file
authoritative for reader-facing output, and a published figure is reader-facing.
"""
import numpy as np
import pandas as pd

from _style import *

W, H = FOREST_W_MM, 76

# Each family gets a blank slot above it; the family name sits in that gap. Writing the
# name alongside the first row of the family put it on the same baseline as the row label
# above and the two overprinted.
GAP = 1.0

COHORT = [
    ("primary_excluding_annotation_coincident", "Primary", BLUE),
    ("inclusive_exact_overlaps_at_0A", "Inclusive, 0 Å retained", ORANGE),
    ("inclusive_exclude_hog1_pby107_position_resolution", "Inclusive, less HOG1", ORANGE),
    ("inclusive_exclude_prm15_s158_phosphointermediate", "Inclusive, less PRM15", ORANGE),
    ("legacy_phase0_supp6_selected_excluding_overlaps", "Legacy Supp-6 cohort", BLUE),
    ("primary_serine_threonine_only", "Primary, Ser/Thr", BLUE),
]
FEATURE = [
    ("dist_act_site_A", "Active site only", BLUE),
    ("dist_binding_A", "Binding only", BLUE),
    ("dist_core_plus_site_A", "Core plus site", BLUE),
    ("dist_all_with_dna_bind_A", "Core plus DNA-binding", BLUE),
]


def rows():
    """(label, n, estimate, lo, hi, colour, marker) top to bottom, plus break indices."""
    co = pd.read_csv(f"{P5}/cohort_sensitivity.csv").set_index("cohort")
    rc = pd.read_csv(f"{P5}/residue_class_sensitivity.csv").set_index("residue")
    fe = pd.read_csv(f"{P5}/feature_definition_sensitivity.csv").set_index(
        "distance_definition")
    sf = pd.read_csv(f"{P5}/sift_comparator_sensitivity.csv").set_index("cohort")

    out = []
    for key, lab, col in COHORT:
        assert key in co.index, "missing cohort sensitivity row: %s" % key
        r = co.loc[key]
        out.append((lab, int(r.n_sites), r.estimate, r.ci_low, r.ci_high, col, "o"))
    y = rc.loc["Y"]
    out.append(("Primary, Tyr", int(y.n_sites), y.estimate, y.ci_low, y.ci_high,
                BLUE, "o"))

    for key, lab, col in FEATURE:
        assert key in fe.index, "missing feature-definition row: %s" % key
        r = fe.loc[key]
        out.append((lab, int(r.n_sites), r.estimate, r.ci_low, r.ci_high, col, "o"))

    s = sf.loc["exclude_annotation_coincident"]
    out.append(("SIFT", int(s.n_sites), s.sift_auc, s.sift_ci_low, s.sift_ci_high,
                PURPLE, "D"))
    out.append(("Distance, same support", int(s.n_sites), s.distance_auc,
                s.distance_ci_low, s.distance_ci_high, BLUE, "D"))

    starts = [(0, "Cohort and residue class"),
              (len(COHORT) + 1, "Distance-feature definition"),
              (len(COHORT) + 1 + len(FEATURE), "Post hoc comparator, common support")]
    return out, starts


def build():
    data, starts = rows()
    parent = data[0][2]
    n = len(data)
    heads = dict(starts)

    # Lay rows out top-down, inserting a blank slot wherever a family begins.
    ypos, y, head_y = [], 0.0, {}
    for i in range(n):
        if i in heads:
            y += GAP
            head_y[i] = y - GAP / 2
        ypos.append(y)
        y += 1.0
    span = y - 1.0
    ypos = [span - v for v in ypos]                      # flip so row 0 sits at the top
    head_y = {i: span - v for i, v in head_y.items()}

    fig = panel(W, H)
    ax = fig.add_axes([FOREST_L, 0.130, FOREST_W, 0.800])
    ax.axvline(0.5, color=INK3, ls=(0, (3, 3)), lw=0.8, zorder=1)
    ax.axvline(parent, color=BLUE, ls=(0, (1, 2)), lw=0.8, alpha=0.55, zorder=1)

    for i, (lab, nn, est, lo, hi, col, mk) in enumerate(data):
        yy = ypos[i]
        if i in heads and i > 0:
            ax.axhline(yy + GAP / 2, color="#e0e3e6", lw=0.5, zorder=0)
        ax.plot([lo, hi], [yy, yy], color=col, lw=1.2, zorder=3, solid_capstyle="butt")
        for x in (lo, hi):
            ax.plot([x, x], [yy - .13, yy + .13], color=col, lw=1.2, zorder=3)
        ax.plot([est], [yy], mk, ms=3.6, color=col, mec="white", mew=0.5, zorder=4)

    ax.set_yticks(ypos)
    ax.set_yticklabels(["%s  (%d)" % (l, nn) for l, nn, *_ in data], fontsize=6.5)
    ax.set_ylim(-0.7, span + 0.7)
    ax.set_xlim(*FOREST_XLIM)
    ax.set_xticks(FOREST_XTICKS)
    ax.set_xlabel("AUC (protein-cluster 95% CI)")
    grid(ax, axis="x")
    ax.tick_params(axis="y", length=0)

    # Family names sit in the blank slot, in the left band, never over a row label.
    for i, name in starts:
        ax.text(-0.012, head_y[i], name, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=6.2, color=INK3, style="italic")

    h = [plt.Line2D([], [], color=BLUE, marker="o", ms=3.6, lw=1.2, mec="white", mew=0.5),
         plt.Line2D([], [], color=ORANGE, marker="o", ms=3.6, lw=1.2, mec="white", mew=0.5),
         plt.Line2D([], [], color=PURPLE, marker="D", ms=3.6, lw=1.2, mec="white", mew=0.5)]
    ax.legend(h, ["Primary arm", "Inclusive arm", "SIFT (post hoc)"],
              frameon=False, loc="lower left", bbox_to_anchor=(-0.004, 1.002), ncol=3,
              handlelength=1.6, handletextpad=0.5, columnspacing=2.0,
              fontsize=6.5, labelcolor=INK2, borderpad=0)
    letter(fig, "D")
    save(fig, "p2d_sensitivity_forest")


if __name__ == "__main__":
    build()
