# HANDOFF BUNDLE — Pitch Rating rebuild (2026-08-02)

Give this entire folder to the engineer as one zip. Reading order and everything else
is inside the master document.

## 1 · MASTER DOCUMENT (start here)
- `WORKORDER-PITCH-RATING-REBUILD.md` — the complete work order: doctrine, data tree,
  decision register, phases+ gates P0–P8, hand-back/audit protocol, non-negotiables,
  Annex A researcher brief, Annex B grammar, Annex C golden fixtures, Annex D migration,
  Annex E glossary, Annex F data operations.

## 2 · BINDING DOCUMENTS (must be read before coding; conflicts → stop and ask)
- `LIVE-BLUEPRINT.md` — evidence doctrine + no-fabrication rules.
- `COMMUNICATION-RULES-v1.md` — working conduct.

## 3 · REFERENCE (`reference/`)
- `ZONES.md` — the decision/scar log (append-only).
- `CALIBRATION-2..13.md` — replay method; ship discipline; failed candidates.
- `INTEGRITY-AUDIT.md`, `SLATE-2026-08-01-03.md` — mute channel + settlement freeze discipline.
- `app-v2.6-cross.html` — the CURRENT app: golden reference for the behaviour matrix (Annex C)
  and port source. Untouched legacy; never edit it.

## 4 · DATA (`packs/` + harness `harness/`)
- 6 canonical packs (russian · czech · hibernian · malisheva · malisheva-closure · usa) —
  seed corpus for the unified store and the golden fixtures.
- `smoke_test.js` + 13 audit/replay harnesses — the test idiom to extend (node + vm, no browser).
- `WORKORDER-MLS.md` — open round-2 data order (relevant to Annex A's MLS row; do not duplicate).

## 5 · MISSING — OWNER MUST ADD BEFORE HANDOVER (currently absent from this bundle)
1. **`ENGINE_SPEC.md`** — required for Phase 2 Dixon-Coles fit work (WO §2). If it cannot be
   supplied, the owner must state in writing that the port-only fallback in WO §2 applies.
2. **`Southampton_BP-TEAM-PACK_v2.txt`** and **`Ross-County_St-Johnstone_BP-TEAM-PACK_v2.txt`** —
   the two already-researched packs the merger audit reported as delivered; Phase 3 must load
   them or document why not.
3. **Owner's live store export** (`pitch-rating-full` JSON from the current app's Data tab) —
   Phase 1's migration gate requires the real store (rows + log), not a synthetic stand-in.
Drop these into this folder when available; mark the bundle version and date here: ______.

## Superseded / do not hand over
`uploads/PITCH-RATING-MERGER-WORK-ORDER.md` (superseded by the rebuild WO — context only),
`COVERAGE-PLAN.md` (strategy note), `WORKORDER-BRAZIL.md` (separate researcher-side order
under the same Annex-A discipline), older app files (`app-v2.5-final.html`, `match-audit-tool.html`).
EOF
echo bundeled && ls HANDOFF | wc -l