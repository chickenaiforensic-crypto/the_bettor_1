# ZONES v0.5 — calibrated zone instrument (shipped in app-v2.8.0-cross, tuned 2026-08-01)

Final presentation for every evidence-engine fixture: per-section summations and
one TOTAL summation (TA / Draw / TB out of 100%), read through this ladder.
Supersedes v0.4 — v0.5 adds: C8 opponent-quality-weighted current-tourney
performance rating shipped (v2.8.0, demote-only, CALIBRATION-4.md). Earlier:
C2 gate (v2.6.9), C4 context layer dormant (v2.7.0), C5 draw-risk drop (v2.7.1),
Candidate A measured and REJECTED.

Summation source: evidence-weight distribution across all paths, neutral band
|est| ≤ 0.25 (engine buckets — exact rule in aggregate()). Shares sum to 100%.
Engine math identical to the v2.6.9 calibration state (Candidate A reverted).

## Calibration sample
671 games replayed blind, cutoff = each kick-off (strict causality):
- 610 RPL rows (2024-25, 2025-26, 26-27 MD1, cups; leak-free universe,
  both seasons reconciled 16/16 vs official tables)
- 61 UECL/domestic pack rows
- 600 games yielded evidence; 71 NO CALL (no paths — correct discipline).
Log: replay_zones_log.csv (per-game H/D/A, leader, zone, actual).

## Shipped zone table (post-gate + C5 + C8, zone_tally_ctx.js on frozen v2.8.0)

| Zone | n | leader W | D | L | leader-or-draw |
|---|---|---|---|---|---|
| **STRONG CALL** (S ≥ 85, gate-passed) | 59 | 78% | 14% | 8% | 92% |
| **WIN** (65–85, gate-passed, has H2H) | 118 | 67% | 15% | 18% | 82% |
| **WIN-DRAW** (55–65 + demotions) | 166 | 49% | 25% | 25% | 75% |
| **lean** (50–55 + demotions) | 109 | 47% | 24% | 29% | — |
| **TOSS** (<50 + demotions) | 148 | 45% | 25% | 30% | — |

Ladder is now strictly monotone in leader W (78 > 67 > 49 > 47 > 45); pairs run
92 / 82 / 75 / 71 / 70. Demotions only ever move confidence down (C2 gate, C5
draw-risk, C8 performance, CTX flags) — nothing inflates it.
Pre-C8 engine table (computeZone only, zone_tally.js) frozen for reference:
strong 60: 78/92 · win 125: 65/80 · windraw 201: 48/72 · lean 97: 53/78 · toss 117: 43/68.

Region naming: leader = TA → home zones; leader = TB → **home-lose regions**.
Dual zones settle as covered by either outcome of the pair.

## Measured leader-share curve (pre-zone, n=600) — unchanged math

| Leader share S | n | leader won | draw | opp won | leader-win% | leader-or-draw% |
|---|---|---|---|---|---|---|
| 45–55 | 212 | 98 | 53 | 61 | 46% | 71% |
| 55–65 | 146 | 69 | 36 | 41 | 47% | 72% |
| 65–85 | 166 | 101 | 31 | 34 | 61% | 80% |
| 85–100 | 74 | 54 | 9 | 11 | 73% | 85% |

## Rules in force

1. **Ladder (v0.2 anchors):** STRONG ≥85 · WIN ≥65 · WIN-DRAW ≥55 · lean ≥50 · else TOSS.
2. **C2 confirmation gate:** WIN/STRONG require ≥2 of 3 sections agreeing with the
   leader at ≥55% section share; else demote to WIN-DRAW. Contra-leading section
   ≥55 prints as a flag. (Gated STRONG 78%/92%, n=60 — best subgroup in the system;
   quarantined bucket 42% w — correctly demoted.)
3. **C5 draw-risk drop (v2.7.1):** post-gate WIN with **no H2H evidence** → WIN-DRAW.
   Measured: that cohort drew 31% vs the 18% pool rate (n=26, pairs at 85%).
   STRONG exempt (its no-H2H cohort wins 80%, n=20).
4. **C4 context flags (v2.7.0, dormant until CTX packs are fed):** demote-only
   tripwires on a named fixture date — `keeper-change`, `star-absence`,
   `new-manager-debut`, `rotation-risk`. One rung per flag against the zone
   leader; flags against the trailer are listed, never boost (blueprint rule).
   Syntax: `CTX|team|YYYY-MM-DD|flag|detail|source`.

## Per-section measured health (total settles; sections guide trust)
- H2H leads 75%+: n=249 → 59% win / 80% w-or-d. At 60–75: only **39% win**.
- Common leads 75%+: n=229 → **64% win / 83% w-or-d** (best per share).
- Level-3 leads 75%+: n=283 → 48% win / 70% w-or-d (corroboration, not standalone).

## Warnings (standing)
1. **STRONG sub-bands:** 85–90 measured 0% loss / 100% leader-or-draw (n=23);
   ≥90 carries every post-gate STRONG loss (14%, n=37) — the h2h-blowout tail
   survives the gate at low frequency. Variance-level signal (n=5) — annotated, no rule.
2. 95–100% raw-share pocket: 65% leader-win, 7 losses — h2h-only inflation.
   Candidate A (venue correction + saturation) was built and A/B-replayed:
   **no gain on any motive, pocket worse (36% vs 44%) — rejected, engine reverted**
   (full record: CALIBRATION-3.md §1).
3. Recency weighting (C6): losses skew older evidence (260d vs 207d median) but
   actionable splits show no discrimination (pair 84/84) — measured-weak, not taken.
4. NO CALL ~10.6% is correct discipline, keep. 20-game forward slate under frozen
   v2.7.1 re-checks anchors prospectively; C3 side-adjusted anchors parked until then.

## Applied
- Rubin v Akron (18 Apr 26 replay): TA 61 / D 15 / TB 24 → **WIN-DRAW → actual 1-1 → zone-hit.**
- Akron v Rubin (1 Aug 26 logged under v2.6.9): H 10 / D 20.6 / A 69.4 → **TB WIN, call: Rubin** — settles vs 90-min score.

## v0.6 — re-baseline after RPL cup-completeness load (2026-08-01)
Universe 612 → 643 rows (RPL 488, CUP 152, SUP 1, RPLPO 2); masked replay now covers 632 games with evidence.
- v2.7.1 table: strong n=40 W73/pair90 · win n=134 W63/pair82 · windraw n=230 W50/pair75 · lean n=105 W50/pair77 · toss n=123 W37/pair67
- v2.8.0 (shipped, computeZoneCtx): strong n=38 W74/pair89 · win n=129 W65/pair83 · windraw n=189 W52/pair78 · lean n=116 W48/pair72 · toss n=160 W38/pair68
- Ladder strictly monotone on both W% and pair% under the enriched universe; C8 audit T1 standalone buckets monotone (23/34/52/54/64); T2 disagree subsets still worse than agree on every rung.
- Akron v Rubin re-run: TA 10.0 / D 19.4 / TB 70.6 → **TB WIN 70.6%** (frozen pre-load call was TB WIN 69.4%; zone family unchanged, verdict stands).

## v0.7 — C11 shipped (v2.8.1, 2026-08-01)
Cold-trailer star guard: trailer star<5 on STRONG/WIN demotes one rung.
Post-ship ladder (632): strong n=15 W80/pair93 · win n=101 W69/pair89 ·
windraw n=240 W53/pair77 · lean n=116 W48/pair72 · toss n=160 W38/pair68.
Strictly monotone. Pool reconciliation: canonical pool = 704 (61 seeds+packs, 643 RPL).
Audit: CALIBRATION-5.md. C9 contra-section gate measured and REJECTED (cohort W71).

## v0.8 — display layer (v2.8.2): auto-audit standby request emitter
Optional per-fixture data requests (AUTO-REQUESTS.md). Display-only — ladder and all
zone behavior identical to v2.8.1. No re-calibration needed.

## v0.9 — display layer (v2.8.3): request block UI
Standby requests now render as an executive component: collapsed by default, typed
items, Copy templates and Download .txt (identical payloads). Zone logic untouched.

## v0.10 — C13 TB away-leader honesty gate shipped (v2.9.0, 2026-08-01)
TB-led STRONG/WIN demote one rung (demote-only; intermediates v2.8.4–2.8.9 live in
CALIBRATION-7/8/9.md and INTEGRITY-AUDIT.md: C7 weights+band, C8 last-6 window,
C9 display calibration, 3 integrity mutes).
Post-ship ladder (633, post-mute): strong n=9 W100/pair100 · win n=38 W79/pair87 ·
windraw n=257 W63/pair85 · lean n=101 W48/pair73 · toss n=228 W39/pair69.
Actionable n=304 actW 66.1 / pair 85.5 — identical to v2.8.9 totals, labels now
honest (TB strong ran 83 n=6, TB win 62 n=37 pre-gate; both halves replicated).
Audit: CALIBRATION-13.md. V1 full-TB demotion recorded as available strict-mode
trade (+4-5 actW for −36% volume), not default.

## v0.11 — pack-league discovery + honest calibration label (v2.9.1, 2026-08-01)
User catch: the league filter listed only the 18 embedded leagues, and classify()
was hard-coded `false` — every loaded fixture, incl. RPL-RPL, wore the
"cross-border / no calibrated table" label. Two display-layer fixes, engine
bit-identical (zone table, shares, CAL9, gates all unchanged):
1. League filter now surfaces pack-loaded leagues (from identity league codes)
   ABOVE the embedded 18 — e.g. "Russia — RPL (loaded pack)"; refreshes after
   every import. Filter stays display-only, never restricts rating.
2. `bpSameCalibrated(hid,aid)` computes classify()'s calibration input instead of
   literal false: both teams sharing a code in CALIBRATED_PACK_LEAGUES = {RPL}
   (entry earned via the 633-game replay) → "Calibrated domestic". Cross fixtures
   keep the honest "Lean only". Adding a league requires its own replay doc.
Functional pin: same fixture flips Calibrated domestic ↔ Lean only when one
side's league tag moves RPL ↔ CZ1 (smoke C18, suite 114/114).
v2.9.2 hardening: packLeagueList filters legacy junk tags (NA / unknown /
"loaded team data") at read time — older store states can't pollute the list.
Functional pin C18b: real russian pack import surfaces RPL (and FNL, correctly)
in the filter; suite 116/116. NOTE: the live store only shows Russia after
re-importing packs/russian-team-pack.txt — the pre-regeneration pack carried
league code NA, so old identities have no RPL tag.

## v0.12 — tag canonicalization + silent-edit incident (v2.9.3, 2026-08-01)
User-reported duplicate Scotland rows led to the root cause of ALL name-format
league tags: the app embeds a seed (HIB_MAL_SEED_PACK, parsed by the LEGACY v1
grammar at load — league field = NAME, not code). User pack imports run the
strict-v2 parser correctly (verified live: russian import = strict, 3 mutes
applied). Fix: LEAGUE_ALIAS + canonLg at every read point (filter list, picker
dedupe, filter match, calibration check) — "Scottish Premiership"→SC0 merges the
seed tag; Hibernian double-row deduped to its single rated row; SC1 stays
(legit Championship: Raith/Morton/Ayr). Albania/Denmark/Ireland name rows are
genuine European-opponent seed teams, not duplicates.
INCIDENT DISCLOSURE: v2.9.2's badge + SKIP edits silently failed to persist
(tool-reported success; file unchanged — caught by comparing backup checksums
against pins). Re-applied in v2.9.3 with post-edit grep verification as standing
protocol; version pin now checks badge AND footer explicitly.
backups/app-v2.9.2-cross.html is MISLABELED (contains v2.9.1 content) — retained
as evidence; true v2.9.3 snapshot saved with md5 verification.
Suite: smoke 124/124 · closure 19/19 · packs 27/27 · rpl import clean · concat 61.

## v0.13 — team-name canon layer (v2.9.4, 2026-08-01)
Owner-reported: "Krylya Sovetov Samara" spelling would not take despite a
respelled pack + html update. Root cause (same family as the Dynamo duplicate
false alarm): pack identity keys are NAME-derived (idKey = country|name) and
persist in the user's local store — html carries zero team names, so no app
edit can relabel a loaded identity, and re-importing a respelled pack MINTS A
SECOND identity + duplicates every match. Never do that.
Fix (label-only, zero engine change): TEAM_NAME_CANON {"krylya sovetov samara"
→ "Krylia Sovetov Samara"}; both entry points (addIdentity, resolveName)
canonicalize, so EITHER spelling keys onto ONE identity forever;
migrateTeamNames() runs on every store load and rewrites an existing store in
place — identity key, match homeId/awayId + fingerprints (deduped, muted flag
unioned), aliases, teamStats, venues, ctxFlags. Zero data loss; mutes ride the
match rows. Test hook: BlueprintEmbed.migrateNames.
Numbers-untouched proof: md5 of perfRatings/aggregate/sectionShares/computeZone/
computeZoneCtx/zoneLadder/classify/bpSameCalibrated all IDENTICAL to the v2.9.3
backup; NEUTRAL_BAND/PHASE_WEIGHT/CAL9 constants unchanged. Zone table frozen.
Data side: rpl_names.json respelled; packs/russian-team-pack.txt regenerated
(693 lines, 26 teams, 644 MATCH, 3 MUTE, old spelling kept as TEAM-row aliases);
rpl import re-verified clean (0 errors). NOTE: do NOT load the respelled pack
into any pre-v2.9.4 html copy — on old builds the new spelling would key as a
second identity. v2.9.4 migrates the store automatically on load; no re-import
needed. Smoke: migrateNames pin suite added (C20 ×8). Version pin checks badge
AND footer. Backup md5-verified (5987dfcd8bdd8daa24e54eaf90f1404b).
Suite: smoke 132/132 · packs 27/27 · rpl import clean.

## v0.14 — same-class sweep + MLS round-1 intake (v2.9.5, 2026-08-02)
Owner directive: no fix ships without sweeping for siblings of that defect.
Sweep results: (1) LEAGUE-CODE-NA class — 15 TEAM rows across hibernian/
malisheva/closure packs recoded (KOS ALB DEN IRL NIR SRB POL SVN CYP SWE ISL
MLT); user heals by one re-import of each recoded pack (zero-drift merge,
pattern proven on czech: 1336→1336 matches, leagues repaired). (2) FILTER-
DUP class — recoded codes collided with seed NAME tags (Albania×2 etc., the
Scotland v2.9.3 pattern); LEAGUE_ALIAS extended (ALB/DEN/KOS/IRL name→code),
all read points already canon-wired: 48 raw tags → 43 filter rows, one per
league. (3) 14 embedded-seed stub identities remain league-less by design
(cup-opponent placeholders, zero matches; tagging would assert unverified
divisions — documented, not patched). MLS round-1 (WORKORDER-MLS): pack built
as EVIDENCE-CARRIER ONLY (packs/usa-team-pack.txt: 45 TEAM/85 MATCH/17 NOTE;
5 AET scores corrected to 90-min per doctrine; 6 slugs added incl. missing
fc-cincinnati; MLS/USL/USL1 codes populated pre-emptively). NO replay, NO
calibration, NO CALIBRATED_PACK_LEAGUES entry — full-season bulk (round 2) is
the gate. 6-pack census: 1421 matches / 792 identities / 3 mutes, drift exact
(+85/+45/0); duplicate+GAP audit 0. Engine md5 parity vs v2.9.4 backup: all 8
functions IDENTICAL; zone table frozen. Smoke 133/133 (C19+1 alias pin,
version pin badge+footer). Backup md5-verified (70b84a8bcef4a66c6b72a75e568da119).

## v0.15 — unified evidence presentation (v2.9.6, 2026-08-02)
Owner finding: "two different apps in one" — three render pipelines each
stacked their own card pile; on rated fixtures the model card was followed by
scattered evidence text and a loose paths card, with gate flags interleaved as
help-text and no zone statement at all. Owner layout decision: model-led frame
(stars/rating/markets card is good, stays), evidence reorganised INTO one
structured panel, paths as a separate audit card always last.
Shipped: evidencePanelHtml + evidencePathsCardHtml — ONE evidence read for all
three pipelines: (1) header labeled by instrument (never anonymous numbers);
(2) single final statement: NO PLAY banner (gates eff<2 / agree<60% /
|weighted|<0.35, frozen pin strings preserved) or zone tag headline with
leader/paths/effective/agree subline; (3) sections as one table — per-phase
H/D/A %/Σw plus Total raw + CAL9-calibrated rows; (4) form strip (star/SOS/
perf/conversion); (5) gates & flags grouped under one subhead (C2/C5/C8/C11/
C13/CTX, each named — the C13 marker moved here without text loss); (6) goals
read display-only; (7) separate paths card last (count footer now also carries
unweighted est + spread). On model screens the panel is silent when no rows
connect the sides (previous behaviour kept). Removed: the standalone "Blueprint
evidence audit" append card, the summary/summation scatter renderers (dead
code, 7.2 KB), all interleaved help-text flags. Render proven bit-identical
to frozen audit numbers (Makhachkala v Lokomotiv: 0/60/40 · 6/38/56 · 30/35/35,
display 20.9/34.5/44.6, NO PLAY at agree 49%). Engine md5 parity: all 8
functions IDENTICAL vs v2.9.5 backup; zone table frozen; zones remain
statements, evidence shares never dressed as probability. Smoke 137/137
(7 stale-structure pins rewritten to the unified anchors, 4 new C21 pins);
backup md5-verified (b9be62df8d70b10323e3209fcb099b39).

