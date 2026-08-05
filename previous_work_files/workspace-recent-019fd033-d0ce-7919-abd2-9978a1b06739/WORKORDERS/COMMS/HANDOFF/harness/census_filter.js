/* census_filter.js — what leagues exist in the store vs what the filter shows (2026-08-01).
   1) Fresh 5-pack import census: every (country, league) identity tag, SKIP-hidden flagged.
   2) Heal simulation: force Czech identities to stale ['NA'] (mimics a pre-code import),
      re-import the czech pack, verify leagues heal in place with ZERO match/identity drift. */
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
function imp(p) {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
}
["russian-team-pack", "czech-team-pack", "hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(imp);

const c1 = evX(`(function(){
  var st=BlueprintEmbed.store();
  var SKIP={"NA":1,"unknown":1,"loaded team data":1,"":1};
  var vis={}, hid={}, noLeague=0;
  Object.keys(st.identities).forEach(function(k){
    var it=st.identities[k], lgs=(it.leagues||[]).filter(function(l){return l;});
    if(!lgs.length){ noLeague++; hid[(it.country||'?')+' | (none)']=(hid[(it.country||'?')+' | (none)']||0)+1; return; }
    lgs.forEach(function(l){
      var key=it.country+' | '+l;
      if(SKIP[l]) hid[key]=(hid[key]||0)+1; else vis[key]=(vis[key]||0)+1;
    });
  });
  return {matches:st.matches.length, ids:Object.keys(st.identities).length,
          muted:st.matches.filter(function(m){return m.muted;}).length,
          noLeague:noLeague, vis:vis, hid:hid};
})()`);
console.log("=== FRESH 5-PACK CENSUS ===");
console.log("matches", c1.matches, "| identities", c1.ids, "| muted", c1.muted, "| identities with NO usable league tag:", c1.noLeague);
console.log("\nVISIBLE in league filter (" + Object.keys(c1.vis).length + " tags):");
Object.keys(c1.vis).sort().forEach(k => console.log("  " + k + "  ×" + c1.vis[k]));
console.log("\nHIDDEN by SKIP junk filter (" + Object.keys(c1.hid).length + " tags):");
Object.keys(c1.hid).sort().forEach(k => console.log("  " + k + "  ×" + c1.hid[k]));

/* Heal simulation: user's persisted Czech identities carry stale ['NA'] (pre-code import). */
const c2 = evX(`(function(){
  var st=BlueprintEmbed.store();
  var m0=st.matches.length, i0=Object.keys(st.identities).length;
  var czKeys=Object.keys(st.identities).filter(function(k){return st.identities[k].country==='Czech Republic';});
  var brno0=JSON.stringify(st.identities[Object.keys(st.identities).find(function(k){return st.identities[k].name==='Zbrojovka Brno';})].leagues||[]);
  czKeys.forEach(function(k){ st.identities[k].leagues=['NA']; });   // stale-store damage
  return {m0:m0,i0:i0,czN:czKeys.length,brno0:brno0};
})()`);
imp("czech-team-pack");  // re-import of CURRENT coded pack into the damaged store
const c3 = evX(`(function(){
  var st=BlueprintEmbed.store();
  var kb=Object.keys(st.identities).find(function(k){return st.identities[k].name==='Zbrojovka Brno';});
  var sparta=Object.keys(st.identities).find(function(k){return st.identities[k].name==='Sparta Prague';});
  var naCzech=Object.keys(st.identities).filter(function(k){
    return st.identities[k].country==='Czech Republic' && (st.identities[k].leagues||[]).some(function(l){return l==='NA';});
  }).length;
  return {m1:st.matches.length, i1:Object.keys(st.identities).length,
          brno1:st.identities[kb].leagues, sparta:st.identities[sparta].leagues, naCzech:naCzech,
          muted:st.matches.filter(function(m){return m.muted;}).length};
})()`);
console.log("\n=== HEAL TEST: stale ['NA'] store + re-import current czech pack ===");
console.log("before: matches " + c2.m0 + " · identities " + c2.i0 + " · Czech identities " + c2.czN + " · Brno leagues " + c2.brno0);
console.log("after : matches " + c3.m1 + " · identities " + c3.i1 + " · Brno leagues " + JSON.stringify(c3.brno1) + " · Sparta leagues " + JSON.stringify(c3.sparta) + " · Czech still-NA " + c3.naCzech + " · muted " + c3.muted);
console.log(c3.m1 === c2.m0 && c3.i1 === c2.i0 ? "HEAL OK — zero match/identity drift, leagues repaired in place"
                                               : "DRIFT — investigate before advising re-import");

console.log("\n=== THE 24 LEAGUE-LESS IDENTITIES (hidden by SKIP, by design or not) ===");
const c4 = evX(`(function(){
  var st=BlueprintEmbed.store(), SKIP={"NA":1,"unknown":1,"loaded team data":1,"":1};
  var out=[];
  Object.keys(st.identities).forEach(function(k){
    var it=st.identities[k];
    var lgs=(it.leagues||[]).filter(function(l){return l && !SKIP[l];});
    if(lgs.length) return;
    var n=st.matches.filter(function(m){return m.homeId===k||m.awayId===k;}).length;
    out.push((it.country||'?')+' :: '+it.name+'  ('+n+' matches)');
  });
  return out.sort();
})()`);
c4.forEach(x => console.log("  " + x));
