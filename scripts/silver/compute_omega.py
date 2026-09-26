import pandas as pd
import numpy as np
from scripts.utils.paths import DATA_SILVER
from scripts.utils.normalization import zscore_clip

OMEGA_WEIGHTS: dict[str, float] = {
    "d_fin":       0.25,
    "d_hegemon":   0.25,
    "d_network":   0.20,
    "d_creativity": 0.15,
    "d_tot":       0.15,
}
WINDOW = 10

def _first_derivative(series: pd.Series, window: int) -> pd.Series:
    return series.diff(window) / window

def run() -> None:
    phi = pd.read_parquet(DATA_SILVER / "phi_silver.parquet")
    psi = pd.read_parquet(DATA_SILVER / "psi_silver.parquet")

    df = phi[["fin_norm"]].join(psi[["hegemon_norm", "network_norm", "tot_norm"]], how="outer")

    result_parts = []
    for country, grp in df.groupby(level="country_cow"):
        grp = grp.sort_index(level="year")
        part = pd.DataFrame(index=grp.index)

        # Each derivative: positive = deteriorating = contributes to higher Ω
        part["d_fin"]       = _first_derivative(grp["fin_norm"],     WINDOW)   # rising fin = worse
        part["d_hegemon"]   = _first_derivative(grp["hegemon_norm"], WINDOW)   # rising pressure = worse
        part["d_network"]   = _first_derivative(grp["network_norm"], WINDOW)   # rising peripherality = worse
        part["d_creativity"]= 0.0  # Phase 1 placeholder; Phase 2 replaces with patent derivative
        part["d_tot"]       = _first_derivative(grp["tot_norm"],     WINDOW)   # worsening ToT = worse

        result_parts.append(part)

    df_omega = pd.concat(result_parts)

    # Standardize each derivative (zscore, clip ±3σ) then rescale to [-1, +1].
    # d_creativity is a Phase-1 constant placeholder (0.0 for every row): its
    # standard deviation is 0, and running it through zscore_clip would rely
    # on that function's zero-std guard (which returns an all-zero array, not
    # NaN/inf) to stay well-behaved. To avoid depending on that guard and to
    # keep the placeholder's intent explicit, skip zscore_clip for it and
    # leave it at its already-bounded constant value.
    for col in OMEGA_WEIGHTS:
        if col == "d_creativity":
            continue
        z = zscore_clip(df_omega[col].dropna().values)
        # Map ±3 z-score range → [-1, +1]
        full = pd.Series(float("nan"), index=df_omega.index)
        full.loc[df_omega[col].notna()] = z / 3.0
        df_omega[col] = full.clip(-1, 1)

    df_omega["omega"] = sum(
        df_omega[col].fillna(0) * weight
        for col, weight in OMEGA_WEIGHTS.items()
    ).clip(-1, 1)

    df_omega["omega_ci_wide"] = df_omega["omega"].isna()

    out = DATA_SILVER / "omega_silver.parquet"
    df_omega[list(OMEGA_WEIGHTS.keys()) + ["omega", "omega_ci_wide"]].to_parquet(out)
    print(f"Saved {len(df_omega)} rows → {out}")

if __name__ == "__main__":
    run()
