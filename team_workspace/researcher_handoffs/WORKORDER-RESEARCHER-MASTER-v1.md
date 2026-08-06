# RESEARCHER WORKORDER MASTER — Zero-Harcode Data Collection

**Document ID:** WORKORDER-RESEARCHER-MASTER-v1  
**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**Application:** All researcher data collection workorders  

---

## HOW TO USE THIS DOCUMENT

This is the MASTER TEMPLATE for all researcher workorders. Every specific league workorder (ITA, GER, FRA, SCO1, etc.) is a filled-in instance of this template. The template is rigourous by design — it leaves NO room for falsification, guessing, or unaudited data.

**If you cannot complete a section as specified, STOP and write `NOTE|warning|blocker`. Do NOT improvise. Do NOT invent data.**

---

## SECTION 0: MANDATORY PRE-WORK

### 0.1 Read This Entire Document Before Touching Any Data Source

**Rule:** You must read this document in full before starting. Sign below to confirm.

```
Researcher acknowledgment: I have read this entire document.
Name: _______________
Date: _______________
```

### 0.2 Federation Check — DO NOT SKIP

Every workorder specifies a COMPETITION. Before collecting a single row:

1. Read the competition name in the workorder
2. Read the roster of clubs in workorder §3
3. **Scan your first 10 rows:** every club must be on the roster
4. If ANY club is not on the roster → WRONG COMPETITION → STOP

> **History:** The first researcher attempt in this programme delivered RWANDA data instead of RUSSIA. The federation check exists because of that failure. Do not repeat it.

### 0.3 Source Hierarchy (Non-Negotiable)

You must use sources in this order:

| Priority | Source Type | Examples | Requirement |
|---|---|---|---|
| **PRIMARY** | RSSSF archive pages | rsssf.org/tablese/eng2022.html | Parse directly; transcribe exactly |
| **SECOND** | Independent index | worldfootball.net, soccerway, official league archive | Cross-verify every round |
| **THIRD** | Adjudication source | Wikipedia, transfermarkt, press | Only for resolving PRIMARY vs SECOND conflicts |

**Rule:** If PRIMARY and SECOND disagree → resolve to PRIMARY + write `NOTE|warning|source_conflict`. Never assume. Never guess.

### 0.4 The "Never" List

You must NEVER:

- [ ] Invent a team name
- [ ] Invent a score
- [ ] Invent a date
- [ ] Use bookmaker odds or market data (P1 violation)
- [ ] Deliver standings tables (rows only; tables are recompute targets)
- [ ] Use .zip files (text files only)
- [ ] Paste fragments (one complete file per workorder)
- [ ] Guess at unverifiable data (write `NOTE|warning|blocker` instead)
- [ ] Skip the table reproduction test
- [ ] Skip the cross-verification step

---

## SECTION 1: SCOPE DEFINITION

### 1.1 Competition Identifier

```
Competition: [EXACT NAME FROM WORKORDER]
Federation: [COUNTRY]
Sport: Football (soccer)
```

### 1.2 Season Range

```
Start season: [YYYY-YY]
End season: [YYYY-YY] or "through today"
Total seasons: [NUMBER]
```

### 1.3 Row Count Specification

```
Rows per season: [NUMBER] (e.g., 380 for 20-club league, 612 for 18-club Bundesliga)
Total expected rows: [NUMBER]
Note: [Any deviations from standard, e.g., playoffs, relegation matches]
```

### 1.4 What IS in Scope

```
[List exactly what matches to collect]
Example: All regular-season league matches, 2021-22 through 2025-26
```

### 1.5 What IS NOT in Scope

```
[List what to exclude]
Example: FA Cup, League Cup, European matches, lower divisions
```

---

## SECTION 2: GRAMMAR SPECIFICATION

### 2.1 Match Row Format (BP-TEAM-PACK v2)

Every match row MUST follow this exact format:

