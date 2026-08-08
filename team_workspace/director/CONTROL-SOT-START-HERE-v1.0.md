# CONTROL SOT — START HERE v1.0

**Issued:** 2026-08-08
**Use:** Read this before relying on a branch, country pack, chat message, or app country list.

## The one control document

Read first:

```text
Supervior/Build Docs/DIRECTOR-CONTROL-SOT-v1.0.md
```

It is the current Director authority for what is approved, returned, rejected, or unverified.

## Country-pack rule

A country appearing in the app does not mean it is approved.

Read:

```text
Supervior/Build Docs/APP-EMBEDDED-SEED-REGISTER-v1.0.md
```

Wales, Slovenia, and every country listed only there are unapproved partial embedded records.

## Safe data rule

Only these scopes are currently approved in the verified 5,082-row store:

```text
England Premier League
Russia: RPL, Cup, playoffs, Super Cup
Czechia: First League, MOL Cup, playoffs
```

Everything else requires its own accessible pack, hash, independent auditor report, and status update in the Director control register.

## Runtime rule

The current v3.17 app automatically loads unapproved embedded seeds on a first boot. It is not a clean production data boot.

Use the clean-boot builder workorder before presenting a fresh app as production-ready:

```text
team_workspace/builder/WORKORDER-BUILDER-CLEAN-BOOT-QUARANTINE-v1.0.md
```
