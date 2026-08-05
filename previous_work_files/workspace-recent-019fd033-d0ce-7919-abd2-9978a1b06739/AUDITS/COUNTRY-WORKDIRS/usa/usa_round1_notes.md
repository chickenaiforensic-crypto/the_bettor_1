# USA / WORKORDER-MLS — round-1 acceptance audit (2026-08-02)

Returned payload: slug table (29 MLS + 9 lower-division), 85 match rows, 68 odds rows,
2024 final + 2025 top-5 standings. Verdict: **accepted with 5 score corrections,
6 identifier additions, and a hard coverage gate.** No SEASON rows built (grammar
requires home/away splits — not delivered). No mutes (no integrity basis yet).

## F-A · 90-minute doctrine breach — 5 AET scores corrected (supplier's own NOTEs prove it)
Their claim "all knockout games locked to 90-minute scorelines" was true only for
shootout games. These five carried AFTER-EXTRA-TIME results:

| date | fixture | returned | stored (90m) | outcome note kept |
|---|---|---|---|---|
| 2024-05-08 | Union Omaha v Sporting KC | 1-2 | **1-1** | SKC won 2-1 aet |
| 2024-05-21 | Sacramento v San Jose | 4-3 | **3-3** | Sacramento won 4-3 aet |
| 2024-07-10 | Sporting KC v FC Dallas | 2-1 | **1-1** | SKC won 2-1 aet |
| 2024-09-25 | LAFC v Sporting KC (USOC final) | 3-1 | **1-1** | LAFC won 3-1 aet |
| 2024-11-23 | LAFC v Seattle | 1-2 | **1-1** | Seattle won 2-1 aet |

All 12 penalty-shootout rows were already correct at 90 (draws). Doctrine applied:
ET/pens settle as draws on the match row; advancement facts ride as NOTE rows.

## F-B · identifier table incomplete — 6 slugs added
- `fc-cincinnati` — the 30th MLS club, missing from the master table despite 5 rows referencing it.
- 5 lower-division slugs referenced by its own USOC rows but absent from the table:
  `las-vegas-lights`, `charleston-battery`, `fc-tulsa`, `loudoun-united`, `indy-eleven`.

## F-C · coverage gate (the decisive one)
85 rows are a **decision-day + knockout + 3 July-2026 rounds** slice. Absent: 2024 MD1-33
(~365 league rows), the entire 2025 season (~510 league rows + playoffs), 2026 Feb-Jul,
Leagues Cup. Consequences per ship discipline:
- pack loads as **evidence carrier only** (identities, USOC cross-tier ties, playoff endpoints);
- **no masked replay, no zone calibration, no CALIBRATED_PACK_LEAGUES entry** — needs full
  seasons, reconciled table-for-table (RPL bar: 16/16 vs official tables);
- calendar-year seasons noted for future half-split design;
- supplier offered full 2024+2025 tables — **say yes and demand the match-level bulk, not just tables.**

## F-D · integrity screen parked
Priced rows: 59 (34 of 2024 incl. playoffs, 25 of 2026 July). 8 NA rows = screen-ineligible by
declaration. n far too small for a favorite-collapse z-test (RPL screen used 644). Parked
until full bulk; odds substrate saved at `usa/usa_odds_r1.csv` (never enters the app).

## F-E · standings retained as reconciliation targets
2024 East garble strings decode cleanly (verified arithmetically):

MIA 34/22-8-4/79:49/74 · CLB 19-9-6/72:40/66 · CIN 18-5-11/58:48/59 · ORL 15-7-12/59:50/52 ·
CLT 14-9-11/46:37/51 · NYC 14-8-12/54:49/50 · RBNY 11-14-9/55:50/47 · MTL 11-10-13/48:64/43 ·
ATL 10-10-14/46:49/40 · DC 10-10-14/52:70/40 · TOR 11-4-19/40:61/37 · PHI 9-10-15/62:55/37 ·
NSH 9-9-16/38:54/36 · NE 9-4-21/37:74/31 · CHI 7-9-18/40:62/30

2024 West: pts+GD only (LAFC 64/+20, LA 64/+19, RSL 59, SEA 57, HOU 54, MIN 52, COL 50,
VAN 47, POR 47, AUS 42, DAL 41, STL 37, SKC 31, SJ 21). 2025: top-5 per conference only
(PHI 66, CIN 65, MIA 65, CLT 59, NYC 56 · SD 63, VAN 63, LAFC 60, MIN 58, SEA 55).
SEASON rows deferred — need HOME/AWAY W-D-L + GF-GA splits (strict-grammar arithmetic gates).

## F-F · odds-join date shift
3 rows dated +1 day vs the match rows (vancouver–lafc listed 11-04 → played 11-03;
lafc–vancouver 11-09 → 11-08; inter-miami 11-10 → 11-09) — late US kickoffs keyed on UK dates.
Screener must join with ±1d tolerance. Also: USOC odds stop after the May 7-8 round
(May 21+ rows absent entirely, incl. MLS-v-MLS games).

## F-G · same-class sweep (owner directive 2026-08-02)
Directive: fixing one instance obliges a sweep for others.
1. **League-code NA class** (Czech/Russia): 15 TEAM rows across hibernian/malisheva/closure
   packs recoded (KOS ALB DEN IRL NIR SRB POL SVN CYP SWE ISL MLT). Zero NA codes remain in packs.
   User heal = one re-import of each recoded pack (merge-on-add, zero-drift pattern proven on czech).
2. **Filter duplicate-row class** (Scotland v2.9.3): recoded codes collided with seed NAME tags
   → v2.9.5 LEAGUE_ALIAS extension (ALB/DEN/KOS/IRL name→code). Filter: 48 raw tags → 43, one row per league.
3. **USA pack built code-populated from day one** (MLS/USL/USL1) — lesson applied pre-emptively.
4. **Krylya class** (name-spelling): TEAM_NAME_CANON mechanism (v2.9.4) stands as the general fix;
   no additional misspelled identities found in the duplicate audit (0 duplicate names, 0 GAPs).
5. Remaining known: 14 embedded-seed stub identities have no league tag (11 Scottish lower-league
   cup-opponent placeholders, Eastleigh, Cádiz, Málaga — zero matches). Left SKIP-hidden by design;
   tagging them would assert divisions without a verified source.

## Acceptance state
- `packs/usa-team-pack.txt`: 45 TEAM · 85 MATCH · 17 NOTE · 1 SOURCE — strict import **0 errors**.
- 6-pack census: **1421 matches · 792 identities · 3 mutes** — drift vs 5-pack canonical (+85/+45/0) exact.
- Duplicate/GAP audit: **0**. USA probes: LAFC resolves + alias LAFC→same id; corrected AET row reads 1-1 in store; USOC count 21.
- Engine md5 parity vs v2.9.4 backup: all 8 functions IDENTICAL. Smoke **133/133**.
