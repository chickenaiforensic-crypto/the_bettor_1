# WORK ORDER — AUDITOR: PHASE 0 SOURCE OF TRUTH VERIFICATION

**Issued by:** Director of Intelligence  
**Date:** 2026-08-06  
**Auditor:** [TO BE ASSIGNED]  
**Priority:** CRITICAL — First verification before any data is trusted  
**Format:** Audit report in `Supervior/Build Docs/` + log in `Supervior/updates/`  

---

## ⚠️ READ THIS FIRST

You are the ONLY person allowed to say "this is true." You earn it every time with fresh code. Nothing enters the store on your trust — not from the researcher, not from the builder, NOT FROM A PREVIOUS AUDITOR.

**History:** The previous auditor's gates missed 11 date errors (CZ1). Your method is what caught them. Do not inherit trust from any previous audit.

---

## 0. MANDATORY PRE-WORK

### 0.1 Confirmation of Reading

```
I, [Auditor Name], confirm I have read:
[ ] START-HERE-COLD-START.md (in full)
[ ] COMMUNICATION-RULES-v1.md (in full)
[ ] ROLE-AUDITOR.md (in full)
[ ] WORKORDER-AUDITOR-MASTER-v1.md (in full)
[ ] VERIFICATION-DATA-2026-08-05.md (in full)
[ ] COLD-START-PACKAGE.md (in full)

Signature: _______________
Date: _______________
```

### 0.2 The "Never" List for Auditors

You must NEVER:

- [ ] Reuse the previous auditor's scripts as evidence (fresh code only)
- [ ] Trust a file on arrival without hashing (md5/sha256 first)
- [ ] Assume — if it's not confirmed in file/output, it's not known
- [ ] Guess — no inferences presented as facts
- [ ] Silent-rewrite your own instrument errors (log them with your name)
- [ ] Accept "registered" self-reports as evidence
- [ ] Use stories instead of file/code/pin citations

### 0.3 Your Binding Rules

1. **Fresh code, always.** Write your own parser. Compare outputs. Reuse previous scripts only as cross-check.
2. **Verify the instrument before the verdict.** A test that cannot distinguish Array.push() from a void-bet is not a test.
3. **Pins on arrival.** Every file: md5/sha256 on arrival, compared against declared pin before anything else.
4. **Third-source adjudication.** Where archive and pack disagree, adjudicate against independent third source. Write reasoning in report.
5. **Errata owned.** Your instrument's errors logged with your name — never silent-rewritten.
6. **The harness is yours.** Run test-run ladder on every candidate. Artifact table IS approval record.
7. **No stories.** Every assertion cites a file, code line, or pin.

---

## 1. YOUR MISSION: PHASE 0 VERIFICATION

### 1.1 Objective

Verify that the 4 IMPORT-READY packs are authentic, complete, and accurate. Establish them as the single source of truth for all team and tournament data.

### 1.2 Files to Verify

| File | Declared md5 | Rows | Competition |
|---|---|---|---|
| RPL-2021-2026_BP-TEAM-PACK_v2.txt | c3a72b35e834cc030d62b3d160c79b25 | 732 | Russian Premier League |
| RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt | 91bce98de5ff5f999a2f03f3ee7d3caa | 189 | Russian Cup |
| MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt | 662fe5dfe38002474855110b2a17ea6c | 120 | MOL Cup |
| CZ1-2021-2026_BP-TEAM-PACK_v2.txt | 29c3b6c9d63906bde4db20ac4e6b742c | 841 | Czech First League |

### 1.3 File Locations

```
Primary location: previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/DATA-PACKS/IMPORT-READY-2026-08-03/

Backup location (returns): previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/DATA-PACKS/returns/
```

---

## 2. VERIFICATION PROTOCOL (STEP BY STEP)

### Step 1: Receipt + Pin Verification

```
FOR EACH FILE:
1. Copy file to your working directory
2. Compute md5: md5sum <filename>
3. Compute sha256: sha256sum <filename>
4. Compare against declared md5 in §1.2
5. Record in your report:

File: _______________
Received date: _______________
Computed md5: _______________
Declared md5: _______________
Match: YES / NO
Computed sha256: _______________

If md5 DOES NOT MATCH: STOP. File may be corrupted or tampered. Notify Director immediately.
```

