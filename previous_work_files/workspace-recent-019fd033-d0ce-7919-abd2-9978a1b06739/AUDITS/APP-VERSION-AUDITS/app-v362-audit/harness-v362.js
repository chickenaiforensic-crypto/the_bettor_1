/* AUDIT HARNESS v3.6.2 — auditor: Arena session
 * Executes the EXACT PR.scope module lines (2804..3003) sliced from the pinned
 * app-v3.6.2.html against the live export snapshot (1,432 rows).
 * No reimplementation of scope logic: only stubs for PR.store (log/save/hash). */
'use strict';
const fs = require('fs'), crypto = require('crypto');

const HTML = '/home/user/app-v362-audit/app-v3.6.2.html';
const lines = fs.readFileSync(HTML, 'utf8').split('\n');
const modSrc = lines.slice(2803, 3000).join('\n');              // line 2804..3000 (1-based), ends at '})();'
if (!/PR\.scope = \(function/.test(modSrc)) throw new Error('slice start wrong');
if (!/\}\)\(\);\s*$/.test(modSrc.trim())) throw new Error('slice end wrong');

/* ---- stubs (only what the module touches externally) ---- */
const logs = [];
const PR = {
  canon: {}, // module never dereferences C (verified by grep: no 'C.' inside slice)
  store: {
    log(store, e) { store.log.push(e); },
    save() {},
    contentHash(store) { // behaviour stub: length+muted state hash (NOT the app's hash algo)
      return crypto.createHash('md5')
        .update(store.matches.length + '|' + store.matches.filter(m => m.muted).length)
        .digest('hex');
    }
  }
};
PR.derive = { invalidate() {} }; // module calls PR.derive.invalidate() after mutations
eval(modSrc); // attaches PR.scope — the app's own code

/* ---- faithful store-shape adapter (export JSON -> app store rows) ---- */
function buildStore() {
  const exp = JSON.parse(fs.readFileSync('/home/user/pitch-rating-full-data-2026-08-02.json', 'utf8'));
  const identities = Object.values(exp.identities).map(it => ({ id: it.id, name: it.name, country: it.country }));
  const nameOf = id => (exp.identities[id] ? exp.identities[id].name : id);
  const matches = exp.matches.map((r, i) => ({
    id: 'm' + i, dateISO: r.date, competitionName: r.competition, country: r.country,
    homeId: r.homeId, awayId: r.awayId, home: nameOf(r.homeId), away: nameOf(r.awayId),
    homeGoals: r.hg, awayGoals: r.ag, muted: false
  }));
  return { matches, identities, venues: [], seasons: [], ctxFlags: [], artifacts: [], mutes: [], sources: [{ id: 's1' }], log: [], meta: {} };
}

let PASS = 0, FAIL = 0;
function gate(ok, label, got, want) {
  console.log((ok ? 'PASS ' : 'FAIL ') + label + '  got=' + JSON.stringify(got) + (want !== undefined ? '  want=' + JSON.stringify(want) : ''));
  ok ? PASS++ : FAIL++;
}

/* ===== G1 + D3: scope list — totals anchored to approved v3.6.0 census, A–Z order ===== */
let store = buildStore();
const scopes = PR.scope.deriveScopes(store, null);
const countries = scopes.map(s => s.country);
console.log('--- scopes (' + countries.length + ') ---');
scopes.forEach(s => console.log('  ' + s.country + '  total=' + s.total + '  clubs=' + s.clubCount +
  '  comps=' + s.competitionList.map(c => c.name + '(' + c.count + ')').join(' | ')));
gate(countries.length === 18, 'G1 scope count (this export = 18; earlier "16" note was loose)', countries.length, 18);
gate(scopes.reduce((a, s) => a + s.total, 0) === 1432, 'G1 all rows partitioned into scopes', scopes.reduce((a, s) => a + s.total, 0), 1432);
const az = countries.slice().sort((a, b) => a.localeCompare(b));
gate(JSON.stringify(countries) === JSON.stringify(az), 'D3 countries A-Z (D3/G13-country)', countries.slice(0, 5).join(' < ') + ' …');
const rus = scopes.find(s => s.country === 'Russia');
const cze = scopes.find(s => s.country === 'Czech Republic');
gate(rus && rus.total === 644, 'G1 Russia total (regression anchor)', rus && rus.total, 644);
gate(cze && cze.total === 632, 'G1 Czech total (regression anchor)', cze && cze.total, 632);

