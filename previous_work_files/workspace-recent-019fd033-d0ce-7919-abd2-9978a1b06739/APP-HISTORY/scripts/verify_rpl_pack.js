/* verify_pack.js — import czech-team-pack via the real app parser, then replay the Liberec analysis from the pack. */
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
// import through the REAL import path
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/russian-team-pack.txt","utf8");
evX("BlueprintEmbed.importData()");
const report = els["bpImportReport"].innerHTML;
const res = {errors: /Load blocked/.test(report) ? [report.slice(0,500)] : [], teams: null, matches: null, sources: null, notes: [], warnings: /warning/.test(report) ? [report.match(/<div class=\"banner ban-warn\">([\s\S]*?)<\/div>/)?.[1]?.slice(0,300)] : []};
if (!res.errors.length) { const m = report.match(/Loaded (\d+) team row\(s\), (\d+) season row\(s\), (\d+) form row\(s\), (\d+) venue row\(s\), (\d+) new match row\(s\), (\d+) source row\(s\)/);
  if (m) { res.teams = +m[1]; res.seasons = +m[2]; res.forms = +m[3]; res.venues = +m[4]; res.matches = +m[5]; res.sources = +m[6]; } }
const stt = S.BlueprintEmbed.store(); res.storeMatches = stt.matches.length;
console.log("import errors:", res.errors.length ? res.errors.slice(0,10) : "none");
console.log("imported: teams", res.teams, "matches", res.matches, "sources", res.sources, "notes", res.notes.length, "warnings:", res.warnings.length ? res.warnings.slice(0,5) : "none");
// resolve + analyze from the imported pack
const out = evX(`(function(){
  var st=BlueprintEmbed.store();
  var ids=Object.keys(st.identities).filter(function(k){return /akron|rubin/i.test(k);});
  return {ids:ids,
    ev:(function(){var lib=ids.filter(function(k){return /akron/.test(k)})[0], tep=ids.filter(function(k){return /rubin/.test(k)})[0];
      if(!lib||!tep) return null;
      var ev=BlueprintEmbed.analyze(lib,tep,"2026-08-01"); if(!ev||!ev.ag) return null;
      var z=computeZoneCtx(ev.paths,ev.ag,lib,tep,"2026-08-01");
      var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
      return {homeId:lib, awayId:tep, phaseCounts:ev.ag.phaseCounts, n:ev.paths.length,
        TA:(100*ev.ag.homeW/tw).toFixed(1), D:(100*ev.ag.neuW/tw).toFixed(1), TB:(100*ev.ag.awayW/tw).toFixed(1), zone:z.tag};})()};})()`);
console.log("identity keys:", JSON.stringify(out.ids));
console.log("pack-based analysis:", JSON.stringify(out.ev, null, 1));
