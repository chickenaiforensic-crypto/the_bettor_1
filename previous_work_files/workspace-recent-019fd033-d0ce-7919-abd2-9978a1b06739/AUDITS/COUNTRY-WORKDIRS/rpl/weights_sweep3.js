/* stage 3: band frontier + draw-mass integrity + champion per-bucket detail */
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
evX(`(function(){var orig=perfRatings;var cache={};perfRatings=function(h,a,c){var k=h+"|"+a+"|"+c;if(!(k in cache))cache[k]=orig(h,a,c);return cache[k];};})()`);
const G=[];
matches.forEach(m=>{
  if(!m.homeId||!m.awayId||m.homeId===m.awayId)return;
  const r=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");if(!ev||!ev.ag)return null;return {paths:ev.paths.map(function(p){return {phase:p.phase,estimate:p.estimate,weight:p.weight,ids:p.ids};})};})()");
  if(!r)return;
  G.push({h:m.homeId,a:m.awayId,date:m.date,actual:m.hg>m.ag?"H":m.hg<m.ag?"A":"D",paths:r.paths});
});
function buildAgg(paths,wH2H,wCOM,w3RD,band){
  const P=paths.map(p=>{let w=p.phase==="h2h"?p.weight/3*wH2H:p.phase==="common"?p.weight/2*wCOM:p.weight/1.5*w3RD;return {phase:p.phase,estimate:p.estimate,weight:w,ids:p.ids};});
  const totalW=P.reduce((a,p)=>a+p.weight,0);
  let homeW=0,awayW=0,neuW=0,phaseCounts={h2h:0,common:0,third:0};
  P.forEach(p=>{phaseCounts[p.phase]++;if(p.estimate>band)homeW+=p.weight;else if(p.estimate<-band)awayW+=p.weight;else neuW+=p.weight;});
  const weighted=P.reduce((a,p)=>a+p.estimate*p.weight,0)/totalW;
  const agree=Math.max(homeW,awayW,neuW)/totalW;
  const unique={},dedup=[];P.forEach(p=>{const k=p.ids.slice().sort().join("~");if(!unique[k]){unique[k]=1;dedup.push(p);}});
  dedup.sort((a,b)=>(b.weight*Math.abs(b.estimate))-(a.weight*Math.abs(a.estimate)));
  const used={};let independent=0;
  dedup.forEach(p=>{if(p.ids.some(id=>used[id]))return;independent++;p.ids.forEach(id=>used[id]=1);});
  return {paths:P,ag:{weighted:weighted,unweighted:P.reduce((a,p)=>a+p.estimate,0)/P.length,homeW:homeW,awayW:awayW,neuW:neuW,agree:agree,effective:independent,phaseCounts:phaseCounts}};
}
function runConfig(c,subset){
  let ll=0,n=0,dS=0;const zones={};
  for(const g of(subset||G)){
    const {paths,ag}=buildAgg(g.paths,c.h2h,c.com,c.trd,c.band);
    const z=evX("(function(){var z=computeZoneCtx("+JSON.stringify(paths)+","+JSON.stringify(ag)+","+JSON.stringify(g.h)+","+JSON.stringify(g.a)+","+JSON.stringify(g.date)+");return {key:z.key,side:z.side};})()");
    const tw=ag.homeW+ag.neuW+ag.awayW;
    const pA=g.actual==="H"?ag.homeW/tw:g.actual==="D"?ag.neuW/tw:ag.awayW/tw;
    ll+=-Math.log(Math.max(pA,0.01));n++;dS+=ag.neuW/tw;
    const leader=z.side==="TA"?"H":"A";
    zones[z.key]=zones[z.key]||{n:0,w:0,d:0,l:0};
    zones[z.key].n++;if(g.actual===leader)zones[z.key].w++;else if(g.actual==="D")zones[z.key].d++;else zones[z.key].l++;
  }
  const order=["strong","win","windraw","lean","toss"];
  const ladder=order.filter(k=>zones[k]).map(k=>+(100*zones[k].w/zones[k].n).toFixed(1));
  const monotone=ladder.every((v,i,a)=>i===0||a[i-1]>=v-0.01);
  const act=["strong","win","windraw"].reduce((o,k)=>zones[k]?{n:o.n+zones[k].n,w:o.w+zones[k].w,p:o.p+zones[k].w+zones[k].d}:o,{n:0,w:0,p:0});
  return {ll:ll/n,drawShare:dS/n,zones:zones,ladder:ladder,monotone:monotone,actW:act.n?100*act.w/act.n:0,actPair:act.n?100*act.p/act.n:0,actN:act.n};
}
console.log("actual draw rate: 24.3%");
[[3,3,0.75],[3,2,0.5]].forEach(w=>{
  [0.50,0.55,0.60,0.65,0.70].forEach(bd=>{
    const c={h2h:w[0],com:w[1],trd:w[2],band:bd};
    const f=runConfig(c);
    console.log(`${w[0]}/${w[1]}/${w[2]} band ${bd.toFixed(2)}  ll ${f.ll.toFixed(4)}  meanDrawShare ${(100*f.drawShare).toFixed(1)}%  actW ${f.actW.toFixed(1)} pair ${f.actPair.toFixed(1)} n ${f.actN} mono ${f.monotone} ${JSON.stringify(f.ladder)}`);
  });
});
[0.25].forEach(t=>{
  const c={h2h:3,com:2,trd:t,band:0.5}; const f=runConfig(c);
  console.log(`3/2/${t} band 0.50  ll ${f.ll.toFixed(4)}  meanDrawShare ${(100*f.drawShare).toFixed(1)}%  actW ${f.actW.toFixed(1)} pair ${f.actPair.toFixed(1)} n ${f.actN} mono ${f.monotone}`);
});
// champion detail
const champ={h2h:3,com:3,trd:0.75,band:0.5};
const cf=runConfig(champ);
console.log("\nCHAMPION 3/3/0.75 band 0.50 zone table:");
["strong","win","windraw","lean","toss"].forEach(k=>{const z=cf.zones[k];if(!z)return;
  console.log(`  ${k.padEnd(8)} n=${String(z.n).padEnd(3)} W ${(100*z.w/z.n).toFixed(0).padStart(2)}% D ${(100*z.d/z.n).toFixed(0)}% L ${(100*z.l/z.n).toFixed(0)}% pair ${(100*(z.w+z.d)/z.n).toFixed(0)}%`);});
fs.writeFileSync("/home/user/rpl/weights_champ.json",JSON.stringify({cfg:champ,ll:cf.ll,drawShare:cf.drawShare,ladder:cf.ladder,zones:cf.zones,actW:cf.actW,actPair:cf.actPair,actN:cf.actN},null,1));
