"""Build the Kennedy 2024 human cohort with the same predictor as the yeast analysis.

Distance is the minimum heavy-atom separation between the edited residue and the nearest
residue UniProt annotates as ACT_SITE or BINDING, in an AlphaFold DB monomer model. That is
the definition used in phase0_calibration/src/02_structures.py and it is not re-derived here.

Resumable: UniProt features and AlphaFold models are cached on disk and skipped if present. Offline
mode fails closed on missing UniProt inputs, uses only cached AlphaFold models, and asserts that every
parsed model sequence and residue number agrees with the cached reviewed UniProt sequence.
"""
import argparse
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
AF = os.path.join(CACHE, "af")
FEAT = os.path.join(CACHE, "uniprot")
AF_MANIFEST = os.path.join(CACHE, "af_v6_manifest.csv")
for d in (CACHE, AF, FEAT):
    os.makedirs(d, exist_ok=True)

COHORT = os.path.join(
    HERE, "kennedy2024_cohort_candidate.rebuilt.csv"
)
FEATURE_TYPES = {"Active site", "Binding site"}


def uniprot_features(acc, offline=False):
    """Expanded ACT_SITE/BINDING residue positions, with evidence codes, for one accession."""
    path = os.path.join(FEAT, f"{acc}.json")
    if not os.path.exists(path):
        if offline:
            raise FileNotFoundError(f"offline UniProt cache missing for {acc}")
        url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(path, "w") as fh:
            fh.write(r.text)
        time.sleep(0.12)
    entry = json.load(open(path))
    rows = []
    for f in entry.get("features", []):
        if f.get("type") not in FEATURE_TYPES:
            continue
        loc = f.get("location", {})
        try:
            start = int(loc["start"]["value"])
            end = int(loc["end"]["value"])
        except (KeyError, TypeError):
            continue
        codes = ";".join(sorted({e.get("evidenceCode", "") for e in f.get("evidences", [])}))
        for p in range(start, end + 1):
            rows.append({"acc": acc, "res": p, "feat_type": f["type"], "evidence": codes})
    return rows, entry.get("sequence", {}).get("value", "")


def alphafold_model(acc, offline=False):
    """Cache the AlphaFold DB monomer mmCIF for one accession. Returns path or None."""
    dest = os.path.join(AF, f"{acc}.cif")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return dest
    if offline:
        return None
    meta = requests.get(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}", timeout=90)
    if meta.status_code != 200:
        return None
    payload = meta.json()
    if not payload:
        return None
    url = payload[0].get("cifUrl")
    if not url:
        return None
    r = requests.get(url, timeout=180)
    if r.status_code != 200:
        return None
    tmp = dest + ".part"
    with open(tmp, "wb") as fh:
        fh.write(r.content)
    os.replace(tmp, dest)
    time.sleep(0.05)
    return dest


