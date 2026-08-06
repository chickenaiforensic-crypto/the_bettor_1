# CONTRIBUTING — Git Workflow for the_bettor_1

**Active branch:** `arena/019fd213-the-bettor-1`  
**Rule:** All work happens on this branch. Do not create other branches.

## Setup

```bash
git clone https://github.com/chickenaiforensic-crypto/the_bettor_1.git
cd the_bettor_1
git checkout arena/019fd213-the-bettor-1
git pull origin arena/019fd213-the-bettor-1
```

## Workflow

1. **Read mandatory docs** (in order):
   - `COMMUNICATION-RULES-v1.md`
   - `START-HERE-COLD-START.md`
   - `Supervior/Build Docs/BLUEPRINT-SOT-2026-08-04.md`
   - `Supervior/Build Docs/ENGINE-MASTERPLAN-2026-08-05.md`
   - `Supervior/Build Docs/FUNCTIONALITY-2026-08-05.md`
   - Your role brief in `Supervior/ROLES/`

2. **Pick your workorder** from `Supervior/WORKORDER-INDEX.md` (researcher 01-17, builder B0-B7). One workorder at a time.

3. **Do the work** in your local checkout. Never edit `previous_work_files/`.

4. **Commit small, commit clear:**
   ```bash
   git add handoffs/yourfile.txt
   git commit -m "researcher: UEFA connector 2021-2026 return — 2123 rows, md5 abc123"
   git push origin arena/019fd213-the-bettor-1
   ```

   Use prefixes:
   - `researcher: ...`
   - `builder: ...`
   - `auditor: ...`
   - `planner: ...`
   - `docs: ...`

5. **Returns:**
   - Researcher: ONE `.txt` in `handoffs/`, BP-TEAM-PACK v2, never zip.
   - Builder: b64 `.txt` + evidence JSON in `handoffs/`.
   - Always include md5: `md5sum handoffs/file.txt` + `wc -l` counts.

6. **PR/Issues:**
   - Push auto-updates the branch; owner opens PR to main when ready.
   - Use PR comments to request audit: include file name, md5, row counts.

## Checks Before Push

- [ ] File name exactly as workorder says?
- [ ] No zip, no tables-as-data, rows only?
- [ ] 90-minute doctrine (AET/pens = 90' + NOTE advancement)?
- [ ] TieIds shared for two-leg ties (not per-leg)?
- [ ] md5/sha256 generated?
- [ ] `git status` clean except your return?

## Prohibited

- Editing `previous_work_files/` (history).
- Importing rejected files "to see".
- Inventing scores/dates/teams — use `NOTE|warning|blocker`.
- Using market odds in any role (P1 — permanent ban).
- Claiming a gate passed without output — show numbers.

## Auditor Gates (What I Will Run)

- Researcher: grammar → boundary → dedupe → names → structure → table reproduction → legacy cross-diff → approval card.
- Builder: byte-diff vs baseline md5 `17dd2b5b66ceb572a3fd946db9b56a92` → P1 grep (no odds/fetch) → no-network → one-gate → ladder `audit_work/backtest_harness.py` re-run.

Every gate that fails returns with exact defect; fix only that.

## Help

If blocked: one direct question in GitHub Issue with file/line/pin reference. Do not proceed blind.

*Fresh code always. Trust nothing. Every claim traces to file, code line, or pin.*
