APP-V3.6.0/ — auditor-verified build for owner UAT (2026-08-04)

  app-v3.6.0.html   md5 edf52d78b2fa1690721aa3a72018b634 · 630,363 B
  (byte-exact the builder's pinned source; the copy that travelled here carried
   an extra 1,290-byte Cloudflare tracking script injected mid-transit — stripped
   and proven by md5 match. Use THIS file, not a re-download.)

SEALED BASELINE unchanged: app-v3.5.2.html md5 6bd76ae0… (untouched, still the rollback).

UAT — Data tab → "Country packs" → run §5 gates IN ORDER (G1→G12):
  G1  panel shows Russia 644 (489/152/2/1, 26 clubs) · Czech Republic 632 (561/63/8, 45)
  G2  preview: full breakdown, remove vs kept club lists, attached counts
  G3  purge button disabled until the backup .json auto-downloads
  G4  MUTE Russia → counts held out · UNMUTE → identical counts back
  G5  PURGE Russia → Coverage 1,432-644 = 788, log shows scope-purge + backup name
  G6  load the downloaded backup json → store back to exactly 1,432 (undo proof)
  G7  (only if you choose to test the add path) drop RPL pack c3a72b35 → +732 → 1,520, zero skips
  G8  Czech preview: 632 with 561/63/8, 45 clubs, keep-list rendered
  G9  drop the same pack twice → second drop = all "Skipped duplicate", totals unchanged
  G10 no per-country coding (auditor-grepped, clean)
  G11 engine boots clean after purge/replace, no console errors
  G12 log/snapshot entries written for every operation

TEST DISCIPLINE: do G1-G6 first (they leave the store intact or provably restored).
If any gate fails: STOP, tell me gate number + what you saw + Coverage numbers.

KNOWN RETURN ITEMS (auditor, to builder — v3.6.1 delta):
  R1  league-level clear selection (G2-L: e.g. purge only "MOL Cup") — built file does
      country level only (workorder amendment arrived after build start). Not blocking:
      every no-mix flow we have clears WHOLE countries.
  R2  preview row list shows first 400 rows (Russia=644) — counts are exact, list is
      visually capped. Nit, same delta.
