# COLD-START NOTE — RESEARCHER (2026-08-06)

**From:** Lead planner/analyst (covering during team break)
**To:** Researcher — when you return, read this FIRST, then the files referenced.

---

## What happened while you were away

1. **Store CLOSED at 5,082 rows.** D-1 (11 CZ1 date fixes) applied. D-2 (MOL Cup full-span +82) executed. Final breakdown: ENG 1,900 · CZE 1,603 · RUS 1,579.
2. **Independent re-audit completed** (zero inherited trust, fresh parsers). Every row verified against RSSSF + third sources. One new defect class found (D-1, fixed). Adjudication register written. See `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md`.
3. **Engine masterplan written** (`Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md`) — one weighted engine, build order S0–S7, approval by measured test run only.
4. **UEFA Connector workorder drafted & queued** as #17 — this is the HIGHEST PRIORITY new data commission. Owner confirmed: UCL + UEL + UECL + qualifiers, 2021-22 through 2025-26 (+2026-27 played), ties with ≥1 programme-league club (ENG/RUS/CZE/SPA/ITA/GER/FRA).
5. **Parallel researcher approved** by owner. You can run workorders 06–16 in parallel with researcher #2 on #17.

---

## Your current queue (what to do, in order)

| Priority | # | Workorder | Status | Action |
|---|---|---|---|---|
| 🔴 HIGH | 17 | UEFA-CONNECTOR | QUEUED | **START NOW.** See workorder for grammar, sources, gates. RSSSF country archives + uefa.com + Wikipedia + worldfootball. |
| 🟡 | 06 | SPA (La Liga) | QUEUED | Can run in parallel with #17 |
| 🟡 | 07 | ITA (Serie A) | QUEUED | After #06 or in parallel |
| 🟡 | 08 | GER (Bundesliga) | QUEUED | After #07 or in parallel |
| 🟡 | 09 | FRA (Ligue 1) | QUEUED | After #08 or in parallel |
| ⚪ | 10–16 | SCO1, SCOCUP, SCOLC, KOS, KOSCUP, MLS, USOC | QUEUED | Lower priority; run after the big 5 |

---

## Key reminders (read these files in this order)

1. `START-HERE-COLD-START.md` — mandatory reading order
2. `COMMUNICATION-RULES-v1.md` — binding work rules (never guess, audit before asking)
3. `Supervior/ROLES/ROLE-RESEARCHER.md` — your role brief
4. `Supervior/Workorder/WORKORDER-UEFA-CONNECTOR-2021-2026-5YSPAN.md` — your priority commission
5. `Supervior/WORKORDER-INDEX.md` — full queue

## Standing rules you must NOT forget

- **Section 0 of every workorder = the federation check.** First attempt in this programme was the wrong country. Do the check.
- **Rows, never tables.** Standings are recompute targets, never inputs.
- **90-minute doctrine.** AET/pens = 90' score + `NOTE|info|advancement`.
- **Never guess.** Unverifiable = `NOTE|warning|blocker`.
- **Return:** ONE `.txt` per workorder, named exactly as the workorder says, into `handoffs/`. No .zip.
- **Source hierarchy:** RSSSF primary → one independent index → worldfootball. Conflicts = `NOTE|warning|source_conflict`.

## What the auditor checks on your return

Grammar → boundary → dedupe vs live store → names → structure → table reproduction → independent cross-diff → one approval card. Your self-gate counts are registered, never trusted.

---

*Everything above traces to a file in this repo. If this note conflicts with a workorder, the workorder wins — stop and ask.*
