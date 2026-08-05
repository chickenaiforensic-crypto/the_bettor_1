/* audit_flip.js — orientation + store-delta reproduction harness (2026-08-01 audit-grade). \n   Four orientation audits + store census. SUI inclusion toggled by env SUI=0/1.\n
   and Lokomotiv Moscow v Dynamo Moscow (RPL, 2026-08-29 listed, as-of-2026-08-01 evidence). */
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
["russian-team-pack", "czech-team-pack", "hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});
var WITH_SUI = process.env.SUI === "1";
const st = S.BlueprintEmbed.store();
function audit(label, homeId, awayId, homeName, awayId2, cutoff) {
  var awayName = awayId2;
  homeId = evX("BlueprintEmbed.resolve(" + JSON.stringify(homeId) + ",'')") || homeId;
  awayId = evX("BlueprintEmbed.resolve(" + JSON.stringify(awayId) + ",'')") || awayId;
  const r = evX("(function(){var ev=BlueprintEmbed.analyze(" + JSON.stringify(homeId) + "," + JSON.stringify(awayId) + "," + JSON.stringify(cutoff) + ");" +
    "if(!ev||!ev.ag)return {nullify:1};var ag=ev.ag;var z=computeZoneCtx(ev.paths,ag," + JSON.stringify(homeId) + "," + JSON.stringify(awayId) + "," + JSON.stringify(cutoff) + ");" +
    "var g=evidenceGoalsEstimate(ev.paths," + JSON.stringify(homeId) + "," + JSON.stringify(awayId) + "," + JSON.stringify(cutoff) + ");" +
    "var tw=ag.homeW+ag.neuW+ag.awayW;var c9=cal9(ag.homeW/tw*100,ag.neuW/tw*100,ag.awayW/tw*100);" +
    "return {key:z.key,word:z.word,side:z.side,S:z.S_,tag:z.tag,secs:z.secs,gated:z.gatedFrom||null,c5:z.c5From||null,c8:z.c8From||null,c11:z.c11From||null," +
    "perf:z.perf?{starH:z.perf.starH,starA:z.perf.starA,h:z.perf.home,a:z.perf.away}:null," +
    "raw:[ag.homeW/tw*100,ag.neuW/tw*100,ag.awayW/tw*100],cal:c9,eff:ag.effective,agree:ag.agree,w:ag.weighted," +
    "npaths:ev.paths.length,pc:ag.phaseCounts,g:g?{est:g.est,region:g.region}:null};})()");
  console.log("\n=== " + label + " ===");
  if (r.nullify) { console.log("  NO evidence graph rows resolve -> NO CALL"); return; }
  console.log("  paths " + r.npaths + " (h2h " + (r.pc.h2h || 0) + " · common " + (r.pc.common || 0) + " · third " + (r.pc.third || 0) + ") | effective " + r.eff +
    " | agree " + (100 * r.agree).toFixed(0) + "% | weighted " + r.w.toFixed(2));
  (r.secs || []).forEach(s => console.log("  [" + s.name + "] " + homeName + " " + (100 * s.hW / s.W).toFixed(0) + "% · draw " + (100 * s.dW / s.W).toFixed(0) + "% · " + awayName + " " + (100 * s.aW / s.W).toFixed(0) + "%  (Σw " + s.W.toFixed(1) + ")"));
  console.log("  TOTAL (calibrated display): " + homeName + " " + r.cal[0].toFixed(1) + " · Draw " + r.cal[1].toFixed(1) + " · " + awayName + " " + r.cal[2].toFixed(1) + "   [raw mass " + r.raw.map(x => x.toFixed(1)).join("/") + "]");
  console.log("  ZONE: " + r.tag + (r.gated ? " (gate from " + r.gated + ")" : "") + (r.c5 ? " (draw-risk no-h2h)" : "") + (r.c8 ? " (perf drop)" : "") + (r.c11 ? " (star drop)" : ""));
  if (r.perf) console.log("  form last-6: " + homeName + " star " + r.perf.starH.toFixed(0) + (r.perf.h ? " perf " + r.perf.h.perf.toFixed(1) + "/SOS " + r.perf.h.sos.toFixed(1) : " cold") + " | " + awayName + " star " + r.perf.starA.toFixed(0) + (r.perf.a ? " perf " + r.perf.a.perf.toFixed(1) + "/SOS " + r.perf.a.sos.toFixed(1) : " cold"));
  if (r.g) {
    const T = evX("EVG2_TABLE")[r.g.region];
    console.log("  TOTAL GOALS: est " + r.g.est.toFixed(2) + " " + r.g.region + " (replay mean " + T.act.toFixed(2) + " · O1.5 " + T.o15 + "% · U2.5 " + T.u25 + "% · O2.5 " + T.o25 + "%)");
  }
}
console.log("CANONICAL STORE CENSUS: matches=" + st.matches.length + " (SUI " + (WITH_SUI ? "included" : "EXCLUDED") + ") identities=" + Object.keys(st.identities).length);
audit("F1 Dynamo Makhachkala (H) v Lokomotiv — settled 2-1 — canonical", "Dynamo Makhachkala", "Lokomotiv Moscow", "Makhachkala", "Lokomotiv", "2026-08-02");
audit("F2 Lokomotiv (H) v Dynamo Makhachkala — REVERSED (fictional) — canonical", "Lokomotiv Moscow", "Dynamo Makhachkala", "Lokomotiv", "Makhachkala", "2026-08-02");
audit("F3 Lokomotiv (H) v Dynamo Moscow — listed 2026-08-29 — canonical", "Lokomotiv Moscow", "Dynamo Moscow", "Lokomotiv", "Dynamo M", "2026-08-29");
audit("F4 Dynamo Moscow (H) v Lokomotiv — REVERSED — canonical", "Dynamo Moscow", "Lokomotiv Moscow", "Dynamo M", "Lokomotiv", "2026-08-29");
