# Manuscript design spec — recovered 2026-08-13 by measurement

## Why this file exists

The PDF Kyle sent to David Chang on 2026-08-12 was **not** built by the renderer in the release tree,
and the script that did build it did not survive. On 2026-08-13 the manuscript was rebuilt with
`phase0_calibration/manuscript/src/build_preprint_pdf.py`, which was the only builder findable in the
vault. That silently replaced the design: US Letter became A4, Charis SIL became DejaVu Sans, 20 pages
became 19, and a red "DRAFT — NOT FOR POSTING" banner and a running header appeared on every page.

Kyle identified the regression by eye. This file records the original design, measured directly from
`phosphosite_proximity_paper.pdf` as sent (SHA-256 begins `8e9ea94e83b2b4e7`, 1,550,539 bytes,
20 pages), so it can be rebuilt without the original script.

## The two builders, and which one is right

| | Original (correct) | Release-tree renderer (wrong for this document) |
|---|---|---|
| File | not recovered | `phase0_calibration/manuscript/src/build_preprint_pdf.py` |
| Page | **US Letter, 612 × 792 pt** | A4, 595 × 842 pt |
| Body font | **Charis SIL 10 pt** | DejaVu Sans 9.4 pt |
| Draft banner | **none** | red "DRAFT — NOT FOR POSTING", every page |
| Running header | **none** | "Nguyen · exploratory yeast calibration" |
| Abstract | **plain paragraphs** | boxed, shaded |
| Pages | **20** | 19 |
| Metadata | stripped | hardcoded, stale |

The release-tree renderer is correct for `preprint_draft_v1`, the superseded single-author draft it was
written for, and it is hash-bound to that document. It must not be used for the current manuscript.

## Measured page geometry

| Quantity | Value |
|---|---|
| Page size | 612 × 792 pt (US Letter) |
| Left margin | 64.0 pt |
| Right margin | 64.0 pt (measured 65.4 to the last glyph edge) |
| Top margin | 61.2 pt to first baseline top |
| Bottom margin | 57.0 pt |
| Text column width | 482.6 pt measured; 484.0 pt with 64 pt margins |

## Measured type

| Role | Font | Size | Notes |
|---|---|---|---|
| Body | Charis SIL Regular | 10.0 pt | 3,047 of ~3,240 characters on page 1 |
| Body leading | — | **14.2 pt** | modal baseline delta, 26 occurrences on page 1 |
| Paragraph spacing | — | 24.2 pt baseline-to-baseline | 14.2 leading + ~10 pt space between paragraphs |
| Title (H1) | Charis SIL Bold | 15.0 pt | |
| Section heading (H2) | Charis SIL Bold | 12.5 pt | |
| Inline bold | Charis SIL Bold | 10.0 pt | |
| Inline italic | Charis SIL Italic | 10.0 pt | |
| Superscript | Charis SIL Regular | 8.3 pt | affiliation and footnote markers |
| Monospace | Nimbus Mono PS | — | inline code spans |

Noto Serif Regular also appears, as a fallback for glyphs Charis SIL does not cover.

## Fonts

Charis SIL is embedded in the source PDF but content-reduced, so the embedded copies cannot typeset new
text. The upstream release is vendored instead, under `fonts/`:

| File | SHA-256 (first 16) |
|---|---|
| `CharisSIL-Regular.ttf` | `346337374aa347d6` |
| `CharisSIL-Bold.ttf` | `68460d2b76c8f781` |
| `CharisSIL-Italic.ttf` | `e776e2961117b39c` |
| `CharisSIL-BoldItalic.ttf` | `acdf6dc54c0ee5e0` |

Charis SIL 6.101, from `software.sil.org/downloads/r/charis/CharisSIL-6.101.zip`, SIL Open Font
License 1.1. `fonts/OFL.txt` is the licence as shipped. The OFL permits redistribution, so these can
travel with the public repository; the reserved font name means a modified font may not keep the name.

Nimbus Mono PS is not vendored. It carries the URW/AFPL heritage and is present in many Linux
distributions; a metrically similar substitute is acceptable for the few inline code spans, and any
substitution should be recorded here.

## Figures

Two raster figures, on **page 4** and **page 10** of the 20-page original. Sources are
`phase0_calibration/manuscript/figure1.png` and `figure2.png`, referenced from the Markdown.

## Producer chain

The delivered file reports `Producer(MuPDF 1.29.0)` with every other property empty. The original
renderer's identity was overwritten by a MuPDF normalization pass, which is the project's existing
determinism step. Metadata was left empty rather than set.

**Decision for the rebuild:** set correct properties rather than leaving them empty. The stale values
the release-tree renderer wrote — an abandoned title, one author on a two-author paper — are worse than
either. Title, authors and keywords are derived from the Markdown so they cannot drift.

## What is not recovered

- The original script, its language, and its Markdown parser.
- Exact heading spacing above and below, list indents, and table styling. These are reconstructed to
  match visually and are not measured to the point.
- Why the original ran to 20 pages against the release renderer's 19. Page size and font metrics
  account for most of it; this was not decomposed.
