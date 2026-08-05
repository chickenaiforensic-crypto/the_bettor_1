# XX — M10 Outcomes-Only Integrity Screen Spec (P1-Compliant, No Market)

**Date:** 2026-08-05 — Auditor Support task completion, per SOT A-05 RESOLVED  
**Status:** DRAFT SPEC — Owner P5 approval required before ship  
**Authority:** SOT §1 P1 No market data Ever excluded in ALL roles input/feature/benchmark/sanity check/fallback, SOT §10 M10 Integrity screening of new data RESOLVED in principle (A-05): legacy market-price screen is P1-non-compliant, do NOT restore, replacement = outcomes-only screen spec owed by auditor, METHODOLOGY P1 doctrine ruling 2026-08-04.

---

## Why Legacy Screen Is Banned

Old project tree had integrity screen that muted 3 RPL rows using market closing prices → METHOD P1-non-compliant. That screen's loss at 2026-08-04 purge is doctrine-consistent. Any future screen must be outcomes-only (own-model collapse detection), never price-referenced.

## What Muted Rows Are (Doctrine)

- Suspicious games flagged with rationale, kept visible and excluded from every calculation — never deleted — exclusion = MUTE (L3538). Restore button reverses (L3542).
- Snapshots taken before every data commit (L3548) + purge hash snapshots scope-post.
- New-data integrity screening must be outcomes-only (A-05, owner-collision screen spec owed by auditor).

## Outcomes-Only Integrity Screen — Automated Detection (P1-Compliant)

Detects collapse from own model, not from market.

### 1. Brier Shock — Settlement Variance >2.0σ

- **What:** For each league, compute rolling Brier over last 30 settled tips (from Log & Settlement tab, settlement rule draw=loss I5 never push). Compute mean and sd over last 100 settled. If latest 30 Brier mean is >2.0σ above historical mean (worse), flag last 10 matches as potential integrity anomaly — own-model collapse.
- **Why outcomes-only:** Uses only our own settlement ledger (home/draw/away Brier, logloss, direction) + settled outcomes, no market.
- **Action:** Mute scope? No — flag with NOTE|info|integrity_flag|brier_shock|league X last 30 Brier 0.72 vs historical 0.58 +2.3σ, reveal in Integrity & Snapshots tab with rationale "Own model Brier shock — last 30 worse than historical 2.3σ — manual review recommended — muted pending review?" — human approves mute via verbatim-approve button, not auto-mute.
- **Threshold:** 2.0σ, window 30 vs 100, requires n≥30 settled.

### 2. Rating Jumps — Per-Team Att/Def Shifts >0.5 Goals Without Results

- **What:** For each team, track att/def ratings over time (L1). If att jumps >0.5 log-goals or def jumps >0.5 (worse) over last 3 matches WITHOUT corresponding match results (i.e., rating changed but no new matches? Or rating jumps >0.5 in 3 matches where expected change per match is LR*error*0.5 max ~0.055*3*0.5 ~0.08, so 0.5 is huge), flag as potential data error or integrity issue.
- **Why outcomes-only:** Uses only own att/def time series + match results, no market.
- **Action:** Flag team with NOTE|warning|ratings_jump|team X att +0.62 in 3 matches without results? Actually with results but unrealistic jump suggests corrupted result? Human review.
- **Threshold:** >0.5 goal shift in att or def over last 3 matches, where expected max per match ~0.2 (new team 1.6×), so 0.5 in 3 is 2.5× expected.

### 3. Venue Ghosting — Guard for Teams That Never Hosted at Verified Venue (I4)

- **What:** Per METHODOLOGY I4 venue integrity procedural not statistical: never trust parsed venue, hard error if home team never hosted in league, tick-box vs official list, save disabled until confirmed, venue locked at entry. Existing implementation: venue/neutral/relocated flags in match rows + no-reflip at ingest, entry-side flip guard belongs manual-entry surface unaudited M17.
- **Outcome-only check:** For each new pack, check if home team X appears as home in league Y but never appears as home in our verified venue list for that league — hard error save disabled until confirmed via official list tick-box.
- **Action:** Ingest gate holds with human approve (Z-003 style) — row kept verbatim, grouped by competition+pair, human presses "Approve — keep rows verbatim" if venue confirmed via official list, else "Approve — neutral_venue" NOTE info/neutral_venue reason. Never trusts parsed venue.
- **Threshold:** Hard error, not statistical.

### 4. Additional Outcomes-Only Checks (Optional, P1-Compliant)

