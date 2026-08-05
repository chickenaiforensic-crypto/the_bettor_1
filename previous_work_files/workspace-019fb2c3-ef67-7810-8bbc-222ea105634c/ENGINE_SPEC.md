# ENGINE SPECIFICATION — Pitch Rating v2.0

**Companion to `METHODOLOGY.md`. Version 1.0 · 2026-07-30**
Purpose: a cold-start rebuild document. Every constant, every layer, every ordering decision, traced to the running code and the evidence that set it.

Read `METHODOLOGY.md` for *why we work this way*. Read this for *what the engine does*.

---

## PART A — LAYER ARCHITECTURE

The engine is **five layers in strict order of significance**. Each layer may only consume outputs of layers above it. Nothing below Layer 1 may alter Layer 1's inputs.

```
LAYER 0   DATA           completed matches only
   ↓
LAYER 1   RATINGS        Dixon-Coles att / def / home advantage      ← the engine
   ↓
LAYER 2   DISTRIBUTION   Poisson scoreline grid + DC correction
   ↓
LAYER 3   ADJUSTMENT     star draw correction (only layer that edits probability)
   ↓
LAYER 4   CLASSIFICATION tiers, points, stars, expected scoreline
   ↓
LAYER 5   SELECTION      consensus confidence labels (edits nothing)
```

**Order of significance, highest first:**

| Rank | Component | Weight in outcome | Can it change a probability? |
|---|---|---|---|
| 1 | Dixon-Coles ratings | dominant — sets λ | **yes, it *is* the prediction** |
| 2 | League home advantage | large — 1.20×–1.36× goal multiplier | yes, inside λ |
| 3 | Poisson + DC ρ | shapes the whole distribution | yes |
| 4 | Star draw correction | ±0.02 absolute on P(draw) | yes, capped |
| 5 | Per-team home extra | tiny — max ±0.006 log-goals | yes, inside λ |
| 6 | Tier / points / stars | zero — labels | **no** |
| 7 | Consensus confidence | zero — labels | **no** |

**Rule:** significance is ordered by *evidence strength*, not intuition. Layer 1 carries +5.6% Brier. Layer 3 carries +0.047%. Layers 4–5 carry zero and are display only. A component's rank equals its measured contribution.

---

## PART B — LAYER 1: THE RATING ENGINE

### B1. Model form (Dixon-Coles bivariate Poisson)

```
λ_home = exp( μ[league] + att[home] − def[away] + hfa[league] + home_extra[home] )
λ_away = exp( μ[league] + att[away] − def[home] )

clamped: 0.05 ≤ λ ≤ 6.0
```

**Sign convention (critical, and a past source of error):** `def` is *defensive quality*. **Higher `def` = fewer goals conceded = better defence.** It is subtracted from the opponent's attack. Getting this backwards inverts every rating.

### B2. Parameters

| Parameter | Meaning | Source |
|---|---|---|
| `att[team]` | attacking strength, log scale | fitted |
| `def[team]` | defensive strength, log scale | fitted |
| `μ[league]` | league scoring baseline | fitted per league |
| `hfa[league]` | **league home advantage** | fitted per league |
| `home_extra[team]` | club's own home effect beyond league | fitted, clamped ±0.25 |
| `ρ = −0.06` | Dixon-Coles low-score correction | fixed |

### B3. Fitting procedure (online gradient, strict date order)

```
for each match in chronological order:
    predict λ_home, λ_away          ← prediction happens BEFORE the update
    e_h = goals_home − λ_home
    e_a = goals_away − λ_away

    k_h = LR × (1.6 if team seen < 8 matches else 1.0)     # new teams adapt faster
    k_a = LR × (1.6 if team seen < 8 matches else 1.0)

    att[home] += k_h × e_h × 0.5
    def[away] -= k_a × e_h × 0.5
    att[away] += k_a × e_a × 0.5
    def[home] -= k_h × e_a × 0.5

    hfa[league]      += HFA_LR × (e_h − e_a) × 0.02
    home_extra[home] += HFA_LR × (e_h − e_a) × 0.010
    home_extra[home] *= 0.999                              # decay toward zero
    μ[league]        += 0.004 × (e_h + e_a) / 2

    att[t] *= (1 − DECAY);  def[t] *= (1 − DECAY)   for both teams
    clamp hfa to [0.05, 0.55];  home_extra to [−0.25, 0.25]
```

### B4. Constants — and why each has its value

