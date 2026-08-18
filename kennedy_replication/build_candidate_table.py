"""Generate the human candidate table from the Kennedy supplement. The missing first step.

Both format reviews found that the human cohort cannot be rebuilt end to end because
`second_dataset_scan/kennedy2024_cohort_candidate.csv` — the table `build_cohort.py` starts from — had
no deposited generator. This is that generator. The current output is the corrected candidate table;
the earlier deposited 1,595-row table is retained only for provenance.

The cascade it implements, with the counts recorded in `NUMBERS.md` Section 22.4:

    7,425  rows in Supplementary Table 3's Phosphosites sheet
    6,968  with a parsable serine, threonine or tyrosine position
    6,907  whose gene symbol maps to exactly one reviewed human UniProt entry
    6,113  whose residue matches the canonical sequence at that position
    1,590  in 812 proteins carrying at least one eligible ACT_SITE or BINDING residue

Gene-symbol resolution is the step that needs the network: UniProt is queried for the reviewed human
entry of each symbol, and results are cached under `cache/genemap.json` so a rerun is offline. The
per-accession entry JSON and the sequence both come from `cache/uniprot/`, which `build_cohort.py`
already populates.

The script reports its overlap with the superseded deposited table. Exact reproducibility of the
current output is enforced by `verify_human_rebuild.py`, which runs this generator offline and compares
every row and column with the current 1,590-row candidate table.

Usage:
    python build_candidate_table.py [--out kennedy2024_cohort_candidate.rebuilt.csv]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
XL = os.path.join(HERE, "cache", "kennedy_supplement.xlsx")
UNIPROT = os.path.join(HERE, "cache", "uniprot")
UNIPROT_ANNOT = os.path.join(HERE, "cache", "uniprot_annot")   # sequence + act/binding for the rest
GENEMAP = os.path.join(HERE, "cache", "genemap.json")
DEPOSITED = os.path.join(RESEARCH, "second_dataset_scan", "kennedy2024_cohort_candidate.csv")

SITE = re.compile(r"^(.+?)_([STY])(\d+)$")
FEATURE_TYPES = {"Active site", "Binding site"}
EXPERIMENTAL = {"ECO:0000269", "ECO:0007744"}


SCREENS_CACHE = os.path.join(HERE, "cache", "screens_parsed.csv")


def load_screens() -> pd.DataFrame:
    """Both Phosphosites sheets, joined on the site identifier.

    The workbook takes over a minute to open, so the merged result is cached as CSV. Delete
    `cache/screens_parsed.csv` to force a re-read from the .xlsx.
    """
    if os.path.exists(SCREENS_CACHE):
        return pd.read_csv(SCREENS_CACHE)
    keep = ["Phosphosite", "GeneSymbol", "number of sgRNA",
            "Post/Pre- edits (Log2FoldChange)", "p-value", "FDR"]
    a = pd.read_excel(XL, sheet_name="SuppTable 3 Phosphosites")[keep]
    a.columns = ["site", "gene", "nsg", "l3", "p3", "f3"]
    b = pd.read_excel(XL, sheet_name="SuppTable 4 Phosphosites")
    bcol = [c for c in b.columns if "Log2" in str(c)][0]
    b = b[["Phosphosite", bcol, "p-value", "FDR"]]
    b.columns = ["site", "l4", "p4", "f4"]
    merged = a.merge(b, on="site", how="left")
    merged.to_csv(SCREENS_CACHE, index=False)
    return merged


def parse_sites(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in df.itertuples():
        m = SITE.match(str(r.site))
        if not m:
            continue
        rows.append({"site": r.site, "gene": r.gene, "aa": m.group(2), "pos": int(m.group(3)),
                     "nsg": r.nsg, "l3": r.l3, "p3": r.p3, "f3": r.f3,
                     "l4": r.l4, "p4": r.p4, "f4": r.f4})
    return pd.DataFrame(rows)


def resolve_genes(symbols, max_lookups: int = 0, offline: bool = False) -> dict:
    """Gene symbol -> reviewed human accession. Cached, so a rerun needs no network."""
    cache = json.load(open(GENEMAP)) if os.path.exists(GENEMAP) else {}
    todo = [s for s in symbols if s not in cache]
    if todo and offline:
        raise RuntimeError(f"offline cache is incomplete: {len(todo)} gene symbols are unresolved")
    if todo:
        import requests
        print(f"  resolving {len(todo)} gene symbols against UniProt", flush=True)
        for i, sym in enumerate(todo, 1):
            url = ("https://rest.uniprot.org/uniprotkb/search"
                   f"?query=gene_exact:{sym}+AND+organism_id:9606+AND+reviewed:true"
                   "&fields=accession&format=json&size=2")
            try:
                r = requests.get(url, timeout=60)
                hits = r.json().get("results", []) if r.status_code == 200 else []
            except Exception:
                hits = []
            # one reviewed entry only; an ambiguous symbol is dropped rather than guessed
            cache[sym] = hits[0]["primaryAccession"] if len(hits) == 1 else None
            if i % 200 == 0:
                json.dump(cache, open(GENEMAP, "w"))
                print(f"    {i}/{len(todo)}", flush=True)
            time.sleep(0.1)
        json.dump(cache, open(GENEMAP, "w"))
    return cache


def entry(acc):
    """The UniProt entry for an accession, from either cache.

    `cache/uniprot/` holds the 818 proteins the original build kept, so testing only against it would
    make the cohort reproduce by construction: any protein the original dropped has no file and is
    dropped again without being examined. `cache/uniprot_annot/` holds every other mapped accession
    with the two fields the annotation filter reads, so the filter is now actually applied.
    """
    for base in (UNIPROT, UNIPROT_ANNOT):
        p = os.path.join(base, f"{acc}.json")
        if os.path.exists(p):
            return json.load(open(p))
    return None


def eligible_counts(e):
    """Expanded ACT_SITE/BINDING residues, all evidence and experimental only."""
    allres, expres = set(), set()
    for f in e.get("features", []):
        if f.get("type") not in FEATURE_TYPES:
            continue
        loc = f.get("location", {})
        try:
            a, b = int(loc["start"]["value"]), int(loc["end"]["value"])
        except (KeyError, TypeError):
            continue
        codes = {ev.get("evidenceCode", "") for ev in f.get("evidences", [])}
        for r in range(a, b + 1):
            allres.add(r)
            if codes & EXPERIMENTAL:
                expres.add(r)
    return len(allres), len(expres)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-lookups", type=int, default=0,
                    help="resolve at most N new gene symbols then continue; 0 means all")
    ap.add_argument("--offline", action="store_true",
                    help="forbid network access and fail if a required cache entry is missing")
    ap.add_argument("--out", default=os.path.join(HERE, "kennedy2024_cohort_candidate.rebuilt.csv"))
    a = ap.parse_args()

    raw = load_screens()
    print(f"  {len(raw):>6}  rows in the Phosphosites sheets")
    sites = parse_sites(raw)
    print(f"  {len(sites):>6}  with a parsable S/T/Y position")

    gmap = resolve_genes(sorted(sites.gene.astype(str).unique()), a.max_lookups, a.offline)
    unresolved = [g for g in sites.gene.astype(str).unique() if g not in gmap]
    if unresolved:
        print(f"  {len(unresolved)} symbols still unresolved; rerun to continue")
        return 2
    sites["acc"] = sites.gene.astype(str).map(gmap)
    sites = sites[sites.acc.notna()]
    print(f"  {len(sites):>6}  mapping to one reviewed human entry")

    keep, n_all, n_exp = [], [], []
    missing_entries = set()
    counts = {}
    for r in sites.itertuples():
        e = entry(r.acc)
        if e is None:
            missing_entries.add(r.acc)
            continue
        seq = e.get("sequence", {}).get("value", "")
        if not (0 < r.pos <= len(seq)) or seq[r.pos - 1] != r.aa:
            continue
        if r.acc not in counts:
            counts[r.acc] = eligible_counts(e)
        na, ne = counts[r.acc]
        keep.append(r.Index); n_all.append(na); n_exp.append(ne)
    if missing_entries:
        print(f"ERROR: {len(missing_entries)} mapped accessions lack cached UniProt JSON")
        return 3
    sites = sites.loc[keep].copy()
    sites["n_all"], sites["n_exp"] = n_all, n_exp
    print(f"  {len(sites):>6}  whose residue matches the canonical sequence")

    out = sites[sites.n_all > 0].copy()
    print(f"  {len(out):>6}  in {out.acc.nunique()} proteins with an eligible annotated residue")

    cols = ["acc", "gene", "aa", "pos", "n_all", "n_exp", "nsg", "l3", "p3", "f3", "l4", "p4", "f4"]
    out = out[cols].sort_values(["gene", "pos"]).reset_index(drop=True)
    out.to_csv(a.out, index=False)
    print(f"\nwrote {os.path.basename(a.out)}")

    # ---- does it reproduce the deposited table? --------------------------
    if not os.path.exists(DEPOSITED):
        print("deposited table not found; nothing to compare against")
        return 0
    dep = pd.read_csv(DEPOSITED).sort_values(["gene", "pos"]).reset_index(drop=True)
    key_dep = set(zip(dep.acc, dep.pos))
    key_out = set(zip(out.acc, out.pos))
    print(f"\ncomparison with the deposited table")
    print(f"  rows        superseded {len(dep)}   current {len(out)}")
    print(f"  sites only in deposited: {len(key_dep - key_out)}")
    print(f"  sites only in rebuilt  : {len(key_out - key_dep)}")
    print(f"  sites shared           : {len(key_dep & key_out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
