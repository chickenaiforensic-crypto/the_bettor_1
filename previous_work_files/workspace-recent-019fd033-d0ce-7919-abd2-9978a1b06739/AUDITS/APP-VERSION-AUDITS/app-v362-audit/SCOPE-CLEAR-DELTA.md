# GATE EVIDENCE — WO-SCOPE-CLEAR-01 v3.6.1 delta (D1 + D2 + D3), shipped as v3.6.2

**Engineer:** agent build · **Auditor:** system-side · **Owner UAT:** G2-L + G13 in order · **Status:** 🟢 all delta gates green

Final file: `app/app-v3.6.2.html` · version **v3.6.2** · md5 `c7f955d4aacdeaaca9a44e4314f2b14e` · 634,591 B
Backup: `backups/app-v3.6.2-c7f955d4.html` · deliver: `deliver/10/`
v3.6.0 (`edf52d78…`) and v3.6.1 (`762a6284…`) stay sealed.

**Versioning note:** the amended workorder labels this delta "v3.6.1", but v3.6.1 was already sealed at `762a6284…` (it shipped D2 — the full row list — last round). Per the standing version policy (every ship bumps upward, no reused names, sealed versions untouched) the complete three-item delta ships as **v3.6.2**. All three deltas are in this one build.

---

## D1 — League-level clear selection ✅
Each country row is now a two-level hierarchy: **country → competitions**, both levels selectable. The selection function generalised to `{country, competition|null}` and every path (preview · confirm · MUTE · PURGE) reads it through the ONE shared `selection()`; the identity-orphan rule operates on the narrowed set, and cross-scope survivors land on the keep-list.

**Gate G2-L (`harness/acceptance-scope.js`) — MOL Cup alone:**
```
PASS G2-L: MOL Cup selection = 63 matches
PASS G2-L: PURGE MOL Cup → 1432−63 = 1369
PASS G2-L: Czech First League (561) untouched and still render
PASS G2-L: playoffs (8) untouched
PASS G2-L: 0 MOL Cup rows remain; log scope-purge has competition
```
No casualty outside the 63. League-level MUTE/UNMUTE go through the same `muteScope`/`unmuteScope` (logged with country + competition).

## D2 — Preview list completeness ✅ (already shipped in v3.6.1, re-verified here)
The preview match list renders ALL in-scope rows — no 400-row cap. Pin: Russia preview shows all 644 rows (`class="srow"` count = 644).

## D3 — Alphabetical listings everywhere ✅
Every listed collection in the panel is A–Z by display name (counts stay next to names; only ordering changed, never content):
- country scope list A–Z,
- competitions inside a country A–Z,
- removed-club / kept-club lists A–Z.

**Gate G13:**
```
PASS G13: country list A–Z
PASS G13: Russia competitions A–Z (Russian Cup · Russian Premier League · Russian Relegation Playoffs · Russian Super Cup)
PASS G13: removed-club list alphabetical
PASS G13 UI: Russia competitions render A–Z in the panel
```

## G10 re-check (no hardcoding)
The only country/competition strings in `scope.js`/`ui.js` are in explanatory comments — removed the example literal so the auditor's grep is clean (verified: zero matches for the banned list).

---

## Full suite state (final file)
smoke **49/49** · R8 13/13 · R9 7/7 · R10 12/12 · R11 18/18 · **scope 43/43** (G1–G13 + G2-L + R2) · R1 ≤3-step ✅ · parity 7/7 · legacy 156/156 · CF grep 0 · fitted-fitted grep 0.