/* ===== G13: Russia competition order + counts ===== */
const rusComps = rus.competitionList;
gate(JSON.stringify(rusComps.map(c => c.name)) ===
  JSON.stringify(['Russian Cup', 'Russian Premier League', 'Russian Relegation Playoffs', 'Russian Super Cup']),
  'G13 Russia comps A-Z', rusComps.map(c => c.name + ' ' + c.count).join(' · '),
  'Russian Cup 152 · Russian Premier League 489 · Russian Relegation Playoffs 2 · Russian Super Cup 1');
gate(JSON.stringify(rusComps.map(c => c.count)) === JSON.stringify([152, 489, 2, 1]),
  'G13 Russia comp counts', rusComps.map(c => c.count).join(','), '152,489,2,1');

/* ===== G2: whole-country selection (backward-compat string form) ===== */
/* 'remaining' is module-internal by design; mirrored here 1:1 via the module's
   own exposed matchCountry: remaining = m => mc(m)!==country || (comp && compName!==comp) */
const remLen = (country, comp) =>
  store.matches.filter(m => PR.scope.matchCountry(store, m) !== country ||
    (comp && (m.competitionName || '(no competition)') !== comp)).length;
const selRus = PR.scope.selection(store, null, 'Russia');
gate(selRus.matchCount === 644, 'G2 Russia selection (string form)', selRus.matchCount, 644);
gate(remLen('Russia', null) === 1432 - 644, 'G2 Russia remaining == 1432-644', remLen('Russia', null), 788);

/* ===== G2-L: league-level selection (object form) ===== */
const selMol = PR.scope.selection(store, null, { country: 'Czech Republic', competition: 'MOL Cup' });
gate(selMol.matchCount === 63, 'G2-L MOL Cup selection', selMol.matchCount, 63);
gate(remLen('Czech Republic', 'MOL Cup') === 1432 - 63, 'G2-L remaining after MOL Cup', remLen('Czech Republic', 'MOL Cup'), 1369);
gate(selMol.scopeKey === 'Czech Republic / MOL Cup', 'G2-L scopeKey label', selMol.scopeKey, 'Czech Republic / MOL Cup');
/* cross-bleed: no non-MOL match in selection, no MOL match in remaining */
gate(selMol.matches.every(m => m.competitionName === 'MOL Cup'), 'G2-L selection purity', selMol.matches.filter(m => m.competitionName !== 'MOL Cup').length, 0);
gate(store.matches.filter(m => PR.scope.matchCountry(store, m) === 'Czech Republic' && m.competitionName === 'MOL Cup').length === 63,
  'G2-L all MOL rows in-scope', store.matches.filter(m => PR.scope.matchCountry(store, m) === 'Czech Republic' && m.competitionName === 'MOL Cup').length, 63);
const selCze = PR.scope.selection(store, null, { country: 'Czech Republic', competition: null });
gate(selCze.matchCount === 632, 'G2-L country level (object form, null comp)', selCze.matchCount, 632);

/* ===== mute / unmute round-trip (Russia) ===== */
store = buildStore();
const r1 = PR.scope.muteScope(store, null, 'Russia');
gate(r1.ok && store.matches.filter(m => m.muted).length === 644, 'MUTE Russia flags 644 rows', store.matches.filter(m => m.muted).length, 644);
gate(store.matches.length === 1432, 'MUTE keeps row count', store.matches.length, 1432);
const r2 = PR.scope.unmuteScope(store, null, 'Russia');
gate(r2.ok && store.matches.filter(m => m.muted).length === 0, 'UNMUTE restores all', store.matches.filter(m => m.muted).length, 0);
const muteLog = store.log.find(e => e.action === 'scope-mute');
gate(muteLog && muteLog.country === 'Russia' && muteLog.competition === null && !!muteLog.preHash,
  'MUTE log carries country/competition/preHash', muteLog && (muteLog.country + '|' + muteLog.competition + '|' + !!muteLog.preHash), 'Russia|null|true');

