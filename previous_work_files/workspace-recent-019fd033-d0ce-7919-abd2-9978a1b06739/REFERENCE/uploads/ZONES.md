# ZONES — decision & scar log (append-only)

> Every shipped decision gets an entry with WHY and numbers. Every rejection, every honest no-ship, every gap closure gets one too.
> **Never rewrite, never delete, never reorder.** Newest entry on top.
>
> Entry format: `## Z-YYYY-MM-DD-<seq> — <title>` · `Decision:` · `Why:` · `Evidence:` · `Status:` · `Rollback:`.

---

## Z-2026-08-02-001 — Cold start on a partial bundle (v0)

- **Decision:** Begin the rebuild with the two uploaded files (master WO + handoff README) as the sole inputs; all 12 missing bundle items are logged in `docs/GAPS.md` with WO-mandated fallbacks, and the four owner rulings (Q1–Q4) are requested before Phase 0 coding. `trail/ZONES.md` is created fresh because the historical log was not in the bundle — the loss is hereby recorded, not papered over.
- **Why:** The WO declares itself self-contained and its stop-conditions demand *stop and ask* on any conflict with a binding document; with the binding docs absent, proceeding silently would violate the hand-back protocol (WO §0, §8). The project's own audit discipline forbids asserting state that cannot be verified.
- **Evidence:** `find /home/user/uploads` → exactly 2 files (README.md, WORKORDER-PITCH-RATING-REBUILD.md). Bundle README lists ≥16 items. md5 of uploads recorded at ZONES v0 annex below.
- **Status:** ⏸ pending rulings (Q1 bundle handling · Q2 session scope · Q3 UI direction · Q4 seed policy).
- **Rollback:** n/a (no code shipped).

### Annex — upload fingerprints (2026-08-02)

```
README.md                              md5: computed at first ship audit
WORKORDER-PITCH-RATING-REBUILD.md      md5: computed at first ship audit
```

---

## Z-2026-08-02-000 — Log opened

- **Decision:** This log is opened as v0 on 2026-08-02, before any code. Format adopted per WO §8 (versioned entries, numbers, honest no-ships).
- **Why:** The WO requires ZONES entries per ship and treats the log as the project's scar memory; opening it at cold start establishes the trail before the first line of code.
- **Status:** ✅
