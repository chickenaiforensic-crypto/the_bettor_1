# Pitch Rating — Screen Designs v1.0

**Designer:** Senior UI/UX Designer · **Date:** 2026-08-06 · Visuals in `DESIGN-SYSTEM-v1.0.html` (§ Screens). This file specifies layout, component styling, typography, spacing and interactive states per screen.

---

## 1. Match view (verdict card)

**Layout (top → bottom):**
1. Fixture head — league overline, home **vs** away (serif display, 22–24px).
2. Evidence path line — capability pill + path label + reasons.
3. Provenance small-print — `.provenance` "Technical details" (Source · Window · n · Calibration).
4. Sections stack — Probability split → Team strength (stars) → Recent form (W/D/L strip) → Evidence paths → optional cross/goals/graph.
5. Balance panel (support shares).
6. Confidence line (tier pill + meter + number + provenance).
7. Card foot — primary "Save this row" + helper note.

**Typography:** teams serif 22px/700; section headings 11.5px overline `--muted`; values tabular-nums; tier pills uppercase 11px.

**Spacing:** 14px vertical rhythm between sections; 24px card padding.

**Interactive:** each section may expand (graph details); Save button `btn-primary`.

**Provenance (M3):** the `.provenance` block and the confidence line's inline provenance are always present on every fitted/evidence result.

---

## 2. NO CALL view (honest refusal — P3 + M7)

**Layout:**
1. Fixture head (same as Match).
2. `.nocall` block — icon tile (🚫), "No view yet" (serif 21px), one-line plain explanation, and refusal **chips** (`.refusal`) — one per reason, readable, not tiny dim text.
3. **Balance panel always shown below** (M7) — "Balance — support shares (honest no-view state)" with Home-form / Draw / Away-form bars and a `.support-note` explaining it is form-based, not a prediction.
4. Confidence line — `NO CALL` muted pill + "no strength — no data" + sublabel.

**Non-negotiables:** the balance panel is required, never hidden, never optional. The NO CALL state must be visually distinct from a valid verdict (icon + centered heading + chips) — it must not be mistaken for a prediction.

---

## 3. Data view

**Console tabs:** Files / Coverage / Requests / Country packs.
- **Files:** file drop zone (dashed, highlights `--accent` when hovering), accepted-file alert, staged cards, held cards list (amber), replay report.
- **Coverage:** coverage chips per league (status glyph + name) + match counts.
- **Requests:** open requests list.
- **Country packs (scope):** country list with A–Z `details` accordions → per-competition open; preview shows the FULL scrollable row list; confirmation requires a backup download before any clear (`.btn-danger`, disabled until backup confirmed).

**States:** empty (no countries yet), loading (during file ingest), error (invalid file alert).

---

## 4. Calibration view

- Info alert explaining masked replay (plain language).
- Primary actions: "Run masked replay", "Run test-run ladder", ghost "Download ladder artifact (JSON)".
- Test-run ladder table (`.tbl`): Step / Brier 1X2 / Log loss / n / Direction / MDE. Highlighted `tr.full` = full season.
- Artifacts list with green status + kind + version + date.
- Success alert on parity self-check pass.

---

## 5. Log & Settlement view

- Rule alert (warning) — "Draw is a loss for a home-win call — never a push."
- Settlement entry form — Home team · goals input · : · goals input · Away team · Save result (`.btn-primary`). Venue is locked; official-list tick-box enables save (I4).
- Saved-rows table: Fixture / Date / Home / Away / Outcome pill (Home win · Draw-loss).
- Empty state: "Nothing settled yet" + how it works.

---

## 6. Integrity & Snapshots view

- Integrity flag alerts (danger for Brier shock, warning for caution, info for guidance) — plain language + technical small-print.
- Muted rows list — status glyph + fixture + reason + Restore button.
- Snapshots list — summary + timestamp + Restore.
- Empty states for each list.

**P1 note:** this screen is outcomes-only. The spec must NOT reintroduce any market-price screen; legacy market-gate flags stay inert/dropped.

---

## 7. Empty / loading / error states

| State | Component | Where |
|---|---|---|
| No fixture selected | `.empty` "Select a fixture" | Match view |
| No data yet | topbar status dot grey + "No data yet" | Topbar |
| During compute | `.loading` spinner "Computing from the data you have loaded…" | Any compute |
| Ingest in progress | `.loading` in Files | Data view |
| Invalid file / compute failure | `.alert.err` with message | Data / Match |
| No countries | `.dim` "No countries yet…" | Data → Country packs |
| No muted rows / snapshots | `.dim` guidance | Integrity |

All empty states pair an icon tile, a serif heading, one supporting line, and (where relevant) a primary action.

*End of Screen Designs v1.0.*
