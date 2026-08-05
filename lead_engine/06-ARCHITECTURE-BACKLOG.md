# 06 — ARCHITECTURE BACKLOG (Human-Friendly Build, After Structural Engine)

**Date:** 2026-08-05  
**Status:** BACKLOG — per owner order: structural engine first (S0-S6), then architectural/UI build (S7). Poor content quality noted — "so AI instead of human-friendly, quality of presentation and general functionality is poor."

## Current App Audit (v3.6.3 md5 17dd2b5b66ceb572a3fd946db9b56a92)

### What Exists (FUNCTIONALITY-2026-08-05.md)

- One HTML file, no server, localStorage `pitch-rating-v3.store` L381, version badge footer L380 L3459
- Header: theme toggle ◐, Backup button L3070-3071
- Five tabs L3075: Match, Data (Files·Coverage·Requests·Country packs 4 sub-tabs L3355), Calibration, Log&Settlement, Integrity&Snapshots
- Match tab: team picker tolerant spelling grouped by league L3083, Predict → fitted card `predictFitted` L1974 for calibrated model vs online card `predictOnline` L2090 live re-fit for new programme leagues (RPL,CZ1), Save row btn-settle L3178/3570 frozen numbers never change afterwards live may move L3533, Swap ⇅ L3148/3567, perfView L2512 last-6 form displayed never edited
- Files tab: one gate PR.ingest L709, gate checks L724-951 row grammar Annex B/legacy v1 completeness scores non-negative ints 90-min only L887 competition type whitelist COMP_TYPES L737 includes uefa-cl/el/uecl, duplicate fingerprint L890, no future, tie-linkage. Outcome: Clean→staged Approve Approve commits toast "Loaded — N matches." approveStaged L3803 toast L3811; Held Z-003 exactly-two-leg cup ties different tie-ids L922-951 kept verbatim grouped comp+pair human Approve keep rows verbatim fix v3.6.3 L3791-3814; Rejected never stored L3478. Against store dedupe date+canon pair+comp L321 L1016 skip never duplicate. Migration full atomic replace Store replaced by migration L519. First boot 9 seed packs SEED_PACKS L11061-11100.
- Country packs tab scopeView L3369 purgeScope L2957 scope=country optionally competition chain list→preview counts→confirm scopeListView L3379 scopePreviewView L3400 scopeConfirmView L3439 matches/clubs/attached/comp breakdown before L3441-3445 sources kept audit L3429. Mute scope soft clear exclusion=MUTE one action mutes whole scope excluded every calc toast L3620 Unmute restore muteScope L2928 buttons L3431 nothing deleted by mute. Purge hard clear backup-gated button reads "Download backup, then purge" L3434 auto-downloads full backup named pitch-rating-full-data-<date>-pre-purge-<scope>.json downloadBackup L3447 only then unlock backup ready L3433 purge log entry records backup filename L2988 in-app text no undo inside app undo=load backup file you just downloaded L3436. Purge removes scope matches+orphaned identities mutes go with them L2976 engine artifacts survive.
- Coverage tab L3481-3491 one row per league seasons held row counts gaps amber status pill complete/partial/requested honest inventory missing not just existing
- Requests tab L3492-3516 newCentralRequest L3817-3834 one button New central request snapshots whole system writes one request file listing every league needs rows per team with date downloads both files central-request-<date>.json+.txt logs event tracks state open→sections complete/partial→archived L3507-3513 returns matched to open request L3757 D12 only channel for asking data one request whole system no drip-asking
- Calibration tab L3517-3527 Run masked replay re-computes fitted model from current store later hidden predicts compared artifacts replaced only when validation numbers written into artifact n window Brier/score date artifacts store as dc-fitted-* records model/draw table/tiers/markets L1902-1912 rule A-01 doctrine workorder LIVE-DERIVE-01 queued for v3.6.4 rate only if own replay on current data wins else stay silent plain label owner duty click after any data change now owed after 2026-08-04 imports M5
- Log&Settlement L3529-3536 lists settled rows log entries type settle newest 20 audit trail itself every event migrations/commits/purges/snapshots/requests kept inside store log travels every backup append-only provable 55 entries zero unreconciled settlement-rule audit draw=loss entry-side flip guard queued M17 unaudited
- Integrity&Snapshots L3537-3547 muted rows flagged rationale kept visible excluded every calc never deleted exclusion=MUTE Restore button L3542 new-data integrity screening outcomes-only A-05 owner-collision spec owed snapshots taken before every commit L3548 purge adds hash snapshots scope-post entries
- Backup safety L491 exportFull L3569 header button downloads pitch-rating-full.json wrapper format/version/schemaVersion/exportedAt+full store+full log verified real one 2026-08-05 sha256 c7b29e85…8fc00 3588489 bytes complete store 5000+55 log habits backup before purge backup after import round backups raw JSON never zipped transport rule
- Data model store keys meta schema v3.0.0 creation stamp seed pack names seq identities teams canon+aliases matches date competition compType home/away 90-min goals venue country tieId sourceId seasons venues sources every match rows to source URL+date notes AET/penalty rides with data 90-min doctrine ctxFlags mutes log artifacts calibration+form declarations+central requests FORM rows reconciliation-only never hidden compute input L1053

### Problems — Why "AI Instead of Human-Friendly"

