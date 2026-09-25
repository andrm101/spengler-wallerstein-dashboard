import pytest
from scripts.utils.country_codes import harmonize_to_cow, MVP_COUNTRIES


def test_mvp_countries_count():
    assert 12 <= len(MVP_COUNTRIES) <= 16


def test_harmonize_maddison_usa():
    assert harmonize_to_cow("USA", source="maddison") == "USA"


def test_harmonize_maddison_germany():
    assert harmonize_to_cow("DEU", source="maddison") == "GMY"


def test_harmonize_unknown_returns_none():
    assert harmonize_to_cow("XYZ", source="maddison") is None
