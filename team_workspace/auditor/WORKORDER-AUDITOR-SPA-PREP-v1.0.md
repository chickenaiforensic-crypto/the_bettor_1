# WORK ORDER — Auditor: SPA Verification Preparation

**Document ID:** WORKORDER-AUDITOR-SPA-PREP-v1.0  
**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**To:** Auditor  
**Branch:** main (PR #3 merged)  
**Priority:** MEDIUM — Prepare while researcher collects data  

---

## ⚠️ READ THIS FIRST

You are the ONLY person allowed to say "this is true." Fresh code, always. Never reuse previous auditor's scripts as evidence.

The SPA pack is being collected by a researcher. While they work, you prepare your audit scripts so that when the pack arrives, you can verify it immediately.

**Reference:** Read `team_workspace/auditor/WORKORDER-AUDITOR-MASTER-v1.md` for the full auditor protocol.

---

## 0. MANDATORY PRE-WORK

### 0.1 Confirmation

```
I, [Auditor Name], confirm I have read:
[ ] START-HERE-COLD-START.md
[ ] COMMUNICATION-RULES-v1.md
[ ] ROLE-AUDITOR.md
[ ] WORKORDER-AUDITOR-MASTER-v1.md

Signature: _______________
Date: _______________
```

### 0.2 The "Never" List for Auditors

- [ ] Reuse previous auditor's scripts as evidence (fresh code only)
- [ ] Trust a file without hashing it first
- [ ] Assume — if not confirmed, it's not known
- [ ] Guess — no inferences as facts
- [ ] Silent-rewrite instrument errors
- [ ] Accept "registered" self-reports as evidence

---

## 1. YOUR TASK

Prepare fresh verification scripts for SPA pack verification. The scripts must be ready to run the moment the pack arrives.

### What You Need to Prepare

#### 1.1 SPA Pack Parser (`spain_parse.py` or `spain_audit.py`)

Fresh code to parse BP-TEAM-PACK v2 format for SPA:
- Parse MATCH lines: `MATCH|date|competition|compType|home|hg|ag|away|venue|stadium|city|country||sourceLabel`
- Parse TEAM lines (if present): `TEAM|name|country||leagueCode|...`
- Parse SOURCE lines: `SOURCE|label|URL|accessed|type|description`
- Parse NOTE lines: `NOTE|level|tag|text`
- Handle the SPA roster (20 clubs, specific name variants)
- Output: parsed rows with field validation

#### 1.2 SPA Table Reproduction Script (`spain_table_repro.py` or part of combined script)

Fresh code to recompute standings from rows:
- For each season (2021-22 through 2025-26):
  - Compute P, W, D, L, GF, GA, GD, Pts for each team
  - Sort by Points DESC, GD DESC, GF DESC
  - Compare against official RSSSF table
- Must detect ALL discrepancies (club-for-club, position, W-D-L, GF-GA, Pts)
- Output: season-by-season comparison report

#### 1.3 SPA Boundary Scanner (`spain_boundary.py` or part of combined script)

Fresh code to check:
- Dateless rows
- Duplicate fingerprints (date+home+away+competition)
- Future-dated rows (after 2026-08-06)
- Non-integer scores
- Scores > 30
- Missing required fields

#### 1.4 SPA Identity Checker (`spain_identity.py` or part of combined script)

Fresh code to verify:
- Every home/away name matches SPA roster verbatim
- Flag any name variants (e.g., "Real Madrid CF" vs "Real Madrid")
- Flag any teams not in the 20-club roster

**SPA Roster (20 clubs):**
```
Alaves, Almeria, Ath Bilbao, Ath Madrid, Barcelona, Betis, Cadiz, Celta, Elche, Espanol, Getafe, Girona, Granada, Las Palmas, Leganes, Levante, Mallorca, Osasuna, Oviedo, Real Madrid, Sevilla, Sociedad, Valencia, Valladolid, Vallecano, Villarreal
```

**Name Variant Detection — flag these:**
- "Real Madrid CF" → should be "Real Madrid"
- "Athletic Bilbao" → should be "Ath Bilbao"
- "Atletico Madrid" → should be "Ath Madrid"
- "Rayo Vallecano" → should be "Vallecano"
- "Real Sociedad" → should be "Sociedad"
- "Real Betis" → should be "Betis"
- "Valencia CF" → should be "Valencia"
- Any other variant not on the roster

#### 1.5 SPA Sentinel Date Scanner (`spain_sentinel.py` or part of combined script)

Fresh code to detect:
- Rows dumped on suspicious dates (e.g., 20YY-06-30 patterns)
- Multiple rows sharing identical dates in suspicious patterns

#### 1.6 SPA Source Verifier (`spain_source.py` or part of combined script)

Fresh code to check:
- Every MATCH row has a valid sourceLabel
- Every sourceLabel matches a SOURCE line
- SOURCE lines have valid URL, access date, type, description
- Primary source = RSSSF for all rows

---

## 2. SPA SOURCE URLs

**Primary (RSSSF):**
```
https://www.rsssf.org/tabless/span2022.html  (2021-22 season)
https://www.rsssf.org/tabless/span2023.html  (2022-23 season)
https://www.rsssf.org/tabless/span2024.html  (2023-24 season)
https://www.rsssf.org/tabless/span2025.html  (2024-25 season)
https://www.rsssf.org/tabless/span2026.html  (2025-26 season)
```

**Second Index (cross-verification):**
```
https://www.worldfootball.net/season/esp-laliga-2022/
https://int.soccerway.com/season/spain-la-liga-2021-2022/
```

---

## 3. SPA TABLE REPRODUCTION EXPECTATIONS

For EACH season, you must verify:
- 20 clubs
- 380 matches
- Final table: club-for-club, position-order, W-D-L, GF-GA, Pts — ALL EXACT

**Zero tolerance.** If ANY club is in the wrong position, or ANY stat differs, the gate FAILS.

---

## 4. SPA ACCEPTANCE GATES (When Pack Arrives)

When the researcher delivers `SPA-2021-2026_BP-TEAM-PACK_v2.txt`, you run:

| Gate | Test | Fail Action |
|---|---|---|
| **G1: Grammar** | Every row matches BP-TEAM-PACK v2 format | Return with format errors |
| **G2: Boundary** | No dateless/duplicate/future rows | Return with row numbers |
| **G3: Identity** | Every name matches roster verbatim | Return with violations |
| **G4: Source** | Every row has SOURCE line; RSSSF primary + second index | Return rows lacking sources |
| **G5: Table reproduction** | 5 seasons × 20 clubs = 100 club-positions, ALL EXACT | Return with diffs |
| **G6: Shape** | 380 rows per season, every club 38 matches | Return with count diffs |
| **G7: 90-min doctrine** | No ET/pen scores in league matches | Return with violations |
| **G8: Continuity** | Span gap-free | Return with gap list |

**If ALL gates pass:**
- Issue ONE approval card
- Card must include: pack ID, row count, verification method, date, auditor name

**If ANY gate fails:**
- Return to researcher with EXACT defect list
- Include: gate Failed, specific rows/values, expected vs actual
- Do NOT approve partially

---

## 5. DELIVERABLE

Location: `audit_work/`

Deliver fresh scripts:
- `spain_parse.py` — SPA pack parser
- `spain_table_repro.py` — SPA table reproduction
- `spain_boundary.py` — SPA boundary check
- `spain_identity.py` — SPA identity verification
- `spain_sentinel.py` — SPA sentinel date detection
- `spain_source.py` — SPA source verification

OR one combined script: `spain_audit.py`

Each script must be:
- Freshly written (not copied from previous auditor)
- Documented with what it verifies and how
- Re-runnable by anyone

---

## 6. WHEN THE SPA PACK ARRIVES

1. Hash the pack on arrival (md5 + sha256)
2. Compare against any declared pin
3. Run your fresh parser
4. Run all verification scripts
5. Compare against RSSSF tables
6. Issue approval card OR return with defects
7. Log everything in `Supervior/updates/SESSION-*.md`

---

## 7. COMPLIANCE ACKNOWLEDGMENT

```
I, [Auditor Name], acknowledge:

1. I will use FRESH CODE for all verification (not previous auditor's scripts as evidence)
2. I will HASH every file on arrival before processing
3. I will perform TABLE REPRODUCTION for EVERY season
4. I will scan for SENTINEL DATES and GHOST CLUBS
5. I will document EVERY finding with specific row numbers and values
6. I will NOT approve any pack that fails any gate

Auditor signature: _______________
Date: _______________
```

---

*End of WORKORDER-AUDITOR-SPA-PREP-v1.0*
*This workorder is binding.*
