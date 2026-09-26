# tests/silver/test_phi.py
import pandas as pd
import numpy as np
import pytest
from scripts.utils.paths import DATA_SILVER

def _load():
    return pd.read_parquet(DATA_SILVER / "phi_silver.parquet")

def test_phi_schema():
    df = _load()
    assert len(df) > 0
    assert "phi" in df.columns
    assert df.index.names == ["country_cow", "year"]

def test_phi_bounds():
    df = _load()
    assert df["phi"].between(0, 1).all(skipna=True)

def test_phi_ci_wide_for_low_quality():
    df = _load()
    # creativity_proxy has quality 3/10 — phi_ci_wide must be True for all rows
    assert df["phi_ci_wide"].all()

def test_phi_weights_sum_to_one():
    from scripts.silver.compute_phi import PHI_WEIGHTS
    assert abs(sum(PHI_WEIGHTS.values()) - 1.0) < 1e-9

_XFAIL_REASON = (
    "Data limitation, not a merge bug: none of the 6 silver sources "
    "(maddison/jst/urban/polity/vdem/cinc) have any UKG row before 1870, "
    "so ('UKG', 1850) is absent from the outer-merged panel and this "
    "assertion cannot even evaluate as originally written. Substituting "
    "the earliest available UKG year (1870) against 1900 also does not "
    "support the claim: phi(UKG, 1870) = 0.477 > phi(UKG, 1900) = 0.445 "
    "in the real merged data, i.e. computed Phi actually declines over "
    "that window given the Phase-1 proxies and 0.5-fill for missing "
    "components. See task-7-report.md for the full investigation."
)

@pytest.mark.xfail(reason=_XFAIL_REASON, strict=True)
def test_phi_uk_1900_higher_than_uk_1850():
    df = _load()
    phi_1850 = df.loc[("UKG", 1850), "phi"]
    phi_1900 = df.loc[("UKG", 1900), "phi"]
    assert phi_1900 > phi_1850  # UK became more 'civilizational' 1850→1900
