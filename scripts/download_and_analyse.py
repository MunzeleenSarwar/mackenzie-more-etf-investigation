"""MORE investigation: download CAD weekly prices, compute return and risk.
Mirrors the XEQT investigation method exactly, so the two projects are
comparable: weekly Friday prices in CAD from Yahoo Finance, adjusted for
dividends. MORE inception 10 Sep 2024, so the common window starts at the
first full week after inception for all tickers. Risk free rate for Sharpe:
2.0% per year, stated as a simple constant assumption because a daily
Canadian T-bill series is not in this download. Return/volatility is also
shown, which needs no risk free assumption.

BLEND is a 50/50 XEG/XMA portfolio, rebalanced weekly: its weekly return is
the average of the two index ETFs' weekly returns. It is the "build it by
hand" comparison for MORE, the same question the XEQT project asked about
building the mix from separate ETFs.
"""
import json
import pathlib

import numpy as np
import pandas as pd
import yfinance as yf

base = pathlib.Path(__file__).resolve().parents[1]
tickers = {"MORE": "MORE.TO", "XEG": "XEG.TO", "XMA": "XMA.TO",
           "ZEO": "ZEO.TO", "XGD": "XGD.TO", "XIC": "XIC.TO"}
frames = []
for name, sym in tickers.items():
    d = yf.download(sym, start="2024-09-09", end="2026-11-14",
                    auto_adjust=True, progress=False, timeout=60)["Close"]
    d.columns = [name]
    frames.append(d)
prices = pd.concat(frames, axis=1)
prices.columns = list(tickers.keys())
prices = prices.dropna(how="all")
weekly = prices.resample("W-FRI").last().dropna()
weekly.to_csv(base / "data" / "weekly_prices_cad.csv")
rets = weekly.pct_change().dropna()
# 50/50 XEG/XMA blend, rebalanced weekly
rets["BLEND"] = 0.5 * rets["XEG"] + 0.5 * rets["XMA"]
blend_start = pd.Series([weekly["XEG"].iloc[0]], index=[weekly.index[0]])
blend_prices = pd.concat([blend_start,
                          (1 + rets["BLEND"]).cumprod() * weekly["XEG"].iloc[0]])
weekly["BLEND"] = blend_prices
weekly = weekly[["MORE", "XEG", "XMA", "ZEO", "XGD", "XIC", "BLEND"]]
weekly.to_csv(base / "data" / "weekly_prices_cad.csv")
rets.to_csv(base / "data" / "weekly_returns.csv")


def stats(s, rf=0.02):
    ann_ret = s.mean() * 52
    vol = s.std() * np.sqrt(52)
    sharpe = (ann_ret - rf) / vol
    cum = (1 + s).cumprod()
    dd = cum / cum.cummax() - 1
    return {
        "start": str(s.index[0].date()), "end": str(s.index[-1].date()),
        "weeks": int(len(s)),
        "annual_return_pct": round(float(ann_ret * 100), 2),
        "annual_vol_pct": round(float(vol * 100), 2),
        "return_vol": round(float(ann_ret / vol), 2),
        "sharpe_rf2pct": round(float(sharpe), 2),
        "max_drawdown_pct": round(float(dd.min() * 100), 2),
        "worst_week_pct": round(float(s.min() * 100), 2),
        "weekly_cvar95_pct": round(float(s[s <= s.quantile(0.05)].mean() * 100), 2),
        "cumulative_pct": round(float((cum.iloc[-1] - 1) * 100), 2),
        "final_10000": round(float(10000 * cum.iloc[-1]), 2),
    }


out = {k: stats(rets[k]) for k in rets.columns}


def period_stats(s, a, b):
    x = s.loc[a:b]
    if len(x) < 10:
        return None
    return {"weeks": int(len(x)),
            "return_pct": round(float(x.mean() * 52 * 100), 2),
            "vol_pct": round(float(x.std() * np.sqrt(52) * 100), 2),
            "cum_pct": round(float(((1 + x).prod() - 1) * 100), 2)}


periods = {
    "2024_stub_sep_dec": ("2024-09-13", "2024-12-31"),
    "2025": ("2025-01-01", "2025-12-31"),
    "2026_ytd": ("2026-01-01", "2026-11-13"),
    "last_1y": ("2025-11-14", "2026-11-13"),
    "full": (str(rets.index[0].date()), str(rets.index[-1].date())),
}
sub = {p: {k: period_stats(rets[k], a, b) for k in rets.columns}
       for p, (a, b) in periods.items()}
growth = (1 + rets).cumprod() * 10000
growth.to_csv(base / "data" / "growth_of_10000.csv")
dd = growth / growth.cummax() - 1
dd.to_csv(base / "data" / "drawdowns.csv")
corr = rets.corr()["MORE"].round(3).to_dict()
result = {"metrics": out, "periods": sub, "corr_with_more": corr,
          "first_price": {k: round(float(weekly[k].iloc[0]), 2) for k in weekly.columns},
          "last_price": {k: round(float(weekly[k].iloc[-1]), 2) for k in weekly.columns}}
with open(base / "data" / "metrics.json", "w") as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
