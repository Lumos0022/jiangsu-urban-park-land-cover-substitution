# -*- coding: utf-8 -*-
"""Redraw all submission figures in the topjournal design system.

Style contract (from Fig1-5_topjournal_package/README + gen_fig2_v3):
  * Arial sans-serif; 3 font tiers: panel label 9.5 pt bold / axis text 8 pt /
    annotations 6-7 pt; panel labels a b without brackets, top-left aligned
  * semantic palette: INK #1F1F1F, GREY #4D4D4D, GREY_L #8A8A8A, BAND #F3F3F3,
    GRID #EAEAEA, ZERO #7A7A7A, C_A #C0504D (interior), C_B #2E6F9E (annular),
    SIG #C9A227
  * in-figure words kept minimal (<8 words per callout); sentences go to captions
  * outputs: 600 dpi PNG + vector PDF + SVG; pdf.fonttype=42

Data: locked v4 tables used by the manuscript (Table2_primary_models.csv for
coefficients; all_pairs_10pct_park_predictions.csv aggregated for the scatter;
tree_substitution_province_summary.csv for the discrete 3-level scenario;
radial profile and effect-modification summary CSVs for the SI figures).
"""
import csv
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle, Wedge

# ---------------------------------------------------------------- style ----
INK = "#1F1F1F"; GREY = "#4D4D4D"; GREY_L = "#8A8A8A"
BAND = "#F3F3F3"; GRID = "#EAEAEA"; ZERO = "#7A7A7A"
C_A = "#C0504D"; C_B = "#2E6F9E"; SIG = "#C9A227"
DONOR_COLORS = {"tree": "#2E6F9E", "veg_low": "#4C8C4A", "wet": "#3B7DD8",
                "built": "#C0504D", "crop": "#C9A227", "bare": "#8A8A8A"}
DONOR_LABELS = {"tree": "Tree", "veg_low": "Low vegetation", "wet": "Wet cover",
                "built": "Built-up", "crop": "Cropland", "bare": "Bare"}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7.5,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.color": INK, "ytick.color": INK,
    "text.color": INK, "axes.edgecolor": INK,
    "savefig.dpi": 600, "figure.dpi": 100,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

