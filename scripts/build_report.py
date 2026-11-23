"""MORE report PDF. Black text only. Charts may use colour. No first person.
Name appears only on the title line. Mirrors the XEQT report, with a
forecasting section added at the user's choice."""
import json
import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

base = pathlib.Path(__file__).resolve().parents[1]
m = json.loads((base / "data" / "metrics.json").read_text())
f = json.loads((base / "data" / "forecast.json").read_text())
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.black, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.black, spaceBefore=12, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.black, spaceBefore=10, spaceAfter=6)
small = ParagraphStyle("small", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black, spaceAfter=4)


def P(t, s=body):
    return Paragraph(t, s)


cell = ParagraphStyle("cell", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.black)
cellhead = ParagraphStyle("cellhead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.black)


def tbl(data, widths):
    wrapped = [[Paragraph(str(c), cellhead if r == 0 else cell) for c in row] for r, row in enumerate(data)]
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def img(name, w=170 * mm):
    return Image(str(base / "charts" / name), width=w, height=w * 0.55)


story = []
story.append(P("Investigating MORE: What One Ticker Buys, What It Costs, and What Risk It Carries", h1))
story.append(P("Munzeleen Sarwar", body))
story.append(P("Mackenzie Core Resources ETF, TSX: MORE. Price data to 13 November 2026. This report is an investigation, not personal investment advice.", small))
story.append(P("Summary", h1))
story.append(P("MORE is an actively managed fund that buys Canadian natural resource stocks: energy, materials, and precious metals. It launched in September 2024, so this report covers only two years, 113 weeks of prices. That short window is the most important fact in the report. Every return and risk number in it comes from a strong two-year bull period for resources, and the numbers would look different over a longer period that included a real bear market."))
story.append(P("The main findings are simple. First, MORE turned $10,000 into $18,981 over the two years, a gain of 89.81%. Second, two cheap index funds bought together, half XEG and half XMA, turned $10,000 into $20,266, a gain of 102.66%, with almost the same risk-adjusted return. Third, MORE earned its return with the smoothest ride of any resource fund in the group: volatility of 19.01% a year and a worst fall of 10.76%, against 27.14% and 19.28% for XEG and 43.44% and 35.86% for the gold miners fund XGD. Fourth, the two years split cleanly in half: 2025 was the gold year and 2026 was the energy year, and MORE matched the index blend in the first and lagged it in the second. Fifth, forecasting is only possible as a range, not a point: the Monte Carlo gives a median of $51.02 in a year on the historical drift and $40.14 on a conservative 7% drift, from $38.02 today."))
story.append(P("Key facts", h2))
story.append(tbl([
["Item", "Detail"],
["Launch date", "10 September 2024, first trading day 9 September 2024"],
["Type", "Active ETF, discretionary, Canadian natural resources"],
["Reference", "S and P/TSX Energy plus S and P/TSX Materials"],
["Management expense ratio", "0.84% per year (Management Report of Fund Performance, period ended 31 March 2025)"],
["Management fee", "0.75% per year"],
["Distributions", "Quarterly"],
["12 month distributions to November 2026", "$1.12 per unit, a yield of about 3% (third-party check)"],
["Net assets", "$36.6 million at 31 March 2025, about $115 million in November 2026 (third-party checks)"],
["Price, weekly close 13 November 2026", "$38.02 CAD (Yahoo Finance adjusted close)"],
], [62 * mm, 108 * mm]))
story.append(P("1. What MORE buys", h1))
story.append(P("MORE buys stocks, not an index. A manager at Mackenzie picks the weights. The fund held 83 equities plus one fixed income holding at 30 October 2026. The top eight holdings at 29 September 2026 were Agnico Eagle Mines at 5.93%, Cenovus Energy at 5.54%, Canadian Natural Resources at 4.92%, Barrick Mining at 4.59%, TC Energy at 3.71%, TotalEnergies at 3.15%, Methanex at 2.75%, and First Quantum Minerals at 2.56%. Together the top eight were 38.15% of the fund. The sector split at 31 March 2025 was energy 54.3%, materials 38.3%, and other 4.2%."))
story.append(tbl([
["Holding", "Weight, 29 Sep 2026"],
["Agnico Eagle Mines (AEM)", "5.93%"],
["Cenovus Energy (CVE)", "5.54%"],
["Canadian Natural Resources (CNQ)", "4.92%"],
["Barrick Mining (ABX)", "4.59%"],
["TC Energy (TRP)", "3.71%"],
["TotalEnergies", "3.15%"],
["Methanex (MX)", "2.75%"],
["First Quantum Minerals (FM)", "2.56%"],
["Top 8 holdings together", "38.15%"],
], [110 * mm, 60 * mm]))
story.append(img("top_holdings.png"))
story.append(P("Source for weights: Mackenzie product page, major holdings as of 29 September 2026. Sector split source: Annual Management Report of Fund Performance, period ended 31 March 2025."))
story.append(P("Two points matter here. First, the top holdings are the same large names that dominate the energy and materials indexes. Canadian Natural Resources, Cenovus, Agnico Eagle, and Barrick are also the largest holdings of XEG and XMA. The difference between MORE and the index funds is therefore not in the top names. It is in the smaller positions, in the balance between energy and materials, and in the gold tilt. Second, MORE also holds purchased call options, about 4.2% of net assets at 31 March 2025 and 5.2% at 31 December 2025, mostly calls on the gold miners ETF. Those options add leveraged exposure to gold on top of the stocks. The index funds hold no options."))
story.append(P("One more fact about size. At 31 March 2025, funds managed by I.G. Investment Management owned 83.7% of MORE's units. The fund has grown since then, to about $115 million in November 2026 from $36.6 million in March 2025, but it is still small next to XEG at over $1 billion and XGD at over $3.5 billion. A small fund can be harder to trade in large size, and its costs are spread over fewer assets."))
story.append(P("2. How MORE performed", h1))
story.append(P("The table below uses weekly prices in Canadian dollars from 20 September 2024 to 13 November 2026, a total of 113 weeks. Prices are adjusted for dividends and splits. Annual return is the average weekly return multiplied by 52. Volatility is the standard deviation of weekly returns multiplied by the square root of 52. Sharpe ratio uses a stated 2.0% risk free rate, because a daily Canadian T-bill series was not in this download. Return divided by volatility is also shown, because it needs no risk free assumption. BLEND is a 50/50 portfolio of XEG and XMA, rebalanced weekly. It is the do-it-yourself version of MORE."))
story.append(tbl([
["Fund", "Annual return", "Volatility", "Return / volatility", "Sharpe", "Max fall", "$10,000 becomes"],
["MORE", "31.37%", "19.01%", "1.65", "1.54", "-10.76%", "$18,981"],
["XEG (energy)", "32.34%", "27.14%", "1.19", "1.12", "-19.28%", "$18,598"],
["XMA (materials)", "37.31%", "37.15%", "1.00", "0.95", "-31.70%", "$19,367"],
["ZEO (oil and gas, equal weight)", "26.96%", "21.99%", "1.23", "1.14", "-14.73%", "$17,026"],
["XGD (gold miners)", "46.63%", "43.44%", "1.07", "1.03", "-35.86%", "$22,486"],
["XIC (broad TSX)", "22.74%", "11.29%", "2.01", "1.84", "-8.77%", "$16,150"],
["BLEND (50/50 XEG/XMA)", "34.82%", "21.13%", "1.65", "1.55", "-11.32%", "$20,266"],
], [42 * mm, 22 * mm, 20 * mm, 26 * mm, 16 * mm, 20 * mm, 24 * mm]))
story.append(img("growth_of_10000.png"))
story.append(P("Over the full period, MORE turned $10,000 into $18,981. The blend turned it into $20,266, which is $1,285 more. The gold miners fund turned it into $22,486, but with more than twice the volatility. The broad market fund, XIC, turned it into $16,150, the least in the group, but with the lowest volatility and the best Sharpe ratio at 1.84. The Sharpe ratios tell the story in one line: MORE at 1.54 and the blend at 1.55 are effectively tied, XIC is ahead at 1.84, and the single-sector funds are behind at 0.95 to 1.14."))
story.append(P("The two years split cleanly. In 2025, gold ran: XGD gained 151.76% and XMA gained 104.43%, while XEG gained only 16.94%. MORE gained 56.08% and the blend gained 56.53%, almost the same. In 2026 to 13 November, energy ran: XEG gained 55.28% and ZEO gained 42.98%, while XMA lost 1.48% and XGD lost 1.32%. MORE gained 20.51% and the blend gained 30.00%. MORE matched the blend in the gold year and lagged it in the energy year, because the blend holds more energy through XEG and no gold options drag when gold stalls."))
story.append(tbl([
["Period", "MORE", "XEG", "XMA", "ZEO", "XGD", "XIC", "BLEND"],
["2024 (20 Sep to 31 Dec)", "0.92%", "2.42%", "-3.84%", "4.00%", "-9.49%", "5.99%", "-0.40%"],
["2025", "56.08%", "16.94%", "104.43%", "14.51%", "151.76%", "32.50%", "56.53%"],
["2026 (1 Jan to 13 Nov)", "20.51%", "55.28%", "-1.48%", "42.98%", "-1.32%", "15.00%", "30.00%"],
["Last 12 months", "38.40%", "57.69%", "18.67%", "45.39%", "20.77%", "23.47%", "44.15%"],
], [38 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm]))
story.append(P("3. Risk in plain terms", h1))
story.append(P("Volatility measures how much weekly returns move around their average. MORE volatility was 19.01% per year. That is the lowest of any resource fund in the group, against 27.14% for XEG, 37.15% for XMA, and 43.44% for XGD. It is still far above the broad market at 11.29%. MORE is a smoother resource fund, not a calm fund."))
story.append(P("Maximum drawdown measures the largest fall from a previous peak to a later low. For MORE, the largest fall was 10.76%, and the whole fall happened in a single week in April 2025, when tariff news hit markets. In plain terms, $10,000 at the previous peak fell to about $8,924 in that week, before recovering. XEG fell 19.28% from peak to low, XMA fell 31.70%, and XGD fell 35.86%. XIC fell 8.77%, less than MORE, because the broad market holds banks, telecoms, and other sectors that do not move with commodities."))
story.append(img("more_drawdown.png"))
story.append(P("Weekly CVaR at 95% measures the average loss in the worst 5% of weeks. For MORE, that average was a loss of 5.26% in a bad week. For the blend, it was 5.50%. For XEG, it was 8.58%. For XMA, it was 10.57%. For XGD, it was 10.92%. CVaR is useful because it looks only at bad weeks. Volatility looks at good and bad weeks together. A portfolio can look calm on average and still lose a lot in a bad week."))
story.append(P("4. MORE against its neighbours", h1))
story.append(P("The closest comparison is the blend, because MORE's own reference is the energy index plus the materials index. Over the two years, the blend returned more, at 34.82% a year against 31.37% for MORE, with slightly higher volatility, at 21.13% against 19.01%. The two funds moved together closely, with a weekly correlation of 0.954, where 1.00 means they move together exactly. The difference between them is therefore small: the blend is two index funds at 0.61% a year, and MORE is one active fund at 0.84% a year, with a smoother ride and a gold options overlay."))
story.append(tbl([
["Fund", "Provider and type", "Fee"],
["MORE", "Mackenzie. Active, discretionary, Canadian natural resources: energy, materials, precious metals.", "MER 0.84%. Management fee 0.75%."],
["XEG", "BlackRock iShares. Passive, S and P/TSX Capped Energy Index.", "MER 0.61%. Management fee 0.55%."],
["XMA", "BlackRock iShares. Passive, S and P/TSX Capped Materials Index.", "MER 0.61%. Management fee 0.55%."],
["ZEO", "BMO. Passive, Solactive Equal Weight Canada Oil and Gas Index.", "MER 0.61%."],
["XGD", "BlackRock iShares. Passive, S and P/TSX Global Gold Index.", "MER 0.61%. Management fee 0.55%."],
["XIC", "BlackRock iShares. Passive, S and P/TSX Capped Composite Index.", "MER 0.06%."],
], [22 * mm, 78 * mm, 70 * mm]))
story.append(P("MORE behaves more like a materials and gold fund than an energy fund. Its weekly correlation with XEG is only 0.517, against 0.708 with XMA and 0.652 with XGD. Its correlation with the broad market is 0.642. That matches the holdings: the largest positions are gold miners, and the options overlay is on gold. A holder who buys MORE for energy exposure is getting less of it than the name suggests, and more gold."))
story.append(P("XIC is the useful contrast. It returned less over the two years, at 22.74% a year, but with half the volatility of MORE and the best Sharpe ratio in the group. Resource funds beat the broad market in this window because commodities ran. In a window where commodities fall, the same funds would lag, and by more. Two years that include a gold rally and an energy rally flatter every resource fund in this report."))
story.append(P("5. Cost: MORE, building it by hand, and a mutual fund", h1))
story.append(P("MORE charges 0.84% per year. On $100,000, that is $840 per year. The fee is taken inside the fund, so the holder does not pay a separate bill."))
story.append(P("Building the same mix by hand means buying XEG and XMA in equal parts. Both charge 0.61% per year, so the blend costs 0.61% per year, or $610 per year on $100,000. The saving is $230 per year on $100,000. That is real, and it is larger than the $85 saving in the XEQT investigation, because the fee gap is wider: 0.23 points here against 0.08 points there."))
story.append(tbl([
["Option", "Fee per year", "Fee on $100,000 per year", "Illustrative value after 20 years"],
["MORE at 0.84%", "0.84%", "$840", "$330,536"],
["50/50 XEG/XMA blend at 0.61%", "0.61%", "$610", "$345,157"],
["Mutual fund at 2.00%, illustration only", "2.00%", "$2,000", "$265,330"],
], [58 * mm, 28 * mm, 42 * mm, 42 * mm]))
story.append(P("The illustration assumes a constant gross return of 7% per year, which never happens in practice. It is shown only to make the fee difference visible. After 20 years, the blend is ahead by $14,621 on $100,000 in this illustration, before trading costs, time, and tax records. The mutual fund illustration is behind by $65,206, which shows why a 2% fee matters far more than a 0.23% fee difference."))
story.append(P("Building by hand also has costs that are not in the fee. Each rebalance needs trades. Each trade can have a spread, which is the gap between the buy price and the sell price. The holder must track the weights, decide when to rebalance, and keep tax records for each fund. MORE does that work inside one fund, and it adds active decisions and the options overlay that the blend does not have. Whether $230 per year on $100,000 is a fair price for that depends on whether the active decisions add value. Over these two years, they did not: the blend returned more. Two years is not enough to judge a manager, but it is enough to say the fee has not paid for itself yet."))
story.append(P("6. Control: what MORE does not let the holder change", h1))
story.append(P("MORE fixes nothing and lets the holder change nothing. The manager decides the balance between energy, materials, and gold, decides which names to hold, and decides how much of the fund sits in call options. The holder cannot raise the energy weight before an energy rally, or cut gold before gold stalls. The blend, by contrast, lets the holder set the mix: half energy and half materials here, but any split the holder chooses."))
story.append(P("Control helps in some years and hurts in others. In 2025, gold ran and energy lagged, so more gold would have helped. In 2026, energy ran and gold stalled, so more energy would have helped. Having control only helps if the right shift can be made before the year starts. Most holders cannot do that reliably, and neither can most managers."))
story.append(P("Distributions and tax need a short note. MORE pays distributions quarterly. The 12 month distributions to November 2026 were $1.12 per unit, a yield of about 3%. Distributions are taxable in a non-registered account, and the type of distribution matters. Foreign withholding tax can also apply inside the fund, for example on TotalEnergies. The size of that effect depends on the account type and the holder's tax situation. This report does not give personal tax advice. A holder should check the tax treatment for a registered account and a non-registered account separately."))
story.append(P("7. Forecasting: a range, not a prediction", h1))
story.append(P("Two years of data cannot support a point forecast. MORE's annualised return over the window is 31.37%, but the standard error on that estimate is about 12.9 points. That means the data is consistent with a true long-run return anywhere from roughly 6% to 57% a year. Any forecast that takes 31% and projects it forward would be dressing up noise as a prediction. The two methods below give a range of outcomes instead, and both are shown with their limits."))
story.append(P("7.1 Monte Carlo", h2))
story.append(P("The Monte Carlo runs 10,000 paths over the next 52 weeks, in weekly steps, starting at $38.02, the last weekly close. Weekly returns are drawn from a normal distribution with MORE's own weekly volatility of 2.64%. Two drifts are used. The historical drift is MORE's average weekly return, 31.37% a year. The conservative drift is 7% a year, the long-run teaching assumption used in the cost illustration. The seed is fixed, so the simulation reproduces exactly."))
story.append(tbl([
["Drift", "Median price in 1 year", "Median gain", "5th percentile", "95th percentile", "Chance of a loss", "VaR 95%", "CVaR 95%"],
["Historical, 31.37% a year", "$51.02", "+34.18%", "$37.27", "$69.67", "6.1%", "1.97%", "9.01%"],
["Conservative, 7% a year", "$40.14", "+5.58%", "$29.41", "$54.37", "38.6%", "22.64%", "28.64%"],
], [36 * mm, 26 * mm, 18 * mm, 22 * mm, 22 * mm, 22 * mm, 14 * mm, 14 * mm]))
story.append(img("monte_carlo_fan.png"))
story.append(P("On the historical drift, the median path ends at $51.02, and $10,000 becomes $13,418. The 5th percentile ends at $37.27, just below today's price, and the 95th percentile ends at $69.67. The chance of a loss over the year is only 6.1%, because a 31% drift is so strong that it overwhelms the volatility. On the conservative drift, the median ends at $40.14, and $10,000 becomes $10,558. The 5th percentile ends at $29.41, a fall of 22.64%, and the chance of a loss is 38.6%. The honest reading is the gap between the two: the drift assumption, not the volatility, decides whether the next year looks good. And the drift is the least certain number in the whole report."))
story.append(P("The normal distribution is also a limit. Real weekly returns have fatter tails than a normal distribution: big weeks happen more often than the model allows. The April 2025 week, a fall of 10.76% in one week, is an example. The simulation therefore understates the chance of a very bad week."))
story.append(P("7.2 Commodity scenarios", h2))
story.append(P("MORE's returns are driven by oil, gold, and the broad market, so the second method regresses MORE's weekly returns on those three factors over the same 113 weeks. The regression explains 63.4% of the weekly moves. The betas are: WTI oil 0.132, gold 0.321, and XIC 0.957, all statistically significant, with an alpha of essentially zero. The residual volatility is 11.66% a year, which is the part of MORE's movement that oil, gold, and the market do not explain."))
story.append(tbl([
["Factor", "Beta", "Standard error", "t-statistic"],
["Alpha", "-0.000", "0.002", "-0.0"],
["WTI crude oil", "0.132", "0.023", "5.71"],
["Gold", "0.321", "0.055", "5.79"],
["XIC (broad TSX)", "0.957", "0.106", "8.99"],
["R squared", "0.634", "", ""],
["Residual volatility, annualised", "11.66%", "", ""],
], [52 * mm, 30 * mm, 38 * mm, 30 * mm]))
story.append(P("The XIC beta of 0.957 dominates. MORE moves almost one-for-one with the broad Canadian market. The commodity betas are the extra tilt on top. The gold beta of 0.321 is the larger tilt, and the oil beta of 0.132 is small once the market is in the model, because the TSX already contains a large energy weight and absorbs much of the oil effect. That is why an oil rally alone does less for MORE than the name suggests."))
story.append(P("The scenarios below apply those betas to assumed one-year moves in oil, gold, and the TSX. The mapping is linear and assumes the weekly relationship holds over a year, which is an approximation. The scenarios are what-ifs, not forecasts: they say what MORE does if commodities do something, not what commodities will do."))
story.append(tbl([
["Scenario", "Oil", "Gold", "TSX", "Implied MORE move"],
["Base: oil +5%, gold +5%, TSX +7%", "+5%", "+5%", "+7%", "+8.94%"],
["Energy rally: oil +20%, gold 0%, TSX +10%", "+20%", "0%", "+10%", "+12.19%"],
["Gold rally: oil 0%, gold +20%, TSX +5%", "0%", "+20%", "+5%", "+11.18%"],
["Both fall: oil -20%, gold -10%, TSX -10%", "-20%", "-10%", "-10%", "-15.45%"],
["Oil crash, gold safety: oil -30%, gold +10%, TSX -5%", "-30%", "+10%", "-5%", "-5.57%"],
], [62 * mm, 22 * mm, 22 * mm, 22 * mm, 42 * mm]))
story.append(P("Three points stand out. First, the base scenario gives only +8.94%, far below the Monte Carlo median on the historical drift, because the betas are estimated over a period when the market did much of the work. Second, the energy rally and the gold rally give similar results, +12.19% and +11.18%, even though the oil move is the same size as the gold move, because the gold beta is more than twice the oil beta. Third, the oil crash scenario is the most interesting: oil down 30% with gold up 10% still leaves MORE down 5.57%, because the TSX falls too and gold cannot offset both. MORE is not a hedge against an oil crash. It is a resource fund, and it falls when resources fall."))
story.append(P("8. Verdict: who MORE fits, and who it does not fit", h1))
story.append(P("MORE fits a holder who meets all of these points. The money is for the long term, at least 10 years and preferably longer. The holder wants Canadian resource exposure in one fund and does not want to rebalance between energy and materials. The holder accepts that the return will follow commodities, including bad years, and can accept a fall of at least 11% in a week, as happened in April 2025, and larger falls over longer windows, as the peer funds show. The holder accepts paying 0.84% a year for active management and an options overlay, on the view that the manager's tilts will add value over time."))
story.append(P("MORE does not fit a holder who needs the money in the next few years. It does not fit a holder who needs regular income, because the yield is about 3% and it varies. It does not fit a holder who wants a pure energy fund, because MORE behaves more like a materials and gold fund, with a correlation of only 0.517 with XEG. It does not fit a holder who wants the cheapest resource exposure, because two index funds at 0.61% beat it on return over these two years and cost $230 less per year on $100,000. For that holder, the 50/50 blend is a closer fit, at the cost of doing the rebalancing and giving up the active tilts. It also does not fit a holder who wants a long track record, because two years is not enough to judge a fund or a manager."))
story.append(P("The final point is about comparison. MORE should not be judged by one good year or one bad year, and it should not be judged on two years at all. Over the two years in this report, it delivered a high return with moderate volatility for a resource fund, smoother than every single-sector peer, but behind a simple blend of two index funds. That is what an active resource fund with a gold tilt is expected to do in a window where gold ran first and energy ran second. The value of MORE is not that it beats every other fund. The value is that it gives diversified Canadian resource exposure in one ticker, with the manager making the sector calls, at a fee that is high for an index fund and low for an active one."))
story.append(P("9. What was learned from this project", h1))
story.append(P("1. Two years is not enough to judge a fund. MORE has 113 weeks of prices against 375 for XEQT. Every number in this report comes from a window that included a gold rally and an energy rally and no real bear market. The return numbers would look different over a longer period."))
story.append(P("2. A smooth ride is worth something, but it is not the same as a higher return. MORE had the lowest volatility of any resource fund in the group, at 19.01%, and the shallowest fall, at 10.76%. The blend still returned more. Smoothness and return are different things, and a holder should not confuse them."))
story.append(P("3. The do-it-yourself test is the right test for an active fund. MORE's own reference is the energy index plus the materials index, so a 50/50 blend of XEG and XMA is the fair comparison. Over two years, the blend won on return and tied on risk-adjusted return, at a lower fee. That sets the bar the manager has to clear."))
story.append(P("4. A fund's name is not its exposure. MORE is a resources fund, but it behaves more like a materials and gold fund than an energy fund. Its correlation with XEG is 0.517, against 0.708 with XMA and 0.652 with XGD. The top holdings and the options overlay explain why."))
story.append(P("5. The year split matters more than the total. The two-year total hides the fact that 2025 was the gold year and 2026 was the energy year. MORE matched the blend in the first and lagged it in the second. A single total return can hide a fund that wins in one regime and loses in another."))
story.append(P("6. Fees matter more here than in the XEQT investigation. The gap is 0.23 points, not 0.08, which is $230 a year on $100,000 and $14,621 over 20 years in the illustration. An active fee has to earn its keep, and over two years it has not."))
story.append(P("7. Management fee and MER are not the same number. Management fee is what the manager charges. MER is the total reported expense after taxes and other fund costs. MORE's management fee is 0.75% and its MER is 0.84%. Mixing those two up makes a fund look cheaper than it really is."))
story.append(P("8. A forecast is only honest as a range. MORE's annualised return is 31.37%, but its standard error is about 12.9 points. The Monte Carlo median is $51.02 on the historical drift and $40.14 on a 7% drift. The drift assumption decides the answer, and the drift is the least certain number in the report."))
story.append(P("9. Scenarios beat point forecasts for a resource fund. The regression explains 63.4% of MORE's weekly moves with oil, gold, and the market, and the scenarios built on it show the useful facts: gold moves MORE more than oil does, and MORE is not a hedge against an oil crash. A scenario says what happens if, which is the question a holder can actually use."))
story.append(P("Limits and method", h1))
story.append(P("Price data are Yahoo Finance adjusted closes, weekly, Friday, from 20 September 2024 to 13 November 2026. Official net asset value returns differ slightly. Holdings weights are a snapshot, not a permanent mix. The Sharpe ratio uses a stated 2.0% risk free rate, not a market T-bill series. Cost illustrations assume a constant 7% gross return, which is a teaching assumption, not a forecast. The Monte Carlo uses 10,000 paths, weekly steps, a normal distribution, and a fixed seed, and it understates the chance of very bad weeks because real returns have fatter tails. The factor regression uses 113 weeks, and the scenarios apply weekly betas to one-year moves, which is a linear approximation. Past performance does not predict future performance."))
story.append(P("Sources", h1))
story.append(P("Mackenzie Core Resources ETF product page, updated 12 November 2026, and Annual Management Report of Fund Performance for the period ended 31 March 2025. Quarterly Portfolio Disclosure as at 31 December 2025. Yahoo Finance adjusted closes for MORE.TO, XEG.TO, XMA.TO, ZEO.TO, XGD.TO, and XIC.TO, and for WTI crude futures (CL=F) and gold futures (GC=F). Peer fees are from provider and third-party comparisons checked in November 2026, and are labelled as management fee or MER where the source makes that distinction. Scripts, data, and the Excel model are in the project folder, so every number in the performance tables can be recomputed from the weekly price file."))
doc = SimpleDocTemplate(str(base / "MORE_Investigation_Report.pdf"), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm, title="Investigating MORE", author="Munzeleen Sarwar")
doc.build(story)
print("report done")
