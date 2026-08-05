# For Researcher 2 — Activate — Fix UEFA Duplicate Defect

Copy-paste to Researcher 2 (dormant, needs to fix):

---
Subject: Activate — Fix UEFA Connector 1 Duplicate Defect — Branch arena/019fd213-the-bettor-1

Hi [Researcher 2 Name],

You are Researcher 2 — UEFA Connector pack — you delivered 1390 matches on branch arena/019fd1a3-the-bettor-1 — consolidated into planner arena/019fd213-the-bettor-1 handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt 185K — but full audit found 1 defect blocking ingest gate.

**Defect (auditor fresh code audit_work/rere_parse_uefa.py + verify_new_packs.py):**

Duplicate fingerprint:
('2022-04-12', 'Real Madrid', 'Chelsea', 'UEFA Champions League')
  Entry1: 2022-04-12 Real Madrid 1-3 Chelsea venueType QF leg2 stadium '' country Spain sourceId UCL-2122-QF-CHE-REA tieId openfootball
  Entry2: 2022-04-12 Real Madrid 2-0 Chelsea venueType QF leg1 stadium '' country Spain sourceId UCL-2223-QF-CHE-REA tieId openfootball

Same fingerprint date+home+away+competition different scores 1-3 vs 2-0 different leg labels leg2 vs leg1 different source IDs UCL-2122 vs UCL-2223 wrong season — second has wrong season/wrong leg.

Real world: 2021-22 QF Leg1 Apr 6 Chelsea 1-3 Real Madrid, Leg2 Apr 12 Real Madrid 2-3 Chelsea (aet) — so one entry should be Apr 6, other Apr 12 2-3, not both Apr 12 with 1-3 and 2-0. Need check 90-min scores vs official UEFA.com + RSSSF.

**What to fix per workorder §5 + 90-min doctrine + Z-003 hold lesson:**

- Correct dates per RSSSF country European sections #ec + UEFA.com official archive (uefa.com/uefachampionsleague/history) + Wikipedia + worldfootball per-round — both legs dates.
- Correct scores: 90-min doctrine — any tie decided in extra time or penalties carries 90-minute score + mandatory NOTE|info|advancement which side advanced how pens score — never after-ET score.
- Ensure both legs share ONE tieId string (e.g., UCL-2122-QF-CHE-REA) — both legs ONE tieId mandatory: per-leg distinct tieIds trigger app's Z-003 hold screen (proven in programme) — Z-003 hold check exactly-two-leg cup ties whose legs carry different tieIds instead of one shared id.
- Ensure 0 duplicate fingerprint inside file — dedupe fingerprint date+canon(home/away/competition) add-if-new L321/L1016 — currently 1 dup FAIL must be 0 PASS.
- Byte-deterministic rebuild identical — triple-rebuild identical SHA256 — like your GER pack 4f90ddb1 triple-rebuild identical and FRA 44fe06b5 double-rebuild identical and ITA e808c9f8 double-rebuild identical — your UEFA should also be byte-deterministic.
- Re-verify 689 UCL + 437 UEL + 264 UECL = 1390 total, 99 TEAM foreign opponents, 2 SOURCE 61 NOTE, compTypes uefa-cl/el/uecl per loader whitelist L737 already ready.

**Where you work:**

- Branch: you were locked to arena/019fd1a3-the-bettor-1 — expected Arena behavior every session auto-creates arena/<id> branch — your push DID succeed, consolidated into planner arena/019fd213-the-bettor-1.
- Now checkout planner branch to fix: git checkout arena/019fd213-the-bettor-1 && git pull origin arena/019fd213-the-bettor-1 — edit handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt — fix duplicate — then push to planner branch or your own branch and ping — I will fetch and re-audit.

**File path:** handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt on planner branch.

**After fix:** Full auditor gates re-run: participation completeness every programme-league club Euro list 2021-22..2025-26 complete vs official participant lists, structure round/phase counts vs official format (UCL league phase 8 rounds ×18 ties from 2024-25 group stage 6×16 2021-24), shared tieId, 90-min doctrine AET/pens 90' + advancement NOTE, boundary no future no dup, names every home/away resolves roster or TEAM rows zero split, independent cross-diff vs 4244-row European index, spot-audit one matchweek per season NOTE, continuity gap-free 2021-22→today.

If passes → enables S5 league pivot s[L] bias loop fit-to-results loop per owner clarification (per-league X points above) — bump-up/calibrate so live computations always accurate real-world — plus enriches R2 evidence graph immediately for cross-league fixtures.

Please fix now — dormant currently — this blocks S5 league pivot.

— Lead Planner (Arena AI) — branch arena/019fd213-the-bettor-1

---
