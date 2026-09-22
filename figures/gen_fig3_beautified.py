# -*- coding: utf-8 -*-
"""Fig3 beautified: topjournal aesthetics with an improved donor palette.

Palette fix: the old tree (#2E6F9E) and wet (#3B7DD8) blues were nearly
indistinguishable. New palette separates hues with semantic colours:
  tree   deep forest green   #2F6B4F
  veg_low light grass green  #8FBF6E
  wet    water blue          #3E7CB1
  built  brick red           #C0504D
  crop   amber               #D9A62E
  bare   warm grey-brown     #8D8577
Also: alpha 0.95, CVD check strip (deutan/protan) as in the topjournal package.
Data: v4 locked (P01_v2_all_pairs_10pct_park_predictions.csv).
"""
from pathlib import Path
from collections import defaultdict
import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#1F1F1F"; GREY = "#4D4D4D"; GREY_L = "#8A8A8A"
BAND = "#F3F3F3"; GRID = "#EAEAEA"; ZERO = "#7A7A7A"
C_A = "#C0504D"; C_B = "#2E6F9E"; SIG = "#C9A227"

DONOR_COLORS = {
    "tree": "#2F6B4F", "veg_low": "#8FBF6E", "wet": "#4A7BA5",
    "built": "#B45B59", "crop": "#B59752", "bare": "#8D8577",
}
DONOR_LABELS = {
    "tree": "Tree", "veg_low": "Low vegetation", "wet": "Wet cover",
    "built": "Built-up", "crop": "Cropland", "bare": "Bare",
}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7.5,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.color": INK, "ytick.color": INK, "text.color": INK,
    "axes.edgecolor": INK,
    "savefig.dpi": 600, "figure.dpi": 100, "pdf.fonttype": 42, "ps.fonttype": 42,
})

ROOT = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2")
OUTS = [Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures"),
        Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\投稿前\P01_v4_FINAL_SUBMISSION_PACKAGE_20260914\05_Figures"),
        Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\P01_v4_SYNC_20260913\figures")]


def panel_label(ax, lab):
    ax.text(0.0, 1.09, lab, transform=ax.transAxes, fontsize=9.5,
            fontweight="bold", color=INK, va="bottom")


def save_all(fig, stem):
    for out in OUTS:
        for ext in ("png", "pdf", "svg"):
            fig.savefig(out / f"{stem}.{ext}")


def cvd_check(fig, stem):
    """Brettel/Vienot linear-matrix CVD simulation strip (deutan/protan)."""
    def transform(im, M):
        a = np.asarray(im).astype(float) / 255.0
        shp = a.shape
        a = a.reshape(-1, 3) @ M.T
        return (np.clip(a, 0, 1).reshape(shp) * 255).astype(np.uint8)

    DEUTAN = np.array([[0.625, 0.375, 0.000], [0.700, 0.300, 0.000], [0.000, 0.300, 0.700]])
    PROTAN = np.array([[0.567, 0.433, 0.000], [0.558, 0.442, 0.000], [0.000, 0.242, 0.758]])
    import io
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    from PIL import Image
    orig = Image.open(buf).convert("RGB")
    for name, M in (("deutan", DEUTAN), ("protan", PROTAN)):
        sim = Image.fromarray(transform(orig, M))
        strip = Image.new("RGB", (orig.width * 3, orig.height))
        strip.paste(orig, (0, 0)); strip.paste(sim, (orig.width, 0))
        strip.paste(orig, (orig.width * 2, 0))
        strip.save(OUTS[0] / f"cvd_{stem}_{name}.png")
        # text label band
        from PIL import ImageDraw
        d = ImageDraw.Draw(strip)
        d.text((5, 5), name, fill=(255, 255, 255))
        strip.save(OUTS[0] / f"cvd_{stem}_{name}.png")


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
            col = DONOR_COLORS[donor]
            ax.errorbar(pct, m, yerr=[[m - lo], [hi - m]], fmt="o",
                        ms=(3.2 + 0.028 * n) ** 0.5 * 3.2,
                        mfc=col, mec="white", mew=0.6,
                        ecolor=col, elinewidth=1.0, capsize=2.2, zorder=3, alpha=0.95)
        ax.axhline(0, color=ZERO, lw=0.7, ls="--", zorder=1)
        ax.set_xlabel("Parks meeting the donor requirement (% of 728)", fontsize=7.0, labelpad=2)
        ax.set_xlim(-2, 105); ax.set_ylim(-1.75, 1.75)
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
                          mec="white", mew=0.6, label=DONOR_LABELS[d])
               for d in ("tree", "veg_low", "wet", "built", "crop", "bare")]
    fig.legend(handles=handles, loc="lower center", ncol=6, frameon=False,
               bbox_to_anchor=(0.5, -0.02), fontsize=6.5)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.14, wspace=0.12)
    save_all(fig, "Fig3_substitution_matrix")
    cvd_check(fig, "Fig3_substitution_matrix")
    plt.close(fig)
    print("saved Fig3_substitution_matrix.{png,pdf,svg} -> 3 dirs + CVD strips")


if __name__ == "__main__":
    fig3()
