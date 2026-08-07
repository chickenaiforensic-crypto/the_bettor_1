# Pitch Rating — Implementation Spec v1.0 (for the Builder)

**Designer:** Senior UI/UX Designer · **Date:** 2026-08-06
**Target file:** `builder/app-v3.17.0-picker.html` (md5 `d71b042308b0637a81d22ee75795f419`)
**Approach:** The app is a single self-contained HTML file with a replaceable CSS "skin layer" (its own header comment calls it "Phase 6/8; replaceable"). This spec therefore asks for **CSS-layer replacement + minimal HTML/JS touch** — functionality is untouched.

---

## 1. What to keep vs replace (CSS)

The `<style>` block spans lines 1–492 of the baseline. It already contains the design tokens and all component classes. **Keep the architecture, replace values/structure** per below.

### 1.1 KEEP (do not delete)
- All **class names and HTML structure** produced by the JS renderers (`topbar`, `card`, `pbar`, `bal-row`, `nocall`, `provenance`, `ladder-tbl`, `scope-*`, `cov-row`, `chip`, `pill`, `sec`, `secrow`, `console-*`, `tabs`, `tab`, `dropzone`, `staged`, `hold-list`, `settlement-*`, `integrity-*`, `toast`, etc.). The JS outputs these exact strings — renaming them breaks rendering.
- The `@media` stacking rules for the v3.17 picker (search+filter abreast, home+away abreast, swap icon) — these already match the design (stacking ≤600px, swap full-width).
- The `:focus-visible` rule (a11y).
- The `@keyframes spin` and `.busy-icon`.

### 1.2 REPLACE / REWRITE
- The **token block**: replace the `:root{...}` and `html[data-theme="light"]{...}` blocks with the consolidated token set in §2 below. This removes the duplicated families (`--ink-950/-900/-800/-700/-600`, `--emerald`, `--gold`, `--teal`, `--silver`, `--mist`, `--charcoal`, `--slate`, `--surface`, `--paper`) into the one family in the design system. Components still work because the **shared names (`--bg --panel --panel2 --line --line2 --ink --ink2 --muted --dim --accent --accent2 --amber --red --h --d --a --radius --shadow --font-display --font-body --font-mono --max-width`)** are retained with the same names; the new tokens (`--surface-1`, `--line-strong`, `--accent-tint`, etc.) are **additive**.
- **Buttons:** upgrade `.btn` base + variants to the design spec (hover bg `--panel-hover`, active 1px press, disabled `opacity .45 + grayscale`). Keep `.btn-primary/.btn.ghost/.btn.danger/.btn.small/.btn.swap-icon` class names.
- **Inputs/selects/search:** upgrade `.field`-equivalent (`input.search`, `.fld select`) to the spec (focus = accent border + `--accent-tint` ring; error state `.err`; custom select chevron; disabled/read-only).
- **Pills/badges:** align `.pill`, `.pill-accent/.muted/.warn`, `.chip`, `.badge/.badge-emerald/.badge-gold` to design-system tokens.
- **Cards/tables:** `.card` to `--shadow-2` + `--r-lg`; add `.tbl` table styles (right-aligned numeric, hover row, `tr.full` highlight) for `ladder-tbl`.
- **Alerts/provenance/toast:** add the `.alert` (info/ok/warn/err) styles; restyle `.provenance`/`.provenance-panel` into the consistent small-print component; style `.toast`.
- **Empty/loading:** add `.empty` and `.loading`+`.spin` component styles and wire them into existing empty renders.

---

## 2. CSS variables to add (additive, in `:root` and `html[data-theme="light"]`)

```css
/* ADD in both themes (values swap per theme) */
--surface-0; --surface-1; --surface-2; --surface-3; --surface-4;  /* bg elevations */
--panel-hover;            /* hover surface */
--line-faint;             /* table hairlines */
--accent-strong; --accent-deep; --accent-ink; --accent-tint;
--warning; --warning-strong; --warning-ink; --warning-tint;
--danger;  --danger-strong;  --danger-ink;  --danger-tint;
--info;    --info-strong;    --info-ink;    --info-tint;
--home; --home-tint; --draw; --draw-tint; --away; --away-tint;   /* outcome colors */
--sp-1..--sp-16;          /* 4px spacing scale */
--r-xs; --r-sm; --r-md; --r-lg; --r-pill;   /* radius scale */
--shadow-1; --shadow-2; --shadow-3;         /* elevation scale */
```

