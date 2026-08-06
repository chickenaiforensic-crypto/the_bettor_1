# OWNER RELAY CHECKLIST — 2026-08-06 (planner covering)

**Purpose:** what to forward to each team member when they return. Cold-start notes are written and ready.

---

## Step 1: Load the closed store into the app

1. Open app v3.6.3 in browser
2. Drop `previous_work_files/workspace-recent-019fd033-…/pitch-rating-full-5082-D1D2-2026-08-05.json` as a migration file
3. Toast should read: **"Store replaced by migration: 5082 matches · 609 teams"**
4. Go to Calibration tab → click **"Run masked replay"** — this closes **M5**
5. Take a fresh backup: header → Backup button → save `pitch-rating-full.json`

---

## Step 2: Forward to Researcher

**File:** `Supervior/updates/COLD-START-RESEARCHER-2026-08-06.md`

**Message (copy-paste):**
> Cold-start note attached. Read it first. Your priority is workorder #17 (UEFA Connector) — UCL + UEL + UECL + qualifiers, 2021-26, ties with our programme-league clubs. Returns land in `handoffs/` as one `.txt` per workorder. The workorder file is `Supervior/Workorder/WORKORDER-UEFA-CONNECTOR-2021-2026-5YSPAN.md`. Workorders 06–16 (SPA/ITA/GER/FRA/SCO/KOS/MLS/USOC) can run in parallel with a second researcher.

---

## Step 3: Forward to Builder

**File:** `Supervior/updates/COLD-START-BUILDER-2026-08-06.md`

**Message (copy-paste):**
> Cold-start note attached. Read it first, then `START-HERE-COLD-START.md`, then `builder/README-BUILDER.md`. Your first workorder is B0 (`Supervior/Workorder/WORKORDER-BUILDER-B0-HARNESS.md`) — productionise the backtest harness into the app's masked-replay module with the ladder protocol. The approval protocol is `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — read it twice. Deliverables: b64-armoured `.txt` + evidence artifact into `handoffs/`.

---

## Step 4: Forward to Auditor

**File:** `Supervior/updates/COLD-START-AUDITOR-2026-08-06.md`

**Message (copy-paste):**
> Cold-start note attached. Read it first. Key pending items: M5 (masked replay — check after owner runs it), M10 (outcomes-only integrity screen spec — you owe this), M17 (settlement/venue audit), M18 (compliance-suite lineage map from builder), M20 (MOL Cup import confirmation). When researcher packs arrive in `handoffs/`, you gate them per workorder §5. When builder returns arrive, byte-diff + harness re-run. Everything with fresh code — never trust the previous auditor.

---

## Step 5: Confirm to planner

Once each team member has their note and has confirmed understanding, reply here and I will:
- Update the session log
- Track any questions or blockers
- Resume planner duties (workorder coordination, masterplan upkeep, ledger updates)

---

*If any team member has questions that this checklist does not answer, the answer is in the repo — point them to `START-HERE-COLD-START.md`.*
