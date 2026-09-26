# tests/silver/test_ci_wide_semantics.py
#
# Cross-cutting remediation (task-9b): positively confirm that psi_ci_wide and
# omega_ci_wide now actually vary and correctly identify known-sparse rows,
# after the fix that computes them from the RAW (pre-fillna) component
# columns instead of the always-non-null final score.
import pandas as pd
from scripts.utils.paths import DATA_SILVER


def test_psi_ci_wide_varies_and_matches_null_pattern():
    from scripts.silver.compute_psi import PSI_WEIGHTS

    df = pd.read_parquet(DATA_SILVER / "psi_silver.parquet")
    null_weight_fraction = sum(
        df[col].isna().astype(float) * weight for col, weight in PSI_WEIGHTS.items()
    )
    expected = null_weight_fraction > 0.5

    assert (df["psi_ci_wide"] == expected).all()
    # No longer trivially all-False as it was before the fix.
    assert df["psi_ci_wide"].any(), "psi_ci_wide should flag at least some sparse rows"


def test_omega_ci_wide_varies_and_matches_null_pattern():
    from scripts.silver.compute_omega import OMEGA_WEIGHTS

    df = pd.read_parquet(DATA_SILVER / "omega_silver.parquet")
    null_weight_fraction = sum(
        df[col].isna().astype(float) * weight for col, weight in OMEGA_WEIGHTS.items()
    )
    expected = null_weight_fraction > 0.5

    assert (df["omega_ci_wide"] == expected).all()
    assert df["omega_ci_wide"].any(), "omega_ci_wide should flag at least some sparse rows"


def test_omega_ci_wide_flags_usa_warmup_period():
    # USA's 1870-1879 warm-up period has genuinely NaN derivative columns
    # (d_hegemon, d_network, d_tot all NaN -- see test_omega.py), which
    # together carry weight 0.25+0.20+0.15 = 0.60 > 0.5, so omega_ci_wide
    # must be True for these rows now that it is derived from the raw
    # component null pattern instead of the always-non-null final omega score.
    df = pd.read_parquet(DATA_SILVER / "omega_silver.parquet")
    usa = df.loc["USA"].sort_index()
    warmup = usa.iloc[:10]
    assert warmup["omega_ci_wide"].all(), (
        "USA's first 10 rows (1870-1879 warm-up, no 10yr-old observation to "
        "diff against yet) should be flagged omega_ci_wide=True"
    )
