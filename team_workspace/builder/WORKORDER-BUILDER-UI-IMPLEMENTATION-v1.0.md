# WORK ORDER — Builder: UI Implementation v1.0

**Document ID:** `WORKORDER-BUILDER-UI-IMPLEMENTATION-v1.0`
**Issued:** 2026-08-07
**Status:** READY FOR OWNER TO SEND
**Scope:** Implement the approved visual handoff only. Do not rebuild or alter the engine.

## 1. Mandatory reading

Read these files fully before changing code:

1. `COMMUNICATION-RULES-v1.md`
2. `START-HERE-COLD-START.md`
3. `README.md`
4. `Supervior/ROLES/ROLE-BUILDER.md`
5. `team_workspace/builder/WORKORDER-BUILDER-MASTER-v1.md`
6. `team_workspace/designer/DESIGN-HANDOFF-INDEX-v1.1.html`
7. `team_workspace/designer/DESIGN-HANDOFF-REBASE-v1.1.md`
8. `team_workspace/designer/IMPLEMENTATION-SPEC-v1.0.md`
9. This workorder

Reply first with the exact baseline MD5, the files you will change, and confirmation that engine logic will remain untouched.

## 2. Exact baseline

Use only this approved engine as the input:

```text
builder/app-v3.17.0-picker.html
MD5: e6687ad417fd1d3229a000c12f73f1a3
SHA-256: 51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7
```

The designer’s historical `d71...` baseline is not the input for this build.

## 3. What you may change

You may change only the presentation layer needed to implement the design package:

- CSS tokens, component styling, dark/light theme styling, spacing, type, responsive layout, states, and accessible focus treatment.
- UI markup needed for styling: table wrappers, provenance label, empty/loading/error visual containers.
- The icon helper only, if replaced by local inline SVG using `currentColor`.
- User-facing presentation wiring required to withhold the Markets section.

Use no external libraries, fonts, images, scripts, API calls, or network requests.

## 4. What you must not change

Do not change:

- prediction calculations, model constants, parity targets, calibration logic, or derived data;
- `PR.ingest`, validation, source grammar, backups, scope purge, settlement logic, venue guard, mute logic, or data records;
- `SEED_PACKS`, sources, or stored results;
- the mandatory NO CALL balance panel, visible provenance, or draw-as-loss settlement rule.

If a visual requirement appears to require a logic change, stop and write a blocker. Do not improvise.

## 5. P1 visual correction

The user-facing Markets section currently displays betting-style terms such as:

```text
Double chance
Draw no bet
Home −1 handicap
```

Do not relabel these and do not display them. Withhold the entire user-facing Markets section from the rendered verdict UI.

This is a UI-only change:

- do not alter the underlying calculation or calibration code;
- do not add odds, prices, bookmaker material, or new market terminology;
- prove in the evidence that `marketsBlock()` is not rendered from the verdict card and that the prohibited labels are absent from the rendered view.

## 6. Required visual implementation

Implement the designer’s v1.0 specification against the corrected baseline:

- consolidated tokens in both themes, retaining existing variable aliases where UI code needs them;
- button, input, select, tab, chip, pill, card, table, alert, provenance, toast, empty/loading/error states;
- responsive picker, tabs, verdict head, and table scroll behavior;
- clear NO CALL refusal chips with its balance panel always visible;
- visible provenance on every fitted/evidence number;
- local SVG icons or the existing icon fallback; no external assets;
- reduced-motion support.

## 7. Required output

Create versioned files only:

```text
builder/app-v3.18.0-ui-design.html
handoffs/BUILDER-UI-IMPLEMENTATION-v3.18.0-<md5>.b64.txt
handoffs/BUILDER-UI-EVIDENCE-v3.18.0.md
handoffs/BUILDER-UI-EVIDENCE-v3.18.0.json
audit_work/audit_v3_18_ui_design-v1.0.py
Supervior/Build Docs/BUILDER-UI-IMPLEMENTATION-v3.18.0.md
Supervior/updates/SESSION-2026-08-07-UI-IMPLEMENTATION-v1.0.md
```

## 8. Acceptance gates

Your evidence must show:

1. Input baseline hash matches section 2 before editing.
2. New app hash, SHA-256, and size are recorded.
3. No network calls: zero `fetch`, `XMLHttpRequest`, and `$.ajax`.
4. No P1 prohibited display terms in the rendered verdict UI.
5. Markets section withheld while all engine modules and `PARITY_EXPECTED` remain present and unchanged.
6. `PR.ingest` remains the single data gate.
7. NO CALL remains distinct and always contains the balance panel.
8. Provenance remains visible on every fitted/evidence result.
9. Light and dark themes, desktop/tablet/mobile layouts, and keyboard focus work.
10. A new regression audit script proves the unchanged parity target object and reports no logic/data diff outside the allowed UI locations.

A visual completion claim is not approval. The auditor must inspect the resulting v3.18 file independently.

## 9. Return

Commit on your own session branch. Return the branch, commit, every required file path, hashes, audit output, screenshot or preview evidence, and every blocker. Do not merge or release the app yourself.
