APP-V3.6.2/ — auditor-verified build for owner UAT (2026-08-04, supersedes APP-V3.6.1)

  app-v3.6.2.html   md5 c7f955d4aacdeaaca9a44e4314f2b14e · 634,591 B
  (arrived base64-wrapped: decoded and md5-verified byte-exact against the builder's
   MANIFEST package 10 — zero transit junk. APPROVED FOR UAT by auditor 2026-08-04.)
  What v3.6.2 adds vs v3.6.1 (auditor diff: nothing else changed — version bump + CSS
  for country tree + the scope panel only; ingest/migration/hold code byte-identical):
    D1  league-level clear: each country expands to its competitions; you can open,
        preview, MUTE or PURGE ONE competition (e.g. MOL Cup) or the WHOLE country.
    D3  alphabetical everywhere: countries A–Z, competitions inside a country A–Z,
        remove/keep club lists A–Z. (Your ask: easy type-select.)
    D2  (already in v3.6.1) preview shows the FULL match list, no 400-row cap.
  Versioning note: my workorder called this delta "v3.6.1", builder correctly shipped
  it as v3.6.2 because v3.6.1 was already sealed. No conflict — name is cosmetic.

SEALED BASELINE unchanged: app-v3.5.2.html md5 6bd76ae0… (untouched, still the rollback).
You may SKIP the v3.6.1 UAT — v3.6.2 is a strict superset; run everything here.

=====================================================================================
UAT — Data tab → "Country packs" → run gates IN ORDER (G1→G13). Report gate numbers.

  G1  Panel list now shows 18 country scopes, A–Z (Albania 1 · Canada 4 · Cyprus 1 ·
      Czech Republic 632 · … · Russia 644 · Scotland 34 · … · United States 81).
      Note: 18, not 16 — my earlier "16" memo was loose; tiny scopes are single
      European away-legs/friendlies. All 1,432 rows accounted for (auditor-verified).
  G2  Russia row: 644 matches · 4 competitions · 26 clubs; expand it → competitions
      listed A–Z EXACTLY: Russian Cup 152 · Russian Premier League 489 ·
      Russian Relegation Playoffs 2 · Russian Super Cup 1   (this is G13)
  G3  Open whole country (Russia) → preview shows breakdown + FULL scrollable list
      of all 644 rows (no cap) + remove/keep club lists A–Z.
  G4  Purge button stays DISABLED until you click "Download backup" and the
      .json actually lands in your downloads folder (name ends -pre-purge-russia.json)
  G5  MUTE Russia → engine counts drop the 644 · UNMUTE → identical counts back.
  G6  PURGE Russia → Coverage 1,432 − 644 = 788 · log shows scope-purge + backup name.
  G7  Load the downloaded backup .json (migration) → store back to EXACTLY 1,432.
      (This is the undo proof and the purge+restore rehearsal for the Russia endgame.)
  G8  NEW D1 gate — open Czech Republic → open "MOL Cup" only (not the country):
      preview = 63 matches · confirm screen says "Czech Republic / MOL Cup" ·
      download ITS backup (name ends -pre-purge-czech-republic-mol-cup.json;
      a country backup does NOT enable a league purge — each scope needs its own) ·
      PURGE → Coverage 1,432 − 63 = 1,369 · Czech First League (561) and playoffs (8)
      untouched and still visible in Coverage.
  G9  Load that MOL Cup backup → back to EXACTLY 1,432.
  G10 Alphabetical spot-check: country list reads A–Z top to bottom; inside Russia
      the 4 competitions read A–Z; the removed/kept club lists in any preview A–Z.
  G11 (optional add-path rehearsal) drop RPL pack c3a72b35 → +732 → 1,520, zero skips;
      drop again → all "Skipped duplicate", totals unchanged.
  G12 Log tab: one scope-mute/scope-purge line per operation with pre/post snapshots;
      purge lines carry country AND competition fields + backup filename.
  G13 (merged into G2) — competition order check.

TEST DISCIPLINE: G1–G7 first (store-safe or provably restored), then G8–G9, then G10+.
If any gate fails: STOP, tell me gate number + what you saw + Coverage numbers.
Do NOT import any staged data pack during UAT (D14 — everything stays frozen until
the researcher's complete packs are in and audited).
=====================================================================================
Audit trail: AUDIT-APP-V3.6.2-2026-08-04.md (md5 pins, diff stats, harness 32/32).
