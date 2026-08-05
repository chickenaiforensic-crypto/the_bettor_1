# GATE EVIDENCE — P1 Single store & schema (2026-08-02)

**Engineer:** agent build · **Auditor:** system-side · **Status:** 🟢 (documented drift: identity count)

## The one schema (WO §3-1, §4-②)
`identities · matches · seasons · venues · sources · ctxFlags · mutes · log · artifacts · notes · meta` — one canonicalizer (`canon.js`: one `esc`, one `canon`, fingerprint), one store module, content hash (FNV-1a 64 over stable JSON), snapshot/restore, `pitch-rating-full` export/import with backward-compatible migration (`store.js`).

## Seed pipeline (all 9 packs through the ONE ingest gate)
| Source | matches | teams | mutes | notes |
|---|---|---|---|---|
| russian-team-pack.txt | 644 | 26 | 3 | — |
| czech-team-pack.txt | 631 | 45 | 0 | — |
| hibernian-team-pack.txt | 28 | 8 | 0 | — |
| malisheva-team-pack.txt | 15 | 3 | 0 | — |
| malisheva-closure-pack.txt | 17 | 6 | 0 | — |
| usa-team-pack.txt | 85 | 45 | 0 | — |
| Southampton_BP-TEAM-PACK_v2.txt | 15 | 1 | 0 | +2 FORM as verbatim artifacts (Z-003) |
| HIB_MAL_SEED_PACK.txt (embedded seed) | 29 | 14 | 0 | v1 grammar handled |
| MASTER_RECORD_CLOSURE_SEED_PACK.txt (embedded seed) | 0 | 111 | 0 | record-closure; NA codes kept verbatim (ZONES v0.14 class) |
| **Total** | **1,464 → 1,436 after cross-pack dedupe** | **520** | **3** | |

## Census reconciliation vs legacy (ZONES v0.14)
- Legacy: **1,421 matches / 792 identities / 3 mutes** (6 packs + embedded seeds).
- New: 6-pack after dedupe = **1,392** + HIB_MAL seed 29 = **1,421 ✓** + Southampton 15 = **1,436**. Matches: **exact**.
- Mutes: **3/3 preserved** (IA-01/02/03, RPL).
- Identities: **520 vs 792 — deliberate Phase-1 merge** (Dynamo-Moscow class): canon/alias resolution merges name variants onto ONE identity row (WO §6-P1 "every team resolves to exactly one identity row"). The 372-team fitted MODEL roster is also migrated (Annex D) → 520 = pack/seed identities + model-rated teams, de-duplicated.
- Ghost classes: SC1 (7 seed TEAM rows, 0 matches) kept verbatim, renders honest no-data (Annex D; ZONES v0.18/v0.19).

## Migration machinery
- `store.migrate()` tolerates legacy shapes (array identities or idKey-object, matches with `hg/ag/date/homeId/awayId`, venues object, log). Migration report generated per run (rows in/out, identities merged, mutes preserved, unmapped keys).
- Owner's live store export pending (G12): machinery exercised against the assembled seed export round-trip (smoke: `pitch-rating-full round-trip` ✅).

## Commands + raw outputs
```
$ node harness/smoke_test_v3.js  → RESULT: 26 passed, 0 failed
  boot store: 1436 matches · 520 identities · 3 mutes · 9 seed packs
  determinism: identical inputs → identical numbers  ✅
  pitch-rating-full round-trip   ✅
```
