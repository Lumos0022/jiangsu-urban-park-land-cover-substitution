# -*- coding: utf-8 -*-
"""Fig5 (v9): 3.8 -> two-panel figure, full Fig2 design language.

(a) Per-city leave-one-city-out Q^2 gain (Table S15, both responses).
    Redesigned for an international readership:
      * x axis = latitude (deg N), cities plotted south -> north, so the
        south-north gradient is read directly from the spatial axis;
      * thin response-coloured polylines connect each city, exposing the
        south-high / north-low interior pattern and the opposite annular
        pattern;
      * Nantong, the only city with a negative interior gain (-0.16), is
        highlighted with a dark outline and labelled (negative-gain island).
(b) B3 coefficient across five comparable specifications (baseline, physical
    cell-area, amalgamate-before, IPW, Shannon) with t_12 95% CIs, drawn with
    the Fig2 forest vocabulary: grey group bands, grey error bars, solid zero
    line, light x-grid, separate row-label and Estimate [95% CI] columns.

Palette follows Fig2: interior #C0504D, annular #2E6F9E.
Style follows Fig2: Arial 7.5, axes.linewidth 0.5, 600 dpi, PNG/PDF/SVG to
three dirs, CVD strip for the AAA copy.
"""
from pathlib import Path
import csv
import numpy as np
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#1F1F1F"; GREY = "#4D4D4D"; GREY_L = "#8A8A8A"
BAND = "#F3F3F3"; GRID = "#EAEAEA"; ZERO = "#7A7A7A"
C_INT = "#C0504D"; C_ANN = "#2E6F9E"

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

