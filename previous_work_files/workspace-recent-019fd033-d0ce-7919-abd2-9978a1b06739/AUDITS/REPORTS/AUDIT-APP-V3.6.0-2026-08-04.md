# AUDIT CARD — app v3.6.0 (WO-SCOPE-CLEAR-01 return) — 2026-08-04 — **APPROVED FOR UAT + 2 return items**

Builder session returned v3.6.0 claiming md5 `edf52d78b2fa1690721aa3a72018b634` / 630,363 B and 33/33 harness gates. Self-reported counts never adopted; all evidence below is auditor-run on the delivered bytes.

## 1. Transport forensics — md5 mismatch EXPLAINED and resolved byte-perfectly
- Attached file arrived as md5 `c5183f75…` / 631,654 B ≠ claim → immediate hold.
- Forensics: exactly ONE appended line (1,290 B) at line 11074 = Cloudflare injection (`__CF$cv$params` iframe challenge + `cloudflareinsights.com/beacon.min.js` external script) — added in transit by the edge proxy, not by the builder. Same hazard class as the worldfootball CF block.
- Stripped that single line → **size 630,363 B ✓ · md5 `edf52d78b2fa1690721aa3a72018b634` ✓ = builder's pinned source, byte-exact.** Both anomalies resolved to zero residue. Owner's UAT file = `APP-V3.6.0/app-v3.6.0.html` (clean copy, pin re-verified).
- Lesson registered: CORRUPTION-AT-TRANSPORT is a standing risk; md5-on-arrival before any use, always. Policy proven working.

## 2. Seal discipline — v3.5.2 untouched; diff vs 3.5.2 = additive-only except sanctioned lines
Verified by line-diff. ALL changed ('c') regions inspected one by one:
| Region | Content | Verdict |
|---|---|---|
| L357→370 | `APP_VERSION '3.5.2'→'3.6.0'` (+one comment) | ✓ versioning policy honored |
| L1202/1261 (+2 one-liners) | `if (m.muted) return;` inside the two Coverage counting loops | ✓ **sanctioned by G4** (muted convention); minimal-blast edit; nothing else in Coverage logic touched |
| state init (+2) | scopeView/scopeKey/scopeBackups/scopeDropSources fields | ✓ benign |
| tabs2 | `['scope','Country packs']` added | ✓ benign |
| exports | `+ downloadBackup, scopeBackupReady` | ✓ additive |
| +195 lines (engine), +75 (UI), +35 (handlers/CSS) | new `PR.scope` module + views + bindings | ✓ reviewed below |
| **ingest dedupe, commitMigration, hold rule, migration replace** | — | ✓ **byte-identical, zero edits** |

## 3. Feature compliance vs §2/§3/§4 of the workorder (code-read, not claimed)
- Generic scope model: `matchCountry` = m.country → clubs-agree → Multi/ Unassigned; scopes/competitions derived 100% from store ✓ · **G10 grep: zero country/competition literals inside the new code regions** ✓ · no-network: zero external refs in added regions ✓ (the only external script was the transit CF junk = removed).
- ONE selection function (`selection()`) feeding list/preview/confirm/mute/purge — counts provably identical across screens ✓.
- Orphan rule: `refs()` counts remaining references across matches/seasons/venues/ctx/form-artifacts; remove-vs-kept club split rendered incl. **cross-border guard** ("Kept (still referenced)") ✓.
- MUTE: `muted=true` + log `scope-mute` + contentHash snapshot; UNMUTE bitwise; muted-count badge on list rows ✓.
- PURGE: atomic in-place multi-collection filter + one save; no-op honesty path (`scope-purge-noop`); sources kept by default with opt-in drop checkbox + referrer recount ✓; log records backup filename + hash snapshots pre/post ✓ (G12 mechanics).
- **Backup gate is double-enforced**: button renders only when `state.scopeBackups[scopeKey]` set (which only `downloadBackup()` sets, after firing the existing `STORE.exportFull` download) AND the click handler re-checks `scopeBackupReady()` before showing confirm ✓ (G3).
- Post-purge toast: *"Scope purged — next: drop the new packs in Files; they import as pure adds."* ✓ the replace-handoff in words.
- Honest undo line on every preview ✓.

## 4. Two return items (v3.6.1 delta)
- **R1 — G2-L (league-level clear) NOT implemented.** `selection()` resolves `s.country === scopeKey` only; the list view has no per-competition rows. Cause: my league-level amendment (v0.65a) post-dated his build start; he built the original WO. **Blocking only for league-granular clears; every sanctioned no-mix flow (Russia 644 / Czechia 632 / Scotland / Kosovo / MLS+) is whole-country, so current build covers the endgame.**
- **R2 — preview match list capped at 400 rows** (`slice(0, 400)`) — Russia=644 → list truncates; all counts remain exact (selection fn unaffected). Spec said "full row list". Cosmetic-but-specified; same delta.

## 5. What was NOT (and cannot be) auditor-run here
The builder's "33/33 acceptance" harness executes in HIS session — registered, not adopted. Functional acceptance = **owner UAT G1→G12 in the browser** (README-UAT.txt in `APP-V3.6.0/`; G1–G6 leave the store provably intact). Auditor will re-verify by diffing post-UAT owner reports against the pinned numbers (788 / 1,432 / 1,520).

## Verdict
**v3.6.0 (md5 edf52d78…) APPROVED FOR UAT.** Compliance with the binding workorder = full (evidence §2–3). v3.6.1 delta commissioned for R1+R2. Registry: ZONES v0.66.
