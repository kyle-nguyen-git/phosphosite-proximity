"""Render the Markdown preprint into a typeset, reviewable PDF."""

from __future__ import annotations

import html
import importlib.util
import re
from pathlib import Path

from reportlab import rl_config
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


MANUSCRIPT = Path(__file__).resolve().parents[1]
SOURCE = MANUSCRIPT / "preprint_draft_v1.md"
OUTPUT = MANUSCRIPT / "preprint_draft_v1.pdf"
MATPLOTLIB_SPEC = importlib.util.find_spec("matplotlib")
if MATPLOTLIB_SPEC is None or not MATPLOTLIB_SPEC.submodule_search_locations:
    raise RuntimeError("matplotlib is required to locate the bundled DejaVu font files")
FONT_DIR = Path(next(iter(MATPLOTLIB_SPEC.submodule_search_locations))) / "mpl-data" / "fonts" / "ttf"

# Keep the generated review PDF byte-stable for an unchanged environment and input tree.
rl_config.invariant = 1


def register_fonts() -> None:
    files = {
        "DejaVu": "DejaVuSans.ttf",
        "DejaVu-Bold": "DejaVuSans-Bold.ttf",
        "DejaVu-Oblique": "DejaVuSans-Oblique.ttf",
        "DejaVu-BoldOblique": "DejaVuSans-BoldOblique.ttf",
        "DejaVuMono": "DejaVuSansMono.ttf",
    }
    for name, filename in files.items():
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
    pdfmetrics.registerFontFamily(
        "DejaVu", normal="DejaVu", bold="DejaVu-Bold",
        italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique",
    )


def inline_markup(value: str) -> str:
    value = html.escape(value.strip())
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<link href="\2" color="#276FBF"><u>\1</u></link>',
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r'<font name="DejaVuMono">\1</font>', value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    value = re.sub(r"\^([^\^]+)\^", r"<super>\1</super>", value)
    return value


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="PaperTitle", fontName="DejaVu-Bold", fontSize=18, leading=22,
        spaceAfter=13, alignment=TA_LEFT, textColor=colors.HexColor("#171717"),
    ))
    styles.add(ParagraphStyle(
        name="Author", fontName="DejaVu", fontSize=10.2, leading=14,
        spaceAfter=4, textColor=colors.HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name="Section", fontName="DejaVu-Bold", fontSize=13.2, leading=16,
        spaceBefore=15, spaceAfter=7, keepWithNext=True,
        textColor=colors.HexColor("#171717"),
    ))
    styles.add(ParagraphStyle(
        name="Subsection", fontName="DejaVu-Bold", fontSize=10.7, leading=13,
        spaceBefore=11, spaceAfter=5, keepWithNext=True,
        textColor=colors.HexColor("#222222"),
    ))
    styles.add(ParagraphStyle(
        name="BodyPaper", fontName="DejaVu", fontSize=8.6, leading=12.0,
        alignment=TA_LEFT, spaceAfter=6.5, widowOrphanControl=True,
        textColor=colors.HexColor("#222222"),
    ))
    styles.add(ParagraphStyle(
        name="AbstractBody", parent=styles["BodyPaper"], fontSize=8.7, leading=12.2,
        leftIndent=12, rightIndent=12, borderColor=colors.HexColor("#C8CDD2"),
        borderWidth=0.7, borderPadding=9, backColor=colors.HexColor("#F7F8F9"),
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="Small", fontName="DejaVu", fontSize=7.5, leading=9.7,
        textColor=colors.HexColor("#555555"), spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="FigureCaption", fontName="DejaVu", fontSize=7.6, leading=10,
        textColor=colors.HexColor("#444444"), spaceBefore=5, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="Reference", fontName="DejaVu", fontSize=7.5, leading=10,
        leftIndent=14, firstLineIndent=-14, spaceAfter=3.5,
    ))
    styles.add(ParagraphStyle(
        name="TableCell", fontName="DejaVu", fontSize=6.7, leading=8.3,
        textColor=colors.HexColor("#222222"),
    ))
    styles.add(ParagraphStyle(
        name="TableHead", fontName="DejaVu-Bold", fontSize=6.8, leading=8.5,
        textColor=colors.white,
    ))
    return styles


