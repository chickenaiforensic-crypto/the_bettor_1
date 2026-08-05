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
const zones0={}, C8ZONES={};
function bump(t,z,res,lead){ t[z]=t[z]||{n:0,w:0,d:0,l:0}; t[z].n++; if(res===lead)t[z].w++; else if(res==="D")t[z].d++; else t[z].l++; }
const moved=[];
all.forEach(m=>{
  const z=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");if(!ev||!ev.ag)return null;var z=computeZone(ev.paths,ev.ag);return {key:z.key,side:z.side};})()");
  if(!z) return;
  const actual=m.hg>m.ag?"H":m.hg<m.ag?"A":"D";
  const lead=z.side==="TA"?"H":"A";
  bump(zones0,z.key,actual,lead);
  // C8 demote-only rule: perf delta contradicts zone leader -> one rung down. Cold start: no action.
  const E=eloAt(m.date), ph=perfAt(m.homeId,m.date,E), pa=perfAt(m.awayId,m.date,E);
  let key2=z.key;
  const ladder=["strong","win","windraw","lean","toss"];
  if(ph&&pa){ const dp=ph.perf-pa.perf;
    const disagree=(lead==="H"&&dp<0)||(lead==="A"&&dp>0);
    if(disagree){ const ix=ladder.indexOf(key2); key2=ladder[Math.min(4,ix+1)]; moved.push({d:m.date,from:z.key,to:key2,actual,lead}); } }
  bump(C8ZONES,key2,actual,lead);
});

function show(t,tag){ console.log(tag); let prev=101,mono=true;
  ["strong","win","windraw","lean","toss"].forEach(k=>{ const z=t[k]; if(!z)return;
    const w=100*z.w/z.n; if(w>prev+0.5) mono=false; prev=w;
    console.log("  "+k.padEnd(8),"n="+String(z.n).padEnd(4),"W "+(100*z.w/z.n).toFixed(0).padStart(2)+"%","D "+(100*z.d/z.n).toFixed(0).padStart(2)+"%","L "+(100*z.l/z.n).toFixed(0).padStart(2)+"%","pair "+(100*(z.w+z.d)/z.n).toFixed(0)+"%"); });
  console.log("  monotone W ladder:", mono ? "yes":"NO"); }
show(zones0,"baseline shipped v2.7.1:");
show(C8ZONES,"with C8 demote rule:");
console.log("moves:",moved.length, moved.reduce((o,r)=>{o[r.from+"->"+r.to]=(o[r.from+"->"+r.to]||0)+1;return o;},{}));
const dm=moved.filter(r=>r.from==="win"), dw=moved.filter(r=>r.from==="windraw");
function mt(sub,tag){ if(!sub.length){console.log(tag,"n=0");return;}
  const w=sub.filter(r=>r.actual===r.lead).length, d=sub.filter(r=>r.actual==="D").length, l=sub.length-w-d;
  console.log(tag,"n="+sub.length,"W "+(100*w/sub.length).toFixed(0)+"% D "+(100*d/sub.length).toFixed(0)+"% L "+(100*l/sub.length).toFixed(0)+"% pair "+(100*(w+d)/sub.length).toFixed(0)+"%"); }
mt(dm,"moved win->windraw:"); mt(dw,"moved windraw->lean:");
