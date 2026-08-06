# 10 — Cross-League Pivot + Live Per-Team Rating + Current Performance Weighting (Owner Clarification 2026-08-05)

**Owner statement (verbatim, clarified):**
> For cross leagues we use that standard evaluation per team-league then per the results obtain we bump it up/calibrate it to create a per-league rating that pivots one league X points above another league - so that our live computations always produces accurate / real world results
> We also have a per team rating computed through an evaluation system and based on performance it goes up or goes down that way the app is alive when it takes in results
> Also we have the current performance - so if a team comes into a league very efficient than it did before its current performance acquired through a minimum number of play offs evaluation provides a weighted inclusion to its computation for predictions

This document formalises those three mechanisms into the locked singular engine, preserving zero market (P1) and approval by test run (T1-T8).

---

## 1. Cross-League: Standard Evaluation Per Team-League → Per-League Pivot Points

**What owner means in smooth English:**

Every team is first rated inside its own league. An Arsenal rating only knows Premier League results, a Sparta Prague rating only knows Czech league results. They are not forced onto the same scale at birth.

Then we look at real results where leagues met — UEFA Champions League, Europa, Conference + qualifiers (connector pack #17, 2000-2500 rows). Those are the truth.

If English teams consistently beat Czech teams by 0.4 goals more than our per-league ratings predicted, we bump the English league pivot up and the Czech pivot down until the predictions match the real cross-league results.

After that, any cross-league fixture (e.g., Arsenal vs Dynamo Moscow) is computed on one common scale: team rating + its league pivot.

**Formalisation (implements Masterplan §6 fit-to-results loop with owner wording):**

- Let `att[t], def[t]` = per-team attack/defence fitted online within its league (L1).
- Let `s[L]` = league pivot points (log-goals), init 0 for all leagues.
- Common-scale strength: `S[t] = att[t] - def[t] + s[league(t)]`
- For cross-league match home=team A (league LA), away=team B (league LB):
  ```
  λ_home = exp( μ + S[A] - (-def? keep def separation) + hfa[LA] + home_extra[A] + (s[LA]-s[LB])/2 )
  Actually simplest: use standard λ formula but with att/def shifted by s:
  att_common[A] = att[A] + s[LA]
  def_common[A] = def[A] - s[LA] ??? Need consistent — we define strength as att-def.
  Implementation chosen (additive in log-goals, preserves history):
  λ_home = exp( μ[common] + (att[A]+s[LA]) - (def[B]+s[LB]) + hfa + home_extra[A] )
  λ_away = exp( μ[common] + (att[B]+s[LB]) - (def[A]+s[LA]) )
  ```
  Where μ[common] = average of μ[LA], μ[LB] or league-neutral base 0.45 — to be decided by harness.

- **Fit loop (the "bump up / calibrate" owner describes):**
  ```
  1. Connector rows = all UEFA ties where team A from league LA, team B from league LB, result GD = hg-ag.
  2. Predict GD_pred = E[goals_home - goals_away] from current λ_home, λ_away (from Poisson grids mean λ_home - λ_away).
  3. For each league L, bias(L) = mean( GD_pred - GD_actual ) over all connector ties involving L.
     Positive bias = we predicted L too high → should lower s[L].
     Negative bias = we predicted L too low → should bump up.
  4. Update: s[L] ← s[L] - step * bias(L)   step 0.05–0.1
  5. Re-predict, re-measure bias, iterate 20–50 times until |bias|<0.02 goals.
  6. Validation: fit s[L] on 2021-22..2024-25 Euro, test on 2025-26 Euro LAST OMITTED window (untouched), 
     weighted scale vs frozen 1.00 scale (s[L]=0 baseline). Adopt ONLY if weighted wins Brier/RMSE/direction paired.
  ```

- **What "X points below/above" means:** After convergence, s[ENG]=+0.12, s[CZE]=-0.08 means Premier League pivots 0.20 log-goals (~1.22× goal multiplier) above Czech First League on common scale. This is the per-league rating.

- **Live:** s[L] lives in store artifact `dc-fitted-league-pivot` with n/window/Brier/date provenance M3. Auto re-validated on any connector data change (M1). If no validated pivot → plain label "no calibrated bridge" + evidence chain view (P3 honesty).

**Why this is accurate/real-world:** No arbitrary UEFA coefficient — pivots come from direct results only (P1/P2). Our live computations always produce real-world because bias is measured against actual cross-league scores, not opinion.

---

## 2. Per-Team Rating Live — App Is Alive When It Takes Results

**Owner: per team rating computed through evaluation system and based on performance it goes up or down.**

This is L1 Dixon-Coles online fit, already verified exact:

- Each completed result updates four numbers for the two teams involved:
  ```
  att[home] += LR * (hg - λ_home) * 0.5 * (1.6 if seen<8 else 1.0)
  def[away] -= LR * (hg - λ_home) * 0.5 * ...
  att[away] += LR * (ag - λ_away) * 0.5
  def[home] -= LR * (hg - λ_home) * ...
  hfa[league] += HFA_LR*(eh-ea)*0.02
  home_extra[home] += HFA_LR*(eh-ea)*0.010  *=0.999 decay
  μ[league] +=0.004*(eh+ea)/2
  att/def *= (1-DECAY) 0.0022 per match (shrink to mean)
  hfa clamp [0.05,0.55] home_extra ±0.25 λ clamp [0.05,6.0]
  ```
- Seen counter increments, min 6 matches before team can be rated (P3 refusal else).
- So rating goes up after wins above expectation (hg > λ), down after under-performance. App is alive — every new row changes future predictions, no static table.

- **Storage:** att/def/hfa/home_extra/mu live in `dc-fitted-model` artifact, derived from store rows on every masked replay (M5). Not carried precompute (A-01).

- **Display (human-friendly):** Not raw numbers — show trend icon ↑ stable → slight ↑ etc. with provenance small-print: "Live rating from 960 matches, last update 2026-08-02, Brier 0.5675 vs base 0.6465".

---

## 3. Current Performance — Weighted Inclusion If Team Hot

**Owner: if a team comes into a league very efficient than it did before its current performance acquired through minimum number of playoffs evaluation provides weighted inclusion to its computation.**

Interpretation: long-term base rating (≥2 seasons) vs short-term current form (last few playoffs/high-stakes or recent matches). If team is suddenly much more efficient (e.g., promoted team on win streak, or team that won playoffs), its recent efficiency should count extra, but only if we have enough recent evidence.

**This is NOT the old rejected recency weighting C6 (84/84 no discrimination). That test used simple exponential recency on all evidence paths. Owner wants a specific gate: minimum playoffs/min matches evaluation → weighted inclusion.**

Formalisation — Current Performance Blend:

- **Base rating:** L1 fit over long window (≥2 full seasons, n≥ ~60 matches per team across seasons) — stable.

- **Current form rating:** Short-window fit over recent period:
  - Option A (recent league form): last 6 matches before cutoff (perfView L2512) — last-6 W-D-L + goal diff.
  - Option B (playoffs/clutch): playoff legs + final 5 regular rounds (high pressure) — minimum number of playoffs = e.g., 3 playoff ties or 4 matches in last 30 days.

- **Gate:** Only if team meets minimum thresholds:
  - ≥6 recent matches (or ≥3 playoff matches) in last 60 days
  - Both home ≥2 and away ≥2 recent (not just home streak)
  - Current form GD differs from base expectation by >0.5 goals/match (efficiency jump)

- **Weighting:** If gate passes, blend:
  ```
  GD_base = E[λ_home - λ_away] from base ratings
  GD_current = E[λ_home - λ_away] from short-window ratings (same constants, short train)
  α = min(1, (n_recent - min_required)/(max_required - min_required)) * k
     where k = calibration factor 0.3–0.5 (so current never dominates, max 50%)
     n_recent = number of recent matches meeting gate
  GD_final = (1-α)*GD_base + α*GD_current
  ```
  Then convert GD_final back to λ adjustments proportionally: λ_home_final = λ_home_base * (1+ α*delta) etc., preserving Poisson structure.

- **Display:** "Current form: efficient ↑ — last 6: W5 D0 L1 GD +8 vs base +2.3 — weighted 35% into prediction" with icon ⚡ for hot, ❄️ for cold, plain English.

- **Entry test (required per T1-T8):** Short-form blend must beat base-only on last omitted season, paired Brier + direction, per league, with n and MDE. Old C6 rejected because it had no gate and no cap — this version has gate + cap + playoff filter.

- **Status:** Candidate for S4/S5 after M7 — NOT live until harness win. Implement in audit_work as `current_form_blend.py` → test on 5082 store → if wins, ship in builder S4.

---

## 4. How These Three Make App Accurate/Real-World + Alive

- **Per-team live:** Every new result moves att/def — app alive day to day.
- **Per-league pivot:** Every new Euro result moves s[L] — cross-league predictions stay real-world, not frozen UEFA coefficient.
- **Current performance:** If team suddenly hot (playoff run, 6-game win streak), α blend gives it extra credit but capped and gated, so prediction reflects efficiency without overreacting.

All three use only results (P1/P2), all three have provenance M3, all three refuse honestly if insufficient data (P3).

*This clarification upgrades Masterplan §6 from "league-strength scale" to "per-league pivot points X above/below" + adds live per-team + current form weighting as owner intended.*
