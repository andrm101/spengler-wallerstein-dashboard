# scripts/silver/compute_phi.py
import pandas as pd
import numpy as np
from scripts.utils.paths import DATA_SILVER
from scripts.utils.normalization import normalize_series
from scripts.utils.quality_flags import DIMENSION_QUALITY, CI_WIDE_THRESHOLD

PHI_WEIGHTS: dict[str, float] = {
    "fin_norm":          0.25,
    "urban_norm":        0.20,
    "polity_norm":       0.20,
    "phase_proxy":       0.15,
    "mass_society_norm": 0.10,
    "lifecycle_norm":    0.10,
}

def _load_silver() -> pd.DataFrame:
    maddison = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    jst      = pd.read_parquet(DATA_SILVER / "jst_silver.parquet")
    urban    = pd.read_parquet(DATA_SILVER / "urban_silver.parquet")
    polity   = pd.read_parquet(DATA_SILVER / "polity_silver.parquet")
    vdem     = pd.read_parquet(DATA_SILVER / "vdem_silver.parquet")
    cinc     = pd.read_parquet(DATA_SILVER / "cinc_silver.parquet")

    base = maddison.merge(jst,    on=["country_cow", "year"], how="outer")
    base = base.merge(urban,      on=["country_cow", "year"], how="outer")
    base = base.merge(polity,     on=["country_cow", "year"], how="outer")
    base = base.merge(vdem,       on=["country_cow", "year"], how="outer")
    base = base.merge(cinc,       on=["country_cow", "year"], how="outer")
    return base.set_index(["country_cow", "year"]).sort_index()

def run() -> None:
    df = _load_silver()

    # -- fin_norm: financialization (JST tloans_gdp = total loans/GDP) ↑ = higher Φ
    df["fin_norm"] = normalize_series(df["tloans_gdp"])

    # -- urban_norm: urbanization level ↑ = higher Φ
    df["urban_norm"] = normalize_series(df["urban_pop_pct"])

    # -- polity_norm: Caesarism proxy — low polity2 (autocracy/Caesarism) = late phase
    # Invert: polity2 ranges -10 to +10; Caesarism = low score → higher Φ
    df["polity_norm"] = normalize_series(-df["polity2"])

    # -- phase_proxy: V-Dem lib_dem inverted (declining liberalism = later phase)
    df["phase_proxy"] = normalize_series(1 - df["lib_dem"])

    # -- mass_society_norm: polyarchy ↑ = mass politics = higher Φ
    df["mass_society_norm"] = normalize_series(df["polyarchy"])

    # -- lifecycle_norm: composite of age (GDP per capita growth deceleration) + institutional rigidity
    # Use 10yr rolling GDP per capita growth rate; low growth = later lifecycle
    gdppc_growth = df["gdppc"].groupby(level="country_cow").pct_change(10)
    df["lifecycle_norm"] = normalize_series(-gdppc_growth)  # declining growth = higher Φ

    # -- creativity_proxy: patents per capita proxy (placeholder for Phase 1)
    # Placeholder: set to 0.5 with ci_wide=True; replace in Phase 2
    df["creativity_proxy"] = 0.5

    # -- Weighted Φ
    df["phi"] = sum(
        df[col].fillna(0.5) * weight
        for col, weight in PHI_WEIGHTS.items()
    )

    # -- Confidence interval flag: creativity_proxy quality = 3 < CI_WIDE_THRESHOLD (5)
    # Phase 1 always folds creativity_proxy (quality below threshold) into every Φ score,
    # so phi_ci_wide is True for all rows.
    assert DIMENSION_QUALITY["creativity_proxy"] < CI_WIDE_THRESHOLD
    df["phi_ci_wide"] = True

    out = DATA_SILVER / "phi_silver.parquet"
    df[["fin_norm", "urban_norm", "polity_norm", "phase_proxy",
        "mass_society_norm", "lifecycle_norm", "creativity_proxy",
        "phi", "phi_ci_wide"]].to_parquet(out)
    print(f"Saved {len(df)} rows -> {out}")

if __name__ == "__main__":
    run()
