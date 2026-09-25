import pandas as pd
import pytest
from scripts.utils.paths import DATA_SILVER


def test_maddison_silver_exists():
    assert (DATA_SILVER / "maddison_silver.parquet").exists()


def test_maddison_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    assert set(["country_cow", "year", "gdppc", "pop_thousands"]).issubset(df.columns)
    assert df["country_cow"].dtype in [object, "string", "str"] or str(df["country_cow"].dtype) in ["object", "string", "str"]
    assert df["year"].dtype in ["int32", "int64"] or str(df["year"].dtype) in ["int32", "int64"]


def test_maddison_mvp_countries_present():
    df = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    assert "USA" in df["country_cow"].values
    assert "UKG" in df["country_cow"].values


def test_maddison_year_range():
    df = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    assert df["year"].min() <= 1870
    assert df["year"].max() >= 1960


def test_maddison_usa_1900_gdppc_plausible():
    df = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    val = df.loc[(df.country_cow == "USA") & (df.year == 1900), "gdppc"].values
    assert len(val) == 1
    assert 3000 < val[0] < 9000  # Maddison USA 1900 ≈ 8,037 GK$


def test_jst_silver_schema():
    df = pd.read_parquet(DATA_SILVER / "jst_silver.parquet")
    assert set(["country_cow", "year", "tloans_gdp", "iy_gdp"]).issubset(df.columns)


def test_jst_silver_tloans_plausible():
    df = pd.read_parquet(DATA_SILVER / "jst_silver.parquet")
    non_null = df["tloans_gdp"].dropna()
    assert (non_null >= 0).all()
    # tloans_gdp is a dimensionless ratio: expected range 0.02–1.5
    assert (non_null < 5).all()
