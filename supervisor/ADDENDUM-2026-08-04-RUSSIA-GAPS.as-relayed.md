# ADDENDUM REQUEST — to the RESEARCHER session (Russia gaps + MOLCUP transport)
From: AUDITOR (Arena session) · Date: 2026-08-04 · Status: SEND NOW
Context: your DECREE-2026-08-04 override packs (RPL d71ed24f… · RUSCUP f89501cf… ·
CZ1 cbd5710b… · EPL 707dd830…) are fetched, PIN-VERIFIED and WAVE-1 audited.
Two gaps block the Russia clearing; one transport gap blocks Czechia.

## REQ-1 (transport, urgent): push MOLCUP full-span
Your commit `5d75e56` (MOLCUP 202 rows, sha 50ead762…) is LOCAL ONLY — the push died
with your expired token. Remote tip is 5722cb61 and holds only the old 120-row pack.
Reconnect GitHub and push. Nothing else about MOLCUP is needed from you;
I audit on arrival (md5/sha-on-arrival policy stands).

## REQ-2 (Russia addendum pack, D14 blocking): 2026-27 played rows
Owner decree = full seasons 2021 → TODAY. RPL 2026-27 Round 1 was played
2026-07-24..26 and Round 2 had games by 2026-08-04 (rus2027.txt prints them).
The RPL pack ships zero 2026-27 rows. Append the played rounds as rows with the
same grammar (Russian Premier League | domestic-league | Round n). Estimate today:
8 (R1) + played R2 rows. Rolling-append as rounds complete is fine; say so in NOTE.

## REQ-3 (Russia addendum pack, D14 blocking): Super Cup 2025 + 2026 (2 rows)
The outbox spec (Russia-complete, file 02) required both Super Cups; neither pack
carries any. rus2026.txt #sup confirms 2026: Zenit 1-1 Spartak [pen 4-2],
2026-07-18, Nizhny Novgorod (90-min row = 1-1 + advancement NOTE per doctrine);
2025 game = Zenit vs Krasnodar-class summer 2025 final (verify vs rus2026/rus2027
+ report). compType = domestic-cup class per errata; competition string
'Russian Super Cup' to match the store's scope naming.

REQ-2 and REQ-3 can ship as ONE small addendum pack (BP-TEAM-PACK v2, own sha,
announced in WORKORDER-STATUS). Source discipline unchanged: RSSSF primary,
2nd-index where RSSSF is thin, NOTE for anything unverifiable — no guessing.

## Registered (not blocking): Wave-2 items already on my side
RPL full round-grid date-diff; RUSCUP +152-row score-diff; CZ1 Evropu 31-leg diff.
Yours to deliver = REQ-1..3 only.