OUTS = [Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915\05_Figures"),
        Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\投稿前\P01_v4_FINAL_SUBMISSION_PACKAGE_20260914\05_Figures"),
        Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\P01_v4_SYNC_20260913\figures")]
AAA = OUTS[0]
SYNC = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\09_Manuscript\P01_v4_SYNC_20260913")
PKG = Path(r"G:\Codex\Jiangsu_HumanBird_Tradeoff\AAA投稿前最终版本\P01_FULL_SUBMISSION_PACKAGE_20260915")

CITY_EN = {"南京市": "Nanjing", "南通市": "Nantong", "宿迁市": "Suqian",
           "常州市": "Changzhou", "徐州市": "Xuzhou", "扬州市": "Yangzhou",
           "无锡市": "Wuxi", "泰州市": "Taizhou", "淮安市": "Huai\u2019an",
           "盐城市": "Yancheng", "苏州市": "Suzhou", "连云港市": "Lianyungang",
           "镇江市": "Zhenjiang"}
# approximate municipal-centre latitudes (deg N) for the south -> north axis
LAT = {"Suzhou": 31.30, "Wuxi": 31.49, "Changzhou": 31.81, "Nantong": 31.98,
       "Nanjing": 32.06, "Zhenjiang": 32.20, "Yangzhou": 32.39, "Taizhou": 32.49,
       "Yancheng": 33.35, "Huai\u2019an": 33.60, "Suqian": 33.96, "Xuzhou": 34.26,
       "Lianyungang": 34.60}
T12 = stats.t.ppf(0.975, 12)


def panel_label(ax, lab):
    ax.text(0.0, 1.10, lab, transform=ax.transAxes, fontsize=9.5,
            fontweight="bold", color=INK, va="bottom")


def panel_title(ax, txt):
    ax.text(0.045, 1.10, txt, transform=ax.transAxes, fontsize=8.0, va="bottom")


def save_all(fig, stem):
    for out in OUTS:
        for ext in ("png", "pdf", "svg"):
            fig.savefig(out / f"{stem}.{ext}")


def cvd_check(fig, stem):
    def transform(im, M):
        a = np.asarray(im).astype(float) / 255.0
        shp = a.shape
        a = a.reshape(-1, 3) @ M.T
        return (np.clip(a, 0, 1).reshape(shp) * 255).astype(np.uint8)

    DEUTAN = np.array([[0.625, 0.375, 0.000], [0.700, 0.300, 0.000], [0.000, 0.300, 0.700]])
    PROTAN = np.array([[0.567, 0.433, 0.000], [0.558, 0.442, 0.000], [0.000, 0.242, 0.758]])
    import io
    from PIL import Image
    buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    orig = Image.open(buf).convert("RGB")
    for name, M in (("deutan", DEUTAN), ("protan", PROTAN)):
        sim = Image.fromarray(transform(orig, M))
        strip = Image.new("RGB", (orig.width * 3, orig.height))
        strip.paste(orig, (0, 0)); strip.paste(sim, (orig.width, 0))
        strip.paste(orig, (orig.width * 2, 0))
        strip.save(AAA / f"cvd_{stem}_{name}.png")


def read_q2():
    """Per-city delta Q2 for both responses (Table S15)."""
    d = {}
    with open(PKG / "07_Supplementary_Tables" / "Table_S15.csv",
              encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            resp = "interior" if "interior" in row["response"] else "annular"
            d.setdefault(CITY_EN[row["city"]], {})[resp] = float(row["delta_q2"])
    return d


def read_b3_specs():
    """B3 beta + t_12 CI per specification (all five comparable specs)."""
    rows = {}
    with open(SYNC / "ADDITIONAL_SENSITIVITY_COEFFICIENTS.csv",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["predictor"] != "B3_woody":
                continue
            resp = "interior" if "interior" in r["response"] else "annular"
            mode = r["mode"]
            if mode == "baseline":
                rows[("baseline", resp)] = (float(r["beta"]), float(r["se"]))
            elif mode.startswith("physical"):
                rows[("physical", resp)] = (float(r["beta"]), float(r["se"]))
            elif mode.startswith("amalgamate"):
                rows[("amalgamate", resp)] = (float(r["beta"]), float(r["se"]))
    with open(SYNC / "P01_v2_IPW_attrition_sensitivity_coefficients.csv",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["predictor"] != "B3_woody":
                continue
            resp = "interior" if "interior" in r["response"] else "annular"
            rows[("ipw", resp)] = (float(r["beta_ipw"]), float(r["se_city_ipw"]))
    with open(SYNC / "P01_v2_SHDI_control_sensitivity.csv",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["predictor"] != "B3_woody":
                continue
            resp = "interior" if "interior" in r["response"] else "annular"
            rows[("shannon", resp)] = (float(r["beta"]), float(r["se_city"]))
    return rows


def panel_a(ax, d):
    """Prediction gain vs latitude (south -> north); Nantong highlighted."""
    cities = sorted(LAT, key=LAT.get)          # south -> north
    xs = [LAT[c] for c in cities]
    # Fig2-style vertical grid on the value axis + solid zero line
    ax.axhline(0, color=ZERO, lw=0.9, zorder=1)
    ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
    for resp, col in (("interior", C_INT), ("annular", C_ANN)):
        ys = [d[c][resp] for c in cities]
        ax.plot(xs, ys, color=col, lw=0.8, alpha=0.55, zorder=2)  # gradient polyline
        for x, y, c in zip(xs, ys, cities):
            if resp == "interior" and c == "Nantong":
                ax.plot(x, y, "o", ms=6.5, mfc=col, mec=INK, mew=1.8,
                        zorder=4)
                ax.annotate("Nantong \u22120.16", (x, y),
                            xytext=(7, 6), textcoords="offset points",
                            fontsize=6.0, color=INK, ha="left", va="bottom",
                            zorder=5)
            else:
                ax.plot(x, y, "o", ms=5.0, mfc=col, mec=col, mew=1.1,
                        zorder=3, alpha=0.95)
    ax.set_xticks([31, 32, 33, 34, 35])
    ax.set_xticklabels(["31", "32", "33", "34", "35"])
    ax.set_xlim(31.0, 35.0)
    ax.set_ylim(-0.24, 0.48)
    ax.set_yticks([-0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4])
    ax.set_yticklabels(["-0.2", "-0.1", "0", "0.1", "0.2", "0.3", "0.4"])
    ax.set_xlabel("Latitude (\u00b0N), south \u2192 north", fontsize=7.0,
                  color=INK, labelpad=2)
    ax.set_ylabel("\u0394Q\u00b2 in withheld city", fontsize=7.0,
                  color=INK, labelpad=2)
    ax.tick_params(length=2.0, labelsize=6.5, colors=INK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.6)
    panel_label(ax, "a")
    panel_title(ax, "Prediction gain in withheld cities")


def panel_b(labels_ax, fax, nax, rows):
    """Fig2-style forest: row labels | estimates | Estimate [95% CI] column."""
    specs = ["baseline", "physical", "amalgamate", "ipw", "shannon"]
    labels = {"baseline": "Primary (city-clustered)",
              "physical": "Physical cell-area weighting",
              "amalgamate": "Amalgamation before replacement",
              "ipw": "Inverse-probability weighting",
              "shannon": "Shannon diversity covariate"}
    groups = [("annular", C_ANN, 10.75, "Surrounding-ring contrast"),
              ("interior", C_INT, 4.25, "Interior LST")]
    ypos = {}
    for resp, col, yoff, hdr in groups:
        for i, spec in enumerate(specs):
            ypos[(spec, resp)] = yoff - i - 0.5
    # ---- grey group bands across every column -----------------------------
    for ax in (labels_ax, fax, nax):
        ax.axhspan(5.9, 10.6, color=BAND, lw=0, zorder=0)
        ax.axhspan(-0.6, 4.1, color=BAND, lw=0, zorder=0)
    # ---- left column: column header + group headers + row labels ----------
    labels_ax.axis("off")
    labels_ax.text(0.02, 11.55, "Model specification", fontsize=6.3,
                   fontweight="bold", color=GREY_L, va="center")
    for resp, col, yoff, hdr in groups:
        labels_ax.text(0.02, yoff + 0.34, hdr, fontsize=6.3, fontweight="bold",
                       color=GREY_L, va="center")
        for i, spec in enumerate(specs):
            labels_ax.text(0.02, yoff - i - 0.5, labels[spec], fontsize=7.0,
                           color=INK, va="center")
    labels_ax.set_xlim(0, 1); labels_ax.set_ylim(-0.75, 12.0)
    # ---- forest panel ------------------------------------------------------
    fax.axvline(0, color=ZERO, lw=0.9, zorder=1)
    fax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
    for resp, col, yoff, hdr in groups:
        for i, spec in enumerate(specs):
            b, se = rows[(spec, resp)]
            lo, hi = b - T12 * se, b + T12 * se
            y = yoff - i - 0.5
            fax.errorbar(b, y, xerr=[[b - lo], [hi - b]], fmt="o",
                         ms=5.0, mfc=col, mec=col, mew=1.1, color=col,
                         ecolor=GREY, elinewidth=1.0, capsize=2.2,
                         capthick=1.0, zorder=3, alpha=0.95)
    fax.set_xlim(-0.65, 0.65)
    fax.set_xticks([-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6])
    fax.set_xticklabels(["-0.6", "-0.4", "-0.2", "0", "0.2", "0.4", "0.6"])
    fax.set_ylim(-0.75, 12.0)
    fax.tick_params(length=2.0, labelsize=6.5, colors=INK)
    for s in ("top", "right", "left"):
        fax.spines[s].set_visible(False)
    fax.spines["bottom"].set_linewidth(0.6)
    fax.tick_params(axis="y", left=False, labelleft=False)
    fax.set_xlabel("B3 coefficient (K per ILR unit)", fontsize=7.0,
                   color=INK, labelpad=2)
    # ---- numeric column: Estimate [95% CI] --------------------------------
    nax.axis("off")
    nax.text(0.0, 11.55, "Estimate [95% CI]", fontsize=6.3, fontweight="bold",
             color=GREY_L, va="center")
    for resp, col, yoff, hdr in groups:
        for i, spec in enumerate(specs):
            b, se = rows[(spec, resp)]
            lo, hi = b - T12 * se, b + T12 * se

            def f2(x):
                s = f"{x:.2f}"
                return "0.00" if s == "-0.00" else s

            nax.text(0.0, yoff - i - 0.5, f"{f2(b)} [{f2(lo)}, {f2(hi)}]",
                     fontsize=6.2, color=INK, va="center")
    nax.set_xlim(0, 1); nax.set_ylim(-0.75, 12.0)
    panel_label(fax, "b")
    panel_title(fax, "B3 under alternative specifications")


def main():
    d = read_q2()
    rows = read_b3_specs()
    fig = plt.figure(figsize=(7.4, 3.55), dpi=600)
    bot, top = 0.235, 0.905
    pa = fig.add_axes([0.115, bot, 0.285, top - bot])
    labels_ax = fig.add_axes([0.420, bot, 0.210, top - bot])
    fax = fig.add_axes([0.640, bot, 0.230, top - bot])
    nax = fig.add_axes([0.882, bot, 0.108, top - bot])
    panel_a(pa, d)
    panel_b(labels_ax, fax, nax, rows)
    fig.legend(handles=[
        plt.Line2D([0], [0], marker="o", ls="none", ms=5.0, mfc=C_INT,
                   mec=C_INT, mew=1.1, label="Interior LST"),
        plt.Line2D([0], [0], marker="o", ls="none", ms=5.0, mfc=C_ANN,
                   mec=C_ANN, mew=1.1, label="Surrounding-ring contrast")],
        loc="lower center", ncol=2, frameon=False, fontsize=6.8,
        bbox_to_anchor=(0.5, 0.088))
    save_all(fig, "Fig5_prediction_robustness")
    cvd_check(fig, "Fig5_prediction_robustness")
    plt.close(fig)
    # sanity print
    for spec in ("baseline", "physical", "amalgamate", "ipw", "shannon"):
        b, se = rows[(spec, "interior")]
        print(spec, "interior", round(b, 3), "CI", round(b - T12 * se, 3),
              round(b + T12 * se, 3))
        b, se = rows[(spec, "annular")]
        print(spec, "annular", round(b, 3), "CI", round(b - T12 * se, 3),
              round(b + T12 * se, 3))
    print("saved Fig5_prediction_robustness.{png,pdf,svg} -> 3 dirs + CVD strips")


if __name__ == "__main__":
    main()
