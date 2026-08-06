# 15 — Architecture Human-Friendly Prototype (Smooth English, Icon Highlights)

**Date:** 2026-08-05 continued  
**Status:** DRAFT for S7 after S0-S6 gates — ready for builder B7  
**Owner directive:** delivery communicates in smooth English not for bots with scattered contents and random explanations jumbling, icon highlights can always provide context explanation etc

---

## Current App Problems (v3.6.3 md5 17dd2b...)

- One HTML file 635k, 5 tabs, but machine strings leak into main: `predictFitted`, `H 62.3%`, `λ_h 1.84`, `Brier 0.5675`, `DC ρ-0.06`, `ELO 1567`, `starAdj 0.02`.
- No provenance M3 — numbers appear without source/window/n/cal/date.
- Form stars null live path (G17), calibration stale M5, no balance panel M7, coverage undefined M14, teamStats cache empty M6.
- AI-styled: verbose scattered explanations, no clear primary action per tab, no progressive disclosure.
- General functionality poor per owner.

## Target — Smooth English + Icons + Context

### Design System

- **Font:** system sans, 16px base, line-height 1.5, max-width 720px content, centered.
- **Colors:** light/dark via theme toggle ◐ — contrast AAA.
- **Icons:** emoji with title attribute + 4px margin, not decoration. Every icon has tooltip smooth English sentence.
- **Layout:** Header (Backup + store census + last replay date) → Tabs (Match, Evidence, Data, Calibration, Log, Integrity) → Main card (verdict sentence + icons) → Why collapsible → Technical details collapsible small-print.
- **CTAs:** One primary per tab (Predict, Drop file, Run replay) — large, obvious.
- **Empty states:** Honest plain "Not rated yet — needs 6 matches" + balance bar + reasons, never blank or 0%.

### Icon Dictionary (Shared Across Screens)

- 🛡️ Fortress = Team very strong at home — "Wins 78.5% at home when we rate Fortress (7,718 past games like this)"
- 📈 ↑ = Rating up — "Live rating up after beating expectation last 3 games"
- 📉 ↓ = Rating down — "Live rating down after under-performing last 3"
- ⚡ Hot = Efficient lately — "Last 6: W5 L1 GD +8 vs base +2.3 — weighted 35% into tip (if adopted) or tracked only (if not adopted)"
- ❄️ Cold = Struggling
- 🌍 Pivot = League pivot — "Premier League +0.20 above Czech (42 Euro head-to-heads, bias 0.01)"
- 🔗 Chain = Evidence paths — "Shared opponents: both played Shakhtar — 2 paths, spread 1.2 — usable"
- ⚖️ Balance = Support shares — "Home 48% / Draw 22% / Away 30% — evidence split, we say NO CALL"
- 📅 Window = Data window — "Based on 960 games 2021-22 to 2024-25"
- ✅ Calibrated = Replay won — "Live model beat base 12.2% on last hidden season (254 games)"
- 🚫 Withheld = BTTS withheld — "We don't show BTTS — calibration error 6.0% too high"
- 💾 Backup = Safety — "Backup before any purge — undo = load backup file"
- 💡 Tip = Insight — "Draw risk — same-tier gap, draw rate 24% (capped ±2%)"
- 🔍 Provenance = Source — "Source: live DC fit, window ..., n=..., Brier ..., date ..."

### Match Tab Prototype — Smooth English

```
Header: 
  [◐ Theme] [💾 Backup]  v3.7.0  5,082 matches · 609 teams · last replay 2026-08-05 ✅

Team Picker (searchable, grouped by league flag, shows 6-game form):
  [Arsenal ▼] 🛡️ Fortress  W4 D1 L1 last 6   vs   [Sparta Prague ▼] 📈 ↑ W5 D0 L1 ⚡ Hot
  [Swap ⇅]

[Predict] primary CTA

Verdict Card after Predict:

  Arsenal 62% to win at home
  📅 Based on 960 games (2021-22..2024-25)  ✅ Calibrated: beat base 12.2% on last hidden season
  🛡️ Fortress — wins 78.5% when we rate Fortress (7,718 games)

  Confidence: STRONG — won 78% of similar past tips (59 like this) — 📈 trend stable
  🌍 League pivot: Premier League +0.20 above Czech (42 Euro meetings, bias 0.01) — used in this tip
  
  Current form:
  ⚡ Sparta hot — last 6 much better than base (+8 GD vs +2.3 base) — tracked, not weighted yet (test showed +0.009 Brier worse, so base only for now)
  💡 Why not higher? Draw risk — same-tier gap, draw rate 24% (capped ±2%)

  [Save this tip 💾]  [Technical details ▼]

  Technical details collapsed small-print:
    λ_home 1.84 λ_away 0.92 scoreGrid Poisson×Poisson DC τ ρ-0.06 normalised H/D/A raw, 
    goalsGrid shrunk k=0.5 GMU2.6186 → O/U, draw correction draw_table[A|gap1] +0.015 proportional M4,
    att Arsenal +0.32 def -0.11 hfa Premier 0.28 home_extra +0.02, ELO 1567 ★★★★☆ (not prediction),
    points round(100×H_cal)=62, tier A+≥70, consensus STRONG 1.6 both sides ≥4H≥4A 78.6% vs 73% top10%,
    Brier DC 0.5675 vs base 0.6465 -12.2% n254 dir55.9% logloss0.957, window 2021-22..2024-25, replay 2026-08-05,
    provenance: dc-fitted-model n=960 window 2021-22..2024-25 Brier..., league-pivot s[ENG]=+0.12 s[CZE]=-0.08 n=42 bias0.01 date...
```

