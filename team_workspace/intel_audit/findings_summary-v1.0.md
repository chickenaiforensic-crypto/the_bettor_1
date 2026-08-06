# FINDINGS SUMMARY — Quick Reference

**Audit:** external-audit-019fd4fb-2026-08-06  
**Date:** 2026-08-06  

---

## AT A GLANCE

| Category | Count | Action |
|---|---|---|
| ✅ VERIFIED (adoptable) | 8 packs, 11,191 rows | Import to store |
| 🚫 REJECTED (do not use) | 3 packs | Discard |
| 🔄 IN FLIGHT | 1 pack (SPA) | Complete pending |
| 📋 QUEUED (awaiting delivery) | 10 packs | Wait |

---

## ✅ VERIFIED PACKS

| League | Rows | Verification |
|---|---|---|
| EPL | 1,900 | 1,900/1,900 exact vs RSSSF + football-data |
| RPL | 1,220 | 1,220/1,220 exact vs RSSSF + legacy feed |
| RUSCUP | 341 | 341/341 correct (3 RSSSF date misprints adjudicated) |
| CZ1 | 1,401 | 1,390 exact + 11 date fixes (D-1) |
| MOLCUP | 202 (FULLSPAN) | R16→Final exact; R2/R3 wiki-sourced |
| RUS-ADDENDUM | 18 | 18/18 correct |
| SCO1 | (table repro) | 12/12 clubs exact vs RSSSF post-split |
| MLS | 30/30 | Prior auditor verified; 2021 finals spot-checked |

---

## 🚫 REJECTED PACKS

### KOS (Kosovo Superleague)
- **Ghost clubs:** Ferizaj, Suhareka — not in 2023-24 Superliga
- **Table reproduction:** 0/10 vs RSSSF
- **Sentinel dates:** All 180 rows on 2 dates (2023-06-30, 2024-06-30)
- **Provenance:** Mislabeled `rsssf-kos`

### UEFA-FULL
- **Sentinel dates:** 100% of main-stage rows (2,762/2,764)
- **Fake scores:** PSG 4-3 Arsenal (actual: 1-1, 4-3 pens), City–Madrid leg2 mirrored, PSG 5-2 Chelsea invented
- **Missing rounds:** 2023-24 Dortmund–PSG semifinal, UECL 2021-22 playoff (16 matches)
- **Venues:** 2,762/2,764 placeholders
- **TEAM roster:** 5 ghost ClubA ids, invented "1. FC Union Santo André"

### UEFA-CONNECTOR
- **"Dates fixed" claim:** FALSE — 1,388/1,390 still sentinel-dated
- **Country field:** Copy-garbage

---

## 🔄 SPA (IN FLIGHT)

- **Parser:** FIXED — gate-green ×4
- **Second index:** Done
- **Venue lattice:** Done
- **Ledgers:** PENDING
- **Pack completion:** PENDING

---

## 📋 QUEUED (10 PACKS)

ITA, GER, FRA, SCO1, SCOCUP, SCOLC, MLS, USOC, KOS (halted), KOSCUP (halted), UEFA-CONNECTOR (halted)

---

## STORE STATUS

| Metric | Current | Target |
|---|---|---|
| Total rows | 5,000 | 5,082 |
| Missing | 82 (MOLCUP FULLSPAN) | D-2 fix pending |

**WARNING:** Do NOT use stale 16,629-row store — contains 436 fabricated UEFA rows.

---

*For full details, see `external-audit-2026-08-06.md`*
