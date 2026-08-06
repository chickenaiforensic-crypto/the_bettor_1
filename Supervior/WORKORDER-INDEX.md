# WORKORDER INDEX — the queue (updated 2026-08-06)

**Rule:** workorders are the only channel of work. Researcher = one workorder → one return file in `handoffs/`. Builder = one workorder → one build + evidence. Statuses: QUEUED → IN PROGRESS → RETURNED → AUDITED → ADOPTED.

**Current store:** `audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json` — **16,629 rows, 20 competitions** (9 domestic + 3 UEFA). Previous stores: 5,000 (D-1 corrected) → 5,082 (D-1+D-2) → 10,209 → 11,599 → 13,429 → 16,629. All verified by planner 2026-08-06.

## Researcher queue (domestic/cup/European programme — 18 workorders)

| # | Workorder | Scope | Pack in handoffs/ | Status |
|---|---|---|---|---|
| 01 | WORKORDER-RPL-2021-2026-5YSPAN.md | Russian Premier League + playoffs + Super Cups | `RPL-2021-2026_BP-TEAM-PACK_v2.txt` (1,262 lines) + `RUS-ADDENDUM-2026_BP-TEAM-PACK_v2.txt` (40 lines) | ✅ RETURNED — ADOPTED |
| 02 | WORKORDER-CZ1-2021-2026-5YSPAN.md | Czech First League + playoffs | `CZ1-2021-2026_BP-TEAM-PACK_v2.txt` (1,450 lines) | ✅ RETURNED — ADOPTED — D-1 date fix applied |
| 03 | WORKORDER-RUSCUP-2021-2026-5YSPAN.md | Russian Cup | `RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt` (502 lines) | ✅ RETURNED — ADOPTED |
| 04 | WORKORDER-MOLCUP-2021-2026-5YSPAN.md | MOL Cup | `MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt` (322 lines) | ✅ RETURNED — ADOPTED (full-span 202) — D-2 applied |
| 05 | WORKORDER-EPL-2021-2026-5YSPAN.md | England Premier League | `EPL-2021-2026_BP-TEAM-PACK_v2.txt` (1,935 lines) | ✅ RETURNED — ADOPTED |
| 06 | WORKORDER-SPA-2021-2026-5YSPAN.md | Spain La Liga | `SPA-2021-2026_BP-TEAM-PACK_v2.txt` (1,905 lines) | ✅ RETURNED — ADOPTED |
| 07 | WORKORDER-ITA-2021-2026-5YSPAN.md | Italy Serie A | `ITA-2021-2026_BP-TEAM-PACK_v2.txt` (1,945 lines) | ✅ RETURNED — ADOPTED |
| 08 | WORKORDER-GER-2021-2026-5YSPAN.md | Germany Bundesliga | `GER-2021-2026_BP-TEAM-PACK_v2.txt` (1,590 lines) | ✅ RETURNED — ADOPTED |
| 09 | WORKORDER-FRA-2021-2026-5YSPAN.md | France Ligue 1 | `FRA-2021-2026_BP-TEAM-PACK_v2.txt` (1,728 lines) | ✅ RETURNED — ADOPTED |
| 10 | WORKORDER-SCO1-2021-2026-5YSPAN.md | Scottish Premiership | `SCO1-2021-2026_BP-TEAM-PACK_v2.txt` (1,146 lines) | ✅ RETURNED — ADOPTED |
| 11 | WORKORDER-SCOCUP-2021-2026-5YSPAN.md | Scottish Cup | — | QUEUED |
| 12 | WORKORDER-SCOLC-2021-2026-5YSPAN.md | Scottish League Cup | — | QUEUED |
| 13 | WORKORDER-KOS-2021-2026-5YSPAN.md | Kosovo Superleague | `KOS-2021-2026_BP-TEAM-PACK_v2.txt` (191 lines) | ✅ RETURNED — ADOPTED |
| 14 | WORKORDER-KOSCUP-2021-2026-5YSPAN.md | Kosovo Cup | — | QUEUED |
| 15 | WORKORDER-MLS-2021-2026-5YSPAN.md | MLS (USA) | — | QUEUED |
| 16 | WORKORDER-USOC-2021-2026-5YSPAN.md | US Open Cup | — | QUEUED |
| **17** | **WORKORDER-UEFA-CONNECTOR-2021-2026-5YSPAN.md** | **UCL + UEL + UECL + qualifiers, ties with ≥1 programme-league club** | `UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt` (1,502 lines) | ✅ RETURNED — ADOPTED (dates fixed) |
| **18** | **WORKORDER-UEFA-FULL-2021-2026-5YSPAN.md** | **Full UCL + UEL + UECL + qualifiers, entire competitions** | `UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt` (3,579 lines) | ✅ RETURNED — ADOPTED |

**Researcher summary:** 14/18 workorders returned and adopted. 4 remaining (SCO cups, KOS cup, MLS, USOC) — lower priority, not blocking.

*Secondary majors (Portugal, Netherlands, Belgium, Turkey, Greece) and Brazil: standing offers, not queued — owner's word adds them.*

## Builder queue (app builds)

| # | Step | What | App version | md5 | Status |
|---|---|---|---|---|---|
| B0 | S0 harness productionise | `PR.calibration` module, ladder runner in Calibration tab | v3.7.0 | `e688eee2` | ✅ ACCEPTED |
| B1 | S1 LIVE-DERIVE-01 | live re-derive, auto re-validation, provenance M3, live stars G17, teamStats M6, compliance M18, EPL revalidation G16 | v3.8.0 | `d1a7426` | ✅ BUILT |
| B2 | S2 live constants + busy icon | Engine constants live-configurable via UI, bounded steps/caps, animated busy icon, zero hard-coding | v3.9.0 | `d46a18ea` | ✅ BUILT |
| B3 | S3 balance panel | NO CALL shows support shares | — | — | QUEUED — after auditor 16629 ladder |
| B4 | S4 goal-range bins | 0–1 / 2 / 3+ own calibration | — | — | QUEUED — harness-gated |
| B5 | S5 cross-border bridge | League pivot integration into app — re-run with ≥100 test samples, full λ model | — | — | QUEUED — auditor re-running pivot |
| B6 | S6 calibration cadence + M10 | One-click masked replay + monthly sweep + outcomes-only integrity screen | — | — | QUEUED — M10 approved by owner 2026-08-06 |
| B7 | S7 UI/architecture build | **Designer's index build** (Bloomberg meets Athletic editorial) — `designer/` tokens + components + prototype | — | — | QUEUED — after S0–S6 gates; owner will help with UI |

*Every builder step ships only on its measured test run (see `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md`).*