No bot numbers in main, all in Technical details.

### Evidence Tab When NO CALL

```
We can't rate this yet — honest.

Reason: Sparta has only 4 home games (needs 6) — need more results.
What we can show: 🔗 Chain evidence (2 paths)

Via Slavia: Arsenal +0.6, Via Banik: +0.3 — mean +0.45 SD0.21 spread 0.3 — USABLE
⚖️ Balance: 58% Arsenal / 18% Draw / 24% Sparta — evidence split, we say NO CALL rather than guess.

🌍 No calibrated bridge yet — need 20+ Euro ties, we have 12 (UEFA connector pack #17 in progress)

We'd rather say NO CALL than force a number.
```

### Data Tab — Files

```
Drop result file here (.txt)

We check every file for format, dates, scores, duplicates. Rejected files never saved — you'll see reason in plain English.

[Drop zone — click or drop]

Staged: CZ1-2021-2026.txt 1,401 matches
  ✅ Ready to Approve — [Approve]  [View holds 20]  [Discard]
  Holds: 20 cup ties have different tieIds — we keep rows verbatim, you approve keep verbatim (Z-003) — safe.
```

### Coverage Tab

```
What we hold — honest:

England Premier League: 1,900 games 2021-22 to 2025-26 ✅ Complete 📅 5 seasons
Czech First League: 1,381 + 20 playoffs + 202 cup = 1,603 ✅ Complete (11 date fixes D-1 applied) 📅
Russia: 1,579 ✅ Complete
Missing: Spain 0, Italy 0, Germany 0, France 0, Scotland cups 0, MLS 0 — see Request tab

Small-country 156 rows purged by owner decision — backup kept 💾
Leftover test rows Germany 2 Wales 2 purged — final 5,082
```

### Calibration Tab

```
Our model proves itself by hiding last season, retraining on earlier, predicting hidden.

[Run masked replay] primary

Last replay: 2026-08-05 ✅
  RPL: trained 960, tested 254 hidden → beat base 12.2% (0.5675 vs 0.6465) — strong
  CZ1: 1105→276 → beat 6.4%
  ENG: 1520→374 → beat 6.0%

Ladder:
  Last 1 game: 100% direction (noise, not proof)
  Last 10: 66.7% → Last FULL season: 55.9% stable real

Artifacts: dc-fitted-model, draw_table 27 cells, tiers, league-pivot ENG+0.12 CZE-0.08 n42 bias0.01 date2026-08-05

Next monthly sweep due: 2026-09-05
```

### Log & Settlement

```
Settled tips (20 newest):

Arsenal vs Sparta — saved 62% Home — result 2-0 — WIN — draw would be LOSS (never push I5 rule)
...

Every tip frozen at save — live ratings may move later, frozen never changes.

Audit trail: 55 events (migrations, commits, purges, snapshots) — travels in every backup — append-only, provable.
```

### Integrity & Snapshots + Country Packs

```
Muted rows: flagged with reason, kept visible, excluded every calc — never deleted. Restore reverses.

Snapshots: before every commit + purge hash snapshots.

Integrity screen: outcomes-only (no market P1) — future M10 own-model collapse detection.

Country packs:
  Scope: pick country (+ competition) → Preview 1,401 matches 25 clubs → Mute soft (excluded not deleted) vs Purge hard backup-gated "Download backup, then purge" → auto-download named pre-purge → unlock "backup ready" → purge logs backup filename. Text: "No undo inside app. Undo = load backup you just downloaded."
```

---

## Builder Instructions S7

- One HTML file still, <1MB, no network fetch/XHR, localStorage pitch-rating-v3.store.
- Replace machine strings in main with smooth English sentences above, move old strings to <details> Technical details small-print.
- Add icon dictionary with title tooltips — CSS for icon highlights (background #f0f0f0 rounded 4px padding 2px 6px).
- Implement provenance panel M3: source/window/n/cal/date small-print per number.
- Implement balance panel M7: ⚖️ bar chart home/draw/away support shares for NO CALL.
- Fix M14 coverage undefined, M6 teamStats cache, G17 live form stars null.
- Progressive disclosure: summary → why → technical — user can stop after summary.
- Accessibility: keyboard nav, screen reader aria-labels, theme toggle, contrast AAA.
- Performance: no external deps, single file.

*This prototype is target for human-friendly delivery — smooth English, icons with context, not bot scattered — icon highlights always provide context explanation.*
