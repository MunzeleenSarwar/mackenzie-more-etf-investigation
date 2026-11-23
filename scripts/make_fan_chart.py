"""Monte Carlo fan chart for MORE. Colours are for charts only, per her rule.
Historical drift: shaded 5th to 95th percentile band with the median line.
Conservative drift (7% a year): dashed median line for comparison.
Both start at the last weekly close, $38.02 on 13 Nov 2026.
"""
import pathlib

import matplotlib.pyplot as plt
import pandas as pd

base = pathlib.Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
hist = pd.read_csv(base / "data" / "monte_carlo_fan_historical.csv", index_col=0, parse_dates=True)
cons = pd.read_csv(base / "data" / "monte_carlo_fan_conservative_7pct.csv", index_col=0, parse_dates=True)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.fill_between(hist.index, hist["p5"], hist["p95"], alpha=0.25, color="#1D5C30",
                label="Historical drift, 5th to 95th percentile")
ax.plot(hist.index, hist["median"], color="#1D5C30", linewidth=2.5,
        label="Historical drift (31.4% a year), median")
ax.plot(cons.index, cons["median"], color="#111111", linewidth=2, linestyle="--",
        label="Conservative drift (7% a year), median")
ax.axhline(38.02, color="#9CA3AF", linewidth=1, linestyle=":")
ax.set_title("MORE Monte Carlo: 10,000 paths over the next year, from $38.02")
ax.set_ylabel("Price, CAD")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(base / "charts" / "monte_carlo_fan.png", dpi=200)
plt.close(fig)
print("fan chart done")
