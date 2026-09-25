from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW    = ROOT / "data" / "raw"
DATA_BRONZE = ROOT / "data" / "bronze"
DATA_SILVER = ROOT / "data" / "processed"
DATA_GOLD   = ROOT / "data" / "gold"
FIGURES     = ROOT / "figures"

def ensure_dirs() -> None:
    for p in [DATA_BRONZE, DATA_SILVER, DATA_GOLD, FIGURES]:
        p.mkdir(parents=True, exist_ok=True)
