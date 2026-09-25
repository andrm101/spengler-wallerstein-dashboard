import pandas as pd
from scripts.utils.paths import DATA_SILVER


def test_cinc_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "cinc_silver.parquet")
    assert set(["country_cow", "year", "cinc_share"]).issubset(df.columns)
    assert df["cinc_share"].dropna().between(0, 1).all()


def test_cinc_uk_1870_hegemonic():
    df = pd.read_parquet(DATA_SILVER / "cinc_silver.parquet")
    val = df.loc[(df.country_cow == "UKG") & (df.year == 1870), "cinc_share"].values
    assert len(val) == 1
    assert val[0] > 0.15


def test_urban_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "urban_silver.parquet")
    assert set(["country_cow", "year", "urban_pop_pct"]).issubset(df.columns)
    assert df["urban_pop_pct"].dropna().between(0, 100).all()


def test_urban_uk_1900_high():
    df = pd.read_parquet(DATA_SILVER / "urban_silver.parquet")
    val = df.loc[(df.country_cow == "UKG") & (df.year == 1900), "urban_pop_pct"].values
    assert len(val) == 1
    assert val[0] > 30  # NMC v7 data shows ~32.8% urbanization for UK in 1900
