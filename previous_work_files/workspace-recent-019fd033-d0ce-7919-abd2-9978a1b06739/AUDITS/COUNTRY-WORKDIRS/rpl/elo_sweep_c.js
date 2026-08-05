/* elo_sweep_c.js — stage C: rolling window variants + C8-gate cohort loss
   concentration test. Gate validity = demoted cohort carries enriched losses. */
const fs=require("fs"), vm=require("vm");
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
const matches=st.matches.slice().sort((a,b)=>a.date.localeCompare(b.date));
const G=[];
matches.forEach(m=>{
  if(!m.homeId||!m.awayId||m.homeId===m.awayId)return;
  const r=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");if(!ev||!ev.ag)return null;return {paths:ev.paths.map(function(p){return {phase:p.phase,estimate:p.estimate,weight:p.weight,ids:p.ids};}),ag:{homeW:ev.ag.homeW,neuW:ev.ag.neuW,awayW:ev.ag.awayW,agree:ev.ag.agree,effective:ev.ag.effective,weighted:ev.ag.weighted,unweighted:ev.ag.unweighted,phaseCounts:ev.ag.phaseCounts}};})()");
  if(!r)return;
  G.push({h:m.homeId,a:m.awayId,date:m.date,actual:m.hg>m.ag?"H":m.hg<m.ag?"A":"D",paths:r.paths,ag:r.ag});
});
function perfFactory(K,HF,C,STAR_S,WIN){
  if(WIN==="jul1"){
    return `perfRatings=function(homeId,awayId,cutoff){
      var ms=(BlueprintEmbed.store().matches||[]).filter(function(m){return m.date&&m.date<cutoff&&typeof m.hg==="number"&&typeof m.ag==="number";});
      ms.sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:0;});
      var E={},K=${K},HF=${HF};
      ms.forEach(function(m){var eh=E[m.homeId]||1500,ea=E[m.awayId]||1500;var p=1/(1+Math.pow(10,-((eh+HF-ea)/400)));var sc=m.hg>m.ag?1:m.hg<m.ag?0:0.5;E[m.homeId]=eh+K*(sc-p);E[m.awayId]=ea+K*((1-sc)-(1-p));});
      function star(e){return Math.max(0,Math.min(100,(e-${C})/${STAR_S}));}
      function perf(team){var y=+cutoff.slice(0,4),mo=+cutoff.slice(5,7);var ss=(mo>=7?y:y-1)+"-07-01";var n=0,sos=0,pf=0;
        ms.forEach(function(m){if(m.date<ss)return;var h=m.homeId===team;if(!h&&m.awayId!==team)return;var opp=h?m.awayId:m.homeId;var f=h?m.hg:m.ag,c=h?m.ag:m.hg;var st=star(E[opp]||1500);sos+=st;pf+=(f>c?1:f===c?0.5:0)*st;n++;});
        return n>=3?{n:n,sos:sos/n,perf:pf/n}:null;}
      return {starH:star(E[homeId]||1500),starA:star(E[awayId]||1500),home:perf(homeId),away:perf(awayId)};}`;
  }
  const N=+WIN.slice(4);
  return `perfRatings=function(homeId,awayId,cutoff){
    var ms=(BlueprintEmbed.store().matches||[]).filter(function(m){return m.date&&m.date<cutoff&&typeof m.hg==="number"&&typeof m.ag==="number";});
    ms.sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:0;});
    var E={},K=${K},HF=${HF};
    ms.forEach(function(m){var eh=E[m.homeId]||1500,ea=E[m.awayId]||1500;var p=1/(1+Math.pow(10,-((eh+HF-ea)/400)));var sc=m.hg>m.ag?1:m.hg<m.ag?0:0.5;E[m.homeId]=eh+K*(sc-p);E[m.awayId]=ea+K*((1-sc)-(1-p));});
    function star(e){return Math.max(0,Math.min(100,(e-${C})/${STAR_S}));}
    function perf(team){var g=ms.filter(function(m){return m.homeId===team||m.awayId===team;}).slice(-${N});if(g.length<3)return null;var sos=0,pf=0;
      g.forEach(function(m){var h=m.homeId===team,opp=h?m.awayId:m.homeId;var f=h?m.hg:m.ag,c=h?m.ag:m.hg;var st=star(E[opp]||1500);sos+=st;pf+=(f>c?1:f===c?0.5:0)*st;});
      return {n:g.length,sos:sos/g.length,perf:pf/g.length};}
    return {starH:star(E[homeId]||1500),starA:star(E[awayId]||1500),home:perf(homeId),away:perf(awayId)};}`;
}
function zones_for(){
  const zones={};const per=[];
  for(const g of G){
    const z=evX("(function(){var z=computeZoneCtx("+JSON.stringify(g.paths)+","+JSON.stringify(g.ag)+","+JSON.stringify(g.h)+","+JSON.stringify(g.a)+","+JSON.stringify(g.date)+");return {key:z.key,side:z.side,c8:!!z.c8From,c11:!!z.c11From};})()");
    const leader=z.side==="TA"?"H":"A";
    zones[z.key]=zones[z.key]||{n:0,w:0,d:0,l:0};
    zones[z.key].n++;if(g.actual===leader)zones[z.key].w++;else if(g.actual==="D")zones[z.key].d++;else zones[z.key].l++;
    per.push({side:z.side,key:z.key,actual:g.actual,c8:z.c8,c11:z.c11,leader:leader});
  }
  return {zones:zones,per:per};
}
function report(label,K,win){
  evX(perfFactory(K,65,1420,2,win));
  const {zones,per}=zones_for();
  const order=["strong","win","windraw","lean","toss"];
  const ladder=order.filter(k=>zones[k]).map(k=>+(100*zones[k].w/zones[k].n).toFixed(1));
  const mono=ladder.every((v,i,a)=>i===0||a[i-1]>=v-0.01);
  const act=per.filter(p=>["strong","win","windraw"].includes(p.key));
  const actW=100*act.filter(p=>p.actual===p.leader).length/act.length;
  const actPair=100*act.filter(p=>p.actual!=="D"?p.actual===p.leader:true).length/act.length;
  // gate cohort test: games where C8 fired AND baseline(C7,jul1,K20) would have been actionable
  const fired=per.filter(p=>p.c8);
  const fW=fired.length?100*fired.filter(p=>p.actual===p.leader).length/fired.length:0;
  const fL=fired.length?100*fired.filter(p=>p.actual!=="D"&&p.actual!==p.leader).length/fired.length:0;
  const kept=per.filter(p=>!p.c8&&["strong","win","windraw"].includes(p.key));
  const kW=kept.length?100*kept.filter(p=>p.actual===p.leader).length/kept.length:0;
  console.log(`${label.padEnd(18)} actW ${actW.toFixed(1)} pair ${actPair.toFixed(1)} n ${String(act.length).padEnd(3)} mono ${mono} ${JSON.stringify(ladder)} | c8 fired ${fired.length}: W ${fW.toFixed(0)}% L ${fL.toFixed(0)}%  vs kept W ${kW.toFixed(0)}%`);
  return {label,actW,actPair,actN:act.length,mono,ladder,fired:fired.length,fW,kW};
}
const out=[];
out.push(report("BASE K20 jul1",20,"jul1"));
out.push(report("K32 jul1",32,"jul1"));
out.push(report("K20 last6",20,"last6"));
out.push(report("K32 last6",32,"last6"));
out.push(report("K32 last8",32,"last8"));
out.push(report("K32 last10",32,"last10"));
out.push(report("K40 last8",40,"last8"));
fs.writeFileSync("/home/user/rpl/elo_sweep_c.json",JSON.stringify(out,null,1));
