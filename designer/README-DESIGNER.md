# DESIGNER — Cold Start Space for Lead Designer (Executive High-End)
# For Lead Designer — Executive High-End High-Budget Design (Cold Start Free Reign)

Copy-paste this brief to Lead Designer:

---
Subject: Lead Designer Brief — Executive High-End Design — Pitch Rating Zero-Market Engine — Branch arena/019fd213-the-bettor-1

Hi [Name],

You are Lead Designer — executive, high-end, high-budget — free reign to create something professional.

**Context (why this exists):**

We are building a zero-market football prediction engine — results only, no odds ever, zero market influence. One store of 5,082 verified real results (England 1,900, Czech 1,603, Russia 1,579 — 0 dup, 0 future, 609 teams, every row checked vs RSSSF archives, pins EXACT) + pending new leagues Italy 1,901, Germany 1,540, France 1,686 + UEFA connector 1,390 European rows (690 UCL 437 UEL 264 UECL). All verified fresh, no trust.

Engine: per-team live ratings that go up/down when results come in (app alive) + per-league pivot points that bump one league X points above another based on real Euro head-to-heads (so cross-league predictions are real-world accurate) + current form weighted inclusion via minimum playoffs evaluation (if team hot, gated).

Current app v3.7.0 (B0 ACCEPTED v3.7.0 md5 e688eee2...) is functional but poor content quality — AI-styled, scattered contents, random explanations jumbling all over surface, machine strings leak into main UI (predictFitted, λ_h 1.84, Brier 0.5675, DC ρ-0.06, ELO 1567), no provenance, form stars null, calibration stale, no balance panel, coverage undefined. Owner: "quality of presentation and general functionality is poor — so AI instead of human-friendly."

We built a basic wireframe prototype `prototype-human-friendly.html` — it's very basic, just to show main display points — no comment needed on it — it's not the design, it's the requirements sketch.

**Your task: Give free reign to create professional high-end high-budget executive design.**

**Main Display Points (what must be shown — you decide how):**