- **Relegation/Promotion Anomaly:** Team promoted via playoffs but no playoff results in store? Flag — needs playoff evaluation minimum 3 matches per owner clarification 10.
- **Score Extremes:** Score >10 goals? RGL? Integer 0-30 sanity from gate L887 — 90-min doctrine, non-negative integers.
- **Duplicate Fingerprint:** date+canon(home/away/competition) add-if-new dedupe L321 L1016 — match already in store skipped never duplicated — 0 dup in 5082 verified.
- **Future Dates:** vs export date 2026-08-05 — 0 future verified.

### 5. Mute vs Purge Doctrine (No Data Abolition)

- **Exclusion = MUTE:** One action mutes whole scope (excluded from every calculation) toast text L3620 "excluded from every calculation" + Unmute scope restore reverses muteScope L2928 buttons L3431 — nothing deleted by mute.
- **Purge = hard clear** of that scope — backup-gated by machine not promise: before backup exists button reads "Download backup, then purge" L3434 pressing auto-downloads full backup named pitch-rating-full-data-<date>-pre-purge-<scope>.json downloadBackup L3447 only then unlock as backup ready L3433, purge log entry records backup filename L2988, in-app text "There is no undo button inside the app. Undo = load the backup file you just downloaded" L3436 — purge removes scope matches + orphaned club identities mutes attached go with them L2976 engine artifacts survive.
- **Standard replace flow:** backup → purge scope → import new pack → confirm toast counts → fresh backup — as used in programme runbook.

### 6. What This Screen Does NOT Do (P1 Compliance)

- No market data in any role — input, feature, benchmark, sanity check, fallback — prices/shadow never evidence. Historical Gate1 conclusion market-based SUSPENDED pending outcome-only re-test (open item 3).
- No odds fields in ingest grammar, no odds input in engine (SOT §1), no fetch/XMLHttpRequest to odds sites (I6 zero network dependency).
- No profitability claims — calibrated ≠ profitable, only calibration claimed.

### 7. Implementation Plan (After Owner Approval P5)

- **Spec approval:** Owner approves this spec per P5 shipping needs explicit owner approval — violated once historically Study06 stars shipped unapproved → E7 mapped to today's owner→workorder→auditor-gate→UAT chain.
- **Build:** Builder implements as Integrity & Snapshots tab enhancement — new section "Automated Integrity Flags (Outcomes-Only)" — lists flagged matches/teams with rationale + Brier shock chart + rating jump chart + venue ghosting hard error list + Approve Mute verbatim / Restore buttons.
- **Gates:** Settlement & venue-guard audit I5 draw=loss enforcement + I4 entry-side flip guard M17 acceptance pins — unaudited this session per FUNCTIONALITY §14 — M17 audit row.
- **Cadence:** After any data change masked replay auto-reruns M1 monthly full sweep M5, integrity screen runs after each masked replay.
- **Backup-first rule:** Purge/import flows backup-gated undo = load backup.

### 8. Example Flags (Smooth English, Human-Friendly, Not Bot)

Main UI: "⚠️ Integrity flag: Russian Premier League last 30 settled tips Brier 0.72 vs historical 0.58 +2.3σ worse — own model struggling lately — 10 recent matches flagged for manual review — not auto-muted."

Tooltip: "Brier shock — own model — no market — manual review recommended — flagged matches kept visible excluded pending approve?"

Technical details small-print: "Rolling Brier 30 mean 0.72 sd 0.15 historical mean 0.58 sd 0.06 +2.3σ window 30 vs 100 n=30 settled, threshold 2.0σ, flagged last 10 matches IDs m:123 etc — Brier formula sum(p - y)^2 per match — settlement rule draw=loss I5 — never push."

*Spec P1-compliant outcomes-only own-model collapse detection — no market — ready for owner approval P5.*

---

## Pins & References

- SOT v1.3 §1 P1, §10 M10, §12 A-05 RESOLVED, §14 pins live authority
- METHODOLOGY P1-P5, T1-T8, I1-I6, E1-E9
- FUNCTIONALITY v1.0 §10 Integrity & Snapshots tab L3537-3547 muted rows kept visible excluded never deleted, snapshots L3548
- Masterplan v1.1 §5 approval by test run ladder, §8 build order S1-S7 S2 settlement/venue audit M17 S6 calibration cadence M5 S7 architecture human-friendly
- Builder B0 v3.7.0 ACCEPTED report 19-B0-AUDIT

*Draft spec — owner approval required before ship — outcomes-only integrity screen.*
