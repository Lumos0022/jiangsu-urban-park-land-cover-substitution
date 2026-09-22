# -*- coding: utf-8 -*-
"""Fig4 upgraded discrete version: topjournal aesthetics, no connecting line.

Keeps the manuscript-compliant discrete semantics (each amount is a different
donor-eligible subset; points must NOT be connected) while adopting the
topjournal visual language:
  * Delta axis titles (response in the y label)
  * baseline point (0 pp, n=728) as a grey filled marker, distinct from the
    three coloured transfer points
  * terminal K-value labels (-0.70 K / +0.98 K)
  * n labels on the outer side of the points (a: below, b: above)
  * discrete categorical x axis (0/5/10/20 pp) - no dose-response implication
  * font system identical to Fig4_discrete_tree_scenarios (Arial, 9.5 bold
    panel labels, 7.0 axis titles, 6.5 ticks, 6.3 annotations)
Data: v4 locked (P01_v2_tree_substitution_province_summary.csv).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#1F1F1F"; GREY = "#4D4D4D"; GREY_L = "#8A8A8A"
ZERO = "#7A7A7A"
C_A = "#C0504D"; C_B = "#2E6F9E"

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

d = pd.read_csv(Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2\model_v2\P01_v2_tree_substitution_province_summary.csv"),
                encoding="utf-8-sig")

panels = [("LST_interior", "\u0394 interior summer LST (K)", C_A, [-1.35, 0.20], [0, -0.5, -1], -1.05, -16),
          ("annular_contrast", "\u0394 annular contrast (K)", C_B, [-0.12, 1.25], [0, 0.5, 1], 1.13, 14)]

fig, axes = plt.subplots(1, 2, figsize=(7.09, 3.15))
for ax, (resp, ylab, col, ylim, yticks, yk, n_off) in zip(axes, panels):
    q = d[d.response.eq(resp)].sort_values("scenario_pct")
    y = q.mean_delta_K.to_numpy(float)
    lo = q.ci_low_mean_K.to_numpy(float); hi = q.ci_high_mean_K.to_numpy(float)
    x = np.arange(len(q))

    ax.axhline(0, color=ZERO, lw=0.9, zorder=1)
    ax.grid(axis="x", color="#EAEAEA", lw=0.5, zorder=0)

    # baseline (0 pp): grey filled marker (no uncertainty; zero by construction)
    ax.errorbar([x[0]], [y[0]], yerr=[[0.0], [0.0]], fmt="o", ms=5.0,
                mfc=GREY_L, mec=GREY_L, mew=1.1, ecolor="none", zorder=3)

    # transfer points: filled, coloured (Fig2 forest style)
    ax.errorbar(x[1:], y[1:], yerr=[y[1:] - lo[1:], hi[1:] - y[1:]],
                fmt="o", ms=5.0, mfc=col, mec=col, mew=1.1,
                ecolor=GREY, elinewidth=1.0, capsize=2.2, capthick=1.0,
                zorder=3, alpha=0.95)

    # n labels on the outer side (a: below, b: above)
    for xx, yy, n in zip(x, y, q.n_feasible):
        ax.annotate(f"n = {n}", (xx, yy), xytext=(0, n_off), textcoords="offset points",
                    ha="center", va="center", fontsize=6.3, color=GREY, zorder=5)

    # terminal K label in the outer blank margin
    ax.text(x[-1], yk, f"{y[-1]:+.2f} K", ha="center", va="center",
            fontsize=6.3, color=col, zorder=5)

    ax.set_xlim(-0.6, len(q) - 0.4); ax.set_ylim(*ylim)
    ax.set_xticks(x, ["0 pp", "5 pp", "10 pp", "20 pp"])
    ax.set_yticks(yticks)
    ax.set_xlabel("Area transferred from low vegetation to tree", fontsize=7.0, labelpad=2)
    ax.set_ylabel(ylab, fontsize=7.0, labelpad=2)
    ax.tick_params(labelsize=6.5, length=2.0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.6)

    ax.text(0.00, 1.09, "a" if ax is axes[0] else "b", transform=ax.transAxes,
            fontsize=9.5, fontweight="bold", color=INK, va="bottom")

fig.subplots_adjust(left=0.10, right=0.97, top=0.90, bottom=0.14, wspace=0.28)

out_dirs = [Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures"),
            Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\投稿前\P01_v4_FINAL_SUBMISSION_PACKAGE_20260914\05_Figures"),
            Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\P01_v4_SYNC_20260913\figures")]
for out in out_dirs:
    for ext in ("png", "pdf", "svg"):
        fig.savefig(out / f"Fig4_discrete_tree_scenarios.{ext}")
plt.close(fig)
print("saved Fig4_discrete_tree_scenarios.{png,pdf,svg} -> 3 dirs")
