# 07 — CHAIN & LEAGUE-STRENGTH AUDIT (R2 cross-border)

**Date:** 2026-08-05 continued  
**Analyst:** Lead Planner (Arena) — branch arena/019fd213-the-bettor-1  
**Files audited:** `previous_work_files/.../chain/chain.py`, `build_graph.py`, `league_strength.py`, `weighted.py`, `calib_chain.py`, `validate.py`, `verdict.py`, `test_weighted.py`, `test_league_adj.py`, plus `data/homevhome.py`, `hvh_ava.py`, `transitive.py`

## 1. Build Graph — Foundation Step 1 (build_graph.py)

**Input:** `data/all_matches.pkl` 153k matches (ENG 18 leagues + POL, DNK, EUR CL/EL/Conf txt parsers).  
**Method:** Domestic edges DOM:<lg> country mapped via CTRY dict ENG/SCO/GER/ESP/ITA/FRA/NED/BEL/POR/TUR/GRE, plus POL/DNK CSVs, plus European edges EUR:<comp> parsed from `/tmp/ucl/champions-league-master/*/*.txt` with regex `(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)`.  
**Output:** `edges.pkl` — list (date, comp, ch, h, ca, a, hg, ag). Domestic ~? + EUR ne edges. Total printed, clubs count, countries count.  
**Zero market:** results only.  
**Verdict:** historical builder, used for old 153k dataset. Not used in current 5082 store path. Logic sound but hard-coded `/home/user/` paths stale — not load-bearing today. Keep as reference for OLD-PORT-01 (M12).

## 2. Chain System — Foundation Step 2 (chain.py)

**Purpose:** Find and score opponent chains between any two clubs. Results only.

**Normalization:** `norm(s)` — NFKD ascii strip, lower, drop club-type tokens {fc,afc,ac,as,sc,sk,fk,nk,hnk,... sv,vfl,... rcd,ud,ss,...} — aggressive merges AFC Ajax→Ajax, ACF Fiorentina→Fiorentina — fixes split-identity bug that severed cross-border bridges (Study 22). Proven.

**Alias table:** hand-verified map sherifftiraspol→FC Sheriff, dynamokyiv→Dinamo Kiev, flora, vojvodina, lnz, noah, zimbru, zrinjski, braga, etc. — single identity per club across seasons. Discipline matches ROLE-RESEARCHER rule 7 (one identity per club).

**Resolution:** `resolve(name)` — norm key exact → alias norm → canon, else unique prefix match if len diff ≤4 and exactly one candidate. Otherwise None (honest unresolved).

**Edge index:** RES[H][A] = [(date,gd,comp)] built from EDGES pkl — both directions.

**API:** `find_chains(team_a,team_b,since="2021-01-01",max_hops=3)` returns:
- oppA, oppB counts in window,
- direct = [(date,gd,comp)],
- phase2 = shared opponents via x: est = avg_gd(oppA[x]) - avg_gd(oppB[x]), n = lenA+lenB, y0/y1 years, ctx = comp types joined
- phase3 = opponent-of-opponent via x>y where x not shared, y in oppB and not in shared: est = avg_gd(oppA[x]) + avg_gd(oppX[y]) - avg_gd(oppB[y]), n = sum, ctx joined. Shared set excluded to avoid double count.

**Summarise:** mean, sd, lo/hi/spread, oldest/newest, mixed_ctx count.

**Verdict function (honesty shell):**
- NO CHAINS if None
- THIN if n<3 "too few"
- NOT USABLE if spread >4.0 goals "paths disagree"
- WEAK if sd>1.5 high dispersion
- STALE if newest<2021
- else USABLE "n paths sd x.xx"

**Measured effectiveness (from SOT M9):** 3rd phase r=+0.274 n=693 62.6% direction, 2778 European matches. Two known defects:
1. Usability gate disproven — measured: tight spread WORSE than wide (r 0.195 vs 0.384) — spread-based gate rejected (E6, T8).
2. Path discovery too narrow — opponent-of-opponent only, no longer chains, no weighting.

**Weight class:** STANDBY — needs harness win vs frozen scale 1.00 baseline before operational. Currently evidence-cross display only in app. No probability.

**Zero market:** no odds input.

## 3. League Strength — Does Ignoring Distort Chains? (league_strength.py)

**Method:** European matches only as common arena — results only, no coefficient tables.

- ctry map club→home country from domestic edges, fill from European edges where domestic missing.
- Perf per country: played, gf, ga from EUR edges only.
- Compute GD per match for countries with ≥40 euro matches.
- Output league_strength.pkl (strength dict country→GD/match, ctry dict).
- Spread check: strongest vs weakest range, sd.

**Result shape (from old data, not current 5082 — 5082 has 0 Euro rows):** strongest ~+? vs weakest ~-? range few goals per match. Enough to matter.

**Implication for singular engine:** If leagues differ in strength, chaining via goal difference without adjustment biases cross-league predictions. Therefore fit-to-results loop (Masterplan §6): s_L league strength rescales att/def onto common scale.

