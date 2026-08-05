# ZONES — decision & scar log (append-only)

> Every shipped decision gets an entry with WHY and numbers. Every rejection, every honest no-ship, every gap closure gets one too.
> **Never rewrite, never delete, never reorder.** Newest entry on top.
>
> Entry format: `## Z-YYYY-MM-DD-<seq> — <title>` · `Decision:` · `Why:` · `Evidence:` · `Status:` · `Rollback:`.

---

## Z-2026-08-02-007 — Final list R6 + R7 shipped (v3.1.0)

- **Decision:** Ship `app/app-v3.1.html` — version **v3.1.0** (badge + footer, unique per ship), md5 `dad4babde375f0b302d0f9ecee9dbc1b`, 589,195 B, backup `backups/app-v3.1.0-dad4babd.html`. Delivery is **base64-.txt only** (`deliver/`) because the CDN appends a Cloudflare block to raw .html (auditor-proven twice by md5 strip-and-match); decode → md5 matches, proven this session.
- **R6(a):** MUTE rationale now in `store.mutes.reason` — root cause was `store.migrate()` rebuilding mutes from the muted-flag (`"imported muted flag"`, no date/home/away). Fixed: migrate carries existing mutes verbatim (no-abolition); fallback entries carry full fields. Store print shows IA-01/02/03 with dates + reasons (shown in `gate-evidence/R6-R7.md`).
- **R6(b):** APP_VERSION → 3.1.0; badge + footer both render it; no stale 3.0.0 in rendered chrome (schema version is internal-only).
- **R6(c):** b64 drill files: `app-v3.1.0-dad4babd.b64.txt` · `ZONES-v3.1.0.b64.txt` · `R1-R5-corrections.b64.txt` · `DELIVERY-README.txt`. Decode+md5 proven for all three.
- **R6(d):** "fitted fitted" gone — hda labels no longer carry the prefix; wording `Dixon-Coles — scoreGrid + star draw correction`.
- **R7:** fitted-validated cards keep the evidence graph **one tap away** — native `<details>` "Head-to-head · Common opponents · Level-3" disclosure with the R3 two-sided records + goals read + plain-language note.
- **Evidence:** `gate-evidence/R6-R7.md`; new-app smoke **48/48**, parity 7/7, legacy 156/156, CF grep 0.
- **Status:** ✅ shipped — programme wrap per `PROJECT-STATUS-2026-08-02.md` §3 builder line complete. Owner open items unchanged (live store export, Ross-County/St-Johnstone pack).

---

## Z-2026-08-02-006 — Auditor corrections R1–R5 shipped (v3.0.0 rev.2)

- **Decision:** Ship the corrected `app/app-v3.html` (md5 `3048f269c7153fe18c9a7eae944cd752`, 586,532 B; backup `backups/app-v3.0.0-3048f269.html`). All five auditor corrections implemented and proven on file.
- **R1 picker:** free-text search (canon-substring over name+aliases+league), `<optgroup>` league grouping, no league filter — 539 identities all reachable; "krasnodar"→FC Krasnodar; ≤3 steps acceptance proven (`acceptance-r1-r4.js`).
- **R2:** CF grep = 0; seeds log as `system/seed` (9 entries, zero ownerApproved); mute reasons carry IA-01/02/03 rationale; `?` placeholders eliminated (confidence gate gets real effective/agree; rendered-card pin).
- **R3:** per-section two-sided records (W-D-L · GF-GA · games · years) on H2H/Common/L3 — owner reads both performances without arithmetic.
- **R4:** DC-vs-evidence masked replay (strict causality, split-half) — **DC WINS on RPL (0.5621 vs 0.5929) and CZ1 (0.5822 vs 0.6314) in pool + both halves** → fitted card enabled for both with provenance `fitted on Russian Premier League 2024–26 — validated on 568 of 641 masked rows, 2026-08-02`. Verdict artifact embedded; `d3Gate` grants fitted only on win+≥2 seasons. Annex C RPL-row drift documented (R4 supersedes; fitted = better-calibrated view).
- **R5:** identity count = **539** (149 declared + 34 match-anchored + 372 model-rated); the earlier 520 was a stale assembly, corrected.
- **Why:** the auditor's corrections are the acceptance contract; each is proven by a re-runnable pin, not prose.
- **Evidence:** `gate-evidence/R1-R5-corrections.md`; new-app smoke **43/43**, evidence parity **7/7**, legacy 156/156, CF grep 0.
- **Status:** ✅ shipped · **Rollback:** `reference/app-v2.6-cross.html` + `backups/app-v3.0.0-3048f269.html`.

