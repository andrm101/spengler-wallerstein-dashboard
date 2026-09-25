DIMENSION_QUALITY: dict[str, int] = {
    "urbanization":        9,
    "financialization":    8,
    "capital_intensity":   8,
    "hegemonic_cycle":     8,
    "terms_of_trade":      7,
    "political_form":      7,
    "network_centrality":  7,
    "external_power":      7,
    "religious_form":      6,
    "mass_society":        6,
    "zone_classification": 6,
    "lifecycle_stage":     5,
    "interstate_cohesion": 7,
    "surplus_extraction":  5,
    "semi_peripheral":     5,
    "culture_phase":       4,
    "creativity_proxy":    3,
}

CI_WIDE_THRESHOLD = 5


def quality_flag(dimension: str) -> dict:
    """Return quality metadata for a named dimension."""
    quality = DIMENSION_QUALITY.get(dimension, 5)
    return {
        "dimension": dimension,
        "quality": quality,
        "ci_wide": quality < CI_WIDE_THRESHOLD,
    }
