import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960
MISSING = -9


def run() -> None:
    src = DATA_BRONZE / "COW_Trade_4.0" / "National_COW_4.0.csv"
    df = pd.read_csv(src)

    df = df.replace(MISSING, float("nan"))
    df["country_cow"] = df["stateabb"].astype(str)
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df = df.rename(columns={"exports": "total_exports", "imports": "total_imports"})
    df = df[["country_cow", "year", "total_exports", "total_imports"]].copy()
    df["year"] = df["year"].astype(int)

    out = DATA_SILVER / "cow_trade_silver.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {len(df)} rows -> {out}")


if __name__ == "__main__":
    run()
