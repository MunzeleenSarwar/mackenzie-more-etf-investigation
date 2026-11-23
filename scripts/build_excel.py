"""Excel model for the MORE investigation. Mirrors the XEQT model tabs:
Performance, Holdings, Calendar, Cost, Sources, Peers."""
import json
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

base = pathlib.Path(__file__).resolve().parents[1]
m = json.loads((base / "data" / "metrics.json").read_text())
wb = Workbook()
hdr_fill = PatternFill("solid", fgColor="222222")
hdr_font = Font(bold=True, color="FFFFFF", size=11)
title_font = Font(bold=True, size=14)


def sheet(name, title, rows, widths):
    ws = wb.active if len(wb.sheetnames) == 1 and wb.active.title == "Sheet" else wb.create_sheet(name)
    if ws.title != name:
        ws.title = name
    ws["A1"] = title
    ws["A1"].font = title_font
    for j, h in enumerate(rows[0], 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = hdr_font
        c.fill = hdr_fill
    for i, r in enumerate(rows[1:], 4):
        for j, v in enumerate(r, 1):
            ws.cell(row=i, column=j, value=v)
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    return ws


order = ["MORE", "XEG", "XMA", "ZEO", "XGD", "XIC", "BLEND"]
metrics = [["Fund", "Annual return %", "Volatility %", "Return / volatility",
            "Sharpe (2% risk free)", "Max drawdown %", "Worst week %",
            "Weekly CVaR 95% %", "Total gain %", "$10,000 becomes $"]]
for k in order:
    v = m["metrics"][k]
    metrics.append([k, v["annual_return_pct"], v["annual_vol_pct"], v["return_vol"],
                    v["sharpe_rf2pct"], v["max_drawdown_pct"], v["worst_week_pct"],
                    v["weekly_cvar95_pct"], v["cumulative_pct"], v["final_10000"]])
sheet("Performance", "Performance, weekly CAD, 20 Sep 2024 to 13 Nov 2026 (113 weeks)",
      metrics, [12, 16, 14, 18, 20, 16, 14, 18, 14, 16])

hold = [["Holding", "Weight, 29 Sep 2026 % (Mackenzie product page)"],
        ["Agnico Eagle Mines (AEM)", 5.93],
        ["Cenovus Energy (CVE)", 5.54],
        ["Canadian Natural Resources (CNQ)", 4.92],
        ["Barrick Mining (ABX)", 4.59],
        ["TC Energy (TRP)", 3.71],
        ["TotalEnergies", 3.15],
        ["Methanex (MX)", 2.75],
        ["First Quantum Minerals (FM)", 2.56],
        ["Top 8 holdings together", 38.15],
        ["Total holdings in the fund", "83 equities, plus 1 fixed income holding"],
        ["Sector split, 31 Mar 2025 (MRFP)", "Energy 54.3%, Materials 38.3%, Other 4.2%"]]
sheet("Holdings", "MORE top holdings", hold, [48, 52])

cal = [["Period", "MORE total %", "XEG total %", "XMA total %", "ZEO total %",
        "XGD total %", "XIC total %", "BLEND total %"]]
labels = {"2024_stub_sep_dec": "2024 (20 Sep to 31 Dec)", "2025": "2025",
          "2026_ytd": "2026 (1 Jan to 13 Nov)"}
for p, label in labels.items():
    cal.append([label] + [m["periods"][p][k]["cum_pct"] for k in order])
sheet("Calendar", "Total return by period, Yahoo adjusted weekly prices",
      cal, [26, 14, 14, 14, 14, 14, 14, 14])


def fv20(fee):
    return round(100000 * (1.07 - fee) ** 20)


cost = [["Option", "Annual fee %", "Fee on $100,000 per year $",
         "Illustrative $100,000 after 20 years at 7% gross $"],
        ["MORE", 0.84, 840, fv20(0.0084)],
        ["50/50 XEG/XMA blend, both funds at 0.61%", 0.61, 610, fv20(0.0061)],
        ["Mutual fund at 2.00% (illustration only)", 2.00, 2000, fv20(0.02)]]
sheet("Cost", "Cost illustration only. Gross return is assumed constant at 7% and never happens in practice.",
      cost, [52, 16, 28, 48])

src = [["Item", "Source and date"],
       ["MER 0.84%, management fee 0.75%, launch 10 Sep 2024, reference S&P/TSX Energy + S&P/TSX Materials",
        "Mackenzie Core Resources ETF, Annual Management Report of Fund Performance, period ended 31 Mar 2025; Mackenzie product page, updated 12 Nov 2026"],
       ["Top holdings and holding count",
        "Mackenzie product page, major holdings as of 29 Sep 2026; 83 equities plus 1 fixed income holding as of 30 Oct 2026"],
       ["Price history and risk measures",
        "Yahoo Finance adjusted closes, weekly Friday, 20 Sep 2024 to 13 Nov 2026"],
       ["Sharpe risk free rate", "2.0% per year, stated assumption, not a market series"],
       ["Peer MERs", "XEG, XMA, ZEO, XGD 0.61% in recent third-party checks; XIC 0.06%"]]
sheet("Sources", "Sources and method notes", src, [52, 110])

peers = [["Fund", "Provider and type", "Fee"],
         ["MORE", "Mackenzie. Active, discretionary, Canadian natural resources: energy, materials, precious metals.",
          "MER 0.84%. Management fee 0.75%."],
         ["XEG", "BlackRock iShares. Passive, S&P/TSX Capped Energy Index.", "MER 0.61%. Management fee 0.55%."],
         ["XMA", "BlackRock iShares. Passive, S&P/TSX Capped Materials Index.", "MER 0.61%. Management fee 0.55%."],
         ["ZEO", "BMO. Passive, Solactive Equal Weight Canada Oil and Gas Index.", "MER 0.61%."],
         ["XGD", "BlackRock iShares. Passive, S&P/TSX Global Gold Index.", "MER 0.61%. Management fee 0.55%."],
         ["XIC", "BlackRock iShares. Passive, S&P/TSX Capped Composite Index.", "MER 0.06%."]]
sheet("Peers", "Resource peers and the broad market", peers, [12, 78, 52])

f = json.loads((base / "data" / "forecast.json").read_text())
ws = wb.create_sheet("Forecast")
ws["A1"] = "Forecast: Monte Carlo and commodity scenarios, from $38.02 on 13 Nov 2026"
ws["A1"].font = title_font
ws["A3"] = "Monte Carlo: 10,000 paths over 52 weeks, weekly steps, seed 42"
ws["A3"].font = Font(bold=True, size=11)
mc_rows = [["Drift", "Drift % per year", "Median price in 1 year $", "Median gain %",
            "5th percentile price $", "95th percentile price $", "Chance of a loss %",
            "VaR 95% %", "CVaR 95% %", "Median $10,000", "5th percentile $10,000",
            "95th percentile $10,000"]]
for name, label in [("historical", "Historical (MORE average)"),
                    ("conservative_7pct", "Conservative (7% a year)")]:
    v = f["monte_carlo"][name]
    mc_rows.append([label, v["drift_annual_pct"], v["median_terminal"], v["median_gain_pct"],
                    v["p5_terminal"], v["p95_terminal"], v["prob_loss_pct"], v["var95_pct"],
                    v["cvar95_pct"], v["median_10000"], v["p5_10000"], v["p95_10000"]])
for j, h in enumerate(mc_rows[0], 1):
    c = ws.cell(row=4, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, r in enumerate(mc_rows[1:], 5):
    for j, v in enumerate(r, 1):
        ws.cell(row=i, column=j, value=v)
for j, w in enumerate([30, 16, 22, 14, 20, 20, 18, 12, 12, 16, 20, 20], 1):
    ws.column_dimensions[get_column_letter(j)].width = w
r = 8
ws.cell(row=r, column=1, value="Factor regression: MORE weekly return on WTI oil, gold, and XIC, 113 weeks").font = Font(bold=True, size=11)
r += 1
reg_rows = [["Factor", "Beta", "Standard error", "t-statistic"]]
for n in ["alpha", "WTI", "Gold", "XIC"]:
    v = f["regression"][n]
    reg_rows.append([n, v["beta"], v["se"], v["t"]])
reg_rows.append(["R squared", f["regression"]["r2"], "", ""])
reg_rows.append(["Residual volatility, annualised %", f["regression"]["resid_vol_annual_pct"], "", ""])
for j, h in enumerate(reg_rows[0], 1):
    c = ws.cell(row=r, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, row in enumerate(reg_rows[1:], r + 1):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
r = r + len(reg_rows) + 2
ws.cell(row=r, column=1, value="Commodity scenarios: assumed one-year factor moves and the implied MORE move").font = Font(bold=True, size=11)
r += 1
sc_rows = [["Scenario", "Oil move %", "Gold move %", "TSX move %", "Implied MORE move %"]]
for s in f["scenarios"]:
    sc_rows.append([s["scenario"], s["oil_move_pct"], s["gold_move_pct"],
                    s["tsx_move_pct"], s["implied_more_move_pct"]])
for j, h in enumerate(sc_rows[0], 1):
    c = ws.cell(row=r, column=j, value=h)
    c.font = hdr_font
    c.fill = hdr_fill
for i, row in enumerate(sc_rows[1:], r + 1):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
wb.save(base / "MORE_Investigation_Model.xlsx")
print("excel done")