ROOT = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2")
PKG = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\投稿前\P01_v4_FINAL_SUBMISSION_PACKAGE_20260914")
OUTS = [Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures"),
        PKG / "05_Figures",
        Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\P01_v4_SYNC_20260913\figures")]

def panel_label(ax, s, dx=0.0, dy=1.09):
    ax.text(dx, dy, s, transform=ax.transAxes, fontsize=9.5, fontweight="bold",
            color=INK, va="bottom", ha="left")

def save_all(fig, stem):
    for out in OUTS:
        fig.savefig(out / f"{stem}.png")
        fig.savefig(out / f"{stem}.pdf")
        fig.savefig(out / f"{stem}.svg")
    plt.close(fig)
    print("saved", stem)

# ------------------------------------------------------------------- Fig 1 --
def fig1():
    import geopandas as gpd
    parks = gpd.read_file(ROOT / "spatial_v2" / "P01_v2_parks_albers.gpkg")
    boundary = gpd.read_file(
        ROOT.parents[1] / "03_Data" / "A环境数据集" / "行政边界" / "jiangsu_boundary.gpkg",
        layer="province").to_crs(parks.crs)

    fig = plt.figure(figsize=(7.25, 4.60))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.03, 1.16, 1.22], wspace=0.25)

    # (a) Study system
    ax = fig.add_subplot(gs[0, 0])
    boundary.boundary.plot(ax=ax, color=GREY, lw=0.7, zorder=1)
    cent = parks.geometry.centroid
    ax.scatter(cent.x, cent.y, s=4.2, color=C_B, alpha=0.80, edgecolors="none", zorder=2, rasterized=True)
    ax.set_aspect("equal"); ax.set_axis_off()
    panel_label(ax, "a")
    ax.text(0.02, 0.99, "Study system", transform=ax.transAxes, fontsize=8.0,
            fontweight="bold", va="top", ha="left")
    ax.text(0.02, 0.02, "1,034 parks · 13 cities · Jiangsu, China",
            transform=ax.transAxes, fontsize=6.5, color=GREY, va="bottom", ha="left")

    # (b) Geometry and extraction
    ax = fig.add_subplot(gs[0, 1]); ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    panel_label(ax, "b")
    ax.text(0.00, 1.02, "Geometry and extraction", fontsize=8.0, fontweight="bold", va="bottom")
    ax.add_patch(Circle((0.42, 0.60), 0.20, fc="#DCE6F0", ec=C_B, lw=1.0))
    ax.add_patch(Wedge((0.42, 0.60), 0.38, 0, 360, width=0.13, fc="#F1E3D2", ec=C_A, lw=0.7))
    ax.add_patch(Wedge((0.42, 0.60), 0.27, 0, 360, width=0.12, fc="#E8EEF3", ec=C_B, lw=0.6))
    ax.add_patch(Rectangle((0.34, 0.52), 0.16, 0.16, fc="#70A86B", ec="white", lw=0.7))
    ax.text(0.42, 0.60, "park", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    ax.text(0.42, 0.89, "interior + fixed annuli", ha="center", va="center", fontsize=7.0,
            bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=GREY_L, lw=0.5))
    ax.add_patch(FancyArrowPatch((0.42, 0.83), (0.42, 0.785), arrowstyle="-|>", mutation_scale=9, lw=0.7, color=GREY))
    for y, color, title in [(0.30, "#689F38", "WorldCover 10 m"),
                            (0.16, "#B65C42", "Landsat ST 30 m")]:
        ax.add_patch(FancyBboxPatch((0.05, y), 0.74, 0.095, boxstyle="round,pad=0.015",
                                    fc="white", ec=color, lw=0.9))
        ax.text(0.09, y + 0.048, title, fontsize=7.3, va="center", fontweight="bold")
        ax.add_patch(FancyArrowPatch((0.53, 0.43), (0.42, y + 0.105), arrowstyle="-|>",
                                     mutation_scale=8, lw=0.6, color=GREY))
    ax.text(0.86, 0.24, "fractional\noverlap\nweights", fontsize=6.5, color=GREY, va="center")

    # (c) Composition and prediction
    ax = fig.add_subplot(gs[0, 2]); ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    panel_label(ax, "c")
    ax.text(0.00, 1.02, "Composition and prediction", fontsize=8.0, fontweight="bold", va="bottom")
    parts = [("built", 0.17, "#7A7A7A"), ("bare", 0.07, "#C9B58B"), ("tree", 0.31, "#2D7A46"),
             ("low veg.", 0.25, "#9BCB7A"), ("crop", 0.11, "#E2BC58"), ("wet", 0.09, "#5FA9D5")]
    start = 0.05
    for name, share, color in parts:
        ax.add_patch(Rectangle((start, 0.76), 0.90 * share, 0.085, fc=color, ec="white", lw=0.5))
        start += 0.90 * share
    ax.text(0.05, 0.86, "six-part composition", fontsize=7.5, fontweight="bold")
    ax.add_patch(FancyBboxPatch((0.10, 0.44), 0.80, 0.11, boxstyle="round,pad=0.02",
                                fc="#F7F9FB", ec=C_B, lw=0.8))
    ax.text(0.50, 0.495, "five ILR balances + controls", ha="center", va="center", fontsize=7.5)
    ax.add_patch(FancyArrowPatch((0.50, 0.735), (0.50, 0.575), arrowstyle="-|>", mutation_scale=9, lw=0.7, color=GREY))
    ax.add_patch(FancyArrowPatch((0.50, 0.415), (0.50, 0.325), arrowstyle="-|>", mutation_scale=9, lw=0.7, color=GREY))
    ax.add_patch(FancyBboxPatch((0.10, 0.20), 0.80, 0.10, boxstyle="round,pad=0.02",
                                fc="#FDF6EC", ec=C_A, lw=0.8))
    ax.text(0.50, 0.25, "specified donor\u2013recipient transfers", ha="center", va="center",
            fontsize=7.5, fontweight="bold")
    ax.text(0.50, 0.10, "projected change · donor count · bootstrap interval",
            ha="center", va="center", fontsize=6.5, color=GREY)

    fig.subplots_adjust(bottom=0.06, top=0.93, left=0.03, right=0.99)
    save_all(fig, "Fig1_study_design")

