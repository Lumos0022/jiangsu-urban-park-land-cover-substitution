from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
BLUE = "#2C6E9F"
ORANGE = "#D97632"
GREY = "#5E6472"
PALE = "#D9E6EF"

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10, "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 8.5, "axes.linewidth": .7, "xtick.major.width": .7,
    "ytick.major.width": .7, "figure.dpi": 300, "savefig.dpi": 300,
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": .04,
})

def finish(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{stem}.{ext}")
    plt.close(fig)
