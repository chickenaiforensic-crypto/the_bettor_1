# WORK ORDER — USA MLS DATA GATHER (junior brief, paste-ready)

Prepared 2026-08-01 · owner: junior data gatherer · auditor/finaliser: system side.
Status: **ROUND 1 RETURNED 2026-08-02 — accepted-with-corrections, evidence-carrier only.
See `usa/usa_round1_notes.md` (5 AET score corrections · 6 missing slugs added ·
coverage gate · integrity screen parked). ROUND 2 REQUIRED for any replay/calibration:
full match-level 2024 + 2025 bulk (not just tables — supplier offered tables; demand rows)
+ 2026 Feb–Jul + reconciliation inputs (home/away W-D-L, GF-GA splits per team-season).**

## 1. Scope

USA Major League Soccer — two most recent full playing seasons, calendar-year format:
- **2024 MLS season** (Feb–Dec 2024): regular season + MLS Cup Playoffs.
- **2025 MLS season** (Feb–Dec 2025): regular season + MLS Cup Playoffs.
- **US Open Cup 2024 + 2025:** every game involving at least one MLS club
  (lower-division opponents included — they are evidence carriers, mirror of the
  Russian Cup methodology).
- **2026 season in progress:** include all completed rounds up to the gather date
  (mirrors the RPL "new-season MD1+" rule).
- EXCLUDE: Leagues Cup (cross-border tournament), Canadian Championship,
  friendlies, All-Star game.

Estimated volume: ~1,000–1,100 rows total.

## 2. Sources (hierarchy — on conflict the higher wins, and you record the dispute)

1. **Primary bulk source:** football-data.co.uk CSV downloads — `USA.csv`
   (season files under mmz4281/<season>/USA.csv). Clean FT scores, dates, and
   closing odds columns.
2. **Cross-check / authority:** official mlssoccer.com results (schedule pages),
   match-by-match for every playoff row and any CSV row that looks off.
3. **US Open Cup:** ussoccer.com official Open Cup results; fallback cross-check
   soccerway/flashscore. Record any disagreement in a NOTE row.
4. **Odds (for the integrity screen, NOT for predictions):** Pinnacle closing and
   market-average closing 1X2 prices per game, as carried in football-data
   (PSo/AvgC). Where missing (Open Cup, early rounds), mark NA — do not invent.

## 3. Output format (matches the existing pack schema exactly)

One CSV per competition-year plus one merged text pack. Row grammar:

```
MATCH|YYYY-MM-DD|COMP|home-slug|away-slug|home-goals|away-goals
```

- COMP codes: `MLS` (regular season) · `MLSPO` (playoffs) · `USOC` (US Open Cup).
- **90-minute doctrine (hard rule):** knockout/playoff games decided in extra time
  or penalties are recorded at the 90-minute score — level after 90 = a draw,
  even if someone advanced. Put the shootout outcome only in a NOTE.
- Slugs: lowercase team identifiers, stable across all three comps
  (e.g. `lafc`, `inter-miami`, `seattle`). Deliver a `NAME|slug|Official Team Name`
  mapping sheet alongside (football-data names vs official names differ — alias table required).
- Odds columns go in a parallel CSV: `date,home,away,PinnacleCloseHome/Draw/Away,AvgCloseHome/Draw/Away`.

## 4. Acceptance criteria (what I check at audit)

- Row count reconciles vs official competition records per season/comp.
- Every playoff/USOC row cross-checked against source 2/3 — zero unexplained conflicts.
- No duplicate fixtures (same date+teams), no self-games, dates strictly ISO.
- Penalty-decided games carry the draw-at-90 score + NOTE.
- Alias table complete: every slug resolves to one official name.

## 5. What happens next (system side, after your delivery)

Source audit → universe + name build (usa/usa_universe.json) → pack generation
(packs/usa-team-pack.txt) → harness validation → masked-replay zone table vs the
calibrated domestic model → integrity screen on the odds columns → MLS goes live
(or back for fixes). Nothing enters predictions before the replay validates.
