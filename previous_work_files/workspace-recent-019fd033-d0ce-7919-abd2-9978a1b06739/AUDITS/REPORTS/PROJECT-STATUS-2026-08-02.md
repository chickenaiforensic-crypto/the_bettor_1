# PITCH RATING — programme status at wrap (2026-08-02, Europe/Paris)

One page. Numbers only, everything pinned. The rule the whole programme ran on:
**a league exists because its match data exists; a percentage exists because it won its way
through blind replay; a claim exists because someone re-ran it.**

---

## 1 · The app

| | |
|---|---|
| Current app | **`app-v3.5.1.html`** (v3.5.1) — md5 `ce61de0f9e500d3917d053e9e4e77c3e` (604,770 B; base64 drill 3/3 md5-verified) · backup `backups/app-v3.5.1-ce61de0f.html` · raw .html downloads from the channel are poison (Cloudflare blocks) — b64 only |
| Prior | `app-v3.5.html` md5 `400077a9…` · `app-v3.4.html` md5 `b464f046…` (+ backups; all superseded by v3.5.1) |
| Legacy (reference, untouched) | `app-v2.6-cross.html` = v2.9.9, md5 `14a7a9572f2428eb1689a2f601c3583c` — smoke 156/156, rollback anchor |
| Store | 1,436 matches · 539 identities (167 pack/match + 372 model-rated) · 3 mutes (retained, excluded from compute) · full log |
| Engines | evidence graph (ported, parity 7/7 vs legacy) · Elo/perf (CAL8) · Dixon-Coles (ENGINE_SPEC, migrated 153k-match fit) |
| Fitted cards | 18 legacy-fit leagues + **RPL + CZ1** (earned on masked replay: Brier 0.5621/0.5822 vs evidence 0.5929/0.6314 — pool + both halves) |
| Data in | files only (drive folder/picker → stage → approve → commit). No paste, no network, no framework |
| Data integrity | 9 seed packs, all byte-verified vs canonical; dedupe on; mutes visible with reasons; ghosts honest |

## 2 · Proven this week (audit trail — all re-runnable)

- Engine port exact: Krasnodar v Fakel Δ = 0 (S_=78.5714 both apps) — AUDIT-APP-V3.md
- Live compute: 1 injected row → hash changed, zone 67.1→67.7, gate C11 fired
- CSKA v Krylia fitted: 59.1/23.9/17.0 with provenance `fitted on Russian Premier League 2024–26 — validated on 568 of 641 masked rows`
- R1: "krasnodar"→FC Krasnodar, all 539 reachable · R3: per-side W-D-L records per section
- Honesty: MLS no-share → NO CALL + form · ghosts → honest states · BTTS withheld as untested
- Suites: new-app 43/43 · parity 7/7 · legacy 156/156 · packs 27/27 · closure 19/19 · concat 61/61
- Docs: `AUDIT-APP-V3.md` (2 addenda) · `ZONES.md` through v0.27 · builder trail + gate evidence verified

## 3 · Still open — who owns what

**Owner homework ① — RECEIVED + GATED (2026-08-02).** `pitch-rating-full-data-2026-08-02.json` (md5 `5a8ba494…`) passed the migration machinery: 2,525/2,525 rows carried, 0 mismatches, fitted path + gate live on the migrated store (MIGRATION-GATE-2026-08-02.md). Blocker: no UI import path (M1) + provenance key mapping (M2/M3) → **R11 to builder (v3.5.2)**, forward `R11-FORWARD-TO-BUILDER.md` verbatim. Homework ② (Scotland pack): teams now carried by migration; pack still wanted for depth. v3.5.1 (verified): routine returns flip the correct league section (codes inferred from staged match rows), zero-commit returns log one honest skip with no success line/stamp/state-flip, replay TB-led hitRate fixed, ingest commit-skip honest, flat picker live. Central Request System (D12) truthful end-to-end: one button → snapshot + `central-request-<date>.txt` → returns to the same intake; Requests fulfilment icons are now trustworthy for routine returns.

**Owner (2 items):**
1. Live store export — `pitch-rating-full` JSON from the OLD app's Data tab (lets the migration gate run on real history; predictions/log carry over).
2. `Ross-County_St-Johnstone_BP-TEAM-PACK_v2.txt` (P3; SC1 currently ghosts by design until its data lands).

**Research/data pipeline:**
Brazil WO ready on your word · MLS round-2 supplier order open · SC1 cure waits on Annex-A bulk ·
Swiss per your standing go · WTA parked.

**On request (standing offers):** frozen-vs-current slate re-verification (Krasnodar frozen 75.8 vs
current recompute flagged) · settlement run vs SLATE-2026-08-01-03.md once the new app's result
ledger starts filling.

## 4 · The doctrine that now holds (unchanged when data changes)

Results only · 90-minute doctrine (ties by tieId, advancement as NOTE) · no odds/injuries/lineups as
inputs · no fixture substitution · no data abolition (exclusion = MUTE flag only, visible, reversible) ·
system may always refuse · frozen numbers settle, forward numbers may drift · every claim re-runnable.

---
### 2026-08-02 (late) — doctrine clarification + full queue staged
Owner clarified the 5-year rule: **the window is continuous, not capped slices** — 2021-22 season → today, gap-free end to end; researcher-side "research all data" = the control record proving our old data has no gaps; every return audited against the full federation span; unexplained holes keep the commission open. Written as §5.1 Continuity clause in all 4 backfill workorders + handoffs README rule 7 + AUDIT-DATA-QUALITY doctrine block. Queue staged in REPO-UPLOAD/: ① RPL league (open w/ researcher) ② CZ1 league ③ Russian Cup ④ MOL Cup — all <2024-06-30 cutoff, one-at-a-time gating. Owner homework unchanged: download final files (app-v3.5.2 + export + Southampton pack) and run the 3-click migration BEFORE any return is loaded.

### 2026-08-02 (night) — queue now COMPLETE: 7 workorders staged
All leagues in the system now carry a handoff: RPL (open), CZ1, RUSCUP, MOLCUP (all 5YSPAN cutoff files) + NEW: SCO1 ~1,100 rows · KOS ~890 · MLS ~2,800 (no-cutoff appendix-exclusion files; rosters pinned from live RSSSF). Owner authorized PARALLEL research (overnight); auditor approvals remain one card per return in queue order. Not commissioned (his word adds): US Open Cup, Scottish Cup, UEFA quals, friendlies. Owner homework unchanged: 3-click migration first; REPO-UPLOAD/ drag = the whole 7-file queue in one Commit.

### 2026-08-02 (night 2) — queue = 11: four national cups added
US Open Cup ⑧ · Scottish Cup ⑨ · Scottish League Cup ⑩ · Kosovo Cup ⑪ — closing the last national-competition gaps. Still fixture-led (out unless decreed): UEFA quals/group ties (tracked-club partial by design), friendlies, one-match Super Cups.

### 2026-08-03 — queue = 16: the five major leagues staged (owner decree)
EPL 1,900 · SPA 1,900 · ITA 1,900 · GER 1,530 (18 clubs) · FRA 1,678 (20->18 trap pinned). All ~135 member clubs already exist on the roster — no TEAM rows expected, dup risk dead. Program ≈16,300 rows. Next-tier majors (POR/NED/BEL/TUR/GRE) await his word. Reminder: final app = `app-v3.5.2.html` in workspace root (md5 6bd76ae0...).
