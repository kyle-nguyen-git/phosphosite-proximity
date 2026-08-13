"""Compose individually-built panel PDFs into figures. Placement only, never rescaling.

Each panel is stamped at its authored millimetre size, so type keeps the point size it was
built at. Both figures are authored at COL2 (183 mm) so a typesetter setting them to
double-column width applies a 1.0x scale; the previous 160 mm Figure 1 matched no journal
column measure and would have been enlarged 1.14x.
"""
import os

import fitz

from src._style import COL2

PT = 72 / 25.4
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DEST = os.path.dirname(HERE)

FIGURES = {
    "figure1": dict(size=(COL2, 74), panels=[
        ("p1a_cohort_flow", 3, 5),
        ("p1b_roc", 108, 5),
    ]),
    "figure2": dict(size=(COL2, 217), panels=[
        ("p2a_ecdf", 3, 4),
        ("p2b_pae_scatter", 93, 4),
        ("p2c_confidence_forest", 3, 70),
        ("p2d_sensitivity_forest", 3, 138),
    ]),
}


def compose(name, spec):
    w, h = spec["size"]
    doc = fitz.open()
    page = doc.new_page(width=w * PT, height=h * PT)
    for panel, x, y in spec["panels"]:
        src = fitz.open(os.path.join(OUT, f"{panel}.pdf"))
        pw, ph = src[0].rect.width, src[0].rect.height
        rect = fitz.Rect(x * PT, y * PT, x * PT + pw, y * PT + ph)
        assert rect.x1 <= w * PT + 1e-6 and rect.y1 <= h * PT + 1e-6, \
            f"{name}: {panel} runs off the canvas at ({x}, {y})"
        page.show_pdf_page(rect, src, 0)          # native size, never scaled
        src.close()
    pdf = os.path.join(DEST, f"{name}.pdf")
    # no_new_id keeps the trailer /ID out, so an unchanged rebuild is byte-identical.
    # Setting the ID by hand does not work: MuPDF regenerates the second element on save.
    doc.save(pdf, no_new_id=1)
    page.get_pixmap(dpi=600).save(os.path.join(DEST, f"{name}.png"))
    doc.close()
    print(f"  {name:10s} {w:5.0f} x {h:5.0f} mm  ->  {pdf}")


if __name__ == "__main__":
    for name, spec in FIGURES.items():
        compose(name, spec)