```
MATCH|<dateISO>|<competition>|<compType>|<home>|<hg>|<ag>|<away>|<venue>|<stadium>|<city>|<country>||<sourceLabel>
```

**Field definitions:**

| Field | Requirement | Example |
|---|---|---|
| `<dateISO>` | YYYY-MM-DD format, actual match date | 2022-08-21 |
| `<competition>` | Exact competition string from workorder | England Premier League |
| `<compType>` | One of: domestic-league, domestic-cup, other | domestic-league |
| `<home>` | Roster string verbatim (see §3) | Arsenal |
| `<hg>` | Home goals, integer 0-30 | 2 |
| `<ag>` | Away goals, integer 0-30 | 0 |
| `<away>` | Roster string verbatim (see §3) | Chelsea |
| `<venue>` | Venue detail (round number for leagues) | MD1 |
| `<stadium>` | Stadium name | Emirates Stadium |
| `<city>` | City | London |
| `<country>` | Country | England |
| `<sourceLabel>` | Source label from §4 SOURCE lines | rsssf-eng2022 |

### 2.2 TEAM Row Format (Only if new identities needed)

```
TEAM|<name>|<country>||<leagueCode>|<logoURL>|<primaryColor>|<secondaryColor>|<url>|<venue>|<capacity>
```

**Rule:** If you believe a club is missing from the roster, STOP and write `NOTE|warning|blocker`. Do NOT invent a TEAM row without auditor approval.

### 2.3 SOURCE Line Format

Every source used must have a SOURCE line:

```
SOURCE|<label>|<plain URL>|<accessed YYYY-MM-DD>|<type>|<what it verified>
```

**Type must be one of:** `primary-archive`, `second-index`, `third-source`, `official-db`

### 2.4 NOTE Line Format

```
NOTE|info|<tag>|<text>
NOTE|warning|<tag>|<text>
NOTE|warning|blocker|<text>
```

**Tags you may use:** `catalog`, `source_conflict`, `name_rename`, `venue_note`, `aet`, `postponed`, `awarded`, `blocker`

### 2.5 File Termination

Every file MUST end with:

```
END
```

---

## SECTION 3: IDENTITY DISCIPLINE

### 3.1 Roster Strings (Use Verbatim)

The workorder will provide a list of exact roster strings. You MUST use these exact strings in home/away fields.

```
[WORKORDER PROVIDES LIST]
Example: Arsenal, Chelsea, Liverpool, Man City, Man United, Tottenham, etc.
```

### 3.2 Rename Rules

If a source uses a different name, map silently to the roster string and NOTE the rule once:

```
NOTE|info|name_rename|Source uses "Spurs" → roster string "Tottenham"
NOTE|info|name_rename|Source uses "Wolverhampton" → roster string "Wolves"
```

### 3.3 Prohibited Actions

- [ ] Do NOT use "Tottenham Hotspur" when roster says "Tottenham"
- [ ] Do NOT use "Manchester City" when roster says "Man City"
- [ ] Do NOT use "Athletic Bilbao" when roster says "Ath Bilbao"
- [ ] Do NOT create variant spellings
- [ ] Do NOT add clubs not on the roster

---

## SECTION 4: SOURCE DOCUMENTATION

### 4.1 Primary Source Usage

For RSSSF primary sources:

```
1. Navigate to the exact URL specified in the workorder
2. Verify the page covers the correct season
3. Transcribe every match date, home team, away team, home goals, away goals
4. Record the exact URL accessed and date accessed
5. If the page has a stated match/goal total, verify your count matches
```

### 4.2 Second-Index Cross-Verification

For every round/section:

```
1. Open the second-index URL (worldfootball.net, etc.)
2. Compare every match: date, home, away, score
3. If ALL match → proceed
4. If ANY diff → resolve to PRIMARY + write NOTE|warning|source_conflict
5. Record the second-index URL and access date in SOURCE line
```

### 4.3 SOURCE Lines Required

