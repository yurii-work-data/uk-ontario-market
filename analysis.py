import math
import pathlib

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = pathlib.Path(__file__).parent
OUT = HERE / "output"
CHARTS = HERE / "charts"
CHARTS.mkdir(exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
UK = "#1f4e79"
ON = "#c0504d"
GREY = "#8a8176"


def read(name):
    return pd.read_csv(OUT / f"{name}.csv")


def months(series):
    return pd.to_datetime(series + "-01")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(CHARTS / name)
    plt.close(fig)


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


def fmt_p(p):
    return "p < 0.001" if p < 0.001 else f"p = {p:.3f}"


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    t = (b.mean() - a.mean()) / se
    return {"mean_a": a.mean(), "mean_b": b.mean(), "diff": b.mean() - a.mean(), "t": t, "p": 2 * norm_sf(abs(t))}


notes = ["# Statistical notes\n"]


size = read("01_market_size_1")
size["date"] = months(size.month)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
ax1.plot(size.date, size.uk_ggy_cad_m_whole_market_est, color=UK, label="UK online, whole market estimate")
ax1.plot(size.date, size.uk_ggy_cad_m, color=UK, linestyle="--", linewidth=1, label="UK online, reported (about 70% of market)")
ax1.plot(size.date, size.on_naggr_cad_m, color=ON, label="Ontario, iGO operators")
ax1.set_ylabel("Monthly gross gaming revenue, CAD million")
ax1.set_title("Two regulated online markets, same currency", fontsize=10)
ax1.legend(frameon=False, fontsize=8)
ax1.set_ylim(0, None)
ax2.plot(size.date, size.uk_ggy_cad_per_adult, color=UK, label="UK (whole market estimate)")
ax2.plot(size.date, size.on_naggr_cad_per_adult, color=ON, label="Ontario")
ax2.set_ylabel("Gross gaming revenue per adult, CAD per month")
ax2.set_title("Per adult, Ontario caught up with the UK in 2025", fontsize=10)
ax2.legend(frameon=False, fontsize=8)
ax2.set_ylim(0, None)
for ax in (ax1, ax2):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
save(fig, "01_market_size.png")

last12 = size.tail(12)
first12 = size[(size.month >= "2023-04") & (size.month <= "2024-03")]
below = size[size.on_naggr_cad_per_adult <= size.uk_ggy_cad_per_adult].month.max()
cross = size[size.month > below].month.min()
notes += [
    "## Market size",
    f"- Last 12 months to {size.month.max()}: UK online whole market estimate CAD {last12.uk_ggy_cad_m_whole_market_est.sum():,.0f}M, "
    f"Ontario CAD {last12.on_naggr_cad_m.sum():,.0f}M ({100 * last12.on_naggr_cad_m.sum() / last12.uk_ggy_cad_m_whole_market_est.sum():.0f}% of the UK figure).",
    f"- Per adult in the last 12 months: UK CAD {last12.uk_ggy_cad_per_adult.mean():.2f} per month, Ontario CAD {last12.on_naggr_cad_per_adult.mean():.2f}. "
    f"Ontario has been above the UK per adult every month since {cross}.",
    f"- A year earlier (Apr 2023 to Mar 2024) Ontario was at CAD {first12.on_naggr_cad_per_adult.mean():.2f} per adult against UK CAD {first12.uk_ggy_cad_per_adult.mean():.2f}.",
    "",
]


mix_uk = read("02_product_mix_1")
mix_on = read("02_product_mix_2")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
uk_years = mix_uk[(mix_uk.year >= 2021) & (mix_uk.year <= 2025)]
bottom = np.zeros(len(uk_years))
for col, label, color in [("slots_pct", "Slots", "#1f4e79"), ("casino_pct", "Other casino", "#5b8db8"), ("betting_pct", "Betting", "#a3835c"), ("poker_pct", "Poker", "#c9c2b6")]:
    ax1.bar(uk_years.year.astype(str), uk_years[col], bottom=bottom, label=label, color=color)
    for i, v in enumerate(uk_years[col]):
        if v > 5:
            ax1.text(i, bottom[i] + v / 2, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=8)
    bottom += uk_years[col].to_numpy()
ax1.set_title("UK online GGY by product", fontsize=10)
ax1.legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1.0, -0.08), ncol=4)
on_years = mix_on[mix_on.year <= 2026]
bottom = np.zeros(len(on_years))
for col, label, color in [("casino_pct", "Casino (incl. slots)", "#1f4e79"), ("betting_pct", "Betting", "#a3835c"), ("poker_pct", "Poker", "#c9c2b6")]:
    ax2.bar(on_years.year.astype(str), on_years[col], bottom=bottom, label=label, color=color)
    for i, v in enumerate(on_years[col]):
        if v > 5:
            ax2.text(i, bottom[i] + v / 2, f"{v:.0f}%", ha="center", va="center", color="white", fontsize=8)
    bottom += on_years[col].to_numpy()
