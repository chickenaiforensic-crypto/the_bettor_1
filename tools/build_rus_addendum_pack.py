#!/usr/bin/env python3
"""Deterministic builder for the RUS-ADDENDUM pack (ADDENDUM-2026-08-04 REQ-2 + REQ-3).
Contents: RPL 2026-27 played rounds (R1+R2 = 16 rows) + Russian Super Cup 2025/2026 (2 rows).
Rows transcribed in audit/ledger/rpl-2026-27.txt and audit/ledger/rus-supercup-2025-2026.txt.
Byte-deterministic: no timestamps, no randomness, LF newlines, ASCII-only."""
import hashlib, sys

OUT = "handoffs/RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt"

L = []  # pack lines

L.append(
    "NOTE|info|pack_id|RUS-ADDENDUM-2026_BP-TEAM-PACK_v2 - Russia addendum drop per "
    "supervisor/ADDENDUM-2026-08-04-RUSSIA-GAPS REQ-2 (RPL 2026-27 played rows) and REQ-3 "
    "(Russian Super Cup 2025 + 2026), commissioned together with supervisor/SPEC-2026-08-04-RUSSIA-COMPLETE "
    "(owner decree D14, full seasons 2021 to today). 18 MATCH rows = 16 league (Round 1 x8, Round 2 x8 of "
    "2026-27, completed by 2026-08-02) + 2 Super Cup finals. Rolling-append policy per REQ-2: played rounds "
    "ship as they complete; next round starts 2026-08-08 (zero rows). The pinned full-span packs stay "
    "byte-untouched (RPL sha256 d71ed24f..., RUSCUP sha256 f89501cf..., their auditor pins preserved); this "
    "addendum is a separate file with its own sha, registered in WORKORDER-STATUS. Compiled 2026-08-04."
)

L += [
    "SOURCE|rsssf-rus2027-1l|https://www.rsssf.org/tablesr/rus2027.html|2026-08-04|primary-archive|Russia 2026/27 #1l (fetched 2026-08-04): Round 1 results with dates + per-game attendances printed in full (Total Att: 102,232; Average: 12,779); Round 2 printed as fixtures only [Jul 31 - Aug 3] at fetch; full R1-R30 calendar through May; membership incl. [P] tags Fakel/Rodina and NBs (Akron home at Samara; Dynamo Makhachkala at Kaspiysk)",
    "SOURCE|premierliga-heritage-2627|https://heritage.premierliga.ru/tournaments/championship/|2026-08-04|authoritative-official|RPL official heritage match centre (fetched 2026-08-04): Rounds 1-2 with weekday, kickoff, score and match centre ids match_16241-16256; proves the Round-2 window was completed 2026-07-31..2026-08-02 (no Aug-3 game); Round 3+ printed as fixtures",
    "SOURCE|wiki-rpl-2627|https://en.wikipedia.org/wiki/2026%E2%80%9327_Russian_Premier_League|2026-08-04|second-index|independent season index (fetched 2026-08-04): venues table 16/16 (Rodina = Arena Khimki 14,950; Fakel = Fakel Stadium 10,052), FBR results matrix R1/R2 16/16 vs official, league table + GameStats through 2026-08-02 (16 matches, 51 goals, att 193,274 avg 12,080; high 30,953 Krasnodar-Fakel; low 3,324 Rodina-Rostov); ru.wiki mirror sighted (goals cell stale 48 vs 51 - lagged update, disclosed)",
    "SOURCE|rsssf-rus2025-sup|https://www.rsssf.org/tablesr/rus2025.html#sup|2026-08-04|primary-archive|Russia 2024/25 #sup 'Russian Super Cup 2025' (fetched 2026-08-04): FC Krasnodar 0-1 CSKA (Moskva) [Igor Divejev 48; red Cobnan 89], referee Cistjakov (Azov), 12.07.25 'Kazan Arena' era print, Att: 34,677, full lineups",
    "SOURCE|rsssf-rus2026-sup|https://www.rsssf.org/tablesr/rus2026.html#sup|2026-08-04|primary-archive|Russia 2025/26 #sup 'Russian Super Cup 2026' (fetched 2026-08-04): Zenit 1-1 Spartak [pen 4-2], scorers Martins 25 / Sobolev 90+8 pen, full shoot-out lines + lineups, referee Bulanov (Saransk), 18.07.26 Niznij Novgorod Stadium, Att: 42,139",
    "SOURCE|wiki-supercup-2025|https://en.wikipedia.org/wiki/2025_Russian_Super_Cup|2026-08-04|second-index|independent match box (fetched 2026-08-04): 2025-07-12 Ak Bars Arena Kazan, att 34,677, referee Chistyakov, Diveyev 48' named Man of the Match, report link rfs.ru/match/55756, CSKA 8th title",
    "SOURCE|wiki-supercup-2026|https://en.wikipedia.org/wiki/2026_Russian_Super_Cup|2026-08-04|second-index|independent match box (fetched 2026-08-04): 2026-07-18 Nizhny Novgorod Stadium, att 42,139, referee Bulanov, Zenit won 4-2 on penalties (10th title), report link rfs.ru/match/57020; qualification lines (Zenit champions / Spartak cup winners)",
]

