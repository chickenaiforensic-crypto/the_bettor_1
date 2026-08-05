# OLD-APP QUESTIONNAIRE REPLAY — ample-data games, answers audited (2026-08-01)

User order: games with ample data also run through the old app's questionnaire
(match-audit-tool.html), answers properly answered AND audited. Method: the REAL old-app
code driven headless in a sandbox (integrity probe: computeVerdict/subscales/sigmoid ✓),
answers computed from universe results only, strict cutoff = fixture date.
Log: `oldapp_log.csv`, runner: `study_oldapp.js`.

## Scope
609 RPL games → **437 ample-data** (≥4 informative shared opponents, last-5 window ≥3 each,
last-10 ≥8 each, home/away splits ≥3 each) + 73 more lacking only prior h2h (marked *).
CLEAR_WIN is unreachable: it requires market edge (odds), and this exercise is results-only.
Top reachable tier = STRONG_LEAN. Answer rules are mapping choices, fully disclosed in the
runner header; sensitivity on thresholds not re-tuned — first pass as declared.

## Old-app tier accuracy (leader win / D / L)
| Tier | n | W | D | L |
|---|---|---|---|---|
| STRONG_LEAN | 213 | 59% | 21% | 20% |
| STRONG_LEAN* (no h2h) | 35 | 63% | 23% | 14% |
| LEAN | 147 | 55% | 25% | 20% |
| TIDE_MATCH | 70 | 39% | 19% | 43% (correctly weak) |

## The comparison the user asked for ("see what it brings up")
- Old app at its best (59–63%) ≈ our **WIN** zone (65%) and clearly below our **STRONG**
  zone (78%). Ordering is sane (TIDE correctly weakest), so the questionnaire is a real
  instrument — just the weaker one on this universe.
- **Double-confirmation test** (zone STRONG/WIN × old STRONG_LEAN, same side): n=124 →
  69% w — and at the strongest cell (strong × STRONG_LEAN, n=47) 77% w / 9% L ≈ zone alone
  (78% / 8%). **No measured amplification: the old app adds no lift on top of the zones on
  ample-data games.** Keep it as the questionnaire discipline for thin-data/other-sport
  cases; zones stay the football verdict engine.
- Shared blind spot, confirmed once more: regime-shift upsets (worked game #1: Spartak v
  newly-promoted Dynamo Makhachkala — both systems strong on the favorite, promoted side won).
  That gap is availability/context data — the C4 layer (and the old app's own
  availability/anomaly flags — the design corroborates C4, it was already battle-shaped there).

## Answer-rule audit (the "audit that" half)
- **COMMON_OPPONENT direction: 353/354 nonzero classes agree with the engine's common
  section (100%)**; 353/479 (74%) including my EVEN-class calls (EVEN where the engine saw
  a small split — conservative round-down, never a wrong direction). 0 violations of the
  shared-count ≤ engine common-path count bound.
- Subscale answer distributions balanced (no class collapse): COMMON
  {+2:64,+1:116,0:151,−1:121,−2:58}; H2H {+2:105,+1:60,0:91,−1:39,−2:142,ND:73}.
- Three fully worked games printed in the runner output with every subscale's raw
  computation (per-opponent GD diffs, form PPG diffs, live-table positions, h2h PPG),
  each reproducible from `rpl_universe.csv` by hand.
- Disclosed insufficiencies (no guessing, per blueprint): availability = NO/NO (no lineup
  feed in a results-only universe — this is exactly the C4 feed); odds unset (results-only
  discipline — old app itself requires odds only for the value check, not the tier);
  resilience answered via narrow-games points-rate proxy (no in-match data); anomaly via
  "lost to a side ≥10 places below" proxy (real anomaly = line movement + effort markers,
  neither exists in results data).

## Verdict
Old questionnaire = validated but weaker instrument on dense data (59% best tier vs
78% STRONG zone), zero amplification when double-confirmed. Its honest role going forward:
the research-discipline template for sports without a results graph (its sport selector
covers tennis/basketball/baseball/volleyball) — NOT a second football engine.
