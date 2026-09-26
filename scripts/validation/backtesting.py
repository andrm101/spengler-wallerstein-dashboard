"""
Backtesting validation: does the Downfall Index (DI) peak ahead of known
historical transitions, with a meaningful pre-collapse vs. stable-era gap?

SCOPE CORRECTION (Task 11, post-Task-10 ruling): originally 7 targets across
1848/1914/1929. Task 10's calibration run found all four 1848-revolution
targets (FRN/AUH/GMY) structurally unreachable: every bronze ingestion script
(Tasks 3-6) hard-floors YEAR_MIN=1870, so 1838-1847 data does not exist
anywhere in this pipeline, and "AUH" (Austria-Hungary) was never in
MVP_COUNTRIES. Re-ingesting further back is out of scope for Phase 1
(explicit user decision, see progress ledger). EVENTS below is trimmed to the
3 targets that can actually produce a row (UKG-1914, USA-1929, UKG-1929).

IMPORTANT CAVEAT: the alpha/beta weights baked into di_panel.parquet come
from Task 10's calibration grid search, which found an IDENTICAL loss
(3.6667) across all 55 (alpha, beta) combinations tested. The "best" pair
is therefore an arbitrary tie-break, not a validated optimum. Any reporting
of this backtest (or of alpha/beta generally) should describe the DI panel
as using a documented Phase 1 placeholder calibration, not as "calibrated
against historical transitions."
"""
import numpy as np
import pandas as pd
from scripts.utils.paths import DATA_GOLD

# Backtesting specification (from design spec Section 7.2), trimmed to the 3
# targets actually reachable given the pipeline's YEAR_MIN=1870 floor and
# MVP_COUNTRIES excluding "AUH" -- see the scope-correction note above.
# Event -> (country_cow, event_year, pre_collapse_window_start, stable_comparison_start)
EVENTS = [
    ("1914 WWI",         "UKG", 1914, 1904, 1870),
    ("1929 Depression",  "USA", 1929, 1919, 1880),
    ("1929 Depression",  "UKG", 1929, 1919, 1880),
]

def cohen_d(a: np.ndarray, b: np.ndarray) -> float:
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan")
    pooled_std = np.sqrt(((n1 - 1) * a.std()**2 + (n2 - 1) * b.std()**2) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / pooled_std if pooled_std > 0 else float("nan")

def run() -> None:
    panel = pd.read_parquet(DATA_GOLD / "di_panel.parquet")

    rows = []
    for event, country, event_year, pre_start, stable_start in EVENTS:
        if country not in panel.index.get_level_values("country_cow"):
            continue

        di = panel.loc[country, "di"].sort_index()

        pre_collapse = di.loc[pre_start : event_year - 1].dropna().values
        stable_era   = di.loc[stable_start : pre_start - 1].dropna().values

        if len(pre_collapse) == 0 or len(stable_era) == 0:
            continue

        peak_year  = int(di.loc[pre_start : event_year].idxmax())
        peak_value = float(di.loc[peak_year])
        d          = cohen_d(pre_collapse, stable_era)

        # Passing criteria (from design spec):
        # 1. DI peaks within pre-collapse window
        # 2. Cohen's d >= 0.5 (pre-collapse decade vs stable era)
        passes = (pre_start <= peak_year <= event_year) and (not np.isnan(d)) and (d >= 0.5)

        rows.append({
            "event":              event,
            "country_cow":        country,
            "event_year":         event_year,
            "di_peak_year":       peak_year,
            "di_peak_value":      round(peak_value, 2),
            "pre_collapse_mean":  round(pre_collapse.mean(), 2),
            "stable_mean":        round(stable_era.mean(), 2),
            "cohen_d":            round(d, 3) if not np.isnan(d) else None,
            "passes":             passes,
        })

    report = pd.DataFrame(rows)
    out = DATA_GOLD / "backtest_report.csv"
    report.to_csv(out, index=False)

    n_pass = report["passes"].sum()
    print(f"Backtesting: {n_pass}/{len(report)} targets passed")
    print(
        "NOTE: di_panel.parquet's alpha/beta are a documented Phase 1 placeholder "
        "(Task 10 grid search found an identical loss across all 55 combinations "
        "tested), not a validated calibration."
    )
    print(report[["event", "country_cow", "di_peak_year", "cohen_d", "passes"]].to_string())

if __name__ == "__main__":
    run()
