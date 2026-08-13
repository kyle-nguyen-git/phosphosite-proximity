"""Panel 1A - cohort reconstruction ladder.

Every count is derived at build time from results/cohort_disposition.csv and the two
committed cohort files, then asserted against manuscript Table 1. Nothing is typed by
hand, so a change upstream fails the build instead of silently disagreeing with the table.

Counting unit note: stage 1 counts SOURCE-coordinate substitutions and every later stage
counts RESOLVED-coordinate substitutions, matching Table 1. The two differ by exactly one
- PBY107's HOG1 T178 resolves onto T174, which PBY131 already occupies - which is why 490
becomes 479 rather than 480 across the mismatch stage.
"""
import pandas as pd
from matplotlib.patches import FancyBboxPatch

from _style import *

W, H = 105, 66

# (terminal-disposition substring removed at this stage, wording for the note line)
DROPS = [
    ("mismatch", "unresolved mismatches"),
    ("no raw screening profile", "lacked a Supp. Data 3 profile"),
    ("WGS", "WGS quality flags"),
    ("scar-control", "scar-correlation entries"),
]
TITLES = [
    "Sequence matched after PBY107 resolution",
    "Sequence matched with a condition-level profile",
    "After whole-genome-sequencing exclusion",
    "After scar-correlation exclusion",
]
# Table 1 / NUMBERS.md section 4: (strain records, unique substitutions, proteins) per
# stage. Parsed from the authority rather than typed here; the last row is the
# core-eligible stage, which the ladder reaches after the four drops.


def ladder():
    c = pd.read_csv(os.path.join(RES, "cohort_disposition.csv"))
    rows = [("%d point-mutant strain records" % len(c),
             "%d source-coordinate substitutions · %d UniProt accessions"
             % (c.drop_duplicates(["acc", "source_pos"]).shape[0], c.acc.nunique()))]
    got = [(len(c), c.drop_duplicates(["acc", "source_pos"]).shape[0], c.acc.nunique())]
    cur = c
    for (key, note), title in zip(DROPS, TITLES):
        n_out = int(cur.cohort_disposition.str.contains(key).sum())
        cur = cur[~cur.cohort_disposition.str.contains(key)]
        subs = cur.drop_duplicates(["acc", "pos"]).shape[0]
        rows.append(("%s  ·  %d records" % (title, len(cur)),
                     "%d substitutions · %d proteins · %d %s excluded"
                     % (subs, cur.acc.nunique(), n_out, note)))
        got.append((len(cur), subs, cur.acc.nunique()))
    cascade = numbers_cascade()
    assert got == cascade[:5], \
        "ladder disagrees with NUMBERS.md section 4: %s vs %s" % (got, cascade[:5])

    inc = pd.read_csv(os.path.join(RES, "analysis_inclusive_sensitivity.csv"))
    fin = pd.read_csv(os.path.join(RES, "analysis_final.csv"))
    arms = numbers_arms()
    assert (len(inc), inc.acc.nunique(), int(inc.y.sum())) == arms["inclusive"]
    assert (len(fin), fin.acc.nunique(), int(fin.y.sum())) == arms["primary"]
    # The core-eligible stage was previously rendered unguarded.
    assert (int(inc.source_replicate_strain_count.sum()), len(inc), inc.acc.nunique()) \
        == cascade[5], "core-eligible stage disagrees with NUMBERS.md section 4"
    rows.append(("Core annotation and structure eligible  ·  %d records"
                 % int(inc.source_replicate_strain_count.sum()),
                 "%d substitutions · %d proteins · replicate strains aggregated"
                 % (len(inc), inc.acc.nunique())))
    final = ("Primary  %d substitutions · %d proteins · %d screen-positive"
             % (len(fin), fin.acc.nunique(), int(fin.y.sum())),
             "Inclusive 0 Å sensitivity  %d · %d · %d"
             % (len(inc), inc.acc.nunique(), int(inc.y.sum())))
    return rows, final


def build():
    rows, final = ladder()
    fig = panel(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fits = []
    n = len(rows) + 1
    top, bot = 0.935, 0.030
    slot = (top - bot) / n
    bh = slot * 0.72
    for i, (a, b) in enumerate(rows):
        y = top - (i + 1) * slot + (slot - bh) / 2
        bx = ax.add_patch(FancyBboxPatch((0.020, y), 0.960, bh,
                                         boxstyle="round,pad=0,rounding_size=0.010",
                                         fc="#f4f6f7", ec="#d6dade", lw=0.6, zorder=2))
        fits.append((ax.text(0.5, y + bh * 0.66, a, ha="center", va="center",
                             fontsize=6.9, color=INK, zorder=3), bx))
        fits.append((ax.text(0.5, y + bh * 0.26, b, ha="center", va="center",
                             fontsize=6.5, color=INK3, zorder=3), bx))
        ax.annotate("", xy=(0.5, y - (slot - bh) * 0.62), xytext=(0.5, y),
                    arrowprops=dict(arrowstyle="-|>", color="#b9c0c5", lw=0.7,
                                    shrinkA=0, shrinkB=0), zorder=1)

    y = top - n * slot + (slot - bh) / 2
    bx = ax.add_patch(FancyBboxPatch((0.020, y), 0.960, bh,
                                     boxstyle="round,pad=0,rounding_size=0.010",
                                     fc="#e9f5f0", ec=GREEN, lw=0.9, zorder=2))
    fits.append((ax.text(0.5, y + bh * 0.66, final[0], ha="center", va="center",
                         fontsize=6.7, color=INK, fontweight="bold", zorder=3), bx))
    fits.append((ax.text(0.5, y + bh * 0.26, final[1], ha="center", va="center",
                         fontsize=6.5, color=INK2, zorder=3), bx))
    # Rule 4 in geometry as well as numbers: assert every line fits its box rather than
    # trusting a measured-once point size. Overflowing box text was on the rebuild's own
    # defect list and the panel-level edge-ink check cannot see it.
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for txt, box in fits:
        tw = txt.get_window_extent(r).width
        bw = box.get_window_extent(r).width
        assert tw <= bw - 4, ("box text overflows by %.1f px: %r"
                              % (tw - (bw - 4), txt.get_text()))
    letter(fig, "A")
    save(fig, "p1a_cohort_flow")


if __name__ == "__main__":
    build()
