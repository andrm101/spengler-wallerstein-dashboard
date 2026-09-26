import pandas as pd
from scripts.utils.paths import DATA_GOLD

def test_backtest_report_exists():
    assert (DATA_GOLD / "backtest_report.csv").exists()

def test_backtest_schema():
    df = pd.read_csv(DATA_GOLD / "backtest_report.csv")
    assert set([
        "event", "country_cow", "di_peak_year", "cohen_d",
        "cohen_d_ci_lower", "cohen_d_ci_upper", "passes",
    ]).issubset(df.columns)

def test_pass_rate_is_honestly_reported():
    # POST-HOC CORRECTION (final review, I-5): this used to assert
    # pass_rate >= 0.5. After fixing cohen_d's ddof bug (sample variance,
    # not population variance) and the "peak strictly before the event
    # year" window (a peak concurrent with the transition year no longer
    # counts as "ahead of" it), the real pass rate at the committed
    # alpha=beta=0.1 placeholder calibration is 1/3, not 2/3. Asserting a
    # >=50% floor here would either fail honestly or invite quietly
    # reverting the statistical fixes to keep the test green -- neither is
    # acceptable per this project's no-overstating-results standard. This
    # test instead checks the report is well-formed and the pass rate is
    # a genuine, reportable number; the actual rate is documented in
    # docs/LIMITATIONS.md and must not be silently inflated.
    df = pd.read_csv(DATA_GOLD / "backtest_report.csv")
    assert len(df) == 3
    assert df["passes"].dtype == bool or set(df["passes"].unique()).issubset({True, False})
    pass_rate = df["passes"].mean()
    assert 0.0 <= pass_rate <= 1.0
