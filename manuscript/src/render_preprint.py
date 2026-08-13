"""Render every preprint page and bind the images to the source PDF by SHA-256."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


MANUSCRIPT = Path(__file__).resolve().parents[1]
PDF = MANUSCRIPT / "preprint_draft_v1.pdf"
RENDERED = MANUSCRIPT / "rendered"
RENDER_DPI = 144


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_contact_sheet(page_paths: list[Path], destination: Path) -> None:
    columns = 2
    gap = 16
    margin = 18
    thumbnail_width = 360
    thumbnails: list[Image.Image] = []
    for page_path in page_paths:
        with Image.open(page_path) as source:
            thumbnail = source.convert("RGB")
            thumbnail.thumbnail((thumbnail_width, 10_000), Image.Resampling.LANCZOS)
            thumbnails.append(thumbnail.copy())

    rows = (len(thumbnails) + columns - 1) // columns
    cell_width = max(image.width for image in thumbnails)
    cell_height = max(image.height for image in thumbnails)
    sheet = Image.new(
        "RGB",
        (
            margin * 2 + columns * cell_width + (columns - 1) * gap,
            margin * 2 + rows * cell_height + (rows - 1) * gap,
        ),
        "white",
    )
    for index, thumbnail in enumerate(thumbnails):
        row, column = divmod(index, columns)
        x = margin + column * (cell_width + gap)
        y = margin + row * (cell_height + gap)
        sheet.paste(thumbnail, (x, y))
    sheet.save(destination, optimize=True)


def main() -> None:
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise SystemExit("pdftoppm is required to render the preprint")
    page_count = len(PdfReader(str(PDF)).pages)
    if page_count == 0:
        raise SystemExit("preprint PDF contains no pages")

    with tempfile.TemporaryDirectory(prefix="preprint-render-") as temporary:
        prefix = Path(temporary) / "page"
        subprocess.run(
            [pdftoppm, "-png", "-r", str(RENDER_DPI), str(PDF), str(prefix)],
            check=True,
        )
        generated = sorted(Path(temporary).glob("page-*.png"))
        if len(generated) != page_count:
            raise SystemExit(
                f"rendered {len(generated)} pages from a {page_count}-page PDF"
            )

        RENDERED.mkdir(parents=True, exist_ok=True)
        for stale in RENDERED.glob("page-*.png"):
            stale.unlink()
        for stale_name in ("contact-sheet.png", "render_manifest.json"):
            stale = RENDERED / stale_name
            if stale.exists():
                stale.unlink()

        page_paths: list[Path] = []
        for page_number, source in enumerate(generated, start=1):
            destination = RENDERED / f"page-{page_number:02d}.png"
            shutil.copy2(source, destination)
            page_paths.append(destination)

    contact_sheet = RENDERED / "contact-sheet.png"
    build_contact_sheet(page_paths, contact_sheet)
    manifest = {
        "pdf": PDF.name,
        "pdf_sha256": sha256(PDF),
        "page_count": page_count,
        "render_dpi": RENDER_DPI,
        "pages": [
            {
                "page": index,
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for index, path in enumerate(page_paths, start=1)
        ],
        "contact_sheet": {
            "file": contact_sheet.name,
            "bytes": contact_sheet.stat().st_size,
            "sha256": sha256(contact_sheet),
        },
    }
    (RENDERED / "render_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(
        f"rendered {page_count} pages at {RENDER_DPI} dpi; "
        f"PDF sha256={manifest['pdf_sha256']}"
    )


if __name__ == "__main__":
    main()
