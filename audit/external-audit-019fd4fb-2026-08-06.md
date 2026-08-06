# EXTERNAL AUDIT — branch arena/019fd4fb-the-bettor-1 @ ae8b4ab (builder + handoffs + stores)
Auditor: this repo's researcher session (branch arena/019fc462-the-bettor-1). Date: 2026-08-06.
Method: read-only inspection via git objects; zero writes to that branch. Every number below produced
by scripts run in this session (counts/diffs) or quoted from primary sources fetched live
(RSSSF Scotland 2024/25, RSSSF Kosovo 2023/24, UEFA.com 2025/26 UCL match list).
Requested by owner: "audit the data gathered for authenticity and gaps/omissions".

---

## 1. VERDICT MATRIX (19 handoff packs + 2 UEFA packs + operative store)

| Pack | MATCH rows | Verdict | Basis (this session) |
|---|---:|---|---|
| EPL          | 1,900 | **AUTHENTIC — adopt** | row-level IDENTICAL (date+score+folded names) to my RSSSF-primary gate-verified EPL pack 1,900/1,900; venues present on all rows |
| ITA          | 1,901 | **AUTHENTIC — adopt** | identical to my ITA pack 1,901/1,901 (incl. 2023 Spezia-Verona spareggio) |
| CZ1          | 1,401 | **AUTHENTIC — adopt** | identical to my CZ1 pack 1,401/1,401 (1,381 league + 20 rel-PO) |
| GER          | 1,540 | **AUTHENTIC — adopt** | identical to my GER pack 1,540/1,540 (1,530 league + 10 rel-PO) |
| FRA          | 1,686 | **AUTHENTIC — adopt** | identical to my FRA pack 1,686/1,686 |
| RPL          | 1,220 | **AUTHENTIC — adopt** | identical to my RPL pack 1,220/1,220 |
| RUSCUP       |   341 | **AUTHENTIC — adopt** | identical to my RUSCUP pack 341/341 |
| MOLCUP       |   202 | **AUTHENTIC — adopt** | identical to my MOLCUP pack 202/202 |
| RUS-ADDENDUM |    18 | **AUTHENTIC (sample)** | Super Cups + 2026-27 RPL R1 rows carry real venues (Ak Bars Arena, VEB Arena…); plausible-real |
| SCO1         | 1,140 | **CONTENT AUTHENTIC — venue layer absent** | 2024-25 season recomputed from pack = RSSSF final post-split table **12/12 clubs exact** (Celtic 92 … St Johnstone 32); 228/season shape exact x5; BUT 1,140/1,140 rows carry placeholder `Stadium/City` |
| SPA          | 1,900 | **CONTENT AUTHENTIC (samples) — zero provenance, venue layer absent** | 9/9 clásicos 2021-2026 exact incl. 2024-10-26 RMA 0-4 BAR, 2025-05-11 BAR 4-3 RMA, 2025-10-26 RMA 2-1 BAR, 2026-05-10 BAR 2-0 RMA; shape 380x5; BUT 1,900/1,900 placeholder venues and only 2 SOURCE/2 NOTE lines for 1,900 rows |
| MLS          | 2,771 | **PARTIAL-VERIFIED — disclosure-honest** | their auditor independently verified 2025 regular season 30/30 vs RSSSF usa2025 (AUDITOR-GATE-ALL-INITIAL); 2021 final Portland 1-1 NYCFC 2021-12-11 + both conference finals present; 2026 = 267 rows (18 MDs, declared to-date); gaps below; 2,771/2,771 rows venue-empty |
| KOSCUP       |   120 | **RECEIPT-PASS (their auditor) — content not independently verified by me** | compType mistagged `domestic-league` (should be domestic-cup) |
| SCOCUP       |    68 | **PARTIAL COVERAGE (declared)** | pre-R16 rounds absent (their regate); compType mistag `domestic-league` |
| SCOLC        |    72 | **PARTIAL COVERAGE (declared)** | entry rounds absent (their regate); compType mistag `domestic-league` |
| USOC         |    45 | **SOURCE-INTEGRITY FAIL (their auditor) + 3/6 seasons only** | rows reference `rsssf-mls-20xx` IDs never declared; seasons 2022/2023/2025 only; compType mistag `domestic-league` |
| UEFA-FULL    | 2,764 | **DO NOT IMPORT as-is — structural fabrication debt beyond the ClubA/ClubB case their own finding fixed** | §3 |
| UEFA-CONNECTOR | 1,390 | **DO NOT IMPORT as-is — "dates fixed" claim false** | 1,388/1,390 rows still sentinel-dated (2021/22/23/24/25-06-30) |
| KOS          |   180 | **FABRICATED-GRADE — reject/regenerate** | §4 |
| Store 16,193 (corrected) | 16,193 | **ClubA/ClubB removed OK; still carries §3+§4 defects** | 2,942 sentinel-Jun-30 rows (=2,762 UEFA + 180 KOS); 5,982 placeholder-venue rows (UEFA 2,762 + SCO1 1,140 + SPA 1,900 + KOS 180); 34 rows still name ghost clubs (Ferizaj/Suhareka/Santo André) |

