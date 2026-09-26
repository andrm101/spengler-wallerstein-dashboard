import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scripts.utils.paths import DATA_GOLD, FIGURES

# NOTE (Task 12 correction): the original design spec listed a 1848 Revolutions
# marker here, but this Phase 1 pipeline hard-floors YEAR_MIN=1870 in every
# bronze ingestion script (see Task 10/11 findings), so no 1848 data exists
# anywhere in the panel. A 1848 entry would also fall outside the plotted
# xlim(1870, 1960) and never render. It is intentionally omitted rather than
# left in as dead/misleading code.
COLLAPSE_EVENTS = {1914: "WWI", 1929: "Great Depression"}
COUNTRIES_DISPLAY = {
    "USA": "United States", "UKG": "United Kingdom", "FRN": "France",
    "GMY": "Germany",       "ITA": "Italy",
}

def run() -> None:
    panel = pd.read_parquet(DATA_GOLD / "di_panel.parquet")
    panel = panel.reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))
    any_low_conf = False

    for cow, label in COUNTRIES_DISPLAY.items():
        sub = panel[panel["country_cow"] == cow].sort_values("year")
        if sub.empty:
            continue
        ax.plot(sub["year"], sub["di"], label=label, linewidth=1.5)
        ax.fill_between(sub["year"], sub["ci_lower"], sub["ci_upper"], alpha=0.1)

        # I-2: visually flag rows where any of the three layer components
        # (phi/psi/omega) was itself low-confidence/wide-CI.
        if "di_ci_wide" in sub.columns:
            low_conf = sub[sub["di_ci_wide"] == True]  # noqa: E712
            if not low_conf.empty:
                ax.scatter(low_conf["year"], low_conf["di"], marker="x", s=14,
                           alpha=0.5, color="grey", zorder=5)
                any_low_conf = True

    for year, label in COLLAPSE_EVENTS.items():
        ax.axvline(x=year, color="red", linestyle="--", linewidth=0.8, alpha=0.6)
        ax.text(year + 0.5, 92, label, fontsize=7, color="red", rotation=90, va="top")

    if any_low_conf:
        ax.scatter([], [], marker="x", s=14, alpha=0.5, color="grey",
                   label="Low-confidence (wide-CI component)")

    ax.set_xlabel("Year")
    ax.set_ylabel("Downfall Index (0–100)")
    ax.set_title("Downfall Index (Phase 1) — Western Europe + North America\n"
                 "Composite structural-vulnerability index. Uncalibrated placeholder "
                 "weights; not independently validated.")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_xlim(1870, 1960)
    ax.set_ylim(0, 100)

    # Caveat: the shaded fill_between bands are a flat +/-15% heuristic
    # (see scripts/gold/compute_di.py), not a statistical confidence interval.
    fig.text(0.01, 0.05,
             "Shaded bands: ±15% heuristic range, not a statistical confidence interval.",
             fontsize=6, color="grey")

    # Caveat: sharp early-period swings for some countries are driven by
    # fin_norm (JST tloans_gdp, 36.7% null) transitioning from a neutral-fill
    # value to a real observation, not a verified historical shift. See
    # docs/LIMITATIONS.md.
    fig.text(0.01, 0.03,
             "Caveat: sharp early-period swings for some countries reflect missing-data "
             "transitions (see docs), not verified historical events.",
             fontsize=6, color="grey")

    # Source attribution line (CLAUDE.md requirement)
    fig.text(0.01, 0.01,
             "Sources: Maddison Project Database 2023; JST Macrohistory Database R6; "
             "COW National Material Capabilities v7; V-Dem v16; Polity5 (2018); "
             "COW Trade v4.0",
             fontsize=6, color="grey")

    out = FIGURES / "di_timeline.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved → {out}")

if __name__ == "__main__":
    run()
