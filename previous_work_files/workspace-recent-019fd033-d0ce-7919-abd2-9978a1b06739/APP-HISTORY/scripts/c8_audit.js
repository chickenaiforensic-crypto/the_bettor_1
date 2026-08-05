/* c8_audit.js — audit candidate C8 (opponent-quality-weighted current-tourney performance rating). */
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
const st=S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m=>[m.home,m.away]))].forEach(s=>{if(!st.identities[s])st.identities[s]={id:s,name:NAMES[s]||s};});
RPL.forEach(m=>st.matches.push({id:[m.date,m.comp,m.home,m.away,m.hg,m.ag,"home"].join("|"),date:m.date,competition:m.comp,homeId:m.home,awayId:m.away,hg:m.hg,ag:m.ag,venue:"home"}));
const all=st.matches.slice().sort((a,b)=>a.date.localeCompare(b.date));

/* --- C8 spec v1 (causal): Elo start 1500, K=20, home+65, all comps, < cutoff.
   star = clamp((elo-1420)/2, 0, 100). Current tourney = games with seasonStart(Jul 1) <= date < cutoff.
   SOS = mean star(opp); Perf = mean [result(1/.5/0) x star(opp)]. Cold start: <3 games -> undefined. --- */
function eloAt(cutoff){
  const E={};
  all.forEach(m=>{ if(m.date>=cutoff) return;
    const eh=E[m.homeId]||1500, ea=E[m.awayId]||1500;
    const p=1/(1+Math.pow(10,-((eh+65-ea)/400)));
    const s=m.hg>m.ag?1:m.hg<m.ag?0:0.5;
    E[m.homeId]=eh+20*(s-p); E[m.awayId]=ea+20*((1-s)-(1-p));
  });
  return E;
}
const star=e=>Math.max(0,Math.min(100,(e-1420)/2));
function seasonStart(d){ const y=+d.slice(0,4), mo=+d.slice(5,7); return (mo>=7?y:y-1)+"-07-01"; }
function perfAt(team,cutoff,E){
  const ss=seasonStart(cutoff);
  const g=all.filter(m=>m.date>=ss&&m.date<cutoff&&(m.homeId===team||m.awayId===team));
  if(g.length<3) return null;
  let sos=0,perf=0;
  g.forEach(m=>{ const h=m.homeId===team, opp=h?m.awayId:m.homeId;
    const f=h?m.hg:m.ag, c=h?m.ag:m.hg;
    const res=f>c?1:f===c?0.5:0, st_=star(E[opp]||1500);
    sos+=st_; perf+=res*st_; });
  return {n:g.length, sos:sos/g.length, perf:perf/g.length};
}
const rows=[];
all.forEach(m=>{
  if(m.date<"2024-08-15") return; // need some current-season games even to try
  const z=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);return {key:z.key,side:z.side};})()");
  if(!z) return;
  const E=eloAt(m.date);
  const ph=perfAt(m.homeId,m.date,E), pa=perfAt(m.awayId,m.date,E);
  if(!ph||!pa) return;
  const actual=m.hg>m.ag?"H":m.hg<m.ag?"A":"D";
  rows.push({d:m.date,zone:z.key,side:z.side,dp:ph.perf-pa.perf,ds:star(E[m.homeId]||1500)-star(E[m.awayId]||1500),actual});
});
console.log("auditable games (both teams >=3 current-season games):", rows.length);

/* T1: standalone signal — deltaPerf buckets vs home outcome */
const buckets=[[-99,-5],[-5,-1],[-1,1],[1,5],[5,99]];
console.log("\nT1 standalone: deltaPerf bucket -> home W/D/L:");
buckets.forEach(b=>{
  const g=rows.filter(r=>r.dp>=b[0]&&r.dp<b[1]); if(!g.length) return;
  const w=g.filter(r=>r.actual==="H").length, d=g.filter(r=>r.actual==="D").length, l=g.length-w-d;
  console.log(`  [${b[0]},${b[1]}) n=${String(g.length).padEnd(4)} W ${(100*w/g.length).toFixed(0).padStart(2)}% D ${(100*d/g.length).toFixed(0).padStart(2)}% L ${(100*l/g.length).toFixed(0).padStart(2)}%`);
});
/* T1b: deltaStar for comparison */
console.log("T1b raw Elo-star delta bucket -> home W/D/L:");
buckets.forEach(b=>{
  const g=rows.filter(r=>r.ds>=b[0]&&r.ds<b[1]); if(!g.length) return;
  const w=g.filter(r=>r.actual==="H").length, d=g.filter(r=>r.actual==="D").length, l=g.length-w-d;
  console.log(`  [${b[0]},${b[1]}) n=${String(g.length).padEnd(4)} W ${(100*w/g.length).toFixed(0).padStart(2)}% D ${(100*d/g.length).toFixed(0).padStart(2)}% L ${(100*l/g.length).toFixed(0).padStart(2)}%`);
});

/* T2: add-on value inside shipped zones — perf agrees/disagrees with zone leader */
console.log("\nT2 inside shipped zones: perf-agree vs perf-disagree leader outcomes:");
["strong","win","windraw","lean","toss"].forEach(zk=>{
  const g=rows.filter(r=>r.zone===zk); if(g.length<20) return;
  const ag=g.filter(r=>(r.side==="TA"&&r.dp>0)||(r.side==="TB"&&r.dp<0));
  const dis=g.filter(r=>(r.side==="TA"&&r.dp<0)||(r.side==="TB"&&r.dp>0));
  function rate(sub){ if(!sub.length) return "n=0";
    const lead=r=>r.side==="TA"?"H":"A";
    const w=sub.filter(r=>r.actual===lead(r)).length, d=sub.filter(r=>r.actual==="D").length, l=sub.length-w-d;
    return "n="+String(sub.length).padEnd(4)+" W "+(100*w/sub.length).toFixed(0).padStart(2)+"% D "+(100*d/sub.length).toFixed(0).padStart(2)+"% L "+(100*l/sub.length).toFixed(0).padStart(2)+"% pair "+(100*(w+d)/sub.length).toFixed(0)+"%"; }
  console.log("  "+zk.padEnd(8)+" agree   "+rate(ag));
  console.log("  "+zk.padEnd(8)+" disagree "+rate(dis));
});
