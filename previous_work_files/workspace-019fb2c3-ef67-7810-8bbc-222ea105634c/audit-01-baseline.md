# Audit 01 — Baseline of `match-audit-tool.html`

**File:** 138 KB, 2,505 lines, single self-contained HTML page (no build, no deps).
**Audited:** 2026-07-29 · **Scope:** orientation pass before the football update.
**Lens:** everything is judged twice — (a) does it work as built, (b) is it fit for *predicting football home games*.

---

## 1. What the app actually is

A **4-step manual research harness with a weighted scoring layer on top**, plus a persistent log.

```
Step 1  Setup        sport + Team A/B + tournament
                     ├─ picker: curated competition → Gemini "next 2 days" schedule → click to fill
                     └─ paste-a-game: free text → Gemini → JSON array → click to fill
Step 2  Questions    generates a long, sport-branched research prompt (9 sections + ground rules)
                     └─ "Run with Gemini" POSTs it to <backend>/api/research
Step 3  Feed back    paste the model's KEY: VALUE block → parseAndFill() → 5 subscales + 8 side fields
Step 4  Verdict      computeVerdict() → tier + probability + edge + "top plays" → auto-saved to log

Log tab              index + detail records, search/filter, single & bulk result checking
                     (<backend>/api/check-result), manual override, export/import JSON v2,
                     optional Chrome File System Access "Logs folder"
```

**Honest framing:** this is not a predictive model. It is a **structured elicitation form**. All signal comes from an LLM's qualitative 5-point ratings; the code converts those ratings into a number. That's a legitimate design — but it means every accuracy question is really a question about the prompt and the rater, not the arithmetic.

### The maths, in full

| Stage | Formula |
|---|---|
| Subscale weights | commonOpponent .30, currentForm .25, recentForm .20, conditionsFit .10, headToHead .10 — **sum 0.95** |
| Level values | Strongly favors A `+2` · Favors A `+1` · Even `0` · Favors B `-1` · Strongly favors B `-2` · `NO_DATA` excluded |
| Raw score | `Σ(w·v) / 0.95` (NO_DATA divides by **full** weight → missing data shrinks toward even. Good.) |
| Normalised | `norm = raw / 2` → range −1…+1 |
| Probability | `probA = 1 / (1 + e^(−4·norm))` |
| Football draw | `draw = 0.26 · (1 − |norm|)`; `A3 = probA·(1−draw)`, `B3 = (1−probA)·(1−draw)` |
| De-vig | 3-way normalisation if draw odds present, else 2-way |
| Edge | `model(leader) − market(leader)`, bases matched (3v3 or 2v2) |
| Confidence | from SHARED_COUNT only (`0/1`→low, `2-3`→medium, `4+`→high), then capped down by completeness (<0.4→low, <0.6→ not high) |

Resulting probability curve:

| norm | probA | draw est | A / draw / B (football) |
|---|---|---|---|
| 0.00 | .500 | .260 | **.370 / .260 / .370** |
| 0.15 | .646 | .221 | .503 / .221 / .276 |
| 0.30 | .769 | .182 | .629 / .182 / .189 |
| 0.50 | .881 | .130 | .766 / .130 / .104 |
| 1.00 | .982 | .000 | .982 / .000 / .018 |

Tier gates: `PASS` if ≥2 of {commonOpp NO_DATA, H2H NO_DATA, baseline conflicts, quality contradicted} — unless every signal agrees *and* edge ≥ 8%, then LEAN. Else `INSUFFICIENT_DATA` if confidence low; `TIDE_MATCH` if |norm| < 0.15; `CLEAR_WIN` if |norm| > 0.4 + high confidence + no red flags + edge ≥ 5%; `STRONG_LEAN` if all that but edge < 5%; else `LEAN`.

---

## 2. What is genuinely well built

Worth stating before the criticism, because these are the parts I'd keep:

- **Missing-data handling is honest.** Dividing by full weight instead of renormalising is the single best decision in the file — most homebrew models get this wrong and manufacture confidence out of thin evidence. The completeness cross-check on top of SHARED_COUNT can only push confidence *down*, never up.
- **Hard gate on unanswered fields.** Placeholder `""` options that refuse to compute, rather than defaulting to "neutral". Correct.
- **Strict YES/NO parsing** with off-format values pushed into `skipped` and surfaced, instead of silently reading as `NO`.
- **Write-detail-before-index** in `saveLogEntry`, with in-memory rollback. No orphaned index rows.
- **Storage adapter** (artifact storage → localStorage fallback) plus real export/import. The log survives.
- **Market independence rule** in the prompt (sections 1–8 locked before any odds page is opened) is a real anti-leak discipline; most tools let the model read a tipster blurb and launder it as analysis.
- **Separating "model is confident" from "there is betting value"** (STRONG_LEAN vs CLEAR_WIN) is a distinction most tools collapse.
- The code comments are unusually candid about which numbers are unfitted guesses. That made this audit much faster.

---

## 3. Findings

Severity: 🔴 blocks accurate football home-game prediction · 🟠 real defect · 🟡 worth fixing

