"""Render the manuscript to PDF in the design Kyle sent David Chang on 2026-08-12.

The script that produced that file did not survive. Its design was measured out of the delivered PDF
and is recorded in DESIGN_SPEC.md; this renderer implements that spec. It is deliberately separate from
`phase0_calibration/manuscript/src/build_preprint_pdf.py`, which belongs to the superseded
`preprint_draft_v1`, is hash-bound to it, and produces a different document: A4 rather than US Letter,
DejaVu Sans rather than Charis SIL, a boxed abstract, and a red draft banner with a running header on
every page.

No page numbers, headers or footers: the original has none.

Usage:
    python render_manuscript_pdf.py SOURCE.md OUTPUT.pdf
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab import rl_config
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors

HERE = Path(__file__).resolve().parent
FONTS = HERE / "fonts"

# ---- measured geometry (DESIGN_SPEC.md) ---------------------------------------------------------
PAGE = LETTER                 # 612 x 792 pt
MARGIN_X = 64.0
MARGIN_TOP = 64.1
MARGIN_BOTTOM = 57.0
BODY_SIZE = 10.0
BODY_LEADING = 14.2
PARA_SPACE = 10.0             # 24.2 pt baseline-to-baseline minus the 14.2 pt leading
CODE_SIZE = 8.5
TABLE_SIZE = 8.0

# Nimbus Mono PS is URW's Courier clone and is metrically compatible with Courier, which reportlab
# ships. The substitution is recorded in DESIGN_SPEC.md.
MONO = "Courier"
MONO_BOLD = "Courier-Bold"

rl_config.invariant = 1       # keep the output byte-stable for an unchanged input and environment


def register_fonts() -> None:
    faces = {
        "CharisSIL": "CharisSIL-Regular.ttf",
        "CharisSIL-Bold": "CharisSIL-Bold.ttf",
        "CharisSIL-Italic": "CharisSIL-Italic.ttf",
        "CharisSIL-BoldItalic": "CharisSIL-BoldItalic.ttf",
    }
    missing = [f for f in faces.values() if not (FONTS / f).exists()]
    if missing:
        raise SystemExit(
            f"missing vendored fonts in {FONTS}: {', '.join(missing)}\n"
            "See DESIGN_SPEC.md — Charis SIL 6.101, SIL Open Font License."
        )
    for name, filename in faces.items():
        pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))
    pdfmetrics.registerFontFamily(
        "CharisSIL", normal="CharisSIL", bold="CharisSIL-Bold",
        italic="CharisSIL-Italic", boldItalic="CharisSIL-BoldItalic",
    )


def styles() -> dict:
    base = dict(fontName="CharisSIL", fontSize=BODY_SIZE, leading=BODY_LEADING,
                alignment=TA_LEFT, textColor=colors.black)
    return {
        "body": ParagraphStyle("body", spaceAfter=PARA_SPACE, **base),
        # measured: 15 pt bold title, 12.5 / 11 / 10.5 for the heading levels
        "h1": ParagraphStyle("h1", fontName="CharisSIL-Bold", fontSize=15.0, leading=19.0,
                             spaceBefore=0, spaceAfter=12.0, textColor=colors.black),
        "h2": ParagraphStyle("h2", fontName="CharisSIL-Bold", fontSize=12.5, leading=16.0,
                             spaceBefore=14.0, spaceAfter=7.0, textColor=colors.black),
        "h3": ParagraphStyle("h3", fontName="CharisSIL-Bold", fontSize=11.0, leading=14.5,
                             spaceBefore=12.0, spaceAfter=6.0, textColor=colors.black),
        "h4": ParagraphStyle("h4", fontName="CharisSIL-BoldItalic", fontSize=10.5, leading=14.0,
                             spaceBefore=10.0, spaceAfter=5.0, textColor=colors.black),
        "cell": ParagraphStyle("cell", fontName="CharisSIL", fontSize=TABLE_SIZE, leading=10.4,
                               alignment=TA_LEFT, textColor=colors.black),
        "cellhead": ParagraphStyle("cellhead", fontName="CharisSIL-Bold", fontSize=TABLE_SIZE,
                                   leading=10.4, alignment=TA_LEFT, textColor=colors.black),
        "listitem": ParagraphStyle("listitem", spaceAfter=3.0, **base),
    }


# ---- inline markup ------------------------------------------------------------------------------
_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_ITAL = re.compile(r"(?<![\*\w])\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)", re.S)
_SUP = re.compile(r"\^([^\^\s]+)\^")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def inline(text: str, mono: str = MONO) -> str:
    """Markdown inline markup to reportlab paragraph markup.

    Code spans are extracted before escaping so their contents cannot be reinterpreted as markup,
    which matters here because the manuscript uses identifiers such as `min_dist_A` and `ACT_SITE`.
    """
    stash: list[str] = []

    def keep(m: re.Match) -> str:
        stash.append(m.group(1))
        return f"\x00{len(stash) - 1}\x00"

    text = _CODE.sub(keep, text)
    text = _LINK.sub(r"\1", text)          # the original prints link text only, no URL
    text = html.escape(text, quote=False)
    text = _BOLD.sub(r"<b>\1</b>", text)
    text = _ITAL.sub(r"<i>\1</i>", text)
    text = _SUP.sub(r"<super>\1</super>", text)

    def restore(m: re.Match) -> str:
        body = html.escape(stash[int(m.group(1))], quote=False)
        return f'<font face="{mono}" size="{CODE_SIZE}">{body}</font>'

    return re.sub(r"\x00(\d+)\x00", restore, text)


# ---- tables -------------------------------------------------------------------------------------
def split_row(line: str) -> list[str]:
    """Split a pipe table row, honouring backslash-escaped pipes."""
    parts, cur, i = [], [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if c == "|":
            parts.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    parts.append("".join(cur))
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells)


def build_table(rows: list[list[str]], st: dict, avail: float) -> Table:
    header, body = rows[0], rows[1:]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    header, body = rows[0], rows[1:]

    # Column widths proportional to the longest natural line in each column, floored so a narrow
    # column stays readable and capped to the text measure.
    weights = []
    for c in range(ncol):
        longest = max((len(re.sub(r"[*`\\]", "", r[c])) for r in rows), default=1)
        weights.append(max(longest, 4) ** 0.72)
    total = sum(weights)
    widths = [max(34.0, avail * w / total) for w in weights]
    if sum(widths) > avail:                       # rescale if the floors overflowed
        widths = [w * avail / sum(widths) for w in widths]

    data = [[Paragraph(inline(c), st["cellhead"]) for c in header]]
    data += [[Paragraph(inline(c), st["cell"]) for c in r] for r in body]

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ---- document -----------------------------------------------------------------------------------
def build(source: Path, output: Path) -> None:
    register_fonts()
    st = styles()
    avail = PAGE[0] - 2 * MARGIN_X

    # SimpleDocTemplate's frame carries 6 pt of padding on every side, which would push the text
    # measure in from the 64 pt margin the original uses. The frame is built explicitly with zero
    # padding so the measured geometry is the geometry that ships.
    doc = BaseDocTemplate(
        str(output), pagesize=PAGE,
        leftMargin=MARGIN_X, rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOTTOM,
        title="", author="", subject="", creator="",
    )
    frame = Frame(
        MARGIN_X, MARGIN_BOTTOM,
        PAGE[0] - 2 * MARGIN_X, PAGE[1] - MARGIN_TOP - MARGIN_BOTTOM,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="body",
    )
    doc.addPageTemplates([PageTemplate(id="page", frames=[frame])])

    story: list = []
    lines = source.read_text().splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if not line.strip():
            i += 1
            continue

        # image
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if m:
            path = (source.parent / m.group(2)).resolve()
            if path.exists():
                from PIL import Image as PILImage
                with PILImage.open(path) as im:
                    w, h = im.size
                scale = min(avail / w, 1.0)
                story.append(Spacer(1, 4))
                story.append(Image(str(path), width=w * scale, height=h * scale))
                story.append(Spacer(1, 8))
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,4}) +(.*)$", line)
        if m:
            level = len(m.group(1))
            story.append(Paragraph(inline(m.group(2)), st[f"h{level}"]))
            i += 1
            continue

        # table
        if line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i])
                i += 1
            rows = [split_row(b) for b in block]
            rows = [r for r in rows if not is_separator(r)]
            if rows:
                story.append(Spacer(1, 2))
                story.append(build_table(rows, st, avail))
                story.append(Spacer(1, PARA_SPACE))
            continue

        # lists
        m = re.match(r"^(\s*)([-*+]|\d+\.) +(.*)$", line)
        if m:
            ordered = not m.group(2) in ("-", "*", "+")
            items, first = [], True
            while i < len(lines):
                mm = re.match(r"^(\s*)([-*+]|\d+\.) +(.*)$", lines[i])
                if not mm:
                    # continuation line of the previous item
                    if items and lines[i].startswith(("  ", "\t")) and lines[i].strip():
                        items[-1] += " " + lines[i].strip()
                        i += 1
                        continue
                    break
                if (not mm.group(2) in ("-", "*", "+")) != ordered and not first:
                    break
                items.append(mm.group(3))
                first = False
                i += 1
            story.append(ListFlowable(
                [ListItem(Paragraph(inline(t), st["listitem"]), leftIndent=16) for t in items],
                bulletType="1" if ordered else "bullet",
                bulletFontName="CharisSIL", bulletFontSize=BODY_SIZE,
                leftIndent=16, start="1" if ordered else None,
            ))
            story.append(Spacer(1, PARA_SPACE - 3))
            continue

        # horizontal rule -> the original shows none; skip
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", line.strip()):
            i += 1
            continue

        # paragraph: gather until blank or a construct starts
        para = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if (not nxt.strip() or nxt.lstrip().startswith("|")
                    or re.match(r"^#{1,6} ", nxt) or nxt.startswith("![")
                    or re.match(r"^(\s*)([-*+]|\d+\.) +", nxt)):
                break
            para.append(nxt)
            i += 1
        story.append(Paragraph(inline(" ".join(x.strip() for x in para)), st["body"]))

    doc.build(story)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    build(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    print(f"wrote {sys.argv[2]}")
