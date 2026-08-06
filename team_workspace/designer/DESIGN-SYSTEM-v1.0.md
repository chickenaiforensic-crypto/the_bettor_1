# Pitch Rating — Design System v1.0 (text reference)

**Designer:** Senior UI/UX Designer · **Date:** 2026-08-06 · **Baseline:** `app-v3.17.0-picker.html` (md5 `d71b042308b0637a81d22ee75795f419`)

Companion to the interactive visual spec `DESIGN-SYSTEM-v1.0.html`. This is the text version for reference / PDF export. Token names are the implementation contract.

---

## 1. Color palette

### Brand — emerald core (unchanged identity, refined)

| Token | Dark | Light | Use |
|---|---|---|---|
| `--accent` | `#10b981` | `#047857` | Primary action, active tab, links |
| `--accent-strong` | `#34d399` | `#0f8a63` | Hover emphasis |
| `--accent-deep` | `#047857` | `#065f46` | Gradients, deep accents |
| `--accent-ink` | `#06120b` | `#ffffff` | Text on accent fills |
| `--accent-tint` | 14% emerald mix | `#e0f5ec` | Chips, fills, focus ring |

### Semantic

| Token | Dark | Light | Use |
|---|---|---|---|
| `--warning` | `#c8a84d` | `#8a6e1f` | Partial, caution, draw |
| `--danger` | `#f87171` | `#c0392b` | Errors, away, hard blocks |
| `--info` | `#7aa2f7` | `#2f5fd0` | Neutral guidance, snapshots |
| `--home` | `#10b981` | `#047857` | Home outcome (emerald) |
| `--draw` | `#c8a84d` | `#8a6e1f` | Draw outcome (gold) |
| `--away` | `#f87171` | `#c0392b` | Away outcome (coral) |

### Neutrals

| Token | Dark | Light | Use |
|---|---|---|---|
| `--surface-0` | `#0a0f1a` | `#fbfcfe` | Deepest bg |
| `--surface-1` | `#0e1526` | `#ffffff` | Card surface |
| `--surface-2` | `#131b33` | `#f4f6fb` | Secondary surface |
| `--surface-3` | `#1a2545` | `#eef1f6` | Hover / inset |
| `--line` | 8% white | `#e3e6ea` | Hairlines |
| `--line-strong` | 14% white | `#c9cfd8` | Borders, inputs |
| `--ink` | `#f0f2f8` | `#0a0f1a` | Primary text |
| `--ink-2` | `#b8bdd0` | `#2d384f` | Secondary text |
| `--muted` | `#8a93ab` | `#5b6575` | Captions, labels |
| `--dim` | `#6b7a99` | `#8a93a4` | Disabled, small print |

---

## 2. Typography scale

`--font-display` = "Tiempos Headline", Georgia, serif (editorial voice). `--font-body` = Inter. `--font-mono` = SF Mono for numbers/technical small-print.

| Name | Family | Size | Weight | Spacing | Use |
|---|---|---|---|---|---|
| Display | serif | 34px | 700 | -2% | Verdict headline |
| H1 | serif | 24px | 700 | -1% | Screen title |
| H2 | serif | 20px | 700 | 0 | Card title |
| H3 | sans | 15px | 700 | 0 | Section heading |
| Body | sans | 15px | 400 | 0 | Base text |
| Small | sans | 13px | 400 | 0 | Descriptions |
| Caption/overline | sans | 11px | 700 | +8% up | Overlines, labels |
| Mono | mono | 12px | 400 | tabular-nums | Technical small-print, provenance |

**Rule:** all figures set `font-variant-numeric: tabular-nums`.

---

## 3. Spacing & radius

4px base grid: `--sp-1 4 / --sp-2 8 / --sp-3 12 / --sp-4 16 / --sp-5 20 / --sp-6 24 / --sp-8 32 / --sp-10 40 / --sp-12 48 / --sp-16 64`.

Radius: `--r-xs 6 / --r-sm 10 / --r-md 14 / --r-lg 20 / --r-pill 999`.

Elevation: `--shadow-1` resting, `--shadow-2` card, `--shadow-3` elevated/toast.

---

## 4. Component library (states)

See interactive spec for renders. Summary:

- **Buttons:** `btn` (default), `btn-primary`, `btn-ghost`, `btn-danger`, `btn-small`, `btn-icon` (swap ⇅, pill on desktop / full-width on mobile). States: default, hover, focus (accent ring), active (1px press), disabled (dim + `not-allowed`).
- **Inputs/selects/search:** `.field`. Focus = accent border + `--accent-tint` ring; error = `--danger` border + tint ring + `.field-err` message; read-only = dashed; disabled = dim. Selects get a custom chevron.
- **Tabs:** `.tab` / `.tabs`. Active = accent 2px underline + accent text; optional `.badge-dot` count.
- **Pills/badges/chips:** `.pill` (with `-accent/-warn/-danger/-muted/-info`), `.badge` (`-emerald/-gold`), `.chip`.
- **Cards:** `.card` (panel bg, `--shadow-2`, `--r-lg`).
- **Tables:** `.tbl` in `.tbl-wrap` (horizontal scroll). Right-aligned `.num` cells, tabular-nums, hover row, `tr.full` highlighted.
- **Alerts:** `.alert` with `info/ok/warn/err` variants + icon.
- **Provenance:** `.provenance` small-print dashed panel — shown on every number.
- **Data viz:** `.pbar` + `.bar-seg` (H/D/A), `.bal-row/.balbar/.bal-fill`, `.meter/.meter-fill`, `.stars`, `.frm` (W/D/L strip).
- **Empty/loading/error:** `.empty`, `.loading` + `.spin`, `.alert.err`.

---

## 5. Dark + light theme specification

Both themes share the same token names; only values change via `html[data-theme="light"]`. Dark = navy gradient bg, translucent panels, high-contrast text. Light = soft off-white surface, white cards, ink text. Focus rings, outcome colors, and semantic tints all remap automatically because components consume tokens, never hardcoded hex.

*End of Design System v1.0.*
