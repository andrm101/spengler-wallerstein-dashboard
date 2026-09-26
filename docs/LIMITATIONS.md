# Known Limitations — Downfall Index (Phase 1)

This document records limitations discovered during final whole-branch review
that affect how the pipeline's outputs should be read. It is intentionally a
disclosure document, not a remediation plan — none of the underlying data
issues below have been re-derived or patched; that work is out of scope for
Phase 1 and is deferred to Phase 2.

## Calibration is an uncalibrated placeholder

The α/β weights used in `data/gold/di_panel.parquet` (α=0.1, β=0.1) come from
Task 10's grid search, which found an **identical loss (3.6667) across all 55
(α, β) combinations tested** — the "best" pair is an arbitrary tie-break, not
a validated optimum. At these values, `corr(DI, Φ) ≈ 0.997`: the DI is
effectively a rescaled Spengler Φ score, and Ψ/Ω barely move the displayed
number even though the decomposition figure's bar chart visually implies all
three layers contribute meaningfully. Do not describe the DI as "calibrated"
or "validated" in any report or presentation of this work.

## Backtest outcome is contingent on the uncalibrated α/β choice

The backtest's Cohen's d and pass/fail counts (not just the calibration loss)
are sensitive to α/β. As originally reported (before the I-5 statistical
fixes below), α=β=0.1 (used in the committed panel) yielded 2/3 targets
passing, while α=0.5,β=0.3 (the original plan's default) and α=β=1.0 both
yielded 3/3.

**Updated after the I-5 fix (final review):** `cohen_d()` had a real
statistical bug — it used NumPy's default population variance (`ddof=0`)
inside a pooled-variance formula that expects sample variance (`ddof=1`).
Separately, "peak within the pre-collapse window" originally counted a peak
landing exactly on the event year as "ahead of" the transition, which is
actually concurrent with it. After fixing both (`ddof=1`, and requiring
`pre_start <= peak_year < event_year` strictly), the honest result at the
committed α=β=0.1 calibration is **1/3 targets passing** (UKG-1929 only;
UKG-1914's Cohen's d drops below the 0.5 threshold, and USA-1929's peak now
lands exactly in 1929 — concurrent with, not ahead of, the transition — so it
no longer counts as a pass). See `data/gold/backtest_report.csv` for the
per-target Cohen's d values and their bootstrap 95% CIs. This is a genuine,
not cherry-picked, finding: the fixes were statistically necessary regardless
of their effect on the pass count, and are not adjusted to preserve any
particular outcome. See `scripts/validation/backtesting.py`'s module
docstring and `docs/superpowers/plans/2026-06-25-downfall-index-phase1.md`
Task 11 for further detail.

## `fin_norm` missing-data transitions visibly drive the headline figure

`fin_norm` (Φ layer component, derived from JST Macrohistory Database R6's
`tloans_gdp`, 36.7% null) is neutral-filled to 0.5 wherever missing, and
carries the highest weight (0.25) in the Φ formula. The final review found
that this is now the dominant driver of the biggest visible swings in
`figures/di_timeline.png` — for example, the USA's sharp drop in 1880 and
France's sharp drop in 1900 both coincide exactly with `fin_norm` transitioning
from a neutral 0.5 fill to a real observed value, not with any verified
historical shift in financial structure. This also affects the pre-collapse
baseline period used by the UKG-1914 backtest target.

This is flagged directly on `di_timeline.png` via a caption note, and is
recorded here for anyone auditing the pipeline later. Re-deriving JST
coverage (e.g. interpolation, a dedicated missingness flag distinct from
`*_ci_wide`, or dropping the neutral-fill in favor of leaving `fin_norm`
`NaN` and excluding it from `phi` on a per-row basis) is deferred to Phase 2.

## Confidence bands are a heuristic, not a statistical CI

The `ci_lower`/`ci_upper` columns in `di_panel.parquet` are a flat ±15% of
the DI value (`scripts/gold/compute_di.py::run`), not a bootstrapped or
analytically derived confidence interval. This is now labeled on
`di_timeline.png` directly.

## Cross-layer confidence flag (`di_ci_wide`)

Each Silver layer (`phi_silver`, `psi_silver`, `omega_silver`) carries its own
`*_ci_wide` boolean flag for rows built from unusually sparse underlying data.
As of this fix, `compute_di.py::build_panel` combines these into a
`di_ci_wide` column on the Gold panel (`di_ci_wide = phi_ci_wide | psi_ci_wide
| omega_ci_wide`), and `di_timeline.py` marks these rows with a grey "x"
overlay. Prior to this fix, the upstream flags were computed but never read
downstream, so they had no effect on any output.
