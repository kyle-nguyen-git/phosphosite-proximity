"""One-page summary figure for the phospho distance calibration. Outputs PDF + PNG."""
import json
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.metrics import roc_curve

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE, ORANGE = "#2a78d6", "#eb6834"          # validated pair, worst adjacent CVD dE 96.7
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8985"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "axes.edgecolor": INK3, "axes.linewidth": 0.6, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})

d = pd.read_csv(os.path.join(HERE, "results", "analysis_final.csv"))
inclusive = pd.read_csv(os.path.join(HERE, "results", "analysis_inclusive_sensitivity.csv"))
d["y"] = d.has_pheno.astype(int)
inclusive["y"] = inclusive.has_pheno.astype(int)
y, dist, plddt = d.y.values, d.min_dist_A.values, d.plddt.values

# Every headline number is READ from the committed statistics, never recomputed here.
# Recomputing is how the figure and the write-up drifted apart in the first place.
with open(os.path.join(HERE, "results", "statistics.json")) as _fh:
    STATS = json.load(_fh)
auc = STATS["auc_distance"]["auc"]
lo = STATS["auc_distance"]["ci_low"]
hi = STATS["auc_distance"]["ci_high"]
SIFT = STATS.get("sift_comparator")
SENSITIVITY = STATS["cohorts"]["include_annotation_coincident"]


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan, np.nan
    p = k / n
    den = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / den
    return p, max(0, c - h), min(1, c + h)


fig = plt.figure(figsize=(8.5, 11))
gs = GridSpec(4, 2, figure=fig, height_ratios=[0.58, 1, 1, 0.50],
              hspace=0.74, wspace=0.30, left=0.09, right=0.955, top=0.955, bottom=0.055)


def caption(ax, text):
    """Brief explanatory caption under a panel."""
    ax.text(0, -0.30, text, transform=ax.transAxes, fontsize=7.3, color=INK3,
            va="top", ha="left", wrap=True, linespacing=1.55)

# ---- header -------------------------------------------------------------
h = fig.add_subplot(gs[0, :]); h.axis("off")
h.text(0, 1.0, "Exploratory calibration of AlphaFold distance to active and binding sites\n"
               "against yeast phosphomutant growth phenotypes",
       fontsize=14.5, fontweight="bold", color=INK, va="top", linespacing=1.35)
h.text(0, 0.34, "Yeast phospho-null mutants (Viéitez et al., Nat Biotechnol 2022) mapped onto AlphaFold models. "
                "All data public.",
       fontsize=8.6, color=INK2, va="top")
h.text(0, 0.10, f"Primary AUC {auc:.3f}", fontsize=18, fontweight="bold", color=INK, va="top")
h.text(0.38, 0.085, f"95% CI [{lo:.3f}, {hi:.3f}] (protein-clustered)   ·   chance is 0.500\n"
                     f"{len(d)} sites · {d.acc.nunique()} proteins · {y.sum()} with a growth phenotype\n"
                     f"Inclusive 0 Å sensitivity: AUC {SENSITIVITY['auc_distance']['auc']:.3f} "
                     f"[{SENSITIVITY['auc_distance']['ci_low']:.3f}, {SENSITIVITY['auc_distance']['ci_high']:.3f}] "
                     f"(n={SENSITIVITY['n_sites']})",
       fontsize=8.6, color=INK2, va="top", linespacing=1.7)
h.set_xlim(0, 1); h.set_ylim(0, 1)

# ---- A: ROC -------------------------------------------------------------
ax = fig.add_subplot(gs[1, 0])
fpr, tpr, _ = roc_curve(y, -dist)
inclusive_fpr, inclusive_tpr, _ = roc_curve(
    inclusive.y.to_numpy(int), -inclusive.min_dist_A.to_numpy(float)
)
ax.plot([0, 1], [0, 1], ls=(0, (4, 3)), lw=1.2, color=INK3)
ax.plot(fpr, tpr, lw=2.2, color=BLUE, solid_capstyle="round", label="Primary exclude arm")
ax.plot(
    inclusive_fpr, inclusive_tpr, lw=1.8, color=ORANGE, ls=(0, (4, 2)),
    label="Inclusive 0 Å sensitivity",
)
ax.text(0.52, 0.16, "chance", fontsize=7.5, color=INK3, rotation=33, ha="center")
ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate")
ax.set_title("A   Distance as a classifier", fontsize=9.5, fontweight="bold", color=INK, loc="left", pad=8)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
ax.grid(alpha=0.13, lw=0.5)
ax.legend(frameon=False, fontsize=7.1, loc="lower right")
caption(ax, "Shorter distance was oriented toward a positive outcome.\nThe protein-cluster interval is reported in the header.")

