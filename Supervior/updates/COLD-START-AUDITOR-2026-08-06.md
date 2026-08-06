# COLD-START NOTE — AUDITOR (2026-08-06)

**From:** Lead planner/analyst (covering during team break)
**To:** Auditor — when you return, read this FIRST, then the files referenced.

---

## What happened while you were away

1. **Store CLOSED at 5,082 rows.** D-1 (11 CZ1 date fixes) + D-2 (MOL Cup full-span +82) executed. Breakdown: ENG 1,900 · CZE 1,603 · RUS 1,579. Store pinned in SOT §14; operational files recorded in verification doc.
2. **Full independent re-audit completed** — zero inherited trust, fresh parsers (`audit_work/rsssf_verify.py`, `pack_parse.py`, `legacy_diff.py`). Every row verified. D-1 found and fixed. Adjudication register written.
3. **Engine masterplan written** (`Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md`) — one weighted engine, measured-effectiveness table, computation contract, refusal paths, build order S0–S7.
4. **Feasibility harness live** (`audit_work/backtest_harness.py`) — first run on D-1 store: RPL 0.5675 vs 0.6465 (−12.2%), CZ1 0.6090 vs 0.6509 (−6.4%), EPL 0.6140 vs 0.6534 (−6.0%).
5. **Approval doctrine enforced:** no system ships without measured test run. Ladder protocol in `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`.

---

## Your pending work (what needs your attention)

### Immediate (when data returns arrive)
| Item | What | Status |
|---|---|---|
| Pack returns | Researcher packs land in `handoffs/` — you gate them per workorder §5 | Watch queue — #17 (UEFA) is highest priority |
| Builder returns | B0 harness build will land — byte-diff vs baseline + harness re-run | Not yet returned |

### Standing audit items from the ledger
| Ledger # | What | Status |
|---|---|---|
| M5 | Masked replay regeneration (owed after D-1/D-2 data changes) | **OWED** — owner must click "Run masked replay" in app after loading 5,082 store |
| M10 | Outcomes-only integrity screen for new data (P1-compliant replacement for legacy market-price screen) | **SPEC OWED** — you draft the P1-compliant screen spec → owner approval |
| M17 | Settlement/venue-guard audit: I5 draw=loss enforcement + I4 entry-side flip guard on the app's settlement/entry surfaces | **OWED** — check on v3.6.4 + M5 replay run; findings logged |
| M18 | Compliance-suite lineage map (historic 167 tests ↔ builder's current suites) | **OWED** — builder must map in v3.6.4 return |
| M20 | MOL Cup old 120-row file still in store (full 202-row store exists as `pitch-rating-full-5082-D1D2-2026-08-05.json`) | Owner needs to load via app migration |

### Verification doc (your reference)
- `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` — the complete audit: census, per-league verification, defect register (D-1/D-2/D-3), adjudication register, verdict.
- `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` — SOT §14 is the live pin authority.

---

## Key reminders (read these files in this order)

1. `START-HERE-COLD-START.md` — mandatory reading order
2. `COMMUNICATION-RULES-v1.md` — binding work rules
3. `Supervior/ROLES/ROLE-AUDITOR.md` — your role brief
4. `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` — the current audit state
5. `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` — the structural plan
6. `Supervior/WORKORDER-INDEX.md` — what's queued

## Standing rules

- **Fresh code, always.** Never reuse the previous auditor's scripts as evidence. Write your own parser, compare outputs.
- **Pins on arrival.** md5/sha256 on every file received, compared against declared pin before anything else.
- **Third-source adjudication.** Where archive and pack disagree, adjudicate against an independent third source. Write the reasoning.
- **Errata owned.** Your instrument's errors get logged with your name.
- **The harness is yours.** You run the test-run ladder on every candidate and every build. The artifact table IS the approval record.

---

*If this note conflicts with a workorder or the SOT, the workorder/SOT wins — stop and ask.*
