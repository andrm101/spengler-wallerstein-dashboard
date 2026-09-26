import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import VDEM_TO_COW, MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960

VDEM_VARS = {
    "v2x_libdem":    "lib_dem",
    "v2x_polyarchy": "polyarchy",
    "v2x_clpol":     "civil_lib",
}

def run() -> None:
    src = DATA_BRONZE / "V-Dem-CY-Core-v16.csv"
    cols = ["country_name", "year"] + list(VDEM_VARS.keys())
    df = pd.read_csv(src, usecols=cols, low_memory=False)

    df["country_cow"] = df["country_name"].map(VDEM_TO_COW)
    df = df.dropna(subset=["country_cow"])
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df = df.rename(columns=VDEM_VARS)
    df = df[["country_cow", "year"] + list(VDEM_VARS.values())].copy()
    df["year"] = df["year"].astype(int)

    out = DATA_SILVER / "vdem_silver.parquet"
    df.to_parquet(out, index=False, engine='pyarrow')
    print(f"Saved {len(df)} rows -> {out}")

if __name__ == "__main__":
    run()
