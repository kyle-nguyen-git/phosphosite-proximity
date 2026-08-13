"""Panel 1B - ROC for both cohorts, with a protein-clustered bootstrap band.

The band is a data element, not a printed statistic, so design rule 2 holds. It exists
because the paper's claim is "weak AND imprecise": without it the ROC shows weak and
shows imprecise nowhere, and a reader who looks only at Figure 1 takes away a null.

Resampling is over PROTEINS, matching src/03_analysis.py - sites are nested within
proteins, and resampling sites gives intervals roughly 19% too narrow.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve

from _style import *

W, H = 72, 66
N_BAND, SEED = numbers_roc_band()          # declared in NUMBERS.md section 17
FPR_GRID = np.linspace(0, 1, 201)


def band(d, seed=SEED, n=N_BAND):
    """Percentile envelope of protein-clustered bootstrap ROC curves.

    Pointwise over the false-positive grid, so it is not the AUC interval and is wider
    than it. Resamples that draw one outcome class are discarded, so the effective draw
    count is at most n; NUMBERS.md section 17 declares both the count and that rule.
    """
    rng = np.random.default_rng(seed)
    accs = d.acc.unique()
    by = {a: g for a, g in d.groupby("acc")}
    keep = []
    for _ in range(n):
        s = pd.concat([by[a] for a in rng.choice(accs, len(accs), replace=True)])
        y = s.has_pheno.astype(int).to_numpy()
        if y.min() == y.max():
            continue
        f, t, _ = roc_curve(y, -s.min_dist_A.to_numpy(float))
        keep.append(np.interp(FPR_GRID, f, t))
    k = np.vstack(keep)
    return np.percentile(k, 2.5, axis=0), np.percentile(k, 97.5, axis=0)


def build():
    pri = pd.read_csv(f"{RES}/analysis_final.csv")
    inc = pd.read_csv(f"{RES}/analysis_inclusive_sensitivity.csv")
    arms = numbers_arms()
    assert (len(pri), len(inc)) == (arms["primary"][0], arms["inclusive"][0])

    fig = panel(W, H)
    ax = fig.add_axes([0.160, 0.140, 0.815, 0.815])
    ax.plot([0, 1], [0, 1], ls=(0, (3, 3)), lw=0.9, color=INK3, zorder=1)

    lo, hi = band(pri)
    ax.fill_between(FPR_GRID, lo, hi, color=BLUE, alpha=0.15, lw=0, zorder=2,
                    label="95% band, proteins resampled")

    for d, col, ls, lab, lw in [
        (inc, ORANGE, (0, (3.5, 2)), "Inclusive 0 Å sensitivity", 1.5),
        (pri, BLUE, "-", "Primary cohort", 1.9),
    ]:
        y = d.has_pheno.astype(int).to_numpy()
        f, t, _ = roc_curve(y, -d.min_dist_A.to_numpy(float))
        ax.plot(f, t, lw=lw, ls=ls, color=col, label=lab, zorder=4,
                solid_capstyle="round")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([0, .25, .5, .75, 1])
    ax.set_yticks([0, .25, .5, .75, 1])
    ax.set_xlabel("False-positive rate")
    ax.set_ylabel("True-positive rate")
    grid(ax)

    # Legend in the lower-right wedge, which both curves and the band stay out of.
    # The diagonal is identified in the caption rather than labelled on the plot,
    # matching how the forests leave their AUC 0.5 reference line unlabelled.
    h, l = ax.get_legend_handles_labels()
    order = [l.index("Primary cohort"),
             l.index("95% band, proteins resampled"),
             l.index("Inclusive 0 Å sensitivity")]
    ax.legend([h[i] for i in order], [l[i] for i in order],
              frameon=False, loc="lower right", bbox_to_anchor=(1.010, -0.018),
              handlelength=1.7, handletextpad=0.5, labelspacing=0.35,
              fontsize=6.2, labelcolor=INK2, borderpad=0)
    letter(fig, "B")
    save(fig, "p1b_roc")


if __name__ == "__main__":
    build()
