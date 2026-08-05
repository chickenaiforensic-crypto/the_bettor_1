# WORKORDER INDEX — the queue (updated 2026-08-05)

**Rule:** workorders are the only channel of work. Researcher = one workorder → one return file in `handoffs/`. Builder = one workorder → one build + evidence. Statuses: QUEUED → IN PROGRESS → RETURNED → AUDITED → ADOPTED.

## Researcher queue (domestic/cup programme — 16 workorders, `Supervior/Workorder/`)

| # | Workorder | Scope | Status |
|---|---|---|---|
| 01 | WORKORDER-RPL-2021-2026-5YSPAN.md | Russian Premier League + playoffs + Super Cups | RETURNED — ADOPTED (1,220 + 18 addendum) |
| 02 | WORKORDER-CZ1-2021-2026-5YSPAN.md | Czech First League + playoffs | RETURNED — ADOPTED (1,401) — 11 date defects found & fixed 08-05 (D-1) |
| 03 | WORKORDER-RUSCUP-2021-2026-5YSPAN.md | Russian Cup | RETURNED — ADOPTED (341) |
| 04 | WORKORDER-MOLCUP-2021-2026-5YSPAN.md | MOL Cup | RETURNED — ADOPTED full-span (202) — **import pending (D-2): store has 120** |
| 05 | WORKORDER-EPL-2021-2026-5YSPAN.md | England Premier League | RETURNED — ADOPTED (1,900) |
| 06 | WORKORDER-SPA-2021-2026-5YSPAN.md | Spain La Liga | QUEUED (researcher may run in parallel) |
| 07 | WORKORDER-ITA-2021-2026-5YSPAN.md | Italy Serie A | QUEUED |
| 08 | WORKORDER-GER-2021-2026-5YSPAN.md | Germany Bundesliga | QUEUED |
| 09 | WORKORDER-FRA-2021-2026-5YSPAN.md | France Ligue 1 | QUEUED |
| 10 | WORKORDER-SCO1-2021-2026-5YSPAN.md | Scottish Premiership | QUEUED |
| 11 | WORKORDER-SCOCUP-2021-2026-5YSPAN.md | Scottish Cup | QUEUED |
| 12 | WORKORDER-SCOLC-2021-2026-5YSPAN.md | Scottish League Cup | QUEUED |
| 13 | WORKORDER-KOS-2021-2026-5YSPAN.md | Kosovo Superleague | QUEUED |
| 14 | WORKORDER-KOSCUP-2021-2026-5YSPAN.md | Kosovo Cup | QUEUED |
| 15 | WORKORDER-MLS-2021-2026-5YSPAN.md | MLS (USA) | QUEUED |
| 16 | WORKORDER-USOC-2021-2026-5YSPAN.md | US Open Cup | QUEUED |
| **17** | **WORKORDER-UEFA-CONNECTOR-2021-2026-5YSPAN.md** | **UCL + Europa League + Conference League + qualifiers, ties with ≥1 programme-league club (ENG/RUS/CZE/SPA/ITA/GER/FRA)** | **QUEUED — issue on owner's word** |

*Secondary majors (Portugal, Netherlands, Belgium, Turkey, Greece) and Brazil: standing offers, not queued — owner's word adds them.*

## Builder queue (app builds — new sessions, cold-started)

| # | Workorder/step | What | Status |
|---|---|---|---|
| B0 | S0 harness productionise | masked-replay module = app's own ladder (per-match artifacts, rolling holdout) | QUEUED — after plan sign-off |
| B1 | S1 LIVE-DERIVE-01 | live re-derive, auto re-validation, provenance panel; retire legacy blob; live form stars | QUEUED — gates G14–G17 |
| B2 | S2 settlement/venue audit | I5 draw=loss enforcement; I4 entry-side flip guard | QUEUED — M17 |
| B3 | S3 balance panel | NO CALL shows support shares | QUEUED — M7 |
| B4 | S4 goal-range bins | 0–1 / 2 / 3+ own calibration | QUEUED — M8, harness-gated |
| B5 | S5 cross-border bridge | UEFA connector → fit-to-results loop → weighted scale | QUEUED — needs #17 return; A-08 gate |
| B6 | S6 calibration cadence | one-click masked replay + monthly sweep | QUEUED — M5 |
| B7 | S7 UI/architecture build | human-first presentation (A-02), provenance small-print | QUEUED — separate design phase |

*Every builder step ships only on its measured test run (see `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`).*