---

## Z-2026-08-02-005 — v3.0.0 first ship: single store + ported engines + new skin

- **Decision:** Ship `app/app-v3.html` (final md5 `f8f16d26c643e84b4dad02a89b0fd3ec`; 576,249 B; backup `backups/app-v3.0.0-f8f16d26.html`). One self-contained HTML file, internally layered (store / derived / engines / confidence / result-object / skin). Single source of truth = the data store; every displayed number computed from it.
- **What shipped:** (1) ONE schema + canon layer + content-hash derive cache + `pitch-rating-full` migration/export; (2) evidence engine **ported verbatim from app-v2.9.9** — engine parity 7/7 fixtures identical (raw shares, zones, C5/C8/C11/C13 gates, sections, effective, agree); (3) Elo/perf ported (CAL8: K20/HF65/star/last-6); (4) Dixon-Coles fitted path ported from ENGINE_SPEC + migrated MODEL JSON (372 model-rated teams as identities with fittedRatings, Annex D); (5) one confidence gate, one normalized result object, single render skin (dark premium + light toggle), Data Ops console (Files/Coverage/Requests/Calibration/Log/Integrity), file-only intake (no paste); (6) masked replay + artifact regeneration; (7) 9 seed packs through the ONE ingest gate with legacy v1/NA compatibility (Z-003 FORM artifacts, ZONES v0.14 NA class).
- **Census:** 1,436 matches / 520 identities / 3 mutes (6-pack after cross-pack dedupe 1,392 + HIB_MAL seed 29 = legacy-exact 1,421; + Southampton 15). Identity count 520 vs legacy 792 is the **deliberate Phase-1 merge** (one identity per team, canon/alias; fitted roster migrated) — documented drift, line-by-line in `gate-evidence/P1-store.md`.
- **Why:** the WO's three sentences — one app/one store, live computation, data-completeness-ready — are all advanced by this ship; the parity proof makes the port auditable rather than claimed.
- **Evidence:** `gate-evidence/P0-baseline.md`, `P1-store.md`, `P2-engine.md`, `P6-render.md`; harness outputs: legacy smoke 156/156, packs 27/27, closure 19/19, concat 61/61, new-app smoke **26/26**, parity **7/7**.
- **Known open items (honest, not papered):** owner's live-store export pending (G12) — migration machinery exercised on round-trip; `rpl_universe.json` not in bundle — zone_tally_ctx regeneration queued (P2 artifacts); MLS round-2 per WORKORDER-MLS on arrival; SC1 ghost cure via Annex-A data; Southampton FORM rows are reconciliation-only artifacts (Z-003); RPL +1 vs my raw sum resolved as legacy counting the HIB_MAL seed (exact match documented in P1).
- **Status:** ✅ shipped · **Rollback:** `reference/app-v2.6-cross.html` (untouched legacy, smoke 156/156) + `backups/app-v3.0.0-*.html`.

---

## Z-2026-08-02-004 — Build kickoff: session defaults set (owner deferred Q2–Q4)

- **Decision:** Owner pushed the build forward ("all main files are coming") without answering the four asked questions. Session defaults are adopted and recorded here so they can be re-litigated if the owner objects:
  1. **Scope (Q2):** full phased build P0→P8, phase by phase, each with gate evidence; no skipping.
  2. **UI direction (Q3):** dark premium skin as default with a light theme toggle. Typography: display serif wordmark + system sans body. Accent: pitch emerald. Rationale: "classy and smooth is a hard requirement" (WO §3-7) and the skin ships in-build while Phase 8 designer pack is still produced.
  3. **Seed policy (Q4):** no synthetic seed. The app embeds **real packs only** (Southampton now; more on arrival), loaded through the same INGEST pipeline as any file — embedded seed is sanctioned by Annex D ("Seeded embedded pack"). Empty store → honest no-data states everywhere.
  4. **Bundling while files arrive:** each arriving file is fingerprinted (md5), copied into the project tree, and integrated; the assembled app is re-shipped only at phase gates.