| Constant | Value | Justification |
|---|---|---|
| `LR` learning rate | **0.055** | balances responsiveness against stability across 153k matches |
| `DECAY` | **0.0022** per match | form fades; without it 2003 ratings persist into 2026 |
| `HFA_LR` | **0.010** | home advantage moves slowly; it is a structural property |
| new-team multiplier | **1.6×**, first 8 matches | promoted sides reach true level fast instead of dragging a stale prior |
| `home_extra` decay | **0.999** per match | prevents a club accumulating a permanent unearned home bonus |
| min matches to rate | **6** | below this the rating is noise |
| `ρ` | **−0.06** | corrects Poisson's known under-prediction of 0-0 and 1-1 |
| λ clamp | **[0.05, 6.0]** | numerical guard; prevents exp() blow-up on extreme ratings |

**These constants must match between the Python trainer (`data/rating.py`) and the browser update engine.** Verified identical: max difference `0.00e+00` across 7 quantities.

### B5. Measured home advantage (output, not assumption)

| League | Multiplier | | League | Multiplier |
|---|---|---|---|---|
| Spain Segunda | **1.36×** | | Portugal | 1.27× |
| Greece | 1.34× | | Scotland | 1.26× |
| Spain La Liga | 1.33× | | Germany Bundesliga | 1.26× |
| Netherlands | 1.30× | | England Championship | 1.25× |
| Italy Serie B | 1.29× | | England Premier League | 1.24× |
| France Ligue 2 | 1.28× | | England League One | 1.23× |
| Turkey | 1.28× | | Italy Serie A | 1.22× |
| Belgium / France L1 | 1.27× | | **England League Two** | **1.20×** |

A single global constant — as the retired app used — is wrong for every league simultaneously.

Per-team effects are **real but tiny**: Bayern, Atlético, Man City, Liverpool, Dortmund top out at **+0.006** log-goals. Folklore overstates fortress effects; the model correctly declines to inflate them.

---

## PART C — LAYER 2: DISTRIBUTION

### C1. Scoreline grid

```
P(i,j) = Poisson(i; λ_home) × Poisson(j; λ_away) × τ(i,j)     for i,j in 0..10

τ(0,0) = 1 − λ_h·λ_a·ρ
τ(0,1) = 1 + λ_h·ρ
τ(1,0) = 1 + λ_a·ρ
τ(1,1) = 1 − ρ
τ(i,j) = 1        otherwise

normalise so Σ P(i,j) = 1
```

`H = Σ P(i>j)`, `D = Σ P(i=j)`, `A = Σ P(i<j)`

### C2. Two grids, deliberately

| Grid | Used for | Why |
|---|---|---|
| `scoreGrid(λh, λa)` | **1X2**, expected scoreline | unmodified — best estimate of who wins |
| `goalsGrid(λh, λa)` | **over/under, handicap** | totals **shrunk toward the league mean** |

```
goalsGrid:  total  = λh + λa
            shrunk = GMU + k·(total − GMU)      k = 0.5,  GMU = 2.6186
            scale both λ by (shrunk / total)
```

**Why shrinkage exists — this is not arbitrary.** Before it, over/under markets were badly miscalibrated because the model spread predicted totals too widely:

| Market | Before shrink | After (k=0.5) |
|---|---|---|
| Over 1.5 | ±15.4% | **±1.8%** |
| Over 2.5 | ±10.3% | **±2.7%** |
| Over 3.5 | ±12.7% | ±3.3% |
| BTTS | ±11.2% | ±6.0% → **withheld** |

`k = 0.5` was fitted on 70% of data and tested on the held-out 30%. **The model predicts *who wins* better than it predicts *how many goals*** — the two grids encode that honestly instead of pretending one number serves both.

---

## PART D — LAYER 3: STAR DRAW CORRECTION

### D1. Star classification (user specification)

```
metric  = (3·won + drawn) / played          ← games won/drawn against games played
qualify = played ≥ 5                        ← user-set minimum
shrink  = (metric·played + league_mean·6) / (played + 6)
stars   = quintile rank 1..5 within league, on the shrunk metric
hyst    = 0.05 percentile buffer — must clear a boundary by this margin to move level
```

**Why each element:**

| Element | Reason | Evidence |
|---|---|---|
| shrinkage, weight 6 | a 5-game record must not be trusted like a 30-game one | — |
| hysteresis 0.05 | without it 21.0% of teams changed star level every week | churn → **8.7%** |
| quintiles within league | a 5★ in Greece ≠ a 5★ in England; ranks are league-relative only | cutoff spread 0.410–1.027 |
| min 5 games | user directive | — |