def main():
    from Bio.PDB import MMCIFParser, ShrakeRupley
    from Bio.Data.IUPACData import protein_letters_3to1_extended as three_to_one

    ap = argparse.ArgumentParser()
    ap.add_argument("--cohort", default=COHORT, help="candidate table to build from")
    ap.add_argument("--out", default=os.path.join(HERE, "kennedy_analysis.csv"))
    ap.add_argument("--targets-out", default=os.path.join(HERE, "uniprot_targets.csv"))
    ap.add_argument("--deadline", type=int, default=0,
                    help="stop after N seconds and checkpoint; rerun to continue")
    ap.add_argument("--offline", action="store_true",
                    help="forbid downloads and rebuild only from the pinned local cache")
    args = ap.parse_args()
    started = time.time()

    # Per-protein results are appended to a checkpoint so a run that stops partway can be resumed.
    # The Shrake-Rupley pass over 800 structures does not fit in one short session.
    ckpt = args.out + ".partial.jsonl"
    done_accs = set()
    if os.path.exists(ckpt):
        for line in open(ckpt):
            try:
                done_accs.add(json.loads(line)["acc"])
            except Exception:
                pass
        print(f"resuming: {len(done_accs)} proteins already done", flush=True)

    cohort = pd.read_csv(args.cohort)
    accs = sorted(cohort.acc.unique())
    print(f"cohort: {len(cohort)} sites, {len(accs)} proteins", flush=True)
    if args.offline:
        af_meta = pd.read_csv(AF_MANIFEST).set_index("accession")
    else:
        af_meta = None

    # ---- UniProt features -------------------------------------------------
    targets, seqs = {}, {}
    for i, acc in enumerate(accs, 1):
        try:
            rows, seq = uniprot_features(acc, args.offline)
        except Exception as exc:  # network or malformed entry
            print(f"  uniprot FAIL {acc}: {exc}", flush=True)
            continue
        targets[acc] = rows
        seqs[acc] = seq
        if i % 100 == 0:
            print(f"  uniprot {i}/{len(accs)}", flush=True)
    feat = pd.DataFrame([r for v in targets.values() for r in v])
    feat.to_csv(args.targets_out, index=False)
    print(f"target residues: {len(feat)} over {feat.acc.nunique()} proteins", flush=True)

    # ---- AlphaFold models -------------------------------------------------
    have = 0
    for i, acc in enumerate(accs, 1):
        if alphafold_model(acc, args.offline):
            have += 1
        if i % 50 == 0:
            print(f"  alphafold {i}/{len(accs)} (cached {have})", flush=True)
    print(f"models available: {have}/{len(accs)}", flush=True)

    # ---- distances --------------------------------------------------------
    parser = MMCIFParser(QUIET=True)
    sr = ShrakeRupley()
    MAXASA = {  # Tien et al. 2013 theoretical, as used by the yeast pipeline
        "A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225,
        "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240,
        "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174,
    }
    out = []
    by_acc = {a: g for a, g in cohort.groupby("acc")}
    ck = open(ckpt, "a")
    for i, (acc, sites) in enumerate(by_acc.items(), 1):
        if acc in done_accs:
            continue
        if args.deadline and time.time() - started > args.deadline:
            print(f"deadline reached at protein {i}/{len(by_acc)}; rerun to continue", flush=True)
            break
        path = os.path.join(AF, f"{acc}.cif")
        tgt = sorted({r["res"] for r in targets.get(acc, [])})
        exp_tgt = sorted({r["res"] for r in targets.get(acc, [])
                          if "ECO:0000269" in r["evidence"] or "ECO:0007744" in r["evidence"]})
        # A protein with no model or no annotated target contributes no rows, but it still has to be
        # marked done or a resumed run will retry it forever and never reach the end.
        if not os.path.exists(path) or not tgt:
            ck.write(json.dumps({"acc": acc, "_skipped": "no_model_or_no_target"}) + "\n")
            ck.flush(); done_accs.add(acc)
            continue
        try:
            structure = parser.get_structure(acc, path)
        except Exception:
            ck.write(json.dumps({"acc": acc, "_skipped": "unparsable_model"}) + "\n")
            ck.flush(); done_accs.add(acc)
            continue
        res = {}
        for r in structure[0].get_residues():
            if r.id[0] != " ":
                continue
            heavy = [a for a in r if a.element != "H"]
            if not heavy:
                continue
            try:
                aa1 = three_to_one[r.get_resname().capitalize()]
            except KeyError:
                continue
            res[r.id[1]] = (aa1, heavy, float(np.mean([a.get_bfactor() for a in heavy])))
        positions = sorted(res)
        if af_meta is None or acc not in af_meta.index:
            raise RuntimeError(f"AlphaFold provenance metadata missing for {acc}")
        meta = af_meta.loc[acc]
        if not bool(meta.exact_canonical_entry) or int(meta.latest_version) != 6:
            raise RuntimeError(f"AlphaFold canonical/version assertion failed for {acc}")
        model_reference = str(meta.model_sequence)
        if positions != list(range(1, len(model_reference) + 1)):
            raise RuntimeError(f"model numbering/length mismatch for {acc}")
        model_seq = "".join(res[p][0] for p in positions)
        if model_seq != model_reference:
            raise RuntimeError(f"model sequence does not match pinned AFDB metadata for {acc}")
        try:
            sr.compute(structure[0], level="A")
            sasa_ok = True
        except Exception:
            sasa_ok = False
        for row in sites.itertuples():
            if row.pos not in res:
                continue
            aa1, atoms, plddt = res[row.pos]
            if aa1 != row.aa:
                continue  # numbering mismatch against the model
            def nearest(cands):
                best, at = np.inf, np.nan
                for t in cands:
                    if t not in res or t == row.pos:
                        continue
                    for a1 in atoms:
                        for a2 in res[t][1]:
                            d = a1 - a2
                            if d < best:
                                best, at = d, t
                return (best, at) if np.isfinite(best) else (np.nan, np.nan)
            dmin, near = nearest(tgt)
            dexp, _ = nearest(exp_tgt)
            rsa = np.nan
            if sasa_ok:
                try:
                    rsa = sum(a.sasa for a in atoms if hasattr(a, "sasa")) / MAXASA.get(aa1, np.nan)
                except Exception:
                    pass
            out.append({
                "acc": acc, "gene": row.gene, "pos": row.pos, "aa": row.aa,
                "min_dist_A": dmin, "nearest_feat_pos": near,
                "min_dist_exp_A": dexp,
                "plddt": plddt, "rsa": rsa,
                "n_annot_residues": len(tgt), "n_annot_exp": len(exp_tgt),
                "l3": row.l3, "p3": row.p3, "f3": row.f3,
                "l4": row.l4, "p4": row.p4, "f4": row.f4,
            })
        produced = [r for r in out if r["acc"] == acc]
        if not produced:
            # Structure parsed and targets exist, but every site failed the model-numbering or
            # residue-identity check. Still a completed protein.
            ck.write(json.dumps({"acc": acc, "_skipped": "no_site_matched_model"}) + "\n")
            ck.flush(); done_accs.add(acc)
            continue
        for rec in produced:
            # numpy scalars from Bio.PDB do not serialise; the checkpoint stores plain floats
            clean = {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v)
                     for k, v in rec.items()}
            ck.write(json.dumps(clean) + "\n")
        ck.flush()
        done_accs.add(acc)
        if i % 50 == 0:
            print(f"  distances {i}/{len(by_acc)} ({len(out)} sites)", flush=True)
    ck.close()

    recs = [json.loads(l) for l in open(ckpt)] if os.path.exists(ckpt) else []
    seen = {r["acc"] for r in recs}
    skipped = sorted({r["acc"] for r in recs if r.get("_skipped")})
    rows = [r for r in recs if not r.get("_skipped")]
    df = pd.DataFrame(rows).drop_duplicates(subset=["acc", "pos"])
    remaining = set(by_acc) - seen
    if skipped:
        print(f"{len(skipped)} proteins contributed no rows (no model or no annotated target)", flush=True)
    if remaining:
        print(f"INCOMPLETE: {len(remaining)} proteins still to do; rerun", flush=True)
        return 1
    df = df.sort_values(["gene", "pos"]).reset_index(drop=True)
    df.to_csv(args.out, index=False)
    print(f"\nwrote {os.path.basename(args.out)}: {len(df)} sites, {df.acc.nunique()} proteins", flush=True)
    print(df[["min_dist_A", "plddt", "rsa"]].describe().round(2).to_string(), flush=True)


if __name__ == "__main__":
    sys.exit(main() or 0)
