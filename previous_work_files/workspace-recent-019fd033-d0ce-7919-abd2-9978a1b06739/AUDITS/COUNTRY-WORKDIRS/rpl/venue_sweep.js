/* venue_sweep.js — CALIBRATION-10 (section #6: venueFactor). Replays 633 games with
   venueFactor patched to different tiers for relocated/neutral/unknown. Measures:
   games where raw engine output changes at all, zone flips, actW/pair vs actual. */
const fs = require("fs"), vm = require("vm");
let html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const VF_LINE = "  function venueFactor(v){v=norm(v); if(v==='normal'||v==='home'||v==='club-home')return 1; if(v==='relocated'||v==='partial-home')return 0.75; if(v==='neutral')return 0.55; return 0.75;}";
if (html.indexOf(VF_LINE) < 0) { console.error("venueFactor line not found - abort"); process.exit(1); }

function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
function run(fRE, fNE, fUN) {
  const patched = html.replace(VF_LINE,
    `  function venueFactor(v){v=norm(v); if(v==='normal'||v==='home'||v==='club-home')return 1; if(v==='relocated'||v==='partial-home')return ${fRE}; if(v==='neutral')return ${fNE}; return ${fUN};}`);
  const scripts = [...patched.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
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
    createElement(t) { return makeEl(t + Math.random()); }, querySelector(s) { return makeEl(s); },
    querySelectorAll() { return []; }, addEventListener() {} };
  vm.createContext(sandbox);
  scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "s" + i }));
  const S = sandbox, evX = e => vm.runInContext(e, S);
  ["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
    S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
    evX("BlueprintEmbed.importData()");
  });
  const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
  const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
  const st = S.BlueprintEmbed.store();
  [...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
  RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home", muted: m.muted || undefined }));
  const matches = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
  const out = [];
  matches.forEach(m => {
    if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
    const r = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
      "if(!ev||!ev.ag)return null;var ag=ev.ag;var z=computeZoneCtx(ev.paths,ag," + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
      "var tw=ag.homeW+ag.neuW+ag.awayW;" +
      "var touched=ev.paths.some(function(p){return p.phase==='h2h' && p.weight < 2.99;});" +
      "return {key:z.key,side:z.side,S:+z.S_.toFixed(3),H:ag.homeW/tw*100,D:ag.neuW/tw*100,A:ag.awayW/tw*100,w:+ag.weighted.toFixed(4),t:touched,nh2h:(ag.phaseCounts&&ag.phaseCounts.h2h)||0};})()");
    if (!r) return;
    out.push({ date: m.date, actual: m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D", ...r });
  });
  return out;
}
const variants = [
  ["shipped 0.75/0.55/0.75", 0.75, 0.55, 0.75],
  ["all 1.00 (no venue discount)", 1, 1, 1],
  ["harder 0.50/0.30/0.50", 0.5, 0.30, 0.5],
  ["halved-power 0.85/0.75/0.85", 0.85, 0.75, 0.85]
];
const runs = variants.map(v => [v[0], run(v[1], v[2], v[3])]);
const base = runs[0][1];
console.log("games per run:", runs.map(r => r[1].length).join("/"));
function acc(games) {
  let actW = 0, actN = 0, pairW = 0, pairN = 0;
  games.forEach(g => {
    const lead = g.side === "TA" ? "H" : "A";
    const actionable = g.key !== "toss" && g.key !== "lean";
    if (actionable) { actN++; if (g.actual === lead) { actW++; pairW++; } else if (g.actual === "D") pairW++; pairN++; }
  });
  return { actW: 100 * actW / actN, pair: 100 * pairW / actN, n: actN };
}
console.log("\nrun                                    changed vs shipped   zone flips   actW/pair (actionable)");
runs.forEach(([name, gms]) => {
  let changed = 0, flips = 0;
  if (gms !== base) gms.forEach((g, i) => {
    const b = base[i];
    if (Math.abs(g.H - b.H) > 0.05 || Math.abs(g.D - b.D) > 0.05 || Math.abs(g.A - b.A) > 0.05 || Math.abs(g.w - b.w) > 1e-6) changed++;
    if (g.key !== b.key || g.side !== b.side) flips++;
  });
  const a = acc(gms);
  console.log("  " + name.padEnd(36) + String(changed).padStart(8) + String(flips).padStart(12) +
    "   " + a.actW.toFixed(1) + " / " + a.pair.toFixed(1) + "  n=" + a.n);
});
const touched = base.filter(g => g.t);
console.log("\ngames where a discounted H2H evidence path exists:", touched.length);
touched.forEach(t => console.log("   ", t.date, "zone=" + t.key, t.side, "S=" + t.S, "h2hN=" + t.nh2h, "actual=" + t.actual));
fs.writeFileSync("/home/user/rpl/venue_sweep.json", JSON.stringify({ variants: runs.map(r => r[0]), base: base, touched: touched }));