**Rejected earlier construction:** `att + def` composite. It misranked Sunderland (7th in the table) as 1★ and Nott'm Forest (16th) as 4★, because `def` had wider spread than `att` and dominated the sum. Replaced in v2.0.

### D2. What stars measure

Same-star fixtures draw **28.1%** vs **26.4%** for different-star (+1.68pt, CIs disjoint). Monotonic across the range:

| \|star gap\| | Draw rate |
|---|---|
| 0 | **28.1%** |
| 1 | 28.1% |
| 2 | 26.3% |
| 3 | 24.9% |
| 4 | **21.9%** |

### D3. The correction

```
tier  = league division tier (1 = top flight, 2 = second, 3 = third/fourth)
tgt   = draw_table[tier | star_gap]        (27 fitted cells; falls back to draw_base[tier])
w     = 0.2 (tier 1) | 0.5 (tier 2) | 0.5 (tier 3)

D2 = (1−w)·D + w·tgt
D2 = clamp(D2, D − 0.02, D + 0.02)          ← hard cap

rem = 1 − D2
H  = rem · H/(H+A)                          ← PROPORTIONAL SPLIT
A  = rem · A/(H+A)
D  = D2
renormalise
```

### D4. Why per-tier, and why proportional — both were errors first

**Per-tier:** a single global table was wrong in *opposite directions* — over-predicting top-flight draws by up to 3.5pt while under-predicting second-tier draws by 2.5pt, cancelling into an apparently useless average. Top flights are ~45% more stratified (PPG sd 0.448 vs 0.309), so one star covers more real ability there.

**Proportional split (rule M4):** originally the away side absorbed the entire draw adjustment while P(home) never moved (measured: `dD 0.0106, dA 0.0106, dH 0.0000`). That made a real gain read as net-negative.

| Approach | Full 1X2 | p |
|---|---|---|
| Away absorbs all | −0.009% | 0.58 |
| **Proportional** | **+0.047%** | **0.0000** |

**Verified live:** `dH=+0.00603, dD=−0.00891, dA=+0.00288` — both sides absorb.

### D5. Measured effect (59,615 out-of-sample, rolling-origin, paired)

| Metric | Change | p |
|---|---|---|
| Home Brier | +0.049% | 0.0001 |
| Draw Brier | +0.084% | 0.0001 |
| Away Brier | +0.008% | 0.41 (neutral) |
| **Full 1X2** | **+0.047%** | **0.0000** |
| Log loss | +0.041% | 0.0002 |

By division: tier 2 **+0.096%** (p=0.0001), tier 3 **+0.092%** (p=0.0014), top flight +0.003% (neutral, no harm).

---

## PART E — LAYER 4: CLASSIFICATION

### E1. Tier table — labels only, zero probability impact

| Tier | Points (=round(100·H)) | Observed win | Draw | Loss | PPG | n |
|---|---|---|---|---|---|---|
| **A+ Fortress** | 70+ | **78.5%** | 14.1% | 7.4% | 2.50 | 7,718 |
| **A Strong** | 60–69 | 64.2% | 21.6% | 14.2% | 2.14 | 11,799 |
| **B Lean** | 52–59 | 54.7% | 26.0% | 19.3% | 1.90 | 20,335 |
| **C Marginal** | 45–51 | 47.5% | 28.3% | 24.2% | 1.71 | 28,246 |
| **D Coin-flip** | 35–44 | 40.8% | 29.9% | 29.3% | 1.52 | 44,718 |
| **E Avoid** | 0–34 | 28.2% | 26.8% | 45.0% | 1.11 | 37,544 |

Tiers are cut on **calibrated probability**, so "70 points" means the home side wins ~70% of the time — validated in every 10-point bucket. Max calibration error **1.66%** (covid excluded).

### E2. Expected scoreline

Highest-probability cell of the **uncorrected** grid, reported with its true frequency (~13%). Correct-score is inherently low-confidence; showing the frequency prevents it reading as a forecast.

---

## PART F — LAYER 5: SELECTION (edits nothing)

### F1. Consensus

```
HvH = home's home GD/game − away's home GD/game     "who is better at home"
AvA = home's away GD/game − away's away GD/game     "who is better away"

CONSENSUS    = (HvH + AvA) / 2        strength    (r = +0.91 with model — redundant)
DISAGREEMENT = |HvH − AvA|            reliability (r = −0.09 — independent)

requires ≥ 4 home and ≥ 4 away matches for both sides, else null
```

### F2. Labels (applied to tier A/A+ only)

