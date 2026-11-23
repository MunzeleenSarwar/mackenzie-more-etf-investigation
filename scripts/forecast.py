"""MORE forecasting: Monte Carlo fan chart and commodity scenarios.

Two methods, both honest about the short window (113 weeks):

1. Monte Carlo. 10,000 paths over the next 52 weeks, weekly steps, starting
   at the last weekly close (13 Nov 2026). Weekly returns drawn from a normal
   distribution with MORE's own weekly volatility. Two drifts:
   (a) historical: MORE's average weekly return over the window;
   (b) conservative: 7% a year, the long-run teaching assumption used in the
   cost illustration. The historical drift is shown first, but its standard
   error is about 13 points a year, so it is not a forecast of the return.
   Output is a range of outcomes, not a point prediction.

2. Commodity scenarios. MORE weekly returns regressed on three weekly
   factors: WTI crude (CL=F), gold (GC=F), and the broad TSX (XIC). The
   betas are then applied to assumed one-year factor moves to give an implied
   one-year MORE move for each scenario. The mapping is linear and assumes
   the weekly relationship holds over a year, which is an approximation.
   Betas come from 113 weeks, so they are noisy.

Seed is fixed so the simulation reproduces exactly.
"""
import json
import pathlib

import numpy as np
import pandas as pd
import yfinance as yf

base = pathlib.Path(__file__).resolve().parents[1]
rng = np.random.default_rng(42)
N_PATHS = 10000
WEEKS = 52

rets = pd.read_csv(base / "data" / "weekly_returns.csv", index_col=0, parse_dates=True)
more = rets["MORE"]
mu_w = float(more.mean())
sigma_w = float(more.std())
start_price = float(pd.read_csv(base / "data" / "weekly_prices_cad.csv",
                                index_col=0, parse_dates=True)["MORE"].iloc[-1])
se_annual = 52 * sigma_w / np.sqrt(len(more))

# ---------------------------------------------------------- 1. Monte Carlo
drifts = {"historical": mu_w, "conservative_7pct": 0.07 / 52}
mc = {}
fan = {}
for name, mu in drifts.items():
    draws = rng.normal(mu, sigma_w, size=(N_PATHS, WEEKS))
    paths = start_price * np.cumprod(1 + draws, axis=1)
    paths = np.hstack([np.full((N_PATHS, 1), start_price), paths])
    terminal = paths[:, -1]
    pct = np.percentile(paths, [5, 25, 50, 75, 95], axis=0)
    fan[name] = pd.DataFrame(
        {"p5": pct[0], "p25": pct[1], "median": pct[2], "p75": pct[3], "p95": pct[4]},
        index=pd.date_range("2026-11-20", periods=WEEKS + 1, freq="W-FRI"))
    mc[name] = {
        "drift_annual_pct": round(float(mu * 52 * 100), 2),
        "median_terminal": round(float(np.median(terminal)), 2),
        "mean_terminal": round(float(terminal.mean()), 2),
        "p5_terminal": round(float(np.percentile(terminal, 5)), 2),
        "p95_terminal": round(float(np.percentile(terminal, 95)), 2),
        "median_gain_pct": round(float((np.median(terminal) / start_price - 1) * 100), 2),
        "p5_gain_pct": round(float((np.percentile(terminal, 5) / start_price - 1) * 100), 2),
        "p95_gain_pct": round(float((np.percentile(terminal, 95) / start_price - 1) * 100), 2),
        "prob_loss_pct": round(float((terminal < start_price).mean() * 100), 2),
        "var95_pct": round(float((1 - np.percentile(terminal, 5) / start_price) * 100), 2),
        "cvar95_pct": round(float((1 - terminal[terminal <= np.percentile(terminal, 5)].mean()
                                   / start_price) * 100), 2),
        "median_10000": round(float(10000 * np.median(terminal) / start_price), 2),
        "p5_10000": round(float(10000 * np.percentile(terminal, 5) / start_price), 2),
        "p95_10000": round(float(10000 * np.percentile(terminal, 95) / start_price), 2),
    }
    fan[name].to_csv(base / "data" / f"monte_carlo_fan_{name}.csv")
print("start price:", start_price)
print("weekly mean %:", round(mu_w * 100, 3), "weekly vol %:", round(sigma_w * 100, 3),
      "SE of annual return (points):", round(se_annual * 100, 2))
print(json.dumps(mc, indent=2))

# ------------------------------------------- 2. factor regression + scenarios
frames = []
for name, sym in {"WTI": "CL=F", "Gold": "GC=F"}.items():
    d = yf.download(sym, start="2024-09-09", end="2026-11-14",
                    auto_adjust=True, progress=False, timeout=60)["Close"]
    d.columns = [name]
    frames.append(d)
fac = pd.concat(frames, axis=1).resample("W-FRI").last().dropna()
fac_rets = fac.pct_change().dropna()
df = pd.concat([more.rename("MORE"), fac_rets, rets["XIC"]], axis=1, join="inner").dropna()
print("regression weeks:", len(df))
X = np.column_stack([np.ones(len(df)), df["WTI"], df["Gold"], df["XIC"]])
y = df["MORE"].values
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
resid = y - X @ beta
dof = len(df) - X.shape[1]
s2 = float(resid @ resid / dof)
cov = s2 * np.linalg.inv(X.T @ X)
se = np.sqrt(np.diag(cov))
tstat = beta / se
ybar = y.mean()
r2 = 1 - float(resid @ resid) / float(((y - ybar) ** 2).sum())
names = ["alpha", "WTI", "Gold", "XIC"]
reg = {"weeks": int(len(df)), "r2": round(float(r2), 3),
       "resid_vol_annual_pct": round(float(np.sqrt(s2) * np.sqrt(52) * 100), 2)}
for n, b, s, t in zip(names, beta, se, tstat):
    reg[n] = {"beta": round(float(b), 3), "se": round(float(s), 3),
              "t": round(float(t), 2)}
print(json.dumps(reg, indent=2))
print("factor correlations with MORE:")
print(df.corr()["MORE"].round(3).to_string())

scenarios = [
    ("Base: oil +5%, gold +5%, TSX +7%", 0.05, 0.05, 0.07),
    ("Energy rally: oil +20%, gold 0%, TSX +10%", 0.20, 0.00, 0.10),
    ("Gold rally: oil 0%, gold +20%, TSX +5%", 0.00, 0.20, 0.05),
    ("Both fall: oil -20%, gold -10%, TSX -10%", -0.20, -0.10, -0.10),
    ("Oil crash, gold safety: oil -30%, gold +10%, TSX -5%", -0.30, 0.10, -0.05),
]
alpha_ann = float(beta[0]) * 52
out = []
for label, o, g, t in scenarios:
    implied = alpha_ann + float(beta[1]) * o + float(beta[2]) * g + float(beta[3]) * t
    out.append({"scenario": label, "oil_move_pct": o * 100, "gold_move_pct": g * 100,
                "tsx_move_pct": t * 100, "implied_more_move_pct": round(float(implied * 100), 2)})
print(json.dumps(out, indent=2))

result = {"start_price": start_price, "weeks": int(len(more)),
          "weekly_mean_pct": round(mu_w * 100, 3),
          "weekly_vol_pct": round(sigma_w * 100, 3),
          "se_annual_return_points": round(float(se_annual * 100), 2),
          "monte_carlo": mc, "regression": reg, "scenarios": out}
with open(base / "data" / "forecast.json", "w") as f:
    json.dump(result, f, indent=2)
print("forecast done")
