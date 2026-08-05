/* goals_replay.js — masked-replay pool (canonical) re-analysed from TOTAL GOALS perspective.
   Estimator EV-G: results-only, causal (date<cutoff), evidence-weighted mean of total goals
   in matches involving each side, averaged across sides.
   Baselines: B0 rolling store mean <cutoff; B1 unweighted last-10 per side. */
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
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/"+p+".txt","utf8");
  evX("BlueprintEmbed.importData()");
});
const RPL = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json","utf8"));
const NAMES = JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json","utf8"));
const st = S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m=>[m.home,m.away]))].forEach(s=>{ if(!st.identities[s]) st.identities[s]={id:s,name:NAMES[s]||s}; });
RPL.forEach(m=>st.matches.push({id:[m.date,m.comp,m.home,m.away,m.hg,m.ag,"home"].join("|"),date:m.date,competition:m.comp,homeId:m.home,awayId:m.away,hg:m.hg,ag:m.ag,venue:"home"}));
const byId={}; st.matches.forEach(m=>{byId[m.id]=m;});
const matches = st.matches.slice().sort((a,b)=>a.date.localeCompare(b.date));

// one structural sample so the estimator matches real path shape
const sample = evX(`(function(){var ev=BlueprintEmbed.analyze("cska","krylja","2026-08-01");
  return ev.paths.slice(0,4).map(function(p){return {phase:p.phase,weight:p.weight,ids:p.ids};});})()`);
console.log("PATH SHAPE SAMPLE:", JSON.stringify(sample));

function sideMeans(paths, hid, aid){
  const hM={}, aM={};
  paths.forEach(p=>{
    const w=p.weight||1;
    (p.ids||[]).forEach(id=>{
      const m=byId[id]; if(!m) return;
      const tot=m.hg+m.ag;
      if(m.homeId===hid||m.awayId===hid){ if(!(id in hM)||w>hM[id].w) hM[id]={w:w,t:tot}; }
      if(m.homeId===aid||m.awayId===aid){ if(!(id in aM)||w>aM[id].w) aM[id]={w:w,t:tot}; }
    });
  });
  function mean(map){ let sw=0,st_=0; Object.keys(map).forEach(k=>{sw+=map[k].w;st_+=map[k].w*map[k].t;}); return sw?{m:st_/sw,n:Object.keys(map).length}:null; }
  return {h:mean(hM), a:mean(aM)};
}
function last10mean(tid, cutoff){
  const g=matches.filter(m=>m.date<cutoff&&(m.homeId===tid||m.awayId===tid)).slice(-10);
  if(!g.length) return null;
  return g.reduce((s,m)=>s+m.hg+m.ag,0)/g.length;
}
function storeMean(cutoff){
  const g=matches.filter(m=>m.date<cutoff);
  return g.reduce((s,m)=>s+m.hg+m.ag,0)/g.length;
}

const out=[]; let noEv=0;
matches.forEach(m=>{
  if(!m.homeId||!m.awayId||m.homeId===m.awayId) return;
  const r=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "if(!ev||!ev.ag)return null;var z=computeZoneCtx(ev.paths,ev.ag,"+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "return {key:z.key,side:z.side,h2hN:(ev.ag.phaseCounts&&ev.ag.phaseCounts.h2h)||0,cold:(z.perf?(!z.perf.home||!z.perf.away):true),paths:ev.paths.length};})()");
  if(!r) { noEv++; return; }
  const evp=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");return ev.paths.map(function(p){return {phase:p.phase,weight:p.weight,ids:p.ids};});})()");
  const sm=sideMeans(evp,m.homeId,m.awayId);
  const b0=storeMean(m.date), b1h=last10mean(m.homeId,m.date), b1a=last10mean(m.awayId,m.date);
  out.push({
    date:m.date, comp:m.competition||"?", h:m.homeId, a:m.awayId, hg:m.hg, ag:m.ag, tot:m.hg+m.ag,
    zone:r.key, leader:r.side, h2hN:r.h2hN, cold:r.cold, npaths:r.paths,
    evh:sm.h?sm.h.m:null, eva:sm.a?sm.a.m:null, evn_h:sm.h?sm.h.n:0, evn_a:sm.a?sm.a.n:0,
    b0:b0, b1:(b1h!==null&&b1a!==null)?(b1h+b1a)/2:null
  });
});
out.forEach(g=>{ g.evg = (g.evh!==null&&g.eva!==null)?(g.evh+g.eva)/2:(g.evh!==null?g.evh:g.eva); });
fs.writeFileSync("/home/user/rpl/goals_replay.json", JSON.stringify(out,null,1));
console.log("games:",out.length," no-evidence skipped:",noEv);
const maes={evg:[],b0:[],b1:[]};
out.forEach(g=>{ if(g.evg!==null)maes.evg.push(Math.abs(g.evg-g.tot)); maes.b0.push(Math.abs(g.b0-g.tot)); if(g.b1!==null)maes.b1.push(Math.abs(g.b1-g.tot)); });
console.log("MAE  EV-G:",(maes.evg.reduce((a,b)=>a+b,0)/maes.evg.length).toFixed(3)," B0:",(maes.b0.reduce((a,b)=>a+b,0)/maes.b0.length).toFixed(3)," B1:",(maes.b1.reduce((a,b)=>a+b,0)/maes.b1.length).toFixed(3));
const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;
console.log("mean expected EV-G:",mean(out.map(g=>g.evg)).toFixed(3)," mean actual:",mean(out.map(g=>g.tot)).toFixed(3)," B0:",mean(out.map(g=>g.b0)).toFixed(3));
