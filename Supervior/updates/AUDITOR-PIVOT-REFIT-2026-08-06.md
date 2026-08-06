# Auditor Pivot Re-fit — 16,629 Store (2026-08-06)

**Status:** Owner-requested re-run complete. **Do not promote pivot constants to production.** The ≥100-row validation, full-λ model, HFA and Brier requirements are met, but data mapping/coverage is too thin to establish all nine domestic league strengths.

## Reproducible evidence

- Fresh code: `audit_work/league_pivot_fit_16629.py`
- Artifact: `audit_work/league_pivot_16629_artifact.json`
- Store: `audit_work/pitch-rating-full-16629-europe-complete-2026-08-05.json`
- No market data is read or used.

## Required method pins

| Requirement | Result |
|---|---|
| Test population ≥100 | **PASS:** 614 valid UEFA rows dated on/after 2024-07-01 |
| Full λ model | **PASS:** Poisson home/away lambdas use fitted attack/defence, league-relative pivot, per-league domestic HFA and home extra effect |
| Per-league HFA | **PASS:** online domestic HFA fitted independently, bounded [.05, .55] |
| H/D/A Brier | **PASS:** 11×11 Poisson grid; frozen `.629892`, weighted `.628809`, improvement `+0.1719%` |
| Iterations / step | **PASS:** exactly 100 deterministic updates at `.05` |
| SPA/SCO/KOS re-filter | **PASS:** canonical-name mapping rerun across all nine domestic leagues; SPA 25, SCO 6, KOS 40 mapped UEFA appearances |

## Audit constraints

1. 343 UEFA Champions League rows have malformed non-calendar dates and were excluded before causal ordering.
2. Of 2,857 valid UEFA rows, only 189 have at least one canonically mapped domestic-programme side. The 614-row test is nevertheless the full valid UEFA test population; unmapped foreign clubs use the neutral rating prior and contribute to Brier, but cannot generate a league-pivot gradient.
3. France has zero mapped UEFA appearances. Czech and Scottish coverage is too sparse for a strength conclusion. The emitted zero values are an absence-of-evidence result, **not** fitted constants.
4. The observed Brier gain is small (+0.1719%). It validates execution of the requested evaluation, not a production claim.

**Acceptance:** methodological rerun accepted; production league-pivot update withheld pending repair of malformed UEFA dates and sufficient, identity-resolved cross-league coverage for every league to be weighted.
