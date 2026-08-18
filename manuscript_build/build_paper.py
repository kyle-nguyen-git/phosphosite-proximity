"""Rebuild the PDF and Word versions of the current preprint from its Markdown source.

The Markdown at `outputs/fulbright/research/phosphosite_proximity_paper.md` is the source of
record. The PDF and .docx beside it are build products and must never be edited directly.

The PDF renderer is the one frozen inside the release tree
(`phase0_calibration/manuscript/src/build_preprint_pdf.py`). That file is hash-bound and is not
edited here; it is imported and its three path globals are redirected, which is why the image
references in the Markdown are written relative to this directory. The Word builder takes its
paths on the command line and needs no redirection.

Both builders live outside the vault's default interpreter's dependency set. Create the
environment first:

    python3 -m venv .venv && .venv/bin/pip install reportlab pillow matplotlib python-docx lxml

Then:

    .venv/bin/python build_paper.py

matplotlib is not used for drawing here; the frozen renderer reads the DejaVu TTF files that ship
inside the matplotlib package, so it must be importable.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
STEM = "phosphosite_proximity_paper"
SOURCE = RESEARCH / f"{STEM}.md"
PDF = RESEARCH / f"{STEM}.pdf"
DOCX = RESEARCH / f"{STEM}.docx"
PDF_RENDERER = HERE / "render_manuscript_pdf.py"
DOCX_RENDERER = HERE / "render_manuscript_docx.py"


def source_metadata() -> dict:
    """Title, authors and keywords taken from the Markdown so they cannot drift from it."""
    lines = SOURCE.read_text().splitlines()
    title = next(ln[2:].strip() for ln in lines if ln.startswith("# "))
    authors = next(
        ", ".join(re.findall(r"\*\*([^*]+)\*\*", ln))
        for ln in lines
        if ln.startswith("**") and "^1^" in ln
    )
    keywords = next(
        (
            ln[len("**Keywords:**"):].replace(";", ",").strip()
            for ln in lines
            if ln.startswith("**Keywords:**")
        ),
        "",
    )
    return {"title": title, "author": authors, "keywords": keywords}


def build_pdf() -> None:
    subprocess.run([sys.executable, str(PDF_RENDERER), str(SOURCE), str(PDF)], check=True)
    stamp_pdf_metadata()


def strip_images(text: str) -> str:
    """Remove embedded figures for the PLOS build, which uploads them as separate files."""
    return re.sub(r"^!\[[^\]]*\]\([^)]*\)\n\n?", "", text, flags=re.M)


def stamp_pdf_metadata() -> None:
    """Overwrite the renderer's hardcoded document properties.

    The delivered original left every property empty, and the release-tree renderer wrote stale ones:
    a title Kyle abandoned, and one author on a two-author paper. Both are worse than correct values,
    so they are set here from the Markdown and cannot drift from it.
    """
    import pymupdf

    meta = source_metadata()
    doc = pymupdf.open(PDF)
    doc.set_metadata({
        "title": meta["title"],
        "author": meta["author"],
        "subject": "Exploratory secondary analysis of two published phosphosite-mutant screens, in yeast and human",
        "keywords": meta["keywords"],
        "creator": "phosphosite-proximity manuscript pipeline",
        "producer": "",
    })
    doc.save(PDF, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP, no_new_id=1)
    doc.close()
    print(f"metadata: {meta['author']} — {meta['title'][:60]}…")


def build_docx() -> None:
    subprocess.run([sys.executable, str(DOCX_RENDERER), str(SOURCE), str(DOCX)], check=True)


if __name__ == "__main__":
    if not SOURCE.exists():
        raise SystemExit(f"source not found: {SOURCE}")
    build_pdf()
    build_docx()
    for path in (PDF, DOCX):
        print(f"{path.name}: {path.stat().st_size:,} bytes")
