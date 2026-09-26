import pandas as pd
from scripts.utils.paths import DATA_GOLD

def test_backtest_report_exists():
    assert (DATA_GOLD / "backtest_report.csv").exists()

def test_backtest_schema():
    df = pd.read_csv(DATA_GOLD / "backtest_report.csv")
    assert set(["event", "country_cow", "di_peak_year", "cohen_d", "passes"]).issubset(df.columns)

def test_at_least_half_targets_pass():
    df = pd.read_csv(DATA_GOLD / "backtest_report.csv")
    pass_rate = df["passes"].mean()
    assert pass_rate >= 0.5, f"Only {pass_rate:.0%} of backtesting targets passed"