L += [
    "NOTE|info|rolling_append|2026-27 RPL rows ship as rounds complete (rolling policy per REQ-2, say-so NOTE): this drop carries Round 1 (8 rows) + Round 2 (8 rows), last played 2026-08-02; Round 3 is scheduled 2026-08-08..10 per premierliga-heritage-2627 and is NOT played at the 2026-08-04 return date - zero rows. League running total vs the pinned RPL pack: 1,200 + 16 = 1,216 rows to date.",
    "NOTE|info|source_adaptation|RSSSF rus2027 (primary) printed Round 1 complete but Round 2 fixture-only at fetch day. Round-2 rows are dated/scored from the RPL official heritage match centre (match_16249..16256) and reconcile against wiki-rpl-2627 in all three of its independent structures: FBR matrix 16/16 (R1+R2), league table through 2026-08-02 recomputed 16/16 club-for-club from this pack's rows (validator G09), and infobox totals (16 matches, 51 goals). No RSSSF/wiki conflict to adjudicate - RSSSF will re-sync on its next refresh. worldfootball has no 2026-27 RPL page at fetch day (404 at both season-slug shapes) - third index absent, documented.",
    "NOTE|info|estimate_variance|Count variance vs the commissioning estimates, no rework needed: SPEC-2026-08-04 item 1 expected '1,209 rows today' (8 R1 + 1 R2) and REQ-2 estimated '8 + played R2 rows'; delivered = 16 addendum league rows (1,216 cumulative) because Round 2 completed in full by 2026-08-02 - the pair estimate was drafted against an earlier round-2 snapshot.",
    "NOTE|info|playoff_composition|Registered for the audit diff (no change made): SPEC-2026-08-04 item 2 enumerates 16 playoff legs (2022/2023/2024/2026) naming 2026 'Shinnik-Akron'. The pinned RPL pack ships 20 legs including the four 2025 ties (PFC Sochi - Pari NN; Ural - Akhmat) and the actual 2026 ties (Akron - Rotor; Ural - Dynamo Makhachkala). Shinnik Yaroslavl was not a playoff participant (First League 8th; seeds were Ural 3rd, Rotor 4th - rsssf-rus2026 #2l/#prorel). The SPEC enumeration is incomplete, not a pack gap.",
    "NOTE|info|supercup_scope|02-SPEC item 3 + REQ-3 commission the 2025 and 2026 Russian Super Cups only: competition string 'Russian Super Cup' per the store's scope naming; compType domestic-cup chosen per ERRATA-2026-08-03 cup class and flagged here as the 02-SPEC hard rule requires ('super cups pending builder confirm - flag your choice in a NOTE'). Editions 2021-2024 exist (Zenit 2021/2022/2024, CSKA 2023 per the list of finals) but are outside this commissioned scope - zero rows shipped, not an oversight.",
    "NOTE|info|advancement|2026 Russian Super Cup: Zenit St Petersburg won 4-2 on penalties after a 1-1 draw in 90 minutes (no extra time under Super Cup regulations; the MATCH row carries the 90-minute score per the 90-minute doctrine). Goals: Christopher Martins 25 - Aleksandr Sobolev 90+8 (pen). Shoot-out per rsssf-rus2026-sup: 1-0 I.Divejev, 1-1 P.Solari, 2-1 Felipe Augusto, 2-1x N.Umyarov (held), x2-1 A.Mostovoy (wide), 2-1x I.Dmitriyev (held), 3-1 Jhon Jhon, 3-2 C.Wooh, 4-2 A.Sobolev. Referee Evgeniy Bulanov (Saransk); Nizhny Novgorod Stadium, att 42,139 (report rfs.ru/match/57020 per wiki box). Zenit's 10th Super Cup title.",
    "NOTE|info|advancement|2025 Russian Super Cup: CSKA Moscow beat FC Krasnodar 1-0 in 90 minutes (Igor Diveyev 48; named Man of the Match per wiki box), referee Artyom Chistyakov (Azov), Ak Bars Arena, att 34,677 (report rfs.ru/match/55756 per wiki box). Red card: Moses Cobnan (Krasnodar) 89, per rsssf-rus2025-sup. Qualification: Krasnodar 2024-25 champions, CSKA 2024-25 Russian Cup winners. CSKA's 8th Super Cup title.",
    "NOTE|info|venue_era|Venue strings continue the pinned RPL-pack usage (venue-consistency decree): rsssf-rus2025-sup prints the 2025 final venue as 'Kazan Arena' = the same ground as the pinned Ak Bars Arena (sponsor era; row carries the pack string). The 2026 neutral venue is printed 'Nizhny Novgorod Stadium' by BOTH RSSSF and wiki (not the SovComBank Arena sponsor era used for Pari NN home games) - row carries the shared print. Rodina Moscow homes = Arena Khimki, Khimki (wiki-rpl-2627 venues 14,950; rsssf-rus2026 #2l prints Rodina at Khimki through 2025-26 as well); the club's own Spartakovets Stadium carried its 2023 playoff rows (RPL pack venue_policy NOTE). Baltika keeps pinned Rostech Arena (wiki-rpl-2627 prints 'Rostec Arena' - same ground, spelling era). Krasnodar keeps pinned Ozon Arena (sponsor era from R27 2025). Fakel keeps pinned Fakel Stadium (10,052; in use from the 2023-24 boundary per the RPL ledger EXCEPTIONs).",
    "NOTE|info|identity|Club strings are the pinned WO-RPL section-3 roster strings: all sixteen 2026-27 participants already appear verbatim in the RPL pack (Rodina Moscow from its 2023 playoff rows). The TEAM row below registers Rodina Moscow's first span TOP-FLIGHT identity (2025-26 First League champions 19-11-4 58-28 68pts - rsssf-rus2026 #2l; Premier League debut season; aliases simply Rodina). Source compact spellings map to roster strings as before (RSSSF 'Dinamo Mh' = Dynamo Makhachkala; 'Krylja S.'/'KS' = Krylia Sovetov Samara; 'Ahmat' = Akhmat Grozny; 'Akron Togliatti' = Akron Tolyatti). Igor Diveyev appears for ZENIT in the 2026 Super Cup - verified Zenit's summer-2026 signing from CSKA (rsssf-rus2026-sup lineup); an earlier provisional wiki read that flagged it as an anomaly is withdrawn.",
    "NOTE|info|source_conflict|wiki-rpl-2627 hat-trick table dates Maksim Glushenkov's treble (Orenburg 0-3 Zenit) '2 August 2025' - an editorial YEAR typo (season began 2026-07-24); the match was played 2026-08-02 (premierliga-heritage-2627 match_16251 plus both indexes' table-update stamps). Row carries 2026-08-02. ru.wiki infobox shows 48 goals vs en.wiki 51 - a mid-day snapshot lag on the mirror page, no score conflict. No other index conflicts.",
    "NOTE|info|boundary|Rows span 2025-07-12..2026-08-02 only (return date 2026-08-04): zero rows for unplayed fixtures, zero dateless rows, zero duplicate (date, home, away) pairs, no row dated past the return date. The 2026-27 season is NOT complete (regular season to 2027-05-29 + playoffs): this pack extends the played edge only; future drops append completed rounds under the rolling policy.",
    "NOTE|info|attendance|Round-1 attendance anchors per rsssf-rus2027 print: 15,196 / 5,091 / 23,601 / 15,335 / 9,289 / 18,866 / 10,051 / 4,803 - summing EXACTLY to the printed Total Att 102,232 (Average 12,779 = total/8). Round-2 aggregate per wiki-rpl-2627 GameStats: 193,274 season total - 102,232 = 91,042 over 8 games; printed per-game marks: Krasnodar-Fakel 30,953 (season high), Rodina-Rostov 3,324 (season low).",
]

