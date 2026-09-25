# JST Macrohistory Database R6 (Jordà, Schularick & Taylor)
# Replaces GFDD (financialization) and Penn WT (capital/investment) for 1870–1949.
import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import JST_ISO_TO_COW, MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960


def run() -> None:
    src = DATA_BRONZE / "JSTdatasetR6.xlsx"
    df = pd.read_excel(src)

    # JST R6 columns: year, country, iso, tloans, iy, ...
    # tloans = total loans to private non-financial sector (nominal local currency)
    # gdp = GDP (nominal local currency)
    # iy = investment / GDP (already a ratio)
    df["country_cow"] = df["iso"].map(JST_ISO_TO_COW)
    df = df.dropna(subset=["country_cow"])
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]

    # Compute tloans_gdp as a dimensionless ratio
    df["tloans_gdp"] = df["tloans"] / df["gdp"]
    df = df.rename(columns={"iy": "iy_gdp"})
    # Select only required columns
    df = df[["country_cow", "year", "tloans_gdp", "iy_gdp"]]
    df["year"] = df["year"].astype(int)

    out = DATA_SILVER / "jst_silver.parquet"
    df.to_parquet(out, index=False)
    print(f"Saved {len(df)} rows to {out}")


if __name__ == "__main__":
    run()
