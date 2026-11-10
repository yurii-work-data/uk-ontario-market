# Two regulated online gambling markets: the UK and Ontario, 2020 to 2026

A market-level analysis built entirely on public data: the monthly figures the two regulators publish, the UK Gambling Commission's operator data for online gambling (March 2020 to March 2026) and iGaming Ontario's market performance report (April 2022 to September 2026). Exchange rates come from the Bank of Canada. Everything runs with Python 3 plus pandas, numpy, matplotlib and openpyxl; the SQL is PostgreSQL dialect and runs on an in-memory SQLite copy so nothing needs to be installed.

The questions are the ones an operator, an investor or a regulator asks about these two markets: how big are they in the same currency and per adult, what people play, how much a player is worth, what the UK's 2025 slot stake limits changed, how seasonal the business is, what happened when live sport stopped in 2020, how much sports results alone move revenue, and where Ontario is heading over the next year. It ends with recommendations.

## How to run

```
python3 prepare_data.py raw
python3 run_sql.py
python3 analysis.py
```

`prepare_data.py` reads the two regulator workbooks and the Bank of Canada CSVs from `raw/` and writes tidy CSVs to `data/`. `run_sql.py` loads them into SQLite, runs the queries in `sql/` and writes each result to `output/`. `analysis.py` makes the eight charts in `charts/`, the statistical notes in `output/stats.md` and the forecast in `output/forecast_ontario_naggr.csv`.

## Data and definitions

The UK figures are gross gambling yield (stakes minus winnings) reported by the largest online operators, which the Commission says cover about 70% of the online market. Where the text says "whole market estimate" the reported figure is divided by 0.7. Active players are counted per product, so one person playing slots and betting on sport appears twice; the Commission warns these columns must not be summed, and this analysis does not. Slot session data covers online slots only.

The Ontario figures are non-adjusted gross gaming revenue (NAGGR) and cash wagers for all operators under agreement with iGaming Ontario, which excludes OLG's own site. Active player accounts are unique within a month. ARPPA is NAGGR per active account.

Pounds are converted to Canadian dollars at the Bank of Canada monthly average rate. Per-adult figures use 53.9 million adults for the UK and 12.6 million for Ontario. Both are round numbers from the 2021 and 2022 census bases and are only meant for order-of-magnitude comparison.

The two measures are close but not identical: GGY and NAGGR both take stakes minus winnings before operating costs, but bonus treatment differs between regimes, and the UK figure is an estimate of the whole market while the Ontario figure is a full count of the regulated market. Comparisons in this document should be read with that in mind.

## What the data shows

Market size (`sql/01`, chart `01_market_size.png`). In the twelve months to March 2026 the UK online market is worth about CAD 15.8 billion of gross gaming revenue on the whole-market estimate, and Ontario about CAD 4.3 billion, 27% of the UK. Per adult the picture is different: the UK ran at CAD 24 per adult per month over that year and Ontario at CAD 28. Ontario was at CAD 3.50 per adult in its first month in April 2022, drew level with the UK during 2025 and has been above it every month since September 2025. Ontario's year-on-year growth in 2025 was 34% against 9% for the UK in Canadian dollar terms.

Product mix (`sql/02`, chart `02_product_mix.png`). Both markets are moving towards casino. In the UK slots went from 40% of online GGY in 2021 to 51% in 2025 while real-event betting fell from 45% to 38%. In Ontario casino went from 65% of NAGGR in 2022 to 80% in 2026 and betting from 33% to 18%. Ontario's betting hold, revenue as a share of wagers, rose from 6.3% to 7.2% over the same period; casino hold sits around 3.5 to 3.8% of wagers because casino wagers recycle winnings many times.

Monetization (`sql/03`, chart `03_monetization.png`). An active Ontario account produced CAD 304 of NAGGR per month in the last twelve months, on roughly CAD 7,300 of cash wagers. The UK's slots and casino GGY per active, converted to dollars, was about CAD 80 over the same period. The ratio is 3.8 to 1. Part of this is definitional, since a UK active is counted per product and a casual bettor counts as an active, while an Ontario account that wagered anything counts once. Part of it is real: Ontario's market is dominated by casino, which earns more per player than sports betting, and its player base is still small relative to population.

UK slots and the 2025 stake limits (`sql/04`, chart `04_slots_regulation.png`). Online slot stakes were capped at GBP 5 per spin from 9 April 2025 and at GBP 2 for players aged 18 to 24 from 21 May 2025. Comparing the ten months before (June 2024 to March 2025) with the ten months after (June 2025 to March 2026), the share of slot sessions longer than an hour fell from 6.0% to 4.5%, a drop of 1.5 points that happened in a single month after a slow decline of about half a point a year; at current volumes that is about 10 million fewer long sessions over ten months. Revenue did not fall. Slots GGY grew 13.7% year on year before the limits and 10.7% after, a difference that is not statistically distinguishable at these sample sizes, and GGY per 100 spins rose 4.4%. On this evidence the limits changed how long people play, not how much operators earn.

