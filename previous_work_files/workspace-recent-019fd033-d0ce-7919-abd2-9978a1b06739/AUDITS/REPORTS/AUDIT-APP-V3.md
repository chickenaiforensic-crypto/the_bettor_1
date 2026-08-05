# AUDIT — app-v3.html (builder return #1, 2026-08-02)

Auditor: core system (owner-side). Method: static greps + real boot in node/vm sandbox + golden-fixture
recompute + cache-mutation proof. Every claim below carries output previously printed to console in
this session. Nothing asserted without output. Legacy app and handoff bundles untouched.

**File:** `uploads/app-v3.html` · 577,187 B · 10,152 lines · md5 `c581428e77eb785129ea0ee3b8ec9515`
**Builder packet:** the HTML file only — no gate-evidence, no receipts, no ZONES trail.

---

## 1 · What passed (verified by execution, not by reading claims)

| # | Check | Result |
|---|-------|--------|
| P1 | Boots in clean sandbox; 9/9 seed packs commit | **PASS** — 0 seed-skip log lines |
| P2 | Store | 539 identities · 1,436 matches · 77 venues · 79 seasons · 224 sources · 3 mutes · 10 artifacts · 164 notes; migration log "2,529 rows carried" — internally consistent |
| P3 | Canonical pack fidelity | All 6 handoff packs embedded **byte-identical** to `HANDOFF/packs/` (diff-clean). Closure seed identical (93,302 B, decoded) to legacy app's embedded copy. ZERO data tampering |
| P4 | Flagship engine port — Krasnodar v Fakel | **EXACT match** to our canonical recompute: S_=78.5714 → zone WIN-DRAW gated-from-WIN (C2); H2H 3/3/6 lead 50 · Common 39/3/42 lead 92.86 · L3 7.5/4.5/15 lead 50 · npaths 36 · goals 2.352 LOW (table n=68, "under 2.5 landed 57.4%") · home star 100 |
| P5 | Mutes excluded from compute | 3 MUTE rows retained in store (no-abolition ✓) and excluded from evidence — proven indirectly: zone math matches our mute-excluding canonical run to 4 decimals |
| P6 | League registry derived from data (44 entries), not hardcoded | PASS |
| P7 | Live compute / cache | **PROVEN BY MUTATION**: injected 1 MATCH row (2026-07-30) → storeHash changed `b6b1b2af95fc`→`547be9b23dd3` → zone moved 67.1%→67.7% and gate C11 fired ("star drop: cold trailer"); form window shifted correctly. Nothing hardcoded in the result path |
| P8 | Honesty on no-data fixture | Atlanta United FC v Austin FC → refusal "No shared matches — a split would be a fabrication.", form-from-own-rows shown. Unknown-side fixture → "NO CALL — a number would be a fabrication." Correct discipline |
| P9 | Intake doctrine | ZERO `<textarea>` in file; single file input `accept=".txt,.md,.csv,.json"` + dropzone — paste retired per Annex F |
| P10 | Network hygiene of app's own code | No fetch/XHR/sendBeacon/websocket anywhere in the app code (see B1 for the one exception that disqualifies this as-is) |
| P11 | Surface vocab at boot screen | Rendered 73,635 B — zero hits for hash/fingerprint/engine/graph/localStorage/JSON/store/cache |
| P12 | Architecture | canon · store · ingest · derive · elo · evidence · dc · confidence · replay · compute · requests · ui — single store, one result object, one confidence gate, capability-probe router. Matches WO §4 tree |
| P13 | Ghost SC1 fixture (Ross County v St Johnstone) | Fitted path with stars null + `adjusted:false`, TOSS "D Coin-flip" — no invented strength. Provenance note names the migrated fit |

## 2 · Findings — BLOCKERS

**B1 — Foreign network code injected (line 10151).** A Cloudflare challenge-platform script
(`/cdn-cgi/challenge-platform/scripts/jsd/main.js`) with a hidden iframe is embedded after `</body>`.
The WO convention is one self-contained file, **no network calls**; this phones home to a third party
the owner never approved and proves the file transited a Cloudflare proxy. **Delete; hand-back a file
whose last line of JS is the app's own. Gate: `grep -c "cdn-cgi" app.html` must print 0.**