# ------------------------------------------------------------------- Fig 2 --
def fig2():
    d = pd.read_csv(PKG / "04_Tables" / "Table2_primary_models.csv", encoding="utf-8-sig")
    ORDER = ["B1_impervious", "B2_terrestrial", "B3_woody", "B4_crop_wet", "B5_built_bare"]
    LABELS = {"B1_impervious": "Built + bare vs permeable covers",
              "B2_terrestrial": "Tree + low veg. vs crop + wet",
              "B3_woody": "Tree vs low vegetation",
              "B4_crop_wet": "Crop vs water + wetland",
              "B5_built_bare": "Built vs bare"}
    GROUPS = [(["B1_impervious"], "Impervious vs pervious"),
              (["B2_terrestrial", "B3_woody", "B4_crop_wet"], "Within pervious covers"),
              (["B5_built_bare"], "Within impervious covers")]
    RESP = [("LST_interior", "Interior summer LST", C_A),
            ("annular_contrast", "500\u20131,000 m annular contrast", C_B)]
    ypos = {p: i for i, p in enumerate(ORDER[::-1])}
    ytop, ybot = 4.5, -0.5

    fig = plt.figure(figsize=(7.09, 3.35), dpi=600)
    top, bot = 0.875, 0.155
    labels_ax = fig.add_axes([0.010, bot, 0.200, top - bot])
    pa = fig.add_axes([0.222, bot, 0.245, top - bot])
    na = fig.add_axes([0.474, bot, 0.108, top - bot])
    pb = fig.add_axes([0.592, bot, 0.245, top - bot])
    nb = fig.add_axes([0.844, bot, 0.108, top - bot])

    def clean(ax):
        ax.set_xlim(-0.65, 0.65); ax.set_ylim(ybot, ytop)
        ax.set_xticks([-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6])
        ax.tick_params(length=2.0, labelsize=6.5)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_linewidth(0.6)
        ax.tick_params(axis="y", left=False, labelleft=False)
    clean(pa); clean(pb); labels_ax.axis("off"); na.axis("off"); nb.axis("off")

    for names, _ in GROUPS:
        ys = [ypos[p] for p in names]
        lo, hi = min(ys) - 0.5, max(ys) + 0.5
        for ax in (labels_ax, pa, na, pb, nb):
            ax.axhspan(lo, hi, color=BAND, lw=0, zorder=0)
    for names, hdr in GROUPS:
        ys = [ypos[p] for p in names]
        labels_ax.text(0.02, max(ys) + 0.34, hdr, fontsize=6.3, fontweight="bold",
                       color=GREY_L, va="center")
    for p in ORDER:
        labels_ax.text(0.02, ypos[p], LABELS[p], fontsize=7.0, color=INK, va="center")
    labels_ax.text(0.02, 4.92, "ILR balance (SBP)", fontsize=6.3, fontweight="bold", color=GREY_L, va="center")

    for ax, (resp, title, col) in zip((pa, pb), RESP):
        q = d[d.response.eq(resp)].set_index("predictor").loc[ORDER].reset_index()
        ax.axvline(0, color=ZERO, lw=0.9, zorder=1)
        ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
        for _, row in q.iterrows():
            y = ypos[row.predictor]
            sig = row.p_fdr_bh < 0.05
            lo, hi = row.ci95_t_low, row.ci95_t_high
            ax.errorbar(row.beta, y, xerr=[[row.beta - lo], [hi - row.beta]],
                        fmt="o", ms=5.0, mfc=col if sig else "white",
                        mec=col, mew=1.1, color=col, ecolor=GREY,
                        elinewidth=1.0, capsize=2.2, capthick=1.0, zorder=3)
            if sig:
                ax.plot(row.beta, y + 0.28, marker="*", ms=4.6, color=SIG, clip_on=False, zorder=4)
        ax.set_xlabel("Association coefficient (K per ILR unit)", fontsize=7.0, color=INK, labelpad=2)
        ax.text(0.00, 1.09, "a" if ax is pa else "b", transform=ax.transAxes,
                fontsize=9.5, fontweight="bold", color=INK, va="bottom")
        ax.text(0.050, 1.09, title, transform=ax.transAxes, fontsize=8.0, color=INK, va="bottom")

    for ax, (resp, _, _) in zip((na, nb), RESP):
        ax.text(0.0, 4.92, "Estimate [95% CI]", fontsize=6.3, fontweight="bold", color=GREY_L, va="center")
        q = d[d.response.eq(resp)].set_index("predictor").loc[ORDER].reset_index()
        for _, row in q.iterrows():
            y = ypos[row.predictor]
            ax.text(0.0, y + 0.19, f"{row.beta:.2f} [{row.ci95_t_low:.2f}, {row.ci95_t_high:.2f}]",
                    fontsize=6.2, color=INK, va="center")
            ax.text(0.0, y - 0.20, f"q < 0.001" if row.p_fdr_bh < 0.001 else f"q = {row.p_fdr_bh:.3f}",
                    fontsize=6.0, color=GREY_L, va="center")
    save_all(fig, "Fig2_composition_associations")

