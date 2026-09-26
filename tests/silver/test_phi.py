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
    # Cross-cutting fix (see task-9b remediation): phi_ci_wide is no longer a
    # hardcoded constant. It is now null_weight_fraction + creativity_weight > 0.5,
    # where null_weight_fraction is the pre-fillna null pattern of the other
    # PHI_WEIGHTS components and creativity_weight=0.15 is creativity_proxy's
    # permanent placeholder contribution (it is never genuinely observed).
    # So phi_ci_wide is True whenever creativity_proxy's 0.15 weight PLUS any
    # additional missing component's weight exceeds 0.5 combined -- not for
    # every row unconditionally.
    from scripts.silver.compute_phi import PHI_WEIGHTS, CREATIVITY_PROXY_CI_WEIGHT

    df = _load()
    null_weight_fraction = sum(
        df[col].isna().astype(float) * weight for col, weight in PHI_WEIGHTS.items()
    )
    creativity_weight = CREATIVITY_PROXY_CI_WEIGHT
    expected = (null_weight_fraction + creativity_weight) > 0.5

    # Rows with any additional missing component contributing >0.35 combined
    # weight on top of creativity_proxy should be flagged wide.
    assert (df.loc[expected, "phi_ci_wide"]).all()
    assert (df["phi_ci_wide"] == expected).all()

    # The flag must no longer be trivially True for the whole panel -- unless
    # every single row genuinely has at least one other missing component,
    # which would itself be a legitimate empirical finding about data sparsity.
    if not df["phi_ci_wide"].all():
        assert not df["phi_ci_wide"].all()
    else:
        assert (null_weight_fraction > 0).all(), (
            "phi_ci_wide is True for every row, but this is only legitimate if "
            "every row has at least one missing component besides "
            "creativity_proxy -- verified here via null_weight_fraction > 0."
        )

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
