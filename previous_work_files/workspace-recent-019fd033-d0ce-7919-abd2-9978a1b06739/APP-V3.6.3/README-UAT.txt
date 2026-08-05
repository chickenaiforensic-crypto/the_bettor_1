PITCH RATING v3.6.3 — OWNER UAT CARD (auditor-issued 2026-08-04, UTC)
=====================================================================

PINS — check BEFORE opening the file (macOS Terminal):
  base64 -d app-v3.6.3-17dd2b5b.b64.txt > app-v3.6.3.html
  md5 app-v3.6.3.html        must read  17dd2b5b66ceb572a3fd946db9b56a92
  shasum -a 256              must read  268dc5296189cf3016847624ba180cb14904a35a07bb2648428581bb78dad0f9
  size                       must be    635,798 bytes
Any mismatch: do NOT open; tell the auditor.

AUDIT VERDICT (auditor side, 2026-08-04):
- Pins: EXACT (md5 + sha256 + size).
- Byte-diff vs v3.6.2 (c7f955d4...): 4 hunks only — hold-list CSS (+3),
  version bump 3.6.2->3.6.3, the held-card renderer fix (verbatim hold list
  + Approve button "Approve — keep rows verbatim (Z-003)" wired to the
  existing approveStaged), one footnote sentence. NOTHING else changed:
  ingest/validators/commit/dedupe/scope/purge/migration/storage/schema
  untouched (diff-proven).
- Syntax gate: node --check PASS on all 4 inline scripts.
- Builder self-reported suites (registered, not adopted): hold 9/9,
  smoke 49/49, scope 43/43, legacy 156/156.
=> ADOPTED. v3.6.3 replaces v3.6.2 as the UAT/usage target.

UAT STEP G13 (the one that failed in v3.6.2) — 2 minutes:
1. Open app-v3.6.3.html in the browser where your store lives.
   Badge + footer must read v3.6.3.
2. Data > Files > drop CZ1-2021-2026.txt.
3. EXPECT: "CZ1-2021-2026.txt — Held — 20 item(s) need a human check"
   PLUS a scrollable list showing all 20 hold lines
   PLUS a button "Approve — keep rows verbatim (Z-003)" PLUS Discard.
4. Do NOT approve yet. Confirm the controls exist => G13 PASS. Tell auditor.

THEN THE FULL RUN (START-HERE numbers, now with hold expectations):
Step 0  If not done yet: drop pitch-rating-full-data-2026-08-02.json,
        approve migration. Toast MUST read "1,432 matches · 792 teams".
Step 1  Backup (top-right) -> wait for download.
Step 2  Data > Country packs > Czech Republic -> Download backup, then purge
        -> Confirm purge. Scope purged. Total must read 800.
Step 3  Files: drop CZ1-2021-2026.txt -> held 20 (expected) -> Approve ->
        toast "Loaded — 1,401 matches." Total 2,201. Skips must be 0.
Step 4  Files: drop MOLCUP-FULLSPAN.txt -> held 19 -> Approve ->
        "+202 matches." Total 2,403. Skips 0.
Step 5  Backup -> Country packs > Russia -> backup -> purge. Total 1,759.
Step 6  RPL-2021-2026.txt -> held 64 -> approve -> +1,220 -> total 2,979.
Step 7  RUSCUP-2021-2026.txt -> held 52 -> approve -> +341 -> total 3,320.
Step 8  RUS-ADDENDUM-2026.txt -> stages OK (0 holds) -> approve -> +18
        -> total 3,338.
Step 9  EPL-2021-2026.txt -> held 114 -> approve -> +1,900 -> total 5,238.

RULES: one file at a time, in this order; check the total after EVERY step;
any non-zero skip count or any other total = STOP and report to auditor.
Files tab empty after imports is normal (staged cards clear on commit).
