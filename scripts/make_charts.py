"""Charts for the MORE investigation. Colours are for charts only, per her rule.
MORE is forest green; the BLEND is a dashed dark line; peers are grey tones.
"""
import pathlib

import matplotlib.pyplot as plt
import pandas as pd

base = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
g = pd.read_csv(base / "data" / "growth_of_10000.csv", index_col=0, parse_dates=True)
dd = pd.read_csv(base / "data" / "drawdowns.csv", index_col=0, parse_dates=True)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(g.index, g["MORE"], label="MORE", color="#1D5C30", linewidth=2.5)
ax.plot(g.index, g["BLEND"], label="50/50 XEG/XMA blend", color="#111111",
        linewidth=2, linestyle="--")
for c, col in [("XEG", "#6B7280"), ("XMA", "#9CA3AF"), ("ZEO", "#4B5563"),
               ("XGD", "#D1D5DB"), ("XIC", "#2F4F4F")]:
    ax.plot(g.index, g[c], label=c, color=col)
ax.set_title("Growth of $10,000 in CAD, weekly, 20 Sep 2024 to 13 Nov 2026")
ax.set_ylabel("$")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(base / "charts" / "growth_of_10000.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(dd.index, dd["MORE"] * 100, color="#1D5C30")
ax.fill_between(dd.index, dd["MORE"] * 100, 0, alpha=0.2, color="#1D5C30")
ax.set_title("MORE drawdown: fall from the previous peak, in percent")
ax.set_ylabel("%")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(base / "charts" / "more_drawdown.png", dpi=200)
plt.close(fig)

# Top holdings, Mackenzie product page, 29 Sep 2026
labels = ["Agnico Eagle Mines (AEM)", "Cenovus Energy (CVE)",
          "Canadian Natural Resources (CNQ)", "Barrick Mining (ABX)",
          "TC Energy (TRP)", "TotalEnergies", "Methanex (MX)",
          "First Quantum Minerals (FM)"]
vals = [5.93, 5.54, 4.92, 4.59, 3.71, 3.15, 2.75, 2.56]
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(labels[::-1], vals[::-1], color="#1D5C30")
ax.set_title("MORE top holdings, Mackenzie, 29 Sep 2026")
ax.set_xlabel("% of MORE")
for i, v in enumerate(vals[::-1]):
    ax.text(v + 0.1, i, f"{v:.2f}%", va="center")
ax.set_xlim(0, 7)
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(base / "charts" / "top_holdings.png", dpi=200)
plt.close(fig)
print("charts done")