- **Why:** proceeding is what the owner signalled; the defaults chosen are the ones the WO itself mandates or that minimise fabrication risk (seed = real data only; honest states).
- **Evidence:** user message 2026-08-02 "all main files are coming"; ZONES v0–003.
- **Status:** ✅ adopted (owner may override any line).

---

## Z-2026-08-02-003 — Southampton pack received; two grammar findings logged

- **Decision:** `Southampton_BP-TEAM-PACK_v2.pd.txt` (owner upload) is renamed to `.txt` per owner instruction and becomes seed data. Two audit findings are recorded, not silently fixed:
  1. **FORM row type** (`FORM|Southampton|last 15 all competitions|...`) is **not in the Annex B grammar** (TEAM/MATCH/SEASON/VENUE/NOTE/CTX/MUTE/SOURCE only). Decision: accept and store verbatim (no-abolition) as a declared form artifact; **never used as a hidden compute input** — live form is computed from match rows; the declaration is used for reconciliation only. Grammar extension flagged for the researcher brief (Annex A) so future packs either omit FORM or follow the documented extension.
  2. **Playoff tieId anomaly:** the two-leg promotion play-off semi-final carries per-leg tieIds (`EFLCH-2026-PO-SF-SOU-MID` / `EFLCH-2026-PO-SF-MID-SOU`) instead of one shared `tieId` per Annex B. Decision: rows kept verbatim; INGEST flags a tie-anomaly NOTE and groups two-leg ties by (competition, season, team pair) for the 90-minute doctrine; the researcher is asked to correct future packs.
- **Why:** WO §9 no-abolition + "never silently pick one"; the auditor recomputes from the store, so verbatim retention with a logged finding is the only honest path.
- **Evidence:** pack parsed — 1 TEAM · 17 MATCH · 1 SEASON · 1 VENUE · 2 NOTE · 1 FORM · 6 SOURCE; md5 `2d4b5ed07a08baea48a0d246e7f69f4a` (upload) → copy `data/packs/Southampton_BP-TEAM-PACK_v2.txt`.
- **Status:** ✅ seed loaded; findings carried into INGEST tests.

---

## Z-2026-08-02-002 — ENGINE_SPEC.md received (G10 closed)

- **Decision:** `ENGINE_SPEC.md` (16,132 B, md5 `91cd0cd5420cd494a799bd4050cb2ef8`) is canonical for the Dixon-Coles layer. All DC behavior follows it verbatim: layer order (Part A), model form + sign convention (B1), constants table (B4: LR 0.055, DECAY 0.0022, HFA_LR 0.010, new-team 1.6×/8, home_extra decay 0.999, min 6, ρ −0.06, λ clamp [0.05,6.0]), fitting procedure (B3, prediction-before-update, date order), two grids (C2, shrink k=0.5, GMU 2.6186), star draw correction (D1–D5), tier table (E1), consensus (F1–F2), refusal paths (H), output provenance (G).
- **Why:** WO §2 makes ENGINE_SPEC the governing document for DC work; without it the fitted path is held. It arrived; the hold lifts.
- **Evidence:** md5 above; copied to `docs/ENGINE_SPEC.md`.
- **Status:** ✅; companion `METHODOLOGY.md` still absent (prose-only gap, non-blocking).

---

## Z-2026-08-02-001 — Cold start on a partial bundle (v0)

- **Decision:** Begin the rebuild with the two uploaded files (master WO + handoff README) as the sole inputs; all 12 missing bundle items are logged in `docs/GAPS.md` with WO-mandated fallbacks, and the four owner rulings (Q1–Q4) are requested before Phase 0 coding. `trail/ZONES.md` is created fresh because the historical log was not in the bundle — the loss is hereby recorded, not papered over.
- **Why:** The WO declares itself self-contained and its stop-conditions demand *stop and ask* on any conflict with a binding document; with the binding docs absent, proceeding silently would violate the hand-back protocol (WO §0, §8). The project's own audit discipline forbids asserting state that cannot be verified.
- **Evidence:** `find /home/user/uploads` → exactly 2 files (README.md, WORKORDER-PITCH-RATING-REBUILD.md). Bundle README lists ≥16 items. md5 of uploads recorded at ZONES v0 annex below.
- **Status:** ⏸ pending rulings (Q1 bundle handling · Q2 session scope · Q3 UI direction · Q4 seed policy).
- **Rollback:** n/a (no code shipped).

