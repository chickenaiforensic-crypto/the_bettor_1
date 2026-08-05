/* replay_ab_check.js — audit-motive check for Candidate A: TA/TB asymmetry and the
   h2h-driven-only subset, V0 (v2.6.9 behaviour) vs V2 (HFA 0.35 + SAT 2). */
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
  const matches = loadUniverse(S);
  const side = { TA: { strong: { n: 0, w: 0 }, win: { n: 0, w: 0 } }, TB: { strong: { n: 0, w: 0 }, win: { n: 0, w: 0 } } };
  const h2hOnly = { n: 0, w: 0, d: 0, l: 0 };           // h2h section >=75% lead, common absent or <55
  let total = 0, nocall = 0;
  matches.forEach(m => {
    if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
    total++;
    const r = vm.runInContext(
      "(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
      "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);var ss=sectionShares(ev.paths);" +
      "var sec=ss.map(function(s){return {ph:s.phase,side:s.side,lead:s.lead};});" +
      "return {h:ev.ag.homeW,d:ev.ag.neuW,a:ev.ag.awayW,tw:ev.ag.totalWeight,key:z.key,side:z.side,sec:sec,S:z.S_};})()", S);
    const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
    if (!r) { nocall++; return; }
    const leader = r.side === "TA" ? "H" : "A";
    const won = actual === leader;
    if (r.key === "strong" || r.key === "win") {
      side[r.side][r.key].n++; if (won) side[r.side][r.key].w++;
    }
    const h2h = r.sec.find(s => s.ph === "h2h"), com = r.sec.find(s => s.ph === "common");
    if (h2h && h2h.lead >= 75 && (!com || com.lead < 55) && r.S >= 85) {
      h2hOnly.n++;
      h2h.hLead = (h2h.side === "H");
      const h2hWon = actual === (h2h.side === "H" ? "H" : "A");
      if (h2hWon) h2hOnly.w++; else if (actual === "D") h2hOnly.d++; else h2hOnly.l++;
    }
  });
  console.log("\n=== " + tag + " ===");
  ["TA", "TB"].forEach(sd => ["strong", "win"].forEach(k => {
    const z = side[sd][k]; if (!z.n) return;
    console.log(sd + " " + k.toUpperCase().padEnd(6), "n=" + String(z.n).padEnd(4), "win " + (100 * z.w / z.n).toFixed(0) + "%");
  }));
  console.log("TA gap (strong-plus-win pooled):", (() => { const t = side.TA, b = side.TB;
    const ta = 100 * (t.strong.w + t.win.w) / (t.strong.n + t.win.n), tb = 100 * (b.strong.w + b.win.w) / (b.strong.n + b.win.n);
    return "TA " + ta.toFixed(0) + "% vs TB " + tb.toFixed(0) + "%"; })());
  console.log("h2h-driven-only (h2h>=75, common silent, S>=85):", JSON.stringify(h2hOnly), h2hOnly.n ? "leadW " + (100 * h2hOnly.w / h2hOnly.n).toFixed(0) + "%" : "");
}

const V0 = html0.replace("var H2H_HFA=0.35;", "var H2H_HFA=0;").replace("var H2H_SAT_FULL=2;", "var H2H_SAT_FULL=1000;");
run("V0 baseline", V0);
run("V2 Candidate A (HFA 0.35, SAT 2)", html0);