1. **Machine language in UI** — stars, tiers, consensus, HvH/AvA, Brier, Poisson, DC, ELO leak into main UI. Decree A-02 UI-PLAIN-01: machine strings belong in small-print Technical details only. Currently violates.
2. **No provenance** — numbers appear without source/window/n/calibration/date (M3 missing). User cannot verify where number came from.
3. **Form stars null** — live path returns starsHome:null → omitted system M2/G17 — user sees empty.
4. **Calibration artifacts stale** — since imports, replay owed M5 — user cannot trust calibration numbers.
5. **No balance panel on NO CALL** — P3 honest refusal valid but must show balance (home/draw/away support shares) — M7 partial.
6. **TeamStats cache empty** — perfView depends.
7. **Coverage undefined label** — cosmetic M14.
8. **AI-styled presentation** — AI-generated verbosity, lack of human-first hierarchy, no clear primary action, technical jargon without explanation.
9. **General functionality poor** — per owner: "quality of presentation and genera functionality is poor" — needs UX pass after structural work.

## Human-Friendly Target (S7 — After Structural Engine Locked)

### Principles (A-02)

- Plain language in main UI, machine names bracketed small-print only.
- Every number provable — provenance small-print: source, window, n, calibration, date (M3).
- Honest refusal as first-class output: NO CALL with reasons + balance panel, never fabricate.
- One store, one live fit, one verdict card — no second rating universe.
- Backup-gated purge, no in-app undo — text states rule outright.

### Screen Map Target (Post S0-S6)

**Header:**
- Theme ◐, Backup button prominent, version badge, store count honest: "5082 matches · 609 teams · last replay 2026-08-05"

**Match Tab (Daily):**
- Team picker: searchable, tolerant spelling, grouped by league, shows league + country, recent form inline last-6 WDL + ELO star 1-5 visual ★★★★☆ not raw numbers.
- Predict button → verdict card:
  - Top: probability (favourite + %, e.g. "Arsenal 62% Home") provenance small-print underneath (source: live DC fit, window 2021-22..2024-25 train 960 rows, masked replay Brier 0.5675 base 0.6465, date 2026-08-05)
  - Middle: confidence band zone ladder STRONG/WIN etc with n/spread/calibration shown: "STRONG (78% historical, n=59 pair)" not "model confidence 0.78"
  - Bottom: labels tier A+ Fortress 78.5% win n7718 etc, consensus when allowed "STRONG >1.5 goal-diff both lenses ≥4H/≥4A 78.6%", scoreline max cell uncorrected grid + true ~13% freq, stars display-only "Performance ★★★☆☆ (ELO 1567, not a prediction)"
  - Refusal paths: plain label "Not rated yet — <6 matches" / "Evidence only — rating needs 2 full seasons + replay win" / "NO CALL — evidence split 48/22/30 — see balance" + balance panel bar chart home/draw/away support shares
  - Actions: Save row (freeze numbers), Swap, Technical details collapsible small-print (λ_home, λ_away, μ, hfa, Poisson grids, draw table correction ±0.02, ELO numbers)

**Data Tab:**
- Files: drop zone + gate explanation in human words "We check every file for format, dates, scores, duplicates — rejected files never saved". Staged card with Approve, Held Z-003 explanation "Two-leg tie has different tieIds — we keep rows verbatim, you approve", Rejected reason shown.
- Coverage: honest inventory per league seasons with row counts gaps amber status pill complete/partial/requested + shortfall list "MOL Cup now 202, was 120 — +82 added 2026-08-05" + what we hold leaf.
- Requests: New central request button explanation "One request for whole system — lists every league needing rows" + open/archived states.
- Country packs: scope picker country (+ competition), preview counts matches/clubs/attached/comp breakdown, Mute soft "excluded every calculation, not deleted — Unmute restores", Purge hard backup-gated flow "Download backup, then purge" auto-download named pre-purge + backup filename logged + in-app text "No undo inside app — load backup you just downloaded".

**Calibration Tab:**
- Run masked replay button explanation human: "Hides last season, retrains on earlier, predicts hidden, compares — tells us if model beats base rate". Artifact list with numbers: n/window/Brier/logloss/dir/date. Auto-regeneration notice "Auto-reruns after any data change — last run 2026-08-05". Monthly full sweep cadence.

**Log & Settlement:**
- Settled rows newest 20 + settlement rule explanation "Draw = loss for home call — never push, never excluded — feeds calibration". Filter by league/date. Audit trail 55 entries provable.

**Integrity & Snapshots:**
- Muted rows rationale visible excluded every calc never deleted Restore button. Snapshots trail before every commit + purge hash snapshots. New-data integrity outcomes-only screening explanation (future).

**Backup:**
- Download backup button exports full JSON wrapper + store+log verified size.

### UX Quality Bar

- No AI filler: every sentence states one fact with proof.
- Primary action obvious per tab (Predict, Drop file, Run replay, etc.) — one CTA.
- Progressive disclosure: main = plain language human, collapsible Technical details = machine.
- Accessibility: keyboard nav, screen reader labels, color contrast theme toggle works.
- Performance: one HTML file <1MB? Currently 635k, okay — no network fetches.
- Empty states honest: "Not rated yet" not "0%".

### Build Order Dependency

- Structural must be fully planned & passing harness: S0 harness productionised, S1 LIVE-DERIVE-01 live re-derive+auto re-validation+provenance+live form stars, S2 settlement/venue audit I5+I4, S3 balance panel, S4 goal-range bins 0-1/2/3+ calibrated, S5 cross-border UEFA connector fit-to-results weighted scale vs 1.00 baseline, S6 calibration cadence.
- Then S7 UI/architecture build — human-first — separate design phase per owner.

### What NOT to Build (Explicitly)

- Unified European ratings without A-08 replay win.
- Any market/odds input/feature/benchmark.
- Injuries/lineups/xG.
- Profit claims.
- AI confidence language hiding provenance.

*Architecture planned after singular engine weight-locked and winning test runs. Human-friendly = plain words, numbers provable, refusal valid, provenance small-print.*
