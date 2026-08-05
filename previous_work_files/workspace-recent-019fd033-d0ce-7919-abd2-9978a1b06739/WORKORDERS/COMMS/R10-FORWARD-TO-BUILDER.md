# R10 — verification round 10 (v3.5.x) — FORWARD VERBATIM TO BUILDER

Auditor verdict on v3.5.0 (md5 400077a96bf0ce885908aceeb616ebc3): **accepted as CURRENT** — your replay hitRate fix and ingest commit-skip fix are both real and independently re-proven (hitRate 100 on a synthetic all-away-wins league; double-commit → `data/commit-skip`, no false "Pack committed: 0"). Store stable 1,436/539, seeds 9/0, R1/R4/D12 re-probes green. Two notes: your R9-D10/Z-010 docs say 602,425 B — actual is 602,624 B (md5 is correct; cosmetic). The `SECTION|` line I used in an early probe is not in the documented return grammar — v3.5.0's block rejection of unknown rows is correct and stays.

**However: the two defects R9 ordered are still unfixed.** You fixed two other genuine bugs that share the D9/D10 labels. The auditor's repros below are the acceptance contract — run them verbatim on your side before shipping:

## DEFECT D9 (requests.js, parseReturn ~L2689)
League codes are collected ONLY from `staged.identities` (new identities). Routine returns update EXISTING teams → `staged.identities` is empty → `codes: []` → the returned league section never flips.

Auditor repro (run in your harness; DOCUMENTED grammar — plain BP-TEAM-PACK v2, no SECTION line):
1. Boot store (seeds). `PR.ui.newCentralRequest(s, derived, '2026-08-02')`.
2. Return text: `BP-TEAM-PACK v2\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated\nEND\n` (both teams EXIST in the store).
3. `PR.requests.parseReturn` → **actual: codes=[]** ; expected: codes contains "RPL" (infer from staged match rows' league field → catalog/identity map, not only from new identities).
4. `PR.ui.commitReturn` → match stores (1,436→1,437 ✓) but **actual: RPL section stays "requested" while overall flips "partial"**; expected: RPL section → "partial".

Pin to add: routine return (existing teams only) flips exactly the returned league's section; unrelated sections stay "requested".

## DEFECT D10 (ui.js, commitReturn ~L3306-3307)
Unconditional success logging. Repro: commit the SAME return a second time (all rows now duplicates). **Actual: `data/return-commit | Central request return committed: 0 matches, 0 teams ().` + `snapshot/post-return` are logged, and with a fully-rejected block (e.g. unknown row) even the overall request state flips to "partial" with 0 rows stored. Expected: when committed matches+teams = 0 (nothing stored), log a short rejection/nothing-to-store note (your new `commit-skip` wording fits); DO NOT log a return-commit success line, DO NOT stamp snapshot/post-return, DO NOT change request state.

Pin to add: second identical return commits 0 rows, writes exactly one honest skip log, and leaves request state + artifacts untouched.

Ship via b64 as v3.5.1+ (version must bump). No other changes requested in this round.
