"""Rebuild the manuscript figures to PLOS ONE's technical requirements.

PLOS ONE requires figures as "TIFF or EPS only", at "300 - 600 dpi", width "789 - 2250 pixels (at 300
dpi)", height at most "2625 pixels", RGB 8-bit or grayscale, at most 10 MB, and
**"Arial, Times, or Symbol font only in 8-12 point"**.

The release panels are drawn in DejaVu Sans at 7 pt with legends at 6.8 pt, and they live inside the
hash-bound release tree — `phase0_calibration/manuscript/panels/src/_style.py` is bound by the 69-check
verifier, so it is not edited. This script rebuilds the same panels into a separate output directory
with the rcParams overridden after `_style` has been imported, composes them, and writes TIFFs.

Type going from 7 pt to 8 pt inside panels that are laid out at exact physical millimetre sizes can
overflow. The script reports the size change and every panel's dimensions so overflow can be checked
rather than assumed; look at the rendered TIFFs before submitting them.

Usage:
    python build_submission_figures.py [--font Arial] [--size 8] [--dpi 300]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
PANELS = RESEARCH / "phase0_calibration" / "manuscript" / "panels"
OUT = HERE / "submission_figures"

PANEL_SCRIPTS = [
    "p1a_cohort_flow.py", "p1b_roc.py", "p2a_ecdf.py",
    "p2b_pae_scatter.py", "p2c_confidence_forest.py", "p2d_sensitivity_forest.py",
]

# Injected ahead of each panel script. `_style` sets the rcParams at import, so the override has to run
# after that import and before the panel draws anything.
SHIM = """
import matplotlib, matplotlib.pyplot as plt
import _style  # noqa: F401  — sets the release rcParams first
plt.rcParams.update({{
    "font.family": {font!r},
    "font.sans-serif": [{font!r}],
    "font.serif": [{font!r}],
    "font.size": {size},
    "axes.titlesize": {size},
    "axes.labelsize": {size},
    "xtick.labelsize": {size},
    "ytick.labelsize": {size},
    "legend.fontsize": {size},
    "figure.titlesize": {size},
}})
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--size", type=float, default=8.0)
    ap.add_argument("--dpi", type=int, default=300)
    a = ap.parse_args()

    import matplotlib.font_manager as fm
    if a.font not in {f.name for f in fm.fontManager.ttflist}:
        raise SystemExit(f"font {a.font!r} is not available to matplotlib; PLOS accepts Arial, Times or Symbol")

    OUT.mkdir(exist_ok=True)
    # The panel scripts resolve every input path from their own file location, so a flat copy breaks
    # them. Mirror the release layout in a temporary tree instead: real data is symlinked in, and only
    # the drawing code and the output directories are local, so nothing in the hash-bound tree is
    # touched or overwritten.
    root = Path(tempfile.mkdtemp(prefix="plosfig_"))
    cal = root / "phase0_calibration"
    (cal / "manuscript" / "panels").mkdir(parents=True)
    real_cal = RESEARCH / "phase0_calibration"
    for name in ("results", "phase0_5", "data", "NUMBERS.md"):
        src = real_cal / name
        if src.exists():
            (cal / name).symlink_to(src)
    work = cal / "manuscript" / "panels"
    shutil.copytree(PANELS / "src", work / "src")
    shutil.copy(PANELS / "compose.py", work / "compose.py")
    (work / "out").mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONPATH=str(work / "src"), MPLCONFIGDIR=str(root / ".mpl"))

    print(f"rebuilding {len(PANEL_SCRIPTS)} panels in {a.font} {a.size:g} pt")
    for name in PANEL_SCRIPTS:
        src = (work / "src" / name).read_text()
        shim = SHIM.format(font=a.font, size=a.size)
        # keep the module docstring first, then inject
        lines = src.split("\n")
        cut = 0
        if lines and lines[0].startswith(('"""', "'''")):
            q = lines[0][:3]
            cut = next(i for i, l in enumerate(lines) if l.rstrip().endswith(q) and i > 0) + 1
        patched = "\n".join(lines[:cut]) + "\n" + shim + "\n" + "\n".join(lines[cut:])
        (work / "src" / name).write_text(patched)
        r = subprocess.run([sys.executable, str(work / "src" / name)], cwd=work, env=env,
                           capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:])
            raise SystemExit(f"panel {name} failed")
        print(f"  {name}")

    r = subprocess.run([sys.executable, str(work / "compose.py")], cwd=work, env=env,
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit("compose failed")
    print(r.stdout.strip())

    import pymupdf
    from PIL import Image
    dest = work / "out"
    made = []
    for n in (1, 2):
        pdf = next((p for p in [work.parent / f"figure{n}.pdf", dest / f"figure{n}.pdf"]
                    if p.exists()), None)
        if pdf is None:
            print(f"  figure{n}: no composed PDF found")
            continue
        pix = pymupdf.open(pdf)[0].get_pixmap(dpi=a.dpi)
        png = OUT / f"_fig{n}.png"
        pix.save(png)
        img = Image.open(png).convert("RGB")
        tif = OUT / f"Fig{n}.tif"
        img.save(tif, format="TIFF", compression="tiff_lzw", dpi=(a.dpi, a.dpi))
        png.unlink()
        w, h = img.size
        mb = tif.stat().st_size / 1e6
        ok_w = 789 <= w <= 2250
        ok_h = h <= 2625
        ok_mb = mb <= 10
        print(f"  {tif.name}: {w} x {h} px at {a.dpi} dpi, {mb:.1f} MB"
              f"  width {'ok' if ok_w else 'OUT OF RANGE (789-2250)'}"
              f"  height {'ok' if ok_h else 'OVER 2625'}"
              f"  size {'ok' if ok_mb else 'OVER 10 MB'}")
        made.append(tif)

    print(f"\nwrote {len(made)} TIFF(s) to {OUT}")
    print("Look at them before submitting: 7 pt to "
          f"{a.size:g} pt is a {100 * (a.size / 7 - 1):.0f}% type increase inside fixed-size panels.")


if __name__ == "__main__":
    main()