## v0.16 — presentation revert (v2.9.7, 2026-08-02)
Owner decision after side-by-side review: the v2.9.6 unified design is poorer
than the ORIGINAL evidence layout (banner strips, prose summation, "Total
summation" block, zone line). Revert executed wholesale AND verifiably: the
app file equals the v2.9.5 backup byte-for-byte except the two version strings
(version-stripped diff = 0 lines); the removed renderers
(evidenceSummationHtml/evidenceSummaryHtml, "Blueprint evidence audit" append
card, interleaved flag lines) are all back. v2.9.6 retained untouched at
backups/app-v2.9.6-cross.html for reference. Everything non-presentational
from 2.9.4/2.9.5 rides along unchanged (canon migration layer, league-alias
sweep, MLS evidence-carrier pack — app-external data + canon, none of it the
criticised design). Engine md5 parity vs v2.9.3: all 8 functions IDENTICAL;
zone table frozen. Smoke pins restored to the original structure anchors
(7 pins back to v2.9.5 wording, C21 unified pins removed, one revert pin
added) — 134/134. Next step per owner: evidence stats to be shown as part of
the model stats panel — integration design to be agreed before any further
presentation edit. Backup md5-verified (e262e6116194b4a1fe5d276988ca69f4).

## v0.17 — same-league loaded fixtures get the standard design (v2.9.8, 2026-08-02)
**Trigger (owner):** screenshot of "Evidence verdict — cross fixture" for CSKA Moscow v Krylia Sovetov Samara + directive: *"audit your work and ensure all leagues you have added produce results like the actual app design before your evidence section — and dont send me unaudited files"*.

**Audit (audit_league_paths.js, fresh 6-pack store 1421 matches / 792 identities / 3 mutes):**
- Root cause: the standard model card (`renderDomesticRate`) only fires for `kind:"R"` picks in the same league, and `MODEL.teams` covers exactly the embedded 18 leagues. Every pack-loaded league (RPL, FNL, CZ1, CZ2, SC1, KOS, DEN, MLS, USL, USL1 + single-team ALB/IRL etc.) had NO domestic-card branch, so intra-league fixtures fell to the bare cross-fixture evidence card.
- Pre-fix census: 11 stocked pack leagues with ≥2 same-league sides all rendered EVID-X; mixed B+R intra-league pairs (e.g. SC0 rated v pack-loaded) same. Zero duplicate display names found (sweep clean).

**Ship (presentation-only; engine md5 parity v2.9.7→v2.9.8 proven across 12 core fns):**
- `sharedLoadedLeague(hid, aid)`: same-league detection — shared declared canon league code, with a **h2h domestic-league-meeting fallback** so stale stores (junk `NA` tags, pre-heal) still frame correctly. Display-only; never feeds the engine.
- Same-league loaded fixtures render: "Pitch rating — \<League name\>" card → classify/gates banner → **Standard stats lead** (CALIBRATION-9 share bar + zone statement + star/SOS/performance/conversion + CALIBRATION-6 goals band; **NO model markets, NO scorelines** — those exist only for the embedded 18) → titled evidence sections (Section balances. / Total summation. / Zone statement.) → collapsed Evidence paths → save (log row now carries the league tag).
- `BP_LEAGUE_NAMES` display-name table drives the card title, league filter labels ("Russia — Russian Premier League (loaded pack)") and picker rows.
- Cross fixtures unchanged (evidence-verdict framing kept; pin-verified); R+R domestic and R+R cross pipelines untouched.
- Delta vs v2.9.7 backup: 129 version-stripped diff lines, all presentation. Smoke 134→**148/148** (C22: 14 pins). Per-league post-fix census: every stocked same-league pair renders LEAGUE-STD. Stale-store probe: junk-tagged CSKA v Krylia still renders "Pitch rating — Russian Premier League" via the h2h fallback.
- Backup: `backups/app-v2.9.8-cross.html` md5 `b8afd84d2bc5eeb456428c6d2326ac0f`.
- Honest correction logged: the earlier chat message describing a "v2.9.8" ship had not in fact landed on disk (file was still v2.9.7); this entry is the actual ship.

## v0.18 — zero-path honesty: standalone form shown, ghosts admit no data (v2.9.9, 2026-08-02)
**Trigger (owner):** *"why will there be a league with no loaded evidence? ... except there was deception going on"*.
**Connectivity census (census_connectivity.js, fresh 6-pack store, cutoff 2026-08-02):**
- Full-bulk leagues: RPL 171/171, FNL 21/21, CZ1 171/171, CZ2 325/325, KOS 45/45, DEN 3/3, USL1 1/1 pairs connected — **100%**.
- Round-1-sparse leagues: MLS 343/435 (79%), USL 48/78 (62%) — expected at intake (F-C gate: evidence-carrier-only pending round-2 full match-level bulk).
- SC1 0/21 — **different root cause**: the 7 SC1 identities come from the embedded MASTER_RECORD_CLOSURE_SEED_PACK, which deliberately carries TEAM/VENUE/SEASON/SOURCE rows and **no MATCH rows** (record-closure pack). Ghost league tags, no graph. Pack-file cross-check: hibernian pack mentions none of them.
**Mechanics (the answer):** shares/zones are computed ONLY from connecting paths (H2H / common opponents / level-3 chains); a pair whose loaded opponent sets never meet has no path, and inventing a number there would be the deception the owner suspected. perfRatings (Elo K20/HF65, last-6) needs no connection.
**Ship:** loadedLeagueLeadHtml zero-path branch → `standaloneFormLeadHtml`: shows star/SOS/performance/conversion/games per side computed from each side's own rows, with "no share split and no zone" stated; if BOTH sides have zero match rows the card says "Team form — no data. ... nothing to compute" and shows NO numbers. Engine parity v2.9.8→v2.9.9 proven (11 core fns md5-identical). Smoke 148→**156/156** (C23 pins incl. Atlanta United v Austin zero-path render + SC1 ghost render). Final per-league census: connected→full stats, unconnected→standalone form, ghosts→honest no-data. Backup md5 `14a7a9572f2428eb1689a2f601c3583c`.
**Open owner question:** SC1 ghost TEAM rows — keep (card now states truth) or commission real SC1 match data (WorkOrder); stripping TEAM rows would drop the record-closure SEASON linkage.

## v0.19 — owner rule registered: NO DATA ABOLITION (2026-08-02)
Owner decree, verbatim scope: **every data field that leads to the final computation must be fully available; no data field or row is canceled or abolished — the only exclusion mechanism is the MUTE blacklist on suspicious games, nothing else.**
Consequences: (1) the earlier "strip ghost TEAM rows vs commission data" question is dead — ghost declarations (incl. all 7 SC1 identities in the embedded seed) are **retained verbatim** and cured by commissioned data; SC1 is commissioned in full in Annex A of `WORKORDER-PITCH-RATING-REBUILD.md`. (2) MUTE rows stay visible, excluded from all compute paths, reversible on owner-approved lists only. (3) Pack grammar fields may not be dropped even if no current computation uses them. Enforced at: WORKORDER-PITCH-RATING-REBUILD §3-8, §6-P3, §9, Annex A (row completeness), Annex D (migration).

## v0.20 — data-operations architecture registered (2026-08-02)
Owner rulings folded into `WORKORDER-PITCH-RATING-REBUILD.md` as **Annex F** + doctrine §3-7 and engineering conventions amended: (1) intake is **file-based only** — linked drive folder primary, file picker secondary, paste-text retired (formats: .txt/.md header-sniffed, .csv, .json backups); (2) the app **generates data-request files itself** (scope, grammar with filled example, sources, acceptance checks, expected filename + drop point); (3) class doctrine binding: surface never speaks backend (no store/hash/key/fingerprint/graph rows/engine jargon/raw JSON), status is icon-encoded with detail behind one tap, flows are ≤3 visible steps — audited by grep; (4) six-module Data Ops console (Files · Coverage · Requests · Calibration · Log & Settlement · Integrity & Snapshots); (5) league lifecycle labels REQUESTED→STAGED→LOADED→CALIBRATED→STEADY/→DORMANT with rows retained forever in DORMANT (no-abolition). Awaiting owner green light to hand the full work order to the engineer.

## v0.21 — builder return: transmission failure identified, bundle re-packed, 4 rulings surfaced (2026-08-02)
Owner forwarded the app builder's session reply (8 docs: BINDING-STATUS / DECISIONS / GAPS / PLAN / ZONES / README(1) / WO(1) / merger WO). **Status: no code written** — builder executed a correct cold start per WO §0/§8: stopped on the incomplete bundle, logged 12 gaps (G1–G12) with WO-mandated fallbacks, opened a fresh ZONES with the log-loss recorded, and returned 4 rulings (Q1 bundle handling · Q2 scope · Q3 UI direction · Q4 seed policy). Conduct verified as discipline-compliant; nothing silently assumed.
**Root cause (verified):** builder received exactly **2 of 40** bundle files (README + master WO). Their copies checked byte-identical to originals — WO md5 `005f58a579cd6e9f403378baee948248`, README md5 `acd25b03717b727691aa203419b5b876` (diff IDENTICAL, both). The prepared HANDOFF/ bundle never reached them; this was a **transmission failure, not a bundle defect**.
**Action:** re-packed as `HANDOFF-PITCH-RATING-v2.zip` — 40 files + `BUNDLE-MANIFEST.md5` (40 pins); zip md5 `2cb6415135aeaaedfa9f74496fad5f99`; re-extraction verify `md5sum -c` = **40/40 OK**. Builder-side receipt check is now a one-line command, so a repeat drop is machine-detectable.
**Flag for owner:** builder's PLAN P6 records a "session amendment" citing an owner ask (*"excellent UI delivery"*) to build the skin **in-build** — this reverses the registered decision (skin deferred to the professional-designer WO after wiring). Awaiting owner confirm/reject before it stands; if rejected, P6 reverts to plain-but-skin-ready.
**Still missing (owner-supplied, unchanged):** ENGINE_SPEC.md or written port-only sign-off (builder G10 → P2 DC fit held); Southampton + Ross-County/St-Johnstone packs (G11); owner's live store export (G12 → P1 real migration gated). No builder question overrides the D1–D10 register; D10 already fixes phase order.

## v0.22 — owner rulings A0–A4 registered; D11 created; bundle v3 packed (2026-08-02)
Builder's 4 blocking questions ruled by owner (ask_user, 2026-08-02):
- **A1/Q1 — send full bundle** (no WO-alone fallback).
- **A2/Q2 — core-first**: D10 order confirmed; first return = P0–P2 gate evidence; owner/auditor review precedes P4+.
- **A3/Q3 — amendment CONFIRMED, registered as D11**: UI skin built in-build at P6; direction **light editorial, single skin, no toggle**; P6 gate "skin approved by owner" stands; P8 designer pack still produced as polish/spec handover, not a build gate. (This amends the earlier designer-after-wiring decree — owner's own reversal, register-formalized so it is auditable.)
- **A4/Q4 — honest empty state**: no placeholder/demo data ships in the app; synthetic fixtures live only in harness/gate-evidence, never importable into the app.
**Shipped:** `HANDOFF/RULINGS-2026-08-02.md` (md5 `0449a759bae1316f4164cf1d24fed3d7`) — binding-on-receipt memo answering Q1–Q4, closing G1–G9 on bundle arrival (real artifacts supersede fallbacks; DC port opens via the G10 "legacy parameters" branch once the legacy app lands; fresh vs historical ZONES: link, don't merge), restating the 3 open owner items (ENGINE_SPEC/port-only sign-off · Southampton+Ross/St-Johnstone packs · live store export).
**Bundle v3:** `HANDOFF-PITCH-RATING-v3.zip` = 41 manifest-pinned files + manifest; zip md5 `c7f598d93a78941a7e128ccc7056e55e`; re-extraction verify `md5sum -c` = **41/41 OK, 0 failures**. Receipt on the builder side is one command; any shortfall = stop-and-report per the memo.
**Owner homework unchanged:** the 3 items above.

## v0.23 — transport workaround: Arena blocks .zip uploads (2026-08-02, owner report)
Arena upload rejects .zip. Bundle re-wrapped, **contents unchanged**: `HANDOFF-PITCH-RATING-v3.zip` → base64 → `HANDOFF-PITCH-RATING-v3.zip.b64.txt` (334,420 B, md5 `501e9906cba174b0eb85963807034717`).
Round-trip verified before giving to owner: b64-decode → zip **byte-identical** (md5 `c7f598d93a78941a7e128ccc7056e55e`, both) → unzip → `md5sum -c BUNDLE-MANIFEST.md5` = **41/41 OK**. Builder receipt = 3 steps pinned in the delivery note: decode → zip md5 match → 41 × OK; any mismatch = stop and report. No file inside the bundle was edited; RULINGS-2026-08-02.md remains accurate (zip name/md5 unchanged).

## v0.24 — audit of builder return #1 (app-v3.html, 2026-08-02)
Full report: `AUDIT-APP-V3.md`. File 577,187 B · 10,152 lines · md5 `c581428e77eb785129ea0ee3b8ec9515`. Method: sandbox boot (node vm), golden-fixture recompute, cache-mutation proof — all with printed output.
**Passes (13):** 9/9 seed packs commit, 0 skips; 1,436 matches + 539 identities; 6 canonical packs + closure seed byte-identical (zero tampering); flagship fixture Krasnodar v Fakel matches our canonical recompute EXACTLY (S_=78.5714, WIN-DRAW via C2, 36 paths, 2.352 LOW); mutes retained-and-excluded (math identity proof); store-hash-keyed derive PROVEN by mutation (zone 67.1→67.7 + C11 fired on 1 injected row); honest NO CALLs; file-only intake (0 textarea); no app-side network code; boot screen vocab clean; module architecture matches WO §4; dedupe works (27/29 HIB_MAL rows rejected as exact-dups).
**Blockers: B1** Cloudflare challenge script + hidden iframe injected post-`</body>` (network call in a no-network file — file transited a proxy; must delete) · **B2** zero gate-evidence delivered (their own PLAN: asserted-without-output = failed gate) · **B3** D11 inverted: dark default + theme toggle vs ruled light-editorial single skin · **B4** scope: ran to P6 before the P0–P2 checkpoint review.
**Integrity: I1** seeds committed with hardcoded `ownerApproved:true` — 9 untrue approval entries in the immutable log (fix: system-seed action or real approval) · **I2** `CONF.gate` call-site never passes effective/agree → "effective ? paths · agreement ?" leaks to users (data exists at line 2273) · **I3** mute reasons flattened to "imported muted flag".
**Polish:** NA-code league labels collide (double "Scottish Championship", SP1/SP2 both "Spain La Liga") · strict aliases ("Atlanta United" unresolvable) · Ross-County/St-Johnstone pack absent + undocumented (G11) · "fitted fitted" provenance typo.
**Owner learning:** the missing Southampton pack (2026-07-30 commissioned) that never reached us was given directly to the builder — it is inside and verified well-formed.
**Verdict:** real build, honest engine, exact port — not acceptable yet; fixes are hours-scale. Open owner question: embedded canonical seeds as published baseline vs empty-boot + file intake per pack (AUDIT §5).

## v0.25 — gate evidence received + cross-audited; owner amendments D11-A + seeds-accepted; owner field report from phone (2026-08-02)
Builder delivered P0/P1/P2/P6 gate evidence. **Cross-audit vs our own records/runs: consistent** — legacy md5 matches our v2.9.9 backup hash; census 792/1421/3 matches ZONES v0.14; suite counts match; store 1,436/3 matches my sandbox boot; engine parity 7/7 consistent with my independent Krasnodar probe (S_=78.5714 exact). Open discrepancies pinned for final-file recount: identities 520 (their P1) vs 539 (my boot of the prior file); CF-script removal unproven until final html arrives.
**Owner decree D11-A (supersedes D11):** *"leave the dark mode - we will manage it"* — skin as shipped (dark premium + light toggle) stands; the light-editorial-only ruling is withdrawn by the owner. My B3 flag is retired.
**Seeds: accepted by use** — owner runs the seeded app daily; registered as baseline-seeds accepted, with the standing correction that commits must log as system-seed, never ownerApproved:true (I1 still owed in writing).
**Owner field report (screenshots):** fitted card fully visible (rating/stars/tier history/markets+fair odds+calibration error/BTTS-withheld-honesty/scorelines) — owner: *"over 100 times requested"*. His 3 complaints decoded: (1) stats vanished before — answer: RPL gets the same full card ONLY via D3-gated fit on the 644 in-store RPL rows + masked-replay validation (ordered as R4; failure = show the table, never fake); (2) *"couldnt find krasnodar - russia"* — data verified present (644 matches, card computes), it's a picker surfacing defect → R1 (searchable, alias-tolerant, ≤3 steps); (3) evidence sections unreadable → R3 two-sided per-section W-D-L presentation ordered.
**Fix list R1–R5 dispatched to builder** (picker · final file+CF grep+I1/I3/I2 confirmations · evidence two-sided card · RPL/CZ1 D3-gated fit · identity recount).
**Still owed by owner:** live store export (G12) · Ross-County/St-Johnstone pack · ENDs the missing-item list; ENGINE_SPEC optional (port branch open, P2 fitted ship verified).

## v0.26 — R-round audit: REBUILD ACCEPTED (residual R6 cosmetics); channel injected tracker PROVEN (2026-08-02)
Second full audit (details: AUDIT-APP-V3.md addendum 2). **VERDICT: ACCEPTED.** Verified on file: R1 search pins (krasnodar→FC Krasnodar; 539 reachable; aliases work) · R2 seeds `system/seed` ×9 / zero ownerApproved / '?'-placeholders gone · R3 two-sided records real (engine-level W-D-L·GF-GA·dates per side per section) · R4 fitted-online live for RPL+CZ1 (CSKA 59.1/23.9/17.0 exact; Brier 0.5621 vs 0.5929 on card; permanent log #11 system/dc-gate) · R5 identities 539 · legacy parity spots unchanged (HIB-MAL 58.2, MLS honest NO CALL, Celtic 0.509/0.216/0.275).
**Channel proof:** uploaded app-v3.1.html carried a FRESH Cloudflare injection (new token) — strip 938 B → md5 = builder's stamped `3048f269c7153fe18c9a7eae944cd752`. The CDN injects on every .html download. Verified-clean copy at `/home/user/app-v3.1.html` (this is the phone-safe file). Standing rule: builder↔owner transfers in base64 .txt drill only.
**One FALSE claim caught in their gate doc:** "mute reasons pinned in store" — store mutes still show "imported muted flag" ×3. Same asserted-not-proven sin as before; fix demanded as R6-a with store-print proof.
**Registry corrections:** ENGINE_SPEC.md arrived directly owner→builder (their trail Z-002, md5 `91cd0cd5…`) — **G10 CLOSED**; owner's "all main files are coming" had already directed builder session defaults (embedded seeds + dark/toggle) before the rulings zip — earlier flags B3/A4 were owner-decided all along; v0.25 D11-A recorded correctly.
**R6 demanded:** (a) mute-reason mapping + proof; (b) unique version pin per shipped file (rev2 currently displays "3.0.0" same as rev1); (c) b64 transport; (d) "fitted fitted" typo. **R7 requested:** graph view stays one tap away on fitted leagues.
**Owner:** Krasnodar now renders STRONG 77 (77.3/17.0/5.7) — fitted card won its place by beating the graph 0.5621-vs-0.5929 in blind masked replay; frozen slate untouched for old settlements.

## v0.27 — programme wrapped: accepted state pinned, residuals assigned (2026-08-02)
Owner: *"proceed with the rest of the work and wrap this up."* Closing state:
- **NEW APP ACCEPTED** — verified file `/home/user/app-v3.1.html` (md5 `3048f269c7153fe18c9a7eae944cd752`), backup `backups/app-v3.0.0-rev2-3048f269.html` (md5-verified identical). Legacy `app-v2.6-cross.html` (v2.9.9) retired to reference; frozen slate still governs past settlements.
- **Builder owns (R6/R7):** mute-reason mapping+proof · unique version pin per ship · b64 transport · "fitted fitted" typo · graph-view-one-tap on fitted leagues. Small hours; acceptance already granted.
- **Owner owns (2):** live store export (`pitch-rating-full` from old app Data tab → migration gate run) · Ross-County/St-Johnstone pack (P3).
- **Pipeline:** Brazil WO ready to dispatch on owner's word · MLS round-2 supplier order open (WORKORDER-MLS) · SC1 cure queued behind Annex-A researcher bulk · Swiss pack per owner's go · WTA parked.
- **Standing offers (on request):** frozen-vs-current slate re-verification (Krasnodar 75.8-FROZEN vs recompute flag) · settlement run vs SLATE-2026-08-01-03.md once the result ledger starts in the new app.
- Closing summary doc: `PROJECT-STATUS-2026-08-02.md`.

## v0.28 — owner decree D12: CENTRAL REQUEST SYSTEM (2026-08-02; third-incarnation requirement finally written into the register)
Owner, verbatim: *"a central system update that takes snapshots of everything, the teams' last game updates and the request date — so that from a central request you can cover the entire system and also return it there. Why do I see a per-league update request — this is the 3rd time we are doing this app and each time I have to repeat wording."*
**Honest why (owner deserves it):** the per-league design was written in Annex F by us (WO line ~333: `league-<code>-<window>-<date>.txt`); the builder implemented the binding document faithfully — this was a registry failure, not builder disobedience. The requirement from earlier incarnations was never carried into a binding document. Now it is.
**Registered:** `AMENDMENT-2-CENTRAL-REQUEST.md` — one [New central request] action producing `system-snapshot-<date>-<hash>.json` (full store) + `central-request-<date>.txt` (one file; each league needing work = a SECTION; every team line carries its real last-store-game date + plain-words gap; omissions need written reasons) · central return to the same Files intake (`central-request-<date>-r<n>.txt` matched to the open request, ONE approval, per-section validation, post-return rollback snapshot) · separate per-league request files ABOLISHED · Requests tab reduced to [New central request] + open-request fulfilment + archive.
**Pinned into the master WO** (both copies) with a supersession banner at Annex F — new WO md5 `9103d2fac1b80d3eb80e02149cad0bc6` (was `005f58a5…`); builder side: their canonical-copy protocol handles the overlay (AMENDMENT-2 + banner travel in the next b64 packet).
**Builder acceptance pins issued as R8** (grammar header `PITCH-RATING CENTRAL-REQUEST v1`; last-game dates spot-checked vs store for 5 teams; one-approval return commit flips coverage per section; grep proves per-league filename generation gone).

## v0.29 — stale-corpse forensics: channel claim CONFIRMED; v3.2.0 deliverable still in transit (2026-08-02)
Owner forwarded ONE file: `uploads/app-v3.1-stripped.html` (589,153 B, md5 `df94ae48593e499011200c4fccd9bfa7`). Autopsy: a **pre-v3.2 build** (APP_VERSION '3.0.0'; zero CENTRAL-REQUEST; zero "fitted on Russian") transporting **FOUR foreign Cloudflare artifacts**: 2× challenge-platform IIFE (938 B each) + 2× cloudflareinsights beacon module scripts (352 B each, external src + integrity attr + `data-cf-beacon` JSON). After stripping all 2,580 injected bytes: **0 external references remain**; corpse ≈ v3.1-generation minus 2 whitespace bytes at the injection junction (not any stamped clean build — consistent with double-injection on a stale serve). Builder's b64-only rule and "CDN delivers stale, beacon-tagged builds" claim: **confirmed in substance** (their truncated "352-byte beacon" matches the insights blocks exactly).
**The actual final deliverable did NOT arrive:** `deliver/app-v3.2.0-fb4b037d.b64.txt` (claimed md5 target `fb4b037da77d8ed40f8204e6209f15a6`) + trail/evidence b64s are missing from the packet. Final seal is pre-staged and runs on arrival: decode → md5 match → boot battery (R6a store print, version pin, greps CF/fitted-fitted/D12-header, CSKA R7 details element, R8 central-request simulation + return matching, counts) → seal + PROJECT-STATUS bump to v3.2.0.

## v0.30 — FINAL SEAL: v3.4.0 ACCEPTED (b64 drill 5/5; full battery re-run; R9 tail-list issued) (2026-08-02)
Delivery packet decoded + verified 5/5 md5-exact (app 601,011 B → `b464f046b097403a5a91132f26f520ae`). All greps clean (CF 0 · external src 0 · textarea 0 · fitted-fitted 0 · per-league generation 0 · version chrome single-source 3.4.0). Runtime store stable 1,436/539/3; 9 system/seeds; **mute reasons now truthful (IA-01/02/03 + source)**; fixtures re-probed: krasnodar search ✓ · CSKA fitted 0.591/0.239/0.170 + provenance ✓ · graph one tap ✓. D12 end-to-end: button writes snapshot+request+artifact+log; 44 sections; **every one of the 244 real team lines carries its true last-game date**; return commits through one approval; post-return snapshot stamped.
**SEAL: the rebuild is ACCEPTED.** Verified copy `/home/user/app-v3.4.html` + backup `backups/app-v3.4.0-b464f046.html`. b64-only transport is now law for this channel.
**R9 tail-list (hours, honest):** (1) D9 — return section flips dead for routine returns (codes read only from NEW identities; fix: infer from match rows too); fulfilment icons mislead until fixed. (2) D10 — zero-commit returns log success + stamp a snapshot; fix: reject log + no stamp. (3) DELIVERY-README carried stale facts; add D9/D10 pins to their R8 suite (their 13/13 missed both classes).
**Status doc bumped:** PROJECT-STATUS-2026-08-02.md → v3.4.0. Standing owner items unchanged: live store export · Ross-County/St-Johnstone pack.

## v0.31 — v3.5.0 ACCEPTED AS CURRENT (R9 round; D9/D10-as-specified STILL OPEN → R10 with verbatim repro) (2026-08-02)
Delivery package 5: b64 drill 3/3 md5-exact (app 602,624 B → `400077a96bf0ce885908aceeb616ebc3`); both raw .html = true build + 938+352 CF junk (strip → true + 1 stray `\n`) — channel guilty 5th time. Version chrome single-source 3.5.0 (badge L2782 · footer L3166); all greps clean; seeds 9/0; store 1,436/539/0 stable; R1 krasnodar/fakel pins hold.
**Verified real fixes (both independently re-proven):** replay TB-led leader-wins now counted (synthetic all-away-wins league hitRate 100, pre-fix ≈0 — replay.js L2251) · ingest no-op commits now log honest `data/commit-skip` + `committed:false` (double-commit probe, ingest.js L1042).
**R9 mismatch:** the two defects the auditor specified are UNTOUCHED — parseReturn L2689 still collects codes from new identities only (routine RPL return: 1 match stored 1,436→1,437, codes=[], RPL section stays "requested", overall flips "partial", log `return-commit … ()`) · commitReturn L3306-3307 still logs `return-commit … 0 matches` + `snapshot/post-return` on zero-commit returns — proven on the DOCUMENTED return grammar (plain BP-TEAM-PACK v2). Compound: a validation-rejected return block also flips overall state with 0 rows stored. Root cause of mismatch: forwarding carried labels, not the repro text.
**Also:** picker → flat alphabetical + optional league dropdown (owner→builder direct preference, unregistered in DECISIONS; function verified). Unknown-row strictness (v3.4 silent → v3.5 block-reject): honesty improvement, documented returns unaffected. Their docs state 602,425 B (actual 602,624 — transposition; md5 governs).
**SEAL: v3.5.0 = CURRENT.** `/home/user/app-v3.5.html` md5 `400077a9…` + backup `backups/app-v3.5.0-400077a9.html` (identical); anchors intact (v3.4.0 `b464f046…`, legacy `14a7a957…`).
**R10 (forwarded verbatim, this time WITH the repro):** in requests.js parseReturn (~L2689) collect league codes from `staged.matches` league fields/identity map AS WELL AS new identities → routine returns flip the returned league section; in ui.js commitReturn (~L3306) when total committed matches+teams = 0 (or all blocks rejected) log a rejection note and DO NOT log `data/return-commit` success, DO NOT stamp `snapshot/post-return`, DO NOT flip overall state; add both pins (auditor repros in AUDIT-APP-V3.md Addendum 4 C/D are the acceptance contract).

## v0.32 — R10 CLOSED: v3.5.1 SEALED AS CURRENT; builder trail-list EMPTY (2026-08-02)
Package 6 b64 3/3 md5-exact (`ce61de0f9e500d3917d053e9e4e77c3e`, 604,770 B — their docs exact). Diff vs 3.5.0 = 68 surgical lines (collectReturnCodes + silentLog + commitReturn skip + version), read line-by-line, zero scope-creep. **Contract repros (Addendum 4 C/D) pass verbatim:** routine return (existing teams) → codes ["RPL"], RPL section flips "requested"→"partial", unrelated section holds, log names the league; duplicate return → +0 rows, exactly one `data/return-commit-skip`, no success line, no post-return stamp, request state/artifacts untouched. Regressions all green (store 1,436/539, seeds 9/0, R1/R4/D12, R9 fixes intact). **v3.5.1 = CURRENT** (`app-v3.5.1.html` + backup; anchors v3.5.0/v3.4.0/legacy intact). Requests fulfilment icons are truthful from this build on. Builder owes nothing; ball is with owner's homework items.

## v0.33 — Owner's live store export ARRIVED; migration core PROVEN; one blocker found → R11 (2026-08-02)
`pitch-rating-full-data-2026-08-02.json` (1,132,200 B · md5 `5a8ba49475acfa2340ce7fd66e4dfeb0`) — 1,432 matches (22 comps, through 2026-08-01) · 792 identities · 86 venues · 215 sources · 1,078 aliases · 74 teamStats · 0 mutes · 0 ghosts. Ran the app's own machinery end-to-end: deserialize→migrate rowsIn=rowsOut=**2,525**, 792/1,432/86/215 carried, **0 row mismatches**; real-boot flow stamps `dc-fitted-model`×5 + `dc-gate-validation` (RPL,CZ1), CSKA–Krylia = **fitted** (0.589/0.239/0.172) on owner data; picker 792 (krasnodar ✓, **Ross County ✓, St Johnstone ✓** — SC1 ghost class dies with migration). Reconciliation: owner rows = live truth (+11 vs old fixture census: 10 Scottish + 1 MOL); seeds = +15 Southampton → replace-migration + re-add pack via normal intake.
**Defects (R11):** M1 BLOCKER — no UI path to migration: real file stages "Rejected — 38,877 defect(s)" in Data tab (machinery only reachable at boot/localStorage). M2 — match `source` key unmapped → 1,432/1,432 null sourceId. M3 — identity `source` key unmapped → 792/792 no provenance. M3b — 242 multi-league identities → leagueCode null, invisible to future d3Gate season counts. Docs: aliases/teamStats = derived-not-carried; __DC_GATE__ = build-time verdict, replay re-earns.
**Verdict:** owner's data survives whole; migration is BLOCKED at the front door only. Owner homework ① received; ② Scotland pack now optional-but-wanted (teams migrate; pack still fills Scottish depth). Forward `R11-FORWARD-TO-BUILDER.md` verbatim; ship as v3.5.2.

## v0.34 — R11 CLOSED: v3.5.2 SEALED; the front door exists; league-by-league audit OPENED (RPL leg 1 done) (2026-08-02)
Package 7: 5/5 md5-exact (app `6bd76ae0…` 609,411 B). Diff = 141 ordered lines. Owner-drop simulation on his REAL export: migration card → approve → persisted 1,432/792/86/215, logs `data/migration-commit` + fitted/gate stamps, CSKA fitted on migrated data, 1,432/0 row integrity; M2/M3 nulls 0/0; M3b gate-fallback pinned; Southampton re-add +15 → 1,447. Their R11 doc = verified true again. **v3.5.2 = CURRENT** (+backup; anchors intact).
**Audit phase opened (owner decree: league-by-league data quality, 5-year cap):** AUDIT-DATA-QUALITY-2026-08-02.md. Inventory: deepest coverage starts 2024-07; RPL = 2024-25 + 2025-26 complete (240/240 each) + 2026-27 9 rows. Pasted external RPL table FAILED leg 1: "2024-25 champion Zenit" FALSE (rows say Krasnodar 67 vs 66) · Baltika row impossible (8 wins claimed vs our proven 11 in 2025-26 alone). Rule: pasted tables = test targets, never inputs. 5-year RPL needs 2021–24 commission (~720 rows) — standing offer.

## v0.35 — Russia 2021–24 backfill COMMISSIONED (owner approved); audit 5-year cap formalized (2026-08-02)
Decree registered: league-by-league data-quality audit, all leagues capped at 5 past years for flow balance, one league at a time starting RPL. Current RPL depth = 2 full seasons + 2026-27 partial → 3-season gap. `WORKORDER-RPL-2021-24-BACKFILL.md` issued: 720 league rows (3×240) + playoffs, hard cutoff <2024-06-30, RSSSF-primary + 2nd-index verify, 16/16 table reproduction gate recomputed auditor-side, identity roster pinned (FC Ufa expected new; Nizhny→Pari rename alias trap; Khimki-dissolved note), 90-min doctrine, no guessing (NOTE blocker). Cup backfill explicitly deferred. On return: table recompute + boundary dedupe → one owner approval → Russia = 5 full seasons + current; then next league (CZ1 default) repeats the shape, or cups if owner redirects.

## v0.36 — Completeness PROVEN vs independent archive: RPL 2024-25 + 2025-26, CZ1 2024-25 + 2025-26 (2026-08-02)
Owner asked "are you confident the held seasons are full?" — answered with the whole-tournament gate he proposed: uniform per-team game counts + recomputed tables vs RSSSF final tables (fetched live). **All four completed seasons: 16/16 (RPL) and 12+4 (CZ1) EXACT on W-D-L, GF-GA, pts.** Czech "intruders" (Zbrojovka/Artis Brno) = correct 2026-27 promoted-club rows. Russian/MOL cups + playoffs queued for the same diff. Repo `the_bettor_1` = public + EMPTY (0 files) — recommended as archive for returns + official-table snapshots; workflow unchanged.

## v0.37 — Fake "return" burned at intake: wrong league (Rwanda), wrong form (standings), 0 bytes in repo (2026-08-02)
Researcher claimed 5 committed files of "RPL" standings 2021–26. Probe: repo tree = README.md only; claimed paths 404; single initial commit stands. Their message self-incriminates: "I treated RPL as Rwanda Premier League" — plus standings (targets) instead of match rows (inputs), plus re-collecting 2024-26 already proven complete. Verdict: reject wholesale; correction text handed to owner; audit doc updated; repo-check evidence in `repo-check/` probe log. Workorder WORKORDER-RPL-2021-24-BACKFILL.md remains the only valid contract.

## v0.38 — Repo layout prepped for owner drag-drop: Supervisor/ + handoffs/ (2026-08-02)
Owner directed: workorder lives in repo under `Supervisor/`, returns land in `handoffs/`. No push rights auditor-side (account is owner's; no token) → workspace folder `REPO-UPLOAD/` prepared: `Supervisor/WORKORDER-RPL-2021-24-BACKFILL.md` (byte-identical copy, md5 `5635916c…`) + `handoffs/README.md` (binding return rules: match rows not tables, BP-TEAM-PACK v2, naming, no zips, 16/16 recompute gate, no-guess NOTE rule; open commission pinned as Russian PL — anti-Rwanda line written in). Owner drags both folders → Commit changes → auditor probes paths to confirm.

## v0.39 — CZ1 backfill workorder STAGED (WO-CZ1-BACKFILL-02); league queue registered (2026-08-02)
Owner: "prepare the next league workorder; we start with the active leagues we have." Census re-derived from live export: CZ1 561 rows (2024-07-19→2026-07-31, deepest comp) → next after RPL. Workorder written with zero-memory policy: all 3 rosters + rename traps (Fastav→Trinity Zlín per RSSSF's own footnote, OKD Karviná, Jablonec 97) + per-season compositions (21-22: minus Zbrojovka; 22-23: minus Karviná plus Zbrojovka; 23-24: Karviná back) pinned from live RSSSF fetches tsje2022/23/24 this session. Anti-appear list: Dukla (promoted 2024), Artis Brno (2026). Expected: 240 regular + 36 playoff-stage (Titul 15/Záchranu 15/Evropu 6) = 276/season = 828 total; shape 12×35+2×34+2×32 mirrors our verified 24-25/25-26. §0 = anti-Rwanda federation check written into the document. No TEAM rows expected (all 17 clubs on roster incl. Zbrojovka from 2026-27). STAGED per one-league-at-a-time decree: opens when RPL return passes gates; staged into REPO-UPLOAD/Supervisor/ + handoffs README queue updated. Next-after-CZ1 (owner redirects excepted): cups re-diff (auditor-side) then MOL Cup backfill commission.

## v0.40 — Cup backfills STAGED (WO-03 Russian Cup, WO-04 MOL Cup); slice rule PROVEN on live data (2026-08-02)
Owner: "work on the rest, one doc after the other." Before writing, slice-decoded both cups from the live export: MOL Cup 32+31 rows (R3-onward shape), Russian Cup 76+76 uniform (48 group + 28 bracket; 6 RPL-path group rounds of 8 visible in date clusters). Decisive probes: **0 ties without a top-flight club in either cup** → coverage rule = "every official match with ≥1 top-division club, followed through all rounds" — now the gate-reproducible scope in both workorders (auditor recomputes the rule from RSSSF; researcher declares round counts in NOTE). Knockout doctrine hardened: 90-min score + mandatory advancement NOTE per AET/pens tie. Dukla clause corrected for cup (CZ2-era legitimate; reuses existing identity). Queue registered: ① RPL league (OPEN) ② CZ1 league ③ Russian Cup ④ MOL Cup — all cutoff <2024-06-30, each opens only after the previous passes gates. All 4 + README staged in REPO-UPLOAD/ for owner's single drag. Rerouting of ③/④ order = owner's word. Owner architecture question answered: single-file app, no data folder possible; intake = Files tab front door; load order = migration FIRST (3 clicks), returns after, one approval card each.

## v0.41 — Owner decree clarified: 5-year window = CONTINUOUS to today, gap-free (2026-08-02)
Asked (genuine collision with the cap decree); owner answered in own words: "we are getting all 5 year season data up to today … ensure our data (old) is not missing anything … researching all data so that we dont get gaps." Registered: cap = backward depth (2021-22 onward); forward edge = today, always; acceptance adds a span-diff — after gates pass, auditor diffs the whole federation span vs the full research record; any official match stored nowhere = gap defect keeping the commission open (fill or NOTE-explain). Written into all 4 workorders (§5.1), handoffs README (rule 7), AUDIT doc (doctrine block), PROJECT-STATUS. REPO-UPLOAD/Supervisor/ cleaned to exactly the 4 live orders (stray Brazil/MLS/rebuild copies removed — Brazil remains standing-on-owner's-word, not queued). Workorder pins refreshed (README cb673962…).

## v0.42 — Renamed to the owner's decree: all 4 workorders + return packs → 2021-2026 span names (2026-08-02)
Owner flagged visible 2021-24 naming contradicting the up-to-today ruling. All four masters renamed `…-2021-2026-5YSPAN.md`; return packs now `<LEAGUE>-2021-2026_BP-TEAM-PACK_v2.txt`; in-file explanation box in each: name certifies the whole span while NEW rows still hard-stop 2024-06-30 (2024-26 held+verified, recollection = gate failure; 2026-27 fills via weekly central-request). Gap found and fixed on the way: the RPL master predated the Rwanda fiasco and had no §0 federation banner — added (same wording family as its three siblings). Cross-references, handoffs README naming rule, REPO-UPLOAD/Supervisor copies re-synced; pins refreshed (RPL 5c373819…, README 6083d2a9…). Old-named files deleted from masters and staging. Gates/queue/continuity clause unchanged.

## v0.43 — ALL remaining leagues commissioned (owner: "prepare them all, run through the night"); parallel research authorized (2026-08-02)
Owner directive: add every league's handoff so the researcher can run overnight. Read live export first: MLS = slate-scatter (29 clubs x1-3, NO tracked cohort — 2025 entirely absent), Scotland = Hibernian run-in 29 rows, Kosovo = Malisheva run-in 12 rows. Ruling registered: the three fixture-led leagues elevate to WHOLE-TOURNAMENT commissions (slice-mirroring impossible — no cohort); queue becomes ① RPL ② CZ1 ③ RUSCUP ④ MOLCUP ⑤ SCO1 (~1,100 rows) ⑥ KOS (~890) ⑦ MLS (~2,800, biggest, last). Parallel RESEARCH authorized by owner; AUDIT approvals unchanged: one card per return, queue order. Mechanics differ honestly: ①-④ keep the 2024-06-30 hard cutoff (we hold+verified 2024-26); ⑤-⑦ get appendix DO-NOT-RETURN lists (126 rows embedded) instead — no verified block exists to protect. All rosters/compositions/movements pinned from live RSSSF fetches (scot2022/23/24 — Queen's-death postponement quirk noted; kosovo2022/23/24/25 — awarded/abandoned rule incl. Gjilani-Ballkani crowd case + revoked-award NOTE-chain; usa2025 — 30-club map with dot-of-D.C. trap, expansion joins pinned 2021/22/23/25). New catalog strings prescribed: Scottish Premiership Relegation Round; Kosovo Relegation Playoffs. Deliberately NOT commissioned (fixture-led/one-off tier, owner's word would add): US Open Cup, Scottish Cup, UEFA qualifiers, Club Friendlies.

## v0.44 — Handoff cover doc created (owner request): START-HERE.md at repo root (2026-08-02)
Owner: "anything you want to tell him, create a handoff doc." Delivered `REPO-UPLOAD/START-HERE.md` (md5-pinned) — addressed auditor→researcher verbatim: job definition (7 workorders, queue order, MLS last, parallel allowed), delivery mechanics (ONE .txt per workorder into handoffs/ or chat; green-Commit-changes warning — "files left in your own session are undelivered"), unbendable rules (rows never tables; BP grammar; 90-min + advancement NOTEs; RSSSF-primary; NOTE-blocker never guess; ①-④ cutoff vs ⑤-⑦ appendix mechanics), the full audit drill he is aiming at (table reproduction zero-tolerance + span-diff keeps commissions open), the Rwanda failure named as the burn case, honest nightly scale (≈6,600 rows, partial-night safe if files complete). Queue coverage restated to owner: all 5 leagues + 2 cups commissioned; fixture-led tier (US Open Cup, Scottish Cup, UEFA quals, friendlies, Super Cups) un-commissioned until his word.

## v0.45 — National-cup gap closed (owner: "extra tourneys — why not in the workorders?"): 4 more orders staged, queue = 11 (2026-08-02)
Audit of extras: US Open Cup held=21 rows with 0 non-MLS ties (slice rule proven, cup family — commissioned) · Europe rows (UECL/UEL/UCL 16 rows) 100% tracked-club ties (Malisheva/Hibernian/Ballkani/Drita) → fixture-led BY DESIGN, no complete-tournament claim verifiable, stays out · Club Friendlies 4 + Russian Super Cup 1 → spectacle scatter, out. New: ⑧ US Open Cup (2021-cancelled NOTE mandatory — proves deliberate coverage; 2024 Next-Pro quirk clause; 21-row appendix) ⑨ Scottish Cup (4th-round entry slice, new catalog string) ⑩ Scottish League Cup (group stage INCLUDED, Euro-club byes as NOTEs) ⑪ Kosovo Cup (Kupa e Kosoves mapping; Albanian-cup collision warned). All = advancement-NOTE doctrine + bracket reproduction gates + span-diff. README/START-HERE synced to 11; program ≈7,300 rows. Europe/quals/friendlies/super-cups stay fixture-led — stated explicitly in README + told to owner with reasons.

## v0.47 — Owner decree 2026-08-03: major European leagues commissioned (EPL/SPA/ITA/GER/FRA); queue = 16 (2026-08-03)
Owner: "create workorders for all the major leagues." Export scan first: E0=44, SP1=42, I1=48, D1=38, F1=42 identities — union-of-membership check proves **every 2021-26 member club of all five leagues already exists on the roster** (incl. Watford/Norwich, Cadiz, Venezia, Greuther Furth, Troyes...) → §2 TEAM-rows-NOT-expected clause for all five (dup risk structurally dead). Pools pinned verbatim (Man City/Man United/Nott'm Forest; Ath Madrid/Vallecano; Ein Frankfurt/M'gladbach; Paris SG). Traps pinned: Bundesliga 18 clubs/306 rows (not 20/38); Ligue 1 shrink 20->18 in 2023-24 (380+380+306x3=1,678); German RSSSF dir = "duit". Zero held league rows for these → no appendices; total new ≈9,000 rows. Program: 16 workorders, ≈16,300 rows. Secondary majors (Portugal/Netherlands/Belgium/Turkey/Greece) NOT commissioned -- owner word adds them; noted to him explicitly. App location re-confirmed: /home/user/app-v3.5.2.html (md5 6bd76ae0..., 609,411 B) presented in viewer.

## v0.48 — Repo first population detected + integrity-verified: 15/18 files landed, 3 missing (2026-08-03)
Owner's drag partially landed (probe 2026-08-03, tree sha daed7ce5). LANDED at repo ROOT (not inside Supervisor/ — flat structure accepted, files reachable): all 16 workorders MINUS EPL = 15 files. Every landed file raw-fetched and md5-verified against pins — 15/15 BIT-PERFECT (CZ1 cdb5d725, FRA 79539690, GER 8b50d817, ITA a72da162, KOS 9892817e, KOSCUP b3c3b7a9, MLS c544a160, MOLCUP 764657c0, RPL 5c373819, RUSCUP 642ca12e, SCO1 62c474b0, SCOCUP 87e27e72, SCOLC 3214077f, SPA 30d6b835, USOC 327c71d8). MISSING 3: WORKORDER-EPL-2021-2026-5YSPAN.md (pin cb6e86e2), START-HERE.md (pin c42fb2bc), handoffs/README.md (pin f1c3f540). Owner told: drag those 3 — handoffs README must land inside a handoffs/ FOLDER (drag the folder itself). Researcher can already start on RPL (①) from repo root; the two conduct docs still owed to him. Verification drill logged in repo-check/ (tree-*.log + dl/ raw copies).

## v0.49 — Owner challenge ("Are you sure") + researcher session evidence: RPL data EXISTS but undelivered (2026-08-03)
Owner screenshots: (1) a Diff panel (+3858) from the researcher's OWN session showing `.work/rsssf-2021-22.txt` 247 ln, `README.md`, `WORKORDER-STATUS.md` 59 ln, `audit/validation-report.txt` 203 ln, `data/rpl/RPL-2021-22.csv`→`RPL-2025-26.csv` (245/245/245/241/241 ln ≈ 240 match rows + header each), `data/rpl/rpl_all_2021-2026.csv` 1213 ln. (2) repo main page at commit bb0b453. AUDITOR RE-PROBE at that moment: repo = bb0b453 (same commit as his screenshot), 19 files — 16 workorders + README + 2 stale Supervior files; **zero data/, audit/, .work/ content — researcher's files are NOT committed** (rule: left in his session = undelivered). Findings: researcher produced 5-season RPL material (~240 rows/season — scope plausibly correct) BUT (a) container format = CSV, not the commissioned BP-TEAM-PACK v2 .txt (fails format gate; not importable), (b) scope includes 2024-25 + 2025-26 which duplicate our verified block — those belong to the §5.1 control record, NOT the return pack (cutoff <2024-06-30 stands). Instruction issued to owner (paste-verbatim for researcher): deliver ① `RPL-2021-2026_BP-TEAM-PACK_v2.txt` (MATCH lines, 2021-22→2023-24 only, + playoffs, NOTEs, END) into handoffs/, ② the 5-season CSVs + validation report as control material in handoffs/control/ for the span-diff, ③ Commit changes so it actually lands. Stale Supervior/ files STILL on repo — researcher may have followed the retired 2021-24 order; deletion still pending with owner.

## v0.50 — RUSCUP return RECEIVED on branch + audited: 2 researcher defects, 1 auditor-owned erratum (2026-08-03)
Researcher pushed to branch `arena/019fc462-the-bettor-1` (NOT main — main still bb0b453): 5134d94 10:58:55Z = handoffs/RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt (49,083 B, 289 ln, md5 aef7f5ed402909b83565bf3f5ed42d59 pinned), 675f894 11:09:43Z = repo re-org (supervisor/workorders/ + handoffs/ + data/rpl CSVs + audit/ + tools/; stale 2021-24 order archived). Auditor drill: 16/16 workorder mirrors bit-identical (md5) · boundary PASS (max 2024-06-02) · 0 dupes internal + 0 overlap vs held 1,432 · shape 36+77+76=189 · **2021-22 36/36 row-exact vs RSSSF rus2022** (elite-group D1-tag phase counts proven 22/7/4/2/1) · 2022-23+2023-24 spot suite PASS incl. tricky metas (Dinamo-Krylya 01.03.23 VTB; Zenit-Spartak 17.04.24 Gazprom — RSSSF cupdet meta AFTER lineups) · 23 non-group draws: 14 NOTEd, 9 flagged→all benign (7 leg1s, 2 aggregate-decided, no pens) · 2 DEFECTS (researcher): missing TEAM|FC Ufa (3 rows; Ufa RPL 2021-22 per RSSSF table, folded 2022) + KAMAZ string (held="KAMAZ", he wrote "KamAZ Naberezhnye Chelny", 2 rows, dup risk) · 1 DEFECT (auditor-owned): compType line in ALL 5 cup workorders claimed held cup rows use domestic-league — FALSE (held=domestic-cup); loader keeps enum verbatim → ERRATUM-CUP-COMPTYPE-2026-08-03.md issued (cups=domestic-cup, SCOLC=league-cup; leagues unchanged; RUSCUP pack normalized at import-prep) · venue-slot round labels = workorder-prescribed, loader-safe, accepted. Audit card: AUDIT-RUSCUP-RETURN-2026-08-03.md. Import BLOCKED until the 2 name fixes land; seasons 2/3 full-machine diff = second pass before import. Owner upload path: branch via web UI branch selector.

## v0.51 — AUTHOR-AUDIT of every auditor-authored programme doc (owner decree: "audit all your requests for errors and correct them all now") (2026-08-03)
Method: built ground-truth table from live export (competition census + compType per comp + date spans), then machine-checked all 19 authored docs (16 workorders + START-HERE + handoffs README + erratum) + loader source (canonCompName = pass-through ✓ majors strings safe; canonCompType keeps enum verbatim ✓ why the bug matters). FOUND+corrected (all auditor-authored): FAMILY A — 5 cup orders prescribed domestic-league while held cup rows are domestic-cup (RUSCUP/MOLCUP/USOC/SCOCUP/KOSCUP; SCOLC→league-cup) · FAMILY B — playoff comps mis-typed: RPL (Russian Relegation Playoffs=other), CZ1 (Czech Relegation Playoffs=other; league incl. playoff-stage groups stays domestic-league per 561 held), MLS (MLS Cup Playoffs=other per 28 held), KOS (Kosovo Relegation Playoffs=other house convention) · FAMILY C — SCO1 "playoffs too" parenthetical removed. 11 files patched in place, new pins in ERRATA-2026-08-03.md (single merged errata file; cup-only erratum superseded/deleted). VERIFIED CLEAN: competition strings all match held/new-catalog (22-comp census) · cutoff/resume dates (RPL 2024-07-20, CZ1 2024-07-19) · MOLCUP gap fear DISPROVEN (RSSSF tsje2025 cp1250: MOL Cup chapter starts R3 2024-10-23 = exactly held start; no CZ1-club tie exists pre-held — cutoff mechanic clean) · CZ1 "no TEAM rows" correct (all 2021-26 members exist under held SHORT forms: Sparta Prague, Slovacko, Trinity→Zlin, Karvina, Artis Brno [Líšeň rename [*] noted]) · MLS 30/30 club strings resolve held (D.C. United dots, CF Montréal, St. Louis City SC) · SCO1 18/18 resolve · EPL/FRA quoted rosters resolve · RPL roster 19/19 resolve · KOS 6 "unresolvable" = the 6 DESIGNED new TEAM rows (Ulpiana/Feronikeli/Trepça'89/Fushë Kosova/Liria/Suhareka) ✓ · START-HERE/handoffs README = zero compType claims, clean. Owner re-drag needed: 11 corrected orders + ERRATA-2026-08-03.md (repo root + branch mirrors stale). Researcher building RPL league NOW must apply RPL playoff compType=other (else ~6 rows mis-typed per return; auditor would normalize at import-prep and log).

## v0.52 — RPL league return + corrected RUSCUP received (commit e22f3a4 13:53:42Z, squashed branch) and audited (2026-08-03)
Branch was force-rebased: single commit e22f3a4 now carries RUSCUP corrected + RPL league pack + CZ1 ledgers started. RPL pack (125,638 B, md5 c3a72b35e834cc030d62b3d160c79b25): 732 MATCH = 720 league (240×3) + 12 relegation playoffs (2 ties × 2 legs × 3 seasons; playoffs ran 2022/2023/2024 per pack — structure matches RSSSF) · 3 TEAM rows exactly right (FC Ufa, Yenisey Krasnoyarsk, SKA Khabarovsk) · compType errata applied perfectly (domestic-league ×720 / other ×12) · boundary 2024-06-01 ✓ · 0 dupes · 0 overlap · ALL names resolve · **TABLE REPRODUCTION 16/16 ×3 SEASONS EXACT vs RSSSF (48/48 club-seasons W-D-L GF-GA)** → VERDICT APPROVED, byte-ready, no normalization owed. Card: AUDIT-RPL-RETURN-2026-08-03.md. RUSCUP corrected (49,966 B, md5 d8e3ff9e741de6db9ab9295dc0aaae30): FC Ufa TEAM ✓ (22 TEAMs), domestic-cup ×189 self-applied ✓, gates re-run green — ONE micro-defect: "KAMAZ Naberezhnye Chelny" suffix (2 rows) must be exactly KAMAZ → one-word patch requested, import-gated. CZ1 ledgers (②) in progress on his side. Import queue for owner APP AFTER 3-click migration: RPL pack + RUSCUP pack (post-patch) → expected live rows 1,447 + 732 + 189 = 2,368.

## v0.53 — Southampton pack hold decoded + FIXED (auditor-authored defect) (2026-08-03)
Owner staged the pack live: app held it ("1 item needs a human check", only Discard offered). Code-proven mechanics: hold cards render NO Approve (line 3124: approve only for status 'ok') — held files must be fixed + re-dropped by design. Only two hold triggers exist, both tie-linkage (Z-003). Root cause: the playoff SF two legs were authored with PER-LEG tieIds (EFLCH-2026-PO-SF-SOU-MID / EFLCH-2026-PO-SF-MID-SOU) — my slip in the original authoring; loader's (competition,pair) grounder rightly flagged it. Fix applied: both legs now share EFLCH-2026-PO-SF-SOU-MID. NEW PIN: c7dbb89b4b3a00cc731780da25e14c73 (old pin 2d4b5ed0 retired; refs only in audit35* snapshots = history). Re-simulated both gate rules locally on fixed file → 0 holds (stages 'ok' with Approve). AET doctrine verified already present in pack NOTE (SF2 finished 2-1 AET; row = 90-min 1-1 ✓). Multi-file answer for owner: input HAS multiple-attribute (each file gated separately); drill stays ordered single-drops (JSON migration first, alone).

## v0.54 — CZ1 return audited (commit 8034d90 14:28:09Z): body EXACT, ONE omission (12 pro/rel rows); owner decree D13 registered (2026-08-03)
CZ1 pack (143,566 B, md5 c4b4664e123002794229c64e8a026c6c): 829 MATCH, all domestic-league Czech First League, span 2021-07-24→2024-05-31 ✓ boundary · 0 dupes · 0 overlap · names 100% held (0 TEAM rows as prescribed ✓). Gates: **regular-stage tables 16/16 ×3 EXACT** · Evropu brackets **18/18 exact** · CLP +1 row = REAL format (2023-24 only: Boleslav 3-1 Hradec 2024-05-31 — explains 829 vs 828 workorder estimate; HIS count correct, workorder aggregate estimate was coarse) · Titul+Záchranu 2021-22 30/30 exact, 2022-23/24 counts 15/15 ✓. OMISSION vs §1: 12 `Czech Relegation Playoffs` rows (compType `other` per errata) — RSSSF tsje2022/23/24 pro/rel ties: Teplice-Vlašim + Opava-Bohemians (2022), Příbram-Pardubice + Zlín-Vyškov (2023), Vyškov-Karviná + Budějovice-Táborsko (2024), 6 ties × 2 legs, dates/scores pinned in AUDIT-CZ1-RETURN card; Příbram/Vlašim roster-presence to re-verify at patch audit. KAMAZ one-word patch STILL OPEN (RUSCUP pack unchanged at d8e3). **D13 (owner decree):** after programme completes, owner will commission FULL audit of ALL auditor-produced team packs (Southampton etc.) for gaps/errors/omissions — registered; standing offer acknowledged. Also owner note: post-approve row count disappears because commit = save + app re-boot (commitMigration→STORE.save→boot() code-proven); data persists in localStorage; verification path = reopen app → Coverage/Files read counts (expect 1,447) + log 'migration-commit' entry.

## v0.55 — Migration VERIFIED from owner's live Coverage tab (2026-08-03)
Owner pasted post-migration Coverage view. Bucket reconciliation vs export census (expected sums proven): RPL 644 ✓ (=RPL 489+Cup 152+Playoffs 2+SuperCup 1) · MLS 85 ✓ (=36+28+21 USOC) · CZ1 632 ✓ (=561+8+MOL 63) · E0 15 ✓ (= Southampton pack exactly: SOU code E0 per pack NOTE; E1 9 = its 9 E1-coded opponents ✓) · D2 2 ✓ (Paderborn+Braunschweig friendlies) · P1 1 ✓ (Porto friendly) · Albanian 2 ✓ (Vllaznia-Malisheva Q1) · Danish 1 ✓ (Brondby) · SC0 42 ✓ (29 league+split rows + HIB Europe 11 + 2 friendlies) · remaining small buckets (FNL 12, KOS 24, CZ2 37, USL 16, USL1 2, LOI 3, undef 9) follow opponent-tie bucket pattern — no anomaly. 🟡 none-yet leagues all carry central requests = honest no-data doctrine working. COSMETIC (builder-forward, P6): code→display-name map incomplete — CZ1/D2/E0/E1/FNL/RPL/SC0/USL/USL1 render "undefined (N rows)" instead of league names; counts correct, label lookup missing. Migration state: export (1,432) + Southampton (15) = 1,447 expected — all decodable buckets reconcile exactly → migration approved. Next loads: RPL pack 732 + RUSCUP 189 → expect 2,368.

## v0.56 — IMPORT-READY-2026-08-03/ staged for owner (2026-08-03)
Folder (3 files): RPL pack byte-pure (c3a72b35, +732) · RUSCUP pack auditor-normalized (929d4aa5 — KAMAZ one-word fix + provenance NOTE inserted pre-END; delivered pin d8e3ff9e remains on branch) · README-IMPORT.txt (drop order + pins + expected 2,368 + held-card rule). Both re-gated post-folder: 0 unresolved names either file, END intact. KAMAZ fix now owner-side too; researcher's repo copy alignment = his next commit convenience, no longer blocking.

## v0.57 — Three returns audited & APPROVED (2026-08-03): MOLCUP full audit + CZ1 patch + RUSCUP KAMAZ v3
- Transport verified: owner's ERRATA upload on main, commit a98dffe (2026-08-03T19:54:48Z), md5 995a4abca13ae22fb62421670d08360b = auditor pin, byte-perfect (sits in Supervior/ typo folder; works, cosmetic note for repo tidy). Stale retired Supervior/Handoff/WORKORDER-RPL-2021-24-BACKFILL.md remains on main.
- ④ MOLCUP (commit 210a9aaa 17:02:56Z; md5 662fe5df, sha256 5023eb33 matches): 120 MATCH/31 TEAM/20 advancement NOTEs, all domestic-cup. Auditor re-gates: RSSSF R16→Final 45/45 (29 exact, 6 aet-90min, 1 disclosed postponement Plzen-Zlin 04-24, 3 commissioned no-FL exclusions, 6 Slovacko-ties manually line-verified after digit-name parser collision) · slice 41+41+38 ✓ · NOTE↔row wiring 20/20 · 0 dupes · 0 name/TEAM collisions · boundary ✓. R2/R3 bulk machine-diff vs worldfootball queued second-pass. Card AUDIT-MOLCUP-RETURN-2026-08-03.md (94a0f1fe). APPROVED.
- CZ1 patch (commit 9dc08ee 19:21:15Z; md5 29c3b6c9, sha256 55d9bd80 matches): 841 = 829 byte-untouched + 12 playoff rows 12/12 EXACT vs auditor RSSSF pins; compType other; no tieIds; no advancement NOTEs needed. CONDITION: import after MOLCUP (Vlasim/Pribram not held; MOLCUP TEAMs close it. Patch NOTE's "already-on-roster" phrase over-broad for those two — text-only). Card AUDIT-CZ1-PATCH-2026-08-03.md (eb1b1417). APPROVED with order condition.
- RUSCUP v3 (same commit; md5 91bce98d, sha256 c2658b49 matches): MATCH-row delta vs approved d8e3ff9e = exactly the 2 KAMAZ strings; 189/22/END ✓. Auditor hand-normalized copy retired. Addendum on AUDIT-RUSCUP-RETURN card (cd533d72). APPROVED.
- Researcher self-reported gate counts (120/120, 162/162) registered but never adopted; auditor gates above are the record.

## v0.58 — IMPORT-READY-2026-08-03 re-staged (4 packs, order RPL→RUSCUP→MOLCUP→CZ1) (2026-08-03)
Pins: RPL c3a72b35 · RUSCUP 91bce98d · MOLCUP 662fe5df · CZ1 29c3b6c9. Expected Coverage: 2,368 → 2,488 → 3,329 (TEAM declarations do not move the counter per RPL/RUSCUP precedent; MOLCUP carries 31). README-IMPORT.md5 pins + held-card stop rule + order rationale (Vlasim/Pribram dependency) written to IMPORT-READY-2026-08-03/README-IMPORT.txt. Owner action pending: drop in order, report Coverage. Researcher: ⑤ EPL in progress per relay; owes nothing else outstanding on ①-④.

## v0.59 — SECOND-PASS wave 1 complete (2026-08-03 evening): RUSCUP 153/153 · MOLCUP R2/R3 129/129
- RUSCUP 2022-23+2023-24 full machine bracket diff vs RSSSF (local rus2023/24.txt): 2023-24 76/76 EXACT; 2022-23 74 exact + 3 one-day conflicts ALL adjudicated to pack (RSSSF compact headers misprint vs its own Details meta 04.04/05.04/03.05 — pack correct). Script ruscup_bulk_diff.py retained.
- MOLCUP R2/R3 wiki bulk diff (wf Cloudflare-blocked from sandbox): 129 ties — 59 EXACT, 5 AET-OK, 13 alias/pens-adjudicated-present, 47 excluded-OK (season-aware FL sets), 0 missing/0 conflicts. 90-min digit-level for 20 aet/pens ties = only open residual (needs wf). Script molcup_wiki_diff.py. Card AUDIT-SECONDPASS-2026-08-03.md.
- Request queued for researcher (via owner): fetch worldfootball MOL Cup R2/R3 + match-report pages (2021-22..2023-24), drop raw HTML on branch — closes the last 90-min residual. Also standing: 2026 Russian Super Cup existence check.
- Repo-watch: branch HEAD d76adbdc (20:30:43Z) = EPL ledgers WIP, honest PENDING flags; nothing new in handoffs/; main unchanged a98dffe.

## v0.60 — SECOND-PASS wave 2 complete (2026-08-03 night): CZ1 90/90 · Russia span-diff CLOSED · 16-row HELD-DATA date defect proven at RSSSF
- CZ1 group phases (Titul + Zachranu) 2022-23/2023-24/2024-25 bulk diff vs RSSSF tsje2023/24/25 round listings: 90/90 EXACT (script cz1_groups_diff.py). CZ1 return now machine-verified end-to-end (main phase + groups 90/90 + Evropu 18/18 + playoff patch 12/12).
- Russia span-diff: held RPL 2024-25 + 2025-26 (480 rows) vs researcher control CSVs (repo-check/RPL-*-control.csv): 464 exact (all scores byte-identical across both full seasons) + exactly 16 date conflicts, ALL adjudicated AGAINST the held data at fresh RSSSF primaries (rus2025.txt L745 `Round 30 [May 24]`; rus2026.txt L740 `Round 30 [May 17]`).
- **DEFECT (old builder seed, NOT the 4 new packs): 16 held R30 rows misdated** — 2024-25 octet dated 2025-05-19 should be 2025-05-24 (−5d); 2025-26 octet dated 2026-05-11 should be 2026-05-17 (−6d). Scores/sides 16/16 correct; dates only. 5 lookalike rows on those same dates CLEARED (genuine R29 Monday games: rus2025 L741 [May 19] Loko-CSKA 2-2; rus2026 L729 [May 11] Spartak-Rubin, PariNN-CSKA, Akron-Rostov, DinamoM-Krasnodar).
- Collision clearance: RPL pack spans 2021-07-23→2024-06-01 (732 = 720 league + 12 playoff) → zero overlap; held store has 0 rows on the true dates → 4-pack import stays CLEARED, no dup risk. Repair must NOT be a correction import (date-keyed dedup would duplicate) → in-place date edit of 16 rows or MUTE+re-add; owner/builder decision pending; auditor recommends in-place edit.
- Second-pass card extended: AUDIT-SECONDPASS-2026-08-03.md sections 4-6. Open after wave 2: 16-row repair decision · 2026 Russian Super Cup existence check · MOLCUP wf 90-min residual (20 ties, blocked fetcher — request with researcher).

## v0.61 — SECOND-PASS wave 3 (2026-08-03 night): RPL forward edge 9/9 clean · Super Cup 2026 EXISTS+missing -> auditor mini-pack · EPL primaries pre-staged
- rus2027 fetched (rsssf-ref/, 94.5KB UTF-16). Held 2026-27 RPL: R1 8/8 EXACT vs RSSSF round block; R2 Akron 1-2 Rubin (held 2026-08-01) confirmed via en.wiki results grid (match_AKR_RUB=1-2), date inside official window Jul31-Aug3 (RSSSF page not yet R2-updated). Old-seed defect stays confined to the 16 R30 rows of section 5. Season context: Fakel + Rodina promoted [P]; Pari NN + Sochi out; Akron home = Krylja Sovetov stadium Samara.
- SUPER CUP 2026: EXISTS - Zenit 1-1 Spartak [pen 4-2], 18.07.26 Nizhny Novgorod Stadium, recorded at END of rus2026 file (#sup, L4883-4900; rus2027 page carries NO super-cup section - placement quirk). MISSING from held store (only 2025-07-12 row present). Auditor mini-pack authored: IMPORT-READY-SUPERCUP-2026/SUPERCUP-2026_BP-TEAM-PACK_v1.txt md5 1628348112fc3181dec04b5ce868f4ce (90-min 1-1 + mandatory pens advancement NOTE + SOURCE; 0 TEAM, strings byte-resolve, 0 overlap, order-free after 4-pack import; expected Coverage 3,329 -> 3,330). README-SUPERCUP.txt md5 29b16fc8129cbbd5f5e94b98bed25e87. Weekly central-request item CLOSED.
- EPL pre-position: rsssf-ref/eng2022-eng2025 full pages fetched (48-50 Round blocks each; eng2025+eng2026 arrived UTF-8, 2022-24 needed plain copy after UTF-16 probe). eng2026 page SKELETAL (8 blocks, 24KB) - 2025-26 EPL segment diff may need re-fetch or wiki second index. Researcher branch unchanged d76adbdc; main a98dffe.

## v0.62 — EPL baselines 4x LOCKED (380/380, tables 80/80 reproduced) · R30 repair spec shipped (md5 504403c1) · molcup.cz official DB probed (reachable, legacy seasons widget-locked -> residual stays with researcher)
- epl_baseline.py written + replayed from file: audit-baseline/epl-2021-22..2024-25.json all PASS (380 matches each, 0 dupes, printed tables 20/20 W-D-L-GF-GA each season). Known-only irregularities: 2023-24 Everton -8/Forest -4 deductions + 2023-12-16 Bournemouth-Luton abandonment (Lockyer) excluded, replay counted. ⑤ pack audit now machine-diff ready. Parser gotcha archived: Wolverhampton column overflow.
- REPAIR-SPEC-R30-2026-08-03.md: 16 rows enumerated with exact homeId/awayId/score + wrong->correct dates + both repair routes + owner self-check; decision still owner/builder.
- MOLCUP bonus probe: molcup.cz official results DB reachable (158 current rows fully structured incl. PEN/pp. markers) but 2021-24 slices locked behind dead JS widget (data.esportsmedia.cz import.js 404); fotbal.cz 403. Residual (20 aet/pens 90-min digits) assignment UNCHANGED (researcher, wf) + option note: molcup.cz unblocked from his side.
- eng2026 (EPL 2025-26) RSSSF page still skeletal (8 blocks): 25/26 EPL segment needs re-fetch later or wiki second index.

## v0.63 — Majors pre-positioned: 16/16 baselines LOCKED (league_baseline.py) · workorder map recovered (16 WOs: 5 left = FRA/GER/ITA/KOS/KOSCUP + MLS/SCO1/SCOCUP/SCOLC/SPA/USOC) · export census proves majors = pure adds
- Branch tree pulled: supervisor/workorders/ = RPL,CZ1,RUSCUP,MOLCUP,EPL,FRA,GER,ITA,KOS,KOSCUP,MLS,SCO1,SCOCUP,SCOLC,SPA,USOC (+archived RPL-01). WORKORDER-STATUS.md mirrored to repo-check/. ⑤ EPL queued next; majors WOs = 2021-24 backfill segments.
- Export census: ZERO held rows for EPL/LaLiga/SerieA/Bundesliga/Ligue1 -> majors imports are pure adds, no span-diffs, no dup risk.
- RSSSF naming quirks logged: span (not spa), ital (not ita), duit, fran; span2026 = 404; ital/duit/fran 2026 skeletal. Mixed encodings smart-decoded.
- league_baseline.py: 16/16 PASS -> audit-baseline/{laliga,seriea,bundesliga,ligue1}-*.json (4x380 La Liga / 4x380 Serie A / 4x306 Bundesliga / 380+380+306+306 Ligue 1, tables reproduced, dupes 0). majors-aliases.json frozen (99 mappings). All anomalies = real events (Granada fan abd, Ndicka, Bove, Drewes lighter awarded game, Marseille crowd cases with -1s, Juventus -10). Auditor baseline stock = 20 seasons / 7,256 matches.
- Parsers idiom hardened this turn: longest-alias-suffix matcher (multi-word teams safe), wrapped-note tails re-attributed, awd/abd grammars, digit-starting club names, relegation dash separators, double-printed tables.

## v0.64 — OWNER DECREE D14 (2026-08-04): complete-pack strategy; staged 4+1 packs PAUSED; json-load/migration semantics code-proven
Owner: researcher now produces COMPLETE season packs (full spans, not 2021-24 backfills) for cross-check against held old data; staged IMPORT-READY-2026-08-03 (4 packs) + IMPORT-READY-SUPERCUP-2026 (1 pack) imports are PAUSED until complete packs land + audit. Owner loaded the 2026-08-02 export .json.
Code-proven answers (app-v3.5.2.html): (1) migration load = FULL STORE REPLACE incl. teams/venues/sources/mutes/log (commitMigration L3334-3360: 'Store replaced by migration: N matches · N teams'); (2) NO in-app clear/reset button (only factory empty() template L385; store key 'pitch-rating-v3.store' L358 → reset = browser site-data clear); (3) pack ingest = add-if-new ONLY: matches dedupe by date+home+away+competition fingerprint ('Skipped duplicate match', L999-1003), nothing overwritten; TEAM rows merge-enrich; MUTE marks existing row muted (excluded but preserved). → Only override mechanism = migration JSON (full atomic replace, any desired final store can be assembled offline and loaded). Old-league vs complete-new-league conflict rule: identical rows skip safe; ANY changed row (e.g. the 16 misdated R30 rows) would DOUBLE → must be MUTEd or removed before/with a complete-pack import of the same league. Majors (EPL/SPA/ITA/GER/FRA) = zero held rows = pure adds, always safe.

## v0.64a — D14 CLARIFIED BY OWNER (2026-08-04): NO MIXING, ABSOLUTE
Owner, verbatim intent: "I don't want data mixed with both research; unless we get full research of russian league games from the researcher and then we audit, I will not go ahead with import." => Zero cohabitation of builder-seed rows and researcher rows for the same league/scope. ALL staged imports (IMPORT-READY-2026-08-03 4 packs + IMPORT-READY-SUPERCUP-2026 1 pack) remain FROZEN; Russia arrives ONLY as a researcher-complete delivery + audit; per D14 the same rule covers every scope that has old-seed rows (CZ1, MOLCUP, Scottish, MLS, USOC, Kosovo, small buckets). Majors (EPL/SPA/ITA/GER/FRA) remain pure adds in principle. Audited backfill packs RETAINED as independent cross-check references (second transcription for adjudication when the complete packs land), not as import candidates. REPAIR-SPEC-R30 route A/B superseded by route C (replacement at final JSON assembly). App store meanwhile = untouched 2026-08-02 snapshot (1,432); nothing imported.

## v0.65 — Builder workorder WO-SCOPE-CLEAR-01 authored + issued (2026-08-04)
Per owner request ("we need a UI control surface for old data clearing per country pack so it can be replaced without new coding — prepare the workorder for the builder"): WORKORDER-SCOPE-CLEAR-UI-01.md in folder BUILDER-WO-SCOPE-CLEAR/. Design: Data-tab panel 'Country packs — clear & replace'; scopes derived 100% from live store (G10 anti-hardcode grep gate); MUTE (soft, reversible) + PURGE (hard, gated on automatic pre-purge backup .json download; undo = existing migration loader, G6-proven); cross-border guard (never kill a non-scope competition row); orphan-rule identity cleanup with preview keep-list; atomic mutation + log + pre/post snapshots; sources append-only kept. UAT pinned to live census: Russia 644 (489/152/2/1, 26 clubs), Czechia 632 (561/63/8, 45 clubs), purge -> 788, RPL-pack-replace -> 1,520, restore -> 1,432. Target build v3.6.0; v3.5.2 stays sealed (6bd76ae0). Owner UAT runs G1-G12; auditor byte-diffs shared code paths on delivery. Full country census computed live from export (16 scopes, 1,432 rows all resolvable).

## v0.65a — WO-SCOPE-CLEAR-01 amended: league-level selection added (owner ask "per league selected")
Hierarchy now country -> individual competitions, BOTH selectable clear scopes (e.g. purge MOL Cup's 63 rows alone, Czech First League untouched); one shared selection function {country, competition|null}; new gate G2-L pins it (1,432-63=1,369). Amended file pin (verified by md5sum): a7b89f22355a5d831e95aeff8b37d0fa.

## v0.66 — app v3.6.0 AUDITED: byte-verified edf52d78 (CF transit injection stripped) · APPROVED FOR UAT + v3.6.1 delta (G2-L league-level, 400-row cap)
- Transport catch: attached file = c5183f75/631,654B ≠ builder claim; forensics proved EXACTLY one appended line 11074 (1,290B Cloudflare __CF$cv$params + beacon.min.js injection BY THE PROXY, not the builder); strip -> 630,363B / edf52d78b2fa1690721aa3a72018b634 = builder pin EXACT. md5-on-arrival policy caught it; clean UAT file staged at APP-V3.6.0/app-v3.6.0.html (+ README-UAT.txt 82272fb9).
- v3.5.2 seal intact (6bd76ae0). Diff = version bump + 2x G4-sanctioned `if(m.muted)return` Coverage one-liners + additive module/UI/handler/CSS blocks; ingest dedupe, commitMigration, hold-rule, migration-replace BYTE-IDENTICAL. G10 zero-literals clean; no-network clean; engine faithful (one selection fn, orphan rule + cross-border keep-list, atomic+hash snapshots, sources kept default, double backup gate, no-op honesty, pure-adds toast).
- RETURN ITEMS (v3.6.1): R1 G2-L league-level selection absent (selection() is country-only; amendment v0.65a post-dated build start) — non-blocking for the whole-country no-mix endgame; R2 preview list slice(0,400) caps Russia preview (counts exact). Card: AUDIT-APP-V3.6.0-2026-08-04.md.
- Builder self-reported 33/33 harness registered-not-adopted; functional acceptance = owner UAT G1->G12 (G1-G6 store-safe). Next: owner UAT report -> verify vs pinned 788/1432/1520.

## v0.66a — WO v3.6.1 delta authored: D1 league-level clear (R1/G2-L) + D2 full preview list (R2/400-cap) + D3 ALPHABETICAL listings (owner UX, supersedes count-sort)
Owner clarified R-team ask: alphabetical ordering wanted for easy type-jump selection. D3 covers country list, competition rows, removed/kept club lists (A-Z by display name; counts still shown; gate G13 with exact expected order e.g. Russian Cup · Russian Premier League · Russian Relegation Playoffs · Russian Super Cup). Builder delta ships v3.6.1; auditor byte-diffs vs edf52d78.

## v0.67 — app v3.6.1 AUDITED + OWNER-OUTBOX system live (communication rule v1.1)
- v3.6.1 arrived base64-wrapped (package 9): decoded md5 762a62846eb5c9531627e1d67be365a8 = MANIFEST pin, 630,593B, ZERO transit junk (b64 armour works). Diff vs verified v3.6.0 = exactly 2 edits: version bump + preview slice(0,400) removed (FULL row list = R2 delivered, correct). D1 (league-level) + D3 (alphabetical) ABSENT — still owed (v3.6.2 expected). APPROVED FOR UAT; staged APP-V3.6.1/ (README-UAT rewritten for 3.6.1).
- Owner decree -> COMMUNICATION-RULES v1.1 (outbox increment rule): all outgoing deliverables in OWNER-OUTBOX/ with numbered filenames, new version = new number, INDEX.txt carries destination+purpose+md5+status; "the same file" banned from my vocabulary. Populated: 01-WORKORDER-SCOPE-CLEAR-FOR-BUILDER-v2.md (4d52a592, carries D1+D3) + 02-SPEC-FOR-RESEARCHER-RUSSIA-COMPLETE-v1.md (0613624f).
- Builder note registered: SCOPE-CLEAR.b64.txt + ZONES-v3.6.1.b64.txt received (his internal docs; unread beyond md5 cross-check vs his MANIFEST: SCOPE-CLEAR d486f96d matches manifest; his ZONES copy is his, mine remains canonical).

## v0.68 — app v3.6.2 AUDITED: D1 league-level + D3 alphabetical DELIVERED · harness 32/32 on app's own module · APPROVED FOR UAT (supersedes v3.6.1 UAT)
- PACKAGE 10 arrived b64-armoured, zero transit junk: app md5 c7f955d4aacdeaaca9a44e4314f2b14e / 634,591B = MANIFEST exact; ZONES fd559974…; DELTA doc 80ae2141… — all three pins exact.
- Diff vs pinned v3.6.1 (762a6284): 74 out / 121 in, 100% confined to version bump + scope CSS tree + PR.scope module (L2804-3000) + panel handlers. Ingest dedupe L1016 / migration-replace L3727 / LS_KEY / hold logic / both G4 lines (L1223,L1283) BYTE-IDENTICAL. G10 module-range grep clean; 0 network calls; slice(0,400) count 0 (D2 intact).
- BEHAVIOURAL HARNESS (app-v362-audit/harness-v362.js): exact module slice executed vs live 1,432-row export — 32/32 PASS: 18 scopes Σ=1,432 (earlier "16" memo corrected: tiny scopes = Euro away legs/friendlies, Canada 4 = MLS Canada home games; anchors Russia 644/Czech 632/US 81/SCO 34/KOS 19 all match v3.6.0 census); G13 Russia comps A-Z exact (152/489/2/1); G2 string-compat 644->788; G2-L MOL Cup 63->1,369 with zero cross-bleed; MUTE/UNMUTE 644 & 63 round-trips with country+competition+preHash log fields; PURGE MOL Cup removed 63 + 23 orphan Czech cup clubs (zero remaining refs across 5 collections — keep-list proven), sources kept, noop honesty purged-again; PURGE Russia rehearsal -> 788; unknown-scope guard. Per-scope backup keying (country||competition) code-proven: country backup ≠ league purge enabler.
- Version deviation resolved: WO labelled delta "v3.6.1" but v3.6.1 was sealed with D2; builder correctly shipped v3.6.2 (policy: upward, never reuse). Registered-not-adopted: builder suites smoke 49/49 · scope 43/43 · parity 7/7 · legacy 156/156.
- Staged APP-V3.6.2/ (app + rewritten README-UAT: 18-scopes note, G8 league-level MOL Cup gate, G10 A-Z spot-check, per-scope backup warning). OUTBOX file 01 status -> DELIVERED (this build is the response). Researcher branch probe: HEAD 1da8826e205a (2026-08-04T00:50:29Z) RPL full-span ledger (32 tables + venues + wiki 2nd-idx 240/240 x2 seasons + RFU chain) — complete-Russia build visibly started; main a98dffee709f unchanged. Owner owes: UAT G1->G12 on v3.6.2 + send outbox file 02 to researcher.

## v0.69 — DECREE-2026-08-04 override packs WAVE-1 audit (2026-08-04 night): EPL ADOPT · RPL/RUSCUP/CZ1 adopt-pending-Wave2 · MOLCUP NO-GO (not pushed) · gaps F1/F2 · baseline errata owned
- Transport: remote tip 5722cb61 (API rate-limited -> git ls-remote); 4/4 override pack sha256 = researcher claims EXACT via git blobs (raw CDN 404-lagged on moved branch). MOLCUP full-span commit 5d75e56 ABSENT (his token died at push); remote MOLCUP = old 120-row 662fe5df = frozen approved byte-exact.
- EPL 1,900 ADOPT: 1,520/1,520 rows score/side-exact vs baselines 2021-24; 43 DATE-only rows ALL adjudicated in pack's favour (RSSSF misprints proven: [Dec 2] impossible for Everton 3-0 Newcastle/Spurs 1-2 West Ham = 2023-12-07 Thursday Amazon; Newcastle 0-2 West Ham 2024-11-25 = football-data CSV byte check; final-round Sundays vs my baseline round-window Mondays); 2025-26 table 20/20 vs eng2026 (page matured; Arsenal 85 reproduced); boundary 2026-27 zero rows correct (starts 2026-08-21); zero dupes; MD detail 1,900/1,900.
- RPL 1,220: tables 80/80 profile-exact vs rus2022..2026; playoffs 20 legs/5 seasons existence+2 seasons row-exact (Akron 0-1 Rotor agg convention settled). GAPS: F1 zero 2026-27 rows vs decree-through-today (store's 9 verified rows would be erased at purge); F2 Super Cups 2025+2026 absent from both Russia packs (spec outbox-02). Researcher addendum required pre-clear.
- RUSCUP 341 / CZ1 1,401: RUSCUP = old 189 VERBATIM superset (continuity 189/189; surface = +152 rows). CZ1 phase tables 140/140 exact (REG 80 + TITUL 30 + ZACHRANU 30; 2025-26 Zachranu scrambled-print closed 6/6 manually; Karviná fixing-demotion NB confirms pack karvina_incident); pro/rel legs 20/20 row-exact (90-min doctrine on Dukla pens); Artis-on-league-rows 0; Czech 2026-27 zero rows CORRECT (starts Aug 7). Czechia clearing still NO-GO: MOLCUP full-span not on branch.
- AUDITOR ERRATA owned: my epl baselines carry 43 rows with round-window dates (dates only; tables/goals/pins unaffected); logged in AUDIT-CARD-OVERRIDE-2026-08-04, never silent-rewrite. Card: AUDIT-OVERRIDE-2026-08-04/AUDIT-CARD-OVERRIDE-2026-08-04.md. Owner owes: reconnect researcher GitHub; request RPL-2026-27+SuperCup addendum; UAT v3.6.2; decide EPL import now vs batch.

## v0.70 — MOLCUP FULL-SPAN ADOPTED (2026-08-04 close-out): Czechia = first clearing-eligible country · audit card addendum written
- Transport closed: branch tip 84d9471d2c31835eb2370f15e567e1cf568690d2; pack sha256 50ead762d80070dce6cbf468dedd26eb4d4e3706dd264801194af49385791137 = claim EXACT via git blob. Structure 202 MATCH / 43 TEAM / 53 NOTE / 23 SOURCE; continuity 120/120 verbatim.
- All gates PASS and shown: finals 5/5 (RSSSF tsje2026 final print ruled WRONG — stale finalist; pack Jablonec 1-3 Karvina proven by wiki box); tsje2025 season diff clean (Opava-Zlin correctly sliced); tsje2026 25/31 + 5 own-alias closes; R2 2025-26 10/10; R2 2024-25 11/11 after final parser fix (my artifacts only, pack bytes verified); 13 aet ties at 90-min doctrine.
- VERDICT: ADOPT. Czechia runbook armed: backup -> PURGE 632->800 -> import CZ1 1,401 + MOLCUP 202 -> expected 2,403. STILL BLOCKED on owner UAT v3.6.2 (hard prerequisite) — then Czechia executes.
- Clearing matrix: Czechia GREEN (pending UAT) · England GREEN (eligible now, owner decides import-now vs batch) · Russia RED (F1+F2; outbox file 03 addendum REQ-2/REQ-3 with owner to send) · SCO/KOS/US untouched. Researcher moved to FRA full-span.
- Audit card addendum appended: AUDIT-OVERRIDE-2026-08-04/AUDIT-CARD-OVERRIDE-2026-08-04.md (earlier NO-GO section kept verbatim as record).

## v0.71 — WORKSPACE REORGANISED (owner request 2026-08-04): root ~170 entries -> 10 · zero content change, all pins re-verified post-move
- Housekeeping only: files MOVED, none edited/renamed/deleted. Old docs quoting old absolute paths remain valid history — PATH-MAP-2026-08-04.md at root is the translator (old -> new).
- Root now: ZONES.md · COMMUNICATION-RULES-v1.md · OWNER-OUTBOX/ · APP-V3.6.2/ (UAT target, untouched) · AUDITS/ (override audit + baselines + app-version audits + country workdirs + tools + reports) · DATA-PACKS/ (frozen D14 staging + returns) · APP-HISTORY/ (sealed versions + old scripts) · WORKORDERS/ (+ COMMS/) · REFERENCE/ (rsssf-ref, repo-check, store snapshot, uploads, REPO-UPLOAD) · PATH-MAP file.
- POST-MOVE PIN RE-VERIFICATION 14/14 EXACT: app v3.6.2 c7f955d4aacdeaaca9a44e4314f2b14e · v3.5.2 6bd76ae025fc6eee68e3186ac52ac5ec · v3.6.0 edf52d78b2fa1690721aa3a72018b634 · v3.6.1 762a62846eb5c9531627e1d67be365a8 · audit card b45e9fed006f59f861c20eb7a64399b1 (now AUDITS/AUDIT-OVERRIDE-2026-08-04/) · INDEX dbf95d60203a84f023f85f55fef3aadf · outbox 02 0613624f3a513f80a5c332ed24562b5f · outbox 03 e3262ec1497ee8cfe835c8e6565ec5db · pack sha256s EPL 707dd830… RPL d71ed24f… RUSCUP f89501cf… CZ1 cbd5710b… MOLCUP 50ead762… — all byte-identical.
- Working memory updated: all "Relevant files" paths remapped; e.g. override audit now AUDITS/AUDIT-OVERRIDE-2026-08-04/, frozen staging now DATA-PACKS/IMPORT-READY-2026-08-03/, store snapshot now REFERENCE/pitch-rating-full-data-2026-08-02.json.

## v0.72 — OWNER-OUTBOX re-structured per owner decree: contained numbered send-folders DELIVER-nn (COMMUNICATION-RULES v1.2)
- Old flat files -> folders, zero edits: DELIVER-01/01-WORKORDER-SCOPE-CLEAR-FOR-BUILDER-v2.md (DELIVERED, md5 4d52a59264155b5ccbe6c2cdd3447e7e) · DELIVER-02/02-SPEC-FOR-RESEARCHER-RUSSIA-COMPLETE-v1.md (SEND NOW, 0613624f3a513f80a5c332ed24562b5f) · DELIVER-03/03-ADDENDUM-FOR-RESEARCHER-RUSSIA-GAPS-v1.md (SEND NOW, e3262ec1497ee8cfe835c8e6565ec5db). All three md5 re-verified IDENTICAL after move.
- INDEX.txt rewritten for folder layout (table + "next number up: DELIVER-04" + corrected pointers to DATA-PACKS/ and WORKORDERS/ paths from v0.71 reorg) — new INDEX md5 below. COMMUNICATION-RULES appended as v1.2; PATH-MAP amended.
- Outbox rule now: correction = next folder, never edit an old DELIVER-nn; cite DELIVER-nn + filename, never "the same file".

## v0.73 — RUS-ADDENDUM-2026 ADOPTED (18 rows): F1+F2 closed, Russia red->amber · auditor erratum owned (playoff naming)
- Arrival protocol: tip 8e867a8aff7b441d6aa3a121b03b2a31a6dc2785; sha256 30576ac4894930b359db19193f08f05cd3f399ecd7d97f9975184ac02386dcea = claim EXACT via git blob. Pinned AUDITS/AUDIT-OVERRIDE-2026-08-04/RUS-ADDENDUM-2026.txt (+ REGISTERED-* his validation, registered-not-adopted).
- My gates, all run on-machine: R1 vs my rus2027 8/8 EXACT (attendances sum 102,232 = printed); R2 pairings vs RSSSF fixtures 8/8; R1+R2 vs wiki FBR (upd 2026-08-02) 16/16 EXACT both-direction; Orenburg-Zenit date 2026-08-02 proven via hat-trick cite; Super Cups 2025+2026 EXACT vs my rus2025/rus2026 #sup incl. 90-min doctrine NOTE; 0 dupes; TEAM grammar = pinned shape; store-dedupe fingerprint collision impossible at purge-first import.
- Errata owned: my SPEC-02 playoff enumeration 'Shinnik-Akron 2026' wrong (actual Akron-Rotor/Ural-DynMh); pack's 20 legs stand. 
- Clearing matrix: Russia 🟡 AMBER (packs complete+primary-verified; pre-clear = MY Wave-2: RPL grid dates, playoffs 3 seasons, RUSCUP +152) · Czechia 🟢 (UAT-blocked) · England 🟢 (owner decision) · SCO/KOS/US untouched. Rolling-append: R3 drop expected post-2026-08-08, same protocol.
- Audit card ADDENDUM-2 appended (md5 below); premierliga match-centre CAPTCHA-blocked to me - R2 per-day splits beyond the proven 08-02 carry his heritage provenance (registered).

## v0.74 — WAVE-2 COMPLETE (2026-08-04 evening): all row-diffs green, data programme AUDITOR-CLOSED · Russia + Czechia fully verified, both 🟢 pending owner UAT
- RPL: round-grid gate 1,200/1,200 EXACT (rpl_grid_gate.py; fixed my 0022 year bug + Dinamo alias + round-header dates); playoff legs 12/12 -> 20/20 total.
- RUSCUP: 152/152 new-surface rows EXACT (ruscup_w2_diff.py; my 'ATT'-in-TOLYATTI filter bug + Krylja S. alias + two-leg header-date clearing fixed); RSSSF-only remainder = regions-path rounds (out of scope, name-traps proven: Zenit Penza [D4] etc.) + #cupdet reprints (my artifact).
- CZ1: Evropu 31/31 EXACT incl. 2023-24 CLP. Exception R-EX-1 registered: two 2025-26 SF leg-2s carry after-ET official scores (documented, 2 rows, source-faithful; future packs keep 90-min+NOTE).
- FINAL DATA VERDICTS: RPL 1,220 ADOPTED · RUSCUP 341 ADOPTED · CZ1 1,401 ADOPTED · MOLCUP 202 ADOPTED · RUS-ADDENDUM 18 ADOPTED · EPL 1,900 ADOPTED (wave-1).
- Clearing matrix: Russia 🟢 (purge 644->788, import 1,579) · Czechia 🟢 (purge 632->800, import 1,603) · England 🟢 (1,900 pure adds, owner chose timing) · SCO/KOS/US untouched. SOLE REMAINING GATE = owner UAT of APP-V3.6.2 (G1->G12) -> then clearing runbook. Audit card ADDENDUM-3 appended.

## v0.75 — OWNER START-HERE issued: programme closed audit-side, execution hand-off
- START-HERE-2026-08-04.md at root: Phase 0 open app (expect 1,432) -> Phase 1 safety rehearsal (11 plain steps, undo proof = restore to EXACTLY 1,432) -> Phase 2 Czechia (backup, purge 632->800, import CZ1-2021-2026.txt +1,401 + MOLCUP-FULLSPAN.txt +202 = 2,403, 0 skips) -> Phase 3 Russia (purge 644, import RPL+RUSCUP+ADDENDUM = 3,338) -> Phase 4 England (+1,900 pure adds = 5,238). Per-phase totals check against auditor pins; backup-first rule stated (purge disabled until backup downloads; rollback = app-v3.5.2 sealed).
- Import sources: the six ADOPTED packs in AUDITS/AUDIT-OVERRIDE-2026-08-04/ (sha-pinned in audit card). Nothing else may be imported (D14 frozen staging stays frozen).

## v0.76 — INCIDENT-CLOSED (2026-08-04 17:2x UTC): owner report "country pack disappeared on all browsers" = OLD APP OPENED, no data loss
- Owner screenshot: browser URL bar reads app_v3.5.2.html, header badge v3.5.2. Coverage tab top shows seeded "Albanian Superliga - undefined (2 rows) LOADED" + D12 request rows (B1, D1 REQUESTED) = normal baseline-seed content, top of an alphabetical league list.
- Grep-verified on sealed files: v3.5.2 (md5 6bd76ae025fc6eee68e3186ac52ac5ec) contains ZERO hits for PR.scope / purgeScope / country-scope clear control; Scope Clear Control (WO-SCOPE-CLEAR-01) exists only v3.6.0+ (v3.6.2 md5 c7f955d4aacdeaaca9a44e4314f2b14e, PR.scope module line 2787, 12+ refs). VERDICT: nothing disappeared - the country-scope (per-country clear/pack) UI simply does not exist in v3.5.2, in any browser.
- Data safety: both versions share localStorage key 'pitch-rating-v3.store' (v3.5.2 L358 / v3.6.2 L378); seed build runs ONLY when store missing/empty (boot(), L10692 v3.5.2 / L11065 v3.6.2) => opening v3.5.2 does NOT erase an existing store. Store is per-browser (no cross-browser sync) - UAT store lives only in the browser where UAT ran.
- Owner instructed: open app_v3.6.2.html in the UAT browser; keep v3.5.2 as sealed emergency rollback only; report store census number before any purge. Option A/B question (1,447 vs 1,432 baseline) still OPEN.
- Cosmetic defect registered for builder (non-blocking): Coverage row renders country as 'undefined' for league entries without country label.

## v0.77 — INCIDENT-2 (2026-08-04 18:1x UTC): owner screenshot toast "Store migrated - 803 matches / 766 teams" + word "czech"
- Arithmetic vs pinned baseline (REFERENCE/pitch-rating-full-data-2026-08-02.json, md5 5a8ba49475acfa2340ce7fd66e4dfeb0, census computed live): Czech 632 rows, Russia 644.
- 803 = 1,447 - 644 EXACTLY => state = load-test store with RUSSIA purged, NOT Czechia (Czech purge pins: 800 from 1,432 / 815 from 1,447). Toast only fires on .json migration (commitMigration), so owner loaded a post-Russia-purge backup file. Teams 766 = 792-26 (app orphan rule retains entities referenced outside matches; my match-only sim yields 106/125 - registered as sim limitation, verdict rests on match arithmetic).
- STAGED CZ1-2021-2026.txt (held-20) was dropped by the migration re-boot - harmless, re-drop after correct purge. No data lost: purge control is backup-gated (v3.6.2 L3430-3446 downloads pre-purge file before enabling), and all Russia 644 rows also exist in the pinned baseline.
- RECOVERY ORDERED (Option A now firm recommendation): owner migrates REFERENCE/pitch-rating-full-data-2026-08-02.json -> toast must read EXACTLY "1,432 matches / 792 teams" (else stop + report) -> then START-HERE unchanged: purge Czech -> 800 -> CZ1 +1,401 -> 2,201 -> MOLCUP +202 -> 2,403 -> purge Russia -> 1,759 -> RPL 2,979 -> RUSCUP 3,320 -> ADDENDUM 3,338 -> EPL 5,238; all skips 0.
- A/B question state: Option A wipes the unexplained +15 load-test rows (recoverable from his 1,447 pre-purge backup if ever needed); Option B remains available only with his explanation of the 15.

## v0.78 — DEFECT REGISTERED (2026-08-04 18:4x UTC): held packs uncommittable in v3.6.2 (owner report CONFIRMED, code-proven)
- Owner: "no approve button when you attempt to import Czech 21-26". TRUE: staged-card renderer (v3.6.2 L3458) renders Approve only for status 'ok'; 'hold' cards show Discard only; f.holds never displayed. approveStaged (L3791) would commit f.payload correctly - pure UI-affordance gap.
- Instrument replay of app hold rule (CZ1 reproduces EXACT 20 = validated): MOLCUP 19 holds / RPL 64 / RUSCUP 52 / RUS-ADDENDUM 0 / EPL 114 => 5 of 6 packs blocked. HOLD-APPROVE-01 workorder issued: OWNER-OUTBOX/DELIVER-04/ (P0, ship v3.6.3, minimal fix + new harness line G13 hold-review; harness gap owned - my UAT G1-G12 missed the hold-click path, erratum registered).
- Owner path meanwhile: reset store to pinned baseline (toast must read 1,432 / 792), then WAIT for v3.6.3 before purge+imports. Discard of staged CZ1 harmless (staged state only; pack file untouched).
- Import pins for v3.6.3 run (holds = informational, approve-all safe): CZ1 held-20 +1,401 / MOLCUP held-19 +202 / RPL held-64 +1,220 / RUSCUP held-52 +341 / ADDENDUM held-0 +18 / EPL held-114 +1,900; all 0 skipped given purge-first.

## v0.79 — v3.6.3 AUDITED + ADOPTED (2026-08-04 19:0x UTC): HOLD-APPROVE-01 answered
- Arrival pins on APP-V3.6.3/app-v3.6.3.html: md5 17dd2b5b66ceb572a3fd946db9b56a92 | sha256 268dc5296189cf3016847624ba180cb14904a35a07bb2648428581bb78dad0f9 | 635,798 B | APP_VERSION '3.6.3' - ALL EXACT vs manifest. Evidence file md5 EXACT (38af9d9e...).
- Byte-diff vs v3.6.3's base (c7f955d4...): 4 hunks ONLY - hold CSS (+3), version bump, filesView held-card fix (verbatim C.esc'd hold lines + Approve "keep rows verbatim (Z-003)" wired to existing approveStaged), one footnote sentence. Ingest/validators/commit/dedupe/scope/purge/migration/storage/schema UNTOUCHED (diff-proven). node --check PASS x4 scripts.
- Builder self-reported suites (registered, not adopted): hold 9/9, smoke 49/49, scope 43/43, legacy 156/156; no git repo so no commit sha - registered. ZONES-v3.6.3.b64.txt listed in manifest but NOT attached to ferry - noted, not blocking.
- VERDICT: v3.6.3 ADOPTED, replaces v3.6.2 as UAT/usage target (v3.6.2 -> APP-HISTORY candidate). README-UAT v3.6.3 issued with G13 live check + full START-HERE run incl. per-pack hold counts (CZ1 20 / MOLCUP 19 / RPL 64 / RUSCUP 52 / ADDENDUM 0 / EPL 114) and pinned totals 800 -> 2,201 -> 2,403 -> 1,759 -> 2,979 -> 3,320 -> 3,338 -> 5,238; all skips 0.
- INDEX: DELIVER-04 -> ANSWERED. Next number up remains DELIVER-05.

## v0.80 — G13 PASS (owner-reported, 2026-08-04 19:3x UTC): v3.6.3 held-card renders correctly
- Owner screenshots: badge v3.6.3; CZ1 staged card shows "Held - 20 item(s)" + scrollable verbatim hold lines (bohemians 1905~opava, teplice~vlasim, slovacko~zbrojovka brno etc. - verbatim match my instrument list) + button "Approve - keep rows verbatim (Z-003)" + Discard. => HOLD-APPROVE-01 fix confirmed live. CZ1 NOT yet approved (correct: purge-first rule).
- Owner confused amber hold lines for errors -> clarified: they are the informational Z-003 human-check content, expected, 20/20 predicted.
- State uncertainty OPEN: owner has not confirmed baseline reset (toast 1,432/792) nor Czech purge. Next step: read Country packs numbers for Czech Republic (expect 632) and Russia (644 if reset done, 0 if not) before any approve.

## v0.81 — PHASE-4 (ENGLAND) VERIFIED DONE (2026-08-04 ~19:5x UTC, owner screenshots) + order rule restated; Germany/Denmark leftovers flagged
- Owner screenshots: 19:42 England 11 matches·5 comps·114 clubs (=11 of the 15 mystery load-test rows, England-Germany smell: Germany 2 matches·64 clubs) -> 19:50 England 1,900 matches·1 comp·20 clubs = EPL PACK PIN-EXACT. Old 11 English test rows gone (purged before import). England phase DONE; final certification at closing census.
- Owner plan "save old data then purge" = right for Czech/Russia ONLY as backup->purge->import per country (purge wipes old AND new under the flag; recovery = re-import pack, always converges). Restated plainly.
- DO-NOT-PURGE standing: Scotland/Kosovo/US/Canada (approved baseline) + Denmark/Germany (unidentified leftovers, likely remainder of the 15 test rows; pending backup-census identification, then surgical decision).
- Mouse-slip: A/B timing question parked, default carries (Option A: imports first, UI-PLAIN-01 language pass after run).
- NEXT: owner runs Czechia drip (C1 backup -> C2 scope backup+purge -> CZ1 held-20 -> toast +1,401 exactly -> MOLCUP held-19 -> +202 -> Czech Republic = 1,603) then Russia (RPL +1,220 / RUSCUP +341 / ADDENDUM +18 = 1,579), then uploads final backup json for closing census + leftover-row identification.

## v0.82 — CLOSING FILE = STALE PRE-WORK SNAPSHOT (but solves the +15 mystery BY APP LOG) · new backup required
- uploads/pitch-rating-full.json (md5 84136a593e42353a81d7708e0c4d5eaa) exportedAt 2026-08-04T17:25:21Z = 19:25 local: store 803/766/87/223. Pre-work snapshot (before England purge+import and the Czech drip). Cannot certify "all done" off it -> asked owner for the NEWEST pitch-rating-full*.json (or fresh Backup click).
- +15 LOAD-TEST MYSTERY CLOSED by app log inside the file: 2026-08-03T16:19:59Z "Pack committed: 15 matches, 1 teams, 1 season rows" (his load test; 1,432 -> 1,447). Composition proven vs baseline census: England 11 + Germany 2 + Wales 2 = 15 exactly (baseline had 0 of all three). England 11 purged with the EPL replace => expected leftovers in final store: Germany 2 + Wales 2 = 4 rows (unless he purged those too).
- 803-INCIDENT CONFIRMED by same log: 2026-08-04T14:35:43Z "Purged scope Russia: 644 match(es), 26 club(s), 0 attached" (792-26=766 EXACT - my arithmetic matching, two independent proofs), then two migrations reloading the 803-file (15:40Z, 16:18Z).
- Expected final state pins for the closing census: England 1,900 / Czech Republic 1,603 / Russia 1,579 / protected small countries 156 / leftovers 4 (GER 2 + WAL 2) => grand total 5,242 (or 5,238 if GER+WAL also purged). If leftovers present: recommend backup-gated purge of Germany + Wales -> final EXACT 5,238.

## v0.83 — STAR-RATING QUESTION ANSWERED (code-proven) + v3.6.4 combined workorder queued (DELIVER-05)
- Owner: "we have a star ratings system that classify - I don't see it, what did you do to it". Audit answer (all code-proven on v3.6.3 + his own 19:25 backup): engine parameters intact - 7 artifacts incl. dc-fitted-model/tiers/draw-table/gate present; purgeScope cannot delete them (only matches/seasons/venues/ctxFlags/form-declarations of replaced clubs + mutes + orphan identities).
- Mechanism: rated card (Match outlook + Form stars + tier classification) needs identity-level fittedRatings/leagueAttrs stamps (migrated path, L2398). Stamps attach ONCE at fitted-migrate. Purge deleted the holder identity rows (Russia 26 clubs; England ~114 MODEL.teams rows - explains "114 clubs / 11 matches"); new pack identities are created bare; stamping never re-runs => card falls back to honest evidence view. EPL affected via migrated path (E0 IS in the legacy 18-league fitted model). RPL/CZ1 NOT in legacy model - they rate via the ONLINE replay-validated path (__DC_GATE__={RPL:true,CZ1:true}) and should recompute from the new 5-season windows (dcFit derive) - needs owner screen confirmation.
- ELO star layer (derived live from matches) unaffected.
- Gate gap registered: G14 = rated-layer refresh after country replace was not in my runbook/harness (auditor-owned erratum). Builder not at fault - app behaved per honesty rule (refuses a rating it cannot compute).
- Fix queued ONE DROP: DELIVER-05 (md5 above) = RATED-LAYER-01 (idempotent re-stamp for existing identities, no ghost-team recreation, masked-replay refresh on new windows: RPL/CZ1/EPL) + UI-PLAIN-01 (owner decree: plain-language UI; machine strings to small-print details) -> v3.6.4, acceptance adds G14. INDEX next number DELIVER-06.
- PENDING FROM OWNER (3rd ask): fresh post-run Backup upload for closing census (pins: ENG 1,900 / CZE 1,603 / RUS 1,579 / small 156 / leftovers GER2+WAL2 -> 5,242 or 5,238) + screen check Krasnodar-Zenit (RPL online card) and Arsenal-Liverpool (EPL migrated card) for the star question.

## v0.84 — OWNER DOCTRINE ESCALATION (2026-08-04): "live computing system" vs embedded bootstrap - auditor-owned, corrected workorder queued
- Owner accusation + ruling: app carried PRECOMPUTED rating material embedded in the file (window.__FITTED_MODEL__ ~419KB legacy blob 18 leagues + __DC_GATE__ {RPL,CZ1} verdict) + once-ever stamps pinned to identity rows -> rated UI depended on carried data, not live derivation; deleting team rows orphaned it. TRUE, conceded, registered as design debt + my runbook omission (G14). Engine code itself IS live; RPL/CZ1 always rated via the LIVE online path (fit on store rows, replay-validated); migrated blob never covered RPL/CZ1 (code-proven).
- Full D0 inventory of every precomputed input compiled (7 rows incl. calibration artifacts regen-needed, teamStats cache empty, ELO/DC defaults) -> demanded in-app disclosure via new provenance panel (gate G15).
- DELIVER-05 SUPERSEDED (never sent) by DELIVER-06 (md5 above): LIVE-DERIVE-01 = rateable iff app's OWN masked replay on current rows wins (numbers in artifact: n/window/Brier/date); auto re-validation on any data change; no once-ever stamps; bootstrap labeled in plain words and demoted below sufficiency threshold; __DC_GATE__ retired to provenance text; + UI-PLAIN-01 carried; + G14/G15/G16 gates. INDEX next number DELIVER-07.
- Data-side status unchanged: all six packs imported per owner; owner "all done" claimed incl. Russia; closing census still gated on his FRESH backup upload (4th ask) - pins ENG 1,900 / CZE 1,603 / RUS 1,579 / small 156 / leftovers GER2+WAL2 -> 5,242 or 5,238 EE- then programme closing statement EE- then DELIVER-06 ships.

## v0.85 — STAR MATH TRACED (code-proven, v3.6.3) + deeper finding: LIVE path never computed form stars
- Owner demanded exact star computation + ignored-systems ledger (new+old). Delivered both from the file itself.
- Layer A ELO stars (live, unbroken): INIT 1500, K 20, home +65; chronological replay; star=clamp((ELO-1420)/2,0..100), display stars=clamp(round(star/20),1..5). Derived from store rows every derive.
- Layer B fitted card: lambdas from mu*att*def*hfa -> Poisson grid -> H/D/A; tier bands A+ Fortress >=.70 .. E Avoid <.35; form-star grade via starsFor from LEGACY records table ([p,w,d] per team) shrunk PPG (3W+D)/P toward league mean k=star_shrink, needs star_min_games + >=8 peers; star draw correction draw_table[tier|starDiff] blended star_weight capped 0.02.
- G17 finding: predictOnline (live D3 path for RPL/CZ1) returns starsHome/starsAway/starAdj/consensus/confidence = NULL BY DESIGN -> form stars never existed on live data, only via legacy records table. Owner accusation validated at the deepest point. Similarly ship/caution/blocked market flags: written to artifact, read by NO code path (grep-proven inert).
- DELIVER-06 -> v2 (md5 above): adds live form-stars-from-store requirement (or plain not-yet label), inert-blob retirement, gate G17. INDEX refreshed.
- Ignored-systems ledger registered (reply text + this entry): NEW side = calibration suite unregenerated since imports (owner one-click Run masked replay after close), teamStats cache empty, coverage 'undefined' label, FORM rows dormant by design; PROGRAMME-LOST = 3 legacy RPL mute/integrity rows died with Russia purge (new Russian data never re-screened - auditor to schedule re-screen), old identity stamps; OLD side = only blob-ported systems exist here - full old-project coverage audit (OLD-PORT-01) offered on receipt of the old tree (not in audited workspace).

## v0.86 — SINGLE SOURCE OF TRUTH ISSUED: BLUEPRINT-SOT-2026-08-04.md (md5 5898cccd764c755448a12ab0bc57da5c)
- Owner uploaded ENGINE_SPEC.md (md5 91cd0cd5420cd494a799bd4050cb2ef8) + LIVE-BLUEPRINT.md (md5 d01cfde0b7e75f62646bb20eb470233a) and ordered: one SOT doc detailing all computation systems, how the engine is built, how approved omitted systems re-enter.
- Spec-vs-code audit first (decisive): engine code matches ENGINE_SPEC exactly - lambdaFor exp(mu+att-def+hfa+hextra) clamped, fit() constants LR.055/DECAY.0022/HFA_LR.010/1.6<8/0.999, TIERS table byte-identical, star params min5/shrink6/hyst.05, star_weight .2/.5/.5 cap .02, draw_table 27 cells, consensus 1.5/1.0/0.2/min4. Two-grid split incl. goalsGrid k=0.5 GMU 2.6186, BTTS withheld. LIVE path verified = spec B3 gradient verbatim.
- SOT structure: R1 rating engine (5 layers, dual sourcing incl. orphan state + live path), R2 evidence engine (blueprint 8 modules status: 4 LIVE / 3 PARTIAL / 1 NOT BUILT), R3 ELO/CAL8 (live but spec-undocumented - amendment A-03), star categorisation consolidated (owner example formalised), data lifecycle layer, 16-row MISSED-WORK LEDGER (M1-M16 with route-in per row), end-to-end pipeline, amendments register (A-01/A-02 adopted; A-03..A-06 pending), reference pins.
- PATH-MAP updated (re-pinned above). Owner decisions pending: A-03 ELO adopt/retire, A-04 ship/caution/blocked consume-or-drop, A-05 integrity re-screen method, A-06 goal-range timing; actions pending: fresh backup (M15), masked-replay click (M5), METHODOLOGY.md (M13), old tree for OLD-PORT-01 (M12).

## v0.87 — SOT FULL AUDIT + v1.1 ISSUED (md5 5dc8df75aa60cc7705c24ba8bda543ff): METHODOLOGY integrated (md5 6cd6c0c8ebc695a8fe3afc313ddc90ac), cold-start kit defined, ledger M1-M18
- Auditor self-audit of SOT v1.0 per owner order ("does it contain all systems; can a coldstart orient on this alone"). VERDICT v1.0 = NO to both (gaps listed below) -> v1.1 closes them.
- Gaps found in v1.0 -> fixed in v1.1: (G1) METHODOLOGY absent (P1-P5, T1-T8, I1-I6, E1-E9 now integrated); (G2) sync-protocol lineage unmapped (mapped: old paste-sync -> new file ingest); (G3) settlement/I5 draw=loss rule absent (added + audit row M17); (G4) calibration/derived backend under-documented (expanded M5/M6); (G5) blob coverage counts (18 leagues/414 rated teams/342 records per METHODOLOGY VI); (G6) P1 CONFLICT FOUND: legacy market-price mute screen doctrine-violating -> A-05 RESOLVED (outcomes-only screen owed; purge loss doctrine-consistent); (G7) fidelity record noted; (G8) suite lineage 167 vs 156 unproven -> M18 to builder; (G9) kit undefined -> COLD-START KIT K1-K10 pinned table.
- New explicit non-approvals recorded: unified European ratings = proposed NOT approved (open item 5); chain defects (usability gate disproven, narrow path discovery) kept as standby defects, not silent.
- Cold-start verdict v1.1: ORIENT + OPERATE + extend in-app engine = YES with kit K1-K10 (3 foundation docs + app + audit card + pack spec + runbook + rules/ZONES + baseline store, all md5-pinned); legacy off-app trainer rebuild = NO until M12 (old tree upload) - declared, not smoothed.
- Ledger now M1-M18; M13 CLOSED; M10 resolved-in-principle (outcomes-only screen spec owed by auditor, owner P5 approval required).
