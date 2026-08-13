"""Panel 2A - empirical cumulative distance distributions by outcome, primary cohort.

Outcome is encoded INK2/GREEN, never BLUE/ORANGE: those two colours mean cohort arm in
1B and 2C, and reusing them here for a different variable made the reader relearn the
palette between adjacent panels.

The three inclusive-arm 0 Å substitutions appear in no distributional panel, so they are
marked with a rug at x = 0 rather than left invisible.
"""
import numpy as np
import pandas as pd

from _style import *

W, H = 87, 60


def build():
    d = pd.read_csv(f"{RES}/analysis_final.csv")
    n_primary = numbers_arms()["primary"][0]
    assert len(d) == n_primary, "panel 2A is the primary cohort: got %d rows" % len(d)
    y = d.has_pheno.astype(int).to_numpy()
    dist = d.min_dist_A.to_numpy(float)

    inc = pd.read_csv(f"{RES}/analysis_inclusive_sensitivity.csv")
    zero = inc.loc[inc.min_dist_A <= 0, "min_dist_A"].to_numpy(float)

    fig = panel(W, H)
    ax = fig.add_axes([0.130, 0.150, 0.850, 0.800])
    for m, col, ls, lab, lw in [
        (y == 0, INK2, "-", "Screen-negative (n=%d)" % (y == 0).sum(), 1.7),
        (y == 1, GREEN, (0, (3.5, 2)), "Screen-positive (n=%d)" % (y == 1).sum(), 1.6),
    ]:
        v = np.sort(dist[m])
        ax.step(np.r_[0, v], np.r_[0, np.arange(1, len(v) + 1) / len(v)],
                where="post", lw=lw, ls=ls, color=col, label=lab, zorder=3)

    ax.plot(zero, np.full(len(zero), 0.012), marker="|", ls="none", ms=4.5,
            mew=0.9, color=ORANGE, zorder=4, clip_on=False,
            label="Inclusive-only, 0 Å (n=%d)" % len(zero))

    ax.set_xlim(0, 95)          # same distance axis as panel B
    ax.set_ylim(0, 1.005)
    ax.set_xlabel("Distance to nearest annotated residue (Å)", labelpad=2)
    ax.set_ylabel("Empirical cumulative fraction")
    grid(ax)
    ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1.01, -0.01),
              handlelength=1.7, handletextpad=0.5, labelspacing=0.35,
              fontsize=6.2, labelcolor=INK2, borderpad=0)
    letter(fig, "A")
    save(fig, "p2a_ecdf")


if __name__ == "__main__":
    build()
