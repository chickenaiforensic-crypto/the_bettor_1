/* zone_tally.js — final shipped-behavior tally: post-gate + C5 zone table on the 600-game replay. */
const fs = require("fs");
const vm = require("vm");
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
const S = sandbox, evX = e => vm.runInContext(e, S);
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json", "utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json", "utf8"));
const st = S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m => [m.home, m.away]))].forEach(s => { if (!st.identities[s]) st.identities[s] = { id: s, name: NAMES[s] || s }; });
RPL.forEach(m => st.matches.push({ id: [m.date, m.comp, m.home, m.away, m.hg, m.ag, "home"].join("|"), date: m.date, competition: m.comp, homeId: m.home, awayId: m.away, hg: m.hg, ag: m.ag, venue: "home" }));
const matches = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
const zones = {};
let n = 0;
matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  const r = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);return {key:z.key,side:z.side};})()");
  if (!r) return;
  n++;
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  const leader = r.side === "TA" ? "H" : "A";
  zones[r.key] = zones[r.key] || { n: 0, w: 0, d: 0, l: 0 };
  zones[r.key].n++; if (actual === leader) zones[r.key].w++; else if (actual === "D") zones[r.key].d++; else zones[r.key].l++;
});
console.log("SHIPPED v2.7.1 zone table (" + n + " games with evidence):");
["strong", "win", "windraw", "lean", "toss"].forEach(k => {
  const z = zones[k]; if (!z) return;
  console.log("  " + k.padEnd(8), "n=" + String(z.n).padEnd(4),
    "W " + (100 * z.w / z.n).toFixed(0).padStart(2) + "%",
    "D " + (100 * z.d / z.n).toFixed(0).padStart(2) + "%",
    "L " + (100 * z.l / z.n).toFixed(0).padStart(2) + "%",
    "pair " + (100 * (z.w + z.d) / z.n).toFixed(0) + "%");
});
