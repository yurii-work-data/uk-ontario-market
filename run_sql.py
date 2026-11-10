import csv
import pathlib
import re
import sqlite3

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

TABLES = ["uk_online_monthly", "on_market_monthly", "on_product_monthly", "fx_monthly"]

POSTGRES_TO_SQLITE = [
    (r"CREATE OR REPLACE VIEW (\w+)", r"DROP VIEW IF EXISTS \1; CREATE VIEW \1"),
    (r"CAST\(([^)]+) AS int\)", r"CAST(\1 AS INTEGER)"),
    (r"::numeric", ""),
]


def to_sqlite(sql):
    for pattern, replacement in POSTGRES_TO_SQLITE:
        sql = re.sub(pattern, replacement, sql)
    return sql


def load_csv(con, table):
    with open(DATA / f"{table}.csv", newline="") as f:
        reader = csv.reader(f)
        columns = next(reader)
        rows = []
        for row in reader:
            rows.append([None if v == "" else (float(v) if re.fullmatch(r"-?\d+(\.\d+)?", v) else v) for v in row])
    con.execute(f"CREATE TABLE {table} ({', '.join(columns)})")
    con.executemany(f"INSERT INTO {table} VALUES ({', '.join('?' * len(columns))})", rows)


def main():
    con = sqlite3.connect(":memory:")
    for table in TABLES:
        load_csv(con, table)
    for sql_file in sorted((HERE / "sql").glob("*.sql")):
        statements = [s.strip() for s in to_sqlite(sql_file.read_text()).split(";") if s.strip()]
        n = 0
        for statement in statements:
            cur = con.execute(statement)
            if not cur.description:
                continue
            n += 1
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description]
            out = OUT / f"{sql_file.stem}_{n}.csv"
            with open(out, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
            print(f"{out.name}: {len(rows)} rows")
    con.close()


if __name__ == "__main__":
    main()