| Condition | Label | Observed |
|---|---|---|
| consensus > 1.5 | **STRONG** | **78.6%** home wins |
| consensus > 1.0 | **CONFIRMED** | 74.8% |
| consensus < 0 | **CONFLICTED** | model and venue records disagree |
| \|consensus\| < 0.2 and disagreement < 0.5 | **DRAW-LEAN** | 31.8% draw |

Baseline for comparison: the model's own top-10% picks win **73.0%**. Consensus > 1.5 lifts that to **78.6%** — CIs disjoint.

**Why selection-only:** as a probability input it measured +0.0016%, p=0.64 — nothing. As a filter it adds 5.6pt. Different roles, different evidence. Enforced by test: the confidence block never assigns H, D or A.

**Note:** it is the *magnitude* of consensus that works, not agreement between lenses. Filtering on agreement alone scored −0.9%.

---

## PART G — OUTPUT PROVENANCE

Which outputs use corrected vs uncorrected numbers. **This is deliberate and was verified, not assumed.**

| Output | Source | Star-corrected? |
|---|---|---|
| H / D / A | scoreGrid → star correction | **yes** |
| Points, tier | corrected H | **yes** |
| Double chance, DNB | corrected H/D/A | **yes** |
| Over/under 1.5, 2.5, 3.5 | **goalsGrid** (shrunk) | no |
| Home −1 handicap | goalsGrid | no |
| Expected scoreline, top 5 | raw scoreGrid | no |
| Stars, consensus, labels | records | n/a |

**Why the split is safe — measured across all 9,506 fixtures:**
- Likeliest scoreline contradicts the 1X2 lean: **0 cases (0.00%)**
- DNB inconsistent with corrected H/A: **0**
- Over/under non-monotone: **0**
- Max divergence between corrected D and grid D: **0.020** (exactly the cap), mean 0.008

The star correction is a **draw-rate refinement**, not a goals-model change. Propagating it into goals markets would corrupt their independently-validated calibration (O2.5 at ±2.7%). Keeping them separate is correct.

---

## PART H — REFUSAL PATHS

The engine must decline rather than guess. Every path verified live.

| Condition | Behaviour |
|---|---|
| Team not in rated set | `{error: "Unknown team or league"}` |
| Fewer than 5 games | stars = `null`, no draw correction |
| Fewer than 4 home or away games | consensus = `null`, no confidence label |
| Home team never hosted in that league | **hard error** — likely flip |
| Sides evenly matched | warns a flip would be **silent and undetectable** |
| Venue unconfirmed | **save button disabled** |
| BTTS | withheld entirely — ±6.0% calibration |

---

## PART I — COLD-START REBUILD ORDER

Rebuild in this sequence. Each step is validated before the next begins.

1. **Ingest** with D2 validation. Confirm 0 result mismatches, 0 duplicates, league-season counts exact.
2. **Fit Layer 1** online, date order, causality enforced structurally. Target: Brier +5.6% vs base rate, calibration ≤1.7%.
3. **Build Layer 2.** Fit the goals shrink `k` on a train split, verify on held-out. Target: O2.5 ≤3%.
4. **Gate the markets.** Ship ≤3%, flag 3–5%, withhold above. BTTS fails.
5. **Build stars** to the D1 spec. Verify: no misrankings against the real table, churn <10%, monotone in PPG.
6. **Fit draw tables** per tier on training data only. Apply with proportional split and the 0.02 cap.
7. **Validate Layer 3** with paired tests, rolling origin, all five metrics. Ship only if nothing degrades.
8. **Add Layer 5** last. Assert it changes no probability.
9. **Run the compliance suite** — 31 checks — plus 110 functional tests.

**If a step fails its target, stop.** Do not proceed to the next layer with a broken one beneath it.

---

## PART J — WHAT THIS ENGINE DOES NOT DO

Stated plainly so no false capability is implied.

- **No injuries, lineups, suspensions, transfers, or fixture congestion.** Results only. Deferred by user directive.
- **No cross-border rating.** National league graphs are disconnected; a Polish and a Danish club cannot be compared by Layer 1. The chain system exists for this and is **standby, analysis-only**.
- **No competition awareness.** Every fixture is treated as domestic league. Cup, European and neutral-venue handling is **approved but not yet built** (open item 4).
- **No profitability claim.** The engine is calibrated to reality. Calibrated and profitable are different claims; only the first is made.
- **No market data in any role** — permanently, by user directive P1.

---

*Companion document to `METHODOLOGY.md`. Amend together; record every amendment.*
