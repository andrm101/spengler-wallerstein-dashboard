import pandas as pd
import numpy as np
import pytest
from scripts.gold.compute_di import di_formula, rescale_di

def test_di_formula_zero_phi():
    assert di_formula(phi=0.0, psi=0.8, omega=0.5, alpha=0.5, beta=0.3) == 0.0

def test_di_formula_max_inputs():
    result = di_formula(phi=1.0, psi=1.0, omega=1.0, alpha=0.5, beta=0.3)
    assert result == pytest.approx(1.0 * 1.5 * 1.3)

def test_di_formula_negative_omega_reduces_score():
    base   = di_formula(phi=0.8, psi=0.6, omega=0.0,  alpha=0.5, beta=0.3)
    better = di_formula(phi=0.8, psi=0.6, omega=-0.5, alpha=0.5, beta=0.3)
    assert better < base

def test_rescale_di_bounds():
    raw = np.array([0.0, 0.5, 1.95])
    rescaled = rescale_di(raw)
    assert rescaled[0] == pytest.approx(0.0)
    assert rescaled[-1] == pytest.approx(100.0)

def test_di_panel_schema():
    df = pd.read_parquet("data/gold/di_panel.parquet")
    assert len(df) > 0
    assert set(["phi", "psi", "omega", "di", "di_raw"]).issubset(df.columns)
    assert df["di"].between(0, 100).all(skipna=True)

def test_alpha_beta_within_theoretical_constraints():
    df = pd.read_parquet("data/gold/di_panel.parquet")
    alpha = df["alpha"].iloc[0]
    beta  = df["beta"].iloc[0]
    assert 0 < alpha <= 1.0
    assert 0 < beta <= alpha
