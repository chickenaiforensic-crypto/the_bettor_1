# WORK ORDER — Germany Bundesliga 5-Year-Span 2021-2026 (RIGOROUS v1)

**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**Status:** STAGED — Queue Position 15  
**Researcher:** [TO BE ASSIGNED]  
**Format:** ONE `BP-TEAM-PACK v2` text file (`.txt` — never zip, never paste fragments)  

---

## ⚠️ READ THIS FIRST

This is a RIGOROUS workorder. It leaves NO room for falsification, guessing, or Unaudited data. Every section is mandatory.

**History:** Previous audits found fabricated data in KOS (ghost clubs, sentinel dates) and UEFA-FULL (fake scores including PSG 4-3 Arsenal when actual was 1-1, 4-3 pens). This workorder is designed to prevent ANY falsification.

---

## 0. MANDATORY PRE-WORK

### 0.1 Confirmation of Reading

```
I, [Researcher Name], confirm I have read this ENTIRE workorder before starting.
Signature: _______________
Date: _______________
```

### 0.2 Federation Check — GERMANY BUNDESLIGA

**Competition:** Germany Bundesliga (German top division)  
**Country:** Germany  
**Before collecting ANY rows:** Scan your first 10 rows. Every club must be on the §3 roster. If ANY club is not German Bundesliga → WRONG COMPETITION → STOP.

### 0.3 The "Never" List — You Must NEVER:

- [ ] Invent a team name, score, or date
- [ ] Use bookmaker odds or market data (P1 violation)
- [ ] Deliver standings tables (rows only)
- [ ] Use .zip files (text files only)
- [ ] Guess at unverifiable data (write `NOTE|warning|blocker` instead)
- [ ] Skip the table reproduction test (§5.5)
- [ ] Skip the cross-verification step (§4.2)

---

## 1. SCOPE DEFINITION

### 1.1 Competition

```
Competition: Germany Bundesliga
Federation: Germany
Competition string (verbatim): Germany Bundesliga
CompType: domestic-league
```

### 1.2 Seasons — GERMANY DIFFERS: 18 TEAMS, 34 MATCHDAYS

| Season | Teams | Matches per team | Total matches |
|---|---|---|---|
| 2021-22 | 18 | 34 | 306 |
| 2022-23 | 18 | 34 | 306 |
| 2023-24 | 18 | 34 | 306 |
| 2024-25 | 18 | 34 | 306 |
| 2025-26 | 18 | 34 | 306 |
| **TOTAL** | | | **1,530** |

**Plus:** 2026-27 through your return date (state last round/date in a NOTE).

### 1.3 What IS in Scope

- All regular-season Bundesliga matches, 2021-22 through 2025-26

### 1.4 What IS NOT in Scope

- DFB-Pokal (German Cup)
- European matches
- 2. Bundesliga or lower divisions

---

## 2. GRAMMAR — BP-TEAM-PACK v2 (STRICT)

### 2.1 Match Row Format

```
MATCH|<dateISO>|Germany Bundesliga|domestic-league|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|Germany||<sourceLabel>
```

### 2.2 Field Requirements

| Field | Requirement |
|---|---|
| `<dateISO>` | YYYY-MM-DD, actual match date |
| `<competition>` | Exactly `Germany Bundesliga` |
| `<compType>` | Exactly `domestic-league` |
| `<home>` | Roster string verbatim (§3) |
| `<hg>` | Integer 0-30, actual home goals |
| `<ag>` | Integer 0-30, actual away goals |
| `<away>` | Roster string verbatim (§3) |
| `<venue>` | Round number: `MD1` through `MD34` (NOT MD38!) |
| `<stadium>` | Stadium name from source |
| `<city>` | City |
| `<country>` | Exactly `Germany` |
| `<sourceLabel>` | Must match a SOURCE label |

### 2.3 Critical: Germany Has 34 Matchdays, Not 38

```
[REQUIRED] Every row's venue field must be MD1 through MD34
[REQUIRED] Do NOT use MD35-MD38 for Bundesliga (those don't exist)
[REQUIRED] Row count per season = 306 (18 teams × 34 matches / 2)
```

### 2.4 90-Minute Doctrine

- League matches = full-time 90-minute score
- NO extra time or penalty scores in league matches

### 2.5 File Termination

File MUST end with `END`. No standings tables.

---

## 3. IDENTITY DISCIPLINE — USE VERBATIM

### 3.1 Roster Strings

```
[TO BE FILLED FROM WORKORDER — EXAMPLE FORMAT]
Borussia Dortmund
Bayern Munich
RB Leipzig
...
```