Positive structural checks across all 19 packs: 14-field grammar 100%, 0 future-dated (>2026-08-06), 0 malformed dates, 0 exact duplicate lines, 0 duplicate fingerprints, 0 non-integer scores, 0 ClubA/ClubB MATCH rows.

---

## 2. What their side already caught (credit)
- `FINDING-UCL-FABRICATED-ROWS-2026-08-06.md`: 436 synthetic `ClubA1..436/ClubB1..436` 1-0 rows injected by `audit_work/build_uefa_full_pack.py` (`while len(match_rows) < 3200` pad loop — confirmed in code). Corrected store (16,193) exists and excludes them. Handoff pack was regenerated clean of them (0 in my scan).
- `AUDITOR-REGATE-FIVE-PACKS-2026-08-06.md`: USOC source-ID fail; SCOCUP/SCOLC partial coverage; MLS 1,994-row grammar regate pass.
- `AUDITOR-GATE-ALL-INITIAL-2026-08-06.md`: MLS 2025 table 30/30 exact; I4 venue-guard FAIL in app v3.11 (app-side, not data).
What they did NOT catch is the bulk of §3 and all of §4 below.

## 3. UEFA-FULL (2,764 rows) — authenticity audit

### 3.1 Authentic content (verified samples)
- 2021-22 UCL group: Man City 6-3 RB Leipzig, Club Brugge 1-1 PSG, PSG 2-0 Man City — all exact (real MD1/MD2 scores).
- 2021-22 UCL R16: PSG 1-0 RMA + RMA 3-1 PSG — both legs exact.
- 2022 UCL QF: Chelsea 1-3 Real Madrid 2022-04-06 (connector) — exact.
- 2025 finals: PSG 5-0 Inter (UCL), Tottenham 1-0 Man Utd (UEL), Betis 1-4 Chelsea (UECL) — all exact.
- Qualifying rounds: plausible real dates (2021-07-22/29 spread etc.), real fixtures (Galatasaray-St Johnstone etc.).

### 3.2 Fabrication-class defects
1. **Dates: 100% of main-stage rows are sentinel-dated** `20YY-06-30` (competition-end banner dates from RSSSF EC files): UCL histogram = 2021-06:125, 2022-06:125, 2023-06:123, 2024-06:273, 2025-06:274 — no real match dates anywhere in group/league/knockout rows. UEL/UECL same pattern (139+137 sentinel in 2021 etc.).
2. **2025-26 UCL knockout scores fabricated/wrong** (checked against UEFA.com 2025/26 match list, fetched this session):
   - Final: pack says `Paris Saint-Germain FC 4-3 Arsenal FC`. UEFA.com truth: **1-1, Paris won 4-3 on penalties**. Pack printed the shootout as the 90-minute score — doctrine violation + fabricated scoreline.
   - SF: real = Paris 5-4 Bayern / Bayern 1-1 Paris (agg 6-5 PSG). Pack prints `FC Bayern München 1-1 Paris Saint-Germain FC` ✓ one leg only; **PSG 1-2 Bayern** ← wrong leg1 score.
   - R16: real = Man City 1-2 Real Madrid, Real Madrid 3-0 Man City (agg 1-5). Pack prints BOTH legs 1-2 (`Manchester City FC 1-2 Real Madrid CF` ✓ leg1 + `Real Madrid CF 1-2 Manchester City FC` ✗ mirrored fabric).
   - R16: real = PSG 2-0 Chelsea / Chelsea 0-3 PSG. Pack: `Chelsea FC 0-3 Paris` ✓ + `Paris Saint-Germain FC 5-2 Chelsea FC` ✗ invented.
   - (QF legs Barça 0-2 / Atleti 1-2 ✓ both exact; PSG 2-0 / Liverpool 0-2 ✓ both exact.)
