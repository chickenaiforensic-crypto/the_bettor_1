# Auditor Report — Full 16,629 Ladder, M17 and M10

**Auditor:** Auditor Support  
**Date:** 2026-08-06  
**Scope:** Fresh-code production ladder, v3.9.0-b2 settlement/venue acceptance, and P1 review of M10.

## Decision summary

| Item | Decision | Evidence |
|---|---|---|
| Full domestic/UEFA ladder | **CONDITIONAL** | 8 domestic cohorts plus UEFA run; the six shared cohorts preserve `Δ0.0000`; Kosovo has no pre-cutoff history; 343 malformed UEFA dates were excluded rather than silently sorted. |
| M17 I5 settlement | **FAIL / blocker** | The application only saves a prediction snapshot. It cannot record a result or calculate a win/loss, so it cannot enforce the draw-as-loss rule. |
| M17 I4 entry-side venue guard | **FAIL / blocker** | The import validator has no home-hosted/verified-venue membership test, no confirmation control, and no hard save hold for it. |
| M10 P1 review | **PASS AS SPEC ONLY** | The approved specification is outcomes-only and contains no market input, feature, benchmark, sanity check, fallback, odds field, or network dependency. Builder implementation is authorised **only against the M10 scope**; it does not close M17. |

## 1. Fresh full-ladder run

**Inputs and code**

- Store: `audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json` (16,629 rows)
- Fresh runner: `audit_work/ladder_run_16629.py`
- Machine-readable output: `audit_work/ladder_baseline_2026-08-06_16629.json`
- Frozen constants: LR `.055`, decay `.0022`, HFA LR `.010`, rho `-.06`; same holdout ladder (1, 2, 3, 5, 8, 10, 15, 20, 25, 30, FULL).

The runner parses calendar dates with `datetime.date.fromisoformat`; it rejects malformed dates and records the count/examples. That is intentional: lexical ordering of a malformed date would make a causal audit invalid.

### FULL holdout results

| Cohort | Train / test rows | Scored | Model Brier | Base Brier | Log loss | Direction | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| Russian Premier League | 960 / 256 | 254 | .5675 | .6465 | .9572 | 55.9% | PASS |
| Czech First League | 1,105 / 276 | 276 | .6089 | .6509 | 1.0145 | 49.3% | PASS |
| England Premier League | 1,520 / 380 | 374 | .6140 | .6534 | 1.0225 | 49.2% | PASS |
| Italy Serie A | 1,520 / 380 | 374 | .5989 | .6579 | 1.0035 | 52.7% | PASS |
| Germany Bundesliga | 1,224 / 306 | 300 | .5721 | .6477 | .9721 | 54.7% | PASS |
| France Ligue 1 | 1,372 / 306 | 300 | .5971 | .6411 | .9984 | 53.3% | PASS |
| Spain La Liga | 1,520 / 380 | 374 | .5862 | .6299 | .9866 | 50.5% | PASS — new baseline |
| Scottish Premiership | 912 / 228 | 222 | .5828 | .6470 | .9774 | 52.3% | PASS — new baseline |
| Kosovo Superliga | 180 / 0 | — | — | — | — | — | **INSUFFICIENT_DATA** |
| UEFA combined | 2,243 / 614 | 337 | .6130 | .6237 | 1.0248 | 52.8% | CONDITIONAL |

**Parity gate:** RPL, CZ1, EPL, ITA, GER and FRA have identical result-bearing row fingerprints in the 11,599 and 16,629 stores. Independent replays produce metric delta `0.0000` for every one of these six cohorts. Exact data and ladder-comparison booleans are in the JSON artifact.

**Data gates not waived:**

1. Kosovo contains 180 dated rows but all precede the 2025-07-01 production cutoff; therefore it has no test tail and is not a valid production baseline. Do not invent a score by changing the cutoff after seeing the data.
2. UEFA has 343 malformed `dateISO` values (all Champions League), including non-calendar dates. The run uses the 2,857 valid UEFA rows (2,243 train / 614 test) and reports the excluded count. Repair/re-ingest and rerun before treating UEFA as an unconditional acceptance.

## 2. M17 settlement and venue audit — v3.9.0-b2

### I5: draw = loss — FAIL

The settlement console (`builder/app-v3.9.0-b2.html:4183-4189`) merely displays `type === 'settle'` log summaries. The only settlement event handler (`:4224-4229`) saves the fixture names, path label and confidence. It does not accept actual home/away goals, does not derive H/D/A, and does not write an outcome, win/loss, or draw classification. Thus neither a draw-as-loss test nor any settlement test is possible. “Saved rows are final for settlement” is a snapshot label, not settlement logic.

**Required builder acceptance test:** save three frozen rows; enter home win, away win and draw results; assert exactly the draw is recorded `loss` (never `push`), and surface outcome plus immutable prediction/result evidence in the Log & Settlement view.

### I4: entry-side flip / never-hosted guard — FAIL

The parser declares `venue` as a required match field, but `validate` only checks required fields, ISO-looking text, future date, competition type, scores, and duplicate fingerprints (`:823-973`; match checks `:899-915`). The staged venue records are simply appended during commit (`:1021-1024`). There is no check that the selected home team has ever hosted in the verified venue list, no official-list confirmation tick-box, no `neutral_venue` adjudication path, and no save-disabled hard error.

The fixture picker also permits selecting any two existing identities and swapping them (`:4214-4221`) without a venue confirmation surface. This is not the required entry-side guard.

**Required builder acceptance test:** attempt to save/import a row whose home team is absent from that competition’s verified-venue list; assert hard block. Then confirm through explicit official-list approval and assert (a) a durable rationale, (b) venue lock, and (c) neutral/relocated alternative preserved verbatim rather than a silent flip.

## 3. M10 P1 sign-off and builder forwarding

**Signed off: M10 specification only.** `lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md:23-42` uses model/ledger outcomes, ratings, match results and verified venue procedure. It explicitly makes flags human-review items, not automatic mutes. Its P1 exclusion is explicit at `:57-61`: no market data in any role, no odds grammar/engine input, no odds-site fetch/XHR, and no profitability claim.

The builder must preserve those constraints: model probability + settled result only for Brier; rating history + recorded results only for rating-jump flags; verified venue evidence and a human hold only for venue checks. No odds/prices/shadow fields may be introduced. M10 shipping remains separate from the two M17 blockers above.

See `Supervior/updates/RELAY-TO-BUILDER-2026-08-06-M10-AUDITOR-SIGNOFF.md` for the implementation relay.
