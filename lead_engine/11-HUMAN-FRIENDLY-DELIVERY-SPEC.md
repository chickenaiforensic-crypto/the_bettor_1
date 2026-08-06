# 11 — Human-Friendly Delivery Spec (Smooth English, Not Bot Scattered)

**Owner directive:** "I want a delivery that communicates in smooth English not for bots with scattered contents and random explanations jumbling all over the surface - icon highlights can always provide context explanation etc"

Audience: human who wants to bet smarter with zero market, not data scientist. Machine strings belong in small-print Technical details only (A-02 decree).

---

## Principles

1. **One idea per sentence.** Every number has a plain-English sentence + proof in small print.
2. **No bot dumps.** No "Model Brier 0.5675 LogLoss 0.957 dir 55.9% (n=254) etc" in main UI. Main UI = human, details collapsible.
3. **Icons give context.** Use icons as tooltips/highlights, not decoration.
4. **Provenance always, but small.** Every probability shows source, window, n, calibration, date in small print M3.
5. **Honest refusal is UX:** NO CALL is a valid, helpful output with balance bar and reasons, not an error.
6. **App is alive:** Show live rating trends ↑ → ↓ with last update date, not static numbers.

---

## Icon System

| Icon | Meaning | Tooltip (plain English) | Where shown |
|---|---|---|---|
| 🛡️ A+ Fortress | Team very strong at home | "Wins 78.5% at home when we rate Fortress (7,718 past games)" | Match card tier |
| 📈 ↑ | Rating going up | "Live rating up after beating expectation last 3 games" | Team header |
| 📉 ↓ | Rating going down | "Live rating down after under-performing last 3" | Team header |
| ⚡ Hot | Current form much better than base | "Efficient lately — last 6: W5 L1 GD +8 vs base +2.3 — weighted 35% into this tip" | Current performance block |
| ❄️ Cold | Current form worse | "Struggling lately — last 6: L4 — we lowered expectation 20%" | Current performance |
| 🌍 Pivot | League pivot points | "Premier League rates 0.20 points above Czech league based on 42 direct Euro results" | Cross-league card |
| 🔗 Chain | Evidence paths | "Shared opponents: both played Shakhtar — 2 paths, spread 1.2 goals — usable" | Evidence tab |
| ⚖️ Balance | Support shares | "Home 48% / Draw 22% / Away 30% — evidence split, we say NO CALL" | NO CALL card |
| 📅 Window | Data window | "Based on 960 games from 2021-22 to 2024-25, last replay 2026-08-05" | Provenance small print |
| ✅ Calibrated | Replay won | "Our live model beat base rate 12.2% on last season hidden" | Calibration tab |
| 🚫 Withheld | BTTS withheld | "We don't show BTTS — calibration error 6.0%, too high" | Goals section |
| 💾 Backup | Safety | "Backup before any purge — undo = load backup file" | Country packs tab |

All icons have title attribute with smooth English explanation, not just emoji.

---

## Screen Redesign — Smooth English

### Match Tab (Daily Use)

**Before (bot):** "predictFitted H 62.3% D 24.1% A 13.6% λ_h 1.84 λ_a 0.92 tier A+ consensus STRONG 1.6 ELO 1567 starAdj 0.02 Brier 0.5675"

**After (human):**

```
[Team picker: searchable, grouped by league, shows country flag, 6-game form WWWLWD]

Arsenal [🛡️ Fortress] vs Sparta Prague [📈 ↑]
Arsenal last 6: W4 D1 L1  |  Sparta last 6: W5 D0 L1 ⚡ Hot

Verdict: Arsenal 62% to win at home
  📅 Based on 960 games, last replay 2026-08-05
  ✅ Calibrated: live model beat base 12.2% on last hidden season (254 games)
  
  Confidence: STRONG — won 78% of similar past tips (59 tips like this)
  Current form: Sparta hot ⚡ — their last 6 much better than base, we gave them 35% extra credit
  
  Why not higher? Draw risk — same-tier gap, draw rate 24% (we capped adjustment ±2%)
  
  Technical details (small print):
  λ_home 1.84 λ_away 0.92 scoreGrid Poisson DC ρ-0.06 H/D/A raw, draw correction draw_table[A|gap1] +0.015 proportional renorm,
  att Arsenal +0.32 def -0.11 hfa Premier League 0.28 home_extra +0.02, ELO 1567 ★★★★☆ (not a prediction)
  
  [Save this tip] [Swap]
  
  Not enough? For cross-league fixtures where leagues differ: 🌍 Premier League pivots +0.20 above Czech league (42 Euro head-to-heads, bias converged 0.01)
```

Key: Main = one sentence verdict + icons + why. Small print = numbers for auditor.

### Evidence Tab (When No Rating)

