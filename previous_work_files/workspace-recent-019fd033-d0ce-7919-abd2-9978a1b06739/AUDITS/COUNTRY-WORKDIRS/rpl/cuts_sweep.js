/* cuts_sweep.js — CALIBRATION-12 (section #8): full-engine zone cut-point sweep.
   PRE-REGISTERED: objective = actionable (strong+win+windraw) actW AND pair both beat
   shipped 85/65/55/50 in BOTH date-halves. Guardrails: strong W>=80 & n>=7 per half;
   monotone ladder (strong W >= win W >= windraw W); actionable n within 20% of shipped.
   zoneLadder thresholds patched by string replace; gates/gates re-fire naturally. */
const fs = require("fs"), vm = require("vm");
let html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const LADDER = `function zoneLadder(S){
  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "x" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "x" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "x" };
  if (S >= 50) return { key: "lean",    zone: "lean",        note: "x" };
  return { key: "toss", zone: "TOSS", note: "x" };
}`;
const RE = /function zoneLadder\(S\)\{\s*if \(S >= 85\)[\s\S]*?return \{ key: "toss"[^}]*\}\s*;\s*\}/;
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
function run(th) {
  const ladder = `function zoneLadder(S){
  if (S >= ${th.strong}) return { key: "strong",  zone: "STRONG CALL", note: "x" };
  if (S >= ${th.win}) return { key: "win",     zone: "WIN",         note: "x" };
  if (S >= ${th.windraw}) return { key: "windraw", zone: "WIN-DRAW",    note: "x" };
  if (S >= ${th.lean}) return { key: "lean",    zone: "lean",        note: "x" };
  return { key: "toss", zone: "TOSS", note: "x" };
}`;
  const patched = html.replace(RE, ladder);
  if (patched === html) { console.error("ladder patch failed"); process.exit(1); }
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
      "if(!ev||!ev.ag)return null;var z=computeZoneCtx(ev.paths,ev.ag," + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");return {key:z.key,side:z.side};})()");
    if (!r) return;
    out.push({ date: m.date, actual: m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D", zone: r.key, side: r.side });
  });
  fs.writeFileSync("/dev/null", "");
  return out;
}
function evalRun(out) {
  const half = Math.floor(out.length / 2);
  const halves = [out.slice(0, half), out.slice(half)];
  const lead = g => g.side === "TA" ? "H" : "A";
  const won = g => g.actual === lead(g);
  const pair = g => g.actual === lead(g) || g.actual === "D";
  const res = { halves: [], zones: {} };
  halves.forEach(gs => {
    const act = gs.filter(g => ["strong", "win", "windraw"].includes(g.zone));
    res.halves.push({ n: out.indexOf(gs) >= 0 ? gs.length : 0, actN: act.length,
      actW: 100 * act.filter(won).length / Math.max(1, act.length),
      pair: 100 * act.filter(pair).length / Math.max(1, act.length) });
  });
  ["strong", "win", "windraw"].forEach(z => {
    res.zones[z] = halves.map(gs => { const zg = gs.filter(g => g.zone === z);
      return { n: zg.length, W: zg.length ? 100 * zg.filter(won).length / zg.length : null }; });
  });
  return res;
}
const cands = [
  ["shipped 85/65/55/50", { strong: 85, win: 65, windraw: 55, lean: 50 }],
  ["A windraw 60", { strong: 85, win: 65, windraw: 60, lean: 50 }],
  ["B win 70", { strong: 85, win: 70, windraw: 55, lean: 50 }],
  ["C win 70 + windraw 60", { strong: 85, win: 70, windraw: 60, lean: 50 }],
  ["D lean 45", { strong: 85, win: 65, windraw: 55, lean: 45 }],
  ["E strong 80", { strong: 80, win: 65, windraw: 55, lean: 50 }],
  ["F strong 90", { strong: 90, win: 65, windraw: 55, lean: 50 }],
  ["G strong 82 + win 68", { strong: 82, win: 68, windraw: 55, lean: 50 }],
];
console.log(("candidate".padEnd(26) + "|  A actW  A pair (n) |  B actW  B pair (n) | strong W A/B   win W A/B   windraw W A/B | guardrail"));
const results = {};
cands.forEach(([name, th]) => {
  const out = run(th);
  const r = evalRun(out);
  results[name] = { out: out.map(o => [o.date, o.side, o.zone, o.actual]), eval: r };
  const [a, b] = r.halves;
  const sW = r.zones.strong.map(z => z.W === null ? "—" : z.W.toFixed(0)).join("/");
  const wW = r.zones.win.map(z => z.W === null ? "—" : z.W.toFixed(0)).join("/");
  const wdW = r.zones.windraw.map(z => z.W === null ? "—" : z.W.toFixed(0)).join("/");
  const sN = r.zones.strong.map(z => z.n).join("/");
  console.log(name.padEnd(26) + "|  " + a.actW.toFixed(1).padStart(5) + "  " + a.pair.toFixed(1).padStart(5) + "  (" + String(a.actN).padStart(3) + ")" +
    " |  " + b.actW.toFixed(1).padStart(5) + "  " + b.pair.toFixed(1).padStart(5) + "  (" + String(b.actN).padStart(3) + ")" +
    " | s " + sW + "(n" + sN + ")  w " + wW + "  wd " + wdW + " |");
});
fs.writeFileSync("/home/user/rpl/cuts_sweep.json", JSON.stringify(results));
