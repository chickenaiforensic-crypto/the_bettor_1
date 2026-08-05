# PLAN — phase execution, gates, and evidence artifacts

> Rule: a phase ends only when its gate evidence exists in `gate-evidence/` (commands + raw outputs + numbers) and the auditor re-runs it green. Self-certified "done" is not done.

## Phase 0 — Baseline freeze
**Tasks**
- [ ] Define the golden behaviour matrix from WO Annex C (fixture set × output classes) as a machine-readable fixture the harness can diff against — *defined from spec, not captured from the absent legacy app (G6)*.
- [ ] Snapshot policy: every ship → `backups/<name>-<md5>.html` + fingerprint line in ZONES.
- [ ] Rollback rehearsal: restore from a backup at least once; record the run.
**Gate:** matrix file present + a clean-boot reproducible run + one successful restore.
**Evidence →** `gate-evidence/P0-matrix.md`, `gate-evidence/P0-rollback.md`

## Phase 1 — Single store & schema
**Tasks**
- [ ] One schema: `identities · matches · seasons · venues · sources · ctxFlags · mutes · log · artifacts` (WO §3-1, §4-②).
- [ ] Canon/alias/fingerprint module (one canon, one `esc`); identity collision merge (Dynamo-Moscow class).
- [ ] Migration machinery: old `pitch-rating-full` export → new schema, with summary report; **real-store run gated on G12**; fixture-shaped export used for exercise until then.
- [ ] Store content hash → derived cache key (WO §3-3).
- [ ] Retire legacy paste endpoint (F-2).
**Gate:** every team resolves to exactly one identity; migration report shown; matrix passes (documented drift only).
**Evidence →** `gate-evidence/P1-schema.md`, `P1-migration.md`

## Phase 2 — Live-compute core
**Tasks**
- [ ] Evidence engine as pure functions of the store (H2H / common / L3 shares, form, zones).
- [ ] One global Elo chain (all teams).
- [ ] Goals model; DC batch fit / online update **over store rows** — held at capability probe until ENGINE_SPEC.md or legacy parameters arrive (G10).
- [ ] Derived-layer cache keyed to store hash; league registry derived from data.
- [ ] Artifact regeneration pipeline (replay harness → versioned artifacts + validation report). *CAL9/EVG2/zone tables regenerated, never hand-written (G4).*
**Gate:** cache proven (mutate store → derived values change); identical inputs reproduce golden numbers (documented drift only); artifact report generated.
**Evidence →** `gate-evidence/P2-cache.md`, `P2-derive.md`, `P2-artifacts.md`

## Phase 3 — Data completion (continuous)
**Tasks**
- [ ] Publish coverage matrix (league → rows · seasons · gaps · status) — living document.
- [ ] Integrate arriving bulk per league through INGEST; cure ghosts with data, never delete declarations.
- [ ] Load Southampton / Ross-County / St-Johnstone packs on arrival or document why not (G11 — documented: absent).
- [ ] MLS round-2 remainder per `WORKORDER-MLS.md` when it arrives (G9).
**Gate (final):** every displayed league has full match rows for the Annex-A window; no ghosts; 20/20 reconciliations.
**Evidence →** `data/coverage/`, `gate-evidence/P3-*.md`

## Phase 4 — One confidence gate, one strength scale
**Tasks**
- [ ] One gate function accepting either computation kind; one label vocabulary; strength on one scale with provenance label (fitted vs Elo).
- [ ] Re-validate on held-out replay against both old gates before shipping (D8).
**Gate:** validation table shown for both input kinds; ship only on win/tie.
**Evidence →** `gate-evidence/P4-gate.md`

## Phase 5 — Venue bridge + single router
**Tasks**
- [ ] Venue check reads unified venue data for every fixture; cross fixtures get a real check when data supports it, generic warning only when genuinely absent.
- [ ] Router dispatches by capability probe, never list membership.
**Gate:** cross fixtures with venue data receive the same category of venue check as fitted-league fixtures.
**Evidence →** `gate-evidence/P5-venue.md`

## Phase 6 — Single render pipeline (plain, skin-ready)
**Tasks**
- [ ] One normalized result object; one card component; content driven by capability + labels (percentages iff calibrated fit; evidence shares iff graph; NO CALL otherwise).
- [ ] Parity audit table (same fixture through each path → identical structure/vocabulary).
- [ ] **Session amendment (owner ask: "excellent UI delivery"):** the skin is developed in-build (classy, polished) while the architecture stays skin-ready; the Phase 8 designer pack is still produced. Recorded in ZONES at P6.
**Gate:** identical structure/vocabulary across paths; parity audit clean; skin approved by owner.
**Evidence →** `gate-evidence/P6-parity.md`, `gate-evidence/P6-skin.md`

## Phase 7 — Compliance suite
**Tasks**
- [ ] Re-run every harness (extended, not shrunk); known-defects line-by-line pass/fail (blueprint absent — pass/fail against WO §9); provenance per output; refusal paths fired; frozen-settlement discipline confirmed.
**Gate:** the compliance report itself is the deliverable; auditor re-runs it.
**Evidence →** `gate-evidence/P7-compliance.md`

## Phase 8 — Designer handoff work order
**Tasks**
- [ ] Normalized result-object spec · component/state inventory · wording table · sample fixtures per capability class · skin layer isolation proof.
**Gate:** design WO delivered; engine untouched by any design commit.
**Evidence →** `design/`

## Cross-cutting (WO §7 conventions)
- Single HTML file `app/app-v3.html` (or `app-v3.<date>.html` line), no frameworks, no network calls.
- All strings through one `esc()`; backend vocabulary banned from user-visible text; audit greps.
- Data enters only as files (drive folder / file picker) → staging → validate → approve → commit; no paste intake.
- Performance budgets @20k rows: derive-on-change < 2 s · fixture render < 100 ms · 1,000-row import < 5 s.
- Determinism: same store hash → same derived hash → same numbers; no hidden `new Date()` in compute paths.
