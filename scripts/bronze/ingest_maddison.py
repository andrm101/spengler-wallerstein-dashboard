import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import MADDISON_TO_COW, MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960


def run() -> None:
    src = DATA_BRONZE / "mpd2023_web.xlsx"
    df = pd.read_excel(src, sheet_name="Full data")

    # Maddison 2023 columns: countrycode, country, region, year, gdppc, pop
    df = df.rename(columns={"gdppc": "gdppc", "pop": "pop_thousands"})
    df["country_cow"] = df["countrycode"].map(MADDISON_TO_COW)
    df = df.dropna(subset=["country_cow"])
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df = df[["country_cow", "year", "gdppc", "pop_thousands"]].copy()
    df["year"] = df["year"].astype(int)

    out = DATA_SILVER / "maddison_silver.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {len(df)} rows to {out}")


if __name__ == "__main__":
    run()
