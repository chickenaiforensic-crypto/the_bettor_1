# COVERAGE PLAN — which leagues/tournaments to add (2026-08-02)

Goal: **regular in-play games all year that the app actually stocks.** Europe runs
Aug–May; the calendar gaps are **June–July (almost nothing stocked)** and **Dec–Feb
(partial)**. Recommendation below is calendar-driven and data-quality-driven
(primary bulk must exist as machine-readable CSV; football-data.co.uk covers all Tier-1
picks, with official federation + fbref as cross-checks).

## What we already stock
Aug–May: Belgium B1, Germany D1/D2, England E0–E3, France F1/F2, Greece G1, Italy I1/I2,
Netherlands N1, Portugal P1, Scotland SC0 (+ SC1 scaffold), Spain SP1/SP2, Turkey T1.
Jul–May: Russia RPL/FNL, Czech CZ1/CZ2. Feb–Dec: USA MLS (+USL scaffold, round-2 pending).

## TIER 1 — add now (kills the Jun–Jul gap, strong data)
| # | League / tournament | Runs | Why |
|---|---|---|---|
| 1 | **Brazil Série A + Copa do Brasil** | Apr–Dec (cup Feb–Oct) | biggest S. American league, excellent bulk data (football-data `BRA.csv`, CBF, fbref); cup = the "copa" games you asked for → `WORKORDER-BRAZIL.md` ready |
| 2 | **Argentina Primera División** | Feb–Dec (Apertura/Clausura) | year-round, football-data `ARG.csv`; huge in-play volume |
| 3 | **Mexico Liga MX** (Apertura Jul–Dec · Clausura Jan–May) | Jul–May | fills May–July; football-data `MEX.csv`; playoffs Dec + May |
| 4 | **Japan J1 League** | Feb–Dec | long season, stable data (`JPN.csv`); morning-EU kickoff window |
| 5 | **Norway Eliteserien** | Mar–Nov | summer league, clean data (`NOR.csv`) |
| 6 | **Sweden Allsvenskan** | Mar–Nov | summer league, clean data (`SWE.csv`); we already hold one Swedish identity (Djurgården) as evidence carrier |

Tier 1 total: continuous domestic league action **every month of the year** on top of Europe.

## TIER 2 — after Tier 1 proves out (good data, thinner interest)
Finland Veikkausliiga (Apr–Oct) · South Korea K League 1 (Feb–Nov) · China Super League
(Mar–Nov) · Chile Primera (Feb–Dec) · Colombia Primera A (Jan–Dec) · Uruguay Primera (Feb–Dec).

## TIER 3 — cups/continental, add only with league backing
- **Copa Libertadores + Copa Sudamericana** (Feb–Nov): high-interest midweek in-play; cross-border → app treats them as cross fixtures (evidence engine). Add once Brazil+Argentina (+Chile/Colombia) league packs exist, so entrants carry real form.
- **Ghana Premier League** (Sep–Jun): local interest; honest caveat — no machine-readable bulk feed of football-data grade; primary source would be GFA + soccerway/flashscore cross-check with slower acceptance. Possible, but expect a longer audit.
- **Africa Cup of Nations / WC qualifiers**: same cross-fixture treatment; tournament-window only.

## What NOT to add
- Cup competitions without their domestic league (ghost-team lesson, SC1).
- More European 2nd/3rd divisions (calendar overlap adds nothing; data effort high).
- State/regional championships (Brazilian state leagues, reserve/youth leagues) — noisy, duplicative.

## Pack discipline for every addition (hard rules, from shipped lessons)
1. Full match-level bulk from day one — tables-only rounds get rejected (MLS gate).
2. League codes populated from day one (Czech heal lesson) — no `NA`.
3. 90-minute doctrine + advancement NOTEs (Russian/Scottish cup doctrine).
4. Slug mapping sheet with accent aliases (Krylia lesson: one canonical spelling, aliases for the rest).
5. Final tables with home/away W-D-L/GF-GA splits as reconciliation inputs; recompute-and-match 20/20 or the return is rejected.
6. New pack = evidence-carrier-only until coverage gate + first fixture audit pass; replay/calibration entry is a separate decision.

## Suggested order
1. Brazil (this work order ready to send)
2. Argentina + Mexico (same template, parallel gather)
3. Japan, Norway, Sweden (same template)
4. Libertadores/Sudamericana once 1–2 are stocked
