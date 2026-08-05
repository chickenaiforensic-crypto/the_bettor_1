# RELAY TO BUILDER SESSION — 2026-08-05 (copy-paste verbatim)

> You are the builder for the Pitch Rating engine. Everything you need to cold-start is in the repo:
>
> 1. Read `START-HERE-COLD-START.md` (root) — the reading order, in order.
> 2. Read `builder/README-BUILDER.md` — your space, what exists, what done looks like.
> 3. Read `Supervior/updates/MESSAGE-TO-BUILDER-TEST-RUN-LADDER-v1.md` — **your approval protocol.** From now on nothing is approved on documentation; every build is approved by its measured test run on our data. Read it twice.
> 4. Your first workorder: `Supervior/Workorder/WORKORDER-BUILDER-B0-HARNESS.md` — build the test-run harness into the app (masked-replay module with the ladder). The reference app, the 5,082-row store, and the feasibility harness you must reproduce are listed in the workorder.
> 5. Work starts at B0 only, then the owner approves the next step (B1, S1…) — do not scope-creep ahead.
>
> Deliverables: app file as b64-armoured `.txt` + your evidence artifact, into `handoffs/` (see `handoffs/README-HANDOFFS.md`). No raw .html over the channel. md5-verify before and after.
>
> Ground rule from the previous round: "asserted without output" is a failed gate. Show the numbers.

*Workorder B0 carries the full acceptance criteria. If anything in this message conflicts with a workorder, the workorder wins and you stop and ask.*
