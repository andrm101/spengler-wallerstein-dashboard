import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scripts.utils.paths import DATA_GOLD, FIGURES

# NOTE (Task 12 correction): the original design spec listed a 1848 Revolutions
# marker here, but this Phase 1 pipeline hard-floors YEAR_MIN=1870 in every
# bronze ingestion script (see Task 10/11 findings), so no 1848 data exists
# anywhere in the panel. A 1848 entry would also fall outside the plotted
# xlim(1850, 1950) and never render. It is intentionally omitted rather than
# left in as dead/misleading code.
COLLAPSE_EVENTS = {1914: "WWI", 1929: "Great Depression"}
COUNTRIES_DISPLAY = {
    "USA": "United States", "UKG": "United Kingdom", "FRN": "France",
    "GMY": "Germany",       "AUH": "Austria-Hungary", "ITA": "Italy",
}

def run() -> None:
    panel = pd.read_parquet(DATA_GOLD / "di_panel.parquet")
    panel = panel.reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))

    for cow, label in COUNTRIES_DISPLAY.items():
        sub = panel[panel["country_cow"] == cow].sort_values("year")
        if sub.empty:
            continue
        ax.plot(sub["year"], sub["di"], label=label, linewidth=1.5)
        ax.fill_between(sub["year"], sub["ci_lower"], sub["ci_upper"], alpha=0.1)

    for year, label in COLLAPSE_EVENTS.items():
        ax.axvline(x=year, color="red", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.text(year + 0.5, 92, label, fontsize=7, color="red", rotation=90, va="top")

    ax.set_xlabel("Year")
    ax.set_ylabel("Downfall Index (0–100)")
    ax.set_title("Downfall Index — Western Europe + North America, 1850–1950\n"
                 "Structural vulnerability score. High scores indicate configurations "
                 "historically associated with systemic stress.")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(1850, 1950)
    ax.set_ylim(0, 100)

    # Source attribution line (CLAUDE.md requirement)
    fig.text(0.01, 0.01,
             "Sources: Maddison (2020), V-Dem v13, Polity5, COW Trade v4.0, CINC v6.0, "
             "Penn WT v10.1, World Bank GFDD, HYDE 3.2",
             fontsize=6, color="grey")

    out = FIGURES / "di_timeline.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {out}")

if __name__ == "__main__":
    run()
