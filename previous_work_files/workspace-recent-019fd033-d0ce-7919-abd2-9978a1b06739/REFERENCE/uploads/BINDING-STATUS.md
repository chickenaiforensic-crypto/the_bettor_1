# BINDING-STATUS — which documents bind this build

**Rule (from WO §0):** *"This document is self-contained. You do not need to know anything that is not written here or in the binding documents listed in §2. If anything here conflicts with a binding document, stop and ask — never silently pick one."*

**Rule (from handoff README):** binding documents *must be read before coding; conflicts → stop and ask*.

## What was received (2026-08-02)

| # | Document | Role | Present? | Consequence |
|---|----------|------|----------|-------------|
| 1 | `WORKORDER-PITCH-RATING-REBUILD.md` | Master work order | ✅ | Canonical spec for the whole build |
| 2 | `README.md` (handoff) | Bundle map | ✅ | Describes the intended bundle; not normative for architecture |
| 3 | `LIVE-BLUEPRINT.md` | Evidence doctrine, no-fabrication rules, known defects not to regress | ❌ absent | WO §0.2 says read it; absent from bundle → **pending owner ruling (Q1)** |
| 4 | `COMMUNICATION-RULES-v1.md` | Working conduct (audit before editing; never assert without proof) | ❌ absent | Same as above |
| 5 | `ZONES.md` | Decision/changelog record | ❌ absent (fresh created as `trail/ZONES.md` v0) | Recreated fresh; the old log is lost with the bundle — noted as a loss in ZONES v0 |
| 6 | `CALIBRATION-2..13.md` | Replay method; ship discipline; failed candidates | ❌ absent | WO §2 references `CALIBRATION-7.md` fitting conventions and CAL9/EVG2 artifact tables — absent → **DC fit conventions cannot be pinned from source** (see GAPS.md) |
| 7 | `INTEGRITY-AUDIT.md` + `SLATE-2026-08-01-03.md` | Mute/settlement discipline | ❌ absent | Frozen-settlement discipline honored per WO §9 text; slate numbers themselves are lost with the bundle |
| 8 | `app-v2.6-cross.html` | Golden reference for Annex C; port source (fitted parameters) | ❌ absent | No legacy app → no port source, no behaviour-matrix capture from the old app (see GAPS.md) |
| 9 | `ENGINE_SPEC.md` | Dixon-Coles layer order/fitting/provenance/refusals | ❌ absent (README §5 says owner must add) | WO §2: port-only fallback applies until it arrives |
| 10 | 6 canonical packs + `WORKORDER-MLS.md` | Seed corpus + MLS round-2 order | ❌ absent | Store must be seeded another way or wait (see GAPS.md) |
| 11 | `smoke_test.js` + 13 harnesses | Test idiom to extend | ❌ absent | Idiom is preserved (node + vm + DOM stub, no browser); suite rebuilt fresh |

## Standing rule while gaps are open

- The **master work order is the single normative document** for architecture and gates. Where it is silent and a binding doc would have spoken, the item is logged in `GAPS.md` and surfaced at the phase gate, never silently assumed.
- Any document that arrives later **overrides the gap-fallback** retroactively, and the difference is recorded in ZONES.md, not papered over.
- `docs/WORKORDER-PITCH-RATING-REBUILD.md` is a **canonical copy**; if the owner ships an updated WO, the old copy is archived under `reference/` and the new one becomes canonical (ZONES entry required).
