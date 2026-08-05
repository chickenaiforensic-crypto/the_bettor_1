# WORK ORDER — BRAZIL DATA GATHER (junior brief, paste-ready)

Prepared 2026-08-02 · owner: junior data gatherer · auditor/finaliser: system side.
Status: **ROUND 1 OPEN — not yet sent.**
**Hard gates carried from MLS/Czech/Scottish lessons (read first):**
1. **Coverage gate from day one** — full match-level rows for every round, not standings/tables. A tables-only return gets rejected (MLS round-1 lesson).
2. **League codes populated from day one** in every TEAM/MATCH row (Czech heal lesson): `BRA` = Série A, `CDB` = Copa do Brasil.
3. **90-minute doctrine** — every knockout row records the 90-minute score; level after 90 is a draw even if someone advanced on pens/AET. Advancement facts go in NOTE rows only.
4. Cup-only loads are forbidden: a cup without its league behind it produces ghost teams (SC1 lesson). The league bulk below is mandatory, not optional.

## 1. Scope

Brazil — two most recent full playing seasons plus the season in progress, calendar-year format:
- **2024 Série A season** (Apr–Dec 2024): all 380 matches.
- **2025 Série A season** (Apr–Dec 2025): all 380 matches.
- **2026 Série A season in progress:** every completed round up to the gather date.
- **Copa do Brasil 2024 + 2025:** every tie from Round 3 (when Série A clubs enter) through the final — both legs.
- **Copa do Brasil 2026:** every Round 3+ tie completed to date, **including the current round's games**, both legs, with leg labels.
- Optional (do not block delivery): Copa do Brasil Rounds 1–2 rows for Série A clubs that entered early (state-championship qualification path).
- EXCLUDE: state championships (Paulistão/Carioca/Mineiro etc.), Copa Libertadores/Sudamericana (separate later order), Supercopa, friendlies.

Estimated volume: ~1,000–1,150 match rows (380×2 full seasons + ~190 played 2026 + ~90–110 cup rows).

## 2. Sources (hierarchy — on conflict the higher wins, and you record the dispute)

1. **Primary bulk source:** football-data.co.uk CSV — `BRA.csv` season files (mmz4281/<season>/BRA.csv). Clean dates, FT scores, closing odds columns.
2. **Cross-check / authority:** official CBF website (cbf.com.br) competition results pages + fbref.com Brazil Série A/Copa do Brasil match logs — match-by-match for every cup tie and any CSV row that looks off.
3. **Cup leg structure:** soccerway/flashscore tie pages to confirm two-leg pairing and which game is leg 1 vs leg 2.
4. **Odds (integrity screen ONLY, never predictions):** Pinnacle closing and market-average closing 1X2 prices from football-data (PSo/AvgC columns). Where missing (early cup rounds), mark NA — do not invent.

## 3. Output format (matches the existing pack schema exactly)

One CSV per competition-year + one merged text pack. Row grammar exactly as the USA order:

```
MATCH|YYYY-MM-DD|COMP|home-slug|away-slug|home-goals|away-goals
```

- COMP codes: `BRA` (Série A league games) · `CDB` (Copa do Brasil).
- Dates ISO, in the match's local calendar date (Brasília time).
- Two-legged ties: each leg is its own MATCH row and carries a shared tie id so legs pair up; record each leg's own 90-minute score. Put "X advanced on aggregate/penalties" in a NOTE on the tie, never in the score.
- Slugs: lowercase, stable across both comps (e.g. `flamengo`, `palmeiras`, `sao-paulo`, `atletico-mg`, `botafogo`, `gremio`, `corinthians`, `fluminense`, `vasco`, `bahia`, `fortaleza`, `athletico-pr`, `cruzeiro`, `internacional`, `santos`, `bragantino`). Deliver a `NAME|slug|Official Team Name` mapping sheet (football-data names vs official CBF names differ — accent aliases required, e.g. Sao Paulo / São Paulo; Atletico-MG / Atlético Mineiro; Gremio / Grêmio).
- TEAM rows must carry league code `BRA` (and the club's city/country) — no `NA` league fields.
- Odds columns go in a parallel CSV: `date,home,away,PinnacleCloseHome/Draw/Away,AvgCloseHome/Draw/Away`.
- **Reconciliation inputs (demanded, not offered):** the final league table per season with W-D-L and GF-GA **split home vs away per team**, and points (note any deductions in a NOTE row with source).

## 4. Acceptance criteria (what I check at audit)

- Row count reconciles exactly vs official records per season/comp (380/380 per Série A season; cup rows vs CBF bracket).
- **Every team-season W-D-L/GF-GA home/away split recomputed from your match rows equals the official table you delivered — 20/20 teams per season.**
- Every Copa do Brasil tie cross-checked against CBF/fbref — legs paired correctly, zero unexplained conflicts.
- No duplicate fixtures (same date+teams), no self-games, dates strictly ISO, slugs stable across comps.
- Penalty/AET-decided ties carry the 90-min scores + advancement NOTE.
- Pinnacle AND average closing prices present for ≥90% of Série A rows.

## 5. Non-negotiable rules (blueprint)

- Results only. No injuries, no lineups, no referee gossip, no table predictions, no editorial.
- 90-minute scores only — the draw-on-the-row rule above is absolute.
- Never substitute a fixture: if a game can't be verified, mark it NOTE blocker and stop — do not guess a similar game.
- Plain URLs only in SOURCE rows (no markdown links).
- Today is the gather date — anything after today does not exist; no scheduled games, no future rows.
