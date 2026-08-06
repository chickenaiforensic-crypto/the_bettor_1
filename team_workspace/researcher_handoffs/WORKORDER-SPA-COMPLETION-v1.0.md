# WORK ORDER — Spain La Liga Completion (researcher)

**Document ID:** WORKORDER-SPA-COMPLETION-v1.0  
**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**To:** Researcher (SPA — in flight)  
**Branch:** main (PR #3 merged)  
**Priority:** HIGH — in flight, needs completion  

---

## ⚠️ READ THIS FIRST — RIGOROUS STANDARDS

This workorder requires you to follow the **rigorous researcher protocol** defined in `team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.md`. That document is the master template. **Read it in full before starting.**

You are continuing work that was already started. The parser is fixed. The ledgers are partially done. You need to complete the pack to the SAME rigorous standard as every other pack.

**The engine is now LIVE on main (PR #3 merged, commit eaeddb2).** The app can be used. Your data will be loaded into it.

---

## 0. MANDATORY PRE-WORK

### 0.1 Read These Documents in Full

| # | Document | Location |
|---|---|---|
| 1 | `COMMUNICATION-RULES-v1.md` | repo root |
| 2 | `START-HERE-COLD-START.md` | repo root |
| 3 | `README.md` | repo root |
| 4 | `team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.md` | **MASTER TEMPLATE — read this first** |
| 5 | `team_workspace/director/PHASE-TASKLIST-v1.0.md` | Understand the phase you're in |

### 0.2 Confirmation

```
I, [Researcher Name], confirm I have read:
[ ] COMMUNICATION-RULES-v1.md
[ ] START-HERE-COLD-START.md
[ ] README.md
[ ] WORKORDER-RESEARCHER-MASTER-v1.md (MASTER TEMPLATE)
[ ] PHASE-TASKLIST-v1.0.md

I understand the five rules that never change.
I understand the "never" list for researchers.
I understand every gate I must pass.

Signature: _______________
Date: _______________
```

### 0.3 The "Never" List — You Must NEVER:

- [ ] Invent a team name, score, or date
- [ ] Use bookmaker odds or market data (P1 violation — permanent exclusion)
- [ ] Deliver standings tables (rows only; tables are recompute targets)
- [ ] Use .zip files (text files only)
- [ ] Paste fragments (one complete file per workorder)
- [ ] Guess at unverifiable data (write `NOTE|warning|blocker` instead)
- [ ] Skip the table reproduction test (§5.6 below)
- [ ] Skip the cross-verification step (§4.2)

---

## 1. YOUR MISSION

### 1.1 What You're Completing

```
Competition: Spain La Liga
Federation: Spain
File to deliver: SPA-2021-2026_BP-TEAM-PACK_v2.txt
Location: handoffs/ folder
Total rows: 1,900 (5 seasons × 380)
Status: IN FLIGHT — parser fixed, ledgers + pack remaining
```

### 1.2 What Was Already Done

| Component | Status |
|---|---|
| RSSSF primary parser | FIXED — gate-green ×4 |
| Second index cross-verification | DONE |
| Venue lattice | DONE |
| Ledgers | PARTIALLY DONE — YOU COMPLETE THEM |
| Pack | NOT DONE — YOU COMPLETE IT |

### 1.3 Your Deliverable

One text file: `SPA-2021-2026_BP-TEAM-PACK_v2.txt`

Contains:
- NOTE|info|catalog line declaring "Spain La Liga"
- SOURCE lines for every source used
- NOTE lines for every name_rename, source_conflict, quirk
- NOTE|info|spot_audit lines for one matchday per season
- MATCH lines for every match (1,900 total)
- END line at file end

**No standings tables. No .zip. No paste fragments.**

---

## 2. SCOPE DEFINITION

### 2.1 Competition

```
Competition string (verbatim): Spain La Liga
compType: domestic-league
Country: Spain
```

### 2.2 Seasons

| Season | Clubs | Matches per club | Total matches |
|---|---|---|---|
| 2021-22 | 20 | 38 | 380 |
| 2022-23 | 20 | 38 | 380 |
| 2023-24 | 20 | 38 | 380 |
| 2024-25 | 20 | 38 | 380 |
| 2025-26 | 20 | 38 | 380 |
| **TOTAL** | | | **1,900** |

### 2.3 What IS in Scope

- All regular-season La Liga matches, 2021-22 through 2025-26
- Every match: date, home team, away team, home goals, away goals

### 2.4 What IS NOT in Scope

- Copa del Rey (Spanish Cup)
- European matches
- Segunda División

---

## 3. GRAMMAR — BP-TEAM-PACK v2 (STRICT)

### 3.1 Match Row Format

Every row MUST be exactly:

```
MATCH|<dateISO>|Spain La Liga|domestic-league|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|Spain||<sourceLabel>
```

### 3.2 Field Requirements

| Field | Requirement | Verification |
|---|---|---|
| `<dateISO>` | YYYY-MM-DD, actual match date | Must match RSSSF date exactly |
| `<competition>` | Must be exactly `Spain La Liga` | Case-sensitive |
| `<compType>` | Must be exactly `domestic-league` | Not "cup", not "other" |
| `<home>` | Roster string verbatim (§3.3) | No variants allowed |
| `<hg>` | Integer 0-30, actual home goals | Must match RSSSF score |
| `<ag>` | Integer 0-30, actual away goals | Must match RSSSF score |
| `<away>` | Roster string verbatim (§3.3) | No variants allowed |
| `<venue>` | Round number: `MD1` through `MD38` | Matchday must be correct |
| `<stadium>` | Stadium name from source | Must be real stadium |
| `<city>` | City | Must be real city |
| `<country>` | Must be exactly `Spain` | Case-sensitive |
| `<sourceLabel>` | Must match a SOURCE label in §4 | Every row needs source |

### 3.3 Identity Discipline — Use Roster Strings VERBATIM

Every 2021-26 La Liga club uses these EXACT strings. No variants:

```
Alaves
Almeria
Ath Bilbao
Ath Madrid
Barcelona
Betis
Cadiz
Celta
Elche
Espanol
Getafe
Girona
Granada
Las Palmas
Leganes
Levante
Mallorca
Osasuna
Oviedo
Real Madrid
Sevilla
Sociedad
Valencia
Valladolid
Vallecano
Villarreal
```

**Rename/Spelling Traps (map silently, NOTE each rule once):**
- Ath Bilbao / Ath Madrid keep these forms (never Athletic/Atletico)
- Vallecano (never Rayo)
- Sociedad and Betis stay short

### 3.4 90-Minute Doctrine

- League matches = full-time 90-minute score
- NO extra time scores in league matches
- NO penalty scores in league matches
- If a match was postponed and played later, use the ACTUAL play date

### 3.5 File Termination

File MUST end with:

```
END
```

**No standings tables anywhere. Rows only.**

---

## 4. SOURCE HIERARCHY + VERIFICATION (NON-NEGOTIABLE)

### 4.1 Primary Source: RSSSF

```
Primary URL pattern: https://www.rsssf.org/tabless/span<YEAR>.html
Examples:
  2021-22: https://www.rsssf.org/tabless/span2022.html
  2022-23: https://www.rsssf.org/tabless/span2023.html
  2023-24: https://www.rsssf.org/tabless/span2024.html
  2024-25: https://www.rsssf.org/tabless/span2025.html
  2025-26: https://www.rsssf.org/tabless/span2026.html
```

**For each season:**
1. Navigate to the exact RSSSF URL
2. Verify the page shows all 38 matchdays
3. Transcribe EVERY match: date, home, away, home goals, away goals
4. Record the stated total (e.g., "380 matches / X goals") and verify your count matches
5. Note any awarded matches, postponed matches, or special notations

### 4.2 Second-Index Cross-Verification (MANDATORY)

For EVERY round, cross-verify against ONE independent index:

```
Options (choose one per round, must be independent of RSSSF):
- worldfootball.net: https://www.worldfootball.net/season/esp-laliga-2022/
- soccerway.com: https://int.soccerway.com/season/spain-la-liga-2021-2022/
- official La Liga archive
```

**Cross-verification procedure:**

1. Open the second-index page for the round
2. Compare EVERY match: date, home, away, score
3. If ALL match → proceed to next round
4. If ANY difference → resolve to RSSSF (PRIMARY) + write:
   ```
   NOTE|warning|source_conflict|Season [YYYY-YY] MD[N]: RSSSF says [date] [home] [hg]-[ag] [away]; second-index [worldfootball/soccerway] says [diff]. Resolved to RSSSF.
   ```

### 4.3 SOURCE Lines Required

Every source must have a SOURCE line:

```
SOURCE|<label>|<URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>
```

**Example:**
```
SOURCE|rsssf-spain2022|https://www.rsssf.org/tabless/span2022.html|2026-08-06|primary-archive|2021-22: all 38 matchdays dates+scores, official final table, stated total 380 matches
SOURCE|wfl-spain2022|https://www.worldfootball.net/season/esp-laliga-2022/|2026-08-06|second-index|2021-22: independent cross-verify all 380 match dates+scores
```

**Type must be one of:** `primary-archive`, `second-index`, `third-source`, `official-db`

### 4.4 SOURCE Line Rules

- [ ] One SOURCE line per distinct source
- [ ] Each SOURCE line must specify what it verified
- [ ] Access date must be the ACTUAL date you accessed it
- [ ] "what it verified" must be specific (not "everything")

---

## 5. ACCEPTANCE GATES (FAILING ANY = RETURNED INCOMPLETE)

### Gate G1: Grammar Check

```
[ ] Every row matches MATCH|date|competition|compType|home|hg|ag|away|venue|stadium|city|country||sourceLabel
[ ] Competition string is exactly "Spain La Liga" everywhere
[ ] compType is exactly "domestic-league" everywhere
[ ] All fields present, no missing pipes
[ ] File ends with END
[ ] No standings tables anywhere
```

**Fail action:** Return entire pack with specific row numbers and format errors.

### Gate G2: Boundary Check

```
[ ] No dateless rows
[ ] No duplicate fingerprints (date+home+away+competition)
[ ] No future-dated rows (vs 2026-08-06)
[ ] No rows with scores > 30
[ ] No rows with non-integer scores
```

**Fail action:** Return with specific row numbers and defect types.

### Gate G3: Identity Check

```
[ ] Every home/away string matches §3.3 roster verbatim
[ ] Zero name variants (e.g., no "Real Madrid CF", no "Athletic Bilbao")
[ ] No invented teams
[ ] No clubs outside their membership season
```

**Fail action:** Return with specific row numbers and name violations.

### Gate G4: Source Check

```
[ ] Every MATCH row has a valid sourceLabel
[ ] Every sourceLabel matches a SOURCE line in the file
[ ] Every SOURCE line has valid URL, access date, type, description
[ ] Primary source is RSSSF for all rows
[ ] Second-index cross-verification performed for every round
```

**Fail action:** Return rows lacking sources or with invalid SOURCE lines.

### Gate G5: Table Reproduction Test (ZERO TOLERANCE)

**For EACH season (2021-22, 2022-23, 2023-24, 2024-25, 2025-26):**

Recompute the final standings table from your rows ONLY:

```
Season: [YYYY-YY]
Club count: 20

Recomputed table:
Pos  Club           W   D   L   GF  GA  Pts
 1   [Club]        __  __  __  __  __  __
 2   [Club]        __  __  __  __  __  __
 ... (all 20 clubs)

Official RSSSF table:
Pos  Club           W   D   L   GF  GA  Pts
 1   [Club]        __  __  __  __  __  __
 2   [Club]        __  __  __  __  __  __
 ... (all 20 clubs)

MATCH RESULT: [EXACT MATCH / DIFFERS]
If differs, list every discrepancy:
  Position [N]: recomputed [Club] vs official [Club]
  Position [N]: recomputed W-[D]-[L] vs official W-[D]-[L]
  ...
```

**Rule:** Table reproduction must be EXACT — club-for-club, position-order, W-D-L, GF-GA, pts. If ANY club is in the wrong position, or ANY stat differs, the gate FAILS.

**Fail action:** Return with specific season, position, and stat differences.

### Gate G6: Shape Check

```
[ ] Row counts per season match §2.2 (380 per season)
[ ] Every club's match count = 38 per season they were a member
[ ] Relegated clubs absent from wrong years
[ ] Promoted clubs present in correct years
```

**Fail action:** Return with specific count diffs or membership violations.

### Gate G7: Continuity Check

```
[ ] Span is gap-free: every official match from 2021-22 through 2025-26 is present
[ ] Any missing match = written gap defect in NOTE
[ ] Postponed matches have correct (rescheduled) dates, not original dates
```

**Fail action:** Return with gap list.

### Gate G8: 90-Minute Doctrine

```
[ ] All league matches show 90-minute score (no ET, no pens)
[ ] AET/pen matches: 90' score + NOTE|info|advancement
```

**Fail action:** Return with specific violations.

---

## 6. SELF-CHECK CHECKLIST (Before Returning)

Complete EVERY item before returning your file:

```
Row count:
  Total rows: ______ (expected: 1,900)
  Per season: 2021-22: ___ / 2022-23: ___ / 2023-24: ___ / 2024-25: ___ / 2025-26: ___
  Match expected: YES / NO

Duplicate check:
  Duplicates found: ___ (must be 0)
  
Date sanity:
  Future-dated rows: ___ (must be 0)
  
Score sanity:
  Non-integer scores: ___ (must be 0)
  Scores > 30: ___ (must be 0)
  
Name check:
  Non-roster names: ___ (must be 0)
  
Table reproduction:
  2021-22: PASS / FAIL
  2022-23: PASS / FAIL
  2023-24: PASS / FAIL
  2024-25: PASS / FAIL
  2025-26: PASS / FAIL
  
Source documentation:
  SOURCE lines: ___
  Every row has source: YES / NO
  
Spot audit (one matchday per season with URL):
  2021-22 MD___: documented YES / NO
  2022-23 MD___: documented YES / NO
  2023-24 MD___: documented YES / NO
  2024-25 MD___: documented YES / NO
  2025-26 MD___: documented YES / NO
```

---

## 7. RETURN PROTOCOL

### 7.1 File Naming

```
EXACT filename: SPA-2021-2026_BP-TEAM-PACK_v2.txt
```

### 7.2 File Location

```
Place in: handoffs/ folder
Or deliver to: [specified channel]
```

### 7.3 Required File Contents

```
[ ] NOTE|info|catalog line declaring "Spain La Liga"
[ ] SOURCE lines for every source used
[ ] NOTE lines for every name_rename, source_conflict, quirk
[ ] NOTE|info|spot_audit lines for one matchday per season
[ ] MATCH lines for every match in scope
[ ] END line at file end
```

### 7.4 Post-Return Process

1. Auditor receives your file
2. Auditor runs FRESH parse (never reuses your code or scripts)
3. Auditor re-runs ALL gates independently (G1-G8)
4. Auditor performs cross-diff against independent sources
5. Auditor issues ONE approval card OR returns with defect list
6. If approved: commits through app's own intake
7. If rejected: you fix ONLY what is listed, re-return

**Rule:** Your self-check is registered but NEVER adopted in place of auditor verification.

---

## 8. COMPLIANCE ACKNOWLEDGMENT

```
I, [Researcher Name], acknowledge:

1. I have read this ENTIRE workorder (all sections, all gates, all checklists)
2. I have read WORKORDER-RESEARCHER-MASTER-v1.md in full
3. I understand that falsified data = immediate rejection
4. I will NEVER invent teams, scores, or dates
5. I will NEVER use market data (P1 violation)
6. I will perform table reproduction for EVERY season before returning
7. I will cross-verify EVERY round against a second index
8. I will document EVERY source with URL and access date
9. I understand my file will be independently verified by the auditor
10. I understand that if I cannot verify something, I must write NOTE|warning|blocker

Researcher signature: _______________
Date: _______________
```

---

## APPENDIX A: RSSSF SPAIN FOOTBALL PAGE REFERENCES

```
Main index: https://www.rsssf.org/tabless.html
2021-22: https://www.rsssf.org/tabless/span2022.html
2022-23: https://www.rsssf.org/tabless/span2023.html
2023-24: https://www.rsssf.org/tabless/span2024.html
2024-25: https://www.rsssf.org/tabless/span2025.html
2025-26: https://www.rsssf.org/tabless/span2026.html
```

## APPENDIX B: EXAMPLE MATCH ROW

```
MATCH|2022-08-21|Spain La Liga|domestic-league|Real Madrid|1|1|Barcelona|MD1|Santiago Bernabéu|Madrid|Spain||rsssf-span2023
```

(Note: This is an EXAMPLE format only. Verify actual data from sources.)

---

*End of WORKORDER-SPA-COMPLETION-v1.0*
*This workorder is binding. No deviations without documented approval.*