def page_decor(canvas, doc) -> None:
    canvas._doc.Catalog.Lang = PDFString("en-US")
    canvas.saveState()
    width, height = A4
    canvas.setFont("DejaVu-Bold", 7.2)
    canvas.setFillColor(colors.HexColor("#A04444"))
    canvas.drawString(doc.leftMargin, height - 0.38 * inch, "DRAFT — NOT FOR POSTING")
    canvas.setFont("DejaVu", 7.2)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawRightString(width - doc.rightMargin, height - 0.38 * inch, "Nguyen · exploratory yeast calibration")
    canvas.setStrokeColor(colors.HexColor("#D6D6D6"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.47 * inch, width - doc.rightMargin, 0.47 * inch)
    canvas.drawCentredString(width / 2, 0.28 * inch, str(doc.page))
    canvas.restoreState()


class DraftDocTemplate(SimpleDocTemplate):
    """Draw the draft furniture after story content so it remains visible."""

    def afterPage(self) -> None:
        page_decor(self.canv, self)


def make_image(path: Path, caption: str, styles, max_width: float, max_height: float):
    with PILImage.open(path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    image = Image(str(path), width=width * scale, height=height * scale)
    return [KeepTogether([
        image,
        Paragraph(f"<b>{inline_markup(caption)}</b>", styles["FigureCaption"]),
    ])]


def parse_table(lines: list[str], styles, available_width: float):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) > 1 and all(set(cell) <= {"-", ":"} for cell in rows[1]):
        rows.pop(1)
    ncols = max(len(row) for row in rows)
    rows = [row + [""] * (ncols - len(row)) for row in rows]
    data = []
    for row_index, row in enumerate(rows):
        style = styles["TableHead"] if row_index == 0 else styles["TableCell"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    if ncols == 5:
        widths = [0.23, 0.12, 0.14, 0.10, 0.41]
    elif ncols == 4:
        widths = [0.35, 0.15, 0.22, 0.28]
    elif ncols == 6:
        widths = [0.27, 0.10, 0.10, 0.10, 0.12, 0.31]
    else:
        widths = [1 / ncols] * ncols
    table = Table(
        data, colWidths=[available_width * fraction for fraction in widths],
        repeatRows=1, hAlign="LEFT", splitByRow=1,
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3D5366")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9CED3")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F7")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def main() -> None:
    register_fonts()
    styles = build_styles()
    doc = DraftDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=0.67 * inch, rightMargin=0.67 * inch,
        topMargin=0.76 * inch, bottomMargin=0.62 * inch,
        title="Exploratory calibration of AlphaFold-derived distance",
        author="Kyle Nguyen",
        subject="Exploratory secondary analysis preprint draft",
        creator="Reproducible Phase 0.5 manuscript pipeline",
        keywords="yeast, phosphomutant, AlphaFold, UniProt, calibration, exploratory analysis",
    )
    available_width = A4[0] - doc.leftMargin - doc.rightMargin
    available_height = A4[1] - doc.topMargin - doc.bottomMargin
    story = []
    lines = SOURCE.read_text().splitlines()
    in_abstract = False
    in_references = False
    index = 0
    while index < len(lines):
        raw = lines[index].rstrip()
        stripped = raw.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("!["):
            match = re.match(r"!\[([^]]+)\]\(([^)]+)\)", stripped)
            if not match:
                raise RuntimeError(f"bad image directive: {stripped}")
            caption, relative = match.groups()
            path = (MANUSCRIPT / relative).resolve()
            story.extend(make_image(path, caption, styles, available_width, available_height * 0.73))
            index += 1
            continue
        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            story.append(Spacer(1, 4))
            story.append(parse_table(table_lines, styles, available_width))
            story.append(Spacer(1, 9))
            continue
        if stripped.startswith("# "):
            story.append(Paragraph(inline_markup(stripped[2:]), styles["PaperTitle"]))
            index += 1
            continue
        if stripped.startswith("## "):
            heading = stripped[3:]
            in_abstract = heading == "Abstract"
            in_references = heading == "References"
            if heading in {"Methods", "Tables", "References"}:
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), styles["Section"]))
            index += 1
            continue
        if stripped.startswith("### "):
            heading = stripped[4:]
            if heading.startswith("Table 2."):
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), styles["Subsection"]))
            index += 1
            continue
        if stripped.startswith("**") and stripped.endswith("**") and len(stripped) < 240:
            story.append(Paragraph(inline_markup(stripped), styles["Author"]))
            index += 1
            continue
        if stripped.startswith("**Draft status:**"):
            story.append(Paragraph(inline_markup(stripped), styles["Small"]))
            story.append(Spacer(1, 6))
            index += 1
            continue
        if in_references and re.match(r"\d+\.\s", stripped):
            story.append(Paragraph(inline_markup(stripped), styles["Reference"]))
        elif in_abstract and not stripped.startswith("**Keywords:"):
            story.append(Paragraph(inline_markup(stripped), styles["AbstractBody"]))
        elif stripped.startswith("**Keywords:") or stripped.startswith("^1^") or stripped.startswith("Correspondence:") or stripped.startswith("ORCID:"):
            story.append(Paragraph(inline_markup(stripped), styles["Small"]))
        else:
            story.append(Paragraph(inline_markup(stripped), styles["BodyPaper"]))
        index += 1

    doc.build(story)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
