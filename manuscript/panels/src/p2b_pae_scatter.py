"""Panel 2B - pairwise PAE against measured distance, coloured by site pLDDT.

Linear x-axis. The earlier symlog(linthresh=10) left the region the paper actually uses -
the 5, 8, 10 and 15 Å descriptive cutoffs, where 30 of 163 substitutions sit - with no
tick, no label and no gridline, and put its only two labelled ticks at 10^1 and 10^2, the
second beyond the data maximum. Panel A plots the same variable linearly; both now agree.

Not rasterized: 163 markers do not need it, and it was the only raster element in either
figure.
"""
import pandas as pd

from _style import *

W, H = 87, 60


def build():
    d = pd.read_csv(f"{P5}/robustness_analysis.csv")
    # Fail loudly rather than silently plotting all 166 inclusive-arm rows under a
    # legend and caption that both say "primary cohort".
    d = d[d.cohort_primary_exclude_annotation_coincident.astype(bool)]
    n_primary = numbers_arms()["primary"][0]
    assert len(d) == n_primary, "panel 2B is the primary cohort: got %d rows" % len(d)
    assert d[["min_dist_A", "pae_pair_max", "plddt"]].notna().all().all()

    fig = panel(W, H)
    ax = fig.add_axes([0.115, 0.150, 0.725, 0.800])
    s = ax.scatter(d.min_dist_A, d.pae_pair_max, c=d.plddt, cmap="viridis",
                   vmin=d.plddt.min(), vmax=d.plddt.max(),
                   s=11, lw=0.25, edgecolors=INK2, zorder=3)
    ax.set_xlim(0, 95)
    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_xlabel("Distance to nearest annotated residue (Å)", labelpad=2)
    ax.set_ylabel("Max directional site–target PAE (Å)", labelpad=2)
    grid(ax)

    cax = fig.add_axes([0.872, 0.150, 0.028, 0.800])
    cb = fig.colorbar(s, cax=cax)
    cb.outline.set_linewidth(0.5)
    cb.outline.set_edgecolor(INK3)
    cb.ax.tick_params(width=0.5, length=2, labelsize=6.8, color=INK2)
    cb.set_label("Site pLDDT", fontsize=7.5, color=INK2, labelpad=3)
    letter(fig, "B")
    save(fig, "p2b_pae_scatter")


if __name__ == "__main__":
    build()
