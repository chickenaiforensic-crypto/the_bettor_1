IMPORT-READY-2026-08-03 — FOUR audited, approved packs. Drop into the app in THIS ORDER:

  1. RPL-2021-2026_BP-TEAM-PACK_v2.txt     md5 c3a72b35e834cc030d62b3d160c79b25
  2. RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt  md5 91bce98de5ff5f999a2f03f3ee7d3caa  (v3: researcher's byte-pure KAMAZ-exact rebuild, commit 9dc08ee — replaces the auditor hand-fix)
  3. MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt  md5 662fe5dfe38002474855110b2a17ea6c  (MUST land before #4: it declares the Vlasim + Pribram TEAM rows the CZ1 playoff rows use)
  4. CZ1-2021-2026_BP-TEAM-PACK_v2.txt     md5 29c3b6c9d63906bde4db20ac4e6b742c  (841-row version WITH the 12 Czech Relegation Playoffs rows, commit 9dc08ee)

EXPECTED ROW COUNT after each drop (live store was 1,447):
  after #1+#2: 2,368
  after #3:    2,488 MATCH rows (+120); the pack also carries 31 TEAM declarations (RPL/RUSCUP precedent: TEAM lines do not move the Coverage counter)
  after #4:    3,329

RULES
- Multi-select all four files is fine; the app queues them, but approve IN THE ORDER ABOVE.
- If any card shows Held/needs-a-human-check: STOP, tell the auditor which file and what the card says. Do not Discard.
- After the last Approve, report the Coverage numbers back (a photo of the Coverage tab is fine).
- The "undefined (N rows)" display names on some leagues are a known cosmetic gap (builder ticket P6) — the data itself is fine.