# ------------------------------------------------------------------- Fig 3 --
def fig3():
    DATA = ROOT / "substitution_matrix_v2" / "P01_v2_all_pairs_10pct_park_predictions.csv"
    agg = {r: defaultdict(list) for r in ("LST_interior", "annular_contrast")}
    with open(DATA, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["scenario_pct"] != "10":
                continue
            agg[row["response"]][(row["donor"], row["recipient"])].append(float(row["delta_pred_K"]))

    def summarize(d):
        out = {}
        for (donor, recip), v in d.items():
            v.sort()
            n = len(v)
            out[(donor, recip)] = (n, sum(v) / n, v[int(0.025 * n)], v[int(0.975 * n) - 1])
        return out

    sum_int, sum_con = summarize(agg["LST_interior"]), summarize(agg["annular_contrast"])
    N_TOTAL = 728
    HIGHLIGHT = [("veg_low", "tree"), ("tree", "veg_low"), ("built", "wet"), ("wet", "built")]

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.7), sharey=True)
    for ax, (summ, title) in zip(axes, [(sum_int, "Interior LST change (K)"), (sum_con, "Surrounding-ring contrast change (K)")]):
        for (donor, recip), (n, m, lo, hi) in summ.items():
            pct = n / N_TOTAL * 100
            ax.errorbar(pct, m, yerr=[[m - lo], [hi - m]], fmt="o",
                        ms=(3.2 + 0.028 * n) ** 0.5 * 3.2,
                        mfc=DONOR_COLORS[donor], mec="white", mew=0.5,
                        ecolor=DONOR_COLORS[donor], elinewidth=1.0, capsize=2.2, zorder=3, alpha=0.92)
        ax.axhline(0, color=ZERO, lw=0.7, ls="--", zorder=1)
        ax.set_xlabel("Parks meeting the donor requirement (% of 728)", fontsize=7.0, labelpad=2)
        ax.set_xlim(-2, 105); ax.set_ylim(-1.75, 1.75)
        ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=6.5)
        panel_label(ax, "a" if ax is axes[0] else "b")
        ax.text(0.050, 1.09, title, transform=ax.transAxes, fontsize=8.0, va="bottom")
    axes[0].set_ylabel("Projected change (K)", fontsize=7.0, labelpad=2)

    notes = {("veg_low", "tree"): ("low veg \u2192 tree\n297 parks (41%)", (30, -0.42), (3, -0.82)),
             ("tree", "veg_low"): ("tree \u2192 low veg\n600 parks (82%)", (70, 0.47), (84, 0.66)),
             ("built", "wet"): ("built \u2192 wet\n460 parks (63%)", (58, -1.20), (58, -1.62)),
             ("wet", "built"): ("wet \u2192 built\n161 parks (22%)", (22, 0.66), (3, 1.02))}
    for k, (txt, xy, xyt) in notes.items():
        axes[0].annotate(txt, xy=xy, xytext=xyt, fontsize=6.8, ha="left",
                         arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6),
                         bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#BBBBBB", lw=0.4, alpha=0.92))

    handles = [plt.Line2D([0], [0], marker="o", ls="none", ms=6.5, mfc=DONOR_COLORS[d],
                          mec="white", mew=0.5, label=DONOR_LABELS[d])
               for d in ("tree", "veg_low", "wet", "built", "crop", "bare")]
    fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False,
               bbox_to_anchor=(0.5, -0.02), fontsize=6.5)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.14, wspace=0.12)
    save_all(fig, "Fig3_substitution_matrix")

