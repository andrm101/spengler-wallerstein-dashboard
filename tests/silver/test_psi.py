import pandas as pd
import pytest
from scripts.utils.paths import DATA_SILVER

def _load():
    return pd.read_parquet(DATA_SILVER / "psi_silver.parquet")

def test_psi_schema():
    df = _load()
    assert len(df) > 0
    assert "psi" in df.columns
    assert df.index.names == ["country_cow", "year"]

def test_psi_bounds():
    df = _load()
    assert df["psi"].between(0, 1).all(skipna=True)

def test_hegemon_uk_1870_low_pressure():
    df = _load()
    # UK was the hegemon in 1870 — should have LOW structural pressure
    psi = df.loc[("UKG", 1870), "psi"]
    psi_periphery_estimate = df.xs(1870, level="year")["psi"].quantile(0.75)
    assert psi < psi_periphery_estimate