L.append(
    "TEAM|Rodina Moscow|Russia|Russian Premier League|RPL|Rodina|Arena Khimki|Moscow|Russia||||"
)

M = []
# REQ-3 — Russian Super Cup rows (90-minute doctrine; see advancement NOTEs)
M.append("MATCH|2025-07-12|Russian Super Cup|domestic-cup|FC Krasnodar|0|1|CSKA Moscow|Final|Ak Bars Arena|Kazan|Russia||rsssf-rus2025-sup")
M.append("MATCH|2026-07-18|Russian Super Cup|domestic-cup|Zenit St Petersburg|1|1|Spartak Moscow|Final|Nizhny Novgorod Stadium|Nizhny Novgorod|Russia||rsssf-rus2026-sup")
# REQ-2 — RPL 2026-27 Round 1 (rsssf-rus2027 primary)
M.append("MATCH|2026-07-24|Russian Premier League|domestic-league|CSKA Moscow|2|1|Baltika Kaliningrad|Round 1|VEB Arena|Moscow|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-25|Russian Premier League|domestic-league|Dynamo Moscow|0|0|Krylia Sovetov Samara|Round 1|VTB Arena|Moscow|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-25|Russian Premier League|domestic-league|Akron Tolyatti|0|5|Zenit St Petersburg|Round 1|Solidarnost Samara Arena|Samara|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-25|Russian Premier League|domestic-league|Fakel Voronezh|1|2|Dynamo Makhachkala|Round 1|Fakel Stadium|Voronezh|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-25|Russian Premier League|domestic-league|Spartak Moscow|3|0|Rodina Moscow|Round 1|Lukoil Arena|Moscow|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-26|Russian Premier League|domestic-league|Lokomotiv Moscow|1|1|Akhmat Grozny|Round 1|RZD Arena|Moscow|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-26|Russian Premier League|domestic-league|FC Orenburg|2|1|FC Rostov|Round 1|Gazovik Stadium|Orenburg|Russia||rsssf-rus2027-1l")
M.append("MATCH|2026-07-26|Russian Premier League|domestic-league|Rubin Kazan|1|3|FC Krasnodar|Round 1|Ak Bars Arena|Kazan|Russia||rsssf-rus2027-1l")
# REQ-2 — RPL 2026-27 Round 2 (premierliga official + wiki second index; RSSSF fixture-only, see source_adaptation NOTE)
M.append("MATCH|2026-07-31|Russian Premier League|domestic-league|Rodina Moscow|2|4|FC Rostov|Round 2|Arena Khimki|Khimki|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-01|Russian Premier League|domestic-league|Akron Tolyatti|1|2|Rubin Kazan|Round 2|Solidarnost Samara Arena|Samara|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-01|Russian Premier League|domestic-league|CSKA Moscow|1|1|Krylia Sovetov Samara|Round 2|VEB Arena|Moscow|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-01|Russian Premier League|domestic-league|Dynamo Makhachkala|2|1|Lokomotiv Moscow|Round 2|Anzhi Arena|Kaspiysk|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-01|Russian Premier League|domestic-league|Baltika Kaliningrad|2|1|Dynamo Moscow|Round 2|Rostech Arena|Kaliningrad|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-02|Russian Premier League|domestic-league|FC Orenburg|0|3|Zenit St Petersburg|Round 2|Gazovik Stadium|Orenburg|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|3|2|Fakel Voronezh|Round 2|Ozon Arena|Krasnodar|Russia||premierliga-heritage-2627")
M.append("MATCH|2026-08-02|Russian Premier League|domestic-league|Akhmat Grozny|1|2|Spartak Moscow|Round 2|Akhmat Arena|Grozny|Russia||premierliga-heritage-2627")

body = L + M + ["END"]
text = "\n".join(body) + "\n"
with open(OUT, "w", encoding="ascii", newline="\n") as f:
    f.write(text)
sha = hashlib.sha256(text.encode("ascii")).hexdigest()
n_match = sum(1 for x in body if x.startswith("MATCH|"))
n_team = sum(1 for x in body if x.startswith("TEAM|"))
n_source = sum(1 for x in body if x.startswith("SOURCE|"))
n_note = sum(1 for x in body if x.startswith("NOTE|"))
print(f"OK {len(body)} lines, {n_match} MATCH, {n_team} TEAM, {n_source} SOURCE, {n_note} NOTE -> sha256 {sha}")
