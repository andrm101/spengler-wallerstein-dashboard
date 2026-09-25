import numpy as np
import pandas as pd

def minmax_normalize(arr: np.ndarray) -> np.ndarray:
    lo, hi = np.nanmin(arr), np.nanmax(arr)
    if np.isclose(lo, hi):
        return np.full_like(arr, 0.5, dtype=float)
    return (arr - lo) / (hi - lo)

def zscore_clip(arr: np.ndarray, sigma: float = 3.0) -> np.ndarray:
    mu, std = np.nanmean(arr), np.nanstd(arr)
    if np.isclose(std, 0):
        return np.zeros_like(arr, dtype=float)
    z = (arr - mu) / std
    return np.clip(z, -sigma, sigma)

def normalize_series(s: pd.Series, method: str = "minmax") -> pd.Series:
    if method not in ("minmax", "zscore"):
        raise ValueError(f"method must be 'minmax' or 'zscore', got {method!r}")
    if method == "minmax":
        return pd.Series(minmax_normalize(s.values), index=s.index, name=s.name)
    return pd.Series(zscore_clip(s.values), index=s.index, name=s.name)