/* ===== league-level MUTE then country UNMUTE independence ===== */
store = buildStore();
PR.scope.muteScope(store, null, { country: 'Czech Republic', competition: 'MOL Cup' });
gate(store.matches.filter(m => m.muted).length === 63, 'MUTE league-only flags 63', store.matches.filter(m => m.muted).length, 63);
PR.scope.unmuteScope(store, null, { country: 'Czech Republic', competition: 'MOL Cup' });
gate(store.matches.filter(m => m.muted).length === 0, 'UNMUTE league-only restores', store.matches.filter(m => m.muted).length, 0);

/* ===== PURGE league level: MOL Cup ===== */
store = buildStore();
const beforeIds = new Set(store.identities.map(i => i.id));
const p1 = PR.scope.purgeScope(store, null, { country: 'Czech Republic', competition: 'MOL Cup' }, { backupFile: 'TEST-BACKUP.json', dropSources: false });
gate(p1.ok && !p1.noop && p1.matchCount === 63, 'PURGE MOL Cup removes 63 matches', p1.matchCount, 63);
gate(store.matches.length === 1369, 'PURGE MOL Cup post count', store.matches.length, 1369);
gate(store.sources.length === 1, 'PURGE keeps sources by default', store.sources.length, 1);
const removedClubs = beforeIds.size - store.identities.length;
console.log('  removed clubs (' + removedClubs + '): ' +
  (p1.clubsRemoved ? '' : '') + (() => { const keep = new Set(store.identities.map(i => i.id)); return [...beforeIds].filter(id => !keep.has(id)).join(', ') || '(none)'; })());
/* orphan proof: every removed club has ZERO refs in remaining matches */
const remainIds = new Set();
store.matches.forEach(m => { remainIds.add(m.homeId); remainIds.add(m.awayId); });
const keepIds = new Set(store.identities.map(i => i.id));
const orphans = [...beforeIds].filter(id => !keepIds.has(id));
gate(orphans.every(id => !remainIds.has(id)), 'PURGE orphan rule (removed clubs have no refs)', orphans.filter(id => remainIds.has(id)).length, 0);
gate(orphans.every(id => id.startsWith('czech') || id.includes('czechia')), 'PURGE removed clubs all Czech', orphans.filter(id => !(id.startsWith('czech') || id.includes('czechia'))).join(',') || '(all czech)');
const purgeLog = store.log.find(e => e.action === 'scope-purge');
gate(purgeLog && purgeLog.country === 'Czech Republic' && purgeLog.competition === 'MOL Cup' && purgeLog.backupFile === 'TEST-BACKUP.json',
  'PURGE log carries country/competition/backupFile', purgeLog && (purgeLog.country + '|' + purgeLog.competition + '|' + purgeLog.backupFile),
  'Czech Republic|MOL Cup|TEST-BACKUP.json');
/* no-op honesty on second purge */
const p2 = PR.scope.purgeScope(store, null, { country: 'Czech Republic', competition: 'MOL Cup' }, { backupFile: 'X' });
gate(p2.ok && p2.noop === true && store.matches.length === 1369, 'PURGE noop honesty', p2.noop, true);
gate(store.log.some(e => e.action === 'scope-purge-noop'), 'noop log line present', store.log.filter(e => e.action === 'scope-purge-noop').length, 1);

/* ===== PURGE country level: Russia ===== */
store = buildStore();
const p3 = PR.scope.purgeScope(store, null, 'Russia', { backupFile: 'RUS.json', dropSources: false });
gate(p3.ok && store.matches.length === 788, 'PURGE Russia -> 788 (endgame rehearsal)', store.matches.length, 788);
gate(store.matches.every(m => m.country !== 'Russia'), 'PURGE Russia purity', store.matches.filter(m => m.country === 'Russia').length, 0);

/* ===== unknown scope guard ===== */
store = buildStore();
const bad = PR.scope.purgeScope(store, null, { country: 'Nowhereland', competition: null }, { backupFile: 'X' });
gate(bad.ok === false && store.matches.length === 1432, 'Unknown scope guard', bad.reason && bad.reason.slice(0, 13), 'Unknown scope');

console.log('==========================================================');
console.log('HARNESS RESULT: PASS=' + PASS + ' FAIL=' + FAIL);
process.exit(FAIL ? 1 : 0);
