# DIRECTOR CONTROL SOURCE OF TRUTH v1.0

**Issued:** 2026-08-08
**Authority:** Owner decisions + file-backed independent auditor evidence only.
**Purpose:** This is the Director’s control register for the repository. It tells every role what may be used, what is pending, and what is prohibited.

## 1. What this document is

This document is the current **control source of truth**. It does not turn a branch claim, chat message, seed pack, or self-audit into approved data.

A pack is usable only when all four are true:

1. The exact bytes are accessible on a branch or merged main.
2. Hashes are recorded.
3. An independent auditor report is accessible.
4. The register below says `APPROVED FOR IMPORT`.

## 2. Approved baseline

| Asset | Status | Exact location and pin |
|---|---|---|
| Engine correction release | `APPROVED ENGINE CORRECTION` | `main:builder/app-v3.17.0-picker.html` · MD5 `e6687ad417fd1d3229a000c12f73f1a3` · SHA-256 `51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7` |
| Verified store | `APPROVED STORE ARTIFACT` | `main:previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json` · 5,082 MATCH rows · MD5 `3c068c1f67ee8a81d412631fd0feb162` · SHA-256 `c9ad6a54fa008a69fca50cd70ee0d367be7fe8a04fc35f72298698033d7cbe1c` |
| Engine correction audit | `APPROVED FOR THE STATED CORRECTION SCOPE` | `main:Supervior/Build Docs/AUDIT-V3.17.0-PICKER-2026-08-06.md` |
| Store verification | `APPROVED FOR THE STATED STORE SCOPE` | `main:Supervior/Build Docs/VERIFICATION-DATA-2026-08-05.md` |

### Important limit

The v3.17 app is an approved **corrected legacy-continuation release**, not a ground-up new engine. Its code retains legacy migration and bootstrap paths. Do not describe it as a fully new architecture.

## 3. Approved data in the 5,082-row store

| Country / competition group | MATCH rows | Status |
|---|---:|---|
| England Premier League | 1,900 | `APPROVED IN STORE` |
| Russia: RPL, Cup, playoffs, Super Cup | 1,579 | `APPROVED IN STORE` |
| Czechia: First League, MOL Cup, playoffs | 1,603 | `APPROVED IN STORE` |
| **Total** | **5,082** | `APPROVED STORE ARTIFACT` |

No Wales, Slovenia, Scotland, Kosovo, United States, MLS, US Open Cup, UEFA, Italy, Germany, France, or Spain rows are present in this verified store artifact.

## 4. Runtime embedded-seed quarantine

The approved v3.17 file contains nine `SEED_PACKS` and automatically commits them on a first boot through `PR.ingest`.

That behavior is **not approval**. Several packs are partial closure records and contain countries outside the approved 5,082-row store.

The complete inventory is:

```text
Supervior/Build Docs/APP-EMBEDDED-SEED-REGISTER-v1.0.md
Supervior/Build Docs/APP-EMBEDDED-SEED-REGISTER-v1.0.json
```

**Runtime status:** `QUARANTINE REQUIRED`.

Until the clean-boot workorder is completed and audited:

- no embedded seed is approved merely because it appears in the app;
- no country displayed from an embedded seed is a complete approved country pack;
- the app must not be described as a clean production data boot.

## 5. Country approval register