**Guardrail:** No arbitrary multiplier — weights from fit. Historical test: European-edge scale >1.00 degraded RMSE — frozen 1.00 baseline incumbent to beat. Hold-out win required.

**Status:** Reference implementation for OLD-PORT-01. New connector pack #17 (2000-2500 Euro rows) will be the new edges.pkl for current 5082 store.

## 4. Weighted Scale — User's Weighted Result Scale (weighted.py)

**Definition (user's rationale: weighs wins/draws/losses on single scale, separates 0-0 vs scoring draw):**
- draw 0-0: +1
- draw 1-1,2-2...: +2
- win by 1: +4
- win by 2+: +6
- loss by 1: -4
- loss by 2+: -6

Functions `wscore(gf,ga)` and `wscore_from_gd_only(gd)` (0→1.5 midpoint). SCALE dict.

**Measured:** Tested against plain goal difference in `chain/test_weighted.py`, `audit-22-weighted-scale.md`. Result: user spec implemented, but did it improve chain direction? Audit 22 shows weighted scale tested vs plain GD — no significant gain after paired T1 (needs re-check with new Euro data).

**Weight:** Candidate W? Not operational until held-out win. Part of W1-W4 weighting candidates (phase weights).

## 5. Calibration & Validation Chain

- `calib_chain.py` / `test_league_adj.py` / `test_weighted.py` / `validate.py` / `verdict.py` / `segment_test.py` / `totals_test.py` / `p4test.py`
- `validate.py` — checks chain predictions vs actuals? Needs read.
- `verdict.py` — likely same as chain.py verdict but per fixture.
- Tests compare weighted vs unweighted, league-adjusted vs plain.

**Key finding from SOT M9 / audit-21..23:** 
- Chain validation r=+0.274 is promising but below R1 L1 +5.6% Brier. Therefore chain stays as confidence/balance, not probability, until fit-to-results loop wins.
- League weighting from European GD per match is promising direction but not yet winning vs frozen 1.00 baseline — hence A-08 APPROVED-FOR-DOCUMENTATION only, not build order, with explicit harness gate: weighted common scale must beat frozen scale on omitted European window (2025-26 Euro matches).

## 6. How Chain Fits Into Singular Engine (Blueprint §1)

```
STORE 0 Euro rows today → chain graph = thin for cross-league (only domestic paths)
After #17 UEFA connector pack (2000-2500 rows) → chain graph becomes usable for cross-league fixtures
    ↓
Phase2: shared opponents (e.g. Arsenal and Dynamo Moscow both played Shakhtar)
Phase3: opponent-of-opponent (Arsenal > Benfica > Dynamo) 
    ↓
Summarise mean/sd/spread → zone ladder confidence (NOT probability) + balance panel home/draw/away support shares
    ↓
For rated bridge (future S5): fit s_L league strengths via iterative bias loop:
  bias(L)=mean(predicted GD - actual GD) over connector ties involving L
  s_L←s_L×(1+step×bias) step 0.05-0.1 20-50 iterations until bias<tol
  Validate: weighted vs 1.00 frozen on last omitted Euro window
  If wins → s_L rescales att/def for cross-league fixtures → standard L2-L5 apply
  If not → stay silent "no calibrated bridge" + chain evidence view remains (P3 honesty)
```

## 7. Effectiveness Weighting Consolidation

| System | Gain | Weight Class | Gate |
|---|---|---|---|
| chain phase2 shared opponent avg_gd diff | part of r+0.274 62.6% dir | evidence | — |
| chain phase3 opponent-of-opponent | contributes to same r | evidence | — |
| league_strength GD/match per country | range few goals, enough to matter | input to s_L fit | — |
| weighted scale wscore | tested vs plain GD, no sig win yet | candidate W1-W4 | held-out win required |
| fit-to-results loop s_L bias→scale | promise: bump league until matches | future rated bridge | harness win vs 1.00 baseline on omitted Euro window §6 |

**Why standby not dominant:** R1 L1 DC fit beats base -6% to -12% on last omitted season; chain direction 62.6% but small n and high sd/spread — below threshold for probability. Therefore chain = balance/confidence, not probability — enforced by weighting rule (no component consumes higher-ranked output).

## 8. Actions for Builder S5 (Cross-Border)

- Need UEFA connector #17 to become new edges.pkl for current store.
- Productionise chain as app module evidence_graph L1506-1609 already live but narrow — keep but do not use as probability.
- Implement fit-to-results loop in audit_work then port to app as masked replay artifact (M5).
- Validate per §5 ladder: fit on 2021-22..2024-25 Euro, test on 2025-26 Euro LAST OMITTED window, weighted vs frozen 1.00, paired T1, MDE T2.
- If passes → S5 ships, cross-league fixtures rated on weighted common scale.

*Chain is the nervous system for cross-league — not the brain (R1 is). It deserves balance panel (M7) and gated bridge (M9/M19), not premature promotion to probability.*
