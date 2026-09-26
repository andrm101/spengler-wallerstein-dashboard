import pandas as pd
from scripts.utils.paths import DATA_SILVER


def test_cow_trade_schema():
    df = pd.read_parquet(DATA_SILVER / "cow_trade_silver.parquet")
    assert set(["country_cow", "year", "total_exports", "total_imports"]).issubset(df.columns)
    assert df["total_exports"].dropna().ge(0).all()
    # Guard against empty dataframe
    assert len(df) > 0


def test_cow_trade_year_range():
    df = pd.read_parquet(DATA_SILVER / "cow_trade_silver.parquet")
    assert df["year"].min() <= 1870
    assert df["year"].max() >= 1950


def test_cow_trade_mvp_countries():
    df = pd.read_parquet(DATA_SILVER / "cow_trade_silver.parquet")
    assert "USA" in df["country_cow"].values
    assert "UKG" in df["country_cow"].values
