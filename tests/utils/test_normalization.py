import numpy as np
import pandas as pd
import pytest
from scripts.utils.normalization import minmax_normalize, zscore_clip, normalize_series

def test_minmax_normalize_basic():
    arr = np.array([0.0, 5.0, 10.0])
    result = minmax_normalize(arr)
    assert result[0] == pytest.approx(0.0)
    assert result[-1] == pytest.approx(1.0)
    assert result[1] == pytest.approx(0.5)

def test_minmax_normalize_constant():
    arr = np.array([3.0, 3.0, 3.0])
    result = minmax_normalize(arr)
    assert np.all(result == 0.5)

def test_zscore_clip_caps_at_3sigma():
    # Hand-computed: mean([0,0,0,0,0,15]) = 2.5, std = 5.59, z[-1] = (15-2.5)/5.59 = 2.236
    # That does NOT clip. Use a clear outlier: [0]*10 + [100]
    # mean=9.09, std=28.65, z[-1]=(100-9.09)/28.65=3.17 → clips to 3.0
    arr = np.array([0.0]*10 + [100.0])
    result = zscore_clip(arr, sigma=3)
    assert result[-1] == pytest.approx(3.0, abs=0.01)
    # Interior values should not be clipped
    assert all(abs(v) < 3.0 for v in result[:-1])

def test_normalize_series_invalid_method():
    s = pd.Series([1.0, 2.0, 3.0])
    with pytest.raises(ValueError, match="method must be"):
        normalize_series(s, method="invalid")
