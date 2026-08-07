# Researcher3 supporting ledgers

- `parse_mls.py` — RSSSF GitHub-mirror parser used for the MLS partial pack. Validates
  W-D-L/GF-GA against the final standings (0 mismatches 2021-2024).
- `mls_parsed_2021_2025.json` — machine-readable rows emitted by the parser
  (2021-2024 full; 2025 playoff-only because the RSSSF mirror's usa2025.txt has no
  regular-season matchdays yet).
- The USOC pack (`../USOC-2021-2026_BP-TEAM-PACK_v2.txt`) was assembled by hand from
  RSSSF (R16-onwards) + second-index R32 rounds; self-checked with the repo's
  `audit_work/pack_parse.py`.
