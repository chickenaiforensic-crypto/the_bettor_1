# DATA EXPORT — MANIFEST & KNOWN DEFECTS

**Generated:** 2026-07-30 · Location: `/home/user/export/`
**Read this before using any record.**

---

## CRITICAL FINDINGS — read first

### F1. The match you cited is NOT in the dataset

You gave: `2026-07-23 | Sheriff Tiraspol | 0 | 5 | Maccabi Tel Aviv`

**Records for Maccabi v Sheriff in the graph: 0.** The first leg is absent. My Phase 2 analysis reported "never met" — that was true of *my data*, not of reality. Every chain estimate for this tie was built without the single most relevant match in existence.

This invalidates the Maccabi–Sheriff analysis I gave you.

### F2. All European dates are season-stamped, not real dates

```
distinct european dates: 15
most common: 2024-06-30 (957), 2025-06-30 (619), 2022-06-30 (407)
```

Every European match carries `YYYY-06-30`. The true match date was discarded at ingest. Consequences:

- within-season ordering of European matches is lost
- a date cutoff of `<= {year}-06-29` excludes an entire season, not a point in time
- "strictly prior" is enforced at **season** granularity for European links, not match granularity

Domestic dates from football-data CSVs **are** exact. Domestic dates from openfootball txt files are **also season-stamped**. Field `date_precision` in the export marks which is which.

### F3. Fields in your spec that do not exist

`round` · `venue` · `neutral_or_relocated_flag` · `extra_time` · `penalties` · `aggregate_tie`

All emitted as empty columns. **Never collected.** Consequences:
- two-legged ties are stored as two independent matches with no link between them
- neutral-venue and relocated fixtures receive full home advantage
- extra-time and penalty outcomes are not distinguished from 90-minute results

### F4. `CUP`, `PLAYOFF`, `FRIENDLY` contexts are absent

Cup files were skipped at ingest (`if 'cup' in fn.lower(): continue`). Only league and European competition are present.

### F5. Maccabi Tel Aviv has zero domestic matches

Israel is not in the league dataset. All 50 Maccabi records are European ties. Sheriff has 48 domestic (Moldova) plus 36 European.

Your request for "at minimum five years" of domestic results for both clubs **cannot be met for Maccabi from this dataset.**

---

## FILE INDEX

| File | Rows | Contents |
|---|---|---|
| `01_matches.csv` | 202,092 | full match graph in your schema |
| `02_cross_border.csv` | 4,244 | European matches only |
| `03_two_clubs_all_matches.csv` | 134 | every Maccabi and Sheriff record |
| `04a_segmentation_rows.csv` | 1,203 | segmentation test raw output |
| `04b_chain_calibration.csv` | 1,304 | tier calibration raw output |
| `04c_weighted_scale_test.csv` | 1,203 | your +1/+2/+4/+6 scale vs goal difference |
| `04d_fixture_outputs.json` | 17 | the 30 July card |
| `04e_league_strength.csv` | 41 | per-country European GD/match |
| `05_identity_map.csv` | 1,444 | normalised key → canonical name |
| `05_aliases.csv` | 29 | manual alias overrides |
| `06_environment.txt` | — | stdlib only, no external deps |

Plus all `.py` source and all `.pkl` originals.

---

## SCHEMA MAPPING

`edges.pkl` is a list of 8-tuples:

```
(date, competition, home_country, home_team, away_country, away_team, home_goals, away_goals)
```

`competition` is `DOM:<code>` or `EUR:<code>`, mapped to `context_type`:

| Internal | Your schema |
|---|---|
| `DOM:*` | `DOMESTIC` |
| `EUR:CL`, `EUR:CLQ` | `EUR_CL` |
| `EUR:EL`, `EUR:ELQ` | `EUR_EL` |
| `EUR:CONF`, `EUR:CONFQ` | `EUR_CONF` |

Note qualifiers are folded into their parent competition. Distinguish via the raw `competition` column, which is preserved.

---

## ANSWERS TO YOUR VERIFICATION QUESTIONS

**Date cutoff logic** — `chain.find_chains(since=...)` filters `e[0] >= since`. Test harnesses add `<= cut`. Because of F2, for European links this operates on season stamps.

**Match used before or after prediction update** — the chain engine is not an updating model; it reads a static graph. The Dixon-Coles app model (separate system, `pitch-rating.html`) predicts before updating, verified by test. **The chain engine has no such guarantee beyond the date filter**, which F2 degrades.

**Duplicate handling** — `build_graph.py` dedupes domestic on `(league, season, date, home, away)`. European edges are **not deduped**. `ingest_extra.py` dedupes on `(date, home, away, hg, ag)` against the base set.

**Team renaming** — `chain.norm()` strips accents, punctuation, and 40 club-type tokens (`FC`, `AFC`, `ACF`, `FK`, `NK`, `SL`, `RSC`, …). Then `ALIASES` applies 29 manual overrides. This merged 76 previously-split identities. **The aggressive token stripping risks false merges** — e.g. any club whose real name is a stripped token. Audit `05_identity_map.csv` for collisions.

**Aggregate ties** — treated as **two independent matches**. No aggregate awareness. Two-legged qualifiers are double-counted as separate evidence.

**Extra time and penalties** — **not handled**. Scores are as printed in source. openfootball marks some as `(*)` or `a.e.t.`; the regex captures only the leading `N-N`, so an extra-time score may be recorded as a 90-minute result.

**Neutral venues** — **not flagged**. All matches receive full home treatment. Relocated fixtures (e.g. Ukrainian clubs playing abroad) are recorded with the nominal home team at home.

**Domestic vs European labelling** — via the `competition` prefix, reliable.

---

## WHAT I RECOMMEND YOU DO WITH THIS

1. **Reject the Maccabi–Sheriff analysis.** F1 makes it unusable.
2. **Treat every European date as season-only.** Do not assume within-season ordering.
3. **Re-fit the tier table** once real dates and the missing first leg are added — the current table is built on data with F2 and F3 present.
4. **Audit `05_identity_map.csv`** for false merges before trusting any chain.

The segmentation test output you asked for is in `04a`, and its summary statistics are reproduced in `/home/user/audit-24-segmentation.md`.
