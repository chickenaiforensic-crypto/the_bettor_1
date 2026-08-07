# Session log — 2026-08-07: KOS/KOSCUP v2.1 independent auditor verification

**Actor:** Auditor. **Branch (this session's work):** `arena/019fd74a-the-bettor-1`.

## Event
The researcher relayed corrected v2.1 packs (branch `arena/019fd805-the-bettor-1`
@ `e02dcb8`) per the Director's 2026-08-07 order, and explicitly awaited the
independent auditor's verification before import.

## What I did (fresh code; nothing taken on trust)

1. Fetched the branch; verified commit e02dcb8 is the tip, parent f9700e6
   (D1–D4 lineage intact); extracted both packs at that exact commit.
2. Hashes: KOS md5 cde3688f… / sha256 531bc96c…; KOSCUP md5 cca71b17… /
   sha256 acf40a85… — match the relay's declaration exactly. Counts: KOS
   910 MATCH / 8 TEAM / 7 SOURCE / 17 NOTE / 1 END; KOSCUP 123 MATCH / 24
   TEAM / 6 SOURCE / 41 NOTE / 1 END.
3. Data-only diff vs my independently-built v2.1 (019fd74a @ bcaee73):
   **0 lines differ** on any match fact (date|comp|ctype|home|hg|ag|away|
   round|country|tie|src) in either pack — only stadium/city fields differ
   (the researcher's venue refinements).
4. Ran my own gate suite on the researcher's files: KOS 910/900+10,
   appendix 12/12, 0 placeholders, 0 dups, 0 future, 180×5, goals
   463/446/432/446/481, table reproduction 5/5 EXACT from pack alone;
   KOSCUP 123, 0 placeholders, slice 24/24/24/26/25, D1–D4 retained, finals
   match official record. PROBLEMS: 0.
5. Venue spot-verification: Rilindja 74 → Baran Sports Field CONFIRMED
   (Wikipedia: KF Rilindja 1974, Baran, Pejë); MD12 award correct;
   2024-25 SF date keeps RSSSF primary with the conflict disclosed;
   2023-24 SF venue disclosed as inference; TOP Football venue = the ONLY
   unconfirmed value (disclosed blocker NOTE, descriptive label).
6. **NEW FINDING D5:** all 32 TEAM rows (KOS L14–21, KOSCUP L16–39) are
   field-misaligned: ground name in the surface slot, stadium slot = the
   literal string "unknown" (app grammar puts stadium at field 6; adopted
   RUSCUP reference confirms). At ingest this yields identity.stadium
   "unknown", surface = ground name, capacity NaN on KOSCUP rows, and two
   surface="not published" values. Metadata-only impact; the researcher's
   claim that the TEAM layout was fixed to match the reference is not
   accurate. (Errata owned: the v2.0 TEAM blocks were also misaligned; the
   earlier audit pass checked names, not field placement.)

## Verdict
- Match data: **APPROVED** (all three Director reasons satisfied; 1,033
  MATCH rows byte-identical to the independently verified build; every gate
  passes).
- Packs: **RETURNED for the mechanical TEAM-block realignment (D5)** —
  exact fix spec in the report (one field shift per row; no MATCH changes).
- Owner confirmation items (non-blocking for match data): TOP Football
  venue; 2023-24 playoff SF venue inference.

## Deliverables (this session, on 019fd74a)
- Supervior/Build Docs/AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md
  (independent auditor report, supersedes the researcher's self-report as
  the audit authority)
- Supervior/updates/SESSION-2026-08-07-KOS-KOSCUP-REAUDIT-v1.0.md (this log)
- audit_work/kos_koscup_reaudit_2026-08-07-v1.0/remote_e02dcb8/ (extracted
  evidence + gate runs)

*Trail rule: every number traces to a fresh command run this session on the
files extracted at commit e02dcb8.*
