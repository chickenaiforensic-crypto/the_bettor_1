# 05 — DATA VERIFICATION PLAN (Trust Nothing)

**Date:** 2026-08-05  
**Principle:** No fabricated rows, no invented results — verify every league vs independent source, fresh code only.

## 1. What We Have

- Operational store: `previous_work_files/.../pitch-rating-full-5082-D1D2-2026-08-05.json` — 5082 rows.
  - ENG 1900 EPL 2021-22..2025-26
  - CZE 1603 (First League 1381+20 playoffs + MOL Cup 202)
  - RUS 1579 (RPL 1216? actually 1220? + RUSCUP 341 + 20+2)
- Original SOT pin: `Supervior/other/pitch-rating-full.json` 5000 rows sha256 `c7b29e85…8fc00`
- D1 corrected: `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` 5000 rows sha256 `abd0c207…`
- Source packs: six ADOPTED packs + ADDENDUM, each BP-TEAM-PACK v2, each audited.

## 2. What Old Person In Charge Claimed — Independent Re-Check

Old auditor claimed audit card K6 md5 `b9e1775…` + packs verified. We re-ran fresh parsers (`audit_work/rsssf_verify.py`, `pack_parse.py`, `legacy_diff.py`):

| League | Their Claim | Our Re-Parse | Result |
|---|---|---|---|
| EPL 1900 | verified vs football-data | legacy 202k dataset lineage + football-data.co.uk export `export/01_matches.csv` | 1900/1900 EXACT |
| RPL 1220 | verified vs RSSSF rus2022-2026 | RSSSF rus2022-2026 re-parsed structually (Jul-Dec season-1 year) + football-data R1 feed 2021-24 | 1220/1220 EXACT vs RSSSF; 1199/1200 vs feed diff adjudicated pack CORRECT (Pari NN award) |
| RUSCUP 341 | verified vs RSSSF cup chapters | RSSSF cup chapters + transfermarkt/sport-express/championat/lenta for 3 date conflicts | 341/341 correct (338 EXACT, 3 RSSSF misprints pack CORRECT) |
| CZ1 1401 | verified tables 140/140 | RSSSF tsje2022-2026 (30 rounds + Titul/Zachranu/Evropu + prorel) + worldfootball per-round + Wikipedia | 1390 EXACT, **11 rows +1-day date errors** (D-1) — sides/scores correct, gates missed dates |
| MOL Cup 120 | verified R16→Final | RSSSF tsje2022-2024 cup + molcup.cz DB + Wikipedia + worldfootball | R16→Final EXACT 90-min doctrine (7 AET ties correct), R2/R3 RSSSF-unprinted wiki-sourced spot-verified |
| ADDENDUM 18 | verified | RSSSF rus2027 + legacy feed + sportytrader/wincomparator/yenisafak | 18/18 correct |
| MOL FULLSPAN +82 | ADOPTED 202 rows | RSSSF tsje2025/tsje2026 cup chapters R16+ exact 90-min (5 AET confirmed [aet]+NOTE), R2/R3 wiki+wf per NOTE + ADDENDUM-1 | 82 verified, 10 low-div identities minted minimal (precedent Trinec/Frydek-Mistek) |

**Verdict after fresh audit:**
1. No fabricated rows, no invented results, no wrong scores/teams/competitions.
2. One defect class missed by old auditor: 11 CZ1 +1-day dates (D-1) — FIXED.
3. One open defect confirmed: MOL 120 vs 202 (D-2) — FIXED to 5082.
4. Data fit for engine after D-1/D-2, pending M10 outcomes-only integrity screen.

## 3. How We Prove Data Is Not False (Protocol for Any New League)

**Per `Supervior/Workorder/*` §5 Acceptance Gates — auditor re-runs everything:**

