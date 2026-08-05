PITCH RATING — FINAL DELIVERY (2026-08-02) — base64-.txt drill
===============================================================

WHY THIS DRILL
  The CDN appends a Cloudflare block to every raw .html it serves (proven twice
  by md5 strip-and-match). So the app is delivered ONLY as base64 text. Decode
  it yourself; verify the md5; never trust a raw .html download.

FILES IN THIS FOLDER — see MANIFEST.txt for the authoritative list + md5s
  app-v3.1.0-dad4babd.b64.txt   base64 of app-v3.1.html (589,195 B)
  ZONES-v3.4.0.b64.txt          base64 of trail/ZONES.md (v3.4.0 state)
  R1-R5-corrections.b64.txt     base64 of gate-evidence/R1-R5-corrections.md
  DELIVERY-README.txt           this file
  (gate-evidence/R6-R7.md is the plain-text evidence for this final list)

HOW TO DECODE + VERIFY (macOS / Linux)
  base64 -d app-v3.1.0-dad4babd.b64.txt > app-v3.1.html
  md5sum app-v3.1.html
  # expect: dad4babde375f0b302d0f9ecee9dbc1b

WINDOWS (PowerShell)
  [IO.File]::WriteAllBytes("app-v3.1.html",
    [Convert]::FromBase64String((Get-Content app-v3.1.0-dad4babd.b64.txt -Raw)))

STRIP-AND-MATCH (if a download looks wrong)
  If a raw .html's md5 does not match, the CDN appended a Cloudflare block.
  Strip everything after the closing </html> line, re-hash, and it matches.

FINAL FILE FACTS
  File            app-v3.1.html
  Version         v3.4.0  (badge + footer, unique per ship)
  md5             dad4babde375f0b302d0f9ecee9dbc1b
  Bytes           589,191
  Store           1,436 matches · 539 identities · 3 mutes (reasons IA-01/02/03)
  Suites          new-app 48/48 · R8 (D12) 13/13 · evidence parity 7/7 · legacy 156/156 · CF grep 0
  Fitted cards    18 legacy-fit leagues + RPL + CZ1 (replay-validated, provenance on card)
