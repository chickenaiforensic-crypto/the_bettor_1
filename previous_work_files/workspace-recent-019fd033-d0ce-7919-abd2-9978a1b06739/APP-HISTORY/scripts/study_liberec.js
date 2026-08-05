/* study_liberec.js — one-game analysis: Slovan Liberec v Teplice, 2026-08-01 (mask = match day). */
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

// --- load CZE universe (csv) into a clean store ---
const lines = fs.readFileSync("/home/user/cze/cze_universe2.csv", "utf8").trim().split("\n").slice(1);
const st = S.BlueprintEmbed.store();
st.matches.length = 0; // clean store: no seed rows
lines.forEach(l => {
  const [date, comp, home, away, hg, ag] = l.split(",");
  if (!st.identities[home]) st.identities[home] = { id: home, name: home };
  if (!st.identities[away]) st.identities[away] = { id: away, name: away };
  st.matches.push({ id: [date, comp, home, away, hg, ag, "home"].join("|"),
    date, competition: comp, homeId: home, awayId: away, hg: +hg, ag: +ag, venue: "home" });
});
console.log("store rows:", st.matches.length, " pre-cutoff:", st.matches.filter(m => m.date < "2026-08-01").length);
const lb = st.matches.filter(m => (m.homeId==="Liberec"||m.awayId==="Liberec") && m.date < "2026-08-01");
const tp = st.matches.filter(m => (m.homeId==="Teplice"||m.awayId==="Teplice") && m.date < "2026-08-01");
console.log("Liberec games pre-cutoff:", lb.length, " Teplice games pre-cutoff:", tp.length);
console.log("Liberec last 8:", lb.slice(-8).map(m=>m.date.slice(5)+" "+(m.homeId==="Liberec"?"v ":"at ")+(m.homeId==="Liberec"?m.awayId:m.homeId)+" "+(m.homeId==="Liberec"?m.hg+"-"+m.ag:m.ag+"-"+m.hg)).join(" | "));
console.log("Teplice last 8:", tp.slice(-8).map(m=>m.date.slice(5)+" "+(m.homeId==="Teplice"?"v ":"at ")+(m.homeId==="Teplice"?m.awayId:m.homeId)+" "+(m.homeId==="Teplice"?m.hg+"-"+m.ag:m.ag+"-"+m.hg)).join(" | "));

const out = evX(`(function(){
  var ev = BlueprintEmbed.analyze("Liberec","Teplice","2026-08-01");
  if(!ev||!ev.ag) return null;
  var z = computeZoneCtx(ev.paths, ev.ag, "Liberec","Teplice","2026-08-01");
  return { ag: ev.ag, z: z, npaths: ev.paths.length,
    paths: ev.paths.map(function(p){ return {phase:p.phase, weight:p.weight, estimate:p.estimate, text:p.text||p.label||"", via:p.via||"", meta:p}; }) };
})()`);
if (!out) { console.log("NO EVIDENCE"); process.exit(0); }
const { ag, z } = out;
console.log("\n=== PATHS", out.npaths, " phaseCounts:", JSON.stringify(ag.phaseCounts));
// sample one raw path to see fields
console.log("sample path raw:", JSON.stringify(out.paths[0], null, 1).slice(0, 600));

console.log("\n=== H2H paths:");
out.paths.filter(p => p.phase === "h2h").forEach(p => console.log("  w=" + p.weight.toFixed(2), "est=" + p.estimate.toFixed(3), (p.text || "").slice(0, 120)));

console.log("\n=== COMMON-opponent paths (sorted by weight):");
out.paths.filter(p => p.phase === "common").sort((a, b) => b.weight - a.weight)
  .forEach(p => console.log("  w=" + p.weight.toFixed(2), "est=" + p.estimate.toFixed(3), (p.text || "").slice(0, 130)));

console.log("\n=== TOP level-3 chains (of " + out.paths.filter(p => p.phase === "third").length + "):");
out.paths.filter(p => p.phase === "third").sort((a, b) => b.weight - a.weight).slice(0, 8)
  .forEach(p => console.log("  w=" + p.weight.toFixed(2), "est=" + p.estimate.toFixed(3), (p.text || "").slice(0, 130)));

console.log("\n=== SECTION BALANCES (share of section weight):");
z.secs.forEach(s => {
  console.log("  " + s.name.padEnd(18), "Liberec " + (100 * s.hW / s.W).toFixed(1) + "% · draw " +
    (100 * s.dW / s.W).toFixed(1) + "% · Teplice " + (100 * s.aW / s.W).toFixed(1) + "%", " (Σw " + s.W.toFixed(1) + ")");
});
const tw = ag.homeW + ag.neuW + ag.awayW;
console.log("\n=== TOTAL SUMMATION:");
console.log("  Liberec (TA) " + (100 * ag.homeW / tw).toFixed(1) + "% · Draw " + (100 * ag.neuW / tw).toFixed(1) + "% · Teplice (TB) " + (100 * ag.awayW / tw).toFixed(1) + "%");
console.log("  weights:", ag.homeW.toFixed(2), ag.neuW.toFixed(2), ag.awayW.toFixed(2), " weighted-est:", ag.weighted.toFixed(4));
console.log("\n=== ZONE:", z.tag);
console.log("  key:", z.key, " side:", z.side, " S_:", z.S_.toFixed(1), " agree:", z.agree,
  z.gatedFrom ? " gatedFrom=" + z.gatedFrom : "", z.c5From ? " c5From=" + z.c5From : "", z.ctxFrom ? " ctxFrom=" + z.ctxFrom : "");
console.log("  effective paths:", ag.effective, " uniqueChains:", ag.uniqueChains, " reused:", ag.reused);
console.log("  c8From:", z.c8From || "(no C8 action)"); if (z.perf) console.log("  tourney status Liberec:", JSON.stringify({star:+z.perf.starH.toFixed(1), perf:z.perf.home}), " Teplice:", JSON.stringify({star:+z.perf.starA.toFixed(1), perf:z.perf.away}));