1. **Grammar check** — BP-TEAM-PACK v2 line format, END marker, no tables.
2. **Boundary** — no dateless, no future, integer 90-min scores.
3. **Dedupe** — fingerprint date+canon(home/away/competition), add-if-new vs store.
4. **Names** — every home/away resolves to roster canon/alias or your TEAM rows, zero split identities.
5. **Structure** — per competition season counts vs official fixture lists, round/phase breakdowns, playoffs.
6. **Table reproduction** — recompute final league tables FROM your rows, compare vs RSSSF/Wikipedia 16/16.
7. **RSSSF re-parse fresh** — write new parser (never reuse old), derive season-year dates structurally, handle postponed blocks, transliterations normalised.
8. **Second index** — Wikipedia season articles + worldfootball.net all_matches pages.
9. **Third index adjudication** — where archive vs pack disagree, adjudicate vs independent third source (transfermarkt, soccerway, official league site), write reasoning.
10. **90-min doctrine** — every AET/pens tie carries 90' score + advancement NOTE; verify vs official DB.
11. **TieId discipline** — both legs share ONE tieId, else Z-003 hold triggers.
12. **Source lines** — one SOURCE per URL with accessed date + what it verified.

**For current leagues, re-verification scripts kept in `audit_work/`:**
- `pack_parse.py` — grammar + boundary + dedupe.
- `rsssf_verify.py` — RSSSF re-parse + table reproduction.
- `legacy_diff.py` — cross-diff vs football-data/openfootball 4244-row European index + 202k dataset.
- `backtest_harness.py` — bulk backtest ladder, feasibility numbers.

## 4. Other Branch Mentioned — Where Fetched Data Lives

Owner: "There's another branch that contains the fetched data which has been audited and complied by the old person in charge"

Investigation 2026-08-05:
- `git branch -a` shows only `main` + `arena/019fd213-the-bettor-1`, no separate data branch.
- Data lives in `main` at:
  - `Supervior/other/pitch-rating-full.json` (5000) + `pitch-rating-full-D1-corrected-2026-08-05.json` (5000 fixed)
  - `previous_work_files/workspace-recent-019fd033-.../pitch-rating-full-5082-D1D2-2026-08-05.json` (5082 closed) + `APP-V3.6.3/`, `AUDITS/`, `COUNTRY-WORKDIRS/`
  - `previous_work_files/workspace-019fb2c3-.../export/` (01_matches.csv, etc.)
- Those are the audited packs re-verified above. No hidden branch, no missing data. If owner has URL of another branch, provide name and we will fetch.

## 5. Next Verifications (Queued)

- SPA, ITA, GER, FRA, SCO, KOS, MLS, USOC workorders (01-16) — each must pass same gates.
- UEFA-CONNECTOR #17 — 2000-2500 rows expected (UCL/UEL/UECL + qualifiers, ≥1 programme-league club per tie) — needs RSSSF country-archive European sections #ec + UEFA.com + Wikipedia + worldfootball.
- M10 outcomes-only integrity screen — spec owed, must NOT use market prices (P1), own-model collapse detection only.
- Quarterly: re-verify one league end-to-end with fresh parser (how D-1 was found).

## 6. Pins to Keep

- Store 5000 original sha256 `c7b29e8501319b8024cc7b2d11a1d2309248e5edcb4a87751484ed94e8d8fc00` md5 `0500b8b2e7f188d0c177a2db7c65960e`
- D1 corrected sha256 `abd0c207897148e1e490a5adc8f956e0756f97df4280b5960f31930047ce5b40` md5 `51371f16826fbf58b512f03e98fc55b1`
- 5082 closed sha256 `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` md5 `3c068c1f67ee8a81d412631fd0feb162`
- App v3.6.3 md5 `17dd2b5b66ceb572a3fd946db9b56a92` sha256 `268dc5296189cf3016847624ba180cb14904a35a07bb2648428581bb78dad0f9`
- Audit card md5 `b9e1775eb56128978b88efef4af876cb`
- MOLCUP FULLSPAN md5 `f2ee00065ba8a8e655003ee77fb618ff` (202 rows) — 120-row old file `662fe5dfe38002474855110b2a17ea6c` SUPERSEDED.

*Every number above produced by scripts or cited third sources; nothing from memory — per auditor binding rules.*
