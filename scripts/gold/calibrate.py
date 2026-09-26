# Grid search over alpha and beta. Objective: RMSE between DI peak year
# and known historical transition years.
import numpy as np
import pandas as pd
from itertools import product
from scripts.utils.paths import DATA_SILVER, DATA_GOLD
from scripts.gold.compute_di import build_panel

# Known transition targets: (country_cow, target_peak_year_range)
# DI should peak within the window [lo, hi] before the event.
#
# KNOWN DATA-COVERAGE GAPS (Task 10 investigation, documented rather than
# silently patched or worked around):
#
# 1. "AUH" (Austria-Hungary) targets never match any row in `panel`.
#    MVP_COUNTRIES (scripts/utils/country_codes.py) only contains "AUS" and
#    "HUN" separately -- per the documented pre-1918 AUH -> AUS + HUN split
#    -- and every Silver/Gold table is filtered to MVP_COUNTRIES. Since
#    "AUH" is not in that list, phi_silver/psi_silver/omega_silver never
#    contain an "AUH" country_cow value, so calibration_loss's
#    `if country not in panel.index...: continue` guard silently skips both
#    AUH targets.
#
# 2. Empirically (see describe_target_coverage / calibrate.py console
#    output), the 1848-revolution window [1840, 1847] also has NO data for
#    "FRN" and "GMY", because phi_silver/psi_silver/omega_silver only cover
#    1870-1960 (Maddison/V-Dem/Polity harmonized coverage starts at 1870).
#    So even the non-AUH 1848 targets are unusable with the current Silver
#    panel, independent of the AUH issue.
#
# Combined effect: only 3 of the 7 targets actually contribute to
# calibration_loss -- UKG(1904-1913), USA(1919-1928), UKG(1919-1928). Both
# 1848-revolution targets (all three country entries) are dropped: two for
# the AUH/MVP_COUNTRIES mismatch, and FRN/GMY for lack of pre-1870 data.
#
# Decision: left CALIBRATION_TARGETS as-is rather than substituting "AUS"
# for "AUH" or removing the 1848 targets, because (a) Austria alone is not
# a defensible historical stand-in for the pre-1918 Dual Monarchy's combined
# fiscal/political stress, and (b) the 1848 targets cannot be evaluated at
# all right now regardless of country coding, since the Silver panel doesn't
# extend before 1870. Silently rewriting the target list would obscure that
# the calibration is effectively 3/7-target for Phase 1. Revisit if/when (i)
# AUH-specific Silver data is added, harmonized separately from post-1918
# AUS/HUN, and (ii) pre-1870 Maddison/V-Dem/Polity coverage is ingested.
CALIBRATION_TARGETS = [
    ("FRN", 1840, 1847),   # 1848 revolutions — France
    ("AUH", 1840, 1847),   # 1848 revolutions — Austria-Hungary (no coverage, see note above)
    ("GMY", 1840, 1847),   # 1848 revolutions — Prussia/Germany
    ("UKG", 1904, 1913),   # 1914 WWI — UK
    ("AUH", 1904, 1913),   # 1914 WWI — Austria-Hungary (no coverage, see note above)
    ("USA", 1919, 1928),   # 1929 Depression — USA
    ("UKG", 1919, 1928),   # 1929 Depression — UK
]

def peak_year(series: pd.Series) -> int:
    return int(series.idxmax())

def calibration_loss(alpha: float, beta: float) -> float:
    panel = build_panel(alpha, beta)
    errors = []
    for country, lo, hi in CALIBRATION_TARGETS:
        if country not in panel.index.get_level_values("country_cow"):
            continue
        series = panel.loc[country, "di"].sort_index()
        window = series.loc[lo:hi]
        if window.empty:
            continue
        # Peak must be within window; penalize distance to window center
        peak = peak_year(window)
        center = (lo + hi) // 2
        errors.append(abs(peak - center))
    return np.mean(errors) if errors else float("inf")

def describe_target_coverage(alpha: float, beta: float) -> tuple[list, list]:
    """Diagnostic: report which CALIBRATION_TARGETS actually contribute to
    calibration_loss at the given (alpha, beta), and which are skipped
    (country absent from panel, or no data in the [lo, hi] window)."""
    panel = build_panel(alpha, beta)
    used, skipped = [], []
    for country, lo, hi in CALIBRATION_TARGETS:
        label = f"{country} {lo}-{hi}"
        if country not in panel.index.get_level_values("country_cow"):
            skipped.append((label, "country not in panel (not in MVP_COUNTRIES)"))
            continue
        series = panel.loc[country, "di"].sort_index()
        window = series.loc[lo:hi]
        if window.empty:
            skipped.append((label, "no data in window"))
            continue
        used.append(label)
    return used, skipped

def run() -> None:
    alpha_grid = np.arange(0.1, 1.1, 0.1)
    beta_grid  = np.arange(0.1, 1.1, 0.1)

    best_loss  = float("inf")
    best_alpha = 0.5
    best_beta  = 0.3

    results = []
    for alpha in alpha_grid:
        for beta in beta_grid:
            if beta > alpha:  # theoretical constraint: β ≤ α
                continue
            loss = calibration_loss(round(alpha, 1), round(beta, 1))
            results.append({"alpha": round(alpha, 1), "beta": round(beta, 1), "loss": loss})
            if loss < best_loss:
                best_loss  = loss
                best_alpha = round(alpha, 1)
                best_beta  = round(beta, 1)

    results_df = pd.DataFrame(results).sort_values("loss")
    out = DATA_GOLD / "calibration_results.csv"
    results_df.to_csv(out, index=False)
    print(f"Best α={best_alpha}, β={best_beta}, loss={best_loss:.2f}")
    print(f"Calibration grid saved → {out}")

    used, skipped = describe_target_coverage(best_alpha, best_beta)
    print(f"Calibration target coverage at best (α={best_alpha}, β={best_beta}): "
          f"{len(used)}/{len(CALIBRATION_TARGETS)} targets contributed")
    for label in used:
        print(f"  USED:    {label}")
    for label, reason in skipped:
        print(f"  SKIPPED: {label} ({reason})")

    return best_alpha, best_beta

if __name__ == "__main__":
    alpha, beta = run()
    from scripts.gold.compute_di import run as di_run
    di_run(alpha=alpha, beta=beta)
