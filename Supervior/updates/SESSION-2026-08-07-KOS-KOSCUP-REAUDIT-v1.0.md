# SESSION — 2026-08-07 KOS/KOSCUP RE-AUDIT (v2.1)

**Branch:** arena/019fd805-the-bettor-1
**Actors:** Researcher (corrections + fresh gates); Director (instructions); Independent auditor (verification still pending)

---

## 1. Director instruction (2026-08-07)

Both v2.0 packs (commit `f9700e6`, which fixed the auditor's D1–D4 identity defects in KOSCUP) were BLOCKED from import for three reasons:
1. KOS excluded 12 "already-held" 2025-26 rows that are not in the current 5,082-row store (which has zero Kosovo rows) → return a complete standalone pack: **900 + 10 = 910 rows**.
2. Replace every placeholder match venue (KOS 6 playoff rows; KOSCUP 39 stadium rows + 1 city row) — no unknown/blank/Stadium/City placeholders.
3. Transfer formal audit artifacts to the branch after the corrected packs exist.

## 2. Work performed (2026-08-07)

1. **Venue research (≈20 sources searched/fetched):** Wikipedia season articles (2021-22..2025-26 Superleague + 2022-23..2025-26 Kosovar Cup), Wikipedia club pages and List of football stadiums in Kosovo, transfermarkt, soccerway, footballgroundmap, mackolik, and Kosovar press (koha.net, Telegrafi, mesazhi.com, TopSporti, ATV). Resolved venues for all 6 playoff rows and all but one KOSCUP home club. Notable finds: 2022-23 final at Zahir Pajaziti Stadium (Wikipedia + mackolik; Grokipedia's "Ismet Paçarizi, Ferizaj" rejected as unsupported); 2024-25 semi at 18 June Stadium Klina and final at Fadil Vokrri Stadium (Wikipedia/mesazhi); 2023-24 final at 18 June Stadium Klina (Telegrafi); Rahoveci–Drita R16 2024-25 actually played in Gjilan (Wikipedia footnote).
2. **KOS v2.1 built:** all 900 league rows (12 former appendix rows re-included; verified against the worldfootball carrier + Wikipedia matrix), 10 playoff rows with real venues, TEAM-row venues completed (Vushtrria → Ferki Aliu Stadium; Dinamo Ferizaj → Ferizaj Synthetic Grass Stadium), pack NOTES updated (appendix_included, venue_source, playoff_venues).
3. **KOSCUP v2.1 built:** 123 slice ties, all venues real; only residual = TOP Football (venue unpublished anywhere; blocker NOTE + descriptive "TOP Football Sports Field, Prishtine" for auditor confirmation); D1–D4 fixes retained.
4. **Fresh gates:** `audit_work/kos_koscup_reaudit_2026-08-07-v1.0/gates_v21.py` — **ALL GATES PASSED** (see report AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md for full output).
5. **Hashes pinned** (in the audit report). Hashes were recomputed after the final rebuild that aligned TEAM rows to the 13-field adopted reference layout (`TEAM|name|country|league|code|aliases|logoURL|city|country|stadium|capacity|unknown|unknown`); the gate script was rerun on the rebuilt packs and passed.

## 3. Files created/changed

| File | Purpose |
|---|---|
| `handoffs/KOS-2021-2026_BP-TEAM-PACK_v2.1.txt` | Corrected KOS pack (910 MATCH rows) |
| `handoffs/KOSCUP-2021-2026_BP-TEAM-PACK_v2.1.txt` | Corrected KOSCUP pack (123 ties) |
| `Supervior/Build Docs/AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md` | Audit report (hashes, gates, residuals) |
| `Supervior/updates/SESSION-2026-08-07-KOS-KOSCUP-REAUDIT-v1.0.md` | This session log |
| `audit_work/kos_koscup_reaudit_2026-08-07-v1.0/gates_v21.py` | Fresh gate script (independent of builder) |
| `team_workspace/researcher_handoffs/kos_ledgers/build_packs_v21.py` | v2.1 builder (venue maps + 900-row KOS) |

## 4. Open items (for the independent auditor)

1. TOP Football home venue — confirm/correct from match-day records.
2. 2023-24 playoff SF venue (inferred 18 June Stadium, Kline) — confirm.
3. 2024-25 playoff SF date (RSSSF 25 May kept; Wikipedia 24 May) — confirm.
4. 2025-26 MD12 award (Prishtina E Re 3-0 Drenica) — confirmed by official table, diverges from the Wikipedia matrix print.
5. Sample spot-verify of lower-division grounds.

## 5. Status

- KOS v2.1 and KOSCUP v2.1 delivered; fresh gates PASS; hashes pinned.
- **Not imported.** Import requires the independent auditor's verification card (Director instruction: "Do not import either pack before this correction and fresh auditor verification").
