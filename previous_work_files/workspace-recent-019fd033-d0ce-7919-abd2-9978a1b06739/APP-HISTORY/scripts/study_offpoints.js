/* study_offpoints.js — next-category calibration study (user order: after Clear Win,
   study the off-points: WIN/STRONG zone draws and losses; learn the weak-link signatures;
   loss-side calibration should feed back into the clean-win section).
   Runs on the SHIPPED v2.6.9-math engine (Candidate A rejected). Pools = post-gate zones.
   Pre-declared hypotheses H1-H6; a proposal ships only if it beats its pool on signal AND n. */
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
const nameOf = id => (st.identities[id] && st.identities[id].name) || id;
const matches = st.matches.slice().sort((a, b) => a.date.localeCompare(b.date));

const rows = [];
matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  const r = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(m.homeId) + "," + JSON.stringify(m.awayId) + "," + JSON.stringify(m.date) + ");" +
    "if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);var ss=sectionShares(ev.paths);" +
    "return {S:z.S_,key:z.key,side:z.side,w:ev.ag.weighted,mw:Math.abs(ev.ag.weighted),dSh:100*ev.ag.neuW/ev.ag.totalWeight," +
    "h2hN:ev.ag.phaseCounts.h2h||0,eff:ev.ag.effective," +
    "sec:ss.map(function(s){return {ph:s.phase,side:s.side,lead:s.lead};})};})()");
  if (!r) return;
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  const leader = r.side === "TA" ? "H" : "A";
  rows.push({ date: m.date, comp: m.competition, fix: nameOf(m.homeId).slice(0, 16) + " v " + nameOf(m.awayId).slice(0, 16),
    key: r.key, S: r.S, side: r.side, mw: r.mw, dSh: r.dSh, h2hN: r.h2hN, eff: r.eff, sec: r.sec,
    actual, res: actual === leader ? "W" : actual === "D" ? "D" : "L" });
});

function pool(key) { return rows.filter(r => r.key === key); }
function tab(name, sel, fn) {
  const g = {};
  sel.forEach(r => { const k = fn(r); if (k == null) return; g[k] = g[k] || { n: 0, w: 0, d: 0, l: 0 }; g[k].n++; g[k][r.res.toLowerCase()]++; });
  console.log("  " + name);
  Object.keys(g).sort().forEach(k => { const z = g[k];
    console.log("    " + k.padEnd(22), "n=" + String(z.n).padEnd(4),
      "W " + (100 * z.w / z.n).toFixed(0).padStart(2) + "%",
      "D " + (100 * z.d / z.n).toFixed(0).padStart(2) + "%",
      "L " + (100 * z.l / z.n).toFixed(0).padStart(2) + "%"); });
}

["strong", "win"].forEach(key => {
  const p = pool(key);
  if (!p.length) return;
  const w = p.filter(r => r.res === "W").length, d = p.filter(r => r.res === "D").length, l = p.filter(r => r.res === "L").length;
  console.log("\n############ POOL " + key.toUpperCase() + " (post-gate) n=" + p.length +
    " | W " + (100 * w / p.length).toFixed(0) + "% D " + (100 * d / p.length).toFixed(0) + "% L " + (100 * l / p.length).toFixed(0) + "% ############");
  tab("H1 margin |weighted| thin", p, r => r.mw < 0.8 ? "<0.80" : r.mw < 1.4 ? "0.80-1.40" : ">=1.40");
  tab("H2 h2h evidence depth", p, r => r.h2hN === 0 ? "no h2h" : r.h2hN === 1 ? "1 meeting" : r.h2hN === 2 ? "2 meetings" : "3+ meetings");
  tab("H3 third section contra (>=45 lead against zone leader)", p, r => {
    const t = r.sec.find(s => s.ph === "third"); if (!t) return "no third";
    const contra = (t.side === "H") !== (r.side === "TA");
    if (contra && t.lead >= 55) return "contra >=55";
    if (contra && t.lead >= 45) return "contra 45-55";
    return "not contra";
  });
  tab("H4 competition class", p, r => r.comp === "RPL" ? "RPL league" : r.comp === "CUP" ? "RPL cup" : "UEFA/pack");
  tab("H5 engine draw-share (draw-zone probe)", p, r => r.dSh < 20 ? "<20%" : r.dSh < 28 ? "20-28%" : r.dSh < 36 ? "28-36%" : ">=36%");
  tab("H6 S position inside zone", p, r => key === "strong" ? (r.S < 90 ? "85-90" : "90+") : (r.S < 72 ? "65-72" : "72-80" && r.S < 80 ? "72-80" : "80+"));
});

/* draw-zone probe across every game with evidence: does anything call draws? */
console.log("\n############ DRAW CALIBRATION PROBE (all 600 evidence games) ############");
tab("engine draw-share vs actual draws", rows, r => r.dSh < 15 ? "<15%" : r.dSh < 22 ? "15-22%" : r.dSh < 30 ? "22-30%" : r.dSh < 40 ? "30-40%" : ">=40%");
const byD = {};
rows.forEach(r => { const k = r.key; byD[k] = byD[k] || { n: 0, d: 0 }; byD[k].n++; if (r.res === "D") byD[k].d++; });
Object.keys(byD).forEach(k => console.log("  zone " + k.padEnd(8), "n=" + String(byD[k].n).padEnd(4), "draw rate " + (100 * byD[k].d / byD[k].n).toFixed(0) + "%"));

/* loss-side inspection for the clean-win feedback loop: every post-gate WIN/STRONG loss */
console.log("\n############ POST-GATE WIN+STRONG LOSSES — the residue to eliminate ############");
rows.filter(r => (r.key === "win" || r.key === "strong") && r.res === "L").forEach(r => {
  const sec = r.sec.map(s => s.ph[0] + (s.side === "H" ? "+" : "-") + s.lead.toFixed(0)).join(" ");
  console.log("  " + r.date, r.key.padEnd(6), r.side, "S " + r.S.toFixed(0), "|mw| " + r.mw.toFixed(2), "dSh " + r.dSh.toFixed(0), "h2h " + r.h2hN, "eff " + r.eff, "[" + sec + "]", r.comp, r.fix, "=> " + r.actual);
});
console.log("total games with evidence:", rows.length);
