const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id){return{id:id||"",value:"",innerHTML:"",textContent:"",className:"",style:{},checked:false,disabled:false,options:[],placeholder:"",appendChild(){},insertBefore(){},removeChild(){},remove(){},insertAdjacentHTML(p,h){this.innerHTML+=h;},querySelector(){return null;},querySelectorAll(){return[];},focus(){},select(){},click(){},setAttribute(){},getAttribute(){return null;},addEventListener(){},parentNode:null};}
const els = {}, sb = {};
sb.window = sb; sb.console = console; sb.navigator = {}; sb.setTimeout = () => 0; sb.confirm = () => true;
sb.Blob = function (p) { this.parts = p || []; }; sb.FileReader = function () { this.readAsText = function () {}; };
sb.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const ls = {}; sb.localStorage = { getItem: k => (k in ls ? ls[k] : null), setItem: (k, v) => { ls[k] = String(v); }, removeItem: k => { delete ls[k]; } };
const md = makeEl("matchDate"); md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} }; els["matchDate"] = md;
sb.document = { readyState: "complete", body: makeEl("body"), getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; }, createElement(t) { return makeEl(t + Math.random()); }, querySelector(s) { if (!els["q:" + s]) els["q:" + s] = makeEl(s); return els["q:" + s]; }, querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sb); scripts.forEach((s, i) => vm.runInContext(s, sb, { filename: "s" + i + ".js" }));
const S = sb;
["russian-team-pack.txt","czech-team-pack.txt","hibernian-team-pack.txt","malisheva-team-pack.txt","malisheva-closure-pack.txt","usa-team-pack.txt"].forEach(p=>{
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/"+p, "utf8");
  S.BlueprintEmbed.importData();
});
const st = S.BlueprintEmbed.store();
const hid = S.BlueprintEmbed.resolve("FC Krasnodar", "Russia"), aid = S.BlueprintEmbed.resolve("Fakel Voronezh", "Russia");
[["FC Krasnodar", hid], ["Fakel Voronezh", aid]].forEach(([n, id]) => {
  const ms = st.matches.filter(m => !m.muted && (m.homeId === id || m.awayId === id)).sort((a, b) => a.date < b.date ? 1 : -1);
  const lg = st.identities[id].leagues.join(",");
  console.log(n + " [" + lg + "]: " + ms.length + " loaded matches, " + ms[ms.length - 1].date + " .. " + ms[0].date);
});
S.document.getElementById("matchDate").value = "2026-08-02";
S.document.getElementById("homeTeam").value = "B|Russia|FC Krasnodar";
S.document.getElementById("awayTeam").value = "B|Russia|Fakel Voronezh";
S.renderRate();
const o = S.document.getElementById("result").innerHTML;
console.log("card:", (o.match(/<h2>(.*?)<\/h2>/) || ["", "?"])[1]);
const zi=o.indexOf("Zone statement.");const seg=zi>-1?o.slice(zi,zi+400):"?";console.log("zone seg:", seg.replace(/<[^>]+>/g," ").replace(/\s+/g," ").slice(0,220));
console.log("total line:", (o.match(/<b>FC Krasnodar [^<]*<\/b>/) || ["?"])[0]);
console.log("gates strip:", (o.match(/<div class="banner [^"]*"><b>([^<]*)<\/b>/) || ["", "?"])[1]);
const gi=o.indexOf("Estimated total goals");console.log("goals:", gi>-1?o.slice(gi,gi+260).replace(/<[^>]+>/g," ").replace(/\s+/g," ").slice(0,200):"?");
console.log("stats lead present:", o.indexOf("Standard stats") !== -1, "| gates NO PLAY text:", /NO PLAY/.test(o));
