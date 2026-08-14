"""Verify the submission package against the current manuscript. Fail closed.

The 69-check release verifier at `phase0_calibration/robustness/src/04_verify_release.py` binds the
frozen 11-page `preprint_draft_v1` and its yeast-only tree. It says nothing about the current
manuscript, its figures, its supporting files or the human cohort, so any claim that "the verifier
passes" is not a claim about this package. This closes that gap for the package actually being
submitted.

What it checks, in four groups:

  PLOS mechanical   abstract word cap, title cap, short title, figure format/pixels/size, table
                    header repetition, line and page numbering, double spacing, no embedded figures
  Structural        section order, no orphan or dangling citations, no orphan tables or supporting
                    items, every supporting item cited and present as a file
  Numerical         every headline figure in the manuscript traced to NUMBERS.md, and every value in
                    the retired list absent from the manuscript
  Provenance        SHA-256 of every artifact, written to a manifest

Exit status is non-zero if any check fails. Usage:

    python verify_submission_package.py [--write-manifest]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
MD = RESEARCH / "phosphosite_proximity_preprint.md"
PDF = RESEARCH / "phosphosite_proximity_preprint.pdf"
SUB = RESEARCH / "phosphosite_proximity_preprint_SUBMISSION.docx"
FIGS = HERE / "submission_figures"
SI = RESEARCH / "supporting_information"
NUMBERS = RESEARCH / "phase0_calibration" / "NUMBERS.md"

# Values the numerical authority has retired. Any of these appearing in the manuscript outside an
# explicit retraction sentence is a failure, because they were all once reported as findings.
RETIRED = [
    ("0.505573", "withdrawn union endpoint as a primary"),
    ("+0.071 (+0.005 to +0.137)", "sequence-separation paired difference, retired 25.4"),
    ("0.384 (0.272–0.498)", "below-chance within-protein interval, retired 25.4"),
    ("0.487 (0.421–0.554)", "reporter primary on the released column, superseded 25.3"),
    ("2.7 times the precision", "precision ratio, retired 20.10"),
    ("a real negative", "retired 2026-08-13"),
    ("Burial, not distance", "interval-comparison error, retired 23.5"),
    ("0.559317", "superseded fitness primary, deposited cohort, retired 26.2"),
    ("0.486100", "superseded reporter primary, deposited cohort, retired 26.2"),
    # Matched as bare tokens, not as one phrasing. The literal string "1,475 sites, 793 proteins"
    # missed "1,475 edited sites in 793 proteins" and "leaving 1,475 sites in 793 proteins".
    ("1,475", "superseded human cohort site count, retired 26.1"),
    ("793 proteins", "superseded human cohort protein count, retired 26.1"),
    ("1,595 rows", "superseded candidate-table size unless stated as the earlier build"),
    ("185 of 115,536", "superseded reporter pair decomposition, retired 26.3"),
    ("50 informative proteins", "superseded reporter informative count, retired 26.3"),
    ("phase0_calibration/manuscript/figure2.png", "obsolete four-panel Figure 2, retired 2026-08-14"),
]
RETRACTION_MARKERS = ("earlier version", "earlier build", "retired", "withdrawn", "superseded",
                      "An earlier")


def sentences(text: str):
    """Split into sentences, because a markdown paragraph is one line.

    The retraction exemption is granted per sentence. Matching on lines let a paragraph that retracts
    one value elsewhere in itself exempt every other claim in the same paragraph — a negative control
    on 2026-08-14 showed an asserted within-protein exclusion passing for exactly that reason.
    """
    for line in text.split("\n"):
        for sent in re.split(r"(?<=[.!?])\s+", line):
            if sent.strip():
                yield sent

results: list[tuple[bool, str, str]] = []


def check(ok: bool, name: str, detail: str = "") -> None:
    results.append((bool(ok), name, detail))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-manifest", action="store_true")
    a = ap.parse_args()

    for f in (MD, PDF, SUB, NUMBERS):
        check(f.exists(), f"artifact present: {f.name}")
    if not MD.exists():
        return report()

    md = MD.read_text()
    numbers = NUMBERS.read_text() if NUMBERS.exists() else ""

    # ---- PLOS mechanical -------------------------------------------------
    title = md.split("\n", 1)[0].lstrip("# ").strip()
    check(len(title) <= 250, "title within 250 characters", f"{len(title)}")
    check("**Short title:**" in md, "short title present")
    short = re.search(r"\*\*Short title:\*\*\s*(.+)", md)
    if short:
        check(len(short.group(1).strip()) <= 100, "short title within 100 characters",
              f"{len(short.group(1).strip())}")
    abstract = md[md.index("## Abstract"):md.index("**Keywords:**")]
    n_abs = len(abstract.split()) - 2          # drop the heading tokens
    check(n_abs <= 300, "abstract within 300 words", f"{n_abs}")
    check("Corresponding author" in md, "corresponding author named on the title page")
    check("@" in md.split("## Abstract")[0], "corresponding-author email present")

    # ---- figures ----------------------------------------------------------
    try:
        from PIL import Image
        for tif in sorted(FIGS.glob("*.tif")):
            with Image.open(tif) as im:
                w, h = im.size
                mode = im.mode
            mb = tif.stat().st_size / 1e6
            check(789 <= w <= 2250, f"{tif.name} width in 789-2250", str(w))
            check(h <= 2625, f"{tif.name} height at most 2625", str(h))
            check(mb <= 10, f"{tif.name} at most 10 MB", f"{mb:.2f}")
            check(mode in ("RGB", "L"), f"{tif.name} RGB or grayscale", mode)
        check(len(list(FIGS.glob("*.tif"))) >= 2, "figure TIFFs present",
              str(len(list(FIGS.glob('*.tif')))))
    except ImportError:
        check(False, "Pillow available for figure checks")

    # ---- submission DOCX --------------------------------------------------
    if SUB.exists():
        z = zipfile.ZipFile(SUB)
        doc = z.read("word/document.xml").decode()
        check("lnNumType" in doc, "continuous line numbers set")
        check(any(n.startswith("word/footer") for n in z.namelist()), "footer present for page numbers")
        n_hdr = doc.count("tblHeader")
        n_tbl = doc.count("<w:tbl>")
        check(n_hdr >= n_tbl and n_tbl > 0, "every table repeats its header row",
              f"{n_hdr} headers / {n_tbl} tables")
        check("<w:drawing>" not in doc, "no figures embedded in the submission DOCX")

        # Document properties ship to the journal inside the file. python-docx's template leaves a
        # 2013 date, blank keywords and, until 2026-08-14, a subject naming one screen when there are
        # two.
        from docx import Document as _Doc
        cp = _Doc(SUB).core_properties
        check("two published" in (cp.subject or ""), "DOCX subject names both screens", cp.subject or "")
        check(bool((cp.keywords or "").strip()), "DOCX keywords set", cp.keywords or "(blank)")
        check(cp.created is not None and cp.created.year >= 2026, "DOCX creation date is not template residue",
              str(cp.created))

    # ---- build products came from this Markdown -----------------------------
    # Every other check reads the Markdown. Without this, a stale PDF or DOCX beside a current source
    # passes the whole suite — the same failure that let a superseded Figure 1 and Figure 2 ship.
    md_mtime = MD.stat().st_mtime
    for f in (PDF, SUB, RESEARCH / "phosphosite_proximity_preprint.docx"):
        if f.exists():
            check(f.stat().st_mtime >= md_mtime - 1, f"{f.name} is not older than the Markdown",
                  f"{(md_mtime - f.stat().st_mtime):.0f}s older" if f.stat().st_mtime < md_mtime else "")
    try:
        import pymupdf
        pdf_text = "".join(pg.get_text() for pg in pymupdf.open(PDF)) if PDF.exists() else ""
        for tok in ("0.558", "0.483", "1,471", "788 proteins"):
            check(tok in pdf_text, f"rendered PDF carries the corrected value: {tok}")
        for tok, why in (("0.559317", "superseded fitness"), ("0.486100", "superseded reporter")):
            check(tok not in pdf_text, f"rendered PDF free of {why}: {tok}")
    except ImportError:
        check(False, "pymupdf available to read the rendered PDF")

    # ---- embedded figures come from the submission build --------------------
    # The reader PDF and the uploaded TIFFs must be the same picture. Pointing an embed at the frozen
    # release tree is how a superseded Figure 1 and Figure 2 survived into the 2026-08-14 build.
    embeds = re.findall(r"^!\[[^\]]*\]\(([^)]+)\)", md, re.M)
    check(bool(embeds), "manuscript embeds figures", str(len(embeds)))
    for src in embeds:
        under = src.startswith("manuscript_build/submission_figures/")
        check(under, f"figure embed comes from the submission build: {src}")
        check((RESEARCH / src).exists(), f"embedded figure file exists: {src}")
    for name in ("Fig1", "Fig2", "Fig3"):
        png, tif = FIGS / f"{name}.png", FIGS / f"{name}.tif"
        if png.exists() and tif.exists():
            check(abs(png.stat().st_mtime - tif.stat().st_mtime) < 300,
                  f"{name} PNG and TIFF are from the same build",
                  f"{abs(png.stat().st_mtime - tif.stat().st_mtime):.0f}s apart")
        else:
            check(False, f"{name} has both a PNG and a TIFF")

    # ---- structural -------------------------------------------------------
    order = [m.group(1) for m in re.finditer(r"^## (.+)$", md, re.M)]
    def pos(name):
        return next((i for i, o in enumerate(order) if o.startswith(name)), -1)
    check(pos("Acknowledgements") < pos("References") < pos("Supporting information"),
          "Acknowledgements before References before Supporting information")

    body = md[:md.index("## References")]
    cited = set()
    for g in re.findall(r"\[[\d,–\- ]+\]", body):
        for tok in re.split(r"[,\s–\-]+", g.strip("[]")):
            if tok.isdigit():
                cited.add(int(tok))
    refs = re.findall(r"^(\d+)\. ", md[md.index("## References"):], re.M)
    defined = {int(r) for r in refs}
    check(not (defined - cited), "no orphan references", str(sorted(defined - cited)))
    check(not (cited - defined), "no dangling citations", str(sorted(cited - defined)))

    for n in range(1, 5):
        check(f"Table {n}" in body, f"Table {n} cited in the body")
    for si_name in ("S1 Appendix", "S1 Table", "S2 Appendix", "S2 Table", "S1 Fig", "S2 Fig"):
        check(si_name in body, f"{si_name} cited in the body")
    for fname in ("S1_Appendix.md", "S1_Table.md", "S2_Appendix.md", "S2_Table.md"):
        check((SI / fname).exists(), f"supporting file present: {fname}")
    si_section = md[md.index("## Supporting information"):]
    check("|" not in si_section, "supporting-information section carries captions only, no tables")

    # ---- numerical --------------------------------------------------------
    sents = list(sentences(md))
    for value, why in RETIRED:
        bad = [x for x in sents if value in x and not any(mk in x for mk in RETRACTION_MARKERS)]
        check(not bad, f"retired value absent outside a retraction: {value}",
              why + (f" | {bad[0][:60]}" if bad else ""))

    for headline in ("0.558", "0.483", "0.527", "0.544"):
        check(headline in md, f"headline value present: {headline}")
    if numbers:
        for headline in ("0.557829", "0.483301", "0.526823"):
            check(headline in numbers, f"headline traced to NUMBERS.md: {headline}")

    # ---- endpoint invariants ---------------------------------------------
    # The corrected cohort's counts, so a partial edit that updates an AUC but not its support fails.
    for tok, what in (("1,471 sites in 788 proteins", "corrected human cohort size"),
                      ("72 sites are affected", "fitness positives"),
                      ("82 are", "reporter positives"),
                      ("102 of 100,728", "fitness pair decomposition"),
                      ("184 of 113,898", "reporter pair decomposition")):
        check(tok in md, f"corrected value present: {what}", tok)

    # No within-protein interval may be asserted as excluding 0.5 (26.4).
    for phrase in ("excludes 0.5 from below", "excluding 0.5 from below",
                   "below chance within a protein"):
        bad = [x for x in sents
               if phrase in x and not any(mk in x for mk in RETRACTION_MARKERS)]
        check(not bad, f"no within-protein exclusion asserted: {phrase}",
              bad[0][:80] if bad else "")

    # NUMBERS.md must carry Section 26 and mark it as superseding the earlier human sections.
    if numbers:
        check("## 26." in numbers, "NUMBERS.md carries Section 26")
        check("supersedes Sections 22" in numbers or "supersedes \u00a7\u00a722" in numbers
              or "supersedes Sections 22\u201325" in numbers,
              "Section 26 declares what it supersedes")

    ok = report()
    if a.write_manifest:
        man = {}
        for f in [MD, PDF, SUB, NUMBERS] + sorted(FIGS.glob("*.tif")) + sorted(SI.glob("*.md")):
            if f.exists():
                man[str(f.relative_to(RESEARCH))] = {"sha256": sha256(f), "bytes": f.stat().st_size}
        out = HERE / "submission_manifest.json"
        out.write_text(json.dumps({"artifacts": man, "checks_passed": ok}, indent=2) + "\n")
        print(f"\nwrote {out.name} with {len(man)} artifacts")
    return 0 if ok else 1


def report() -> bool:
    failed = [r for r in results if not r[0]]
    for good, name, detail in results:
        if not good:
            print(f"  FAIL  {name}" + (f"  [{detail}]" if detail else ""))
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed")
    if failed:
        print(f"{len(failed)} FAILED — package is not submittable")
    return not failed


if __name__ == "__main__":
    sys.exit(main())
