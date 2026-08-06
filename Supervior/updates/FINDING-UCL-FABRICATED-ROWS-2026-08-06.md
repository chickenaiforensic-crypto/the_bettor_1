# FINDING — UEFA Champions League fabricated rows (2026-08-06)

**Status:** Resolved by removal. Not a date-correction.

## What was found

The 16,629-row store contains **436 fabricated UEFA Champions League rows** — not
"343 malformed dates". These are synthetic placeholder rows with **invented team
names** that no source can resolve:

- `homeName` / `awayName`: `ClubA1..ClubA436` / `ClubB1..ClubB436` (invented teams)
- `homeGoals`/`awayGoals`: all `1-0`
- `stadium` / `city` / `country`: `Stadium` / `City` / `Europe` (placeholders)
- `sourceId`: empty (`""`)
- `tieId`: `rsssf-ec`
- `venueType`: `Qualifying round`
- dates: includes malformed `2023-07-100`-style values (275 rows) and valid-looking
  but team-invented dates (161 rows)

## Source

They were injected by `audit_work/build_uefa_full_pack.py` in a `while len(match_rows) < 3200` loop
that pads with `ClubA{i}`/`ClubB{i}` fake rows to reach an arbitrary 3,200-row target.

## Why not date-corrected

The relay framed this as "correct the dates against RSSSF/uefa.com/worldfootball".
That is impossible: the rows carry no real teams, ties, venues or sources to look up.
Per the project rule *"Never invent a team, score, or date"*, the only honest action
is **removal**, not editing dates on invented matches.

## Corrected store

- **`audit_work/pitch-rating-full-16193-corrected-2026-08-06.json`**
  - `from` 16,629 → `to` 16,193 (removed 436 fabricated rows)
  - remaining: 0 malformed dateISO, 0 placeholder teams, 0 duplicate fingerprints
- The handoffs pack `UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt` also contains the 436
  fabricated rows (3,200 lines). It should be regenerated/flagged by the auditor; the
  real UEFA content is 2,764 rows (UCL 920 + UEL 760 + UECL 1,084).

## Real UEFA rows retained in store

- UEFA Champions League: 920 (738 League phase + 182 Qualifying) — real teams/sources
- UEFA Europa League: 760
- UEFA Conference League: 1,084
- (non-UEFA rows unchanged)

## Not fabricated but adjacent

The separate `build_uefa_pack.py` (connector) uses `Stadium`/`City` defaults for some
rows but with **real team names** — those are NOT in the fabricated set and were retained.
