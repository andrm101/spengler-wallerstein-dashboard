# Design Spec: Downfall Index (DI)
**Date**: 2026-06-23
**Status**: Approved — Ready for Implementation Planning
**Author**: Andrei Manoloiu

---

## 1. Purpose

The Downfall Index (DI) is a hierarchical composite metric that operationalizes civilizational vulnerability to systemic collapse. It integrates three theoretical frameworks — Spengler's civilizational morphology, Wallerstein's world-systems theory, and cybernetic systems theory — into a single interpretable score per nation per year.

**Dual deliverable**:
- **Academic**: A novel composite metric, publishable as a standalone contribution in macro-history, complexity science, or world-systems journals
- **Dashboard**: The headline KPI of the Spengler-Wallerstein-Dashboard; the primary signal visible on first load

**What the index does NOT claim**: The DI measures structural vulnerability and momentum — not deterministic collapse prediction. A nation scoring DI = 85 exhibits the configuration of phase, structural pressure, and momentum historically associated with collapse episodes. It is not predicted to collapse. This distinction is stated in every publication and every dashboard tooltip. Theoretical anchor: Roman (2023–24) *Journal of Big History* — Theta-process identifies collapse-prone configurations retrospectively without implying prospective determinism.

---

## 2. Architecture

The DI is a three-layer hierarchical composite. Layers are sequential, not parallel. Each layer conditions the next.

```
Layer 1: Spengler Phase Position (Φ)
         "Where in the lifecycle is this civilization?"
         Slow-moving background variable. Sets the baseline
         susceptibility. A stable early-culture nation cannot
         score high regardless of other signals.
                    ↓  amplified by
Layer 2: Wallerstein Structural Pressure (Ψ)
         "How much is the world-system working against it?"
         Adjusts the baseline upward based on structural
         position, extraction dynamics, and hegemonic cycle.
                    ↓  modified by urgency
Layer 3: Cybernetic Momentum (Ω)
         "How fast is deterioration accelerating?"
         First derivatives of key dimensions over a rolling
         10-year window. Distinguishes secular stagnation
         from rapid approach to tipping point.
```

**Combination formula:**

```
DI(n, t) = Φ(n,t) × [1 + α · Ψ(n,t)] × [1 + β · Ω(n,t)]

Rescaled 0–100 via min-max normalization across the full historical sample.
```

**Parameters**: `α` and `β` are empirically calibrated via backtesting (Section 6). Theoretical constraints on both parameters are imposed before calibration (Section 6.1).

**Theoretical logic of the hierarchy**:
- Phase position gates the index — morphology is Spengler's primary causal frame (Spengler 1918, *Decline of the West*, Vol. I)
- Structural pressure amplifies phase vulnerability — same phase is more dangerous inside an extractive world-system (Wallerstein 1974, *The Modern World-System I*)
- Momentum modifies urgency — same structural stress is more alarming when accelerating (Downey et al. 2016, *PNAS* 113(35))

---

## 3. Layer 1 — Spengler Phase Position (Φ)

**Scale**: 0.0 (early Culture) → 1.0 (Ossification)

**Output**: Weighted sum of normalized sub-dimensions → Φ ∈ [0, 1]

| Dimension | Dataset | Weight | Direction | Theoretical Reference |
|-----------|---------|--------|-----------|----------------------|
| Financialization | Maddison GDP + World Bank GFDD | **25%** | ↑ = higher Φ | Spengler (1918) — "money replaces blood"; financial dominance is the definitive civilization marker |
| Urbanization Level | HYDE 3.2 | **20%** | ↑ = higher Φ | Spengler (1918) — megalopolis formation is the civilizational hallmark; Inayatullah (2013) — urbanization as phase gate |
| Political Form | Polity5 + V-Dem | **20%** | Caesarism ↑ = higher Φ | Spengler (1918) — political trajectory ends in Caesarism; institutional pluralism = earlier phase |
| Culture vs. Civilization proxy | V-Dem + Polity5 composite | **15%** | Civilization markers ↑ = higher Φ | Bonta (2014) *Semiotica* 201 — phase trajectory operationalization |
| Mass Society / Democratization | V-Dem polyarchy index | **10%** | ↑ = higher Φ | Spengler (1918) — mass politics is a civilization-phase phenomenon; Culture is aristocratic |
| Lifecycle Stage | Maddison + Polity5 + Patents | **10%** | Later stage = higher Φ | Inayatullah (2013) — age + growth deceleration + institutional rigidity composite |

**Artistic Creativity** (3/10 data quality): enters as Phase 2 refinement. Declining creativity is a Spenglerian signal but fragmentary data pre-1900 introduces noise. Phase 1 proxy: patents per capita 10yr rolling average (level, not derivative — rate of change enters Layer 3 as ΔCreativity/Δt).