**Contract:** existing shared names (`--panel --panel2 --line --line2 --ink --ink2 --muted --dim --accent --accent2 --amber --red --h --d --a --radius --shadow --max-width --font-*`) are retained and aliased to the new family so no JS/HTML change is required for them to resolve.

---

## 3. Component HTML structure (changes are minimal)

No functional restructuring. Recommended structural additions that help visual polish and cost nothing functionally:
- Wrap the ladder/saved-rows tables in `<div class="tbl-wrap">` so they scroll on mobile.
- Give section headings a stable `.sec h3` + `.cap` (already exists) — keep.
- Provenance blocks: keep existing `.provenance` / `.provenance-panel` / `.provenance-row` markup; add the "Technical details" `<b>` label in the provenance panel renderer (JS) for clarity.
- Icon glyphs: the JS `ic()` helper returns emoji (`🟢🟡🚫💾📄`). Replace with inline SVG paths that inherit `currentColor`. See §5 for the one-JS-file change.

---

## 4. JavaScript UI behavior changes (minimal — visual only)

1. **Icon set (optional but recommended):** change the `ic(kind)` helper (single function) to return a small SVG sprite (16px, `stroke="currentColor"`, 1.75–2px) instead of emoji. One function, zero other JS change. Fallback: keep emoji if timing is tight — **compliance-neutral**.
2. **Reduced motion:** add a `prefers-reduced-motion` media query that disables the bar/meter width transitions and spin (small CSS-only).
3. **Theme:** keep existing `data-theme` toggle. No change.
4. **Toast:** keep existing `.toast`/`.out` mechanism; restyle only.

Everything else (compute, NO CALL, balance panel, settlement, integrity, snapshots, purge gating, one-gate ingest) is **engine behavior and must not change.**

---

## 5. Compliance flags for the builder (verify against final build)

- **A-02 plain language:** audit all rendered strings for AI-style confidence phrasing. Replace e.g. "confidence score: 0.78 AI-predicted likelihood" → "Home win probability: 55.9%". Machine strings live only in `.provenance` small-print. **No `@keyframes` of the A-02 gate: keep all provenance visible.**
- **P1 (no market data):** the baseline renders a **`markets` block** with labels **"Double chance 1X/12/X2"**, **"Draw no bet — home"**, plus Over-goals rows. These are betting-market **terminology**. Recommended: **relabel** as outcome language ("Win-or-draw (home)", "Either side", "No-draw — home", "Expected goals over 1.5/2.5") **or withhold the block** until the auditor clears it. No odds/prices/spreads/lines/implied-probability/vig/juice/margin values are shown — the P1 data rule holds; this is a **terminology** correction. Flag in the deliverable note.
- **P3 (honest refusal):** NO CALL must stay visually distinct (icon + heading + refusal chips) and the balance panel must always render below it (M7). Do not dim or hide the balance panel.
- **M3 provenance:** every probability/prediction shows Source · Window · n · Calibration in `.provenance`. Keep on all fitted and evidence cards.
- **M7 balance panel:** required on every NO CALL. Already wired (`card()` injects `balanceHtml` even when `!res.ok`); keep.

---

## 6. Responsive breakpoints (already largely present — confirm)

| Range | Behaviour | Verify |
|---|---|---|
| ≥1024 | Two-column picker+stage; picker sticky | default |
| 768–1023 | Single column; picker static | existing `@media(max-width:900px)` |
| ≤767 | Search+filter stack, home+away stack, swap full-width; tabs scroll; touch targets ≥40px | existing `@media(max-width:600px)`; add tab horizontal scroll |

Add: `@media(max-width:900px){ .teams{flex-direction:column} }` so the verdict head stacks the fixture names on tablet/mobile.

---

## 7. Design-system mapping (acceptance)

After implementing, the app should visually match `DESIGN-SYSTEM-v1.0.html` on these checks:
- [ ] Token block consolidated (no duplicate families) in both themes.
- [ ] Buttons: 6 variants + 4 states render per spec.
- [ ] Inputs/selects/search: focus + error + disabled + read-only states.
- [ ] Tabs active underline + optional badge count.
- [ ] Pills/badges/chips: tier, consensus, capability, coverage.
- [ ] Probability split + balance bars + confidence meter + stars + form strip.
- [ ] `.provenance` small-print on every number.
- [ ] NO CALL distinct + balance panel present (M7).
- [ ] Alerts (info/ok/warn/err), empty, loading, error states.
- [ ] Tables scroll + highlight.
- [ ] Both themes render; no hardcoded hex outside tokens.
- [ ] Responsive: desktop/tablet/mobile.

*End of Implementation Spec v1.0.*