# ------------------------------------------------------------------- Fig 4 --
def fig4():
    d = pd.read_csv(ROOT / "model_v2" / "P01_v2_tree_substitution_province_summary.csv", encoding="utf-8-sig")
    panels = [("LST_interior", "Interior LST", C_A), ("annular_contrast", "Surrounding \u2212 interior", C_B)]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.30))
    xlab = ["0 pp", "5 pp", "10 pp", "20 pp"]
    for ax, (resp, title, col) in zip(axes, panels):
        q = d[d.response.eq(resp)].sort_values("scenario_pct")
        x = np.arange(len(q))
        y = q.mean_delta_K.to_numpy(float)
        lo = q.ci_low_mean_K.to_numpy(float); hi = q.ci_high_mean_K.to_numpy(float)
        ax.axhline(0, color=ZERO, lw=0.8, zorder=1)
        ax.errorbar(x, y, yerr=[y - lo, hi - y], fmt="o", ms=6.0, color=col,
                    ecolor=col, elinewidth=1.0, capsize=3.0, zorder=3)
        for xx, yy, n in zip(x, y, q.n_feasible):
            ax.text(xx, yy - 0.16 * (1 if resp == "LST_interior" else -1), f"n = {n}",
                    ha="center", fontsize=6.3, color=GREY)
        ax.set_xticks(x, xlab)
        ax.set_xlabel("Area transferred from low vegetation to tree", fontsize=7.0, labelpad=2)
        ax.set_ylim(-1.35 if resp == "LST_interior" else -0.1, 0.15 if resp == "LST_interior" else 1.5)
        ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=6.5)
        panel_label(ax, "a" if ax is axes[0] else "b")
        ax.text(0.050, 1.09, title, transform=ax.transAxes, fontsize=8.0, va="bottom")
    axes[0].set_ylabel("Projected change (K)", fontsize=7.0, labelpad=2)
    axes[1].set_ylabel("Projected change (K)", fontsize=7.0, labelpad=2)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.88, bottom=0.14, wspace=0.25)
    save_all(fig, "Fig4_discrete_tree_scenarios")

