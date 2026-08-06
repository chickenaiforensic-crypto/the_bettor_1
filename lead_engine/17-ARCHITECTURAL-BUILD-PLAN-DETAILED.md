# 17 — Architectural Build Plan Detailed (Human-Friendly, After Structural Lock)

**Date:** 2026-08-05 final — after structural engine LOCKED v2  
**Status:** PLAN READY FOR BUILDER B7 after S0-S6 gates — addresses owner complaint: poor content AI-styled not human-friendly quality presentation general functionality poor  
**Authority:** Functionality v1.0 screen map L####, SOT A-02 UI-PLAIN-01 plain language decree, 11-HUMAN-FRIENDLY-DELIVERY-SPEC, 15-PROTOTYPE

---

## 1. Problems Today (v3.6.3)

- Machine strings leak into main: `predictFitted`, `predictOnline`, `H 62.3%`, `λ_h 1.84`, `Brier 0.5675`, `DC ρ-0.06`, `ELO 1567`, `starAdj 0.02`, `consensus STRONG 1.6`, `HvH AvA`.
- No provenance M3 — numbers appear without source/window/n/cal/date.
- Form stars null G17 live path, calibration stale M5, no balance panel M7, teamStats cache empty M6, coverage undefined M14, MOL shortfall fixed but UI not reflecting.
- AI-styled: verbose scattered explanations jumbling all over surface, no primary CTA per tab, no progressive disclosure, no icon context tooltips.
- General functionality poor — owner.

## 2. Target Principles (A-02 + Owner Smooth English)

1. **One idea per sentence.** Every number has plain English sentence + proof small-print.
2. **No bot dumps.** Main UI human, details collapsible.
3. **Icons give context.** Every icon has title tooltip smooth English, not decoration.
4. **Provenance always small but present.** Every probability shows source/window/n/cal/date M3.
5. **Honest refusal is UX:** NO CALL valid helpful with balance bar + reasons, not error.
6. **App alive:** Show live rating trends ↑→↓ with last update date, not static.
7. **Primary CTA obvious per tab:** Predict, Drop file, Run replay — one large button.
8. **Empty honest:** "Not rated yet — needs 6 matches" not blank or 0%.
9. **Performance:** one HTML file <1.2MB, no network fetch/XHR, localStorage `pitch-rating-v3.store`, theme toggle ◐ works, contrast AAA, keyboard nav.
10. **File structure:** keep single file for now (zero network I6), but modular JS sections with clear comments `// L1 LIVE FIT`, `// L2 GRIDS`, `// R2 EVIDENCE GRAPH`, `// M3 PROVENANCE PANEL`, etc. Future split after S7 if needed.

## 3. Icon System (Shared)

🛡️ Fortress = very strong at home — "Wins 78.5% at home when we rate Fortress (7,718 past)"
📈 ↑ = rating up — "Live rating up after beating expectation last 3"
📉 ↓ = down — "Live rating down after under-performing last 3"
⚡ Hot = efficient lately — "Last 6: W5 L1 GD +8 vs base +2.3 — tracked, weighted 35% if adopted else tracked only"
❄️ Cold = struggling
🌍 Pivot = league pivot — "Premier League +0.20 above Czech (42 Euro meetings, bias 0.01)"
🔗 Chain = evidence paths — "Shared opponents: both played Shakhtar — 2 paths, spread 1.2 — usable"
⚖️ Balance = support shares — "Home 48% / Draw 22% / Away 30% — split, we say NO CALL"
📅 Window = data window — "Based on 960 games 2021-22..2024-25"
✅ Calibrated = replay won — "Live model beat base 12.2% on last hidden season (254 games)"
🚫 Withheld = BTTS withheld — "We don't show BTTS — calibration error 6.0% too high"
💾 Backup = safety — "Backup before any purge — undo = load backup file"
💡 Tip = insight — "Draw risk — same-tier gap, draw rate 24% (capped ±2%)"
🔍 Provenance = source — "Source: live DC fit, window ..., n=..., Brier ..., date ..."