### 🔴 F1 — There is no home/away concept anywhere in the model
`grep -i home` returns three hits, all cosmetic: a help string ("Surface / pitch / home-away / rest"), one prompt line, and a baseball tooltip. Consequences:

- A and B are symmetric. Nothing in `computeVerdict()` knows which team is at home.
- Home advantage lives only inside `conditionsFit`, **weight 0.10**, as one component of a subjective ±2 rating, competing with rest, altitude and stylistic fit.
- At a dead-even reading (norm = 0) the model outputs **A .370 / draw .260 / B .370**. The empirical top-5-league baseline is roughly **home .44 / draw .25 / away .31**. So on a genuinely balanced fixture the tool understates the home side by ~7 points and overstates the away side by ~6.
- Home advantage is not constant — it varies by league, by club, by crowd, by travel distance, and it has been drifting downward for a decade. None of that can be expressed.

For a tool whose stated purpose is *predicting home games*, this is the structural gap. Everything else is secondary.

### 🔴 F2 — Football league play is misclassified as a bracket tournament
```js
const isLeagueSport = sport === "basketball" || sport === "baseball";
```
Football is excluded. Two knock-on effects:

1. Premier League / La Liga / Serie A fixtures get the **"1. Current tournament run"** question ("how many matches has each side won so far in *the tournament*, and against whom") — bracket-shaped, and nonsense for matchweek 23. The comment above this line documents that exact failure mode for the WNBA and then doesn't apply the fix to football.
2. Football never receives the **SHARED_COUNT inflation caveat** ("in a league both sides have played most of the same opponents by default; a large raw count does NOT mean high-quality evidence").

### 🔴 F3 — Confidence is inflated for domestic league football
Confidence is seeded from SHARED_COUNT alone. In any domestic league at midseason, both sides have faced 15+ identical opponents, so SHARED_COUNT is **always `4+` → high**. Combined with F2 (no caveat), that makes `confidence === "high"` effectively free — and `CLEAR_WIN` requires exactly `confidence === "high"`. The completeness cap only fires when 40–60% of subscale weight is NO_DATA, which for league football basically never happens. **Net: the tool's highest-conviction tier is easiest to reach in precisely the competition where its core evidence is weakest.**

### 🔴 F4 — A draw cannot be predicted, and a draw is scored as a push
Two separate problems that compound:

- The tier system only produces a leader (A or B) or a non-pick. `modelDraw` is computed, displayed, and then never used to make a call. `TIDE_MATCH` is the natural home for "we think this is a draw" and instead it recommends over/unders and DNB.
- In result checking:
  ```js
  const status = data.winnerSide === "draw" ? "push" : data.winnerSide === pickedSide ? "correct" : "incorrect";
  ```
  A **draw marks the pick as push**, and `renderLogStats()` computes hit rate as `correct / (correct + incorrect)` — pushes excluded from the denominator. For a "Team to win" pick a draw is a **loss**. With ~25% of football matches drawn, this silently inflates the reported football hit rate by roughly a third. Any calibration work done on top of this log will be built on a corrupted numerator.

### 🟠 F5 — The draw estimate is a straight line to zero
`draw = 0.26 · (1 − |norm|)` reaches **0.0%** at |norm| = 1 and 5.2% at |norm| = 0.8. Real draw rates have a floor around 8–10% even in heavy mismatches, and the true shape is a hump, not a ramp — draw probability also falls at the *even* end less steeply than this implies. The 0.26 constant is flagged as unfitted in the comments (credit for that), but the functional form is the bigger error, not the constant.

### 🟠 F6 — Misleading reason string when confidence is capped
Tier order is `PASS → confidence==="low" → tideBand → …`. The low-confidence branch always emits:
> "Fewer than 2 shared opponents — not enough to trust the comparison."

But confidence can be `low` via the **completeness** path with SHARED_COUNT = `4+`. The user is then told the opposite of what happened. Same class of issue in the LEAN branch, which is handled correctly there — the fix pattern already exists in the file, it just wasn't applied here.

### 🟠 F7 — Date handling will mis-check results
- `todayISO()` builds from **local** components; `deriveMatchDate()` uses `new Date(ts).toISOString().slice(0,10)` — **UTC**. In Europe/Paris these disagree for anything logged between 00:00 and 02:00 local, sending `/api/check-result` at the wrong day.
- There is **no manual match-date field**. If you type team names instead of clicking a picker result, `pickedGameDate` is nulled (`oninput="pickedGameDate=null"`), the past-date warning can never fire, and the match date falls back to the save timestamp.
- No kickoff time is captured at all, so "has this finished yet" is guesswork.

### 🟠 F8 — "Top plays" are hard-coded suggestions with no model behind them
`buildPlays()` returns handicap and first-half markets tagged `tier: "LEAN"` regardless of anything computed. There is no goals model, no xG, no Poisson, no scoreline distribution — so:
- "Total goals over/under" is recommended with no line and no number.
- "Leader on the handicap/spread" is recommended with no margin estimate.
- "First-half winner" is recommended as "lower-variance", which for football is a poor default (first-half home win rates are far below full-time, and the draw share is much larger).

