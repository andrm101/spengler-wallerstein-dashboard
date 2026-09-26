import pandas as pd
import numpy as np
from scripts.utils.paths import DATA_SILVER
from scripts.utils.normalization import normalize_series

PSI_WEIGHTS: dict[str, float] = {
    "hegemon_norm":   0.25,
    "tot_norm":       0.20,
    "network_norm":   0.20,
    "zone_norm":      0.15,
    "surplus_norm":   0.10,
    "cohesion_norm":  0.10,
}

def _compute_network_centrality(trade: pd.DataFrame) -> pd.Series:
    # Eigenvector centrality approximation: trade share of total world trade
    # Full network eigenvector requires scipy; this is a Phase 1 approximation.
    total_by_year = trade.groupby("year")["total_exports"].transform("sum")
    trade = trade.copy()
    trade["centrality"] = trade["total_exports"] / total_by_year.replace(0, float("nan"))
    return trade.set_index(["country_cow", "year"])["centrality"]

def run() -> None:
    maddison  = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet")
    cinc      = pd.read_parquet(DATA_SILVER / "cinc_silver.parquet")
    cow_trade = pd.read_parquet(DATA_SILVER / "cow_trade_silver.parquet")

    base = maddison.merge(cinc, on=["country_cow", "year"], how="outer")
    base = base.merge(cow_trade, on=["country_cow", "year"], how="outer")
    df = base.set_index(["country_cow", "year"]).sort_index()

    # -- hegemon_norm: declining CINC share = declining power = higher pressure
    # Hegemon has LOW pressure (↑ cinc = ↓ Ψ), so invert
    df["hegemon_norm"] = normalize_series(1 - df["cinc_share"].fillna(0))

    # -- tot_norm: terms of trade proxy — exports/imports ratio
    # Low ratio = unfavorable ToT = higher pressure
    df["tot_raw"] = df["total_exports"] / df["total_imports"].replace(0, float("nan"))
    df["tot_norm"] = normalize_series(1 - df["tot_raw"])  # unfavorable = higher Ψ

    # -- network_norm: trade centrality (higher centrality = lower pressure → invert)
    centrality = _compute_network_centrality(cow_trade)
    df["network_norm"] = normalize_series(1 - centrality)

    # -- zone_norm: GDP per capita rank within sample per year (peripheral = higher Ψ)
    gdppc = pd.read_parquet(DATA_SILVER / "maddison_silver.parquet").set_index(["country_cow", "year"])["gdppc"]
    rank_pct = gdppc.groupby(level="year").rank(pct=True, ascending=True)
    df["zone_norm"] = normalize_series(1 - rank_pct)  # low GDP rank = periphery = higher Ψ

    # -- surplus_norm: exports - imports as share of exports (net extraction direction)
    df["surplus_raw"] = (df["total_imports"] - df["total_exports"]) / df["total_exports"].replace(0, float("nan"))
    df["surplus_norm"] = normalize_series(df["surplus_raw"])

    # -- cohesion_norm: Phase-1 proxy for interstate economic cohesion.
    # cow_trade_silver.parquet (Task 6) has no bilateral partner-count field —
    # only aggregate total_exports/total_imports per (country_cow, year). A true
    # "trade partner count" (the brief's original `trade_partners` column) does
    # not exist in the ingested data and referencing it raises KeyError.
    # Documented approximation: use combined trade volume (exports + imports),
    # normalized, as a stand-in for the country's degree of economic
    # interconnection with the rest of the system. Larger combined trade volume
    # implies more/deeper interstate economic ties -> higher cohesion -> LOWER
    # Ψ pressure, hence the outer `1 -` inversion (consistent with the other
    # dimensions, where the *_norm columns represent pressure, not the raw
    # underlying construct). This is a coarser proxy than a true partner count
    # (it conflates trade size with trade breadth) and should be revisited if a
    # bilateral trade dataset is ingested in a later phase.
    trade_volume = df["total_exports"].fillna(0) + df["total_imports"].fillna(0)
    df["cohesion_norm"] = normalize_series(1 - normalize_series(trade_volume))

    df["psi"] = sum(
        df[col].fillna(0.5) * weight
        for col, weight in PSI_WEIGHTS.items()
    )
    df["psi_ci_wide"] = df["psi"].isna()

    out = DATA_SILVER / "psi_silver.parquet"
    df[["hegemon_norm", "tot_norm", "network_norm", "zone_norm",
        "surplus_norm", "cohesion_norm", "psi", "psi_ci_wide"]].to_parquet(out)
    print(f"Saved {len(df)} rows -> {out}")

if __name__ == "__main__":
    run()
