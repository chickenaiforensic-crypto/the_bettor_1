APP-V3.6.1/ — auditor-verified build for owner UAT (2026-08-04)

  app-v3.6.1.html   md5 762a62846eb5c9531627e1d67be365a8 · 630,593 B
  (arrived base64-wrapped: decoded and md5-verified against the builder's MANIFEST
   package 9 — byte-exact, zero transit junk this time. supersedes v3.6.0.)
  What v3.6.1 changed vs v3.6.0 (auditor diff, exactly 2 edits): version bump +
  scope preview now renders the FULL row list (400-row display cap removed = my R2).
  Still missing (owed as v3.6.2 via OWNER-OUTBOX file 01): league-level clear
  selection (D1) + alphabetical listings (D3). Non-blocking for whole-country clears.

SEALED BASELINE unchanged: app-v3.5.2.html md5 6bd76ae0… (untouched, still the rollback).

UAT — Data tab → "Country packs" → run gates IN ORDER (G1→G12):
  G1  panel shows Russia 644 (489/152/2/1, 26 clubs) · Czech Republic 632 (561/63/8, 45)
  G2  preview: full breakdown, remove vs kept club lists — and NOW the full scrollable
      match list (all 644 rows for Russia, no cap)
  G3  purge button disabled until the backup .json auto-downloads
  G4  MUTE Russia → counts held out · UNMUTE → identical counts back
  G5  PURGE Russia → Coverage 1,432-644 = 788, log shows scope-purge + backup name
  G6  load the downloaded backup json → store back to exactly 1,432 (undo proof)
  G7  (optional add-path test) drop RPL pack c3a72b35 → +732 → 1,520, zero skips
  G8  Czech preview: 632 with 561/63/8, 45 clubs, keep-list rendered
  G9  drop the same pack twice → second drop = all "Skipped duplicate", totals unchanged
  G10 no per-country coding (auditor-grepped, clean)
  G11 engine boots clean after purge/replace, no console errors
  G12 log/snapshot entries written for every operation

TEST DISCIPLINE: G1-G6 first (they leave the store intact or provably restored).
If any gate fails: STOP, tell me gate number + what you saw + Coverage numbers.
