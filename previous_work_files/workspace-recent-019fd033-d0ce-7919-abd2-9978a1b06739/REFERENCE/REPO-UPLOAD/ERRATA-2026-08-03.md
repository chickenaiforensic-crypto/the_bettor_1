# ERRATA — 2026-08-03 (auditor-issued; supersedes the cup-only erratum of the same day)

Eleven workorders carried wrong `<compType>` instructions **authored by the auditor**
(not by any researcher who followed them). Every correction below was verified against
the live export (`pitch-rating-full-data-2026-08-02.json`, 1,432 rows) — the held rows
are the ground truth. The workorder files themselves have been corrected in place; this
document is the change notice for anyone holding an earlier copy.

## Family A — national association cups must be `domestic-cup`
Wrong instruction: `domestic-league` ("matches our existing cup rows" — that claim was
false; held cup rows are `domestic-cup`: Russian Cup 152, MOL Cup 63, US Open Cup 21).

| Workorder | Now correct |
|---|---|
| RUSCUP | `domestic-cup` |
| MOLCUP | `domestic-cup` |
| USOC | `domestic-cup` |
| SCOCUP | `domestic-cup` |
| KOSCUP | `domestic-cup` |

## League cup — SCOLC must be `league-cup`
The app type list has a dedicated league-cup type; Scottish League Cup rows use it.
(Was wrongly `domestic-league`.)

## Family B — promotion/relegation & MLS playoff matches must be `other`
Held ground truth: Russian Relegation Playoffs 2 rows = `other` · Czech Relegation
Playoffs 8 rows = `other` · MLS Cup Playoffs 28 rows = `other`.

| Workorder | League/stage rows | Playoff rows |
|---|---|---|
| RPL | `Russian Premier League` → `domestic-league` | `Russian Relegation Playoffs` → `other` |
| CZ1 | `Czech First League` (regular + all 3 playoff-stage groups) → `domestic-league` | `Czech Relegation Playoffs` → `other` |
| MLS | `Major League Soccer` → `domestic-league` | `MLS Cup Playoffs` → `other` |
| KOS | `Kosovo Superliga` → `domestic-league` | `Kosovo Relegation Playoffs` → `other` |

## Family C — SCO1 misleading parenthetical
"playoffs too" removed: the Scottish order covers regular stage + both split groups
(all `domestic-league`); no separate playoff competition is in scope.

## Impact on delivered work
- **RUSCUP return (189 rows, branch commit 5134d94):** content fully audited and
  standing; the auditor normalizes compType `domestic-league`→`domestic-cup` on all
  189 rows at import-prep. No re-collection needed.
- All future returns: apply the corrected values and cite this file in a
  `NOTE|info|errata_comptype` line.

## New workorder pins (md5) after correction
```
d92beae8c7edc580c48971fe835462a1 CZ1
cb6e86e243419389f843d6e3a187b1db EPL (unchanged)
79539690a70433f257168f379e84d439 FRA (unchanged)
8b50d8170104ae214263d97c289e3e8a GER (unchanged)
a72da1626416d90bffc846ce7c690d7f ITA (unchanged)
30c6141f7fe2e49c5f28bb1e2b53c139 KOS
3e973b3e15127fe146a620963f2e5072 KOSCUP
5bd05db47516d4d806d545083d5797b9 MLS
be738358ffb8baef48960df242f4f250 MOLCUP
9903cf856877d173ba71d72cef64e9c6 RPL
98a540a90aa062ee42d8ec4df166768e RUSCUP
00609865745c0f1705878178c7316e9e SCO1
414072369b1641c75ebce4e316e8131e SCOCUP
f2cd72db1846e074418cdf8938acff8d SCOLC
30d6b8355943cd2b8f3ba02e09da307a SPA (unchanged)
e9973c8c2fb212d776a851cdb2f57010 USOC
```
