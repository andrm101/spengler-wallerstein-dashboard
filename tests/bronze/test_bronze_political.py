import pandas as pd
from scripts.utils.paths import DATA_SILVER

def test_vdem_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "vdem_silver.parquet", engine='pyarrow')
    assert set(["country_cow", "year", "lib_dem", "polyarchy"]).issubset(df.columns)
    assert df["lib_dem"].dropna().between(0, 1).all()

def test_polity_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "polity_silver.parquet", engine='pyarrow')
    assert set(["country_cow", "year", "polity2"]).issubset(df.columns)
    assert df["polity2"].dropna().between(-10, 10).all()

def test_polity_usa_1900_democratic():
    df = pd.read_parquet(DATA_SILVER / "polity_silver.parquet", engine='pyarrow')
    val = df.loc[(df.country_cow == "USA") & (df.year == 1900), "polity2"].values
    assert len(val) == 1
    assert val[0] >= 8