```
We can't rate this yet — honest.

Reason: Sparta has only 4 home games in store (needs 6) — we need more results before we rate.
What we can show: 🔗 Chain evidence

Shared opponents: both beat Slavia last season
  2 paths: Arsenal +0.6 via Slavia, +0.3 via Banik — mean +0.45 SD 0.21 spread 0.3
  Verdict: USABLE ⚖️ Balance 58% Arsenal / 18% Draw / 24% Sparta

No league pivot yet for this pair — 🌍 no calibrated bridge (needs 20+ Euro ties, we have 12)

We'd rather say NO CALL than guess.
```

### Data Tab — Files

```
Drop your result file here (text file .txt)

We check every file for format, dates, scores, duplicates. Rejected files never saved — you'll see reason.

[Drop zone]

Staged: CZ1-2021-2026.txt 1,401 matches → ✅ Ready to Approve
  Holds: 20 cup ties need human keep-verbatim (different tieIds) — click "Approve keep rows verbatim (Z-003)"
```

Smooth English, not "PR.ingest L709 COMP_TYPES whitelist".

### Coverage Tab

```
What we hold — honest inventory:

England Premier League: 1,900 games (2021-22 to 2025-26) ✅ Complete
Czech First League: 1,381 + 20 playoffs + 202 cup = 1,603 ✅ Complete (D-1 11 date fixes applied)
Russia: 1,579 ✅ Complete
Missing: Spain, Italy, Germany, France, Scotland cups, MLS — Request tab

150 small-country rows purged by owner decision — backup kept.
```

No "undefined" labels — M14 fixed.

### Calibration Tab

```
Our model proves itself by hiding last season, retraining on earlier, predicting hidden.

[Run masked replay] — one click after any data change.

Last replay: 2026-08-05
  Russian League: trained 960, tested last 254 hidden → beat base 12.2% (0.5675 vs 0.6465) ✅
  Czech League: trained 1105, tested 276 → beat base 6.4% ✅
  England: trained 1520, tested 374 → beat base 6.0% ✅

Expanding holdout ladder:
  Last 1 game: 100% direction (small, noise)
  Last 10: 66.7% → Last FULL season: 55.9% (stable, real)

Artifacts: dc-fitted-model, draw_table, tiers, league-pivot s[ENG]=+0.12 s[CZE]=-0.08 n=42 bias 0.01 date 2026-08-05

Monthly full sweep: next due 2026-09-05
```

No bot dump of Brier/LogLoss without context.

### Log & Settlement

```
Settled tips (last 20, newest first):

Arsenal vs Sparta — saved 62% Home — result 2-0 — WIN — draw would have been LOSS (never push, I5 rule)
...
Every tip frozen at save — live ratings may move later, frozen never changes.

Audit trail: 55 events (migrations, commits, purges, snapshots) — travels in every backup — append-only, provable.
```

### Integrity & Snapshots

```
Muted rows: suspicious games flagged with reason, kept visible, excluded from every calculation — never deleted. Restore reverses.

Snapshots: taken before every data commit + purge hash snapshots.

Integrity screen: outcomes-only (no market prices per P1) — future M10 screen will detect own-model collapse only.
```

### Country Packs

```
Scope: pick a country (optionally one competition)

Preview before any action:
  Matches: 1,401, Clubs: 25, Seasons: 5, Comps: League + Relegation Playoffs + MOL Cup breakdown

Mute scope (soft): Exclude from every calculation, not deleted — Unmute restores.

Purge (hard): Backup-gated — button says "Download backup, then purge" → auto-downloads pitch-rating-full-data-<date>-pre-purge-<scope>.json → unlocks "backup ready" → purge logs backup filename. Text: "There is no undo inside app. Undo = load backup you just downloaded."

Purge removes scope matches + orphaned identities, keeps artifacts.
```

---

## Writing Rules for Builder S7

- **Plain language first:** Main UI uses words like "We think Arsenal wins 62% at home" not "H_calibrated 0.623".
- **Machine small-print second:** Collapsible <details> Technical details = λ, Poisson, draw_table, att/def, ELO, Brier.
- **Progressive disclosure:** Summary → why → technical. User can stop at summary.
- **Primary CTA per tab:** One obvious button (Predict, Drop file, Run replay). No 5 equal buttons.
- **Empty states honest:** "Not rated yet — needs 6 matches" not 0% or blank.
- **Performance:** one HTML file <1MB, no network fetches.
- **Accessibility:** keyboard nav, screen reader labels, theme toggle works, contrast OK.
- **Icons always with title:** Not just emoji — hover shows smooth English explanation.

*This spec is the target for S7 architectural build after S0-S6 structural gates pass by test run. Human-friendly = smooth English + icons with context + provenance small-print, not AI-sounding scattered bot explanations.*
