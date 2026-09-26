# Orchestrates all dashboard outputs.
from scripts.dashboard.di_timeline import run as timeline
from scripts.dashboard.di_decomposition import run as decompose

# Task 12 correction: the original list included ("AUH", 1910) and
# ("FRN", 1845). "AUH" (Austria-Hungary) was never in MVP_COUNTRIES
# (scripts/utils/country_codes.py), and 1845 predates this pipeline's
# hard YEAR_MIN=1870 floor (every bronze ingestion script filters to it).
# Both pairs are absent from di_panel.parquet's index, which would have
# silently produced an all-zero/NaN "NO DATA" figure rather than crashing.
# Replaced with GMY-1932 (Weimar Germany, pre-Nazi seizure of power --
# post-Depression European case) and RUS-1917 (Russian Revolution --
# WWI-era case), both confirmed present in data/gold/di_panel.parquet,
# alongside the original USA-1925 and UKG-1913 pairs.
if __name__ == "__main__":
    timeline()
    for country, year in [("USA", 1925), ("UKG", 1913), ("GMY", 1932), ("RUS", 1917)]:
        decompose(country, year)
