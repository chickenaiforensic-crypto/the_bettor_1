# WORKORDER v1 — HOLD-APPROVE-01: held packs cannot be committed (no Approve UI)

- **Date:** 2026-08-04 (UTC) · **From:** Auditor · **To:** Builder · **Priority:** P0-blocking (import programme halted)
- **Base file:** `APP-V3.6.2/app-v3.6.2.html` · md5 `c7f955d4aacdeaaca9a44e4314f2b14e` · 634,591 B
- **Ship:** v3.6.3 (versioning policy: every ship bumps upward; badge + footer read APP_VERSION)

---

## D0 — Defect (code-proven, owner-reproduced live)

Staging a pack that passes validation with informational holds (Z-003) lands the file in
`state.staged` with `status:'hold'`, `payload:v.staged`, `holds:v.holds` (stageUpload, L3700 area — correct behaviour).
The Files staged-card renderer (L3458) then does:

```js
(f.status === 'ok' ? '<button class="btn small" data-approve="' + i + '">Approve</button>' : '') +
'<button class="btn small ghost" data-discard="' + i + '">Discard</button>'
```

The **Approve button renders only for `status === 'ok'`**. For `status === 'hold'` the card shows
**only Discard** — the hold texts are never displayed and no commit path exists.
The commit machinery itself is ready and correct: `approveStaged` (L3791) commits `f.payload` with
`ownerApproved: true` and would work for held files unchanged.

Owner reproduction (live screenshot, v3.6.2, 2026-08-04): `CZ1-2021-2026.txt` → "Held — 20 item(s) need a human check" → no Approve control. Confirmed + also matched by auditor instrument replay (exact 20 holds reproduced).

**Blast radius (auditor instrument, app's exact hold rule replayed over the pinned packs):**

| Pack | MATCH rows | Holds the app shows | Committable in v3.6.2? |
|---|---:|---:|:---:|
| CZ1-2021-2026.txt | 1,401 | 20 | **NO** |
| MOLCUP-FULLSPAN.txt | 202 | 19 | **NO** |
| RPL-2021-2026.txt | 1,220 | 64 | **NO** |
| RUSCUP-2021-2026.txt | 341 | 52 | **NO** |
| RUS-ADDENDUM-2026.txt | 18 | 0 | yes (stages 'ok') |
| EPL-2021-2026.txt | 1,900 | 114 | **NO** |

Hold rule replayed for reference (L922-950): (a) a tieId carried by >2 legs; (b) `(canon(competitionName)|canon-h~canon-a sorted)` groups with **exactly 2** legs not sharing one tieId → hold message *"…Rows kept verbatim (Z-003); grouped for 90-min doctrine by competition+pair."* Both classes are informational; rows must import with **0 skipped** after human approval.

## D1 — Fix (minimal, no other behaviour change)

1. In the staged-card renderer, for `status === 'hold'` render **both**:
   - a review list showing **each hold string verbatim** from `f.holds` (scrollable is fine), and
   - an **Approve** button wired to the existing `data-approve` / `approveStaged` handler, label suggested:
     `Approve — keep rows verbatim (Z-003)`.
2. `status === 'ok'` and `'bad'` cards unchanged; Discard unchanged.
3. No changes to: ingest grammar/validators, hold *detection* logic, commit(), dedupe fingerprints, scope/purge, migration, storage keys, schema. This is a UI-affordance fix only.

## D2 — Acceptance gate (auditor will run, evidence required back)

1. **Hold-review UAT row (new harness line G13):** stage a fixture pack with exactly 1 pair-hold → card status 'hold' → hold text visible verbatim → Approve → toast "Loaded — N matches", report.skipped = 0, store grows by exactly fixture rows; re-stage same fixture → all rows skipped as duplicates (add-if-new intact).
2. Regression: rerun your full existing harness — previous 32/32 lines must stay green.
3. Live-run proof on the pinned CZ1 pack (auditor supplies sha pin `cbd5710b…90a6e`): card shows "Held — 20 item(s)…" + 20 verbatim lines + Approve; do **not** commit in the demo store; screenshot back the card + the 20 lines.
4. Return: full HTML file (never zip) + md5 + sha256 + byte size + commit sha of the repo commit + UTC timestamp of build.

## D3 — Explicitly out of scope

Pack editing to dodge holds is **forbidden** (D-rule: no silent data rewrites; e.g. fabricating tieIds on league home/away pairs would falsify data). Holds are expected on 5 of 6 packs — the app must absorb them, not the data.
