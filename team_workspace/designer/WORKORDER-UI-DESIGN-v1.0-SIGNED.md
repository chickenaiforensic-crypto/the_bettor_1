# WORKORDER-UI-DESIGN-v1.0 — ACKNOWLEDGMENT & EXECUTIVE SUMMARY

**Designer:** Senior UI/UX Designer (cold-started, Arena Agent Mode)
**Date:** 2026-08-06
**Workorder:** WORKORDER-UI-DESIGN-v1.0 (Director of Intelligence, HIGH priority)
**Baseline audited:** `builder/app-v3.17.0-picker.html` — md5 `d71b042308b0637a81d22ee75795f419` (742,281 bytes) — matches the pin in §1.1.

---

## 0.1 Confirmation of Reading

I, **Senior UI/UX Designer**, confirm I have read this ENTIRE workorder before starting.

Signature: ____Senior UI/UX Designer____   Date: ___2026-08-06___

## 0.2 The "Never" List for Designers (verified)

- [x] I will NOT hide machine provenance behind "AI-style" confidence language (A-02).
- [x] I will NOT use market data, odds, or prices in any visual element (P1).
- [x] I will NOT design a UI that forces a prediction when the system should say "I don't know" (P3).
- [x] I will NOT remove or hide provenance information from the UI.
- [x] I will NOT make the balance panel optional or hidden on NO CALL (M7).

## 7. Compliance Acknowledgment

I, **Senior UI/UX Designer**, acknowledge:
1. I have read this ENTIRE workorder.
2. I understand A-02: plain language, no AI-style confidence.
3. I understand P1: no market data in any visual element.
4. I understand P3: "I don't know" must be a clear visible output.
5. I understand M3: provenance must be visible on every number.
6. I understand M7: balance panel must show on every NO CALL.
7. I will NOT remove or hide provenance or balance panel.
8. I will design the existing UI, not rebuild functionality.
9. I will deliver a design system + screen designs + implementation spec.

Designer signature: ____Senior UI/UX Designer____   Date: ___2026-08-06___

---

## Audit highlights (Step 1 — done)

The baseline is a working, functional single-file app. Visual polish gaps found:

1. **Design-token sprawl** — three overlapping variable families (`:root` semantic + `--ink-9xx` scale + `--emerald/--gold` dups) create inconsistent greys/accents; components drift (mixed `#06120b` button text, `color-mix` fallbacks everywhere).
2. **Emoji-as-icon** (`ic()`, `🟢🟡🚫💾📄`) — inconsistent weight, OS-dependent, no states. Should be replaced with an SVG sprite set in the design spec.
3. **NO CALL** is functionally correct (distinct `🚫` heading, refusal list, balance panel always injected via M7) but visually under-styled — the refusal reasons are tiny `dim` paragraphs.
4. **Provenance** appears as small-print dashed boxes — good for compliance, needs a consistent "technical details" component style.
5. **Responsive** — picker stacks below 600px, main grid below 900px; tabs wrap. Needs explicit mobile menu handling and better touch targets (the spec documents this).
6. **States** — hover/focus exist; disabled and error states are inconsistent; no dedicated empty-state art for several views.
7. **`markets` block** — renders Double-chance / Draw-no-bet labels. These are betting-market **terminology** and are P1-adjacent. Flagged for builder to relabel or withhold (see IMPLEMENTATION-SPEC §Compliance flags). No odds/price values are shown, so P1 data rule is intact; only the terms are at risk.

## Deliverables (in this folder)

| File | What it is |
|---|---|
| `DESIGN-SYSTEM-v1.0.html` | Self-contained design system + component library + screen designs, dark & light, interactive. THE builder-facing visual spec. |
| `IMPLEMENTATION-SPEC-v1.0.md` | Written implementation spec: exact CSS var changes, keep/replace list, HTML structure, JS behavior, responsive breakpoints, empty/loading/error states, compliance flags. |
| `DESIGN-SYSTEM-v1.0.md` | Text version of the design system (color/type/spacing/component/states) for reference & PDF export. |
| `SCREEN-DESIGNS-v1.0.md` | Per-screen design notes (layout, component styling, typography, spacing, interactive states) + empty/loading/error. |
| `index.html` | A one-page gateway linking the above for UAT convenience. |

*End of acknowledgment — work follows.*