**B2 — Zero gate evidence delivered.** Their own PLAN defines P0/P1/P2 gate files (golden-matrix diff,
migration report on the real store, cache/derive/artifact reports, rollback rehearsal). We were handed
only the .html. My sandbox confirms several gate ITEMS pass (P-column above), but their protocol —
the one they wrote and the owner approved — says **asserted-without-output = failed gate**. The build
cannot be accepted until `gate-evidence/` arrives with commands + raw outputs, reproducible.

**B3 — D11 violated (skin).** Ships `data-theme="dark"` default + a dark↔light toggle (line 2; line 2828).
Ruling D11: **light editorial, one skin, no toggle.** Also the skin comment says "dark premium default +
light editorial toggle" — the enterprise decision was not honored, it was inverted.

**B4 — Scope order broken.** A2 ruled core-first P0–P2, gate evidence reviewed BEFORE P4+. They ran to
P6 (full skin + console) in the first return without the checkpoint. Deviation registered; owner to
absolve or hold.

## 3 · Findings — INTEGRITY / HONESTY (fix before phase acceptance)

**I1 — Forged approval in the immutable log.** Boot commits seeds with `ownerApproved: true` hardcoded
→ the store log contains 9 "commit" entries implying owner approval that never happened. Fix: log as
`system-seed` (honest action type) or route seeds through the owner-approval intake once.

**I2 — '?' placeholders leak to users.** Compute's `CONF.gate()` call never passes `effective`/`agree`
(call site ~line 2298 vs gate fallback line 2089 → sublabel renders literally "effective ? paths ·
agreement ?"). The values exist (`ev.ag.effective`, line 2273). One-call-site fix.

**I3 — Mute reasons flattened.** Store mutes carry reason "imported muted flag"; the pack rationale
("integrity: market-flagged favorite collapse (IA-02)" + z-scores) is lost from the store field.
Owner rule: mutes stay visible WITH reason.

**I4 — No-abolition held; keep it.** Retained muted rows ✓ retained ghost identities ✓.

## 4 · Findings — POLISH / DATA

- **P-a** League registry: NA-code closure teams leak name-as-code entries ("Highland League",
  "Lowland League", "National League", "Scottish League One/Two", second "Scottish Championship"
  beside SC1). SP1 and SP2 both display "Spain La Liga". Display collisions; canon should issue clean
  display codes for the NA class.
- **P-b** Alias strictness: "Atlanta United" unresolvable (store name "Atlanta United FC", aliases []).
  Picker-driven UI makes this acceptable; suffix-aware canon is cheap polish.
- **P-c** G11 half-open: Southampton pack loaded (real 2026-07-30 commissioned pack — the one WE never
  received, owner evidently gave it to the builder) — but **Ross-County/St-Johnstone pack absent and
  undocumented**. G11 requires load-or-document.
- **P-d** Provenance string duplicate: "Dixon-Coles (ENGINE_SPEC v1.0, fitted fitted scoreGrid …)".
- **P-e** Commit log #8 shows dedupe working (HIB_MAL 29 MATCH rows → 2 new commits; 27 exact-dup
  fingerprints rejected). This is correct and worth noting in their P1 evidence.
- **P-f** MLS universe remains the round-1-sparse state (85 matches): MLS shows honest no-call + form.
  Expected per F-C gate; round-2 bulk is the standing researcher order.

## 5 · OWNER RULING NEEDED (one question)

**Seeds inside the app file.** The app ships 9 real canonical packs embedded and auto-loads them at
first boot through the one ingest gate (validated, deduped, logged). A4 ruled "honest empty state — no
placeholder/demo data ships". These packs are real, not fabricated — but shipping data inside the app
file means every app update re-ships data and first-boot bypasses the drive-folder approval flow
(Annex F). Two clean resolutions: (A) accept embedded canonical seeds as the app's published baseline,
log them as system-seed (fixes I1 too); (B) seeds leave the file, app boots empty, packs arrive via
file intake with owner approval per pack.

## 6 · Verdict

