import zipfile
import pandas as pd
from scripts.utils.paths import DATA_BRONZE, DATA_SILVER
from scripts.utils.country_codes import MVP_COUNTRIES

YEAR_MIN, YEAR_MAX = 1870, 1960
MISSING = -9


def run() -> None:
    zip_path = DATA_BRONZE / "NMCv7" / "NMC-v7-abridged.zip"
    with zipfile.ZipFile(zip_path) as z:
        with z.open("NMC-70-abridged.csv") as f:
            df = pd.read_csv(f)

    df = df.replace(MISSING, float("nan"))
    df["country_cow"] = df["stateabb"].astype(str)
    df = df[df["country_cow"].isin(MVP_COUNTRIES)]
    df = df[(df["year"] >= YEAR_MIN) & (df["year"] <= YEAR_MAX)]
    df["year"] = df["year"].astype(int)

    cinc_out = df[["country_cow", "year", "cinc"]].rename(columns={"cinc": "cinc_share"}).copy()
    cinc_out.to_parquet(DATA_SILVER / "cinc_silver.parquet", index=False)
    print(f"Saved {len(cinc_out)} rows -> cinc_silver.parquet")

    urban_out = df[["country_cow", "year", "upop", "tpop"]].copy()
    urban_out["urban_pop_pct"] = (urban_out["upop"] / urban_out["tpop"].replace(0, float("nan"))) * 100
    urban_out = urban_out[["country_cow", "year", "urban_pop_pct"]]
    urban_out.to_parquet(DATA_SILVER / "urban_silver.parquet", index=False)
    print(f"Saved {len(urban_out)} rows -> urban_silver.parquet")


if __name__ == "__main__":
    run()