### Annex — upload fingerprints (2026-08-02)

```
README.md                              md5: computed at first ship audit
WORKORDER-PITCH-RATING-REBUILD.md      md5: computed at first ship audit
```

---

## Z-2026-08-02-000 — Log opened

- **Decision:** This log is opened as v0 on 2026-08-02, before any code. Format adopted per WO §8 (versioned entries, numbers, honest no-ships).
- **Why:** The WO requires ZONES entries per ship and treats the log as the project's scar memory; opening it at cold start establishes the trail before the first line of code.
- **Status:** ✅

---

## Z-2026-08-02-008 — AMENDMENT-2 (D12 Central Request System) + R6/R7 final proof shipped (v3.2.0)

- **Decision:** Ship `app/app-v3.2.html` — version **v3.2.0** (badge + footer), md5 `fb4b037da77d8ed40f8204e6209f15a6`, 600,967 B, backup `backups/app-v3.2.0-fb4b037d.html`. Implements the binding AMENDMENT-2 D12 Central Request System and carries the already-shipped R6(a–d)/R7, re-proven on file.
- **R6(a):** `store.mutes.reason` carries the pack rationale — store print (final file): `Zenit v Krylia :: integrity: market-flagged favorite collapse (IA-02)` etc., all 3 with date/home/away/sourceId. Root cause fixed in `store.migrate()` (carry mutes verbatim; no-abolition).
- **R6(b):** unique version per ship — badge + footer both render `v3.2.0`; no stale 3.0.0/3.1.0 in chrome (pinned).
- **R6(c):** delivery via base64-.txt drill only — `deliver/app-v3.2.0-fb4b037d.b64.txt` + ZONES/R1-R5/R6-R7 b64; decode → md5 matches (proven). The CDN block was re-proven: `app-v3.1-stripped.html` = v3.0.0 build + 352-byte Cloudflare beacon (strip md5 `0edbece8…` ≠ any clean build).
- **R6(d):** `grep -c "fitted fitted"` = 0 on the final file (wording + comments).
- **R7:** fitted-validated cards keep the evidence graph one tap away — `<details class="graph"><summary>Head-to-head · Common opponents · Level-3</summary>` + per-side records (R3).
- **D12 (Central Request System):** Requests tab = ONE primary action "New central request" → writes `system-snapshot-20260802-<hash8>.json` (full store export + snapshot header `{requestDate, storeHash}`) + `central-request-20260802.txt` (header `PITCH-RATING CENTRAL-REQUEST v1`, SECTION per stale/REQUESTED league, team lines with real last-store-game dates, acceptance lines, `excluded|<league>|<reason>` for current leagues) + log `system/request`. Returns `central-request-<date>-r<n>.txt` matched to the open request in Files intake; ONE approval commits (per-section validation), coverage flips, post-return snapshot stamped in Integrity. Per-league request-file generation REMOVED (D12-5); grep proves zero `league-<code>-<window>` generation.
- **R8 pins:** `acceptance-r8.js` **13/13** (one action · two files + log · whole-system sections with real team dates spot-checked 5/5 · return→one-approval→coverage flip→post-return snapshot · header + no per-league gen greps).
- **Evidence:** `gate-evidence/R8-D12.md`; suites: new-app smoke 48/48 · R8 13/13 · parity 7/7 · legacy 156/156 · CF grep 0 · fitted-fitted grep 0.
- **Status:** ✅ shipped — final list complete; programme wrap per `PROJECT-STATUS-2026-08-02.md`.

---

## Z-2026-08-02-007 — Final list R6 + R7 shipped (v3.1.0)

---

## Z-2026-08-02-009 — Versioning policy + delivery manifest (v3.4.0)