### Step 2: Grammar Verification (Fresh Parse)

```
WRITE FRESH CODE to parse each file. Do NOT reuse previous auditor's scripts as primary evidence.

Your parser must verify:
[ ] Every line matches BP-TEAM-PACK v2 format
[ ] MATCH lines: MATCH|date|competition|compType|home|hg|ag|away|venue|stadium|city|country||sourceLabel
[ ] TEAM lines (if present): TEAM|name|country||leagueCode|...
[ ] SOURCE lines: SOURCE|label|URL|accessed|type|description
[ ] NOTE lines: NOTE|level|tag|text
[ ] File ends with END
[ ] No standings tables anywhere (rows only)
[ ] No zip, no paste fragments (text file only)

FAIL ACTION: Return with specific line numbers and format errors.
```

### Step 3: Boundary Verification

```
FOR EACH FILE, SCAN FOR:

[ ] Dateless rows: rows where date field is empty or invalid
[ ] Duplicate fingerprints: same date+home+away+competition appears twice
[ ] Future-dated rows: date is after today (2026-08-06) or after export date
[ ] Non-integer scores: hg or ag is not a whole number
[ ] Scores > 30: any goal count exceeds 30
[ ] Missing required fields: any field empty that should have data

RECORD:
File: _______________
Dateless rows: ___ (list line numbers if > 0)
Duplicate fingerprints: ___ (list if > 0)
Future-dated rows: ___ (list if > 0)
Non-integer scores: ___ (list if > 0)
Scores > 30: ___ (list if > 0)
Missing fields: ___ (list if > 0)

FAIL ACTION: Return with specific row IDs and defect types.
```

### Step 4: Identity Verification

```
EXTRACT all unique home/away team strings from each file.
COMPARE against the expected roster for that competition.

FOR RPL (Russian Premier League):
Expected clubs include: Zenit, Spartak, CSKA, Lokomotiv, Dynamo Moscow, Krasnodar, etc.
[COMPLETE THIS LIST FROM WORKORDER OR RSSSF]

FOR RUSCUP:
Teams should be Russian clubs (at least one Premier League club per match).

FOR MOLCUP:
Teams should be Czech clubs. Verify against known MOL Cup participants.

FOR CZ1 (Czech First League):
Expected clubs include: Sparta Prague, Slavia Prague, Viktoria Plzen, etc.
[COMPLETE THIS LIST FROM WORKORDER OR RSSSF]

RECORD:
File: _______________
Unique home teams: ___
Unique away teams: ___
Teams not on expected roster: ___ (list each with line numbers)
Name variants found: ___ (list each: "found X, expected Y")

FAIL ACTION: Return with specific team names and violations.
```

### Step 5: Source Verification

```
FOR EACH FILE:

[ ] Verify every MATCH row has a valid sourceLabel
[ ] Verify every sourceLabel matches a SOURCE line in the file
[ ] Verify each SOURCE line has:
    - Valid URL (test accessibility or verify was accessible on access date)
    - Real access date (not invented — should be on or before your receipt date)
    - Valid type (primary-archive, second-index, third-source, official-db)
    - Specific "what it verified" description (not vague)

[ ] Verify primary source is appropriate:
    - RPL: RSSSF rus2022/rus2023/rus2024 chapters
    - RUSCUP: RSSSF cup chapters
    - MOLCUP: RSSSF cup chapters + wiki for R2/R3
    - CZ1: RSSSF tsje2022/tsje2023/tsje2024

RECORD:
File: _______________
Total MATCH rows: ___
Rows with sourceLabel: ___
Rows without sourceLabel: ___ (list if > 0)
SOURCE lines found: ___
Invalid SOURCE lines: ___ (list if > 0)
Primary source appropriate: YES / NO

FAIL ACTION: Return rows lacking sources or with invalid SOURCE lines.
```

### Step 6: Table Reproduction Test (ZERO TOLERANCE)

