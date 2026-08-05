# HANDOFFS — where returns land (2026-08-05)

**One file per workorder. This folder is the only door for work product.**

## Researcher returns
- Name exactly as the workorder says: `<SCOPE>-<span>_BP-TEAM-PACK_v2.txt` (e.g. `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt`).
- One text file per workorder. **No .zip, no paste fragments, no tables-as-data.**
- Nothing here is imported on trust. The auditor gates it (workorder §5), then it commits through the app's own intake.

## Builder returns
- App file: b64-armoured `.txt` (the raw-html channel injects junk — b64 is law for large app files) + the test-run evidence artifact (train window, holdout, n, all metrics, date).
- Name: `<STEP>-<version>-<md5prefix>.b64.txt` + `<STEP>-EVIDENCE-<date>.json/txt`.

## Rules that never change
1. **Rows, never tables.** Standings are recompute targets, never inputs.
2. **90-minute doctrine.** AET/pens = 90' score + advancement NOTE.
3. **Never guess.** Unverifiable = `NOTE|warning|blocker`, not a row.
4. **Auditor verification before anything enters the app.** Pins verified on arrival.
5. **The owner relays files that land here** to the session that needs them; the repo is the memory.

*First researcher attempt in this programme was the wrong country. The federation check in every workorder's section 0 exists because of that.*
