# DATA DICTIONARY — RPL 2021/22–2025/26 dataset

Applies to all files in `data/rpl/`. One row = one match. Header row present in
every file. Encoding UTF-8, line endings `\n`, no quoting (no field contains a
comma). Missing values are **empty cells** — empty means "source did not provide",
never "zero".

## Columns (19)

| # | Column | Type / domain | Meaning |
|---|--------|---------------|---------|
| 1 | `Country` | string, always `Russia` | Country tag used by the source. |
| 2 | `League` | string, always `Premier League` | Competition tag used by the source. |
| 3 | `Season` | `YYYY/YYYY` | Season label, e.g. `2021/2022`. Relegation-playoff fixtures carry the season they conclude. |
| 4 | `Date` | `DD/MM/YYYY` | Match date (day first). Chronological within each season file. |
| 5 | `Time` | `HH:MM` | Kick-off time as published by the source. **Timezone is not stated by the source** (football-data historically lists UK/central feed times) — treat as approximate local listing, not canonical MSK. |
| 6 | `Home` | string | Home team (source-canonical name, see quirks below). |
| 7 | `Away` | string | Away team. |
| 8 | `HG` | integer | Home goals, full time. |
| 9 | `AG` | integer | Away goals, full time. |
|10 | `Res` | `H` / `D` / `A` | Full-time result: home win / draw / away win (consistent with HG/AG on every row — validated). |
|11 | `PSCH` | decimal ≥ 1.0 | **Pinnacle Sports closing** 1X2 odds — home win. |
|12 | `PSCD` | decimal ≥ 1.0 | Pinnacle Sports closing odds — draw. |
|13 | `PSCA` | decimal ≥ 1.0 | Pinnacle Sports closing odds — away win. |
|14 | `MaxCH` | decimal ≥ 1.0 | **Market maximum** closing odds (across the source's bookmaker panel) — home. |
|15 | `MaxCD` | decimal ≥ 1.0 | Market maximum closing odds — draw. |
|16 | `MaxCA` | decimal ≥ 1.0 | Market maximum closing odds — away. |
|17 | `AvgCH` | decimal ≥ 1.0 | **Market average** closing odds — home. |
|18 | `AvgCD` | decimal ≥ 1.0 | Market average closing odds — draw. |
|19 | `AvgCA` | decimal ≥ 1.0 | Market average closing odds — away. |

All odds are **decimal** odds as published at market close. There is no
margin/overround removal — implied probabilities must be computed downstream.

## Coverage notes (source properties, not defects of delivery)

* **No** half-time scores / HT results, **no** corner/card/shot statistics, and
  **no** Over-Under, BTTS or Asian-handicap columns exist for RPL in this feed.
  Those columns exist for the big-5 leagues but the author never published them
  for Russia.
* Odds coverage degrades **within** 2025/26 as the source's RPL feeds dropped out
  (see AUDIT A4): rows 18/07–21/07/2025 carry all 12 odds with Max == Avg;
  25/07/2025–05/10/2025 carry PSC only (MaxC/AvgC empty); from 18/10/2025 all 12
  are populated again but Max == Avg on every row; from 31/10/2025 PSC is empty and
  only MaxC/AvgC (identical) remain.
* Eight rows dated 01–03/05/2026 contain the literal value `22` in `MaxCA`, which
  is implausible next to the matching `AvgCA` (~11.7–12.9). This is a source-side
  feed glitch; values are kept verbatim and listed one by one in AUDIT A5.

## Naming quirks (source-canonical, unmodified)

* `Pari NN` — FC **Pari Nizhny Novgorod**; known as **FC Nizhny Novgorod** until
  the 2022 rebrand. The source uses the current name **retroactively**: 2021/22
  rows already say `Pari NN` even though the club then played as Nizhny Novgorod.
  Do not "correct" when joining against contemporaneous sources — alias map:
  `Pari NN` ≡ `Nizhny Novgorod` ≡ `FC Nizhny Novgorod` ≡ `FK Nizhny Novgorod`.
* `FK Rostov` ≡ `Rostov` (other sources). `Dynamo Makhachkala` ≡ `Dinamo Makhachkala`.
  `Krylya Sovetov` ≡ `Krylya Sovetov Samara` ≡ `Krylia Sovetov`. `Ufa` ≡ `FC Ufa`.
* Non-RPL playoff guests appearing only in playoff rows: `SKA Khabarovsk`, `Yenisey`
  (Krasnoyarsk), `Rodina Moscow`, `Arsenal Tula`, `Akron Togliatti` (Akron later a
  full RPL member from 2024/25). They appear exactly twice each (two-legged ties).

## Row counts per file

| File | Rows | Composition |
|---|---|---|
| `RPL-2021-22.csv` | 244 | 240 regular + 4 relegation-playoff |
| `RPL-2022-23.csv` | 244 | 240 regular + 4 relegation-playoff |
| `RPL-2023-24.csv` | 244 | 240 regular + 4 relegation-playoff |
| `RPL-2024-25.csv` | 240 | 240 regular (**source omits the playoff ties** — AUDIT A3) |
| `RPL-2025-26.csv` | 240 | 240 regular (playoffs of ~late May 2026 not in source as of retrieval — AUDIT A3) |
| `rpl_all_2021-2026.csv` | 1,212 | all of the above, source order |
