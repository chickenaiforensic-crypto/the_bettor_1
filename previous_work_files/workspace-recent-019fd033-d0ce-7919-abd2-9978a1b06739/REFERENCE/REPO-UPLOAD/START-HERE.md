# START HERE — handoff to the researcher (from the programme auditor)

You are the researcher for the Pitch Rating rebuild. This repo is the exchange point between you, the owner, and me (the auditor who verifies your work before it may enter the app). Everything you need is in `Supervisor/`. Everything you deliver lands in `handoffs/` — or is pasted in chat as a `.txt` file. **Files left in your own session are undelivered. If you upload here: the green "Commit changes" click is mandatory — dragged-but-not-committed files vanish silently.**

## Your job

1. Open the workorders in `Supervisor/` **in queue order**: ① RPL → ② CZ1 → ③ RUSCUP → ④ MOLCUP → ⑤ SCO1 → ⑥ KOS → ⑦ MLS → ⑧ USOC → ⑨ SCOCUP → ⑩ SCOLC → ⑪ KOSCUP → ⑫ EPL → ⑬ SPA → ⑭ ITA → ⑮ GER → ⑯ FRA (the five majors). Run as many in parallel as you can — but deliver complete files, in that order. **MLS is the big one (~2,800 rows): budget it; the four cup files ⑧–⑪ are small (~100-250 each); the five majors ⑫–⑯ are ~1,500-1,900 each but their club rosters are 100% pre-existing -- the lightest big files of the program.**
2. Per workorder: deliver **ONE** return file named exactly `<LEAGUE>-2021-2026_BP-TEAM-PACK_v2.txt` (e.g. `RPL-2021-2026_BP-TEAM-PACK_v2.txt`), ending with a line `END`.
3. Read the workorder's **§0 federation check first**. Then scan your own finished rows: any club outside its roster pool = you are on the wrong country — stop, restart. (This exact failure burned a full night: a previous return arrived as **standings tables of the Rwandan league** — wrong document class, wrong federation, and never actually delivered. Rows, right country, real delivery — all three or nothing.)

## The rules that never bend

- **Match rows only. Never standings tables.** A row = one played game: date / home / away / score. Tables are what *I* compute to check *you* — they are audit targets, not deliverables.
- Grammar: `BP-TEAM-PACK v2` exactly as each workorder's §2 defines. The loader is strict; unknown names are the #1 cause of rejection.
- **90-minute scores always.** Every tie settled in extra time or on penalties carries a `NOTE|info|advancement` naming who advanced. Without it the bracket cannot be reconstructed and the return fails.
- **Sources:** RSSSF round-by-round = primary (URLs pinned in each workorder), one independent index as cross-check. Any conflict → resolve to RSSSF, log `NOTE|warning|source_conflict`.
- **Never guess.** Unverifiable = `NOTE|warning|blocker`, not a row. Fabrication is the one unforgivable defect.
- **Cutoffs vs appendices:** workorders ①–④ accept **nothing dated 2024-06-30 or later** (we already hold and have verified 2024-26 — recollecting it = automatic fail). Workorders ⑤–⑧ have **no cutoff** but an appendix listing rows we already hold — returning any appendix row = automatic fail. Workorders ⑨–⑯ hold nothing — full slice/span, no exclusion lists.

## What I do with your return (the drill you are aiming at)

Decode and pin the file → boundary/duplicate scan against the live store → **recompute every season's table from your rows alone and compare club-for-club to the official record** (16/16, 12/12+groups, 10/10, or both MLS conferences — zero tolerance) → **span-diff:** every official match in the 2021→today window must exist somewhere; an unexplained hole keeps your commission open → one staged approval card → the owner clicks Approve once and the app intakes it.

Fail a gate and you get the failing gate named back at you — fix, resend, same file name.

## Tonight's scale, honestly

≈16,300 rows across 16 workorders. Do what you can do *well* — the queue order decides what gets verified and approved first, and partial progress lands safely as long as each delivered file is complete per the workorder (a half-season is a blocker-NOTEd return, not 120 silent-missing rows).

**First deliverable: `RPL-2021-2026_BP-TEAM-PACK_v2.txt`.** Good hunting — check your rows against your own sources twice; I will check them a third time.