**Normalization**: Each dimension normalized 0–1 within the full sample range before weighting. Dimensions with data quality < 5/10 flagged with uncertainty band (±1 quality tier in sensitivity analysis).

---

## 4. Layer 2 — Wallerstein Structural Pressure (Ψ)

**Scale**: 0.0 (maximum structural advantage) → 1.0 (maximum structural pressure)

**Output**: Weighted sum of normalized sub-dimensions → Ψ ∈ [0, 1]

**Key property**: Ψ is raw structural pressure before institutional buffering. Scout 3 confirmed that same structural position produces different outcomes depending on state capacity (Korea vs. Argentina anomaly). Institutional moderation is captured in calibration, not hardcoded into Ψ. The data reveals it.

| Dimension | Dataset | Weight | Direction | Theoretical Reference |
|-----------|---------|--------|-----------|----------------------|
| Hegemonic Cycle Position | CINC + Maddison | **25%** | Declining hegemon ↑ = higher Ψ | Wallerstein (1984) *The Politics of the World-Economy*; Kwon (2011) *Sociological Perspectives* 54(4) |
| Terms of Trade | COW Trade | **20%** | Deteriorating ↑ = higher Ψ | Hickel et al. (2024) *Nature Communications* 15:5965; Ricci (2022) *Environment and Planning A* 54(7) |
| Network Centrality in Trade | COW Trade (eigenvector, calculated) | **20%** | Declining centrality ↑ = higher Ψ | Chase-Dunn & Hall (2011) *Journal of Archaeological Research* — network position dynamics |
| Zone Classification | COW Trade + Penn WT (derived) | **15%** | Periphery ↑ = higher Ψ | Wallerstein (1974) — structural position as primary determinant |
| Surplus Extraction Rate | COW Trade + UNCTAD (derived) | **10%** | Net exporter of value ↑ = higher Ψ | Ricci (2022); Hickel et al. (2024) — value flow direction |
| Interstate System Cohesion | COW Alliance + MID | **10%** | Declining cohesion ↑ = higher Ψ | Wallerstein (1984) — system-level fragmentation increases pressure on all nodes |

**Two dimensions deferred to Phase 2** (data quality insufficient):
- Monopoly Rents (4/10): enters when patent concentration + OECD market data available
- Semi-Peripheral Stabilization (5/10): too derived for reliable Phase 1; Capital Intensity Ratio (Penn WT) used as proxy

---

## 5. Layer 3 — Cybernetic Momentum (Ω)

**Scale**: −1.0 (rapid improvement) → 0 (stable) → +1.0 (rapid deterioration)

**Output**: Weighted sum of standardized first derivatives → Ω ∈ [−1, +1]

**Window**: 10-year rolling window. Rationale: shortest interval with adequate data quality across all five dimensions for the 1850–1950 epoch. 5-year windows introduce excessive noise pre-1920; 20-year windows are too slow to detect pre-collapse acceleration.

| Derivative | Source Dimension | Weight | Direction | Theoretical Reference |
|-----------|-----------------|--------|-----------|----------------------|
| ΔFinancialization / Δt | GFDD + Maddison | **25%** | Accelerating ↑ = higher Ω | Kus (2012) *Sociological Perspectives* — financialization-inequality nexus; crowding-out of productive investment |
| ΔHegemonic power share / Δt | CINC + Maddison | **25%** | Declining ↑ = higher Ω | Kwon (2011) *Sociological Perspectives* 54(4) — hegemonic decline measurement |
| ΔNetwork centrality / Δt | COW Trade | **20%** | Declining ↑ = higher Ω | Chase-Dunn & Hall (2011) — network position dynamics |
| ΔCreativity proxy / Δt | Patents per capita | **15%** | Declining ↑ = higher Ω | Spengler (1918) — creativity as culture-phase marker; Bonta (2014) *Semiotica* — phase trajectory |
| ΔTerms of Trade / Δt | COW Trade | **15%** | Deteriorating ↑ = higher Ω | Hickel et al. (2024) *Nature Communications*; Ricci (2022) *Environment and Planning A* |

**Critical slowing down deferred to Phase 2**: Scout 1 confirmed CSD statistics (rising autocorrelation, variance) have high false positive rates on social data (Downey et al. 2016, *PNAS* 113(35)). Reserved as optional overlay signal once core index is calibrated. The EU-GNN-Risk-Monitor's anomaly detection framing — identifying systems at peak stress — is the conceptual reference for this Phase 2 layer.

---

## 6. The 3 Novel Measurements

Each gets a **Phase 1 proxy** (tractable, data-available) and a **Phase 2 full design** (replaces proxy without changing index structure). Consistent with the Innovation Panel methodology: flag quality, report confidence tier, never silently omit.

