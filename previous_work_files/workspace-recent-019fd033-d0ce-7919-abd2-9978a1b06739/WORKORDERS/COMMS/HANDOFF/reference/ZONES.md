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
