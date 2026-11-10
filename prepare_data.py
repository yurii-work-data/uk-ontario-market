import csv
import pathlib
import sys
from datetime import datetime

import openpyxl

RAW = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "raw")
OUT = pathlib.Path("data")
OUT.mkdir(exist_ok=True)

UK_TABLES = {
    "Actives per vertical": "active_players",
    "Bets per vertical": "bets",
    "Session length": "slots_sessions",
    "GGY by vertical": "ggy_gbp",
}
UK_VERTICALS = {
    "Slots": "slots",
    "Other gaming (including casino)": "casino",
    "Casino": "casino",
    "Betting (Real event)": "betting_real_event",
    "Betting (Virtual)": "betting_virtual",
    "Betting (eSports)": "betting_esports",
    "Poker": "poker",
    "Other": "other",
    "Av. session length (minutes)": "avg_session_minutes",
    "Sessions >1hr": "sessions_over_1h",
    "Total number of sessions": "sessions_total",
}


def month_key(label):
    return datetime.strptime(label, "%b-%y").strftime("%Y-%m")


def write(name, header, rows):
    with open(OUT / name, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def parse_ukgc():
    wb = openpyxl.load_workbook(RAW / "ukgc_operator_data_2026-03.xlsx", read_only=True, data_only=True)
    rows = list(wb["Online"].iter_rows(values_only=True))
    out = []
    metric = None
    months = None
    for r in rows:
        head = (str(r[0]).strip() if r[0] is not None else "")
        if head in UK_TABLES:
            metric = UK_TABLES[head]
            months = [month_key(str(c)) for c in r[1:] if c is not None]
            continue
        if metric and head in UK_VERTICALS and r[1] is not None:
            series = UK_VERTICALS[head]
            for m, v in zip(months, r[1:]):
                if v is not None:
                    out.append([m, metric, series, round(float(v), 4)])
        elif metric and head == "":
            metric = None
    write("uk_online_monthly.csv", ["month", "metric", "series", "value"], out)


def parse_igo():
    wb = openpyxl.load_workbook(RAW / "igo_monthly_2026-09.xlsx", read_only=True, data_only=True)
    rows = list(wb["(Data) Monthly Stats"].iter_rows(values_only=True))
    market = []
    for r in rows[3:]:
        if r[1] is None:
            continue
        market.append([r[1], r[0], r[2], r[4], r[6], r[8]])
    write("on_market_monthly.csv",
          ["month", "fiscal_quarter", "cash_wagers_cad_m", "naggr_cad_m", "active_accounts_k", "arppa_cad"], market)

    rows = list(wb["(Data) Product Monthly Stats"].iter_rows(values_only=True))
    product = []
    for r in rows[3:]:
        if r[1] is None or r[2] is None:
            continue
        product.append([r[1], str(r[2]).lower().replace("p2p ", "").replace(" ", "_"), r[3], r[6]])
    write("on_product_monthly.csv", ["month", "product", "cash_wagers_cad_m", "naggr_cad_m"], product)


def parse_fx():
    out = []
    for name, series in [("boc_gbpcad.csv", "GBPCAD"), ("boc_usdcad.csv", "USDCAD")]:
        monthly = {}
        with open(RAW / name, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            in_obs = False
            for row in reader:
                if row and row[0] == "OBSERVATIONS":
                    in_obs = True
                    next(reader)
                    continue
                if in_obs and len(row) == 2 and row[1]:
                    monthly.setdefault(row[0][:7], []).append(float(row[1]))
        for m, vals in sorted(monthly.items()):
            out.append([m, series, round(sum(vals) / len(vals), 4), len(vals)])
    write("fx_monthly.csv", ["month", "pair", "rate", "trading_days"], out)


parse_ukgc()
parse_igo()
parse_fx()
