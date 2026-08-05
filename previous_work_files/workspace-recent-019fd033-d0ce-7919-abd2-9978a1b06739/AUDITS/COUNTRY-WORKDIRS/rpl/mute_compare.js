/* mute_compare.js — INTEGRITY-AUDIT: shipped (no mute) vs muted pool, same v2.8.8 engine.
   Measures zone table, actW/pair (all + halves), 3-way log-loss (raw + CAL9), count of changed games. */
const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
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
function run(tag) {
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
  const RPL = JSON.parse(fs.readFileSync(tag === "mute" ? "/home/user/rpl/rpl_universe.json" : "/tmp/universe_nomute.json", "utf8"));
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
      "var tw=ag.homeW+ag.neuW+ag.awayW;return {key:z.key,side:z.side,S:z.S_,H:ag.homeW/tw,D:ag.neuW/tw,A:ag.awayW/tw};})()");
    if (!r) return;
    out.push({ date: m.date, actual: m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D", zone: r.key, side: r.side, S: r.S, H: r.H, D: r.D, A: r.A });
  });
  return out;
}
function lead(g) { return g.side === "TA" ? "H" : "A"; }
const won = g => g.actual === lead(g);
const pair = g => g.actual === lead(g) || g.actual === "D";
function metrics(out, label) {
  const half = Math.floor(out.length / 2), A = out.slice(0, half), B = out.slice(half);
  const zt = {};
  out.forEach(g => { const z = zt[g.zone] = zt[g.zone] || { n: 0, w: 0, d: 0, l: 0 };
    z.n++; if (won(g)) z.w++; else if (g.actual === "D") z.d++; else z.l++; });
  const act = out.filter(g => ["strong", "win", "windraw"].includes(g.zone));
  const actA = A.filter(g => ["strong", "win", "windraw"].includes(g.zone));
  const actB = B.filter(g => ["strong", "win", "windraw"].includes(g.zone));
  const llr = g => -Math.log(Math.max(g["HDA"["HDA".indexOf(g.actual)] !== undefined ? ["H","D","A"][["H","D","A"].indexOf(g.actual)] : g.H], 1e-9));
  const llDist = (g, f) => { const p = f(g); return -Math.log(Math.max(p, 1e-9)); };
  const llRaw = out.reduce((a, g) => a + llDist(g, x => x[g.actual === "D" ? "D" : g.actual === "H" ? "H" : "A"]), 0) / out.length;
  const llC9 = out.reduce((a, g) => a + llDist(g, x => { const c = [0.6 * x.H * 100 + 15.134, 0.6 * x.D * 100 + 9.732, 0.6 * x.A * 100 + 15.134];
    return c[g.actual === "D" ? 1 : g.actual === "H" ? 0 : 2] / 100; }), 0) / out.length;
  console.log(label, "n=" + out.length);
  ["strong", "win", "windraw", "lean", "toss"].forEach(z => { const t = zt[z]; if (t)
    console.log("   " + z.padEnd(8), "n=" + String(t.n).padEnd(4), "W " + (100 * t.w / t.n).toFixed(0).padStart(2) + "%", "pair " + (100 * (t.w + t.d) / t.n).toFixed(0) + "%"); });
  console.log("   actW " + (100 * act.filter(won).length / act.length).toFixed(1) + " pair " + (100 * act.filter(pair).length / act.length).toFixed(1) + " (n=" + act.length + ")",
    "| A " + (100 * actA.filter(won).length / actA.length).toFixed(1) + "/" + (100 * actA.filter(pair).length / actA.length).toFixed(1),
    "B " + (100 * actB.filter(won).length / actB.length).toFixed(1) + "/" + (100 * actB.filter(pair).length / actB.length).toFixed(1));
  console.log("   3-way ll raw " + llRaw.toFixed(4) + "  CAL9-shrunk " + llC9.toFixed(4));
}
const m0 = run("no-mute"); const m1 = run("mute");
metrics(m0, "BEFORE (no mute):"); metrics(m1, "AFTER  (3 muted):");
let chZ = 0, chS = 0;
m1.forEach((g, i) => { const b = m0[i];
  if (g.zone !== b.zone) chZ++;
  if (g.side !== b.side) chS++; });
console.log("\nzone changes: " + chZ + " of " + m1.length + " | leader side flips: " + chS);
fs.writeFileSync("/home/user/rpl/mute_compare.json", JSON.stringify({ before: m0, after: m1 }));
