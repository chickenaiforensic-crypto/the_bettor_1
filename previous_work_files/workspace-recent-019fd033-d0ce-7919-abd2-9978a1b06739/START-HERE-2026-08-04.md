# START HERE — Pitch Rating: first run + clearing programme (2026-08-04)
Written for someone who has never opened the app. Everything below is in order.
Do the phases one at a time. Numbers you should see are printed next to each step —
if a number differs, stop and tell me the step and what you saw.

---
## PHASE 0 — open the app (2 minutes)
1. In the file list, open the folder **APP-V3.6.2** and double-click **app-v3.6.2.html**.
   It opens in your browser. It is one file, no install, works offline.
2. You should see the Pitch Rating app with **1,432 matches** in total
   (the Coverage counter — top area of the app).
   If you see a different total, STOP and tell me before touching anything.

## PHASE 1 — the safety rehearsal (UAT, 20-30 minutes)
This proves the undo system works on YOUR machine before we clear anything for real.
Nothing here can hurt your data: every step is either harmless or ends with a restore.

Go to the **Data** tab → the section **"Country packs — clear & replace"**.

| step | do this | expect to see |
|---|---|---|
| 1 | Look at the country list | **18 countries**, A-Z. Czech Republic **632**, Russia **644**, Scotland 34, United States 81 |
| 2 | Click the arrow to expand **Russia** | 4 competitions A-Z: Russian Cup **152** · Russian Premier League **489** · Russian Relegation Playoffs **2** · Russian Super Cup **1** |
| 3 | Click **Russia** itself (whole country) | Preview with the FULL scrollable list of all 644 matches, remove/keep club lists in A-Z |
| 4 | Look at the Purge button | It is **disabled** until you download a backup |
| 5 | Click **Backup** ("Download backup, then purge") | A .json file downloads, name ends `-pre-purge-russia.json`. Purge button now works |
| 6 | Click **Purge scope (hard clear)** and confirm | Total drops from 1,432 → **788**. Log line mentions the backup file |
| 7 | Load the backup you just downloaded (the app's normal file-load / migration feature) | Total is back to **EXACTLY 1,432**. **This is the undo proof — the single most important step** |
| 8 | Now expand **Czech Republic**, click only **MOL Cup** (not the whole country) | Preview shows **63** matches, confirm screen says "Czech Republic / MOL Cup" |
| 9 | Backup → Purge that one competition | Total 1,432 → **1,369**. Czech First League (561) still visible |
| 10 | Load that MOL Cup backup | Back to **EXACTLY 1,432** |
| 11 | Click **Mute scope (soft clear)** on Russia, then **Unmute scope (restore)** | Counts drop then return identically — no data lost either way |

**If all 11 steps behaved: UAT PASSED. Tell me "UAT passed" and continue to Phase 2.
If anything differed: STOP, tell me the step number and the numbers you saw. Do not guess.**

## PHASE 2 — real clearing, country 1: CZECHIA (only after UAT passed)
Now we do for real what you just rehearsed. Old data out, audited new data in.

1. Data tab → Country packs → click whole **Czech Republic** → **Backup** (keep this file safe).
2. Click **Purge scope (hard clear)**, confirm. Total: 1,432 → **800**.
3. Import file **CZ1-2021-2026.txt** from folder **AUDITS/AUDIT-OVERRIDE-2026-08-04/**
   (the app accepts pack files on its file-load). Expect **+1,401 matches, 0 skipped**.
4. Import file **MOLCUP-FULLSPAN.txt** from the same folder. Expect **+202 matches, 0 skipped**.
5. Total should now be **2,403**. Check the Log tab: lines carry country + competition + your backup filename.

## PHASE 3 — country 2: RUSSIA
1. Country packs → **Russia** → **Backup** → **Purge**. Total: 2,403 → **1,759**.
2. Import **RPL-2021-2026.txt** (+1,220, 0 skipped).
3. Import **RUSCUP-2021-2026.txt** (+341, 0 skipped).
4. Import **RUS-ADDENDUM-2026.txt** (+18, 0 skipped).
   (The old Super Cup row will NOT collide — it was purged in step 1.)
5. Total should now be **3,338**.

## PHASE 4 — country 3: ENGLAND (pure adds, nothing to purge)
1. Import **EPL-2021-2026.txt** from AUDITS/AUDIT-OVERRIDE-2026-08-04/. Expect **+1,900, 0 skipped**.
2. Final total: **5,238 matches**.

## After each phase
Tell me the numbers you saw (imported / skipped / final total). I compare them against
the auditor pins and mark the country DONE. If a skip count is not zero, stop — a
non-zero skip means a fingerprint collision I need to see.

## The one rule that protects you
**Backup first, always. The purge button will not even click until a backup has downloaded.
Keep those .json files. Undo is always: load the backup back.** Total insurance:
app-v3.5.2.html (sealed rollback copy) also stays untouched in APP-HISTORY/.
