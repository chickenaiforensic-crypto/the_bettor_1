# START HERE — cold start for every new session (2026-08-05)

You are new to this project. Read the following **in this order** — each file exists so the next one makes sense. Do not skim; the last audit that skimmed missed 11 date errors (found later, fixed).

## Order of reading (≈45 minutes total)

| # | Read | What it gives you |
|---|---|---|
| 1 | `COMMUNICATION-RULES-v1.md` | How we talk and work (binding: no vague, no guessing, audit before asking) |
| 2 | `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md` | The whole system on one page: engines R1/R2/R3, doctrine, missed-work ledger M1–M20, amendments A-01..A-08, cold-start kit K1–K10, live pins (§14) |
| 3 | `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md` | The TARGET structure: one weighted engine; **approval by test run** (§5); cross-league fit-to-results loop (§6); build order S0–S7 (§8) |
| 4 | `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md` | What the current app (v3.6.3) does today, screen by screen |
| 5 | `Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` | The truth about the data: 5,000 rows verified, defect register (D-1 fixed / D-2 open), adjudication register |
| 6 | `Supervior/WORKORDER-INDEX.md` | The queue — find YOUR workorder by number |
| 7 | Your role brief: `Supervior/ROLES/ROLE-RESEARCHER.md` **or** `ROLE-BUILDER.md` **or** `ROLE-AUDITOR.md` | Exactly what you do, where your work goes, what gates you face |
| 8 | `README.md` | The map (re-read once; it will now mean something) |

## Standing truths (memorise)
- **The system predicts from results only.** Bookmaker prices are excluded in every role — input, feature, benchmark, sanity check, fallback. "The market says" is never evidence.
- **Approval is a measured test run, not a document.** The protocol: `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` (the ladder: last game → last 2 → expanding holdout → full-system check).
- **The app can say "I don't know".** NO CALL with a balance panel is a valid, shown output. Never fabricate a number to avoid it.
- **Nothing enters the store on trust.** Every return is auditor-verified before import; the auditor re-runs everything with fresh code (never the previous auditor's scripts).
- **Backup before any purge. Undo = load the backup.** There is no other undo.
- **Pins are law.** Files are pinned (md5/sha256) in the SOT §14; when the repo moves, re-pin before citing.

## What you must NEVER do
- Never edit `previous_work_files/` (history) or rewrite a pinned file without an erratum entry.
- Never import a file that failed a gate, "to see what happens".
- Never invent a team, score, or date — write a `NOTE|warning|blocker` instead.
- Never ask a question the system already answers (that is a rule, not a suggestion).
- Never ship anything without its measured test run artifact.
