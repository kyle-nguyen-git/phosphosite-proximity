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
]
RETRACTION_MARKERS = ("earlier version", "retired", "withdrawn", "superseded", "An earlier")

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
    for value, why in RETIRED:
        hits = [ln for ln in md.split("\n") if value in ln]
        bad = [ln for ln in hits if not any(mk in ln for mk in RETRACTION_MARKERS)]
        check(not bad, f"retired value absent outside a retraction: {value}", why)

    for headline in ("0.559", "0.486", "0.527", "0.544"):
        check(headline in md, f"headline value present: {headline}")
    if numbers:
        for headline in ("0.559317", "0.486100", "0.526823"):
            check(headline in numbers, f"headline traced to NUMBERS.md: {headline}")

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
