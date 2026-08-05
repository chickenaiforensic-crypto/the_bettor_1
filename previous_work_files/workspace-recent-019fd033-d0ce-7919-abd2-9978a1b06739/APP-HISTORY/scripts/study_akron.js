/* study_akron.js — Akron v Rubin (2026-08-01) pre/post playoff rows impact check. */
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
["hibernian-team-pack","malisheva-team-pack","malisheva-closure-pack"].forEach(p=>{
  S.document.getElementById("bpImportText").value=fs.readFileSync("/home/user/packs/"+p+".txt","utf8");
  evX("BlueprintEmbed.importData()");});
const RPL=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json","utf8"));
const NAMES=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json","utf8"));
function run(withPO){
  const st=S.BlueprintEmbed.store();
  st.matches.length=0;
  [...new Set(RPL.flatMap(m=>[m.home,m.away]))].forEach(s=>{if(!st.identities[s])st.identities[s]={id:s,name:NAMES[s]||s};});
  RPL.forEach(m=>{ if(!withPO && m.comp==="RPLPO") return;
    st.matches.push({id:[m.date,m.comp,m.home,m.away,m.hg,m.ag,"home"].join("|"),date:m.date,competition:m.comp,homeId:m.home,awayId:m.away,hg:m.hg,ag:m.ag,venue:"home"}); });
  return evX(`(function(){var ev=BlueprintEmbed.analyze("akron","rubin","2026-08-01");if(!ev||!ev.ag)return null;
    var z=computeZoneCtx(ev.paths,ev.ag,"akron","rubin","2026-08-01");
    var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
    return {pc:ev.ag.phaseCounts, n:ev.paths.length, TA:(100*ev.ag.homeW/tw).toFixed(1), D:(100*ev.ag.neuW/tw).toFixed(1), TB:(100*ev.ag.awayW/tw).toFixed(1),
      zone:z.tag, c8:z.c8From||null,
      perf: z.perf?{h:z.perf.starH.toFixed(1), a:z.perf.starA.toFixed(1), hn:z.perf.home, an:z.perf.away}:null,
      secs:z.secs.map(function(s){return s.name+": "+(100*s.hW/s.W).toFixed(1)+"/"+(100*s.dW/s.W).toFixed(1)+"/"+(100*s.aW/s.W).toFixed(1);})};})()`);
}
console.log("WITHOUT playoff rows (frozen state):", JSON.stringify(run(false), null, 1));
console.log("WITH playoff rows (current store):  ", JSON.stringify(run(true), null, 1));
