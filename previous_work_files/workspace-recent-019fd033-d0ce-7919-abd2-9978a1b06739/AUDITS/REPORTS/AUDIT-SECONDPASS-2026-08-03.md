# AUDIT CARD — SECOND PASS waves 1+2 (2026-08-03, evening/night) — bulk machine diffs
Queued items cleared by auditor, all gates re-run locally. Scripts retained for replay: `ruscup_bulk_diff.py`, `molcup_wiki_diff.py`, `cz1_groups_diff.py`.

## 1. RUSCUP 2022-23 + 2023-24 — FULL bracket diff vs RSSSF — **153/153 VERIFIED**
(First pass had verified 2021-22 row-exact + spot suites; the two later seasons were the open bulk items.)
| Season | Ties | Result |
|---|---|---|
| 2023-24 | 76 | **76/76 EXACT — zero divergence** (48 group + 16 QF + 8 SF + 3 finals + Superfinal) |
| 2022-23 | 77 | **77/77 verified**: 74 exact + 3 one-day date conflicts, ALL adjudicated to the pack's favour — RSSSF's compact headers misprint (Ural-Spartak "Apr 5", CSKA-Krylya "Apr 6", Krasnodar-Akron "[May 4]") vs its own Details meta lines (**04.04.23 / 05.04.23 / 03.05.23**). The pack follows the correct Details dates in all three. Internal-RSSSF inconsistency, not a pack defect. |

Parser traps fixed en route (no data impact): TOC anchor collision, two-leg date-pair syntax `[Feb 22, 27]`, home-perspective leg-2 flip, `[D2]`/`[Agg]/[Pen]` markers on club names, digit-leading club names.

