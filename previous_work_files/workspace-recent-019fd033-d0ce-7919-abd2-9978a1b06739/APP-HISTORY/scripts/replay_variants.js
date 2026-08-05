/* replay_variants.js — Candidate A tuning: venue-correction (H2H_HFA) x saturation (H2H_SAT_FULL).
   Each variant is the REAL v2.7.0 engine with constants string-patched, replayed on the
   same 671-game masked universe (cutoff = match date; strict causality).
   Zones computed by the engine's own computeZone (v0.2 anchors 85/65/55/50 + C2 gate),
   so variants are comparable like-for-like. Baseline V0 must reproduce the v2.6.9 curve. */
const fs = require("fs");
const vm = require("vm");
const html0 = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");

function boot(html) {
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
  return sandbox;
}

function loadUniverse(S) {
  const evX = e => vm.runInContext(e, S);
  ["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
    S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
    evX("BlueprintEmbed.importData()");
  });
  const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
  const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
  const st = S.BlueprintEmbed.store();
  [...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
  RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
  return st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
}

function run(tag, html) {
  const S = boot(html);
  const evX = e => vm.runInContext(e, S);
  const matches = loadUniverse(S);
  const bins = {}, zones = {}, pocket = { n: 0, w: 0, d: 0, l: 0 };
  let nocall = 0, total = 0;
  matches.forEach(m => {
    if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
    total++;
    const ev = S.BlueprintEmbed.analyze(m.homeId, m.awayId, m.date);
    const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
    if (!ev || !ev.ag) { nocall++; return; }
    const g = ev.ag;
    const hP = 100 * g.homeW / g.totalWeight, aP = 100 * g.awayW / g.totalWeight;
    const leader = hP >= aP ? "H" : "A";
    const S_ = Math.max(hP, aP);
    const bin = Math.min(95, Math.floor(S_ / 5) * 5);
    if (!bins[bin]) bins[bin] = { n: 0, leadWin: 0, draw: 0, oppWin: 0 };
    bins[bin].n++; if (actual === leader) bins[bin].leadWin++; else if (actual === "D") bins[bin].draw++; else bins[bin].oppWin++;
    if (S_ >= 95) { pocket.n++; if (actual === leader) pocket.w++; else if (actual === "D") pocket.d++; else pocket.l++; }
    const z = evX("computeZone")(ev.paths, g) || null;
  });
  return { total, nocall, bins, pocket };
}
/* computeZone via evX returns the function object — call it inside the context instead */
function run2(tag, html) {
  const S = boot(html);
  const matches = loadUniverse(S);
  const bins = {}, zones = {}, pocket = { n: 0, w: 0, d: 0, l: 0 };
  let nocall = 0, total = 0;
  matches.forEach(m => {
    if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
    total++;
    const r = vm.runInContext(
      "(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
      "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);return {h:ev.ag.homeW,d:ev.ag.neuW,a:ev.ag.awayW,tw:ev.ag.totalWeight,key:z.key,gated:!!z.gatedFrom};})()", S);
    const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
    if (!r) { nocall++; return; }
    const hP = 100 * r.h / r.tw, aP = 100 * r.a / r.tw;
    const leader = hP >= aP ? "H" : "A";
    const S_ = Math.max(hP, aP);
    const bin = Math.min(95, Math.floor(S_ / 5) * 5);
    if (!bins[bin]) bins[bin] = { n: 0, leadWin: 0, draw: 0, oppWin: 0 };
    bins[bin].n++; if (actual === leader) bins[bin].leadWin++; else if (actual === "D") bins[bin].draw++; else bins[bin].oppWin++;
    if (S_ >= 95) { pocket.n++; if (actual === leader) pocket.w++; else if (actual === "D") pocket.d++; else pocket.l++; }
    const key = r.key + (r.gated ? "-gated" : "");
    zones[key] = zones[key] || { n: 0, w: 0, d: 0, l: 0 };
    zones[key].n++; if (actual === leader) zones[key].w++; else if (actual === "D") zones[key].d++; else zones[key].l++;
  });
  console.log("\n=== " + tag + "  (evidence " + (total - nocall) + " / " + total + ", NO CALL " + nocall + ") ===");
  console.log("S bin  | n    | leadW% | D%   | L%");
  Object.keys(bins).sort((a, b) => a - b).forEach(b => {
    const z = bins[b];
    console.log((b + "-" + (+b + 5)).padEnd(6), "|", String(z.n).padEnd(4), "|", (100 * z.leadWin / z.n).toFixed(0).padStart(4) + "%", "|", (100 * z.draw / z.n).toFixed(0).padStart(3) + "%", "|", (100 * z.oppWin / z.n).toFixed(0).padStart(3) + "%");
  });
  console.log("pocket S>=95:", JSON.stringify(pocket), pocket.n ? "leadW " + (100 * pocket.w / pocket.n).toFixed(0) + "%" : "");
  console.log("zones (post-gate): key       | n    | leadW% | D%  | L%  | w-or-d%");
  ["strong", "strong-gated", "win", "win-gated", "windraw", "windraw-gated", "lean", "toss"].forEach(k => {
    const z = zones[k]; if (!z) return;
    console.log("              " + k.padEnd(10), "|", String(z.n).padEnd(4), "|", (100 * z.w / z.n).toFixed(0).padStart(4) + "%", "|", (100 * z.d / z.n).toFixed(0).padStart(3) + "%", "|", (100 * z.l / z.n).toFixed(0).padStart(3) + "%", "|", (100 * (z.w + z.d) / z.n).toFixed(0).padStart(3) + "%");
  });
}

const V = {
  "V0 baseline (v2.6.9 behaviour: HFA 0, no saturation)": [["var H2H_HFA=0.35;", "var H2H_HFA=0;"], ["var H2H_SAT_FULL=2;", "var H2H_SAT_FULL=1000;"]],
  "V1 venue-only (HFA 0.35, no saturation)": [["var H2H_SAT_FULL=2;", "var H2H_SAT_FULL=1000;"]],
  "V2 candidate (HFA 0.35, SAT 2)": [],
  "V3 loose saturation (HFA 0.35, SAT 3)": [["var H2H_SAT_FULL=2;", "var H2H_SAT_FULL=3;"]],
  "V4 strong venue (HFA 0.50, SAT 2)": [["var H2H_HFA=0.35;", "var H2H_HFA=0.50;"]]
};
Object.keys(V).forEach(tag => {
  let h = html0;
  V[tag].forEach(([a, b]) => { if (!h.includes(a)) throw new Error("patch anchor missing: " + a); h = h.replace(a, b); });
  run2(tag, h);
});
