# SESSION — Director Control SOT v1.0

**Date:** 2026-08-08
**Status:** Control register created; no data import performed.

## Finding

The current approved v3.17 app auto-loads nine embedded partial/legacy seed packs on a first boot. These include small records for countries outside the approved 5,082-row store, including Wales and Slovenia.

## Decision recorded

- Embedded seed presence is not data approval.
- Wales, Slovenia, and every country represented only by embedded partial/closure records are classified `UNAPPROVED EMBEDDED SEED`.
- The Director control register is now `Supervior/Build Docs/DIRECTOR-CONTROL-SOT-v1.0.md`.
- The embedded-seed inventory is `Supervior/Build Docs/APP-EMBEDDED-SEED-REGISTER-v1.0.md` and `.json`.
- A P0 clean-boot builder workorder was issued. It requires zero automatic seed loading on first boot.

## No changes made

- No data pack imported.
- No store modified.
- No prediction math modified.
- No runtime app code modified in this session.
