import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scripts.utils.paths import DATA_GOLD, DATA_SILVER, FIGURES

def run(country: str = "USA", year: int = 1925) -> None:
    phi_df   = pd.read_parquet(DATA_SILVER / "phi_silver.parquet")
    psi_df   = pd.read_parquet(DATA_SILVER / "psi_silver.parquet")
    omega_df = pd.read_parquet(DATA_SILVER / "omega_silver.parquet")
    panel    = pd.read_parquet(DATA_GOLD   / "di_panel.parquet")

    di_score = panel.loc[(country, year), "di"] if (country, year) in panel.index else float("nan")
    alpha    = panel["alpha"].iloc[0]
    beta     = panel["beta"].iloc[0]

    # Defensive check (Task 12 correction): the fallback logic above lets a
    # caller pass a (country, year) pair that doesn't exist anywhere in the
    # panel without raising -- it just silently produces NaN/0.0 values that
    # would otherwise be rendered as if they were a real DI score. Per this
    # project's no-overstating-results standard, that must be visible in the
    # figure itself, not just swallowed.
    data_missing = pd.isna(di_score)
    if data_missing:
        print(
            f"WARNING: ({country}, {year}) not found in di_panel.parquet index -- "
            "no real data for this country/year. Rendering a NO DATA figure "
            "instead of a misleading data-less chart."
        )

    phi_val   = phi_df.loc[(country, year), "phi"]   if (country, year) in phi_df.index   else 0.0
    psi_val   = psi_df.loc[(country, year), "psi"]   if (country, year) in psi_df.index   else 0.0
    omega_val = omega_df.loc[(country, year), "omega"] if (country, year) in omega_df.index else 0.0

    labels = ["Φ Phase Position\n(Spengler)", "Ψ Structural Pressure\n(Wallerstein)", "Ω Momentum\n(Cybernetics)"]
    values = [phi_val, psi_val, omega_val]
    colors = ["#4472C4", "#ED7D31", "#A9D18E"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: bar chart of sub-scores
    axes[0].bar(labels, values, color=colors, width=0.5)
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("Sub-score (0–1)")
    axes[0].set_title(f"Layer Sub-scores: {country}, {year}")
    for i, v in enumerate(values):
        axes[0].text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=10)

    # Right: DI score display
    axes[1].set_xlim(0, 100)
    axes[1].set_ylim(0, 1)
    axes[1].barh([0.5], [0.0 if data_missing else di_score], color="#C00000", height=0.3)
    axes[1].set_xlabel("Downfall Index (0–100)")
    if data_missing:
        axes[1].set_title(f"DI = NO DATA  (country/year not in panel)")
    else:
        axes[1].set_title(f"DI = {di_score:.1f}  (α={alpha}, β={beta}: Phase-1 placeholder, not calibrated)")
    axes[1].axvline(x=50, color="grey", linestyle="--", linewidth=0.8)
    axes[1].text(50, 0.85, "Midpoint", ha="center", fontsize=8, color="grey")
    axes[1].set_yticks([])
    if not data_missing:
        axes[1].annotate(
            "Note: at these placeholder weights, DI is dominated by Φ\n"
            "(Ψ/Ω contribute minimally).",
            xy=(0.5, -0.28), xycoords="axes fraction",
            ha="center", va="top", fontsize=7, color="#555555",
        )

    fig.suptitle(
        f"Downfall Index Decomposition — {country}, {year}\n"
        "Structural vulnerability and momentum. Not a collapse prediction.",
        fontsize=11
    )
    fig.text(0.01, 0.01,
             "Sources: Maddison Project Database 2023; JST Macrohistory Database R6; "
             "COW National Material Capabilities v7; V-Dem v16; Polity5 (2018); "
             "COW Trade v4.0",
             fontsize=6, color="grey")

    out = FIGURES / f"di_decomposition_{country}_{year}.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {out}")

if __name__ == "__main__":
    run("USA", 1925)
