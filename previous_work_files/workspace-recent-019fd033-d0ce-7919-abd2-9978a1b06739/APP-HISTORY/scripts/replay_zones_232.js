/* replay_zones.js — masked-replay calibration run for the zone instrument.
   671 games: 61 UECL/domestic pack rows + 610 RPL universe rows.
   Each game replayed blind (cutoff = its own date; strict causality).
   Per game: evidence summation H/D/A (engine buckets, sum 100) + per-section shares.
   Output: CSV log + leader-share hit-rate curve + tuned zone anchors. */
const fs = require("fs");
const vm = require("vm");
let html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8").replace("var PHASE_WEIGHT = {h2h:3, common:2, third:1.5};", "var PHASE_WEIGHT = {h2h:2, common:3, third:1.5};"); console.log("patched weights h2h2/common3/third1.5:", html.indexOf("h2h:2, common:3") >= 0);
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
const els = {}, sandbox = {};
sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _s = {};
sandbox.localStorage = { getItem: k => (k in _s ? _s[k] : null), setItem: (k, v) => { _s[k] = String(v); }, removeItem: k => { delete _s[k]; } };
const md = makeEl("matchDate");
md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = md;
sandbox.document = { readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(t) { return makeEl(t + Math.random()); },
  querySelector(s) { return makeEl(s); }, querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sandbox);
scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "s" + i }));
const S = sandbox, evX = e => vm.runInContext(e, sandbox);

["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const st = S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
const nameOf = id => (st.identities[id] && st.identities[id].name) || id;
const matches = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
console.log("universe rows:", matches.length);

const out = ["date,fixture,hPct,dPct,aPct,leader,leaderShare,actual,h2hH,h2hD,h2hA,comH,comD,comA,thirdH,thirdD,thirdA,paths,effective"];
const bins = {};
for (let b = 35; b < 100; b += 5) bins[b] = { n: 0, leadWin: 0, draw: 0, oppWin: 0 };
const bySrc = { UEFA: { n: 0, nocall: 0 }, RPL: { n: 0, nocall: 0 } };
const secStats = { h2h: {}, common: {}, third: {} }; // lead-share buckets per section: [40,60,75] -> n, hit
let nocall = 0, total = 0;
matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  total++;
  const src = m.competition === "RPL" ? "RPL" : "UEFA";
  const ev = S.BlueprintEmbed.analyze(m.homeId, m.awayId, m.date);
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  if (!ev || !ev.ag) { nocall++; bySrc[src === "RPL" ? "RPL" : "UEFA"].nocall++; return; }
  bySrc[src].n++;
  const g = ev.ag;
  const hP = 100 * g.homeW / g.totalWeight, dP = 100 * g.neuW / g.totalWeight, aP = 100 * g.awayW / g.totalWeight;
  const leader = hP >= aP ? "H" : "A";
  const S_ = Math.max(hP, aP);
  const bin = Math.min(95, Math.floor(S_ / 5) * 5);
  if (bins[bin]) { bins[bin].n++; if (actual === leader) bins[bin].leadWin++; else if (actual === "D") bins[bin].draw++; else bins[bin].oppWin++; }
  const ph = { h2h: [0, 0, 0], com: [0, 0, 0], third: [0, 0, 0] };
  (ev.paths || []).forEach(p => {
    const k = p.phase === "h2h" ? "h2h" : p.phase === "common" ? "com" : "third";
    if (p.estimate > 0) ph[k][0] += p.weight; else if (p.estimate < 0) ph[k][2] += p.weight; else ph[k][1] += p.weight;
  });
  const pct = t => { const s = t[0] + t[1] + t[2]; return s ? [100 * t[0] / s, 100 * t[1] / s, 100 * t[2] / s] : [0, 0, 0]; };
  const sH2H = pct(ph.h2h), sC = pct(ph.com), sT = pct(ph.third);
  // per-section: when a section leads at >=60% share, does the leader win?
  [["h2h", sH2H], ["common", sC], ["third", sT]].forEach(([k, s]) => {
    const l = Math.max(s[0], s[2]); const side = s[0] >= s[2] ? "H" : "A";
    if (l < 55) return;
    const b = l >= 75 ? "75+" : l >= 60 ? "60-75" : "55-60";
    const o = (secStats[k][b] = secStats[k][b] || { n: 0, leadWin: 0, draw: 0, oppWin: 0 });
    o.n++; if (actual === side) o.leadWin++; else if (actual === "D") o.draw++; else o.oppWin++;
  });
  out.push([m.date, nameOf(m.homeId).slice(0, 18) + " v " + nameOf(m.awayId).slice(0, 18),
    hP.toFixed(1), dP.toFixed(1), aP.toFixed(1), leader, S_.toFixed(1), actual,
    ...sH2H.map(x => x.toFixed(0)), ...sC.map(x => x.toFixed(0)), ...sT.map(x => x.toFixed(0)),
    (ev.paths || []).length, g.effective].join(","));
});
fs.writeFileSync("/home/user/replay_zones_log_232.csv", out.join("\n") + "\n");
console.log("\ngames with evidence:", out.length - 1, "| NO CALL (no evidence, discipline):", nocall, "| total:", total);
console.log("by source:", JSON.stringify(bySrc));

console.log("\n=== LEADER-SHARE CURVE (all games with evidence) ===");
console.log("S bin  | n   | leader won | draw | opp won | leader-win% | leader-or-draw%");
Object.keys(bins).forEach(b => {
  const z = bins[b]; if (!z.n) return;
  console.log((b + "-" + (+b + 5)).padEnd(6), "|", String(z.n).padEnd(4), "|", String(z.leadWin).padEnd(10), "|", String(z.draw).padEnd(4), "|", String(z.oppWin).padEnd(8), "|", (100 * z.leadWin / z.n).toFixed(0) + "%".padEnd(12), "|", (100 * (z.leadWin + z.draw) / z.n).toFixed(0) + "%");
});

console.log("\n=== PER-SECTION leader-share hit rates (section leads >=55%) ===");
["h2h", "common", "third"].forEach(k => {
  Object.keys(secStats[k]).sort().forEach(b => {
    const o = secStats[k][b];
    console.log(k, b, "| n=" + o.n, "| leader won", o.leadWin, "| draw", o.draw, "| opp won", o.oppWin, "| win%", (100 * o.leadWin / o.n).toFixed(0), "| w-or-d%", (100 * (o.leadWin + o.draw) / o.n).toFixed(0));
  });
});
