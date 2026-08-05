# DATA VERIFICATION — the 5,000-row store, independently re-audited

**Version 1.0 — 2026-08-05 · Issued by: Auditor (new, zero inherited trust)**
**Subject:** `Supervior/other/pitch-rating-full.json` (sha256 `c7b29e85…8fc00` — hash verified identical to the SOT pin on arrival)
**Method:** fresh code only. No old-auditor script, no researcher artifact, no "registered" self-report was reused as evidence. Every row was re-verified against primary archives with parsers written in this session (`audit_work/rsssf_verify.py`, `audit_work/pack_parse.py`, `audit_work/legacy_diff.py` — kept in the repo for re-run).

---

## 1. What the store is (census, verified from the file)

| fact | value | proof |
|---|---|---|
| Total matches | **5,000** | store.matches |
| England | 1,900 (EPL 2021-22..2025-26) | per-competition count |
| Russia | 1,579 (RPL 1,216 + RUSCUP 341 + Relegation Playoffs 20 + Super Cups 2) | per-competition count |
| Czech Republic | 1,521 (First League 1,381 + Relegation Playoffs 20 + **MOL Cup 120**) | per-competition count |
| Identities | 589; every homeId/awayId resolves | set check |
| Duplicate fingerprints | 0 | date+home+away+comp |
| Future-dated rows | 0 | vs export date 2026-08-05 |
| Score sanity / missing fields | 0 bad / 0 missing | integer 0–30, required keys |
| Audit log | 55 entries, 0 unreconciled | store.log (migration 1,432 → 15 test rows → purges → 6 pack commits) |

**Store = the six adopted packs, byte-for-byte on every match row** (5,000/5,000 fingerprints + scores, 0 extras, 0 missing). No tampering between pack and store. The 120-row MOL Cup file is the OLD pack (M20, see §5).

---

## 2. Independent verification per league (what was checked against what)

| League | Rows | Primary archive (re-parsed fresh) | Independent second index | Result |
|---|---|---|---|---|
| **EPL** | 1,900 | — (see next column) | legacy 202k-match dataset, football-data.co.uk lineage (`export/01_matches.csv`, in-repo) | **1,900/1,900 EXACT** (date + sides + score) |
| **RPL** | 1,220 | RSSSF rus2022–rus2026 (all rounds + prorel) | same legacy dataset (football-data R1 feed, 2021–24) | **1,220/1,220 EXACT** vs RSSSF; 1,199/1,200 vs feed — single diff adjudicated, pack CORRECT (§4) |
| **RUSCUP** | 341 | RSSSF cup chapters rus2022–rus2026 (incl. two-leg combined prints) | transfermarkt / sport-express / championat / lenta for 3 date conflicts | **341/341 correct**: 338 EXACT; 3 RSSSF date misprints adjudicated, pack CORRECT (§4) |
| **CZ1** | 1,401 | RSSSF tsje2022–tsje2026 (30 rounds + Titul/Záchranu/Evropu + prorel) | worldfootball.net per-round pages; Wikipedia | **1,390 EXACT; 11 rows have +1-day date errors** (§3) — sides+scores correct everywhere; 2025-26 also table-reproduced 16/16 vs RSSSF final tables |
| **MOL Cup** | 120 | RSSSF tsje2022–2024 cup chapters (R16→Final) | molcup.cz official DB; Wikipedia; worldfootball (old auditor's wiki/wf gates re-spot-checked) | R16→Final surface EXACT incl. 90-min doctrine (7 AET ties carried at 90' score — pack CORRECT per official DB); R2/R3 rounds are not printed by RSSSF (wiki-sourced by design, spot-verified) |
| **RUS-ADDENDUM** | 18 | RSSSF rus2027 (2026-27 R1); rus2025/rus2026 #sup | legacy feed (R1), sportytrader/wincomparator (R2 spot), yenisafak (Super Cup date) | **18/18 correct** (R1 8/8, R2 8/8, Super Cups 2/2) |

Notes on method: the RSSSF re-parse is a genuinely independent transcription — season-year dates derived structurally (Jul–Dec = season-1 year, Jan–Jun = season-2), postponed-match blocks handled, accented transliterations normalised, two-leg combined prints expanded. Where the archive print and the pack disagreed, the dispute was adjudicated against a **third** source (worldfootball / Wikipedia / transfermarkt / Russian press) — never assumed.

---

## 3. DEFECT REGISTER — found in the adopted data (fix required)

**D-1 — CZ1 pack: 11 rows carry dates one day LATER than the true match dates** (sides and scores are correct; RSSSF, worldfootball and Wikipedia all agree on the correct dates):

| store id | pack date | correct date | match | source |
|---|---|---|---|---|
| m:357 | 2022-08-22 | **2022-08-21** | Zlin 2-2 Jablonec | rsssf-tsje2023 |
| m:355 | 2022-08-22 | **2022-08-21** | Sigma Olomouc 1-2 Slovacko | rsssf-tsje2023 |
| m:354 | 2022-08-22 | **2022-08-21** | Slovan Liberec 1-1 Ceske Budejovice | rsssf-tsje2023 |
| m:356 | 2022-08-22 | **2022-08-21** | Slavia Prague 7-0 Pardubice | rsssf-tsje2023 |
| m:505 | 2023-03-12 | **2023-03-11** | Sigma Olomouc 3-0 Ceske Budejovice | rsssf-tsje2023 |
| m:506 | 2023-03-12 | **2023-03-11** | Slavia Prague 2-1 Viktoria Plzen | rsssf-tsje2023 |
| m:507 | 2023-03-12 | **2023-03-11** | Zlin 2-2 Hradec Kralove | rsssf-tsje2023 |
| m:508 | 2023-03-13 | **2023-03-12** | Bohemians 1905 2-0 Pardubice | rsssf-tsje2023 |
| m:509 | 2023-03-13 | **2023-03-12** | Teplice 1-1 Zbrojovka Brno | rsssf-tsje2023 |
| m:719 | 2023-11-05 | **2023-11-04** | Sparta Prague 2-0 Bohemians 1905 | rsssf-tsje2024 |
| m:743 | 2023-12-10 | **2023-12-09** | Hradec Kralove 2-3 Banik Ostrava | rsssf-tsje2024 |

