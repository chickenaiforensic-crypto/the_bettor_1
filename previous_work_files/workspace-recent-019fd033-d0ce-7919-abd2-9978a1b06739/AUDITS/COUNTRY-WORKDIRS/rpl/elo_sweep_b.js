/* elo_sweep_b.js — stage B: candidate Elo/star params -> downstream zone table + gates.
   perfRatings is global -> safe override per config. C7 weights in force. */
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
console.log("pool:",G.length);
function perfFactory(K,HF,C,STAR_S,boundary){
  return `perfRatings=function(homeId,awayId,cutoff){
    var ms=(BlueprintEmbed.store().matches||[]).filter(function(m){return m.date&&m.date<cutoff&&typeof m.hg==="number"&&typeof m.ag==="number";});
    ms.sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:0;});
    var E={},K=${K},HF=${HF};
    ms.forEach(function(m){var eh=E[m.homeId]||1500,ea=E[m.awayId]||1500;
      var p=1/(1+Math.pow(10,-((eh+HF-ea)/400)));
      var sc=m.hg>m.ag?1:m.hg<m.ag?0:0.5;
      E[m.homeId]=eh+K*(sc-p);E[m.awayId]=ea+K*((1-sc)-(1-p));});
    function star(e){return Math.max(0,Math.min(100,(e-${C})/${STAR_S}));}
    function tourneyStart(d){var y=+d.slice(0,4),mo=+d.slice(5,7);return ${boundary==="jul1"?`((mo>=7?y:y-1)+"-07-01")`:boundary==="aug1"?`(y+"-08-01")`:`((mo>=7?y:y-1)+"-07-01")`};}
    function perf(team){var ss=tourneyStart(cutoff),n=0,sos=0,pf=0;
      ms.forEach(function(m){
        ${boundary==="last6"?``:`if(m.date<ss)return;`}
        var h=m.homeId===team;if(!h&&m.awayId!==team)return;
        var opp=h?m.awayId:m.homeId;var f=h?m.hg:m.ag,c=h?m.ag:m.hg;
        var st=star(E[opp]||1500);sos+=st;pf+=(f>c?1:f===c?0.5:0)*st;n++;});
      ${boundary==="last6"?`return n>=3?{n:Math.min(n,6),sos:sos/n,perf:pf/n}:null;`:`return n>=3?{n:n,sos:sos/n,perf:pf/n}:null;`}}
    ${boundary==="last6"?`function perfLast6(team){var g=ms.filter(function(m){return m.homeId===team||m.awayId===team;}).slice(-6);if(g.length<3)return null;var sos=0,pf=0;
      g.forEach(function(m){var h=m.homeId===team,opp=h?m.awayId:m.homeId;var f=h?m.hg:m.ag,c=h?m.ag:m.hg;var st=star(E[opp]||1500);sos+=st;pf+=(f>c?1:f===c?0.5:0)*st;});
      return {n:g.length,sos:sos/g.length,perf:pf/g.length};}
    return {starH:star(E[homeId]||1500),starA:star(E[awayId]||1500),home:perfLast6(homeId),away:perfLast6(awayId)};`
    :`return {starH:star(E[homeId]||1500),starA:star(E[awayId]||1500),home:perf(homeId),away:perf(awayId)};`}}
  `;
}
function runVariant(label,fn){
  evX(fn);
  const zones={};let c11=0,c8=0;
  for(const g of G){
    const z=evX("(function(){var z=computeZoneCtx("+JSON.stringify(g.paths)+","+JSON.stringify(g.ag)+","+JSON.stringify(g.h)+","+JSON.stringify(g.a)+","+JSON.stringify(g.date)+");return {key:z.key,side:z.side,c8:z.c8From||null,c11:z.c11From||null};})()");
    const leader=z.side==="TA"?"H":"A";
    zones[z.key]=zones[z.key]||{n:0,w:0,d:0,l:0};
    zones[z.key].n++;if(g.actual===leader)zones[z.key].w++;else if(g.actual==="D")zones[z.key].d++;else zones[z.key].l++;
    if(z.c11)c11++; if(z.c8)c8++;
  }
  const order=["strong","win","windraw","lean","toss"];
  const ladder=order.filter(k=>zones[k]).map(k=>+(100*zones[k].w/zones[k].n).toFixed(1));
  const mono=ladder.every((v,i,a)=>i===0||a[i-1]>=v-0.01);
  const act=["strong","win","windraw"].reduce((o,k)=>zones[k]?{n:o.n+zones[k].n,w:o.w+zones[k].w,p:o.p+zones[k].w+zones[k].d}:o,{n:0,w:0,p:0});
  console.log(`${label.padEnd(22)} actW ${(100*act.w/act.n).toFixed(1)} pair ${(100*act.p/act.n).toFixed(1)} n ${String(act.n).padEnd(3)} mono ${mono} ladder ${JSON.stringify(ladder)} c8 ${c8} c11 ${c11}`);
  return {label,zones,ladder,mono,actW:100*act.w/act.n,actPair:100*act.p/act.n,actN:act.n,c8,c11};
}
const out=[];
out.push(runVariant("BASE K20 HF65 (1420/2)",perfFactory(20,65,1420,2,"jul1")));
out.push(runVariant("K32 HF65",perfFactory(32,65,1420,2,"jul1")));
out.push(runVariant("K40 HF65",perfFactory(40,65,1420,2,"jul1")));
out.push(runVariant("K48 HF65",perfFactory(48,65,1420,2,"jul1")));
out.push(runVariant("K64 HF65",perfFactory(64,65,1420,2,"jul1")));
out.push(runVariant("K40 HF85",perfFactory(40,85,1420,2,"jul1")));
out.push(runVariant("K40 (1400/2.5)",perfFactory(40,65,1400,2.5,"jul1")));
out.push(runVariant("K40 last6-window",perfFactory(40,65,1420,2,"last6")));
fs.writeFileSync("/home/user/rpl/elo_sweep_b.json",JSON.stringify(out,null,1));
console.log("saved rpl/elo_sweep_b.json");