### 6.1 Soul-Form / Prime Symbol

*Theoretical anchor*: Spengler (1918) *Decline of the West* Vol. I, Ch. 2 — prime symbol as the spatial intuition underlying a culture's entire expression (Faustian = infinite space; Apollonian = bounded body; Magian = cavern/world-cave). Bonta (2014) *Semiotica* 201 — Peircean typology provides categorical framework.

| | Phase 1 Proxy | Phase 2 Full Design |
|-|--------------|---------------------|
| Method | Ordinal expert classification (1–4: Mythic → Dogmatic → Rationalist → Nihilist) from historiographic consensus (Toynbee, Sorokin, Spengler) | LDA topic modeling on digitized texts (Google Books Ngram corpus, 1800–2000) + DNN image embeddings of architectural output |
| Output | Ordinal phase indicator (1–4); contributes to Layer 1 baseline | Continuous embedding (0–1 per soul-form category); replaces ordinal without structural change |
| Uncertainty | Flagged HIGH — expert judgment, not measured | Flagged MEDIUM — model uncertainty propagated through index |

### 6.2 Artistic-Intellectual Creativity

*Theoretical anchor*: Spengler (1918) — creativity peaks in Culture phase, declines in Civilization. Kus (2012) *Sociological Perspectives* — financialization crowds out productive and creative investment. Bonta (2015) *Semiotica* 207 — phase trajectory predicts creative contraction.

| | Phase 1 Proxy | Phase 2 Full Design |
|-|--------------|---------------------|
| Method | Composite of 3 normalized indicators, equal-weighted — mirroring the Innovation Panel's Location Quotient composite logic applied to innovation signals | GNN-learned embedding from patent citation networks + publication networks + artistic output indices |
| Indicators | (1) Patents per capita, 10yr rolling avg (USPTO/WIPO, 1850+); (2) Scientific publications per capita (1900+); (3) Net migration of educated population where available | All Phase 1 indicators + citation network topology + art historical production index |
| Normalization | Z-score within epoch; capped at ±3σ | GNN node embedding; supervised on known creative peaks (Renaissance, Golden Age Dutch, 1960s–80s US) |
| Output | Creativity index (0–1); inverted for Downfall contribution (declining = higher Ω) | Unified creativity embedding; same inversion |
| Uncertainty | Flagged MEDIUM — proxies fragmentary pre-1900 | Flagged LOW post-1900; MEDIUM pre-1900 |

### 6.3 Commodity Chain Position

*Theoretical anchor*: Wallerstein (1974) *The Modern World-System I* — periphery locked in primary commodity extraction; semi-periphery in intermediate processing; core in high-value manufacturing and services. Hickel et al. (2024) *Nature Communications* — embodied labour flows confirm positional lock-in.

| | Phase 1 Proxy | Phase 2 Full Design |
|-|--------------|---------------------|
| Method | Sectoral export share classification — same NACE-style sectoral LQ logic as Innovation Panel, applied to historical trade categories from COW Trade | I-O matrix reconstruction from national accounts (1960–1990); Product Complexity Index (Hausmann et al. 2009, *Journal of Economic Growth*) from 1962+ |
| Data | COW Trade sectoral breakdown: primary commodities / semi-manufactures / manufactures / services (1870+) | OECD TiVA (1995+); UN Comtrade (1962+); reconstructed I-O matrices |
| Output | Ordinal position (0–3: raw extraction → processing → manufacturing → services/knowledge); contributes to Layer 2 Ψ | Continuous PCI-based score (0–1); replaces ordinal without structural change |
| Uncertainty | Flagged HIGH pre-1900 — trade category data sparse | Flagged MEDIUM 1962+; HIGH pre-1962 |

---

## 7. Calibration Procedure

### 7.1 Theoretical Constraints (Imposed Before Calibration)

| Constraint | Justification |
|-----------|---------------|
| `α > 0` | Structural pressure must amplify phase vulnerability, never suppress it — Wallerstein's core claim (1974) |
| `β > 0` | Deteriorating momentum must increase urgency — cybernetic directionality (Downey et al. 2016) |
| `α ≤ 1` | Structural pressure is amplifier, not primary signal — phase position dominates per Spengler (1918) |
| `β ≤ α` | Momentum modifies structural stress; structural stress modifies phase — hierarchy preserved |

### 7.2 Backtesting Events

| Event | Target behavior |
|-------|----------------|
| 1848 European Revolutions | DI peaks for France, Austria, Prussia in 1840–1847; declines post-1850 |
| 1914 WWI onset | DI peaks for Austria-Hungary, Ottoman Empire in 1905–1913; Germanic powers elevated |
| 1929 Great Depression | DI peaks for US, UK in 1924–1928; peripheral nations already elevated prior |