These read as model output but are static text. That's the most likely place for a user to over-trust the tool.

### 🟠 F9 — No calibration instrumentation
The log records tier, confidence, probability and outcome — everything needed for a Brier score, a reliability curve, and per-tier hit rates. `renderLogStats()` reports **one pooled hit rate across all five sports**. There is no:
- breakdown by tier / confidence / sport,
- Brier or log-loss,
- closing-line value (odds are stored at audit time, never re-checked at kickoff),
- stake or P&L,
- duplicate-fixture detection.

Every threshold in the file (0.15, 0.4, 0.05, 0.08, 0.26, the weight vector, the sigmoid's −4) is hand-set. Without the above you can never move a single one of them on evidence — which is exactly the problem you say you're trying to solve.

### 🟡 F10 — Market display mislabels 2-way football
When football odds are entered without a draw price, `renderVerdict` prints "Market (de-vigged): A x% / B y%" summing to 100. That's a *conditional* (draw-removed) market, presented as if it were the 3-way market shown next to it. The edge calc handles the base-matching correctly; the display does not.

### 🟡 F11 — Football section 5 asks the wrong questions
"Win rate on this **surface** / in these conditions over the last 12 months" is the tennis branch, applied to football. Football needs: home/away splits, fixture congestion, midweek European involvement, travel distance, pitch dimensions, weather. Baseball got a custom branch; football didn't.

### 🟡 F12 — Parser edge cases
- `SHARED_COUNT` fallback: `map.SHARED_COUNT.includes("2") ? "2-3"` — a value of `12` becomes `2-3`.
- `QUALITY_PROXY` is required by the compute gate even when section 3b never ran (`NOT_APPLICABLE` must be explicitly present).
- `parseFloat(v.replace(/[^0-9.]/g,""))` on odds — `"1.85 (bet365)"` survives, but `"2.05/1.90"` becomes `2.051.90` → NaN → skipped (visible, so acceptable).

### 🟡 F13 — Unescaped `innerHTML` on model-supplied strings
35 `innerHTML` sites. Team names arriving from Gemini JSON and from imported log files flow into `renderPastedGames`, `renderLogList` and `renderLogDetail` unescaped. Low practical risk for a personal local file; it's a one-line `escapeHtml()` helper to close.

### 🟡 F14 — Weight vector sums to 0.95
Self-consistent (everything divides by `FULL_WEIGHT`), so not a bug — but 5% of the weight space is allocated to nothing, which suggests a category was removed and the vector never rebalanced. Worth confirming it's intentional before anyone tunes weights.

---

## 4. Football home-game readiness scorecard

| Capability | Status |
|---|---|
| Home/away as a first-class variable | ❌ absent |
| League-aware question set for football | ❌ falls into bracket branch |
| Draw as a predictable outcome | ❌ estimated, never actionable |
| Draw scored correctly against a win pick | ❌ counted as push |
| Calibrated base rates | ❌ symmetric 37/26/37 at even |
| Confidence that means something in a league | ❌ pinned high by construction |
| Goals / scoreline model | ❌ none |
| 3-way de-vig | ✅ correct |
| Edge base-matching (2-way vs 3-way) | ✅ correct |
| Missing-data shrinkage | ✅ correct |
| Result logging + export | ✅ solid |
| Calibration measurement | ❌ hit rate only, pooled, contaminated |

---

## 5. Recommended order of work

Sequenced so each step is testable before the next:

1. **F4b — fix draw→push scoring first.** One line. Until it's fixed, every football number in the log is wrong, and you can't measure whether any later change helped.
2. **F1 — add home/away.** Minimum viable: a "venue" control on Step 1 (A home / B home / neutral) + an explicit home-advantage term applied to `norm` *outside* the subscale block, so it's tunable independently. This also makes the prompt able to ask home/away-split questions.
3. **F2/F3 — add football to the league branch** and split confidence into two axes: *breadth of evidence* (how many subscales are populated) vs *quality of shared-opponent evidence* (informative comparisons, not raw count).
4. **F5 + calibrated baseline** — replace the linear draw ramp and re-centre the even-case output on real league base rates.
5. **F9 — instrumentation.** Per-tier hit rate, Brier score, and store the closing price. This is what turns the tool from a form into a system you can actually improve.
6. **F4a — let TIDE_MATCH express a draw** once 4 and 5 are in.
7. F6, F7, F10–F14 as cleanup.

Items 1–5 are the difference between "structured notes" and "prediction system". Items 6+ are polish.

---

## 6. Open questions for you

1. **Which football?** Domestic league only (where F2/F3 bite hardest), or cup/knockout too? The right fix differs.
2. **What's the output you actually bet?** 1X2 home win, Asian handicap, or over/under? F8 says the tool currently gestures at all three and models none.
3. **Is there an existing log with football results in it?** If yes, I can re-score it correctly (draw = loss) and give you a real baseline hit rate + Brier before we change anything — that's the control group for every later change.
4. **Are you open to a data feed**, or must this stay LLM-elicitation only? A results/xG feed changes what's worth building (real Poisson goals model vs better-calibrated subjective scoring).
