"""
Fetch AlphaFold models for the analysis-set proteins and compute, for each phosphosite:
  - minimum heavy-atom distance to the nearest UniProt ACT_SITE / BINDING residue
  - pLDDT at the site (AlphaFold model-local confidence)
  - relative solvent accessibility (Shrake-Rupley, normalised by Tien et al. 2013 theoretical maxima)

Inputs : results/analysis_set.csv, results/uniprot_features_core.csv
Outputs: data/af/*.cif, results/structural_features.csv

The public release pins AlphaFold DB v6 URLs and file hashes in the third-party manifest.
"""
import csv
import hashlib
import json
import os
import time
import warnings
import pandas as pd, numpy as np, requests
from Bio.PDB import MMCIFParser, ShrakeRupley
from Bio.PDB.Polypeptide import protein_letters_3to1

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFDIR = os.path.join(HERE, "data", "af")
PAE_META_DIR = os.path.join(HERE, "phase0_5", "data", "pae")
THIRD_PARTY_MANIFEST = os.path.join(
    HERE, "release_metadata", "third_party_data_manifest.csv"
)
os.makedirs(AFDIR, exist_ok=True)

# Tien et al. 2013, theoretical maximum accessible surface area (A^2), Gly-X-Gly
MAXASA = {
    "A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104,
    "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155,
    "T": 172, "W": 285, "Y": 263, "V": 174,
}


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expected_cache_hash(relative_path: str) -> str:
    with open(THIRD_PARTY_MANIFEST, newline="") as handle:
        rows = {row["path"]: row for row in csv.DictReader(handle)}
    if relative_path not in rows:
        raise RuntimeError(f"cache path missing from third-party manifest: {relative_path}")
    return rows[relative_path]["sha256"]


def fetch_model(acc: str) -> str:
    """Use or retrieve the checksum-pinned AlphaFold DB v6 mmCIF."""
    dest = os.path.join(AFDIR, f"{acc}.cif")
    relative = os.path.relpath(dest, HERE)
    expected = expected_cache_hash(relative)
    if os.path.exists(dest) and sha256(dest) == expected:
        return dest
    metadata_path = os.path.join(PAE_META_DIR, f"{acc}_metadata.json")
    if not os.path.isfile(metadata_path):
        raise RuntimeError(f"pinned AlphaFold metadata missing for {acc}")
    with open(metadata_path) as handle:
        metadata = json.load(handle)
    if int(metadata.get("latestVersion", -1)) != 6 or metadata.get("isComplex"):
        raise RuntimeError(f"unexpected AlphaFold model contract for {acc}")
    url = metadata.get("cifUrl", "")
    if not url.endswith("model_v6.cif"):
        raise RuntimeError(f"AlphaFold URL is not pinned to v6 for {acc}")
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    temporary = dest + ".part"
    with open(temporary, "wb") as handle:
        handle.write(response.content)
    if sha256(temporary) != expected:
        os.unlink(temporary)
        raise RuntimeError(f"downloaded AlphaFold hash mismatch for {acc}")
    os.replace(temporary, dest)
    return dest


def residue_atoms(structure):
    """Map residue seq id -> (one-letter code, list of heavy atoms, mean B-factor=pLDDT)."""
    out = {}
    for res in structure[0].get_residues():
        if res.id[0] != " ":
            continue
        heavy = [a for a in res if a.element != "H"]
        if not heavy:
            continue
        try:
            aa = protein_letters_3to1[res.get_resname()]
        except KeyError:
            continue
        out[res.id[1]] = (aa, heavy, float(np.mean([a.get_bfactor() for a in heavy])))
    return out


def main():
    sites = pd.read_csv(os.path.join(HERE, "results", "analysis_set.csv"))
    feats = pd.read_csv(os.path.join(HERE, "results", "uniprot_features_core.csv"))
    proteome = pd.read_csv(os.path.join(HERE, "data", "yeast_sgd_uniprot.tsv"), sep="\t")
    proteome.columns = ["acc", "entry", "oln", "gene", "pname", "seq", "length"]
    expected_sequences = dict(zip(proteome.acc.astype(str), proteome.seq.astype(str)))
    feat_by_acc = feats.groupby("acc")["feat_pos"].apply(lambda s: sorted(set(s))).to_dict()

    parser = MMCIFParser(QUIET=True)
    sr = ShrakeRupley()
    rows = []

    for acc, grp in sites.groupby("acc"):
        path = fetch_model(acc)
        struct = parser.get_structure(acc, path)
        res = residue_atoms(struct)
        positions = sorted(res)
        observed_sequence = "".join(res[position][0] for position in positions)
        expected_sequence = expected_sequences.get(str(acc))
        if (
            expected_sequence is None
            or positions != list(range(1, len(expected_sequence) + 1))
            or observed_sequence != expected_sequence
        ):
            raise RuntimeError(f"full AlphaFold/UniProt sequence or numbering mismatch for {acc}")

        # solvent accessibility on the whole chain, once
        try:
            sr.compute(struct[0], level="R")
            sasa_ok = True
        except Exception:
            sasa_ok = False

        targets = [p for p in feat_by_acc.get(acc, []) if p in res]
        for _, r in grp.iterrows():
            pos = int(r["pos"])
            if pos not in res:
                continue
            aa, atoms, plddt = res[pos]
            if aa != r["pmt_aa_wt"]:
                raise RuntimeError(f"substituted-residue mismatch in AlphaFold model for {acc}:{pos}")

            dmin, nearest = np.nan, np.nan
            if targets:
                if pos in targets:
                    # Exact overlap is a valid observation under the declared
                    # nearest-residue estimand; its distance is 0 Å.
                    dmin, nearest = 0.0, pos
                else:
                    best = np.inf
                    for t in targets:
                        for a1 in atoms:
                            for a2 in res[t][1]:
                                d = a1 - a2
                                if d < best:
                                    best, nearest = d, t
                    if np.isfinite(best):
                        dmin = best

            rsa = np.nan
            if sasa_ok:
                try:
                    sasa = sum(a.sasa for a in atoms if hasattr(a, "sasa"))
                    rsa = sasa / MAXASA.get(aa, np.nan)
                except Exception:
                    pass

            rows.append({
                "acc": acc, "pos": pos, "aa": aa,
                "min_dist_A": dmin, "nearest_feat_pos": nearest,
                "plddt": plddt, "rsa": rsa,
                "n_annot_residues": len(targets),
            })

        time.sleep(0.1)

    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "results", "structural_features.csv"), index=False)
    print(f"structures verified: {sites.acc.nunique()}/{sites.acc.nunique()}")
    print(f"sites with structure: {len(out)} across {out.acc.nunique()} proteins")
    print(f"sites with a distance: {out.min_dist_A.notna().sum()}")
    print(out[["min_dist_A", "plddt", "rsa"]].describe().round(2).to_string())


if __name__ == "__main__":
    main()
