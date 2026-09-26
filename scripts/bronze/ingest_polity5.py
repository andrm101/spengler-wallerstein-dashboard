import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import POLITY_CCODE_TO_COW, MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960
POLITY_MISSING = [-66, -77, -88]

def run() -> None:
    src = DATA_BRONZE / "p5v2018.xls"
    df = pd.read_excel(src)

    df["country_cow"] = df["ccode"].map(POLITY_CCODE_TO_COW)
    df = df.dropna(subset=["country_cow"])
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df["polity2"] = df["polity2"].replace(POLITY_MISSING, float("nan"))
    df["durable"] = df["durable"].replace(POLITY_MISSING, float("nan"))
    df = df[["country_cow", "year", "polity2", "durable"]].copy()
    df["year"] = df["year"].astype(int)

    out = DATA_SILVER / "polity_silver.parquet"
    df.to_parquet(out, index=False, engine='pyarrow')
    print(f"Saved {len(df)} rows -> {out}")

if __name__ == "__main__":
    run()
