# WORK ORDER — Builder: Clean-Boot Seed Quarantine v1.0

**Document ID:** `WORKORDER-BUILDER-CLEAN-BOOT-QUARANTINE-v1.0`
**Issued:** 2026-08-08
**Priority:** P0 — runtime data integrity
**Scope:** Remove automatic runtime loading of unapproved embedded seed packs. Do not change prediction math.

## 1. Mandatory reading

Read fully before changing code:

1. `COMMUNICATION-RULES-v1.md`
2. `START-HERE-COLD-START.md`
3. `README.md`
4. `Supervior/ROLES/ROLE-BUILDER.md`
5. `Supervior/Build Docs/DIRECTOR-CONTROL-SOT-v1.0.md`
6. `Supervior/Build Docs/APP-EMBEDDED-SEED-REGISTER-v1.0.md`
7. This workorder

Reply first with the exact baseline hash and a plain statement of how you will prevent auto-seeding.

## 2. Exact baseline

```text
builder/app-v3.17.0-picker.html
MD5: e6687ad417fd1d3229a000c12f73f1a3
SHA-256: 51e275da4d2bbb3a0b198fa7f07d66ec9fd07bb965293b4c63ab8d9ea1e210d7
```

## 3. Defect to remove

On first boot, the app currently loops over `SEED_PACKS`, parses every embedded pack, and commits rows into a new store.

Those packs include partial legacy and closure records for Wales, Slovenia, Kosovo, Scotland, Malta, Iceland, Cyprus, and other countries. They are not approved full country packs.

This automatic runtime loading must stop.

## 4. Required behavior after the fix

A clean first boot must:

1. Create an empty store.
2. Show a plain `No approved data loaded yet` state.
3. Show the existing Data intake path.
4. Load data only after an owner-approved, auditor-approved artifact passes `PR.ingest`.
5. Never auto-commit an embedded pack, legacy seed, closure graph, or model record.

The app may preserve historical seed text outside runtime only if it is not loaded, parsed, displayed as available data, or included in the production bundle.

## 5. What must not change

Do not change:

- Dixon-Coles calculations, ELO, evidence logic, calibration, or parity targets;
- `PR.ingest` grammar, validation, or one-gate rule;
- backup, purge, settlement, provenance, NO CALL, or balance-panel behavior;
- approved 5,082-row store artifact;
- network policy: zero network calls remains mandatory.

If a change appears to need new data or a model rewrite, stop and write a blocker.

## 6. Required output

Use versioned filenames only:

```text
builder/app-v3.18.0-clean-boot.html
handoffs/CLEAN-BOOT-v3.18.0-<md5>.b64.txt
handoffs/CLEAN-BOOT-EVIDENCE-v3.18.0.md
handoffs/CLEAN-BOOT-EVIDENCE-v3.18.0.json
audit_work/audit_clean_boot_v3.18.0-v1.0.py
Supervior/Build Docs/CLEAN-BOOT-AUDIT-PLAN-v1.0.md
Supervior/updates/SESSION-2026-08-08-CLEAN-BOOT-v1.0.md
```

## 7. Required evidence

The new audit script must prove:

1. First boot does not call `PR.ingest.parsePack` or `PR.ingest.commit` for embedded packs.
2. No `SEED_PACKS` runtime payload is present in the production app bundle.
3. First boot contains zero MATCH rows, zero identities from seed packs, and zero country coverage chips derived from seed data.
4. Data intake still uses `PR.ingest` as the only entry gate.
5. No `fetch`, `XMLHttpRequest`, or `$.ajax` calls exist.
6. Existing parity target object is byte-identical.
7. NO CALL, provenance, and settlement safeguards remain present.

## 8. Return

Commit to your assigned Arena branch. Return branch, commit, exact files, MD5, SHA-256, first-boot audit output, and every blocker. Do not merge or release it yourself.