**Researcher must verify exact roster strings from the workorder §3 before starting.**

### 3.2 Rename/Spelling Traps

```
[TO BE SPECIFIED IN WORKORDER — Common traps:]
- "Borussia Mönchengladbach" → check roster for exact form
- "Wolfsburg" → check roster for exact form
- "Schalke 04" → check roster for exact form
```

### 3.3 Prohibited Actions

- [ ] Do NOT create name variants
- [ ] Do NOT add clubs not on the roster

---

## 4. SOURCE HIERARCHY + VERIFICATION (NON-NEGOTIABLE)

### 4.1 Primary Source: RSSSF

```
Primary URL pattern: https://www.rsssf.org/tablesg/ger<YEAR>.html
Examples:
  2021-22: https://www.rsssf.org/tablesg/ger2022.html
  2022-23: https://www.rsssf.org/tablesg/ger2023.html
  2023-24: https://www.rsssf.org/tablesg/ger2024.html
  2024-25: https://www.rsssf.org/tablesg/ger2025.html
  2025-26: https://www.rsssf.org/tablesg/ger2026.html
```

### 4.2 Second-Index Cross-Verification (MANDATORY)

```
Options:
- worldfootball.net: https://www.worldfootball.net/season/ger-bundesliga-2022/
- soccerway.com: https://int.soccerway.com/season/germany-bundesliga-2021-2022/
```

**Procedure:** Cross-verify EVERY round. If ANY difference → resolve to RSSSF + write `NOTE|warning|source_conflict`.

### 4.3 SOURCE Lines Required

```
SOURCE|<label>|<URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>
```

---

## 5. ACCEPTANCE GATES (FAILING ANY = RETURNED INCOMPLETE)

### Gate G1: Grammar Check
```
[ ] Every row matches format exactly
[ ] Competition string = "Germany Bundesliga" everywhere
[ ] compType = "domestic-league" everywhere
[ ] venue field = MD1 through MD34 (NOT MD35-38!)
[ ] File ends with END, no standings tables
```

### Gate G2: Boundary Check
```
[ ] No dateless rows, no duplicates, no future dates
[ ] No scores > 30, no non-integer scores
```

### Gate G3: Identity Check
```
[ ] Every home/away string matches §3 roster verbatim
[ ] Zero name variants
```

### Gate G4: Source Check
```
[ ] Every row has valid sourceLabel matching a SOURCE line
[ ] Primary = RSSSF, second-index cross-verify done for every round
```

### Gate G5: Table Reproduction Test (ZERO TOLERANCE)

```
[ ] For EACH season, recompute final table from rows ONLY
[ ] Must match official table: club-for-club, position-order, W-D-L, GF-GA, pts
[ ] All 18 club-positions must be EXACT per season
```

### Gate G6: Shape Check
```
[ ] Row counts per season = 306 (NOT 380!)
[ ] Every club's match count = 34 per season
```

### Gate G7: Continuity Check
```
[ ] Span gap-free, any missing match = written gap defect
```

---

## 6. SELF-CHECK CHECKLIST

```
Total rows: ______ (expected: 1,530 for 5 seasons)
Per season: 2021-22: ___ / 2022-23: ___ / 2023-24: ___ / 2024-25: ___ / 2025-26: ___
Match expected: YES / NO

Duplicates: ___ (must be 0)
Future-dated: ___ (must be 0)
Non-integer scores: ___ (must be 0)

Table reproduction:
  2021-22: PASS / FAIL (18 clubs)
  2022-23: PASS / FAIL (18 clubs)
  2023-24: PASS / FAIL (18 clubs)
  2024-25: PASS / FAIL (18 clubs)
  2025-26: PASS / FAIL (18 clubs)
```

---

## 7. RETURN PROTOCOL

```
Filename: GER-2021-2026_BP-TEAM-PACK_v2.txt
Location: [repo]/handoffs/
```

---

## 8. COMPLIANCE ACKNOWLEDGMENT

```
I, [Researcher Name], acknowledge:

1. I have read this ENTIRE workorder
2. I will NEVER invent teams, scores, or dates
3. I will NEVER use market data (P1 violation)
4. I will perform table reproduction for EVERY season
5. I will cross-verify EVERY round against a second index
6. I understand Germany has 18 teams × 34 matches = 306 rows/season (NOT 380)
7. I understand my file will be independently verified by the auditor

Researcher signature: _______________
Date: _______________
```

---

*End of WORKORDER-GER-2021-2026_RIGOROUS-v1*
