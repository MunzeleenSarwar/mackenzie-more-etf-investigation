# Investigating MORE

## Question
What does one ticker buy, what does it cost, what risk does it carry,
and when would building a portfolio by hand beat it?

## Answer in one paragraph
MORE is an actively managed Canadian resource fund that holds 83 stocks
across energy, materials, and precious metals, plus call options on gold.
Over 20 September 2024 to 13 November 2026, $10,000 in MORE became $18,981,
while a 50/50 blend of the XEG energy index fund and the XMA materials
index fund became $20,266, with almost the same Sharpe ratio. MORE fell
10.76% from peak to low in April 2025, the smallest fall of any resource
fund in the group. MORE charges 0.84% per year. Building the same mix
from two index funds costs 0.61% per year, a saving of about $230 per
year on $100,000, before trading costs, time, and tax records. Forecasting
gives a range, not a point: the Monte Carlo median is $51.02 in a year on
the historical drift and $40.14 on a conservative 7% drift, from $38.02.

## Files
- MORE_Investigation_Report.pdf: report, plain language, including a
  forecasting section and a Lessons Learned section.
- MORE_Investigation_Model.xlsx: performance, holdings, calendar, cost,
  sources, peers, forecast.
- MORE_Investigation_Notebook.ipynb: recomputation notebook.
- data/: weekly prices, weekly returns, factor returns, growth, drawdowns,
  metrics, forecast, Monte Carlo fan series.
- charts/: growth, drawdown, top holdings, Monte Carlo fan.
- scripts/: download and analysis, charts, forecast, fan chart, Excel,
  notebook, report.

## Method and limits
Weekly Friday prices in CAD from Yahoo Finance, adjusted for dividends.
Sharpe uses a stated 2.0% risk free rate, not a market T-bill series.
Holdings weights are a Mackenzie snapshot at 29 September 2026.
The February 2026 iShares factsheet is not used here; MORE facts are from
the Mackenzie product page and the Management Report of Fund Performance
for the period ended 31 March 2025. Cost illustrations assume a constant
7% gross return, which is a teaching assumption, not a forecast. The Monte
Carlo uses 10,000 paths, weekly steps, a normal distribution, and a fixed
seed. The factor regression uses 113 weeks, and the scenarios apply weekly
betas to one-year moves, which is a linear approximation. Past performance
does not predict future performance. This project is an investigation, not
personal investment advice.
