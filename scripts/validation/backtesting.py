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

NOTE: while the calibration *loss* is flat across the grid (Task 10 finding),
this backtest's Cohen's d and pass/fail outcome ARE sensitive to the choice of
alpha/beta -- e.g. alpha=beta=0.1 (used here) yields a different pass count
than alpha=0.5,beta=0.3 (the original brief default) or alpha=beta=1.0. The
result reported here was not cherry-picked, but it is contingent on an
uncalibrated hyperparameter choice and should not be read as a robust,
calibration-independent finding.
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
    # ddof=1: sample (not population) variance, as required by the pooled
    # sample-variance formula below.
    pooled_std = np.sqrt(((n1 - 1) * a.std(ddof=1)**2 + (n2 - 1) * b.std(ddof=1)**2) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / pooled_std if pooled_std > 0 else float("nan")

def cohen_d_ci(a: np.ndarray, b: np.ndarray, n_boot: int = 1000,
               seed: int = 42) -> tuple[float, float]:
    """Percentile bootstrap 95% CI for Cohen's d (Phase 1 simple approach;
    per CLAUDE.md statistical-rigor requirements -- point estimates alone
    are insufficient)."""
    np.random.seed(seed)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan")
    boot_d = np.empty(n_boot)
    for i in range(n_boot):
        a_s = np.random.choice(a, size=n1, replace=True)
        b_s = np.random.choice(b, size=n2, replace=True)
        boot_d[i] = cohen_d(a_s, b_s)
    boot_d = boot_d[~np.isnan(boot_d)]
    if len(boot_d) == 0:
        return float("nan"), float("nan")
    return float(np.percentile(boot_d, 2.5)), float(np.percentile(boot_d, 97.5))

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

        # Peak window uses event_year (inclusive), the peak-detection window
        # here is separate from the "passes" window check below.
        peak_year  = int(di.loc[pre_start : event_year].idxmax())
        peak_value = float(di.loc[peak_year])
        d          = cohen_d(pre_collapse, stable_era)
        d_ci_lo, d_ci_hi = cohen_d_ci(pre_collapse, stable_era)

        # Passing criteria (from design spec):
        # 1. DI peaks strictly before the transition year (peak_year ==
        #    event_year is concurrent with the transition, not "ahead of"
        #    it -- I-5 fix).
        # 2. Cohen's d >= 0.5 (pre-collapse decade vs stable era)
        passes = (pre_start <= peak_year < event_year) and (not np.isnan(d)) and (d >= 0.5)

        rows.append({
            "event":               event,
            "country_cow":         country,
            "event_year":          event_year,
            "di_peak_year":        peak_year,
            "di_peak_value":       round(peak_value, 2),
            "pre_collapse_mean":   round(pre_collapse.mean(), 2),
            "stable_mean":         round(stable_era.mean(), 2),
            "cohen_d":             round(d, 3) if not np.isnan(d) else None,
            "cohen_d_ci_lower":    round(d_ci_lo, 3) if not np.isnan(d_ci_lo) else None,
            "cohen_d_ci_upper":    round(d_ci_hi, 3) if not np.isnan(d_ci_hi) else None,
            "passes":              passes,
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
    print("NOTE: backtest outcome depends on uncalibrated alpha/beta -- see docstring caveat.")
    print(report[["event", "country_cow", "di_peak_year", "cohen_d", "passes"]].to_string())

if __name__ == "__main__":
    run()
