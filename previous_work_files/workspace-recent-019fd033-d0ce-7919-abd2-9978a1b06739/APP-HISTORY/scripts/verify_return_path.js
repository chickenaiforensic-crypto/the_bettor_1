/* Return-path proof: requests -> user answers -> paste back on Data tab -> zone reacts. */
const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id){return {id:id||"",value:"",innerHTML:"",textContent:"",className:"",style:{},checked:false,disabled:false,options:[],placeholder:"",appendChild(){},insertBefore(){},removeChild(){},remove(){},insertAdjacentHTML(p,h){this.innerHTML+=h;},querySelector(){return null;},querySelectorAll(){return[];},focus(){},select(){},click(){},setAttribute(){},getAttribute(){return null;},addEventListener(){},parentNode:null};}
const els={},sandbox={};sandbox.window=sandbox;sandbox.console=console;sandbox.navigator={};sandbox.setTimeout=()=>0;sandbox.confirm=()=>true;sandbox.Blob=function(){};sandbox.FileReader=function(){this.readAsText=function(){};};sandbox.URL={createObjectURL:()=>"",revokeObjectURL(){}};
const _s={};sandbox.localStorage={getItem:k=>(k in _s?_s[k]:null),setItem:(k,v)=>{_s[k]=String(v);},removeItem:k=>{delete _s[k];}};
const md=makeEl("matchDate");md.parentNode={parentNode:{insertBefore(){}},nextSibling:null,insertBefore(){}};els["matchDate"]=md;
sandbox.document={readyState:"complete",body:makeEl("body"),getElementById(id){if(!els[id])els[id]=makeEl(id);return els[id];},createElement(t){return makeEl(t+Math.random());},querySelector(s){return makeEl(s);},querySelectorAll(){return[];},addEventListener(){}};
vm.createContext(sandbox);scripts.forEach((s,i)=>vm.runInContext(s,sandbox,{filename:"s"+i}));
const S=sandbox,evX=e=>vm.runInContext(e,S);

// 1) load the russian pack so teams resolve
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/russian-team-pack.txt","utf8");
evX("BlueprintEmbed.importData()");
console.log("pack import blocked?", /Load blocked/.test(els["bpImportReport"].innerHTML));

function analyze(){ return evX(`(function(){
  var st=BlueprintEmbed.store();
  var h=Object.keys(st.identities).filter(function(k){return /cska/.test(k);})[0];
  var a=Object.keys(st.identities).filter(function(k){return /krylja|krylya/.test(k);})[0];
  var ev=BlueprintEmbed.analyze(h,a,"2026-08-01");
  var z=computeZoneCtx(ev.paths,ev.ag,h,a,"2026-08-01");
  var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
  return {TA:(100*ev.ag.homeW/tw).toFixed(1),D:(100*ev.ag.neuW/tw).toFixed(1),TB:(100*ev.ag.awayW/tw).toFixed(1),
    tag:z.tag,word:z.word,ctxFrom:z.ctxFrom||null,paths:ev.paths.length};})()`); }

console.log("baseline (no answers):", JSON.stringify(analyze()));

// 2) user pastes back answers on the Data tab: one CTX line + one MATCH line
const answer = [
 "BP-TEAM-PACK v1",
 "# answers to standby requests, CSKA v Krylya 2026-08-01",
 "CTX|CSKA Moscow|2026-08-01|star-absence|first-choice striker out, club site 31 Jul|user-src",
 "MATCH|2026-07-19|Club Friendly|CSKA Moscow|2|0|Spartak Moscow|normal|VEB Arena|Moscow|Russia|CSK-SPA-2026-F|user-src",
 "SOURCE|user-src|https://example.com/club-news|2026-08-01|user-supplied answer rows",
 "END"
].join("\n");
S.document.getElementById("bpImportText").value = answer;
evX("BlueprintEmbed.importData()");
console.log("answer import blocked?", /Load blocked/.test(els["bpImportReport"].innerHTML), "| ctxFlags in store:", evX("BlueprintEmbed.store().ctxFlags.length"));
console.log("after answers:", JSON.stringify(analyze()));

// 3) demote-only check: flag against the TRAILING side must never raise the leader
evX(`(function(){var st=BlueprintEmbed.store();
  var a=Object.keys(st.identities).filter(function(k){return /krylja|krylya/.test(k);})[0];
  st.ctxFlags.length=0; st.ctxFlags.push({teamId:a,date:"2026-08-01",flag:"star-absence",detail:"trailing-side flag",source:"t"});})()`);
console.log("flag on trailing side:", JSON.stringify(analyze()), "(must NOT go above baseline)");