```
THIS IS THE MOST CRITICAL TEST. Write fresh code to recompute standings from rows ONLY.

FOR EACH SEASON IN EACH FILE:

1. Extract all matches for that season
2. For each team, compute:
   - Played (P)
   - Won (W)
   - Drawn (D)
   - Lost (L)
   - Goals For (GF)
   - Goals Against (GA)
   - Goal Difference (GD = GF - GA)
   - Points (Pts = W*3 + D*1)

3. Sort by: Points DESC, then GD DESC, then GF DESC

4. Compare against official table from RSSSF:
   - Club-for-club match
   - Position-order match
   - W-D-L match
   - GF-GA match
   - Pts match

REPORT FORMAT:

Season: 2021-22
Competition: [RPL/CZ1/etc.]
Clubs in pack: ___
Clubs in official table: ___

Recomputed table:
Pos  Club           P   W   D   L   GF  GA  GD  Pts
 1   [Club]        __  __  __  __  __  __  __  __
 2   [Club]        __  __  __  __  __  __  __  __
... (all clubs)

Official RSSSF table:
Pos  Club           P   W   D   L   GF  GA  GD  Pts
 1   [Club]        __  __  __  __  __  __  __  __
 2   [Club]        __  __  __  __  __  __  __  __
... (all clubs)

MATCH RESULT: [EXACT MATCH / DIFFERS]

If DIFFERS, list EVERY discrepancy:
  Position [N]: recomputed [Club] vs official [Club]
  Position [N]: recomputed W-[D]-[L] vs official W-[D]-[L]
  Position [N]: recomputed GF-[GA] vs official GF-[GA]
  Position [N]: recomputed Pts-[N] vs official Pts-[N]

REPEAT FOR EVERY SEASON IN EVERY FILE.

FAIL ACTION: If ANY club is in wrong position or ANY stat differs → FAIL entire file.
```

### Step 7: Cross-Diff Against Independent Sources

```
FOR A STATISTICALLY SIGNIFICANT SAMPLE (or all rows if feasible):

1. Parse the same matches from an independent source
2. Compare: date, home, away, score
3. If all match → mark as verified
4. If any diff → adjudicate against third source

INDEPENDENT SOURCES BY COMPETITION:

RPL:
- Primary: RSSSF rus2022/rus2023/rus2024
- Second index: football-data.co.uk (data/rpl/ in repo)
- Third source (for conflicts): championat.com, sport-express.ru, transfermarkt

CZ1:
- Primary: RSSSF tsje2022/tsje2023/tsje2024
- Second index: worldfootball.net per-round pages
- Third source: Wikipedia Czech First League pages

RUSCUP:
- Primary: RSSSF cup chapters
- Second index: Wikipedia Russian Cup pages
- Third source: transfermarkt, sport-express, championat

MOLCUP:
- Primary: RSSSF cup chapters (R16 onward)
- Second index: Wikipedia MOL Cup pages (R2/R3)
- Official DB: molcup.cz (for AET verification)

RECORD:
File: _______________
Sample size: ___ rows cross-diffed
Rows matching: ___
Rows with diff: ___
Diffs resolved to primary: ___
Unresolved diffs: ___ (list each with sources and your adjudication)

FAIL ACTION: Return rows where cross-diff found unresolved conflicts.
```

### Step 8: Sentinel Date Detection

```
SCAN FOR SUSPICIOUS DATE PATTERNS:

[ ] Check if multiple rows share identical dates in suspicious patterns
[ ] Look for rows dumped on sentinel dates (e.g., 20YY-06-30 patterns)
[ ] Verify each date matches actual match date from primary source

HISTORY (for awareness, not as prior evidence):
- UEFA-FULL had 100% of main-stage rows on sentinel dates 20YY-06-30
- KOS had all 180 rows on two dates: 2023-06-30 and 2024-06-30

RECORD:
File: _______________
Date range: [earliest] to [latest]
Unique dates: ___
Most common date: [date] (appears ___ times)
Suspicious patterns: [describe or "none found"]

If sentinel dates detected → REJECT entire pack as likely fabricated.
```

### Step 9: Ghost Club Detection