## 2. MOLCUP R2/R3 (78 rows) — bulk diff vs en.wiki season pages (second index) — **129/129 ACCOUNTED, 0 contradictions**
(worldfootball — the third index — is Cloudflare-blocked from this sandbox, so the truly independent 90-minute re-split stays open; honest limitation.)
- **59 EXACT** date+score+order · **5 AET-OK** (pack 90-min draw + NOTE aet-score = wiki final) · **9 alias-adjudicated present** (era names Loko Vltavín/Fastav Zlín/FC Viagem Příbram etc. plus pens-marker ties; every one grep-confirmed in-pack) · **4 pens-consistent** (NOTE pens score = wiki pso) · **47 excluded-OK** (every absent tie re-checked as no-top-flight for that specific season — season-aware sets: Zbrojovka FL only 22-23, Karviná out 22-23, Zlín/Zbrojovka out 23-24 ✓ matches the pack's slice rule exactly)
- **0 missing · 0 score conflicts · 0 date conflicts.** Pack's own `spot_audit` NOTE re-lists all R3s with the out-of-slice notices included.
- **90-min residual:** for 20 aet/pens ties the exact 90-minute number rests on wf goal timelines (blocked). What wiki proves: each such pack row is a draw with a consistent winner + correct final score — i.e. doctrine-compliant shape; only the digit-level 90-min value re-verification remains open.
- Nit (text-only, no row impact): pack identity NOTE lists reused identity "**Lanznot**" (sic — Sokol Lanžhot; tie is correctly out-of-slice) and names a few identities that never appear on rows; cosmetic.

## 4. WAVE 2a — CZ1 Titul (championship) + Záchranu (relegation) groups, 2022-23/2023-24/2024-25 — **90/90 EXACT**
Bulk diff of the pack's group-phase rows against the RSSSF round-by-round listings on tsje2023/24/25 (`cz1_groups_diff.py`): 3 seasons × 30 group games (Titul 5 rds × 4 + Záchranu 5 rds × 2) — **all 90 identical on date, sides and score**. Together with the first-pass main-phase diffs and the 12-row playoff patch (`AUDIT-CZ1-PATCH-2026-08-03.md`), the entire CZ1 829+12-row return is now machine-verified end-to-end against the primary source. No divergence of any kind.

## 5. WAVE 2b — Russia span-diff (held store vs researcher control CSVs, adjudicated at RSSSF) — **480/480 CLOSED: 464 exact + 16 proven HELD-DATA date defects**
Compared every held-store RPL league row for 2024-25 and 2025-26 (240 + 240 = 480) against the researcher's independent control CSVs (`data/rpl/RPL-2024-25.csv`, `RPL-2025-26.csv`, pulled from branch to `repo-check/`), then re-adjudicated every disagreement at the RSSSF primary (rus2025.txt / rus2026.txt, fetched fresh this session).

| Verdict | Count | Detail |
|---|---|---|
| EXACT (all fields incl. dates) | 464 | every score in both full seasons also byte-identical — **no score errors anywhere** |
| Date conflicts | **16** | **all 16 adjudicated AGAINST the held data** — see defect ledger below |

**Defect ledger — 16 misdated held rows (old builder seed, NOT any of the 4 new packs):**
- **RPL 2024-25, Round 30 — 8 rows dated `2025-05-19`, true date `2025-05-24`** (a Monday vs the actual Saturday; −5 days). RSSSF rus2025.txt L745: `Round 30 [May 24…]` followed by all 8 fixtures: Krasnodar 3-0 Dinamo Ms · Zenit 3-0 Ahmat · CSKA 2-0 Pari NN · Spartak 5-0 Himki · Akron 1-4 Lokomotiv · Rubin 4-2 Orenburg · Dinamo Mh 1-1 Rostov · Fakel 1-1 Krylja S. Held scores/sides match exactly — only the date is wrong.
- **RPL 2025-26, Round 30 — 8 rows dated `2026-05-11`, true date `2026-05-17`** (−6 days). RSSSF rus2026.txt L740: `Round 30 [May 17…]` with all 8 fixtures: Rostov 0-1 Zenit · Krasnodar 3-0 Orenburg · CSKA 3-1 Lokomotiv · Dinamo Mh 0-0 Spartak · Baltika 1-2 Dinamo Ms · Rubin 2-2 Pari NN · Soci 1-1 Ahmat · Krylja S. 4-1 Akron. Held scores/sides match exactly — only the date is wrong.
- **Lookalike rows cleared (NOT defects):** 5 further held rows share those two wrong dates but are *correctly* dated Round-29 games that genuinely kicked off on those Mondays — `Lokomotiv 2-2 CSKA` (rus2025.txt L741 `[May 19]`, inside the R29 block) and `Spartak 2-1 Rubin`, `Pari NN 1-2 CSKA`, `Akron 1-3 Rostov`, `Dinamo M 2-1 Krasnodar` (rus2026.txt L729 `[May 11]`, R29 block). The control CSVs agree; only the 16 R30 octets diverge.

**Collision / contamination check (ran BEFORE clearing any import):**
- RPL return pack covers 2021-07-23 → 2024-06-01 only (732 rows: 720 league + 12 relegation playoffs) → **zero overlap with the misdated rows; the 4-pack import cannot duplicate or overwrite them.** Import stays cleared.
- Held store currently holds **no rows on the true dates** (0 on 2025-05-24 or 2026-05-17) → a correction, when applied, will not collide with existing rows.
- App dedup is date-keyed → **do NOT fix by importing a 16-row "correction pack"** — it would ADD corrected copies and leave the misdated originals live = duplicate fixtures. Repair must edit the 16 stored rows in place (date field only) or MUTE-and-re-add. **Owner/builder decision; auditor recommends app-side in-place edit of the 16 dates.** Scores untouched.

**Impact note:** results-only engine; both wrong dates are Mondays ~1 week off in dead-rubber final rounds. Win/draw/loss and scorelines are all correct — any form/ratings computed are right on results, only match-day alignment is off by 5–6 days.

## 6. Still open after wave 3
- **Repair of the 16 misdated held rows** — pending owner/builder decision (recommended: in-place date edit, no re-import).
- MOLCUP wf 90-min splits (20 ties) + R2/R3 third-index diff — **needs a non-blocked fetcher**: request to researcher already queued (worldfootball is Cloudflare-blocked from this sandbox).

## 7. WAVE 3 (2026-08-03 night) — Russia forward edge + Super Cup 2026 existence check, both CLOSED
Newly fetched `rsssf-ref/rus2027.html/.txt` (Russia 2026-27 page, 94.5 KB, UTF-16).

**7a. Held 2026-27 RPL rows — 9/9 VERIFIED** (same old builder seed as the section-5 defect; clean here):
| Round | Held rows | Verdict |
|---|---|---|
| R1 (Jul 24-26) | 8 | **8/8 EXACT** vs rus2027.txt round block (CSKA 2-1 Baltika · Akron 0-5 Zenit · Spartak 3-0 Rodina · Dinamo Ms 0-0 Krylja S. · Fakel 1-2 Dinamo Mh · Rubin 1-3 Krasnodar · Lokomotiv 1-1 Ahmat · Orenburg 2-1 Rostov — dates+sides+scores) |
| R2 (window Jul 31 - Aug 3) | 1 (Akron 1-2 Rubin, dated 2026-08-01) | Fixture listed in the rss2027 R2 block; RSSSF page not yet updated with R2 results → second-index confirmation at en.wiki 2026-27 RPL results grid: `match_AKR_RUB = 1-2`. **CONFIRMED; date inside the official round window.** |

Season-context notes (rus2027): promoted clubs Fakel Voronezh + Rodina Moscow (`[P]`); Pari Nizhny Novgorod and PFC Sochi no longer in the division; Akron play home games at Krylja Sovetov's stadium (Samara). R2 closes tonight (round window ends Aug 3).

**7b. 2026 Russian Super Cup — EXISTS, and was MISSING from the held store.**
RSSSF records it at the **end of the 2025-26 file** (`rsssf-ref/rus2026.txt` `#sup`, lines 4883-4900 — a grep of the 2026-27 page finds nothing; placement quirk noted for all future checks). Full detail transcribed: **OLIMPBET RUSSIAN SUPER CUP 2026 — Zenit (SPb) 1-1 Spartak (Moscow) [pen 4-2]**, goals Sobolev 90+8 pen - Martins 25; complete shoot-out ledger present; meta `18.07.26. Nizhnij Novgorod Stadium, Nizhnij Novgorod. Att: 42,139`. Held store carried only the 2025-07-12 edition (Krasnodar 0-1 CSKA). Store had 0 Russian rows on 2026-07-18 → no duplicate possible.
**Action taken (auditor):** 1-row mini-pack authored to blueprint grammar — `IMPORT-READY-SUPERCUP-2026/SUPERCUP-2026_BP-TEAM-PACK_v1.txt` (md5 `1628348112fc3181dec04b5ce868f4ce`): 90-min 1-1 row + mandatory `NOTE|info|advancement` (pens 4-2, Zenit trophy) + provenance SOURCE line. Gates: END present, both club strings byte-resolve against the roster, no overlap, single row = no hold-rule trigger. Owner may drop it any time after the 4-pack import (order irrelevant; expected Coverage 3,329 → 3,330). closes the weekly central-request cycle item.

**7c. EPL pre-position (⑤ incoming):** RSSSF `eng2022`-`eng2025` fetched to `rsssf-ref/` (2021-22 … 2024-25 full season pages; 48-50 `^Round` blocks each — matches the researcher's transcribed ledgers). `eng2026` page currently skeletal (8 round blocks, 24 KB) — flag for the 2025-26 EPL segment: if the researcher's pack covers 2025-26, its primary diff may need a second fetch once RSSSF completes the page, or the wiki second index in the interim.

## 8. WAVE 4 (2026-08-03 late night) — EPL auditor baselines LOCKED · R30 repair spec shipped · MOLCUP third-index detour result

**8a. EPL baselines (`audit-baseline/epl-*.json`, script `epl_baseline.py`, replayable):** 2021-22, 2022-23, 2023-24, 2024-25 — **4 × (380/380 matches, 0 dupes, printed Final Table reproduced 20/20 on W-D-L-GF-GA derived purely from round listings)** → ALL LOCKED. The ⑤ audit-vs-pack can now run as a direct machine diff within minutes of the pack landing. Logged irregularities are exactly the documented ones: Everton −8 + Nottingham Forest −4 point deductions (2023-24 — reported, not merged), and the 2023-12-16 Bournemouth–Luton abandonment (Tom Lockyer) excluded with the 4-3 replay counted. Parser lesson retained in-script: 'Wolverhampton' overflows RSSSF's 12-char name column (single-space before score) — cost 19 lines/season until caught.

**8b. REPAIR-SPEC-R30-2026-08-03.md shipped** (md5 `504403c1…`): the 16 misdated held rows fully enumerated (homeId/awayId/score/wrong→correct date/round) + Route A (in-place date edit, recommended) / Route B (MUTE+re-add) + no-correction-import warning + post-repair self-check for owner. Awaits owner/builder route call.

**8c. MOLCUP third-index detour (bonus probe, not the assigned path):** official **molcup.cz results DB is reachable from this sandbox** (fotbal.cz 403). Current-season listing parses fully (158 rows: dates, stages, full club-name title attrs, scores, `PEN`/`pp.` end markers) — but its legacy-season slices are widget-driven (`data.esportsmedia.cz/data/import.js`, now 404; server echoes filter selections yet keeps serving 2026-27 rows) → not retrievable here without browser JS. **Decision:** 20-tie 90-min residual STAYS with the researcher (worldfootball fetch as assigned); he may find molcup.cz easier since it is not Cloudflare-blocked — added to his request. This is an option, not a change of plan.

## 9. WAVE 5 (2026-08-04-ish, night) — majors pre-positioned: 16 more auditor baselines LOCKED + full workorder map recovered

**9a. Workorder map recovered from branch tree** (`supervisor/workorders/` + root `WORKORDER-STATUS.md`, mirrored to `repo-check/`): the 16-workorder queue is exactly = RPL✅ CZ1✅ RUSCUP✅(override) MOLCUP✅ EPL ⑤ **next** → FRA · GER · ITA · KOS · KOSCUP · MLS · SCO1 · SCOCUP · SCOLC · SPA · USOC. All five majors' WOs demand **2021-22 → 2023-24 backfill segments** (their 2024-26 blocks are NOT held client-side — export census confirms **zero rows** for EPL/LaLiga/SerieA/Bundesliga/Ligue1; only RPL/CZ1/Scottish/MLS/small-buckets exist held). Implication: majors' packs arrive complete-but-backfill-only; nothing to span-diff on import; Coverage jumps will be pure adds.

**9b. RSSSF majors fetched + normalised** (rsssf-ref/): Spain = `tabless/span<Y>`, Italy = `tablesi/ital<Y>` (NOT spa/ita — 404s logged); Germany `tablesd/duit<Y>`, France `tablesf/fran<Y>`; mixed encodings (UTF-16/UTF-8/latin-1) smart-decoded to UTF-8 .txt. **Gaps flagged now, not later:** `span2026` = 404 (no Spain 2025/26 page yet); `ital2026`/`duit2026`/`fran2026` exist but are SKELETAL (early-format pages).

**9c. `league_baseline.py` (replays from file) — 16/16 SEASONS PASS** → baselines in `audit-baseline/`:
| League | Seasons | Matches | Gate |
|---|---|---|---|
| La Liga | 2021-22, 2022-23, 2023-24, 2024-25 | 4 × 380/380 | tables 20/20 each, 0 dupes |
| Serie A | same | 4 × 380/380 | 20/20; Juventus −10 (2022-23) reported not merged |
| Bundesliga | same | 4 × 306/306 | 18/18 |
| Ligue 1 | same | 380+380+306+306 | 20/20+20/20+18/18+18/18 (18-club era from 2023-24) |

Every logged anomaly is a REAL documented event, all dates self-consistent: Granada–Athletic abd (fan, 2023-12-10, excluded/replay counted) · Udinese–Roma abd (Ndicka, 2024-04-14) · Fiorentina–Inter abd (Bove, 2024-12-01) · Bochum 0-2 Gladbach counted-after-abandonment (result stood) · **Union 0-2 Bochum AWARDED** (lighter/Drewes case, 2024-12-14 — `awd` grammar) · Nice −1 / Lyon −1 Nice-Marseille & Lyon-Marseille crowd cases · Montpellier–Clermont abd + Montpellier −1 deduction · Montpellier 0-2 St-Étienne counted (result stood). Frozen alias sets: `audit-baseline/majors-aliases.json` (4 leagues, 99 shortform→official mappings incl. digit-starting clubs '1. FC Köln' etc.).
Total auditor pre-computed baselines now: **20 seasons, 7,256 matches, all table-verified** (4 EPL + these 16) — every league pack ⑤→⑧(+ FRA/ITA/SPA/GER) now audits as a same-day machine diff.

**9d. MOLCUP third index:** is.fotbal.cz dead (000); molcup.cz legacy slices stay widget-locked from here → residual assignment unchanged (researcher/wf; molcup.cz option noted to him).