# ---- B: phenotype rate by distance bin ----------------------------------
ax = fig.add_subplot(gs[1, 1])
edges = [0, 5, 10, 20, 40, np.inf]
labs = ["≤5", "5–10", "10–20", "20–40", ">40"]
xs, ps, los, his, ns = [], [], [], [], []
for i in range(len(edges) - 1):
    m = (dist > edges[i]) & (dist <= edges[i + 1]) if i else (dist <= edges[1])
    if m.sum() == 0:
        continue
    p, l, u = wilson(int(y[m].sum()), int(m.sum()))
    xs.append(i); ps.append(p); los.append(l); his.append(u); ns.append(int(m.sum()))
base = y.mean()
ax.axhline(base, color=INK3, ls=(0, (4, 3)), lw=1.2)
ax.text(len(labs) - 0.55, base + 0.028, f"overall {base:.0%}", fontsize=7.2, color=INK3, ha="right")
ax.errorbar(xs, ps, yerr=[np.array(ps) - np.array(los), np.array(his) - np.array(ps)],
            fmt="o", ms=7, lw=1.6, capsize=3.2, color=BLUE, mfc=BLUE, mec="white", mew=1.2)
for x, p, u, n in zip(xs, ps, his, ns):
    ax.text(x, u + 0.035, f"n={n}", fontsize=7, color=INK3, ha="center")
ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs)
ax.set_xlabel("Distance to nearest annotated residue (Å)")
ax.set_ylabel("Fraction with a growth phenotype")
ax.set_title("B   Descriptive rates by distance stratum", fontsize=9.5, fontweight="bold", color=INK, loc="left", pad=8)
ax.set_ylim(0, 1.02); ax.set_xlim(-0.5, len(labs) - 0.5)
ax.grid(axis="y", alpha=0.13, lw=0.5)
caption(ax, "Bins and Wilson intervals are descriptive at the substitution level;\nthe analysis was not powered around a universal cutoff.")

# ---- C: the confound ----------------------------------------------------
ax = fig.add_subplot(gs[2, 0])
for lab, col, mk in [(0, BLUE, "o"), (1, ORANGE, "^")]:
    m = y == lab
    ax.scatter(dist[m], plddt[m], s=26, c=col, marker=mk, alpha=0.72,
               edgecolors="white", linewidths=0.7,
               label=("no phenotype" if lab == 0 else "growth phenotype"))
r = np.corrcoef(np.log10(dist + 1.0), plddt)[0, 1]
# open a clear band on the right so the key never sits over data
xmax = float(np.nanmax(dist))
ax.set_xlim(-4, xmax * 1.42)
ax.axvline(xmax * 1.06, color=INK3, lw=0.5, alpha=0.35)
ax.axhline(70, color=INK3, ls=(0, (2, 2)), lw=1, xmax=0.72)
ax.text(xmax * 1.02, 72.5, "pLDDT 70", fontsize=7, color=INK3, ha="right")
ax.set_xlabel("Distance to nearest annotated residue (Å)")
ax.set_ylabel("AlphaFold pLDDT at the site")
ax.set_title(f"C   The confound: r = {r:.2f}", fontsize=9.5, fontweight="bold", color=INK, loc="left", pad=8)
ax.legend(frameon=False, fontsize=7.5, loc="upper left", bbox_to_anchor=(0.755, 1.0),
          handletextpad=0.4, labelcolor=INK2, borderaxespad=0)
ax.grid(alpha=0.13, lw=0.5)
caption(ax, "Longer distances tend to occur at lower-confidence sites;\nmeasurement confidence and biological context are entangled.")