### 7.3 Calibration Method

Grid search over `α ∈ [0.1, 1.0]` and `β ∈ [0.1, α]` in 0.1 increments. Select parameters minimizing RMSE between DI peak timing and known transition dates across all three events.

**What "good" calibration looks like** — following the Innovation Panel's discipline of effect sizes over raw significance:
- DI peaks 10–20 years *before* collapse events, not at the moment of collapse
- Effect size (Cohen's d) between pre-collapse decade and stable decades ≥ 0.5
- Ranking coherence: nations widely recognized as vulnerable should score higher than stable comparators in the same epoch
- Sensitivity analysis: report how scores change across full plausible parameter range; no single parameter choice should dominate the results

---

## 8. Output Format and Dashboard Presentation

**Scale**: 0–100 (min-max normalized across the full historical sample)

**Interpretive bands** (illustrative; final values from calibration):

| DI Score | Label | Description |
|----------|-------|-------------|
| 0–20 | Stable | Early culture phase; minimal structural pressure; stable or improving momentum |
| 20–40 | Elevated | Mid-culture phase or moderate structural pressure; monitoring warranted |
| 40–60 | Stressed | Late culture / early civilization phase with structural pressure accumulating |
| 60–80 | Critical | Civilization phase with significant structural pressure and negative momentum |
| 80–100 | Terminal | Full civilization-to-ossification configuration; rapid deterioration detected |

**Dashboard views**:
1. **Timeline chart**: DI score per nation, 1850–2020; known collapse events marked as vertical reference lines
2. **Decomposition panel**: At any selected year, show Φ / Ψ / Ω sub-scores as stacked contribution bars — transparent by design
3. **Comparative ranking**: Nations ranked by DI for selected epoch; confidence intervals displayed
4. **Uncertainty layer**: Toggle to show quality-tier confidence bands; explicitly flags Phase 1 proxies for novel measurements

**Mandatory dashboard tooltip** (on every DI score display):
> "The Downfall Index measures structural vulnerability and momentum, not collapse prediction. High scores indicate configurations historically associated with systemic stress — not deterministic outcomes."

---

## 9. Epoch Data Quality Policy

Consistent with Scout 2 findings:

| Epoch | Quality | DI Policy |
|-------|---------|-----------|
| Pre-1500 CE | VERY LOW | DI not computed; narrative layer only |
| 1500–1800 | MEDIUM | DI computed with wide confidence intervals (±30–40%); flagged prominently |
| 1800–1950 | HIGH | Primary MVP epoch; ±10–15% CI; all 17 base dimensions available |
| 1950–2020 | VERY HIGH | Full model; <5% typical error; all novel Phase 2 metrics included when available |

---

## 10. Publication Strategy

**Primary venue target**: *Journal of World-Systems Research* (Wallerstein community) or *Complexity* (interdisciplinary systems)

**Paper structure**:
1. Theoretical motivation — the gap (no unified framework; Scout 1 confirmed zero published work)
2. Index design — Sections 3–5 above; full formula derivation
3. Novel measurements — Section 6; methodological contribution
4. Calibration — Section 7; backtesting as validation
5. Results — DI trajectories for 15 nations, 1850–2020; anomaly analysis
6. Discussion — what anomalies reveal (Scout 3 catalog); conditional loop activation; limits of structural determinism

**Standalone publication potential** (separate short papers):
- Civilizational Entropy Index (absorbed into Φ as sub-component; publishable separately)
- GNN Creativity Metric (Phase 2; methodology paper)
- Hegemonic Stability Index (absorbed into Ψ; publishable separately)

---

## 11. Methodological Reference Points

The following prior projects inform methodology (not data):

- **EU-Innovation-Panel**: Composite scoring discipline (LQ-style relative positioning, external validation benchmark without feature contamination, effect sizes over raw significance, medallion architecture for data integrity)
- **EU-GNN-Risk-Monitor**: Anomaly/peak detection framing (identifying systems at maximum stress — structurally analogous to Layer 3's momentum detection); GNN anomaly scores as conceptual reference for Phase 2 CSD layer

---

## 12. Constraints

- **Solo development**: orchestration via agent fleet; implementation in stages matching Phase 1 → 2 → 3 roadmap
- **No causal overclaiming**: all language uses "associated with," "correlates with," "historically preceded" — never "causes collapse" from DI alone
- **Borrowed data only for Phase 1**: all eight core datasets are free, peer-reviewed, and immediately accessible
- **Novel measurements deferred**: Phase 1 runs on 17 base dimensions + Phase 1 proxies for the three novel measurements; Phase 2 replaces proxies without structural change
- **Zone-conditional weighting decision deferred**: whether to apply zone-specific weights is an empirical question answered after calibration, not a design assumption
