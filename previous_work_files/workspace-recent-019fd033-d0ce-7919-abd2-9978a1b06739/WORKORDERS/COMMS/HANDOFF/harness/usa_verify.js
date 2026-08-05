/* usa_verify.js — round-1 acceptance gate (2026-08-01): 6-pack import (3 recoded + usa),
   zero-error check, census drift, duplicate-name audit, final filter-visible tag list. */
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
const PACKS = ["russian-team-pack", "czech-team-pack", "hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack", "usa-team-pack"];
PACKS.forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
  const rep = S.document.getElementById("bpImportReport").innerHTML;
  const blocked = /Load blocked/.test(rep), m = rep.match(/(\d+)\s*error/);
  console.log(p.padEnd(26) + (blocked ? "BLOCKED (" + (m ? m[1] : "?") + " errors)" : "import clean"));
});

const r = evX(`(function(){
  var st=BlueprintEmbed.store();
  var SKIP={"NA":1,"unknown":1,"loaded team data":1,"":1};
  var vis={}, hid=0, hidNames=[];
  Object.keys(st.identities).forEach(function(k){
    var it=st.identities[k];
    var lgs=(it.leagues||[]).filter(function(l){return l && !SKIP[l];});
    if(!lgs.length){ hid++; hidNames.push(it.name); return; }
    lgs.forEach(function(l){ l=canonLg(l); vis[it.country+' | '+l]=(vis[it.country+' | '+l]||0)+1; });
  });
  return {matches:st.matches.length, ids:Object.keys(st.identities).length,
          muted:st.matches.filter(function(m){return m.muted;}).length,
          hid:hid, hidNames:hidNames.sort(), vis:vis};
})()`);
console.log("\nCENSUS: matches " + r.matches + " | identities " + r.ids + " | muted " + r.muted);
console.log("league-less identities (SKIP-hidden): " + r.hid + (r.hid ? " -> " + r.hidNames.join(", ") : ""));
console.log("\nfilter-visible tags (" + Object.keys(r.vis).length + "):");
Object.keys(r.vis).sort().forEach(k => console.log("  " + k + " ×" + r.vis[k]));

const audit = evX("BlueprintEmbed.audit()");
const dupLines = String(audit).split("\n").filter(l => /duplicat|GAP/i.test(l));
console.log("\nAUDIT duplicate/GAP lines (" + dupLines.length + "):");
dupLines.slice(0, 12).forEach(l => console.log("  " + l.trim()));

/* USA spot check: identity lookup both ways + one fixture probe */
const us = evX(`(function(){
  var a=BlueprintEmbed.resolve('Los Angeles FC',''); var b=BlueprintEmbed.resolve('LAFC','');
  var c=BlueprintEmbed.resolve('FC Cincinnati',''); var d=BlueprintEmbed.resolve('CF Montréal','');
  var st=BlueprintEmbed.store();
  var lafcGames=st.matches.filter(function(m){return m.homeId===a||m.awayId===a;}).length;
  var aet=st.matches.filter(function(m){return m.date==='2024-11-23'&&m.homeId===a;}).map(function(m){return m.hg+'-'+m.ag;})[0];
  var usl=BlueprintEmbed.resolve('Sacramento Republic FC','');
  var usoc=st.matches.filter(function(m){return m.competition==='US Open Cup';}).length;
  return {lafc:a, lafcAlias:b===a, cincy:!!c, mtl:d&&st.identities[d].country, lafcGames:lafcGames, aetScore:aet, usl:!!usl, usoc:usoc};
})()`);
console.log("\nUSA probe:", JSON.stringify(us, null, 1));
