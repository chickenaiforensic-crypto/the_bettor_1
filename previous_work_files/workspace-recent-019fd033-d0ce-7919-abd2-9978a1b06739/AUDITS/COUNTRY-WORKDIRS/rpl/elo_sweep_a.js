/* elo_sweep_a.js — CALIBRATION-8 stage A: Elo engine params (K, HF) judged on
   pure forward predictive quality across the canonical store matches (705 games).
   Metric: log-loss of Elo p(home) vs actual (1/0.5/0), + star-gap AUC. */
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
const ms=st.matches.filter(m=>m.date&&typeof m.hg==="number"&&typeof m.ag==="number").sort((a,b)=>a.date<b.date?-1:a.date>b.date?1:0);
console.log("games in store:",ms.length);

function eloChain(K,HF){
  const E={},records=[];
  ms.forEach(m=>{
    const eh=E[m.homeId]||1500, ea=E[m.awayId]||1500;
    const p=1/(1+Math.pow(10,-((eh+HF-ea)/400)));
    const sc=m.hg>m.ag?1:m.hg<m.ag?0:0.5;
    records.push({h:m.homeId,a:m.awayId,eh:eh,ea:ea,p:p,sc:sc,date:m.date});
    E[m.homeId]=eh+K*(sc-p);
    E[m.awayId]=ea+K*((1-sc)-(1-p));
  });
  return records;
}
function ll(recs){let s=0;recs.forEach(r=>{const p=Math.min(0.99,Math.max(0.01,r.p));s+=r.sc===1?-Math.log(p):r.sc===0?-Math.log(1-p):-Math.log(1-Math.abs(2*p-1)/2)/2-0;});return s/recs.length;}
// draw-aware loss: use sc in {1,0.5,0} with p_home interpreted as P(home wins incl half-draw info):
// standard approach: loss = |sc - p| mean absolute (robust for 3-way) + AUC on decisive games
function maeP(recs){let s=0;recs.forEach(r=>{s+=Math.abs(r.sc-r.p);});return s/recs.length;}
function auc(recs){
  const d=recs.filter(r=>r.sc!==0.5);
  let wins=0,ties=0,tot=0;
  for(let i=0;i<d.length;i++)for(let j=0;j<d.length;j++){
    if(d[i].sc>d[j].sc){tot++; if(d[i].p>d[j].p)wins++; else if(d[i].p===d[j].p)ties++;}
  }
  return tot?(wins+0.5*ties)/tot:0;
}
console.log("K/HF grid | Brier-MAE | AUC(decisive)");
const grid=[];
[12,16,20,24,32,40].forEach(K=>[45,65,85,100].forEach(HF=>grid.push([K,HF])));
const out=[];
grid.forEach(([K,HF])=>{
  const r=eloChain(K,HF);
  const m=maeP(r), a=auc(r);
  out.push({K:K,HF:HF,mae:m,auc:a});
  console.log(`K=${String(K).padEnd(3)} HF=${String(HF).padEnd(4)} MAE ${m.toFixed(4)} AUC ${a.toFixed(4)}${K===20&&HF===65?"  <- baseline":""}`);
});
out.sort((x,y)=>x.mae-y.mae);
console.log("best by MAE:",JSON.stringify(out[0]),"| best by AUC:",JSON.stringify(out.slice().sort((a,b)=>b.auc-a.auc)[0]));
fs.writeFileSync("/home/user/rpl/elo_sweep_a.json",JSON.stringify(out,null,1));

// frontier extension: K beyond 40
console.log("\nfrontier extension:");
[40,48,56,64,80,96].forEach(K=>{
  const r=eloChain(K,85);
  console.log(`K=${String(K).padEnd(3)} HF=85  MAE ${maeP(r).toFixed(4)} AUC ${auc(r).toFixed(4)}`);
});