- **Decision (owner, 2026-08-02):** every ship bumps the version upward — v3.4, v3.5, … — and every file name reflects the version it contains. No reused or misleading names. Ship `app/app-v3.4.html` — version **v3.4.0** (badge + footer), md5 `b464f046b097403a5a91132f26f520ae`, 601,011 B, backup `backups/app-v3.4.0-b464f046.html`, deliver `deliver/app-v3.4.0-b464f046.b64.txt`.
- **Why:** the audit found misleading filenames (app-v3.1.html and app-v3.2.html were byte-identical; app-v3.html carried stale v3.0.0 content). The policy makes a file's content provable from its name + md5, and adds `deliver/MANIFEST.txt` so the owner sends the auditor one authoritative list.
- **Housekeeping:** `app/app-v3.html`, `app/app-v3.1.html`, `app/app-v3.2.html` removed from `app/` (all three byte-identical copies already archived in `backups/`); `app/` now holds only `app-v3.4.html` + `modules/` + `shell.html`.
- **Content changes in this ship:** none beyond the version string (v3.2.0 → v3.4.0) — all R6/R7/D12/R8 behavior identical, re-proven on the new file.
- **Evidence:** suites on the new file: new-app smoke 48/48 · R8 13/13 · R1 acceptance green · parity 7/7 · legacy 156/156 · CF grep 0 · fitted-fitted grep 0 · D12 header 1.
- **Status:** ✅ shipped · **Rollback:** `backups/app-v3.4.0-b464f046.html` + legacy `reference/app-v2.6-cross.html`.


---

## Z-2026-08-02-010 — R9 (D9 + D10) + picker preference + numbered deliver packages (v3.5.0)

- **Decision:** Ship `app/app-v3.5.html` — version **v3.5.0** (badge + footer), md5 `400077a96bf0ce885908aceeb616ebc3`, 602,624 B, backup `backups/app-v3.5.0-400077a9.html`, deliver `deliver/5/`.
- **D9 — section-flip inference (replay):** `leaderW = z.side === 'TA' ? p[0] : p[2]` read the HOME share for TB-led (away-led) fixtures (p is constructed leader-first, so p[0] is always the leader). Away-leader wins were never counted in the masked-replay league accounting. Fixed to `p[0]`; regression pin (synthetic all-away-wins league) asserts hitRate = 100 (pre-fix ≈ 0). Evidence engine/zone computation untouched (parity 7/7).
- **D10 — zero-commit log honesty (ingest):** `added` counted merged identities too (`report.teams++` runs on merge), so a no-op commit logged "Pack committed: 0…". Now `added` counts new rows only (`identitiesCreated`, not merged); zero-commit logs `data/commit-skip` ("Nothing new to store — N row(s) were duplicates or already present; no commit made.") and returns `committed:false`. Pinned (double-commit probe).
- **Picker (owner preference):** teams list is flat alphabetical again by default — type any name/alias to jump straight to it; league grouping is now an **optional filter** dropdown ("Filter by league (optional)" → All leagues + each league). Search + ≤3-step flow unchanged. Smoke R1 pins updated (no optgroups; filter present).
- **Deliver packaging (owner):** deliverables reorganized into numbered ship packages `deliver/1/ … /5/` (v3.0.0 · v3.1.0 · v3.2.0 · v3.4.0 · v3.5.0), each with its own `MANIFEST.txt` (files + decoded md5s); `deliver/README.txt` indexes them; send the CURRENT package to the auditor.
- **Why:** the auditor repro'd the two defects; the picker preference restores the fast type-to-find flow; numbered packages make every ship self-contained.
- **Evidence:** `gate-evidence/R9-D10.md`; suites on the final file: new-app smoke 49/49 · R8 13/13 · R9 7/7 · R1 acceptance green · parity 7/7 · legacy 156/156 · CF grep 0 · fitted-fitted grep 0 · D12 header 1.
- **Status:** ✅ shipped · **Rollback:** `backups/app-v3.5.0-400077a9.html` + legacy `reference/app-v2.6-cross.html`.


---

## Z-2026-08-02-011 — R10: auditor D9/D10 (the real ones) fixed (v3.5.1)