# ---- D: distributions ---------------------------------------------------
ax = fig.add_subplot(gs[2, 1])
bins = np.linspace(0, 95, 20)
ax.hist(dist[y == 0], bins=bins, histtype="step", lw=2, color=BLUE, label="no phenotype")
ax.hist(dist[y == 1], bins=bins, histtype="step", lw=2, color=ORANGE, ls=(0, (3, 1.6)),
        label="growth phenotype")
m0, m1 = np.median(dist[y == 0]), np.median(dist[y == 1])
ax.axvline(m0, color=BLUE, lw=1.2, alpha=0.5)
ax.axvline(m1, color=ORANGE, lw=1.2, alpha=0.5)
ax.set_xlabel("Distance to nearest annotated residue (Å)")
ax.set_ylabel("Sites")
ax.set_title(f"D   Distributions overlap (medians {m1:.1f} vs {m0:.1f} Å)",
             fontsize=9.5, fontweight="bold", color=INK, loc="left", pad=8)
ax.legend(frameon=False, fontsize=7.5, loc="upper right", handletextpad=0.6, labelcolor=INK2)
ax.grid(axis="y", alpha=0.13, lw=0.5)
caption(ax, "The observed distributions overlap substantially.\nVertical lines mark the medians.")

# ---- footer -------------------------------------------------------------
f = fig.add_subplot(gs[3, :]); f.axis("off"); f.set_xlim(0, 1); f.set_ylim(0, 1)
f.plot([0, 1], [1.0, 1.0], color="#e3e2de", lw=1)
disp = pd.read_csv(os.path.join(HERE, "results", "cohort_disposition.csv"))
eligible = int(disp.eligible_raw_cohort.sum())
f.text(0, 0.86,
       f"{len(disp)} point-mutant records / {disp['Systematic name'].nunique()} genes  →  "
       f"{int(disp.raw_profile_available.sum())} with raw profiles  →  {eligible} sequence/QC-eligible records\n"
       f"→  {len(d)} primary substitutions in {d.acc.nunique()} proteins after excluding 3 annotation-coincident sites; "
       f"the named inclusive sensitivity contains {len(inclusive)} substitutions.",
       fontsize=7.4, color=INK2, va="top", linespacing=1.7)
logistic = STATS["logistic"][0]
cut5 = next(row for row in STATS["cutoffs"] if row["cutoff_A"] == 5)
f.text(0, 0.40,
       f"Cluster-robust logistic regression: OR {logistic['or_per_10x_distance_plus_1A']:.2f} "
       f"[{logistic['ci_low']:.2f}, {logistic['ci_high']:.2f}] per 10-fold increase in distance + 1 Å.\n"
       f"Within 5 Å: {cut5['n_within']} substitutions, {cut5['rate_within']:.1%} positive; "
       f"beyond 5 Å: {cut5['rate_beyond']:.1%} positive. These are descriptive rates, not a threshold test.",
       fontsize=7.4, color=INK2, va="top", linespacing=1.7)
f.text(0, -0.06,
       (f"Post-result SIFT comparator: AUC {SIFT['auc']:.3f} "
        f"[{SIFT['ci_low']:.3f}, {SIFT['ci_high']:.3f}] on {SIFT['n']} substitutions. ") +
       "This is not independent validation. All analyses are exploratory; the interval around the distance AUC remains compatible with effects in either direction.\n"
       "Public source data only. The growth outcome describes alanine-mutant phenotypes, not direct phosphorylation dependence.   ·   Kyle Nguyen   ·   29 July 2026",
       fontsize=7.4, color=INK3, va="top", linespacing=1.7)

for ext in ("pdf", "png"):
    for stem in ("phospho_distance_calibration", "phospho_distance_calibration_by_cohort"):
        fig.savefig(os.path.join(HERE, "results", f"{stem}.{ext}"),
                    dpi=300, bbox_inches="tight")
print(f"AUC {auc:.3f} [{lo:.3f}, {hi:.3f}]  n={len(d)}  proteins={d.acc.nunique()}  pos={y.sum()}")
print("wrote results/phospho_distance_calibration.{pdf,png}")