**STATUS: RESOLVED — owner approved the fix 2026-08-05.** Corrected store delivered: `Supervior/other/pitch-rating-full-D1-corrected-2026-08-05.json` — sha256 `abd0c207897148e1e490a5adc8f956e0756f97df4280b5960f31930047ce5b40` · md5 `51371f16826fbf58b512f03e98fc55b1` · 5,000 rows, only the 11 dates changed, original file untouched.

Impact (recorded pre-fix): dedupe fingerprints, fixture windows and any date-ordered computation shift by one day for these 11 rows. No score, team or result was affected.

**D-2 — M20 (confirmed, previously registered):** store carries the OLD 120-row MOL Cup file; the ADOPTED full-span pack (202 rows) is not imported. Missing 82 rows (2024-25 + 2025-26 rounds). Fix per SOT §10: import `MOLCUP-FULLSPAN.txt` → +82 → store total 5,082.

**D-3 — 3 legacy seed rows were destroyed by the purge programme (already registered):** old-store integrity/mute rows for RPL died with the Russia purge; the new Russian data has never been through an outcomes-only integrity screen (M10/A-05). Not a data-falsity issue — logged for the M10 screen.

---

## 4. ADJUDICATION REGISTER — rows where the archive and the pack disagreed, and the pack is RIGHT (no fix)

| row | archive says | reality (third source) | verdict |
|---|---|---|---|
| Pari NN 0-3 Torpedo (2023-03-19, RPL) | football-data feed: 1-1 | RSSSF: *"Awarded, Pari NN fielded a disqualified player. Original score canceled (1-1)"* | pack = official record ✓ |
| Ural 2-1 Spartak (2023-04-04, RUSCUP SF leg 2) | RSSSF header [Apr 5] | transfermarkt: 04.04.2023, 2:1 | pack date ✓, RSSSF misprint |
| CSKA 1-0 Krylia (2023-04-05, RUSCUP SF leg 2) | RSSSF header [Apr 6] | Grokipedia/Wikipedia: 5 April 2023 | pack date ✓, RSSSF misprint |
| Krasnodar 0-0 Akron [4-2 pen] (2023-05-03, RUSCUP regions final) | RSSSF header [May 4] | sport-express / championat / lenta: 3 мая 2023 | pack date ✓, RSSSF misprint |
| 7 MOL Cup AET ties (e.g. Slovacko 1-1 Karvina; Hradec 1-1 Bohemians; Slavia 2-2 Sparta…) | RSSSF prints after-ET scores (3-1, 2-1, 2-3…) | molcup.cz official DB shows ET goals after 90' | pack = 90-minute doctrine ✓ |

---

## 5. VERDICT

1. **No fabricated rows, no invented results, no wrong scores, no wrong teams, no wrong competitions were found in the 5,000-row store.** Every row traces to a real played match.
2. **One data-quality defect class was found that the previous auditor's gates missed: 11 CZ1 rows with +1-day date errors** (D-1). The old CZ1 gates verified tables (140/140) and playoff legs, but never machine-checked regular-round dates; this re-audit did, and found the 11. **FIXED 2026-08-05** (owner-approved; corrected store `pitch-rating-full-D1-corrected-2026-08-05.json`, sha256 `abd0c207…`).
3. One previously-registered defect is confirmed in the store (D-2, MOL Cup 120 vs 202). **STATUS: RESOLVED 2026-08-05.** The 82 missing rows (2024-25 + 2025-26, `MOLCUP-FULLSPAN.txt` — ADOPTED) are merged into the D-1 store; final file `previous_work_files/workspace-recent-019fd033-…/pitch-rating-full-5082-D1D2-2026-08-05.json` — sha256 `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` · md5 `3c068c1f67ee8a81d412631fd0feb162` · **5,082 rows** (ENG 1,900 · CZE 1,603 · RUS 1,579), 0 duplicate fingerprints, all ids resolve. The 82 rows re-verified vs RSSSF tsje2025/tsje2026 cup chapters: R16+ rows exact under the 90-min doctrine (5 AET ties confirmed by `[aet]` prints + pack advancement NOTEs); R2/R3 rows are RSSSF-unprinted by design (wiki + worldfootball cross-verified per the pack's `source_adaptation` NOTE and audit card ADDENDUM-1). Ten lower-division opponents (Horovice, Police nad Metuji, Benatky nad Jizerou, Uhersky Brod, Horni Redice, Hlinsko, Karlovy Vary, Nove Sady, Petrin Plzen) minted as minimal app-style identities (pack carries no TEAM rows for them — same precedent as store's Trinec/Frydek-Mistek).
4. The old auditor's own instrument had known date-window artifacts on EPL baselines (43 rows, superseded) — irrelevant to the store, which is built from the packs, not the baselines.
5. **The data is fit for the engine, once D-1 and D-2 are applied.** Recommend: correct D-1 (in-place), import FULLSPAN (D-2), then the masked-replay regeneration (M5) and the M10 outcomes-only screen before any new league data enters.

*Verification scripts (fresh, re-runnable): `audit_work/pack_parse.py`, `audit_work/rsssf_verify.py`, `audit_work/legacy_diff.py`. Every number above is produced by those scripts or by the cited third sources; nothing is asserted from memory.*
