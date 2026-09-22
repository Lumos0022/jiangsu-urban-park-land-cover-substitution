# -*- coding: utf-8 -*-
"""Fig. S1 / Fig. S2 redraw in the Fig. 2 top-journal style.

Style contract (identical to gen_fig2_v3_forest_topjournal.py):
  INK #1F1F1F, GREY #4D4D4D, GREY_L #8A8A8A, BAND #F3F3F3, GRID #EAEAEA,
  ZERO #7A7A7A, C_A #C0504D (interior), C_B #2E6F9E (annular);
  Arial 7.5 / tick 6.5 / axis 7.0 / panel 9.5 bold; 600 dpi; PDF type-42.
Data:
  S1  ring_profile_v2/P01_v2_B3_common_sample_radial_profile.csv
      + joint_city_bootstrap.csv (2.5/97.5 percentile intervals)
  S2  effect_modification_v2/P01_v2_exploratory_effect_modification_summary.csv
Outputs (PNG 600dpi + vector PDF) -> AAA 05_Figures (overwrite current S1/S2).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\03_数据库\投稿前重构_20260904\Reanalysis_v2")
OUT = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures")

INK = "#1F1F1F"
GREY = "#4D4D4D"
GREY_L = "#8A8A8A"
BAND = "#F3F3F3"
GRID = "#EAEAEA"
ZERO = "#7A7A7A"
C_A = "#C0504D"
C_B = "#2E6F9E"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7.5,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "savefig.dpi": 600,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


# ---------------------------------------------------------------- Fig. S1 --
def fig_s1():
    p = ROOT / "ring_profile_v2" / "P01_v2_B3_common_sample_radial_profile.csv"
    b = ROOT / "ring_profile_v2" / "P01_v2_B3_common_sample_joint_city_bootstrap.csv"
    d = pd.read_csv(p, encoding="utf-8-sig")
    boot = pd.read_csv(b, encoding="utf-8-sig")

    labels = ["Park interior", "0\u2013250 m", "250\u2013500 m", "500\u20131,000 m"]
    means = [d.B3_interior_beta.iloc[0], *d.B3_contrast_beta]
    cols = ["ring_0_250__interior",
            *[f"{r}__contrast" for r in d.ring]]
    lo = [boot[c].quantile(0.025) for c in cols]
    hi = [boot[c].quantile(0.975) for c in cols]
    cols_pt = [C_A, C_B, C_B, C_B]

    fig, ax = plt.subplots(figsize=(5.65, 3.05), dpi=600)
    x = np.arange(4)
    ax.axhline(0, color=ZERO, lw=0.9, zorder=1)
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    ax.plot(x, means, color=GREY_L, lw=0.8, zorder=2)
    for xi, mi, li, hi_i, c in zip(x, means, lo, hi, cols_pt):
        ax.errorbar([xi], [mi],
                    yerr=[[mi - li], [hi_i - mi]],
                    fmt="o", ms=5.0, mfc=c, mec=c, mew=1.1,
                    ecolor=GREY, elinewidth=1.0, capsize=2.2, capthick=1.0,
                    zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.0, color=INK)
    ax.tick_params(length=2.0, labelsize=6.5, colors=INK)
    ax.set_ylabel("B3 association coefficient (K per ILR unit)",
                  fontsize=7.0, color=INK, labelpad=2)
    ax.set_xlim(-0.45, 3.45)
    ylo = min(lo) - 0.10
    yhi = max(hi) + 0.10
    ax.set_ylim(ylo, yhi)
    ax.set_yticks(np.arange(np.ceil(ylo * 2) / 2, yhi, 0.2))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_linewidth(0.6)
    ax.spines["bottom"].set_linewidth(0.6)
    ax.text(0.005, 0.035,
            "n = 721 parks; 13 cities; bars: 95% joint city-block bootstrap intervals",
            transform=ax.transAxes, fontsize=6.5, color=GREY)
    for f in ("png", "pdf"):
        fig.savefig(OUT / f"FigS1_radial_profile.{f}", bbox_inches="tight")
    plt.close(fig)
    print("FigS1 saved:", means, "CI", list(zip(lo, hi)))


# ---------------------------------------------------------------- Fig. S2 --
def fig_s2():
    p = (ROOT / "effect_modification_v2"
         / "P01_v2_exploratory_effect_modification_summary.csv")
    d = pd.read_csv(p, encoding="utf-8-sig")

    # panel config: (moderator, response, colour, title)
    panels = [
        ("log_area", "LST_interior", C_A, "Park area (log ha) \u00b7 Interior LST"),
        ("ring_built", "LST_interior", C_A, "Built fraction in 500\u20131,000 m ring \u00b7 Interior LST"),
        ("log_area", "annular_contrast", C_B, "Park area (log ha) \u00b7 Surrounding \u2013 interior"),
        ("ring_built", "annular_contrast", C_B, "Built fraction in 500\u20131,000 m ring \u00b7 Surrounding \u2013 interior"),
    ]
    xpos = {"Low": 0.0, "High": 1.0}

    fig, axes = plt.subplots(2, 2, figsize=(7.09, 5.35), dpi=600)
    for ax, (mod, resp, col, title), tag in zip(axes.ravel(), panels, "abcd"):
        q = d[(d.moderator == mod) & (d.response == resp)]
        q = q.set_index("group").loc[["Low", "High"]]
        xs = [xpos[g] for g in q.index]
        ys = q.mean_delta_K.values
        lo = q.ci_low_K.values
        hi = q.ci_high_K.values
        ns = q.n_group.values

        ax.axhline(0, color=ZERO, lw=0.9, zorder=1)
        ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
        ax.plot(xs, ys, color=GREY_L, lw=0.8, zorder=2)
        ax.errorbar(xs, ys,
                    yerr=[[ys[0] - lo[0], ys[1] - lo[1]],
                          [hi[0] - ys[0], hi[1] - ys[1]]],
                    fmt="o", ms=5.0, mfc=col, mec=col, mew=1.1,
                    ecolor=GREY, elinewidth=1.0, capsize=2.2, capthick=1.0, zorder=3)
        ax.set_xticks([0.0, 1.0])
        ax.set_xticklabels([f"Low quartile\n(n = {ns[0]})",
                            f"High quartile\n(n = {ns[1]})"],
                           fontsize=6.5, color=INK)
        ax.tick_params(length=2.0, labelsize=6.5, colors=INK)
        ax.set_ylabel("Projected \u0394T (K)", fontsize=7.0, color=INK, labelpad=2)
        ax.set_xlim(-0.35, 1.35)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_linewidth(0.6)
        ax.spines["bottom"].set_linewidth(0.6)

        ib = q.B3_x_moderator_beta.iloc[0]
        ic = (q.B3_x_moderator_ci_low.iloc[0], q.B3_x_moderator_ci_high.iloc[0])
        ax.text(0.02, 0.06, f"interaction 95% CI [{ic[0]:.2f}, {ic[1]:.2f}]",
                transform=ax.transAxes, fontsize=6.3, color=GREY,
                va="bottom", ha="left")
        ax.text(0.0, 1.10, tag, transform=ax.transAxes, fontsize=9.5,
                fontweight="bold", color=INK, va="bottom", ha="left")
        ax.text(0.045, 1.10, title, transform=ax.transAxes, fontsize=8.0,
                color=INK, va="bottom", ha="left")

    fig.tight_layout(w_pad=1.6, h_pad=2.2)
    for f in ("png", "pdf"):
        fig.savefig(OUT / f"FigS2_area_interaction.{f}", bbox_inches="tight")
    plt.close(fig)
    print("FigS2 saved")


if __name__ == "__main__":
    fig_s1()
    fig_s2()