ax2.set_title("Ontario NAGGR by product (2022 from April, 2026 to September)", fontsize=10)
ax2.legend(frameon=False, fontsize=8, loc="upper right", bbox_to_anchor=(1.0, -0.08), ncol=3)
save(fig, "02_product_mix.png")

notes += [
    "## Product mix",
    f"- UK: slots went from {mix_uk[mix_uk.year == 2021].slots_pct.iloc[0]:.0f}% of online GGY in 2021 to {mix_uk[mix_uk.year == 2025].slots_pct.iloc[0]:.0f}% in 2025; betting fell from "
    f"{mix_uk[mix_uk.year == 2021].betting_pct.iloc[0]:.0f}% to {mix_uk[mix_uk.year == 2025].betting_pct.iloc[0]:.0f}%.",
    f"- Ontario: casino went from {mix_on[mix_on.year == 2022].casino_pct.iloc[0]:.0f}% of NAGGR in 2022 to {mix_on[mix_on.year == 2026].casino_pct.iloc[0]:.0f}% in 2026; "
    f"betting hold rose from {mix_on[mix_on.year == 2022].betting_hold_pct.iloc[0]:.1f}% to {mix_on[mix_on.year == 2026].betting_hold_pct.iloc[0]:.1f}% of wagers.",
    "",
]


