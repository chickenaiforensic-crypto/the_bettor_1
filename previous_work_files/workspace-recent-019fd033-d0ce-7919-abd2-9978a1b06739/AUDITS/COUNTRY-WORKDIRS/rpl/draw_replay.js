/* draw_replay.js — CALIBRATION-9 (section #5: draw-mass mapping) measurement pass.
   v2.8.7 shipped behavior, 633-game masked replay. Records per game:
   displayed balance shares (H/D/A out of 100), zone (post-gates post-C8 path), EVG2 est, actual result. */
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
    "var g=evidenceGoalsEstimate(ev.paths," + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "var tw=ag.homeW+ag.neuW+ag.awayW;" +
    "return {key:z.key,side:z.side,S:+z.S_.toFixed(4),H:ag.homeW/tw*100,D:ag.neuW/tw*100,A:ag.awayW/tw*100," +
    "est:g?+g.est.toFixed(3):null,npaths:ev.paths.length,eff:ag.effective,agree:+ag.agree.toFixed(4),weighted:+ag.weighted.toFixed(4)};})()");
  if (!r) return;
  out.push({ date: m.date, home: m.homeId, away: m.awayId, hg: m.hg, ag: m.ag,
    actual: m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D",
    zone: r.key, side: r.side, S: r.S, balH: +r.H.toFixed(2), balD: +r.D.toFixed(2), balA: +r.A.toFixed(2),
    est: r.est, npaths: r.npaths, eff: r.eff, agree: r.agree, weighted: r.weighted });
});
fs.writeFileSync("/home/user/rpl/draw_replay.json", JSON.stringify(out));
console.log("games with evidence: " + out.length);
console.log("mean displayed  H " + (out.reduce((a, g) => a + g.balH, 0) / out.length).toFixed(1) +
  " · D " + (out.reduce((a, g) => a + g.balD, 0) / out.length).toFixed(1) +
  " · A " + (out.reduce((a, g) => a + g.balA, 0) / out.length).toFixed(1));
const act = ["H", "D", "A"].map(k => 100 * out.filter(g => g.actual === k).length / out.length);
console.log("actual outcome    H " + act[0].toFixed(1) + " · D " + act[1].toFixed(1) + " · A " + act[2].toFixed(1));