**Real build, real port, honest engine — but NOT acceptable yet.** B1 (foreign network code) and B3
(D11 inversion) are direct convention/ruling violations; B2 is the builder's own protocol unmet; I1
put an untruth in the permanent log. None require architectural change: ~hours, not days. Phase call
after fixes + gate evidence: P1 core ✓-leaning, P2 ✓-leaning (cache proof mine, theirs pending),
P0 PENDING (their golden matrix absent), P6 SKIN NOT APPROVED (D11).

---

## Addendum (2026-08-02, ~17:00) — status after owner's phone session
- **B3 retired:** owner decree D11-A — skin as shipped (dark + toggle) stands; the light-only ruling was withdrawn by the owner.
- **B2 partially closed:** P0/P1/P2/P6 gate evidence received and cross-audited — consistent with this audit's independent runs. Remaining: final `app-v3.html` + `trail/ZONES.md` + backup md5 for the CF grep (B1) and identity recount (520 vs 539).
- **Seeds:** accepted by owner's live use of the seeded app; I1 (system-seed logging) still owed.
- **New owner-facing fix list R1–R5 dispatched** (picker surfacing/final file/two-sided evidence card/RPL D3-gated fitted card/identity recount). R4 is the doctrine-legal route to the full stats card for Russia.

---

## Addendum 2 (2026-08-02, ~17:45) — R-round verdict: ACCEPTED (residual cosmétique R6)

Re-audited `app-v3.1.html` (uploads) + builder trail + corrections doc. Full battery re-run (4 script blocks only, node vm boot, probes).

**Transit finding (proven):** the uploaded file arrived with a fresh Cloudflare block (new token) — removed 938 bytes → md5 becomes exactly the builder's stamped `3048f269c7153fe18c9a7eae944cd752`. The CDN injects it on every .html download; the builder's own file is clean (their CF-grep=0 claim TRUE on their bits). Verified-clean copy shipped to owner as `/home/user/app-v3.1.html`. Future transfers: base64 .txt only. (Their stated "586,532 B" vs actual 586,571 B: 39-byte misreport; md5 controls — identity certain.)

**R1 ✓** `PR.ui.filterTeams`: "" → 539; "krasnodar"→FC Krasnodar; "fakel"→Fakel; "ross county"→Ross County; alias "hibs"→Hibernian; optgroup "Russian Premier League".
**R2 ✓/✗** seeds log `system/seed` ×9, zero ownerApproved in log ✓; '?' eliminated — real values render ("effective 3 connections · agreement 64%") ✓; **I3/mute claim FALSE on file** — store mutes still "imported muted flag" ×3 while the doc claims "pinned in store". Asserted, not proven — their own §1 rule. → R6-a.
**R3 ✓** records verified at engine level: HIB-MAL L3 Hibernian 3W-2D-6L (13-16, 11g) vs Malisheva 3W-0D-3L (9-15, 6g); Malisheva-Drita L3 1-0-0 (2-0, 2026) vs 0-1-4 (5-10, 2025–26) — matches their rendered sample.
**R4 ✓✓** CSKA v Krylia fitted-online: 0.591/0.239/0.170 exactly; provenance + Brier 0.5621-vs-0.5929 note on card; permanent log entry #11 `system/dc-gate` records the enablement. Krasnodar v Fakel: STRONG 77.
**R5 ✓** identities 539; categories 167 unrated + 372 rated (their 149+34+372 breakdown overlaps by 16 — presentation loose, total right).
**Doctrine parity intact** on probes HIB-MAL (58.2 TB), MLS NO CALL+form, legacy fitted Celtic 0.509/0.216/0.275.
**Trail audit:** fresh engine_spec arrived directly from owner (G10 CLOSED — builder trail Z-002 logs md5 `91cd0cd5…`); owner's "all main files are coming" irected builder defaults before my rulings zip — earlier "violations" (seeds, dark+toggle) were owner-driven all along; registry entries stand corrected (v0.25 D11-A).

