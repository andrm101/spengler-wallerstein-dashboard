# tests/utils/test_quality_flags.py
from scripts.utils.quality_flags import quality_flag, CI_WIDE_THRESHOLD, DIMENSION_QUALITY

def test_quality_flag_known_dimension():
    result = quality_flag("urbanization")
    assert result["dimension"] == "urbanization"
    assert result["quality"] == DIMENSION_QUALITY["urbanization"]  # 9
    assert result["ci_wide"] is False  # 9 >= 5

def test_quality_flag_low_quality_dimension():
    result = quality_flag("creativity_proxy")
    assert result["quality"] == 3
    assert result["ci_wide"] is True  # 3 < 5

def test_quality_flag_boundary_at_threshold():
    # quality == CI_WIDE_THRESHOLD (5) should be ci_wide=False (strict less-than)
    result = quality_flag("lifecycle_stage")
    assert result["quality"] == CI_WIDE_THRESHOLD
    assert result["ci_wide"] is False

def test_quality_flag_unknown_dimension_defaults():
    result = quality_flag("nonexistent_dim")
    assert result["quality"] == 5
    assert result["ci_wide"] is False
