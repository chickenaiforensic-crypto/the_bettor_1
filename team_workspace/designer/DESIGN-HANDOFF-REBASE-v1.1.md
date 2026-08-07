# DESIGN HANDOFF REBASE v1.1

**Issued:** 2026-08-07
**Purpose:** Make the designer’s v1.0 package safe to hand to the builder after the approved engine correction.
**Status:** Visible design handoff. It is not an engine change and not a replacement for builder verification.

## 1. Source package verified

The five v1.0 design files were copied byte-for-byte from:

```text
origin/arena/019fd7e1-the-bettor-1
commit 5da72c512d9b65da30d0639d496571500dd0d2bb
```

| File | SHA-256 |
|---|---|
| `DESIGN-SYSTEM-v1.0.html` | `a4d145315c1f733e758405b7d99e331ee2e1cf0179da641a15a474ed2301c9fb` |
| `DESIGN-SYSTEM-v1.0.md` | `fb9e557cc11613e7d03b1bad959f07b6db85f0482cf7db121d42c6bbb5c0b80c` |
| `IMPLEMENTATION-SPEC-v1.0.md` | `d9b5777716d923838e130f1ea2256ba7a29d5fe7cb42e6e694fe9ef782975134` |
| `SCREEN-DESIGNS-v1.0.md` | `5ef1e32856c14681125a90edcc7512058c7587be8ccd7e9193c1bf41f2f50c95` |
| `WORKORDER-UI-DESIGN-v1.0-SIGNED.md` | `4aa3b766d7a80d67b2e8057d1c8300a8ef01b76b70d9e8593126f7cbc2962e08` |

## 2. Correct builder baseline

The designer inspected the earlier v3.17 baseline:

```text
MD5 d71b042308b0637a81d22ee75795f419
```

The builder must instead implement against the approved corrected engine on `main`:

```text
builder/app-v3.17.0-picker.html
MD5 e6687ad417fd1d3229a000c12f73f1a3
SHA-256 51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7
```

The visual specification remains usable because the correction removed prohibited seed content and an unused constant, not the picker layout or the relevant UI structure.

## 3. Binding implementation boundaries

The next builder task is visual implementation only.

- Do not change prediction calculations, calibration, parity targets, stored data, ingestion logic, or `PR.ingest`.
- Do not add network calls.
- Do not add market data, odds, prices, bookmaker language, or betting terminology.
- Keep visible provenance on every result number.
- Keep the clear NO CALL state and its balance panel.
- Preserve the existing backup, intake, settlement, and integrity safeguards.

## 4. P1 display correction

The current app visibly renders labels such as `Double chance`, `Draw no bet`, and `Home −1 handicap`. The designer correctly flagged those as betting-style terminology.

For the UI implementation, the builder must withhold the entire user-facing Markets section rather than relabel it. This is a presentation removal only: do not change the underlying engine calculations without a separate approved engine workorder.

## 5. Next handoff

Use:

```text
team_workspace/builder/WORKORDER-BUILDER-UI-IMPLEMENTATION-v1.0.md
```

The builder must produce a new versioned app file, run regression and compliance checks, and wait for independent approval before any release.
