import numpy as np
import pandas as pd
from scripts.utils.paths import DATA_SILVER, DATA_GOLD

def di_formula(phi: float, psi: float, omega: float,
               alpha: float, beta: float) -> float:
    return phi * (1 + alpha * psi) * (1 + beta * omega)

def rescale_di(raw: np.ndarray) -> np.ndarray:
    lo, hi = np.nanmin(raw), np.nanmax(raw)
    if np.isclose(lo, hi):
        return np.full_like(raw, 50.0, dtype=float)
    return (raw - lo) / (hi - lo) * 100

def build_panel(alpha: float, beta: float) -> pd.DataFrame:
    phi_df   = pd.read_parquet(DATA_SILVER / "phi_silver.parquet")[["phi"]]
    psi_df   = pd.read_parquet(DATA_SILVER / "psi_silver.parquet")[["psi"]]
    omega_df = pd.read_parquet(DATA_SILVER / "omega_silver.parquet")[["omega"]]

    panel = phi_df.join(psi_df, how="outer").join(omega_df, how="outer")

    panel["di_raw"] = di_formula(
        phi=panel["phi"].fillna(0),
        psi=panel["psi"].fillna(0),
        omega=panel["omega"].fillna(0),
        alpha=alpha,
        beta=beta,
    )
    panel["di"] = rescale_di(panel["di_raw"].values)
    panel["alpha"] = alpha
    panel["beta"]  = beta
    return panel

def run(alpha: float = 0.5, beta: float = 0.3) -> None:
    panel = build_panel(alpha, beta)

    # Uncertainty bands: ±15% of DI as Phase 1 CI (replaced by bootstrap in Phase 2)
    panel["ci_lower"] = (panel["di"] * 0.85).clip(0, 100)
    panel["ci_upper"] = (panel["di"] * 1.15).clip(0, 100)

    out = DATA_GOLD / "di_panel.parquet"
    panel.to_parquet(out)
    print(f"Saved {len(panel)} rows → {out}  (α={alpha}, β={beta})")

if __name__ == "__main__":
    run()