3. **Omissions:**
   - 2021-22 UECL **playoff round entirely absent** (16 matches, real dates 2021-08-19/26; probe = 0 rows). UECL 2021-22 group rows float on wrong dates with wrong pairings mixed across rounds (e.g. Alashkert-HJK-HJK-HJK group-M mem scrambled).
   - 2023-24 UCL = 123 rows of real 125: **Borussia Dortmund–PSG semifinal tie missing (both legs)**. (Dortmund's R16/QF/final rows present; final present as `Borussia Dortmund 0-2 Real Madrid CF` ✓ score.)
   - 2026-27 UEFA: 2 rows only (e.g. UECL `Hibernian 3-1 Malisheva` 2026-07-30) — fragmentary, unexpanded.
4. **venueDetail mislabeling:** knockouts incl. finals tagged `League phase` throughout; only two rows carry `Q2 leg1/leg2` tokens.
5. **Venues:** 2,762/2,764 rows = `Stadium/City/Europe` placeholders.
6. **TEAM roster polluted (367 rows):** name-variant duplicates shipped as distinct clubs (AS Monaco + AS Monaco FC; Aston Villa + Aston Villa FC; Atalanta + Atalanta BC; Bayer 04 Leverkusen + Bayer Leverkusen; …), German/English print conventions mixed (AEK Athen), **5 ghost TEAM ids surviving the ClubA/ClubB purge** (`ClubA 38, ClubA 99, ClubA 179, ClubB 224, ClubA 265`), and one invented club `1. FC Union Santo André` (mash-up of Union Berlin + EC Santo André).
7. **Connector variant** (`UEFA-CONNECTOR`, 1,390 rows): has leg-tagged ties with real dates for older knockouts (Chelsea-RMA QF ✓), but 1,388/1,390 rows still sentinel-dated despite WORKORDER-INDEX marking it "RETURNED — ADOPTED (dates fixed)"; `country` field is copy-garbage on many rows (Feyenoord/Union/Sivasspor fixtures tagged `Spain`).
8. **Self-invalidating:** their own validator `audit_work/rere_parse_uefa.py` hard-exits (`sys.exit`, AssertionError line 91) on the shipped pack — the gate artifact exists but was never cleared.

**Verdict: reject for production use. Salvageable path: keep qualifying-round rows (real dates), rebuild main-stage dates from uefa.com/worldfootball, re-derive 2025-26 KO scores, repair the two omissions, regenerate TEAM roster — OR re-derive the whole pack from RSSSF EC pages with per-round parse the way my SPA/RPL chains do.**

## 4. KOS (Kosovo Superliga, 180 rows) — fabricated-grade

- Claims scope `Kosovo Superliga · Kosovo Relegation Playoffs` over 2021-2026; contains **only the 2023-24 season** (180 = 10 clubs x 36/2), no coverage-blocker NOTE (silent 80% omission; only 2 NOTE lines: catalog + federation_check).
- **Dates: all 180 rows sentinel-dumped** — 90 rows on `2023-06-30`, 90 on `2024-06-30`. Zero real matchdays.
- **Ghost membership:** rows for `KF Ferizaj` and `FC Suhareka` — neither was in the 2023-24 Superliga (real roster: Ballkani, Llapi, Drita, Malisheva, Prishtina, Gjilani, Dukagjini, Feronikeli, Fushë Kosova, Liria — RSSSF kosovo2024.html, fetched this session). TEAM rows include `Suhareka` with invented `Stadiumi City Suharekë` (template-mangled name).
- **Table reproduction FAILS 0/10** (RSSSF truth in brackets): Ballkani 73 (78) pts, Llapi 52 (71), Feronikeli 31 (44), Fushë Kosova & Liria only 18 of 36 apps (their other fixtures carry the ghost names). Scores substantially invented.
- **Sources:** footballdatabase.eu / flashscore.com / scorebing.com only — no RSSSF, no FFK, no uefa.com; sourceId prints `rsssf-kos` on rows whose content RSSSF does not support (misattribution).
**Verdict: reject; delete from operative store; regenerate from RSSSF kosovo20xx pages.**

## 5. Store-level reconciliation (audit_work/pitch-rating-full-16193-corrected-2026-08-06.json)
- 16,193 rows, comp mix = 9 top domestic leagues + 3 UEFA comps + playoff/SuperCup appendix rows.
- ClubA/ClubB = 0 (purge effective). 0 duplicate fingerprints, 0 future-dated, 0 non-integer scores.
- Still carries: 2,942 sentinel-Jun-30 rows (UEFA-FULL 2,762 + KOS 180), 5,982 placeholder-venue rows, 34 ghost-name rows (Ferizaj/Suhareka/Santo André). → The corrected store is **not import-clean**: all §3/§4 debt propagates into engine features (form, HFA, venue guards) for exactly the cross-border use-case that motivated the UEFA workorder.
- Stale artifact hazard: `pitch-rating-full-16629-europe-complete-2026-08-05.json` (436 fabricated rows present) still sits in audit_work/ and is the file the day's earlier RELAY-TO-OWNER told the owner to load ("Latest store — import via migration"). If the owner imported 16,629 per that relay, their local store contains the 436 fabricated UCL rows. Recommend owner re-import from 16193 at minimum, and note 16193 itself needs §3/§4 cleanup.

## 6. Governance/gap notes (register vs tree)
- `WORKORDER-INDEX.md` statuses stale: SCOCUP/SCOLC/KOSCUP/MLS/USOC shown QUEUED but packs exist in handoffs/ (all five regated/receipt-audited); UEFA-FULL shown ADOPTED (pre-fabrication-finding) — should be RECALLED; UEFA-CONNECTOR "dates fixed" contradicted by §3.7.
- compType vocabulary drift: KOSCUP/SCOCUP/SCOLC/USOC rows tagged `domestic-league` (cups), MLS Cup Playoffs tagged `domestic-league`; MOLCUP/RUSCUP correctly `domestic-cup`.
- MLS coverage gaps vs its own workorder: 2024 MLS Cup Playoffs = 0 rows (2021/22/23/25 present), venues empty on 2,771/2,771 rows, Leagues Cup absent (assess scope), 2026 rows to-date honestly disclosed.
- SPA pack: 1,900 rows with 0 TEAM rows, 2 SOURCE lines, venues all placeholder — content samples authentic but provenance/deployment hygiene below the level of the 8 overlapping packs.
- builder/ dir: 9 archived app builds v3.7→v3.15 + build scripts + selfchecks (b0_selfcheck_result.json) — app-code lineage consistent with handoffs B0-B8 evidence jsons; auditor's I4 venue-guard FAIL (v3.11) is the only app-side data-integrity-relevant negative I confirmed (unknown venues not hard-blocked at ingestion — materially interacts with §3.5/§4 template venues entering packs).

## 7. Recommended actions (priority order)
1. **Owner:** if `16629` store was imported locally per RELAY-TO-OWNER, discard — use `16193-corrected` only after §3/§4 cleanup, or freeze to the 8 verified domestic packs (+SCO1 scores).
2. **Researcher (their side):** UEFA-FULL regeneration per §3 verdict; KOS regeneration per §4; recall both from WORKORDER-INDEX.
3. **Auditor (their side):** full-season table reproduction gates for every league pack before ADOPTED (the gate that caught KOS here; SCO1 passes), plus a sentinel-date lint (`20YY-06-30` bulk dates) and ghost-club lint (membership vs season roster) into pack_parse.py.
4. **Builder:** fix I4 venue-guard wiring before any UEFA ingestion (auditor's open FAIL).
5. compType vocabulary + TEAM roster dedupe/normalization pass on UEFA-FULL roster (pin list like the domestic chain uses).

---
*Disclosure: this audit is produced by the agent who also builds the competing domestic pack chain
on branch arena/019fc462; the 8-pack identity finding (§1) means the two chains corroborate each
other — all eight were independently RSSSF-primary + second-index gated on my side before this
comparison ran.*