CSS: `.icon {background:#f0f0f0;border-radius:4px;padding:2px 6px;margin:0 4px;font-size:14px}` + title.

## 4. Screen-By-Screen Redesign Spec (For Builder B7)

### Header

- Left: Logo "Pitch Rating" + version badge v3.7.0 + store census "5,082 matches · 609 teams" + last replay "last replay 2026-08-05 ✅" with 📅✅ tooltips
- Right: [◐ Theme] [💾 Backup] button prominent

### Match Tab (Daily)

- **Team Picker:** searchable `<input>` with datalist grouped by league flag, tolerant spelling (Nott'm Forest apostrophe, Slovacko accent), shows country flag + 6-game form WWWLWD inline + icons 🛡️📈⚡. Knows alias.
- **Actions:** [Predict] primary large, [Swap ⇅] secondary.
- **Verdict Card after Predict:**
  ```
  Main sentence bold 20px: "Arsenal 62% to win at home"
  Sub row 14px gray: 📅 Based on 960 games (2021-22..2024-25) ✅ Calibrated: beat base 12.2% on last hidden season
  Row: 🛡️ Fortress — wins 78.5% when we rate Fortress (7,718 games) | Confidence: STRONG — won 78% of similar past tips (59 like this)
  Row: 🌍 League pivot: Premier League +0.20 above Czech (42 Euro meetings, bias 0.01) — used in this tip
  Row: Current form: ⚡ Sparta hot — last 6 much better than base (+8 vs +2.3) — tracked, not weighted yet (test +0.009 Brier worse, base only for now) / or if playoff-only passes 0% usage: "No recent playoff form — base only"
  Row: 💡 Why not higher? Draw risk — same-tier gap, draw rate 24% (capped ±2%)

  [Save this tip 💾] primary

  <details><summary>Why this tip? (plain English)</summary>
    We trained on 960 games before this season, hid last season, predicted hidden, beat base 12.2% — so we trust our live rating. Arsenal attack +0.32 defence -0.11 etc.
  </details>

  <details><summary>Technical details (small-print)</summary>
    λ_home 1.84 λ_away 0.92 scoreGrid Poisson DC ρ-0.06 normalised H/D/A raw, goalsGrid shrunk k=0.5 GMU2.6186 → O/U, draw correction draw_table[A|gap1] +0.015 proportional M4, att Arsenal +0.32 def -0.11 hfa Premier 0.28 home_extra +0.02, ELO 1567 ★★★★☆ (not prediction), points round(100×H_cal)=62 tier A+≥70 consensus STRONG 1.6 both ≥4H≥4A 78.6% vs 73% top10%, Brier DC 0.5675 vs base 0.6465 -12.2% n254 dir55.9% logloss0.957 window 2021-22..2024-25 replay 2026-08-05, provenance dc-fitted-model n=960 window..., league-pivot s[ENG]=+0.12 s[CZE]=-0.08 n=42 bias0.01 date...
  </details>
  ```
- **Refusal Examples:**
  - "We can't rate this yet — honest. Reason: Sparta has only 4 home games (needs 6). What we can show: 🔗 Chain evidence 2 paths mean +0.45 SD0.21 USABLE ⚖️ Balance 58%/18%/24% — we say NO CALL rather than guess. 🌍 No calibrated bridge yet — need 20+ Euro ties, we have 12 (UEFA connector #17 in progress)"
  - "Evidence only — rating needs 2 full seasons + replay win — plain label"

### Evidence Tab (New, Separate from Match? Or Sub-Card)

- Dedicated tab or sub-section in Match card showing chain graph:
  - Direct meetings list date comp GD
  - Phase2 shared opponents table via, est, y0-y1, n, ctx
  - Phase3 opponent-of-opponent
  - Summary mean/sd/range/spread/oldest/newest/mixed_ctx + verdict USABLE/THIN/NOT USABLE/WEAK/STALE with why sentence.

### Data Tab (4 Sub-Tabs Today: Files, Coverage, Requests, Country Packs — Keep But Human-Friendly)

- **Files:**
  - Drop zone with plain English: "Drop your result file here (.txt) — we check format, dates, scores, duplicates. Rejected files never saved — you'll see reason in plain English."
  - Staged card: file name, matches count, status Clean/Held Z-003/Rejected, Approve button primary, View holds, Discard secondary.
  - Held explanation: "20 cup ties have different tieIds — we keep rows verbatim, you approve keep verbatim (Z-003) — safe. This happened because both legs of cup tie should share ONE tieId."
  - Rejected explanation: plain sentence + L####? No, plain: "Row 12: date 2026-13-01 invalid — no 13th month".

- **Coverage:**
  - Table: League | Seasons | Games | Status pill complete/partial/requested | Gaps amber | Last update
  - Honest inventory: "England: 1,900 games 2021-22 to 2025-26 complete. Czech: 1,603 complete (11 date fixes D-1 applied). Russia: 1,579 complete. Missing: Spain 0, Italy 0, etc. Small-country 156 purged by owner decision — backup kept. Leftover Germany 2 Wales 2 purged — final 5,082."
  - Fix M14 Coverage undefined label — show country.

- **Requests:**
  - "One request for whole system — lists every league needing rows. No drip-asking D12."
  - Button [New central request] explains: "Snapshots whole system and writes one request file listing every league that needs rows per team with date. Downloads both .json + .txt, logs event, tracks open→complete/partial→archived."
  - Open requests list + returns matched.

- **Country Packs:**
  - Scope picker country (+ competition optional) → Preview counts matches/clubs/attached/comp breakdown before any action L3441-3445.
  - Mute scope (soft) explanation: "Exclude from every calculation, not deleted — Unmute restores. Nothing deleted by mute." Button Mute/Unmute.
  - Purge (hard) backup-gated: button reads "Download backup, then purge" L3434 auto-downloads full backup named `pitch-rating-full-data-<date>-pre-purge-<scope>.json` L3447 only then unlocks "backup ready" L3433 purge logs backup filename L2988 in-app text "There is no undo inside app. Undo = load backup file you just downloaded" L3436.
  - Purge removes scope matches + orphaned identities, mutes go with, engine artifacts survive L2976.

### Calibration Tab

- Explanation smooth: "Our model proves itself by hiding last season, retraining on earlier, predicting hidden."
- Primary [Run masked replay] one-click after any data change.
- Last replay display: RPL trained 960 tested 254 hidden beat base 12.2% etc ✅ + ladder Last 1 100% (noise) → Last 10 66.7% → Last FULL 55.9% stable real.
- Artifacts list: dc-fitted-model, draw_table 27 cells, tiers, league-pivot s[ENG]=+0.12 s[CZE]=-0.08 n=42 bias0.01 date2026-08-05, current-form blend α gated etc.
- Monthly sweep due date.

### Log & Settlement Tab

- Settled tips 20 newest: saved % Home vs result WIN/LOSS — draw would be LOSS never push I5 rule explanation.
- Every tip frozen at save — live may move later frozen never changes.
- Audit trail 55 events travels every backup append-only provable.

### Integrity & Snapshots Tab

- Muted rows flagged reason kept visible excluded every calc never deleted Restore button.
- Snapshots taken before every commit + purge hash snapshots scope-post.
- Integrity screen outcomes-only (no market P1) future M10 own-model collapse detection.

### Backup

- Header button downloads `pitch-rating-full.json` wrapper format/version/schemaVersion/exportedAt + store+log verified size.

## 5. Technical Rails (Doctrine) Where Each Lives in Code

| Rule | Where enforced in new build |
|---|---|
| Results-only no market P1 | Ingest grammar no odds fields, engine no odds input, grep fetch/XHR/odds/price =0 |
| 90-min doctrine AET/pens 90' + NOTE advancement | Gate integer-score check L887 note system |
| Compute live or stay silent A-01 | Footer truth sentence + LIVE-DERIVE-01 S1 gate, provenance panel M3, NO CALL valid |
| No data abolition exclusion=MUTE purge backup-gated | Mute L2928 L3431 purge L2957 L3433-3451 L2988 |
| One gate rejections never stored | PR.ingest L709 L3478 |
| Dedupe add-if-new rows kept verbatim | L321/1016 L3458-3814 |
| D12 central request only | Requests tab §7 |
| Plain language A-02 | Main smooth English, machine small-print bracketed |
| Every claim provable | Log in every backup + ZONES chain + provenance M3 |
| League pivot s[L] bump-up/calibrate | Fit loop bias iteration 20-50 step0.05-0.1 artifact dc-fitted-league-pivot n/window/Brier/date |
| Live per-team up/down app alive | L1 online gradient att/def up/down seen min6 P3 |
| Current form weighted inclusion gated | Gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 0.15-0.35 blend (1-α)base+αrecent |

## 6. File Structure After S7 (Proposed)

- Keep single file `app-v3.7.0.html` <1.2MB for I6 zero network, but internal sections:
  ```
  // === L0 DATA STORE ===
  // === L1 LIVE DC FIT ===
  // === L2 GRIDS ===
  // === L3 STAR DRAW ===
  // === CURRENT FORM BLEND ===
  // === L4/L5 TIERS/CONSENSUS ===
  // === R2 EVIDENCE GRAPH + CHAIN + LEAGUE PIVOT ===
  // === R3 ELO STARS ===
  // === M3 PROVENANCE PANEL ===
  // === M7 BALANCE PANEL ===
  // === UI HUMAN-FRIENDLY ===
  // === BACKUP/MIGRATION/INGEST GATE ===
  ```
- Future after S7: split into modules if needed, but keep single file as build artifact for audit.

## 7. Acceptance Criteria for S7 (UI-PLAIN-01)

- [ ] Main UI contains 0 machine strings (no predictFitted, λ_h, Brier, Poisson, DC, ELO raw) — all in Technical details collapsible.
- [ ] Every probability has provenance small-print source/window/n/cal/date M3.
- [ ] Every NO CALL shows ⚖️ balance bar home/draw/away shares + reason.
- [ ] Every rating shows live trend 📈📉 + last update date + calibration ✅.
- [ ] Cross-league shows 🌍 pivot X points above/below with n/bias tooltip.
- [ ] Current form shows ⚡/❄️ hot/cold with last 6 W-D-L GD vs base + weighted % or tracked only explanation.
- [ ] Icons have title tooltips smooth English.
- [ ] One primary CTA per tab obvious.
- [ ] Empty states honest not blank.
- [ ] Coverage undefined fixed M14, teamStats cache fixed M6, form stars null fixed G17, calibration stale fixed M5, balance panel fixed M7.
- [ ] Backup-gated purge flow works: button "Download backup, then purge" → auto-download → unlock → purge logs backup filename → text "No undo inside app. Undo = load backup".
- [ ] P1 grep no market, no-network grep 0 fetch/XHR, one-gate grep.
- [ ] Byte-diff vs baseline v3.6.3 shows only intended hunks (provenance panel, balance panel, live stars, plain language).
- [ ] Test suites: smoke 49, R8 13, R9 7, R10 12, R11 18, scope 43, hold 9, parity 7, legacy 156 + new current-form + league-pivot suites, all pass, lineage map M18 mapped 167 historic onto today's.

*Architectural build after structural S0-S6 locks — human-first, smooth English, icons with context, app alive via per-team live + per-league pivot + current form gated.*