mon = read("03_monetization_3")
mon["date"] = months(mon.month)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(mon.date, mon.on_arppa_cad, color=ON, label="Ontario: NAGGR per active account (ARPPA)")
ax.plot(mon.date, mon.uk_gaming_ggy_per_active_cad, color=UK, label="UK: slots and casino GGY per active (per vertical)")
ax.plot(mon.date, mon.uk_slots_ggy_per_active_cad, color=UK, linestyle="--", linewidth=1, label="UK: slots GGY per slots active")
ax.set_ylabel("CAD per active per month")
ax.set_ylim(0, None)
ax.set_title("An Ontario account yields nearly four times a UK gaming active", fontsize=10)
ax.legend(frameon=False, fontsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
save(fig, "03_monetization.png")

m12 = mon.tail(12)
notes += [
    "## Monetization",
    f"- Last 12 months: Ontario ARPPA CAD {m12.on_arppa_cad.mean():.0f} per account per month; UK slots and casino GGY per active CAD {m12.uk_gaming_ggy_per_active_cad.mean():.0f}; "
    f"ratio {m12.on_arppa_cad.mean() / m12.uk_gaming_ggy_per_active_cad.mean():.1f}x. UK actives are counted per vertical and one person can appear in several, "
    "so the UK figure is a lower bound per person and the gap is partly definitional.",
    "",
]


slots = read("04_slots_and_regulation_1")
slots["date"] = months(slots.month)
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, col, title in [
    (axes[0], "sessions_over_1h_pct", "Slot sessions over one hour, % of sessions"),
    (axes[1], "ggy_per_100_spins_gbp", "GGY per 100 spins, GBP"),
    (axes[2], "slots_ggy_gbp_m", "Slots GGY, GBP million per month"),
]:
    ax.plot(slots.date, slots[col], color=UK)
    ax.axvline(pd.Timestamp("2025-04-09"), color=ON, linewidth=1, linestyle="--")
    ax.axvline(pd.Timestamp("2025-05-21"), color=ON, linewidth=1, linestyle=":")
    ax.set_title(title, fontsize=9)
    ax.set_ylim(0, None)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
axes[0].text(pd.Timestamp("2025-04-09"), axes[0].get_ylim()[1] * 0.95, " stake limits\n 5 GBP, then 2 GBP for 18-24", color=ON, fontsize=7, va="top")
fig.suptitle("UK online slots before and after the 2025 stake limits", fontsize=10)
save(fig, "04_slots_regulation.png")

before = slots[(slots.month >= "2024-06") & (slots.month <= "2025-03")]
after = slots[(slots.month >= "2025-06") & (slots.month <= "2026-03")]
t_sessions = welch(before.sessions_over_1h_pct, after.sessions_over_1h_pct)
t_spin = welch(before.ggy_per_100_spins_gbp, after.ggy_per_100_spins_gbp)
yoy_before = slots[(slots.month >= "2024-06") & (slots.month <= "2025-03")].slots_ggy_gbp_m.to_numpy()
yoy_prev = slots[(slots.month >= "2023-06") & (slots.month <= "2024-03")].slots_ggy_gbp_m.to_numpy()
yoy_after = slots[(slots.month >= "2025-06") & (slots.month <= "2026-03")].slots_ggy_gbp_m.to_numpy()
growth_before = (yoy_before / yoy_prev - 1) * 100
growth_after = (yoy_after / yoy_before - 1) * 100
t_growth = welch(growth_before, growth_after)
long_sessions_avoided = (before.sessions_over_1h_pct.mean() - after.sessions_over_1h_pct.mean()) / 100 * after.sessions_m.sum() * 1e6
notes += [
    "## UK slots and the 2025 stake limits (10 months before, Jun 2024 to Mar 2025, against 10 months after, Jun 2025 to Mar 2026)",
    f"- Sessions over one hour: {t_sessions['mean_a']:.2f}% to {t_sessions['mean_b']:.2f}% of sessions ({t_sessions['diff']:+.2f} pp, {fmt_p(t_sessions['p'])}). "
    f"At the after period's volume that is about {long_sessions_avoided / 1e6:.1f} million fewer long sessions over ten months.",
    f"- GGY per 100 spins: GBP {t_spin['mean_a']:.3f} to {t_spin['mean_b']:.3f} ({100 * t_spin['diff'] / t_spin['mean_a']:+.1f}%, {fmt_p(t_spin['p'])}).",
    f"- Year on year growth of slots GGY: {growth_before.mean():+.1f}% in the ten months before the limits, {growth_after.mean():+.1f}% in the ten months after ({fmt_p(t_growth['p'])}). "
    f"Slots GGY kept growing; the limits changed session length, not revenue.",
    "",
]


season_uk = read("05_seasonality_1")
season_on = read("05_seasonality_2")
fig, ax = plt.subplots(figsize=(8, 3.6))
x = np.arange(1, 13)
ax.plot(x, season_uk.uk_betting_season_index, marker="o", color=UK, label="UK betting GGY")
ax.plot(x, season_on.on_betting_season_index, marker="o", color=ON, label="Ontario betting NAGGR")
ax.plot(x, season_uk.uk_slots_season_index, marker="s", color=UK, linestyle="--", linewidth=1, label="UK slots GGY")
ax.plot(x, season_on.on_casino_season_index, marker="s", color=ON, linestyle="--", linewidth=1, label="Ontario casino NAGGR")
ax.axhline(100, color=GREY, linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_ylabel("Index, centred 12-month average = 100")
ax.set_title("Betting is seasonal, casino is not", fontsize=10)
ax.legend(frameon=False, fontsize=8, ncol=2)
save(fig, "05_seasonality.png")

notes += [
    "## Seasonality (index against the centred 12-month average, 100 = average)",
    f"- UK betting: peak in March ({season_uk.uk_betting_season_index.max():.0f}), trough in September ({season_uk.uk_betting_season_index.min():.0f}); slots stay within "
    f"{season_uk.uk_slots_season_index.min():.0f} to {season_uk.uk_slots_season_index.max():.0f}.",
    f"- Ontario betting: peak {season_on.on_betting_season_index.max():.0f} in month {int(season_on.loc[season_on.on_betting_season_index.idxmax(), 'month_of_year'])}, "
    f"trough {season_on.on_betting_season_index.min():.0f} in month {int(season_on.loc[season_on.on_betting_season_index.idxmin(), 'month_of_year'])}; casino "
    f"{season_on.on_casino_season_index.min():.0f} to {season_on.on_casino_season_index.max():.0f}.",
    "",
]


on = read("03_monetization_2")
market = pd.read_csv(HERE / "data" / "on_market_monthly.csv")
hist = market[market.month >= "2024-04"].reset_index(drop=True)
y = np.log(hist.naggr_cad_m.to_numpy())
t = np.arange(len(hist))
moy = pd.to_datetime(hist.month + "-01").dt.month.to_numpy()
X = np.column_stack([np.ones(len(t)), t] + [(moy == m).astype(float) for m in range(2, 13)])
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
resid = y - X @ beta
sigma = resid.std(ddof=X.shape[1])
future_months = pd.period_range(pd.Period(hist.month.iloc[-1], "M") + 1, periods=12, freq="M")
tf = np.arange(len(t), len(t) + 12)
moyf = np.array([p.month for p in future_months])
Xf = np.column_stack([np.ones(12), tf] + [(moyf == m).astype(float) for m in range(2, 13)])
pred = Xf @ beta
forecast = pd.DataFrame({
    "month": [str(p) for p in future_months],
    "naggr_cad_m": np.exp(pred),
    "low_80": np.exp(pred - 1.28 * sigma),
    "high_80": np.exp(pred + 1.28 * sigma),
})
forecast.round(1).to_csv(OUT / "forecast_ontario_naggr.csv", index=False)
monthly_growth = math.exp(beta[1]) - 1

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(months(market.month), market.naggr_cad_m, color=ON, label="Ontario NAGGR, actual")
ax.plot(months(forecast.month), forecast.naggr_cad_m, color=ON, linestyle="--", label="Forecast, log-linear trend with monthly seasonality")
ax.fill_between(months(forecast.month), forecast.low_80, forecast.high_80, color=ON, alpha=0.15, label="80% interval")
ax.set_ylabel("CAD million per month")
ax.set_ylim(0, None)
ax.set_title(f"Ontario: next 12 months about CAD {forecast.naggr_cad_m.sum() / 1000:.1f} billion", fontsize=10)
ax.legend(frameon=False, fontsize=8)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
save(fig, "06_ontario_forecast.png")

last12_actual = market.tail(12).naggr_cad_m.sum()
notes += [
    "## Ontario forecast (fit on Apr 2024 to Sep 2026, log-linear trend plus month effects)",
    f"- Underlying growth {monthly_growth * 100:.2f}% per month, about {((1 + monthly_growth) ** 12 - 1) * 100:.0f}% a year; residual standard deviation {sigma * 100:.1f}% of the level.",
    f"- Next 12 months (Oct 2026 to Sep 2027): CAD {forecast.naggr_cad_m.sum():,.0f}M, 80% interval CAD {forecast.low_80.sum():,.0f}M to {forecast.high_80.sum():,.0f}M, "
    f"against CAD {last12_actual:,.0f}M in the last 12 actual months.",
    f"- At Ontario's 20% tax on iGaming revenue that is roughly CAD {forecast.naggr_cad_m.sum() * 0.2:,.0f}M of provincial revenue over the year, if the trend holds.",
    "",
]

lock = read("06_lockdown_1")
lock_act = read("06_lockdown_2")
lock["date"] = months(lock.month)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
ax1.plot(lock.date, lock.real_event_gbp_m, color=UK, marker="o", label="Real-event betting")
ax1.plot(lock.date, lock.slots_gbp_m, color=UK, marker="s", linestyle="--", linewidth=1, label="Slots")
ax1.plot(lock.date, lock.casino_gbp_m, color=ON, marker="s", linestyle="--", linewidth=1, label="Casino")
ax1.plot(lock.date, lock.poker_gbp_m, color=GREY, marker="^", linewidth=1, label="Poker")
ax1.axvspan(pd.Timestamp("2020-03-20"), pd.Timestamp("2020-06-15"), color=GREY, alpha=0.12)
ax1.set_ylabel("GGY, GBP million per month")
ax1.set_title("UK online GGY by product, 2020. Shaded: no live sport", fontsize=10)
ax1.legend(frameon=False, fontsize=8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
spring = lock[lock.month <= "2020-07"]
ax2.bar(spring.date, -spring.real_event_shortfall_gbp_m, width=20, color=UK, label="Real-event betting, change against March")
ax2.bar(spring.date, spring.other_products_gain_gbp_m, width=20, color=ON, alpha=0.8, label="All other products, change against March")
ax2.axhline(0, color=GREY, linewidth=0.8)
ax2.set_ylabel("GBP million against March 2020")
ax2.set_title("Casino and poker absorbed a sixth of the lost betting money", fontsize=10)
ax2.set_xlim(pd.Timestamp("2020-02-15"), pd.Timestamp("2020-08-15"))
ax2.legend(frameon=False, fontsize=8)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
save(fig, "07_lockdown.png")

march, april, june = (lock.set_index("month").loc[m] for m in ["2020-03", "2020-04", "2020-06"])
act_m, act_a, act_j = (lock_act.set_index("month").loc[m] for m in ["2020-03", "2020-04", "2020-06"])
notes += [
    "## UK lockdown, spring 2020 (GGY by product, March 2020 as the base)",
    f"- April 2020 against March: real-event betting {april.real_event_vs_march_pct:.0f}% (GBP {march.real_event_gbp_m:.0f}M to {april.real_event_gbp_m:.0f}M), "
    f"betting actives {act_m.betting_actives_m:.2f}M to {act_a.betting_actives_m:.2f}M; whole online market {april.total_vs_march_pct:.0f}%.",
    f"- Other products gained GBP {april.other_products_gain_gbp_m:.0f}M in April against a betting shortfall of GBP {april.real_event_shortfall_gbp_m:.0f}M: "
    f"casino +{100 * (april.casino_gbp_m / march.casino_gbp_m - 1):.0f}%, poker +{100 * (april.poker_gbp_m / march.poker_gbp_m - 1):.0f}%, slots {100 * (april.slots_gbp_m / march.slots_gbp_m - 1):.0f}%. "
    f"Substitution covered {100 * april.other_products_gain_gbp_m / april.real_event_shortfall_gbp_m:.0f}% of the loss.",
    f"- June 2020, first full month with football back: real-event betting +{june.real_event_vs_march_pct:.0f}% against March, actives {act_j.betting_actives_m:.2f}M, "
    f"whole market +{june.total_vs_march_pct:.0f}%. Poker and casino went back to where they were within two months.",
    "",
]


hold_summary = read("07_hold_volatility_1").set_index("product")
hold = read("07_hold_volatility_2")
hold_year = read("07_hold_volatility_3")
hold["date"] = months(hold.month)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
ax1.plot(hold.date, hold.hold_pct, color=ON, marker="o", markersize=3, label="Betting hold, actual month")
ax1.plot(hold.date, hold.trailing_hold_pct, color=ON, linestyle="--", linewidth=1, label="Trailing 12-month hold")
ax1.axhline(hold_summary.loc["casino", "avg_hold_pct"], color=UK, linewidth=1, label=f"Casino hold, average {hold_summary.loc['casino', 'avg_hold_pct']:.1f}%")
ax1.set_ylabel("NAGGR as % of cash wagers")
ax1.set_ylim(0, None)
ax1.set_title("Ontario betting hold swings between 3.5% and 9%; casino does not", fontsize=10)
ax1.legend(frameon=False, fontsize=8)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
colors = np.where(hold.result_effect_cad_m >= 0, ON, UK)
ax2.bar(hold.date, hold.result_effect_cad_m, width=20, color=colors)
ax2.axhline(0, color=GREY, linewidth=0.8)
ax2.set_ylabel("CAD million against expected at trailing hold")
ax2.set_title("What sports results alone added or removed each month", fontsize=10)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
save(fig, "08_hold_volatility.png")

bet = hold_summary.loc["betting"]
cas = hold_summary.loc["casino"]
effect = hold.result_effect_cad_m
last12_wagers = hold.tail(12).cash_wagers_cad_m.sum()
last12_naggr = hold.tail(12).naggr_cad_m.sum()
rolling12 = effect.rolling(12).sum().dropna()
hold_slope = np.polyfit(np.arange(len(hold_year)), hold_year.hold_pct, 1)[0]
notes += [
    "## Ontario betting hold volatility (hold = NAGGR / cash wagers)",
    f"- Betting hold averages {bet.avg_hold_pct:.2f}% with a standard deviation of {bet.hold_sd_pp:.2f} points, a coefficient of variation of {100 * bet.hold_sd_pp / bet.avg_hold_pct:.0f}%; "
    f"range {bet.min_hold_pct:.1f}% to {bet.max_hold_pct:.1f}%. Casino hold averages {cas.avg_hold_pct:.2f}% with a standard deviation of {cas.hold_sd_pp:.2f} points.",
    f"- Against the trailing 12-month hold, the monthly result effect averages CAD {effect.abs().mean():.0f}M in either direction, "
    f"from CAD {effect.min():.0f}M ({hold.loc[effect.idxmin(), 'month']}) to +CAD {effect.max():.0f}M ({hold.loc[effect.idxmax(), 'month']}). "
    f"On the last twelve months of wagers (CAD {last12_wagers:,.0f}M) one point of hold is worth CAD {last12_wagers / 100:.0f}M a year.",
    f"- Over any twelve-month window the result effect nets to between CAD {rolling12.min():.0f}M and +CAD {rolling12.max():.0f}M, "
    f"so an annual betting revenue plan built on the trailing hold carries roughly ±{100 * 1.28 * rolling12.std() / last12_naggr:.0f}% of results noise at 80% confidence.",
    f"- Annual hold has risen from {hold_year.hold_pct.iloc[0]:.2f}% in 2022 to {hold_year.hold_pct.iloc[-1]:.2f}% in 2026, about {hold_slope:.2f} points a year, consistent with a growing share of parlays and same-game bets.",
    "",
]

(OUT / "stats.md").write_text("\n".join(notes))
print("\n".join(notes))
