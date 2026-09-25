# Consolidated Evidence Inventory — Phase 0 Reconnaissance
**Date**: 2026-06-23
**Tracks Complete**: 1 (Theory), 2 (Data), 3 (Feedback Loops)

---

## Executive Summary

All three reconnaissance tracks are complete. Phase 0 has produced a clear, evidence-based picture of what is known, what is contested, and where genuine novelty lies.

**Overall verdict**: Ready for Phase 1 MVP implementation with appropriate scope constraints. The project sits on a genuine research frontier with no existing unified framework — this is the primary novel contribution. Data availability is excellent for the MVP epoch (1850–1950, Western Europe + North America). Feedback loop evidence is weaker than theory predicts, which is itself an important finding that shapes the dashboard's epistemic framing.

---

## Track 1: Theoretical Validation — Summary

**Source**: `evidence/track-1-theoretical-validation.md`

### Key Findings

**Spengler operationalization**: Virtually none exists in peer-reviewed literature. The morphology remains qualitative; soul-form and prime symbols have never been numerically operationalized. Bonta (2014, 2015) achieved categorical semiotic classification but not quantification. This is not a technical gap but a conceptual one — Spengler explicitly rejected numerical measurement.

**Wallerstein operationalization**: Substantially more mature. Core-periphery structure is **Established** via trade network analysis and labour flow accounting (Hickel et al. 2024, *Nature Communications*). Hegemonic cycles are **Plausible** — three hegemons identified but index weighting is arbitrary and Kwon (2011) shows England dominated in two successive periods, contradicting Wallerstein's exact dates. No prospective prediction tool exists.

**Cybernetics operationalization**: Critical slowing down validated in Neolithic population collapse (Downey et al. 2016, *PNAS*) and partially in financial crises (1987 Black Monday yes; 2000/2008 mixed). Bifurcation detection is **Established** on controlled systems, **Plausible** on social systems. Entropy metrics are **Exploratory** — Scaffolding Entropy (2024, preprint) has two retrospective validations only.

**Integration**: **Zero published work** combining all three frameworks. Wallerstein + cybernetics at **Plausible** (Schunck et al. 2024 model). Spengler + cybernetics and Spengler + Wallerstein have no published precedent.

### Novelty Confirmed

The unified Spengler-Wallerstein-cybernetic framework is genuinely novel. Three bridge theories constitute the innovation:
1. Spengler phase transitions as detectable bifurcation points
2. Wallerstein hegemonic cycles as complexity overshoot (Tainter mechanism)
3. Unequal exchange operationalized as a positive feedback loop with early-warning signatures

---

## Track 2: Data Source Audit — Summary

**Source**: `evidence/track-2-data-audit.md`

### Key Findings

**Data readiness**: HIGH
- 17/20 dimensions have ready-made peer-reviewed datasets
- 3/20 require novel operationalization: Soul-Form (LDA + DNN), Artistic Creativity (GNN composite), Commodity Chain Position (I-O reconstruction)
- 5 novel publishable metrics identified: Civilizational Entropy Index, GNN Creativity Metric, Hegemonic Stability Index, Semi-Peripheral Stabilization Score, Terms-of-Trade Vulnerability Index

**MVP epoch (1850–1950, Western Europe + North America)**: All 17 ready-made dimensions measurable with high confidence. 8 core datasets sufficient (Maddison, HYDE, V-Dem, Polity5, COW, Penn WT, World Bank GFDD, CINC).

**Best dataset**: HYDE 3.2 (urbanization; 9/10 quality; pre-1500 usable with caveats)

**Highest-confidence dimensions**: Urbanization (9/10), Economic Form & Financialization (8/10), Capital Intensity Ratio (8/10), Hegemonic Cycle Position (8/10)

**Lowest-confidence dimensions**: Soul-Form (0/10 — no data exists), Commodity Chain Position (2/10 — pre-1990 gap), Artistic Creativity (3/10 — fragmentary)

**Epoch quality gradient**:
- Pre-1500: VERY LOW — exploratory/narrative only
- 1500–1800: MEDIUM — pattern identification; ±30–40% CI
- 1800–1950: HIGH — MVP sweet spot; ±10–15% CI
- 1950–2020: VERY HIGH — global, <5% typical error

### Phase 1 Data Readiness Confirmed