# ----------------------------------------------------------------- Fig S1 --
def figS1():
    p = ROOT / "ring_profile_v2" / "P01_v2_B3_common_sample_radial_profile.csv"
    b = ROOT / "ring_profile_v2" / "P01_v2_B3_common_sample_joint_city_bootstrap.csv"
    d = pd.read_csv(p, encoding="utf-8-sig"); boot = pd.read_csv(b, encoding="utf-8-sig")
    labels = ["Park interior", "0\u2013250 m", "250\u2013500 m", "500\u20131,000 m"]
    means = [d.B3_interior_beta.iloc[0], *d.B3_ring_beta]
    cols = ["ring_0_250__interior", *[f"{r}__ring" for r in d.ring]]
    lo = [boot[c].quantile(0.025) for c in cols]; hi = [boot[c].quantile(0.975) for c in cols]
    fig, ax = plt.subplots(figsize=(5.0, 3.15))
    x = range(4)
    ax.axhline(0, color=ZERO, lw=0.8, zorder=1)
    ax.errorbar(x, means, yerr=[[m - l for m, l in zip(means, lo)], [h - m for m, h in zip(means, hi)]],
                fmt="o-", color=C_B, ecolor=GREY, capsize=3.0, lw=1.1, ms=5.5, zorder=3)
    ax.set_xticks(list(x), labels, fontsize=6.8)
    ax.set_ylabel("B3 coefficient (K per ILR unit)", fontsize=7.0, labelpad=2)
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6.5)
    ylo = min(lo) - 0.10; yhi = max(hi) + 0.10
    ax.set_ylim(ylo, yhi)
    ax.set_yticks(np.arange(np.ceil(ylo * 2) / 2, yhi, 0.2))
    fig.subplots_adjust(left=0.16, right=0.97, top=0.92, bottom=0.18)
    save_all(fig, "FigS1_radial_profile")

# ----------------------------------------------------------------- Fig S2 --
def figS2():
    d = pd.read_csv(ROOT / "effect_modification_v2" / "P01_v2_exploratory_effect_modification_summary.csv",
                    encoding="utf-8-sig")
    mods = [("log_area", "Park area (log ha)"), ("ring_built", "Built fraction in 500\u20131,000 m ring")]
    resps = [("LST_interior", "Interior LST"), ("annular_contrast", "Surrounding \u2212 interior")]
    fig, axes = plt.subplots(2, 2, figsize=(6.8, 5.0))
    for ri, (resp, rlab) in enumerate(resps):
        for ci, (mod, mlab) in enumerate(mods):
            ax = axes[ri, ci]
            q = d[(d.moderator.eq(mod)) & (d.response.eq(resp))].set_index("group").loc[["Low", "High"]]
            means = q.mean_delta_K.to_numpy(float); los = q.ci_low_K.to_numpy(float); his = q.ci_high_K.to_numpy(float)
            beta = q.B3_x_moderator_beta.iloc[0]; blo = q.B3_x_moderator_ci_low.iloc[0]; bhi = q.B3_x_moderator_ci_high.iloc[0]
            ax.errorbar(["Low quartile", "High quartile"], means,
                        yerr=[means - los, his - means], fmt="o", ms=5.5, color=C_B,
                        ecolor=C_B, elinewidth=1.0, capsize=3.0, zorder=3)
            ax.axhline(0, color=ZERO, lw=0.8, zorder=1)
            ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            ax.tick_params(labelsize=6.3)
            ax.set_ylim(-1.30 if resp == "LST_interior" else -0.1,
                        0.20 if resp == "LST_interior" else 1.55)
            ax.text(0.02, 0.03, f"interaction 95% CI [{blo:.2f}, {bhi:.2f}]",
                    transform=ax.transAxes, fontsize=6.0, color=GREY)
            panel_label(ax, "a" if (ri, ci) == (0, 0) else "b" if (ri, ci) == (0, 1)
                        else "c" if (ri, ci) == (1, 0) else "d")
            ax.text(0.05, 1.05, f"{mlab} \u00b7 {rlab}", transform=ax.transAxes,
                    fontsize=7.0, va="bottom")
    axes[0, 0].set_ylabel("Projected \u0394 (K)", fontsize=7.0, labelpad=2)
    axes[1, 0].set_ylabel("Projected \u0394 (K)", fontsize=7.0, labelpad=2)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.95, bottom=0.07, wspace=0.30, hspace=0.42)
    save_all(fig, "FigS2_area_interaction")

if __name__ == "__main__":
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
    fig1(); fig2(); fig3(); fig4(); figS1(); figS2()
    print("ALL DONE")