1. **Match Tab Daily Use:**
   - Team picker searchable, tolerant spelling (Nott'm Forest apostrophe, Slovacko accent), grouped by league flag, shows country, shows 6-game form WWWLWD inline + icons.
   - Primary CTA Predict (large, obvious) + Swap.
   - Verdict Card after Predict:
     - Main sentence bold 20-24px: "Arsenal 62% to win at home" — smooth English, not bot "H 62.3%".
     - Sub row: data window + calibration status: "Based on 960 games (2021-22..2024-25) — Calibrated: beat base 12.2% on last hidden season (254 games)" with icons 📅✅ and tooltip.
     - Tier: Fortress wins 78.5% (7,718 games) 🛡️ icon with tooltip.
     - Live rating trend 📈 ↑ up / 📉 ↓ down: "Live rating up after beating expectation last 3 games" — app is alive.
     - League pivot 🌍: "Premier League +0.20 above Czech (42 Euro meetings, bias 0.01)" — used in this cross-league tip.
     - Confidence: STRONG — won 78% of similar past tips (59 like this).
     - Current form ⚡ Hot / ❄️ Cold: "Last 6: W5 L1 GD +8 vs base +2.3 — tracked, not weighted yet (test +0.009 Brier worse, base only) or weighted 35% if adopted" — with icon.
     - Why not higher? Draw risk — same-tier gap, draw rate 24% (capped ±2%) 💡.
     - Actions: Save this tip 💾 primary.
     - Why this tip? collapsible plain English.
     - Technical details collapsible small-print 12px gray: λ_home 1.84 λ_away 0.92 scoreGrid Poisson×Poisson DC τ ρ-0.06 normalised H/D/A raw max cell ~13%, goalsGrid shrunk k=0.5 GMU2.6186 → O/U, draw correction draw_table[A|gap1] +0.015 proportional M4 cap ±0.02 never moves favourite, att +0.32 def -0.11 hfa Premier 0.28 home_extra +0.02, ELO 1567 ★★★★☆ (not prediction), points round(100×H_cal)=62 tier A+≥70 consensus STRONG 1.6 both ≥4H≥4A 78.6% vs 73% top10%, Brier DC 0.5675 vs base 0.6465 -12.2% n254 dir55.9% logloss0.957 window 2021-22..2024-25 replay 2026-08-05, provenance dc-fitted-model n=960 window... league-pivot s[ENG]=+0.12 s[CZE]=-0.08 n=42 bias0.01 date..., current-form α capped etc.

2. **Evidence Tab / NO CALL Honest Refusal (Valid UX):**
   - When not rated: "We can't rate this yet — honest. Reason: Sparta has only 4 home games (needs 6) — need more results."
   - Chain evidence: shared opponents, phase2/phase3 paths via, est, y0-y1, n, ctx + summary mean/sd/range/spread/oldest/newest/mixed_ctx + verdict USABLE/THIN/NOT USABLE/WEAK/STALE with why sentence.
   - Balance ⚖️: home/draw/away support shares bar chart 58%/18%/24% — "evidence split, we say NO CALL rather than guess."
   - No calibrated bridge yet: "need 20+ Euro ties, have 12 (UEFA connector in progress)" 🌍.

3. **Data Tab (4 Sub-Tabs: Files, Coverage, Requests, Country Packs):**
   - Files: drop zone plain English "Drop your result file here (.txt) — we check format, dates, scores, duplicates. Rejected files never saved — you'll see reason." Staged card Clean/Held Z-003/Rejected, Approve primary, View holds, Discard. Holds explanation: "20 cup ties have different tieIds — we keep rows verbatim, you approve keep verbatim (Z-003) — safe."
   - Coverage: honest inventory table League | Seasons | Games | Status pill complete/partial/requested | Gaps amber | Last update + small-country 156 purged backup kept, leftover GER2 WAL2 purged final 5,082 currently ~11,589 after new packs. Fix M14 coverage undefined.
   - Requests: one request for whole system D12, New central request button explains snapshots whole system writes one request file listing every league needing rows per team with date, downloads .json+.txt, logs event, tracks open→complete/partial→archived.
   - Country Packs: scope picker country (+ competition optional) → Preview counts matches/clubs/attached/comp breakdown before any action, Mute soft explanation "Exclude from every calculation, not deleted — Unmute restores. Nothing deleted by mute." vs Purge hard backup-gated button "Download backup, then purge" → auto-downloads full backup named pitch-rating-full-data-<date>-pre-purge-<scope>.json → unlocks "backup ready" → purge logs backup filename, text "There is no undo inside app. Undo = load backup you just downloaded."

4. **Calibration Tab:**
   - Explanation smooth: "Our model proves itself by hiding last season, retraining on earlier, predicting hidden."
   - Primary Run masked replay one-click after any data change + Run test-run ladder + Download artifact.
   - Last replay display: RPL trained 960 tested 254 hidden beat base 12.2% etc + ladder Last 1 100% (noise, not proof) Last 10 66.7% → Last FULL 55.9% stable real + artifacts dc-fitted-model, draw_table 27 cells, tiers, league-pivot ENG+0.12 CZE-0.08 n42 bias0.01 date.
   - Monthly sweep due date.

5. **Log & Settlement Tab:**
   - Settled tips 20 newest: saved % Home vs result WIN/LOSS — draw would be LOSS never push I5 rule explanation.
   - Every tip frozen at save — live may move later frozen never changes.
   - Audit trail 55 events travels every backup append-only provable.

6. **Integrity & Snapshots Tab:**
   - Muted rows flagged reason kept visible excluded every calc never deleted Restore reverses.
   - Snapshots before every commit + purge hash snapshots.
   - Integrity screen outcomes-only (no market P1) future M10 own-model collapse detection.

7. **Header:**
   - Logo Pitch Rating + version badge v3.7.0 → v3.8.0 S7 + store census 5,082 matches · 609 teams + last replay 2026-08-05 ✅ 📅✅ + theme toggle ◐ + Backup 💾 primary.

8. **Icon System with Context (your free reign to style, but meaning fixed):**
   🛡️ Fortress = very strong at home — "Wins 78.5% at home when Fortress (7,718 past)"
   📈 ↑ = rating up — "Live rating up after beating expectation last 3"
   📉 ↓ = down
   ⚡ Hot = efficient lately — "Last 6: W5 L1 GD +8 vs base +2.3 — weighted 35% if adopted else tracked only"
   ❄️ Cold
   🌍 Pivot = league pivot X points above/below — "Premier League +0.20 above Czech (42 Euro head-to-heads, bias 0.01)"
   🔗 Chain = evidence paths — "Shared opponents: both played Shakhtar — 2 paths, spread 1.2 — usable"
   ⚖️ Balance = support shares — "Home 48% / Draw 22% / Away 30% — split, we say NO CALL"
   📅 Window = data window — "Based on 960 games 2021-22..2024-25"
   ✅ Calibrated = replay won — "Live model beat base 12.2% on last hidden season (254 games)"
   🚫 Withheld = BTTS withheld — "We don't show BTTS — calibration error 6.0% too high"
   💾 Backup = safety — "Backup before any purge — undo = load backup file"
   💡 Tip = insight — "Draw risk — same-tier gap, draw rate 24% (capped ±2%)"
   🔍 Provenance = source — "Source: live DC fit, window ..., n=..., Brier ..., date ..."

**Free Reign — High-End Executive:**

- You have free reign to create something professional — high-end, high-budget, executive — think Bloomberg Terminal meets Apple Human Interface + sports editorial (The Athletic, Opta) — not AI-generated bootstrap.
- Color: executive — deep navy / charcoal + accent emerald / gold, not primary blue. Light/dark theme AAA contrast. Typography: serious serif for verdict (e.g., Tiempos Headline) + sans for UI (Inter, SF Pro) — or your choice — must feel high-budget.
- Layout: max-width 720-900px centered, card system with subtle shadows, not flat. Progressive disclosure: summary → why → technical — user can stop after summary. Primary CTA obvious per tab, not 5 equal buttons. Empty states honest with illustration maybe — not blank.
- Interactions: smooth, not jarring — team picker searchable grouped league flag, swap animation, balance bar animated, calibration ladder table sortable.
- Performance: keep single HTML file <1.2MB for now (zero network I6), no external deps, localStorage pitch-rating-v3.store, theme toggle, keyboard nav, screen reader aria-labels, but your design system can propose future split into modules after S7 if needed.
- No market: no odds, no bookmaker references, no price.
- Provenance always small but present: every probability has source/window/n/cal/date M3 small-print.
- Honest refusal is first-class UX: NO CALL valid helpful with balance bar + reasons, not error.

**Constraints (non-negotiable doctrines where each lives):**

- Results-only no market P1 — ingest grammar no odds fields, engine no odds input, grep fetch/XHR/odds/price=0
- 90-min doctrine AET/pens 90' + NOTE advancement — gate integer-score check L887 note system
- Compute live or stay silent A-01 — footer truth sentence + LIVE-DERIVE-01 S1 gate, provenance panel M3, NO CALL valid
- No data abolition exclusion=MUTE purge backup-gated — Mute L2928 L3431 purge L2957 L3433-3451 L2988
- One gate rejections never stored — PR.ingest L709 L3478
- Dedupe add-if-new rows kept verbatim — L321/1016 L3458-3814
- D12 central request only — Requests tab
- Plain language A-02 — main smooth English, machine small-print bracketed
- Every claim provable — log in every backup + ZONES chain + provenance M3
- League pivot s[L] bump-up/calibrate — fit loop bias iteration 20-50 step0.05-0.1 artifact dc-fitted-league-pivot n/window/Brier/date
- Live per-team up/down app alive — L1 online gradient att/def up/down seen min6 P3
- Current form weighted inclusion gated — gate ≥6 recent or ≥3 playoff GD diff>0.5 α capped 0.15-0.35 blend (1-α)base+αrecent

**Deliverables from you (Lead Designer):**

- Design system: colors, typography, spacing, icon style (refined from emoji to custom SVG but keep meanings), component library (card, badge, pill, bar, button primary/secondary, drop zone, table ladder, balance bar).
- High-fidelity mockups: Match tab verdict card + NO CALL evidence, Data Files/Coverage/Requests/Country Packs, Calibration ladder, Log Settlement, Integrity Snapshots, Header — desktop + mobile.
- Figma link or HTML/CSS prototype (can be separate from single-file app — we will port your design into single-file app for audit: byte-diff vs baseline, P1/no-network/one-gate greps identical new module contributes 0, all 4 script blocks node --check OK, empty-store P3 refusals no crash — same gates as B0).
- Interaction notes: how team picker searchable grouped, how provenance collapsible small-print, how balance bar animates, how primary CTA obvious.
- Executive summary: why this design feels high-end high-budget, not AI-styled.

**Where to work:**

- Repo: chickenaiforensic-crypto/the_bettor_1
- Branch: arena/019fd213-the-bettor-1 (planner branch — contains all planning docs lead_engine/00-22 + audit_work/ + prototype-human-friendly.html basic sketch + builder/app-v3.7.0-b0.html baseline B0 ACCEPTED v3.7.0 md5 e688eee2...)
- Your space: create `designer/` folder or `design/` — put Figma exports, HTML prototypes, design tokens, README-DESIGNER.md
- Reference: `lead_engine/11-HUMAN-FRIENDLY-DELIVERY-SPEC.md` + `15-ARCHITECTURE-PROTOTYPE.md` + `17-ARCHITECTURAL-BUILD-PLAN-DETAILED.md` + `prototype-human-friendly.html` (basic wireframe showing main display points — your job is to make it executive)
- Current app baseline to redesign: `builder/app-v3.7.0-b0.html` (B0) — shows functional but poor presentation.

**What to do first:**

1. Read `START-HERE-COLD-START.md` (8 files, 45 min) + `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` v1.3 + `ENGINE-MASTERPLAN-2026-08-05.md` v1.1 §1-§10 + `FUNCTIONALITY-2026-08-05.md` + `lead_engine/11,15,17` + `prototype-human-friendly.html` — understand engine + current poor UI.
2. Audit current app v3.7.0: list every machine string leaking into main, missing provenance, missing balance, etc — produce UX audit 1-page.
3. Design system: propose high-end executive design tokens, free reign.
4. Mockups: high-fidelity for Match tab (verdict + NO CALL) + Data tab (Files/Coverage/Country Packs backup-gated flow) + Calibration ladder — show smooth English + icons with context tooltips + provenance small-print + balance bar.
5. Present: either Figma link + HTML prototype in `designer/` + README with rationale why high-end high-budget executive.

**Free reign means free reign:** Create something professional you'd show to an executive paying high budget — not bootstrap, not AI-generated scattered. Icon highlights can always provide context explanation, main display points must be shown as above but you decide how.

**Branch for your work:** You can work on your own arena branch (Arena auto-creates arena/<id>-the-bettor-1 per session) or directly on planner branch arena/019fd213-the-bettor-1 — if you create own branch, I will fetch and merge into planner like I did for Researcher1 019fc462 (ITA/GER/FRA) + Researcher2 019fd1a3 (UEFA 1390) + Builder 019fd227 (B0). Push your design to handoffs/ or designer/ and comment md5.

**Questions:** One direct question with file/line/pin — GitHub Issue on planner branch.

— Lead Planner (Arena AI) — branch arena/019fd213-the-bettor-1 — 2026-08-05

---
