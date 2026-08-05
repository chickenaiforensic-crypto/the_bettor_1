# Study 20 — Coverage Test: 17 Fixtures, 30 July 2026

**Date:** 2026-07-30 · **Status:** honest coverage report, no predictions issued

---

## 0. Result

**The system cannot rate any of these 17 fixtures.**

| Capability | Result |
|---|---|
| Ratable by the main model | **0 / 17** |
| Both clubs present in the chain graph | 6 / 17 |
| Enough chain paths to attempt an estimate | **1 / 17** |
| Estimate that survives scrutiny | **0 / 17** |

I am not issuing predictions on these. Doing so would violate P3 (the system must be able to say "I don't know") and would mean fabricating numbers for fixtures the data cannot reach.

---

## 1. Why the main model fails all 17

Every fixture is a **European qualifier** between clubs from leagues outside our 18-league dataset:

Israel, Moldova, Cyprus, Croatia, Ukraine, Azerbaijan, Estonia, Armenia, Czechia, Norway, Romania, Sweden, Wales, Serbia, Switzerland, Belarus, Austria, Latvia, Bosnia, Iceland, Hungary, Slovenia, Faroe Islands.

Five clubs *are* in the model — PAOK, Ajax, Gent, Panathinaikos, Nordsjælland — but in **every case their opponent is not**. A rating requires both sides.

This is open item 4 in `METHODOLOGY.md`: the competition field was approved but not built. These fixtures are precisely why it matters.

---

## 2. Chain graph coverage

| Fixture | Home | Away |
|---|---|---|
| Pafos v Hajduk Split | ✅ | ✅ |
| Zira v Paide Linnameeskond | ✅ | ✅ |
| Jablonec v NK Varaždin | ✅ | ✅ |
| Austria Wien v Liepāja | ✅ | ✅ |
| Panathinaikos v Paksi | ✅ | ✅ |
| Koper v NSÍ Runavík | ✅ | ✅ |
| Maccabi Tel Aviv v Sheriff | ✅ | ✗ |
| PAOK v Dynamo Kyiv | ✅ | ✗ |
| Nordsjælland v GAIS | ✅ | ✗ |
| The New Saints v Flora Tallinn | ✅ | ✗ |
| Ajax v Vojvodina | ✅ | ✗ |
| Gent v LNZ | ✅ | ✗ |
| Brann v Universitatea Cluj | ✗ | ✅ |
| Sion v BATE Borisov | ✗ | ✅ |
| Noah Yerevan v Zimbru | ✗ | ✗ |
| Zrinjski v Valur | ✗ | ✗ |
| Braga v Železničar Pančevo | ✗ | ✗ |

Name resolution was audited individually — all matches are genuine (`Pafos → Pafos FC`, `NK Varazdin → NK Varaždin`, `Liepaja → FK Liepāja` are accent/suffix differences, not false matches).

---

## 3. The 6 connected fixtures produce almost nothing

| Fixture | Opponents (H/A) | 2nd phase | 3rd phase |
|---|---|---|---|
| Pafos v Hajduk Split | 3 / 4 | none | none |
| Zira v Paide | 5 / 5 | none | none |
| Jablonec v Varaždin | 3 / 1 | none | none |
| Austria Wien v Liepāja | 6 / 1 | none | none |
| **Panathinaikos v Paksi** | 35 / 7 | none | **4 paths** |
| Koper v NSÍ Runavík | 2 / 1 | none | none |

Being *in the graph* is not the same as being *connected to each other*. Five of six have too few European matches to form any path.

### The one fixture with paths

**Panathinaikos v Paksi** — 4 third-phase paths, all 2022–2025:

| via | Estimate |
|---|---|
| Fiorentina → Polissya Zhytomyr | **+2.50** |
| Botev Plovdiv → NK Maribor | **+2.50** |
| Djurgården → NK Maribor | −0.50 |
| Rennes → AEK Larnaca | **−3.50** |

```
mean +0.25   sd 2.49   range −3.50 to +2.50   spread 6.00
```

Two paths say Panathinaikos wins comfortably, one says Paksi wins comfortably. **A mean of +0.25 from a 6-goal spread is not a prediction — it is noise with an average.**

The Study 19 finding that high spread can still predict was measured on **pooled** data (n=693). It does not license reading a single 4-path estimate with a 6-goal range. n=4 is a hypothesis, not a finding.

---

## 4. What this reveals about the system's real scope

The engine covers **18 domestic leagues in 12 countries**. European qualifying rounds draw from **55 UEFA associations**. On a July qualifying night, the overlap is close to zero.

This is not a defect in the model — it is correctly declining what it cannot see. But it is a hard limit on usefulness for the fixtures you actually want to play.

**The honest position:** the system as built serves domestic league football in its 18 covered leagues. It does not serve European qualifiers, and no amount of chain work will change that while the underlying league data is missing.

---

## 5. What would actually fix this

Ranked by leverage:

**A. Ingest more domestic leagues.** The direct fix. Adding Israel, Croatia, Ukraine, Czechia, Norway, Romania, Sweden, Austria, Switzerland, Serbia, Hungary, Slovenia, Cyprus, Azerbaijan, Estonia, Latvia, Belarus, Armenia, Moldova, Bosnia, Iceland, Wales, Faroes would make most of these fixtures ratable by **Layer 1**, which carries +5.6% Brier — versus the chain system's +0.274 correlation.

football-data.co.uk publishes ~20 additional leagues in the same format we already parse. Poland and Denmark were added this way in one step.

**B. Build the competition field** (open item 4, approved). Even with full coverage, a European qualifier is not a domestic league match — two legs, reduced home advantage, rotation risk. The model must know what it is looking at.

**C. Unified European ratings** (open item 5, not approved). Fit domestic and European matches together so national rating scales are linked directly rather than chained hop by hop.

**Recommendation: A then B.** A is mechanical, uses the pipeline we already have, and moves these fixtures from *unratable* to *Layer 1 ratable*. The chain system is a fallback for when that fails — not a substitute for having the data.

---

## 6. What I will not do

Issue estimates on 17 fixtures where the model has no rating, five of six chain-connected pairs have zero paths, and the one exception has a 6-goal spread across 4 paths.

You asked for a strong test. The honest result of that test is: **coverage 0/17, and here is exactly why and what fixes it.**