```
[REQUIRED] One SOURCE line per distinct source used
[REQUIRED] Each SOURCE line must specify what it verified
[REQUIRED] Access date must be the actual date you accessed it
```

---

## SECTION 5: SELF-CHECK GATES (Before Returning)

### 5.1 Row Count Check

```
Total rows collected: [NUMBER]
Expected rows: [NUMBER]
Match: YES / NO
If NO: explain discrepancy in NOTE
```

### 5.2 Duplicate Check

```
Duplicates found: [NUMBER]
Method: date+home+away+competition fingerprint
If > 0: REMOVE duplicates before returning
```

### 5.3 Date Sanity Check

```
Future-dated rows: [NUMBER]
If > 0: REMOVE or explain (postponed matches with new date are OK; invented future dates are NOT)
```

### 5.4 Score Sanity Check

```
Non-integer scores: [NUMBER]
Scores > 30: [NUMBER]
If > 0 for either: FIX before returning
```

### 5.5 Name Check

```
Rows with non-roster team names: [NUMBER]
If > 0: FIX all name variants before returning
```

### 5.6 Table Reproduction Test (MANDATORY)

For each season:

```
Season: [YYYY-YY]
Number of clubs: [N]
Recompute standings from your rows:
  Position 1: [Club] W-[D]-[L] GF-[GA] Pts-[N]
  Position 2: [Club] W-[D]-[L] GF-[GA] Pts-[N]
  ...
  Position N: [Club] W-[D]-[L] GF-[GA] Pts-[N]

Official table (from source):
  Position 1: [Club] W-[D]-[L] GF-[GA] Pts-[N]
  ...

Match: YES / NO
If NO: list every club-position that differs
```

**Rule:** Table reproduction must be EXACT — club-for-club, position-order, W-D-L, GF-GA, pts. Zero tolerance.

### 5.7 Spot-Audit Trail

```
For each season, list one full matchday in a NOTE with source URL:

NOTE|info|spot_audit|Season [YYYY-YY] Matchday [N]:
NOTE|info|spot_audit|  [date] [home] [hg]-[ag] [away] venue [venue]
NOTE|info|spot_audit|  ...
NOTE|info|spot_audit|Source: [URL]
```

---

## SECTION 6: RETURN PROTOCOL

### 6.1 File Naming

```
[SCOPE]-2021-2026_BP-TEAM-PACK_v2.txt
Example: ITA-2021-2026_BP-TEAM-PACK_v2.txt
```

### 6.2 File Location

```
Handoffs folder: [repo]/handoffs/
Or deliver to: [owner/auditor via specified channel]
```

### 6.3 File Contents Checklist

Before returning, verify your file contains:

```
[ ] NOTE|info|catalog line declaring competition
[ ] SOURCE lines for EVERY source used
[ ] NOTE lines for every name_rename, source_conflict, quirk
[ ] MATCH lines for every match in scope
[ ] END line at file end
[ ] No standings tables anywhere
[ ] No zip, no paste fragments
```

### 6.4 What Happens After Return

1. Auditor receives your file
2. Auditor runs FRESH parse (never reuses your code)
3. Auditor re-runs ALL self-check gates independently
4. Auditor performs cross-diff against independent sources
5. Auditor issues ONE approval card OR returns with defect list
6. If approved: commits through app's own intake
7. If rejected: you fix ONLY what is listed, re-return

**Rule:** Your word is registered, never adopted. The auditor's verification is what matters.

---

## SECTION 7: COMPLIANCE ACKNOWLEDGMENT

```
I, [Researcher Name], acknowledge that I have read and understood this workorder master document.

I understand that:
1. Falsified data = immediate rejection + possible removal from project
2. I must never guess, invent, or skip verification steps
3. My file will be independently verified by the auditor with fresh code
4. If I cannot verify something, I must write NOTE|warning|blocker
5. The table reproduction test is MANDATORY, not optional

Signature: _______________
Date: _______________
```

---

*End of Researcher Workorder Master v1*
*This document is binding for all researcher data collection workorders.*