```
FOR EACH TEAM IN EACH PACK:

1. Verify the team existed in that competition that season
2. Cross-reference against official league roster for that season
3. Flag any team that:
   - Never existed in that competition
   - Was not in that division that season
   - Is a renamed version of another team without disclosure

HISTORY (for awareness, not as prior evidence):
- KOS had ghost clubs Ferizaj and Suhareka that were not in 2023-24 Superliga

RECORD:
File: _______________
Total unique teams: ___
Teams verified as legitimate: ___
Potential ghost clubs: ___ (list each with evidence)

If ghost clubs detected → REJECT entire pack.
```

### Step 10: 90-Minute Doctrine Verification

```
FOR LEAGUE MATCHES (compType = domestic-league):

[ ] Verify no extra-time scores (hg/ag should be 90-minute score)
[ ] Verify no penalty scores (hg/ag should be 90-minute score)
[ ] If a match went to AET/pens, verify it shows 90' score only

FOR CUP MATCHES (compType = domestic-cup):

[ ] Verify AET/pen ties show 90' score + NOTE|info|advancement
[ ] Verify two-leg ties show both legs separately with correct dates

RECORD:
File: _______________
League matches checked: ___
AET/pen violations in league matches: ___ (list if > 0)
Cup matches checked: ___
AET/pen handled correctly: YES / NO

FAIL ACTION: Return with specific violations.
```

---

## 3. SUMMARY REPORT FORMAT

```
AUDIT REPORT — PHASE 0: SOURCE OF TRUTH VERIFICATION
========================================================
Auditor: [Name]
Date: [YYYY-MM-DD]
Branch: arena/019fd71e-the-bettor-1

FILES VERIFIED
------------------------------------------------========
1. RPL-2021-2026_BP-TEAM-PACK_v2.txt
   md5: [computed] vs declared c3a72b35e834cc030d62b3d160c79b25 → MATCH: YES/NO
   Rows: [count]
   Grammar: PASS/FAIL
   Boundary: PASS/FAIL (details)
   Identity: PASS/FAIL (details)
   Source: PASS/FAIL (details)
   Table reproduction: PASS/FAIL
     2021-22: PASS/FAIL
     2022-23: PASS/FAIL
     2023-24: PASS/FAIL
   Cross-diff: PASS/FAIL (sample size, results)
   Sentinel date scan: PASS/FAIL
   Ghost club scan: PASS/FAIL
   90-min doctrine: PASS/FAIL
   Overall: APPROVED / REJECTED

2. RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt
   [SAME FORMAT AS ABOVE]

3. MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt
   [SAME FORMAT AS ABOVE]

4. CZ1-2021-2026_BP-TEAM-PACK_v2.txt
   [SAME FORMAT AS ABOVE]

SUMMARY
------------------------------------------------========
Files approved: ___ / 4
Files rejected: ___ / 4

If any rejected, list defects:
[FILE]: [DEFECTS]

If all approved:
These 4 packs are verified as authentic, complete, and accurate.
They are established as the single source of truth for team and tournament data.

VERIFICATION METHODOLOGY
------------------------------------------------========
- Fresh parse with custom code (scripts retained in audit_work/)
- Pin verification (md5/sha256 on arrival)
- Grammar verification (BP-TEAM-PACK v2 format)
- Boundary verification (dates, duplicates, scores)
- Identity verification (roster match)
- Source verification (every row sourced, primary = RSSSF)
- Table reproduction (zero tolerance, all seasons)
- Cross-diff against independent sources
- Sentinel date detection
- Ghost club detection
- 90-minute doctrine verification

PINS
------------------------------------------------========
RPL pack: md5 [computed] / sha256 [computed]
RUSCUP pack: md5 [computed] / sha256 [computed]
MOLCUP pack: md5 [computed] / sha256 [computed]
CZ1 pack: md5 [computed] / sha256 [computed]

Store (if verifying): Supervior/other/pitch-rating-full.json
Store md5: [computed]
Store sha256: [computed]

ERRATA
------------------------------------------------========
[Any instrument errors encountered, logged with your name]
[Or "None"]

========================================
VERDICT: [ALL APPROVED / SOME REJECTED / ALL REJECTED]
========================================
```

