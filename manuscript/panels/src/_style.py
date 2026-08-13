"""Shared style for individually-built manuscript panels.

Design rules, applied everywhere:
  1. Panels are built at an EXACT physical size in mm. Composition is placement only,
     never rescaling, so type stays at its intended point size in the final figure.
  2. NO statistics printed inside a plot's data area. Numbers live in the caption.
     Floating text blocks over data were the main defect of the previous figures.
  3. Legends sit outside the axes, or in a region proven empty for that panel.
  4. Every panel reads its numbers from committed files. Nothing is hand-typed.

Colour vocabulary, fixed across both figures so the reader learns it once:
  BLUE / ORANGE  = cohort arm (primary / inclusive). Never used for anything else.
  INK2 / GREEN   = outcome (screen-negative / screen-positive).
  PURPLE         = post hoc comparator (SIFT), visually apart from both.
"""
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MM = 1 / 25.4                      # mm -> inches
COL2 = 183                         # journal double-column width, mm

_SRC = os.path.dirname(os.path.abspath(__file__))          # .../manuscript/panels/src
PANELS = os.path.dirname(_SRC)                              # .../manuscript/panels
HERE = os.path.dirname(os.path.dirname(PANELS))             # .../phase0_calibration
RES = os.path.join(HERE, "results")
P5 = os.path.join(HERE, "phase0_5", "results")
NUMBERS = os.path.join(HERE, "NUMBERS.md")
OUT = os.path.join(PANELS, "out")
os.makedirs(OUT, exist_ok=True)


# --- numerical authority -------------------------------------------------------------
# Rule 4 above says nothing is hand-typed. A panel that asserts against an integer typed
# into its own source only proves the typist and the pipeline agree with each other, so
# the counts a panel guards against are parsed out of NUMBERS.md at build time. Changing
# a cohort count now requires changing the authority, which is the point.

def _numbers_section(heading):
    """Lines of the NUMBERS.md section whose heading starts with `heading`."""
    with open(NUMBERS) as fh:
        text = fh.read()
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.startswith(heading)
            continue
        if inside:
            out.append(line)
    if not out:
        raise SystemExit("NUMBERS.md has no section starting %r" % heading)
    return out


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")] if "|" in line else []


def _count(cell):
    m = re.fullmatch(r"\*{0,2}([0-9][0-9,]*)\*{0,2}", cell)
    return int(m.group(1).replace(",", "")) if m else None


def numbers_cascade():
    """Section 4 cohort cascade as [(strain records, substitutions, proteins), ...]."""
    rows = []
    for line in _numbers_section("## 4."):
        cells = _cells(line)
        if len(cells) != 4:
            continue
        counts = [_count(c) for c in cells[1:]]
        if all(c is not None for c in counts):
            rows.append(tuple(counts))
    if len(rows) != 6:
        raise SystemExit("NUMBERS.md section 4 gave %d cascade rows, expected 6" % len(rows))
    return rows


def numbers_arms():
    """Section 1 arms as {"primary": (n, proteins, positive), "inclusive": (...)}."""
    arms = {}
    for line in _numbers_section("## 1."):
        cells = _cells(line)
        if len(cells) != 6:
            continue
        counts = [_count(c) for c in cells[1:4]]
        if any(c is None for c in counts):
            continue
        label = cells[0].lower()
        if "primary" in label:
            arms["primary"] = tuple(counts)
        elif "sensitivity" in label or "included" in label:
            arms["inclusive"] = tuple(counts)
    if set(arms) != {"primary", "inclusive"}:
        raise SystemExit("NUMBERS.md section 1 did not yield both arms: %s" % sorted(arms))
    return arms


def numbers_roc_band():
    """(draws, seed) for the Figure 1B ROC envelope, declared in NUMBERS.md section 17.

    The envelope is a reader-facing resampling result, so its draw count and seed belong
    in the authority like every other declared draw count. A panel that invents its own
    is the defect this replaces.
    """
    with open(NUMBERS) as fh:
        m = re.search(
            r"Figure 1B ROC envelope.*?\*\*([0-9,]+)\*\* protein-cluster draws"
            r".*?seed \*\*([0-9]+)\*\*", fh.read(), re.DOTALL)
    if not m:
        raise SystemExit("could not parse the Figure 1B ROC-envelope contract from NUMBERS.md")
    return int(m.group(1).replace(",", "")), int(m.group(2))

# Validated pair: worst adjacent CVD dE 96.7 (see dataviz palette validation)
BLUE, ORANGE = "#2a78d6", "#eb6834"
GREEN = "#1baf7a"
PURPLE = "#7a4fd0"
INK, INK2, INK3 = "#16181a", "#585c60", "#9aa0a6"
GRID = "#e8eaec"

# Both forests are 177 mm wide and share these, so one AUC unit is the same number of
# millimetres in each. Stacking two forests is only worth doing if they compare by eye;
# previously the same primary interval was drawn 15.0 mm wide in one and 16.2 mm in the
# other. Change these together or not at all.
FOREST_W_MM = 177
FOREST_L, FOREST_W = 0.295, 0.690
FOREST_XLIM = (0.15, 1.03)
FOREST_XTICKS = [0.2, 0.4, 0.6, 0.8, 1.0]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 7,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8,
    "xtick.labelsize": 6.8,
    "ytick.labelsize": 6.8,
    "legend.fontsize": 6.8,
    "axes.edgecolor": INK3,
    "axes.linewidth": 0.6,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.4,
    "ytick.major.size": 2.4,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,            # embed TrueType so text stays editable/selectable
    "ps.fonttype": 42,
    # Pinned, not inherited: a user matplotlibrc with savefig.bbox=tight would crop
    # every panel to its ink and silently break compose.py's placement geometry.
    "savefig.bbox": "standard",
    "savefig.pad_inches": 0,
})


def panel(width_mm, height_mm):
    """A figure sized in millimetres, with no implicit padding."""
    fig = plt.figure(figsize=(width_mm * MM, height_mm * MM))
    fig._panel_mm = (width_mm, height_mm)
    return fig


def letter(fig, ch, inset_mm=0.6):
    """Panel letter, top-left, at a CONSTANT millimetre inset on every panel."""
    w, h = fig.get_size_inches()
    fig.text(inset_mm * MM / w, 1 - inset_mm * MM / h, ch,
             fontsize=9, fontweight="bold", color=INK, va="top", ha="left")


def grid(ax, axis="both"):
    ax.grid(axis=axis, color=GRID, lw=0.5, zorder=0)
    ax.set_axisbelow(True)


def save(fig, name):
    """Emit PDF (for vector composition) and PNG (for quick eyeballing)."""
    want = getattr(fig, "_panel_mm", None)
    for ext in ("pdf", "png"):
        # Drop the wall-clock /CreationDate so a rebuilt panel is byte-comparable to the
        # committed one. Same contract as rl_config.invariant in build_preprint_pdf.py.
        meta = {"CreationDate": None} if ext == "pdf" else None
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=600, metadata=meta)
    w, h = fig.get_size_inches()
    if want is not None:
        got = (round(w / MM, 3), round(h / MM, 3))
        assert got == (round(want[0], 3), round(want[1], 3)), \
            f"{name}: saved at {got} mm, authored at {want} mm"
    plt.close(fig)
    print(f"  {name:28s} {w/MM:6.1f} x {h/MM:6.1f} mm")
