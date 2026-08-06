# RELAY TO BUILDER — 2026-08-06 (planner approved, verified)

**Status:** Planner has audited and verified B0/B1/B2. Good work. Here's where things stand and what's next.

---

## What was built (all verified by planner, all accepted)

| Build | Version | What | md5 |
|---|---|---|---|
| B0 | v3.7.0 | S0 harness — `PR.calibration` module, ladder runner | `e688eee2` |
| B1 | v3.8.0 | S1 live-derive, auto re-validation, provenance M3, live stars G17, teamStats M6, compliance M18 | `d1a7426` |
| B2 | v3.9.0 | Live engine constants (UI-configurable, bounded, versioned), busy icon, zero hard-coding | `d46a18ea` |

**Zero-hard-coding verified by planner:** fetch=0, XHR=0, one-gate=11, `liveTeamRecord` ✅, `liveStarsFor` ✅, `autoRevalidate` ✅, `getLiveConstants` ✅, `__DC_GATE__` demoted to provenance, `__FITTED_MODEL__` first-boot only.

## Store expanded to 16,629 rows

20 competitions, 9 domestic + 3 UEFA. Four incremental stores built. Harness average gain +8.70% across 6 leagues.

## What's next (do NOT start until auditor delivers the 16629 ladder baseline)

### After auditor delivers:
1. **Integrate league pivot into the app** — the `league_pivot_artifact.json` has per-league s[L] values. These need to go into the engine as a `dc-fitted-league-pivot` artifact, auto re-validated on connector data change M1. Currently stored in `audit_work/` only — not in the app.
2. **Refine pivot with full λ model + ≥100 test samples** — current pivot uses simplified att-def diff with only 35 test matches (cutoff 2024-07-01). Need to:
   - Use full Dixon-Coles λ model (λ_home = exp(μ + att_home - def_away + hfa + hextra + s[LA]-s[LB]))
   - Use per-league HFA from domestic fit, not fixed 0.25
   - Expand test window — 614 UEFA rows available after 2024-07-01, plus SPA/SCO1/KOS now in store increases in-scope ties. Target ≥100 test matches minimum.
   - Validate with Brier (not just MSE) — convert GD predictions to H/D/A probabilities via Poisson grid
   - Increase max_iter to 100, step 0.05 for convergence to tol 0.02
3. **M10 integrity screen** — spec drafted in `lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md`. **OWNER APPROVED 2026-08-06.** Build as Integrity & Snapshots tab enhancement.

### S7 UI direction — USE THE DESIGNER'S SYSTEM, NOT THE OLD PROTOTYPE

The old `prototype-human-friendly.html` was a basic wireframe that made the owner request a designer. **The approved direction is the designer's index build:**
- `designer/design-tokens.css` — deep navy/charcoal + emerald/gold palette, Tiempos Headline + Inter typography
- `designer/components.css` — buttons, badges, cards, balance bar, verdict typography
- `designer/prototypes/index.html` — high-fidelity mockup (Bloomberg Terminal meets The Athletic editorial)
- `designer/README-DESIGNER.md` — design system, interaction notes, icon dictionary with fixed meanings

When building S7, import and use the designer's tokens + components. Do NOT start from the old prototype.

### Do NOT touch:
- Engine constants beyond bounded steps/caps (the live-configurable system in B2 is the path)
- Anything that would add fetch/XHR/odds (P1 permanent)
- The store directly — all imports through the one gate

## Key files

- Latest app: `builder/app-v3.9.0-b2.html` (reference baseline going forward)
- Build scripts: `builder/build_b0.py`, `build_b1.py`, `build_b2_live_constants.py`
- League pivot: `audit_work/league_pivot_artifact.json`, `league_pivot_full_artifact.json`
- Evidence: `handoffs/B0-EVIDENCE-2026-08-05.json`, `B2-EVIDENCE-2026-08-05.json`
- Cold start: `Supervior/updates/COLD-START-BUILDER-2026-08-06.md`

*Planner verified all builds. Wait for auditor's 16629 ladder baseline before next step.*