Seasonality (`sql/05`, chart `05_seasonality.png`). Betting is seasonal and casino is not. UK betting GGY peaks in March (index 126 against the centred twelve-month average) with the Cheltenham Festival and the end of the football season, and bottoms in September (77) after the summer transfer window. Ontario betting peaks in January (133) and November (130) with the NFL playoffs and the autumn overlap of NFL, NBA and NHL, and bottoms in July and August (80). Slots and casino stay within about 8% of their average all year in both markets. For an operator this is the difference between a product whose budget needs a monthly profile and one that can be planned flat.

Lockdown 2020 (`sql/06`, chart `07_lockdown.png`). The UK series starts in March 2020, so it contains the months without live sport. In April 2020 real-event betting GGY fell 62% against March, from GBP 160 million to 62 million, and betting actives fell from 4.6 million to 2.1 million. Casino rose 23%, poker 67%, virtual and esports betting roughly doubled from a small base, slots were flat. All other products together gained GBP 16 million against a betting shortfall of GBP 98 million, so substitution covered about a sixth of the loss and the whole online market was down 20%. In June, the first full month with football back, betting was 36% above March, the market 11% above, and casino and poker were back at their pre-lockdown level within two months.

Betting hold volatility (`sql/07`, chart `08_hold_volatility.png`). Ontario's betting hold averages 6.55% with a standard deviation of 1.3 points (range 3.5% to 9.1%); casino hold averages 3.56% with a standard deviation of 0.2 points. Against the trailing twelve-month hold, the month's sports results add or remove CAD 11 million on average, from minus 36 million in December 2024 to plus 30 million in December 2025. One point of hold on the last twelve months of wagers is CAD 127 million a year. Over any twelve-month window the effect nets to between minus 61 and plus 63 million, about 5% of annual betting revenue at 80% confidence. Annual hold has risen from 6.3% in 2022 to 7.2% in 2026, about a quarter of a point a year.

Forecast (chart `06_ontario_forecast.png`, `output/forecast_ontario_naggr.csv`). A log-linear trend with month effects fitted on April 2024 to September 2026 gives underlying growth of 2.2% per month, about 30% a year, with a residual standard deviation of 5%. It projects CAD 6.2 billion of NAGGR for October 2026 to September 2027, with an 80% interval of 5.8 to 6.6 billion, against 4.8 billion in the last twelve actual months. At Ontario's 20% revenue share that is roughly CAD 1.2 billion of provincial revenue over the year if the trend holds. The main risk to the forecast is deceleration: year-on-year growth has already come down from 155% in 2023 to around 25% in mid 2026, and a simple log-linear trend does not bend.

## Recommendations

For an operator entering Ontario: a casino-led product with sports as the acquisition hook, marketing budgeted against the betting calendar (November and January about 30% above the average month, July and August 20% below), player value modelled on revenue per account rather than wagers, and betting revenue planned as a range with the hold assumption stated, because a single month can miss the trailing-hold expectation by a third and a year by about 5%.

For a UK operator facing further stake or deposit limits: model the change in spins per session and the shift between stake bands rather than a headline revenue hit, since the 2025 limits changed session length and left revenue intact. Model any loss of the sports product as a near-total loss of that line for its duration with an immediate recovery after, since in 2020 only a sixth of lost betting revenue moved to other products.

For the province: CAD 6.2 billion of NAGGR between October 2026 and September 2027 means roughly CAD 1.2 billion at the 20% share, with an 80% range of 1.16 to 1.32 billion; the low end is the planning case because growth is decelerating and a trend model does not bend.

## Layout

```
prepare_data.py   reads raw/ (regulator workbooks, Bank of Canada CSVs), writes data/
run_sql.py        runs sql/ on SQLite, writes output/*.csv
analysis.py       statistics, charts, forecast
sql/              PostgreSQL queries: views, market size, product mix, monetization, slots and regulation, seasonality, lockdown 2020, hold volatility
raw/              source files as downloaded
data/             tidy monthly CSVs
output/           query results, stats.md, forecast
charts/           eight PNG charts
```

## Sources and licences

All inputs are public data released for reuse. UK Gambling Commission, Gambling business data on gambling to March 2026 (operator data, published May 2026). iGaming Ontario, Market Performance Report, monthly data tables to September 2026. Bank of Canada, daily exchange rates FXGBPCAD and FXUSDCAD. Adult populations from the UK 2021 census and the Canadian 2021 census for Ontario, rounded. The Gambling Commission data is published under the Open Government Licence v3.0; the iGaming Ontario report and the Bank of Canada rates are published openly on their websites for public use with attribution. The files in `raw/` are unchanged copies of the public downloads, and nothing here contains personal or operator-confidential data.

Yurii Cherevko, 2026.