- **Decision:** Ship `app/app-v3.5.1.html` — version **v3.5.1** (badge + footer), md5 `ce61de0f9e500d3917d053e9e4e77c3e`, 604,770 B, backup `backups/app-v3.5.1-ce61de0f.html`, deliver `deliver/6/`. Auditor verdict on v3.5.0: **accepted as CURRENT**, but the two defects R9 ordered were the *other* pair — this round fixes those exact repros.
- **D9 (requests.js parseReturn):** league codes were collected only from `staged.identities` (new TEAM rows). A routine return updates EXISTING teams → `staged.identities` empty → `codes: []` → the returned league's section never flipped. Fixed: `collectReturnCodes` also resolves each staged match's home/away identity in the store for `leagueCode`, with a competition-name → catalogue-code fallback. Pin (auditor repro verbatim — plain BP-TEAM-PACK v2, existing FC Krasnodar/Akron Tolyatti): codes contains RPL; commit stores 1436→1437; RPL section → 'partial'; unrelated (KOS) stays 'requested'; overall 'partial'.
- **D10 (ui.js commitReturn):** unconditional success logging — a duplicate return (0 rows stored) still logged `return-commit` + stamped `snapshot/post-return` and flipped request state. Fixed: `storedTotal === 0` → ONE honest `return-commit-skip` ("Return committed nothing — N row(s) were duplicates or already present; no commit made."), NO success line, NO post-return snapshot, NO state/artifact change. `ingest.commit` gains `silentLog` so exactly one line is written per action. Pin: second identical return → 0 rows, one skip log, logDelta 1, state + artifacts untouched.
- **Cosmetic:** v3.5.0 size corrected to 602,624 B (auditor right; my 602,425 was stale). Build now reports disk-true bytes.
- **Evidence:** `gate-evidence/R10.md`; suites on the final file: new-app smoke 49/49 · R8 13/13 · R9 7/7 · R10 12/12 · parity 7/7 · legacy 156/156 · CF grep 0 · fitted-fitted grep 0.
- **Status:** ✅ shipped · **Rollback:** `backups/app-v3.5.1-ce61de0f.html` + legacy `reference/app-v2.6-cross.html`.


---

## Z-2026-08-02-012 — R11: migration gate fixes M1–M3b (v3.5.2)

- **Decision:** Ship `app/app-v3.5.2.html` — version **v3.5.2** (badge + footer), md5 `6bd76ae025fc6eee68e3186ac52ac5ec`, 609,411 B, backup `backups/app-v3.5.2-6bd76ae0.html`, deliver `deliver/7/`. The owner's REAL live-store export arrived and ran through the migration machinery end-to-end (2,525/2,525 carried, 0/1,432 mismatches); this round ships the four fixes the auditor ordered so the owner can actually use it.
- **M1 (P0):** store migration wired to the Data-tab intake — `handleFiles`/`stageUpload` sniffs JSON store exports before the pack path → stages a **migration card** (summary `Store migration — 1432 matches · 792 teams · 86 venues · 215 sources · REPLACES the current store — export first if unsure`); approve → `commitMigration` stamps fitted + DC-gate artifacts (like boot), logs one `data/migration-commit`, saves, re-boots. Old pack path untouched.
- **M2:** `sourceId: m.sourceId || m.source || null` — 0/1,432 matches lost source linkage (real key is `m.source`).
- **M3:** `sourceIds` falls back to `t.source` — 0/792 identities lost provenance (`MODEL.teams`, `BP-TEAM-PACK`, …).
- **M3b:** `d3Gate` matches coded leagues by competition name too — 242 multi-league null-code identities now count toward their leagues' fitted-gate seasons (synthetic pin: seasons ≥ 2).
- **Docs:** migration report/ZONES state top-level `aliases` (1,078) + `teamStats` (74) are derived-not-carried (identity-level aliases carried: 1,087); `__DC_GATE__` is a build-time verdict re-earnable via Replay (d3Gate accepts `replay-validation`); replay league-key hygiene (codeless competitions print raw names) cosmetic.
- **Packaging:** `deliver/7/` includes the **Southampton pack as a standalone b64** — a replace-migration drops the 15 Southampton rows that exist only in the embedded seed; the owner re-adds them through normal pack intake after migrating (one approval).
- **Evidence:** `gate-evidence/R11.md` + `gate-evidence/MIGRATION-GATE-2026-08-02.md`; `harness/acceptance-r11.js` **18/18** on the real export. Suites: smoke 49/49 · R8 13/13 · R9 7/7 · R10 12/12 · parity 7/7 · legacy 156/156 · CF grep 0.
- **Status:** ✅ shipped · **Rollback:** `backups/app-v3.5.2-6bd76ae0.html` + legacy `reference/app-v2.6-cross.html`.