Six weeks to download, standardize, validate, and compute all 17 ready-made dimensions. Novel dimensions (#3, #8, #5 in full form) deferred to Phase 2.

---

## Track 3: Feedback Loop Validation — Summary

**Source**: `evidence/track-3-feedback-loops.md`

### Key Findings

**Confidence tier distribution**:
- PLAUSIBLE (2): Financialization → Cultural Decay; Urbanization → Atomization
- EXPLORATORY (5): Elite Overproduction → Instability; Hegemonic Decline → Crisis; Semi-Peripheral Buffering; Trade Rebalancing; Cultural Renaissance

**This is lower than theory predicts** — none of the seven loops achieved ESTABLISHED status. This is itself a finding: the cybernetic framework is at an early empirical stage.

**Critical anomaly: Positive loops weaker than expected**
- Hegemonic decline loop: British-American transition was peaceful (the only historical hegemonic transition without war). INF treaty reversed Cold War arms race without conflict. Power transition theory overstates conflict probability.
- Elite overproduction loop: Fails in institutionally open systems (US, China). Works in closed labor markets (Chile). Theory requires specification of boundary conditions.

**Critical insight: Negative loops require active management**
- Semi-peripheral buffering (Korea, Taiwan) was achieved through deliberate state capacity (directed credit, industrial policy), not passive equilibrium.
- Trade rebalancing failed across Latin America — the loop does not activate without sufficient technological capability.
- Passive systems do not self-stabilize; absence of active stabilization is a risk factor.

**Fundamental architectural finding for dashboard**:
Feedback loops are **conditionally activated** by institutional arrangements, not mechanically driven by structural position alone. Zone classification + institutional quality index must jointly determine feedback loop activation probability.

---

## Cross-Track Insights

### Where Tracks Reinforce Each Other

1. **Data maturity matches theoretical maturity**: Wallerstein's well-operationalized theory (Track 1) corresponds to the best-quality data (Track 2 — COW Trade, CINC, Penn WT, Hickel methodology). Spengler's unmeasured theory corresponds to the data gaps (Soul-Form: 0/10; Creativity: 3/10). The gaps are aligned — which means the project's novel measurement work targets exactly the theoretical frontier.

2. **Feedback loop weakness confirms data limitations**: Track 3's finding that loops are mostly Plausible/Exploratory aligns with Track 1's finding that cybernetic early-warning methods have limited validation on social systems. No historical data source provides the high-frequency, long-duration time-series needed for rigorous feedback loop estimation.

3. **MVP scope is well-supported across all tracks**: The 1850–1950 Western European epoch has the best data (Track 2), is where Wallerstein's hegemonic transitions are most documented (Track 1), and is where feedback loops like financialization-inequality have the most empirical grounding (Track 3: OECD panel studies cover this period).

### Where Tracks Conflict or Introduce Tension

1. **Temporal scale mismatch (confirmed)**: Track 1 documents that Spengler operates at 1,000+ year grain, Wallerstein at 90–120 years, cybernetics at 5–50 years. Track 2 shows that pre-1500 data is VERY LOW quality. This means the Spengler long-wave component will require narrative/historiographic grounding rather than quantitative modeling. The dashboard must distinguish between quantitative layers (Wallerstein + cybernetics) and interpretive layers (Spengler phase classification).

2. **Institutional quality as confounding variable**: Track 3 shows that institutional arrangements mediate feedback loop strength. Track 2 doesn't include institutional quality as a standalone dimension. This gap should be addressed by elevating V-Dem institutional indicators as explicit control variables, not just proxies for political form.

3. **Causal direction uncertainty**: Track 1 flags that the direction of causality between Spengler's phase transitions and Wallerstein's structural dynamics is unresolved. Track 3 shows that reverse causality is a concern within individual loops (financialization vs. wage decline). The VAR modeling approach (bidirectional causality testing) is the correct methodological response.

---

## Gaps Requiring Follow-Up

| Gap | Track | Priority | Proposed Resolution |
|-----|-------|----------|---------------------|
| Soul-form operationalization: no data exists | 1, 2 | Medium | LDA topic modeling on digitized historical texts; DNN image analysis of art/architecture (Phase 2) |
| Commodity chain position pre-1990: no I-O matrices | 2 | Medium | Reconstruct from national accounts (1960–1990); Product Complexity Index as proxy (1962+) |
| GNN creativity metric: fragmentary inputs | 2 | Low | Patent networks (1850+) + citation networks (1900+) + publications (1800+) combined as Phase 2 deliverable |
| Feedback loop activation conditions: not formally specified | 3 | High | Add institutional quality index (from V-Dem) as conditional moderator in VAR models; test whether loop strength varies by regime type |
| Hegemonic cycle dating: no consensus | 1 | Low | Use Kwon (2011) methodology as baseline; document contested dates; present multiple scenarios in dashboard |
| Pre-1500 data quality: VERY LOW | 2 | Low | Commit to narrative/historiographic layer only for pre-1500; no quantitative claims in this epoch |
| Critical slowing down validation on social systems | 1, 3 | Medium | Phase 2 research track: test CSD indicators on 1800–1950 data for known transitions (1848, 1917, 1929) |

---

**Phase 0 Status: ALL THREE TRACKS COMPLETE**
**Readiness for Phase 1: CONDITIONAL YES — see IMPLEMENTATION-READINESS.md**