**R6 (cosmetic, hours):** (a) map pack MUTE reason → store.mutes.reason, prove by store print (their claim was FALSE) ; (b) version pin: badge+footer unique per shipped file (rev2 must not display "3.0.0" like rev1); (c) all transfers via base64 .txt drill; (d) "fitted fitted" provenance typo.
**R7 (request):** on replay-validated fitted leagues (RPL/CZ1) keep the evidence graph reachable under one tap — owner explicitly uses the graph sections; don't hide them behind the fitted monopoly.

---

## Addendum 3 (2026-08-02, ~19:15) — FINAL SEAL: v3.4.0 accepted, R9 tail-list (2 real defects in the Requests flow)

b64 drill on the final packet: **5/5 files decode to manifest md5s exactly** (app 601,011 B → `b464f046b097403a5a91132f26f520ae`). Static gates: CF/cloudflareinsights 0 · external src 0 · textarea 0 · fitted-fitted 0 · `league-<code>-<window>` generation 0 · D12 header 1 · 4 script blocks · APP_VERSION 3.4.0 single-source (badge+footer). Runtime: store 1,436/539/3 stable · 9× system/seed · **mute reasons NOW carry IA-01/02/03 verbatim + source (previous false claim now true)** · zero ownerApproved in log.

Re-probes on v3.4.0: R1 "krasnodar"→FC Krasnodar / 539 reachable · R4 CSKA 0.591/0.239/0.170 + provenance · R7 graph section present on fitted cards · R5 539.
D12 verified end-to-end: button → 2 files + artifact(sent, 44 sections) + system/request log · snapshot format/requestDate/storeHash ✓ · request header/return-to naming exact · 44 sections, 0 excluded (correct for data ending 08-01) · **244/244 real team lines date-exact** · 19 compressed placeholders for unstocked leagues with named windows · plain-pack return: ok, +2 matches, request→partial.
**Verdict: ACCEPTED — sealed.** Verified app shipped to owner as `/home/user/app-v3.4.html` + md5-stamped backup; b64 drill is now the only transport.

### R9 — tail-list (hours; before heavy reliance on the Requests fulfilment display)
1. **D9 — section flips are dead for routine returns.** `parseReturn` collects section codes only from NEW identities a return creates; weekly returns contain only existing teams → `codes=[]` → no league section ever flips (RPL stayed 'requested' after a committed RPL return) while overall state flips to 'partial' unconditionally. Fix: infer codes from staged match rows' league names too; flip only real ones. My repro + line refs shipped.
2. **D10 — zero-commit returns log success.** Failed blocks still produce `data/return-commit … 0 matches` + `snapshot/post-return` stamps. Fix: committed.matches===0 → log 'return-rejected', no snapshot stamp, toast the truth.
3. **Docs:** DELIVERY-README recycles stale facts (v3.1.0/dad4babd/589,191) in the final packet. Their 13/13 R8 acceptance did not cover the D9/D10 classes — add the two pins.

---

# ADDENDUM 4 — v3.5.0 (R9 round) — 2026-08-02 18:5x

**Ship received:** `app-v3.5.0-400077a9.b64.txt` + ZONES-v3.5.0.b64 + R9-D10.b64 + MANIFEST + 2 raw .html.
**b64 drill:** 3/3 decode → md5 EXACT vs MANIFEST (app `400077a96bf0ce885908aceeb616ebc3` = true build, 602,624 B; zones `58ca2c01…`; r9 `cd63ccb7…`).
**Channel:** both raw .html = true build + 1×938 challenge + 1×352 insights; strip 2 blocks → md5 `88ff6567…` = true + 1 stray `\n`. Channel guilty 5th time; b64 remains law.

## Static gate (true file)
APP_VERSION '3.5.0' single source; badge L2782 + footer L3166 both interpolate `STORE.APP_VERSION` ✓ · 4 script blocks · textarea 0 · fitted-fitted 0 · CF refs 0 · external src/href 0 · grammar header ×1 · ownerApproved:true only in code paths (L604 legacy-mute synthesis, L3218 owner file-approve, L3291 return commit) — seeds commit `seed:true` w/o ownerApproved (L10593) ✓.

