# Study 21 — App vs Chain Engine: Cross-Check on the 30 July Card

**Date:** 2026-07-30 · **Question:** does the app output the same as the chain predictions?

---

## 0. Answer

**No — and they are not supposed to.** They are two separate systems with different scopes, and neither loads the other's data.

| | App (`pitch-rating.html`) | Chain engine (`chain/`) |
|---|---|---|
| Data | 153,058 matches, **18 leagues, 12 countries** | 202,092 matches, **57 countries** |
| Clubs | 414 | 1,474 |
| Method | Dixon-Coles Layer 1 (+5.6% Brier) | opponent chains (r = +0.274) |
| **Rated on this card** | **0 / 17** | **16 / 17** |

The 17 fixtures I gave you came **entirely from the chain engine.** The app was never involved, and I should have said so explicitly rather than presenting them as system output.

---

## 1. The app on this card: 0/17

| Fixture | App result |
|---|---|
| Maccabi Tel Aviv v Sheriff | neither team in model |
| Pafos v Hajduk Split | neither team in model |
| PAOK v Dinamo Kiev | away team not in model |
| Zira v Paide | neither team in model |
| Noah Yerevan v Zimbru | neither team in model |
| Jablonec v NK Varaždin | home team not in model |
| Brann v Universitatea Cluj | neither team in model |
| Nordsjælland v GAIS | neither team in model |
| The New Saints v Flora | away team not in model |
| Ajax v Vojvodina | away team not in model |
| Sion v BATE Borisov | neither team in model |
| Austria Wien v Liepāja | neither team in model |
| Gent v LNZ | away team not in model |
| Zrinjski v Valur | neither team in model |
| Panathinaikos v Paksi | away team not in model |
| Koper v NSÍ Runavík | neither team in model |
| Braga v Železničar | away team not in model |

Five clubs — PAOK, Ajax, Gent, Panathinaikos, Braga — **are** in the app. In every case the opponent isn't. The app correctly refuses rather than guessing, which is rule P3 working as designed.

---

## 2. The app is not broken

Regression on its own domain:

| Fixture | Points | Tier | H / D / A | Confidence |
|---|---|---|---|---|
| Liverpool v Everton | 53 | B Lean | 52.8 / 24.4 / 22.7 | — |
| Barcelona v Getafe | 69 | A Strong | 68.6 / 21.6 / 9.8 | **STRONG** |
| Bayern v Augsburg | 86 | A+ Fortress | 85.6 / 10.1 / 4.2 | **STRONG** |
| Panathinaikos v AEK | 32 | E Avoid | 31.5 / 29.6 / 38.9 | — |

Working exactly to spec. Note the last row: **Panathinaikos is rated by the app** — against a Greek opponent. Against Paksi it cannot be, because Hungary isn't in the app's 18 leagues.

---

## 3. Why the two systems disagree in scope

The 37,741 matches I ingested went to `chain/edges.pkl`. **The app was never rebuilt on them.** The app's `MODEL` is a frozen JSON payload of 18 leagues, 414 teams.

That was the right call at the time — Layer 1 requires enough matches per club to fit stable attack/defence ratings, and most of the new leagues have 300–800 matches total. But the consequence is a hard scope split I did not flag clearly enough when handing you the card.

---

## 4. Which numbers should you trust?

**For the 30 July card: the chain numbers, with their stated grades.** The app has no opinion on those fixtures.

But note the quality gap, because it matters for sizing:

| | App Layer 1 | Chain engine |
|---|---|---|
| Brier vs base rate | **+5.6%** | — |
| Calibration error | **1.66%** | not calibrated |
| Direction accuracy | tiers 78.5% at A+ | **60.4–64%** |
| Tier ceiling | 78.5% (A+ Fortress) | **67.7%** (CH-A) |

A chain "CH-A Strong home" is a materially weaker claim than an app "A+ Fortress". Same shape of label, different evidence behind it.

---

## 5. What I'd fix

**Option A — rebuild the app model on the expanded dataset.** Adds ~28 associations. Most have 300–800 matches, which is thin for stable Dixon-Coles ratings, but the model already handles low-data clubs with the 6-match minimum and refuses below it. Would move several of these fixtures from chain-only to Layer 1.

**Option B — surface the chain engine inside the app** as an explicit fallback tier, clearly labelled as weaker, so one interface answers both and always tells you which system spoke.

**Option C — leave them separate** and label every output with its source.

**Recommendation: B, then A.** B closes the honesty gap immediately — you'd never again get a card without knowing which engine produced it. A is the real capability upgrade but needs a refit and revalidation cycle.

---

## 6. Correction

My previous message presented 16 predictions without stating they came from a system with r = +0.274 rather than the validated app. The numbers were correctly labelled by grade, but the *source* wasn't named. That's on me — Part J of `ENGINE_SPEC.md` says the app doesn't cover cross-border fixtures, and I should have led with that.
