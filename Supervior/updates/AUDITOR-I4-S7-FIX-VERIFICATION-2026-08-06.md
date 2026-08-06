# Auditor Verification — I4 Import Guard and S7 CSS Fix (2026-08-06)

## S7 CSS — PASS

Verified `builder/app-v3.15.0-fixed.html`:

- one application `:root` theme block (line 13) and existing `html[data-theme="light"]` override (line 66);
- one unscoped body rule, owned by the application (line 95): `background:var(--bg); color:var(--ink)`;
- S7 component rules are scoped and use application variables; no wholesale designer `body` or second `:root` reset is present (comments/rules around lines 312–395).

This addresses the blank/black rendering failure caused by wholesale designer CSS. The B8 evidence hash is `d7a3553481e8f10b12c1e26c0fa0fbbf`.

## I4 venue guard — PASS (static import-path verification)

Verified `builder/app-v3.15.0-fixed.html`:

1. The patched validation path builds venue holds (lines 2505–2529) for never-hosted-anywhere, never-hosted-in-competition, and known-venue mismatch cases.
2. Each hold is appended to `res.holds`, preserving row data rather than silently flipping it.
3. Import review detects I4 holds (lines 4866–4880), presents official-list / neutral-or-relocated controls, and disables the ordinary approval route until adjudicated.
4. Commit-time defence is present: the code emits `Venue hard block at commit` rather than trusting display-only state.

This is the required Z-003-style two-stage control: validation hold plus commit recheck, with a human confirmation/neutral adjudication route and durable venue rationale. It corrects the earlier failure where `isVenueVerified()` was merely defined/rendered but never connected to ingestion.

**Acceptance:** I4 source/static gate passes in v3.15.0. Browser UAT should still execute the supplied case: import a new stadium for an established home team, observe blocked approval, then confirm via official-list control and verify the durable venue-lock log entry.