---

## 4. APPROVAL CARD FORMAT (IF ALL PASS)

```
========================================
APPROVAL CARD — PHASE 0 SOURCE OF TRUTH
========================================
Date: [YYYY-MM-DD]
Auditor: [Name]
Packs verified: 4

1. RPL-2021-2026_BP-TEAM-PACK_v2.txt
   md5: c3a72b35e834cc030d62b3d160c79b25 ✓
   Rows: 732
   All gates passed ✓

2. RUSCUP-2021-2026_BP-TEAM-PACK_v2.txt
   md5: 91bce98de5ff5f999a2f03f3ee7d3caa ✓
   Rows: 189
   All gates passed ✓

3. MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt
   md5: 662fe5dfe38002474855110b2a17ea6c ✓
   Rows: 120
   All gates passed ✓

4. CZ1-2021-2026_BP-TEAM-PACK_v2.txt
   md5: 29c3b6c9d63906bde4db20ac4e6b742c ✓
   Rows: 841
   All gates passed ✓

VERDICT: ALL FOUR PACKS APPROVED AS SINGLE SOURCE OF TRUTH
========================================
```

---

## 5. REJECTION FORMAT (IF ANY FAIL)

```
========================================
REJECTION NOTICE — PHASE 0 SOURCE OF TRUTH
========================================
Date: [YYYY-MM-DD]
Auditor: [Name]
Pack(s) rejected: [list]

REJECTED PACKS:

1. [PACK NAME]
   Reason: [specific reason]
   Defects:
   - [Defect 1 with specific row numbers/values]
   - [Defect 2 with specific row numbers/values]
   - ...

RECOMMENDATION: [Do not use / rework required / etc.]

========================================
```

---

## 6. YOUR DELIVERABLES

```
[REQUIRED] Audit report in: Supervior/Build Docs/AUDIT-PHASE0-VERIFICATION-2026-08-06.md
[REQUIRED] Log entry in: Supervior/updates/SESSION-2026-08-06-AUDIT.md
[REQUIRED] Fresh scripts retained in: audit_work/ (for re-run)
[REQUIRED] Pin registry updated with computed hashes
```

---

## 7. COMPLIANCE ACKNOWLEDGMENT

```
I, [Auditor Name], acknowledge:

1. I have read all required documents in full
2. I understand that I am the ONLY person allowed to say "this is true"
3. I will use FRESH CODE for all verification (not previous auditor's scripts as evidence)
4. I will HASH every file on arrival before processing
5. I will NEVER assume — if it's not confirmed, it's not known
6. I will NEVER guess — no inferences as facts
7. I will perform TABLE REPRODUCTION for every season in every pack
8. I will perform CROSS-DIFF against independent sources
9. I will scan for SENTINEL DATES and GHOST CLUBS
10. I will document EVERYTHING with specific row numbers and values
11. I understand that my verdict determines whether these packs become the source of truth

Auditor signature: _______________
Date: _______________
```

---

## 8. IMPORTANT NOTES

### 8.1 Do NOT Use Prior Audit as Evidence

The prior audit (`audit/external-audit-019fd4fb-2026-08-06.md`) is INFORMATIONAL ONLY. You must verify everything yourself with fresh code. You may use it as a cross-check, but not as primary evidence.

### 8.2 Known Issues to Watch For

From prior audit findings:
- CZ1 had 11 date errors (+1 day) — D-1, now fixed in corrected store
- MOLCUP store has 120 rows (OLD), 202-row FULLSPAN not imported — D-2
- KOS pack: REJECTED (fabricated)
- UEFA-FULL: REJECTED (fabricated)
- UEFA-CONNECTOR (prior): REJECTED (sentinel dates)

These are for your AWARENESS. Verify everything yourself.

### 8.3 If You Find Problems

1. Document specifically: file, row number, field, expected vs actual
2. Do NOT fix it yourself (researchers fix their own packs)
3. Return with defect list
4. Log in session file

---

*End of WORKORDER-AUDITOR-PHASE0-VERIFICATION-v1*
*This workorder is binding. No deviations without documented approval.*