## Runtime gate (node vm, 4-block boot, harness audit35/audit_v35.js — outputs above)
| # | Probe | Expected | Got | Verdict |
|---|---|---|---|---|
| A | boot counts | 1436/539 stable | 1436 matches · 539 ids · 539 reachable · 0 flags | ✅ |
| A | seeds | 9× system/seed, 0 ownerApproved | 9 · 0 · mute reason IA-02 verbatim | ✅ |
| B | R1 search | krasnodar→FC Krasnodar | ["FC Krasnodar"] · fakel→Fakel Voronezh | ✅ |
| B | R4 fitted path | fitted | path.kind=fitted (CSKA-Krylia) | ✅ |
| C | **D9-as-specified** (routine return, documented grammar, existing teams only) | RPL section flips "requested"→"partial" | parseReturn codes=`[]` → section stays **"requested"**, overall flips "partial", log `return-commit … 1 matches, 0 teams ().` | ❌ **OPEN** |
| D | **D10-as-specified** (all-duplicate return) | no return-commit / no post-return | `data/return-commit … 0 matches` + `snapshot/post-return` both logged | ❌ **OPEN** |
| E | their D10 (ingest double-commit) | committed:false + commit-skip, no "Pack committed: 0" | committed=false · `data/commit-skip "Nothing new to store — 1 row(s)…"` · no false line | ✅ real fix |
| F | their D9 (replay TB-led hitRate) | 100 (pre-fix ≈0) | SLG hitRate=100 (n=22) | ✅ real fix |

## Findings
- **R9 mismatch:** builder fixed two GENUINE bugs matching the D9/D10 labels (replay.js L2251 leader-share read; ingest.js L1042 added-count) — both independently re-proven ≈0→100 / no-op→skip. The two defects the auditor specified and repro'd (parseReturn L2689 codes from `staged.identities` only; commitReturn L3306-3307 unconditional logs) were NOT touched (L2689/L3306 byte-same behaviour as v3.4.0). Root: forwarding carried labels, not the repro text. R10 carries the verbatim repro.
- **Compound (recorded in R10):** a return block rejected by validation (e.g. stray line → `unknown row type`) commits 0 rows yet commitReturn STILL logs return-commit + post-return and flips overall state to "partial". Unknown-row strictness itself (v3.4 silent-tolerate → v3.5 block-reject) is an honesty improvement; documented returns unaffected.
- **Picker:** flat alphabetical + optional league dropdown (owner→builder direct preference; not in registry — function verified, R1 pins hold).
- **Cosmetic:** their R9/Z-010 docs state 602,425 B — actual 602,624 B (digit transposition; md5 correct, gate by md5 stands).

## Verdict
**v3.5.0 ACCEPTED AS CURRENT** (net-positive: two verified real fixes, zero regressions on documented paths; D9/D10-as-specified remain → **R10 tail**, verbatim repro forwarded this time). CURRENT = `/home/user/app-v3.5.html` md5 `400077a96bf0ce885908aceeb616ebc3`; backup `backups/app-v3.5.0-400077a9.html` (identical); rollback anchors intact (v3.4.0 `b464f046…`, legacy `14a7a957…` 156/156).

---

# ADDENDUM 5 — v3.5.1 (R10: auditor D9/D10) — 2026-08-02 19:1x — **CLOSED**

