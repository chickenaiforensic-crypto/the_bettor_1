# Pitch Rating — forward-test plan (football gate → tennis)

Date: 2026-07-31 · App: v2.6.7-cross (frozen for the whole slate)
Owner call: 20 games → then calibrate if needed → then done with football → tennis replication.

---

## 1. The two engines decide the map

| Engine | Where it fires | Cost per game | What the test must prove |
|---|---|---|---|
| Calibrated model (Dixon–Coles, percentages) | Both teams inside the 18 rated leagues | Zero — no packs needed | Probabilities still calibrate on 2026-27 games; no band inversion |
| Evidence engine (H2H / common / level-3; Lean only / NO CALL) | Any fixture with an unrated side | One pack per new opponent | Leans hit above base rate; NO CALL fires when data is thin; nothing fabricated |

Mixing the two lanes in one sample would corrupt both readings. They run separately.
Known debt the test targets: phase weights 3/2/1.5 and cross-bridge scale 1.00 are unvalidated; cross-border percentages stay withheld until calibration tables exist.

## 2. Tournament productivity map (most mappable areas, ranked)

### Tier 1 — rated domestic leagues (Lane 1 core)
Maximal per-team and common-opponent data: every side meets the same opponents all season, all in-model.

| League | Code | Volume | Availability |
|---|---|---|---|
| Scotland Premiership | SC0 | 6/round | **Season open NOW (1–3 Aug)** |
| Belgium Pro League | B1 | 8/round | **In season (MD2 this weekend)** |
| Turkey Süper Lig | T1 | 9/round | from ~8 Aug |
| Netherlands Eredivisie | N1 | 9/round | from ~7–9 Aug |
| Portugal Primeira | P1 | 9/round | from ~8–10 Aug |
| England PL/Ch/L1/L2 | E0–E3 | 46–48/wk | from ~8–16 Aug — volume king |
| France 1/2, Germany 1/2, Italy A/B, Spain 1/2, Greece | F,D,I,SP,G | 8–10/round each | rolling in to ~23 Aug |

### Tier 2 — UEFA ties with at least one rated club (Lane 2 core)
Common-opponent web is dense across borders — the Malisheva closure produced 19 level-3 chains from modest bridge data.

- **UECL/UEL Q3 first legs (4–6 Aug)** and playoffs (20/27 Aug): Hibernian–Shkëndija, Motherwell tie, plus Rangers/Hearts (UEL Q3 seeded pools), Anderlecht/USG, Benfica, PAOK/Olympiakos, Beşiktaş/Fenerbahçe, AZ/NEC, Real Sociedad/Celta, Bournemouth/Sunderland/Palace, Juventus/Milan, Marseille/Rennes, Leverkusen/Hoffenheim pools; Celtic (UCL qualifier per SPFL postponement note).
- League phases from Sep–Oct: dozens of rated-vs-unrated fixtures per matchday.

### Tier 3 — strong-coverage unrated leagues (supplementary only)
Norway, Sweden, Denmark, Finland, Ireland (in season); Poland, Czechia, Austria, Switzerland, Croatia, Serbia. Evidence engine with double packs — heavier research cost; filler when UEFA is quiet.
Flag: making these *rated* = model retraining — parked, not in this plan's scope.

### Excluded (Tier D)
Thin-record sides/competitions (Andorra, Luxembourg, Belarus, Montenegro, Kazakhstan, etc.) — NO CALL territory by design; never in the sample.

## 3. The 20-game slate

### Lane 1 — calibrated domestic (12 games)
- **Scotland R1 (Sat–Mon):** Falkirk v St Mirren (1 Aug 15:00), Aberdeen v Hearts (1 Aug 17:30), St Johnstone v Kilmarnock (2 Aug 14:00), Hibernian v Motherwell (2 Aug 16:30), Celtic v Dundee (3 Aug 19:30) — 5 games.
- **Belgium MD2 (1–2 Aug):** 7 games picked from the official fixture list at slate-lock (16 rated clubs).
- Both sides rated → Rate tab, model output, no packs. Domestic lane is blind-immune by construction: the model is frozen and no pack curation is involved.

### Lane 2 — evidence engine, cross-border (8 games)
- **UECL/UEL Q3 first legs (4–6 Aug), one rated club per tie**, picked from the confirmed Q3 draw; Hibernian v Shkëndija (6 Aug) is fixture #1.
- One team pack per unrated opponent, cutoff = match date, minus the game itself, loaded before rating.
- Blinding rule: fixtures whose result I (the assistant) have already seen are excluded or researched by an external researcher via the app's request template — my curation must never know the answer.

## 4. Protocol per game (identical every time)

1. Fixture confirmed from an official list before kickoff; Lane 2: pack loaded first.
2. Rate blind (cutoff = match date) → **Save verdict to Log before kickoff**.
3. No engine/app edits during the slate — **v2.6.7-cross is frozen for all 20** (calibration hygiene: one model version per sample).
4. After FT: settle in Log with the 90-minute result (Leagues Cup-style shootouts/AET ignored; draw is not a home-win success).
5. Tally sheet updated the same day: band, verdict, leans, NO CALLs, hit/miss.

## 5. Gates (defined now, not after)

- **Gate 0 — replay backtest (added 2026-07-31, results in REPLAY-RESULTS.md):** masked leave-one-out replay of all 61 stored matches exposed **h2h section = 36% anti-signal** (raw GD reuse, no venue-flip/shrinkage); aggregate leans 50%; common 57%, chains 50% (noise); NO CALL discipline held (66% abstention, all caps intact). Consequences: engine unchanged until a calibration candidate beats this same replay at ≥60%; Lane 2 leans go into the slate as pre-registered *tests*, not *validations*.
- **Lane 1:** sampled Brier in line with validation baseline (0.6112 broad tolerance at n=12); no band inversion (A+/A losing more than B/D bands); calibrated-vs-actual gaps eyeballed per band for the big-project list.
- **Lane 2:** lean hit rate ≥ 60% with NO CALL rate reported separately (a lean tally that avoids games counts as discipline, not failure); zero un-settleable verdicts; every NO CALL logged with its reason.
- **Decision rule after 20:** gross failure → fix weights/bridge scale and re-test another slate; directional-but-small issues → log for the big calibration project (uncalibrated percentages stay locked); clean → close football, start tennis.
- Honesty bound: n=20 catches gross failure and discipline, not fine calibration (100+ per band). Nobody recalibrates off one shock result.

## 6. Responsibilities

- **Assistant:** pack research + audits (Lane 2), tally sheet maintenance, harness integrity, no result-peeking before settlement (disclosed if unavoidable).
- **User:** rate each fixture in the app pre-kickoff, save verdicts, settle after FT, pick any game to drop from a slate before it's rated.

## 7. Tennis replication (parked until the football gate passes)

Confirmed mappable from this architecture: player ratings table (serve/return split), same pack schema (TEAM→PLAYER), same evidence grammar (H2H / common opponent / chains; surface maps to venueTreatment), same Log/merge/drive infrastructure, same settlement. Surface-level work only after football closes clean.

## 8. Immediate next actions

1. **Assistant:** verify Belgium MD2 fixture list (official source) → lock Lane 1 slate of 7 before tomorrow 15:00 kickoffs.
2. **Assistant:** confirm UECL/UEL Q3 tie list with rated clubs → propose Lane 2 slate of 8 incl. Hibernian–Shkëndija.
3. **User:** say go → Lane 2 pack research begins (Shkëndija first, cutoff 2026-08-06).
