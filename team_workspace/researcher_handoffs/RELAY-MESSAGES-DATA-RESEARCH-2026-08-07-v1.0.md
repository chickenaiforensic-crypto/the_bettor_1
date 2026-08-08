# READY-TO-SEND DATA RESEARCH MESSAGES v1.0

**Use:** Send one complete block to one new researcher. Do not combine jobs.
**Do not send:** SPA, ITA, GER, or FRA researcher jobs. Their returns are already with, or queued for, the auditor.

## Shared rule

Every researcher message below requires the researcher to read the assigned workorder and `WORKORDER-RESEARCHER-MASTER-v1.1.md` fully before collecting a single row. A return is never approved until the auditor says so.

---

## 1. Kosovo Superliga researcher

```text
You are the Kosovo Superliga data researcher.

Before doing any work, read these files fully:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-KOS-2021-2026-REGENERATION-v1.0.md

This is a fresh regeneration because the earlier Kosovo pack was rejected. Do not reuse any old Kosovo rows, dates, teams, venues, or sources.

Reply first with: competition/seasons, expected row shape, and your primary plus independent source. Do not collect rows until you have done that.
```

## 2. Kosovo Cup researcher

```text
You are the Kosovo Cup data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-KOS-2021-2026-REGENERATION-v1.0.md
7. team_workspace/researcher_handoffs/WORKORDER-KOSCUP-2021-2026-REGENERATION-v1.0.md

This is a fresh cup regeneration. Use domestic-cup, not domestic-league. Do not reuse the previous Kosovo Cup candidate.

Reply first with: competition/seasons, the active-Superliga-club scope rule, and your primary plus independent source.
```

## 3. Scottish Premiership researcher

```text
You are the Scottish Premiership data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md

Build the whole 2021-22 to 2025-26 span from sources. The old candidate cannot be copied because its venue and provenance layer was incomplete.

Reply first with: competition/seasons, 228-row season shape, and your primary plus independent source.
```

## 4. Scottish Cup researcher

```text
You are the Scottish Cup data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md
7. team_workspace/researcher_handoffs/WORKORDER-SCOCUP-2021-2026-REGENERATION-v1.0.md

This replaces a partial old candidate. Use domestic-cup, include every in-scope tie, and use real venues and sources.

Reply first with: editions, the active-Premiership-club scope rule, and your primary plus independent source.
```

## 5. Scottish League Cup researcher

```text
You are the Scottish League Cup data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-SCO1-2021-2026-REPAIR-v1.0.md
7. team_workspace/researcher_handoffs/WORKORDER-SCOLC-2021-2026-REGENERATION-v1.0.md

This replaces a partial old candidate. Include group-stage and knockout matches involving an eligible Premiership club. Use league-cup, not domestic-league.

Reply first with: editions, scope rule, and your primary plus independent source.
```

## 6. US Open Cup researcher

```text
You are the US Open Cup data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-MLS-2021-2026-REPAIR-v1.0.md
7. team_workspace/researcher_handoffs/WORKORDER-USOC-2021-2026-REGENERATION-v1.0.md

This is a fresh regeneration. The 2021 cancellation must be documented. Use domestic-cup and do not reuse the incomplete three-season candidate.

Reply first with: editions, MLS-club scope rule, and your primary plus independent source.
```

## 7. MLS researcher

```text
You are the Major League Soccer data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-MLS-2021-2026-REPAIR-v1.0.md

Build regular seasons 2021-25, every MLS Cup Playoff, and only source-confirmed 2026 matches through your return date. The prior candidate missed the 2024 playoffs and used blank venues; do not reuse it.

Reply first with: seasons, regular-season row counts, playoff scope, and your primary plus independent source.
```

## 8. UEFA connector researcher

```text
You are the UEFA connector data researcher.

Read fully before doing any work:
1. COMMUNICATION-RULES-v1.md
2. START-HERE-COLD-START.md
3. README.md
4. Supervior/ROLES/ROLE-RESEARCHER.md
5. team_workspace/researcher_handoffs/WORKORDER-RESEARCHER-MASTER-v1.1.md
6. team_workspace/researcher_handoffs/WORKORDER-UEFA-CONNECTOR-2021-2026-REGENERATION-v1.0.md

This is a high-risk clean rebuild. Do not reuse any previous UEFA-FULL or UEFA-CONNECTOR rows. Official UEFA match records are the primary date, score, and venue source. Default season-end dates, placeholder venues, and penalty scores used as football scores are immediate failures.

Reply first with: competitions/seasons, programme-league scope rule, structure-ledger plan, and your official plus independent sources.
```

---

## Auditor message — send after the SPA acknowledgement

```text
You have the SPA return. Verify it independently with fresh code; do not treat the researcher’s gate results as approval.

After SPA, audit these existing candidate packs before any new researcher is assigned to them:
- origin/arena/019fc462-the-bettor-1:handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt
- origin/arena/019fc462-the-bettor-1:handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt
- origin/arena/019fc462-the-bettor-1:handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt

Read team_workspace/auditor/WORKORDER-AUDITOR-MAJOR-PACK-RECEIPTS-v1.0.md fully. Issue one separate APPROVED, REJECTED, or BLOCKED card for each pack. Do not import any pack.
```