**b64 drill:** 3/3 md5-exact vs MANIFEST pkg 6 → app 604,770 B = `ce61de0f9e500d3917d053e9e4e77c3e` (builder's byte/md5 docs exact this round).
**Static gate:** APP_VERSION '3.5.1' single (zero stale 3.5.0) · textarea/CF/fitted-fitted/external-src all 0 · 4 script blocks · grammar header ×1.
**Diff footprint vs v3.5.0:** 68 lines, surgical, zero scope-creep — L357 version · ingest `silentLog` wrapper (all non-return paths unchanged) · `collectReturnCodes` (identities + per-match home/away identity resolution + competition→catalog fallback) · commitReturn early-return skip. Read line-by-line, approved.
**Runtime verdict (harness audit351/audit_v351.js — contract = Addendum 4 repros, verbatim):**
- **D9 PASS every clause:** codes `["RPL"]` (was `[]`) · 1,436→1,437 stored · log `return-commit … (RPL)` · **RPL section → partial** · unrelated ALB stays "requested" · overall "partial" · honest post-return stamp only because rows stored.
- **D10 PASS every clause:** duplicate return → +0 rows · logDelta exactly 1 = `data/return-commit-skip` ("Return committed nothing — 1 row(s)…") · NO return-commit success · NO post-return · request state JSON + artifacts count byte-identical before/after.
- **Regressions:** 1,436/539 · seeds 9 · ownerApproved 0 · R1 krasnodar/fakel · R4 fitted · D12 sections 44 · ingest commit-skip (non-silent path) intact · synthetic replay hitRate 100 intact.
**Their docs:** R10.md + Z-011 claims match verified reality (12/12 pin set = my contract clauses; size correction 602,624 B acknowledged).
**SEAL: v3.5.1 = CURRENT.** `/home/user/app-v3.5.1.html` + `backups/app-v3.5.1-ce61de0f.html` (md5 `ce61de0f…` both). Anchors: v3.5.0 `400077a9…`, v3.4.0 `b464f046…`, legacy `14a7a957…`.
**Builder trail-list EMPTY.** Programme remaining = owner homework (live store export · Ross/St-Johnstone pack) + standing offers (slate re-verification · settlement run) + researcher pipeline on owner's word.

---

# ADDENDUM 6 — v3.5.2 (R11: migration gate M1–M3b) — 2026-08-02 20:2x — **CLOSED**

**b64 drill:** 5/5 md5-exact vs MANIFEST pkg 7 (app 609,411 B `6bd76ae025fc6eee68e3186ac52ac5ec`; Southampton pack `2d4b5ed0…`; their MIGRATION-GATE.b64 = our doc byte-identical `68fc34d7…`).
**Static:** APP_VERSION '3.5.2', 0 stale version strings; all banned greps 0; grammar header ×1.
**Diff vs v3.5.1: 141 lines, all ordered scope** — M1 `stageUpload` JSON-sniff + migration card + `commitMigration` (stamps fitted+gate like boot, `data/migration-commit`, save, re-boot) · M2 `m.sourceId||m.source` ×2 sites · M3 `t.source→sourceIds` · M3b d3Gate competition-name fallback · `approveStaged` router.
**Runtime (audit352/audit_v352.js + DOM-drop sims — outputs in session):**
- Seed-side regressions: 1,436/539, krasnodar ✓, CSKA fitted ✓.
- **M1:** file-input drop of the REAL export → migration state → approve → persisted **1,432/792/86/215**; log tail `system/fitted-migrate, system/dc-gate, data/migration-commit`; artifacts dc-fitted-model ×5 + dc-gate-validation; CSKA–Krylia = **fitted** on migrated store; row integrity 1,432 resolvable / 0 mismatched. Old "Rejected — 38,877" path gone; pack path unaffected. Visible-card sentence proven at template level (`filesView` .staged-info ← `C.esc(f.summary)` with exact wording) — sandbox DOM can't faithfully switch console tabs; functional chain proven end-to-end.
- **M2/M3 pins:** 0 null sourceId (matches) · 0 empty sourceIds (identities).
- **M3b pin:** d3Gate seasons=2 with all identities' leagueCode nulled (competition-name fallback) · fitted:false without replayWin artifact (correct semantics preserved).
- **Southampton door:** same file-input → approve → 1,432→**1,447** (+15 exact), `data/commit`.
**Their docs:** R11.md claims = independently verified true (all pins re-run auditor-side); core gate table matches our method.
**SEAL: v3.5.2 = CURRENT.** `/home/user/app-v3.5.2.html` + `backups/app-v3.5.2-6bd76ae0.html` (`6bd76ae0…`). Southampton pack pinned at `/home/user/Southampton_BP-TEAM-PACK_v2.txt` (`2d4b5ed0…`). Anchors: v3.5.1 `ce61de0f…`, v3.5.0 `400077a9…`, v3.4.0 `b464f046…`, legacy `14a7a957…`.
**Migration path is now open end-to-end.** Owner sequence: v3.5.2 → Files tab → drop live export → Approve migration card → drop Southampton pack → Approve → 1,447 rows.
