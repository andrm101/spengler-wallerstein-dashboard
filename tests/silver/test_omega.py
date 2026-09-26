import pandas as pd
import numpy as np
import pytest
from scripts.utils.paths import DATA_SILVER

def _load():
    return pd.read_parquet(DATA_SILVER / "omega_silver.parquet")

def test_omega_schema():
    df = _load()
    assert "omega" in df.columns
    assert df.index.names == ["country_cow", "year"]

def test_omega_bounds():
    df = _load()
    assert df["omega"].between(-1, 1).all(skipna=True)

def test_omega_window_creates_nan_first_10_years():
    df = _load()
    usa = df.loc["USA"].sort_index()
    # USA's real coverage in the underlying panel starts at 1870 (verified by
    # direct inspection of the generated omega_silver.parquet), is contiguous
    # (no gaps) through the observed range, and the derivative window is
    # WINDOW=10 (.diff(10)), so positional slicing correctly corresponds to
    # calendar years here.
    #
    # NOTE: the final "omega" column itself does NOT go NaN during this
    # warm-up period. compute_omega.py builds omega as
    #   sum(df_omega[col].fillna(0) * weight for col, weight in OMEGA_WEIGHTS)
    # so when every weighted component is NaN (no 10-year-old observation to
    # diff against yet), fillna(0) turns that into a weighted sum of zeros,
    # i.e. omega reads exactly 0.0 -- not NaN -- for the first 10 rows. This
    # conflates "no data yet" with "genuinely neutral momentum" and is a
    # separate finding documented in the task report; it is NOT something
    # this test suite treats as in-scope to change, since Step 2's
    # compute_omega.py is specified verbatim.
    #
    # The 10-year window's NaN-producing effect *is* directly observable at
    # the source: the per-factor derivative columns (d_hegemon, d_network,
    # d_tot) are NaN for the first 10 rows and populated from row 10 onward.
    for col in ("d_hegemon", "d_network", "d_tot"):
        assert usa[col].iloc[:10].isna().all(), f"{col} should be NaN for the first 10 rows"
        assert usa[col].iloc[10:].notna().any(), f"{col} should have real values after the window fills"
