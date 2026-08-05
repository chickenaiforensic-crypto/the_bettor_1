/* replay_full.js — dump ALL replayed games with zone internals for cohort/candidate-gate analysis. */
const fs=require("fs"),vm=require("vm");
const html=fs.readFileSync("/home/user/app-v2.6-cross.html","utf8");
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
function makeEl(id){return {id:id||"",value:"",innerHTML:"",textContent:"",className:"",style:{},checked:false,disabled:false,options:[],placeholder:"",appendChild(){},insertBefore(){},removeChild(){},remove(){},insertAdjacentHTML(p,h){this.innerHTML+=h;},querySelector(){return null;},querySelectorAll(){return[];},focus(){},select(){},click(){},setAttribute(){},getAttribute(){return null;},addEventListener(){},parentNode:null};}
const els={},sandbox={};sandbox.window=sandbox;sandbox.console=console;sandbox.navigator={};sandbox.setTimeout=()=>0;sandbox.confirm=()=>true;sandbox.Blob=function(){};sandbox.FileReader=function(){this.readAsText=function(){};};sandbox.URL={createObjectURL:()=>"",revokeObjectURL(){}};
const _s={};sandbox.localStorage={getItem:k=>(k in _s?_s[k]:null),setItem:(k,v)=>{_s[k]=String(v);},removeItem:k=>{delete _s[k];}};
const md=makeEl("matchDate");md.parentNode={parentNode:{insertBefore(){}},nextSibling:null,insertBefore(){}};els["matchDate"]=md;
sandbox.document={readyState:"complete",body:makeEl("body"),getElementById(id){if(!els[id])els[id]=makeEl(id);return els[id];},createElement(t){return makeEl(t+Math.random());},querySelector(s){return makeEl(s);},querySelectorAll(){return[];},addEventListener(){}};
vm.createContext(sandbox);scripts.forEach((s,i)=>vm.runInContext(s,sandbox,{filename:"s"+i}));
const S=sandbox,evX=e=>vm.runInContext(e,S);
["hibernian-team-pack","malisheva-team-pack","malisheva-closure-pack"].forEach(p=>{S.document.getElementById("bpImportText").value=fs.readFileSync("/home/user/packs/"+p+".txt","utf8");evX("BlueprintEmbed.importData()");});
const RPL=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json","utf8"));
const NAMES=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json","utf8"));
const st=S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m=>[m.home,m.away]))].forEach(s=>{if(!st.identities[s])st.identities[s]={id:s,name:NAMES[s]||s};});
RPL.forEach(m=>st.matches.push({id:[m.date,m.comp,m.home,m.away,m.hg,m.ag,"home"].join("|"),date:m.date,competition:m.comp,homeId:m.home,awayId:m.away,hg:m.hg,ag:m.ag,venue:"home"}));
const out=[];
st.matches.slice().sort((a,b)=>a.date.localeCompare(b.date)).forEach(m=>{
  if(!m.homeId||!m.awayId||m.homeId===m.awayId)return;
  const r=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "if(!ev||!ev.ag)return null;var z=computeZoneCtx(ev.paths,ev.ag,"+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "return {key:z.key,side:z.side,S_:z.S_,agree:z.agree,nContra:z.contra.length,c8:!!z.c8From,"+
    "secsN:z.secs.length,h2hN:(ev.ag.phaseCounts&&ev.ag.phaseCounts.h2h)||0,"+
    "perf:z.perf?{sH:z.perf.starH,sA:z.perf.starA,hN:z.perf.home?z.perf.home.n:-1,hP:z.perf.home?z.perf.home.perf:-1,aN:z.perf.away?z.perf.away.n:-1,aP:z.perf.away?z.perf.away.perf:-1}:null};})()");
  if(!r)return;
  const actual=m.hg>m.ag?"H":m.hg<m.ag?"A":"D";
  const leader=r.side==="TA"?"H":"A";
  const res=actual===leader?"W":actual==="D"?"D":"L";
  const lg=leader==="H"?m.hg:m.ag, wg=leader==="H"?m.ag:m.hg;
  out.push({date:m.date,h:m.homeId,a:m.awayId,score:m.hg+"-"+m.ag,zone:r.key,side:r.side,S:+r.S_.toFixed(1),
    agree:r.agree,contra:r.nContra,c8:r.c8,secsN:r.secsN,h2hN:r.h2hN,perf:r.perf,res,resMargin:res==="L"?wg-lg:0});
});
fs.writeFileSync("/home/user/rpl/replay_full.json",JSON.stringify(out));
console.log("games:",out.length);