| Scope | Current status | Exact control position |
|---|---|---|
| Wales | `UNAPPROVED PARTIAL EMBEDDED RECORDS` | Two Southampton seed rows plus identity/record-closure metadata. No Wales league pack or auditor approval exists. |
| Slovenia | `UNAPPROVED PARTIAL EMBEDDED RECORDS` | Three Celje closure rows. No Slovenian league pack or auditor approval exists. |
| Iceland, Malta, Cyprus, Sweden, Denmark, Albania, Serbia, Poland, Portugal, Northern Ireland, Belgium, Greece, Netherlands, Turkey | `UNAPPROVED PARTIAL EMBEDDED RECORDS` | Present only in partial seed/closure or identity records. No full approved country pack is registered. |
| Spain La Liga | `AUDIT VERDICT REPORTED; FORMAL CONTROL ARTIFACT PENDING` | Pack exists on `arena/019fd805-the-bettor-1`; do not import until the independent auditor report is accessible and recorded here. |
| Italy Serie A | `CANDIDATE PACK — PROJECT AUDIT PENDING` | Candidate pack exists on `arena/019fc462-the-bettor-1`; no project receipt approval is recorded here. |
| Germany Bundesliga | `CANDIDATE PACK — PROJECT AUDIT PENDING` | Candidate pack exists on `arena/019fc462-the-bettor-1`; no project receipt approval is recorded here. |
| France Ligue 1 | `CANDIDATE PACK — PROJECT AUDIT PENDING` | Candidate pack exists on `arena/019fc462-the-bettor-1`; no project receipt approval is recorded here. |
| Kosovo Superliga + Kosovo Cup | `RETURNED — D5 TEAM METADATA REALIGNMENT` | Auditor report `arena/019fd74a-the-bettor-1:Supervior/Build Docs/AUDIT-KOS-KOSCUP-REAUDIT-2026-08-07-v1.0.md`. Match rows passed, but neither pack may import until TEAM fields are corrected and re-audited. |
| Scottish Premiership / Scottish Cup / Scottish League Cup | `RECEIVED — AUDIT PENDING` | Research packs exist on `arena/019fdd60-the-bettor-1`. No independent approval is recorded here. |
| MLS | `PARTIAL / UNAPPROVED` | The 2021–24 partial file is not a full MLS return and must not import. |
| US Open Cup | `RETURNED — GRAMMAR + 2024 COMPLETENESS` | v2.1 has sourceId in the wrong field and relies on absent 2024 appendix rows. No import. |
| UEFA connector / UEFA full | `REJECTED / REGENERATE` | Prior audit found sentinel dates, missing phases, identity debt, and wrong scorelines. |

## 6. Branch role register

| Branch | Role in control process |
|---|---|
| `main` | Approved engine correction and approved 5,082-row store artifact; not a home for current researcher returns yet. |
| `arena/019fd71e-the-bettor-1` | Director control branch: this register, workorders, design handoff, and control documents. |
| `arena/019fd74a-the-bettor-1` | Auditor evidence and current KOS/KOSCUP D5 return verdict. |
| `arena/019fd805-the-bettor-1` | SPA and KOS/KOSCUP researcher return transport. |
| `arena/019fdd60-the-bettor-1` | Scottish researcher return transport. |
| `arena/019fdd64-the-bettor-1` | USOC and partial MLS researcher return transport. |
| `arena/019fc462-the-bettor-1` | External candidate-pack and external-audit transport. |

Other branches are historical work or builder/session history. Their presence is not approval.

## 7. Non-negotiable operating rules

1. Branch presence is not approval.
2. Chat text is not a deliverable.
3. Every imported pack needs an accessible auditor report and hash pin.
4. Only the approved-store table in section 3 may be treated as current approved data.
5. Embedded seeds are quarantined until clean boot removes automatic loading.
6. No pack may bypass `PR.ingest`.
7. Every revision needs a new versioned filename and a new auditor verdict.

## 8. Required next gates

1. Builder completes `WORKORDER-BUILDER-CLEAN-BOOT-QUARANTINE-v1.0.md`.
2. SPA auditor report is transferred to an accessible branch and independently recorded here.
3. KOS/KOSCUP D5 TEAM-field realignment is returned and re-audited.
4. USOC grammar and missing 2024 rows are returned and re-audited.
5. ITA, GER, FRA, Scottish packs, MLS, and UEFA each receive separate independent audit cards.
6. Only then are approved pack bytes incorporated into the verified store through the one intake gate.

## 9. Director declaration

As of 2026-08-08, this register is the only Director authority for status claims. If another document or message disagrees, this register wins until it is revised with a versioned file, hashes, and audit evidence.
