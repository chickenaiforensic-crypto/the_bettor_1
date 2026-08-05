/* census_connectivity.js — per-league pair connectivity proof.
   For each stocked league: all same-league pairs -> how many have >=1 evidence
   path (H2H / common opponents / level-3 chain) vs zero. Also dumps one zero-path
   pair's loaded match involvement to show the mechanical reason. */
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id){return{id:id||"",value:"",innerHTML:"",textContent:"",className:"",style:{},checked:false,disabled:false,options:[],placeholder:"",appendChild(){},insertBefore(){},removeChild(){},remove(){},insertAdjacentHTML(p,h){this.innerHTML+=h;},querySelector(){return null;},querySelectorAll(){return[];},focus(){},select(){},click(){},setAttribute(){},getAttribute(){return null;},addEventListener(){},parentNode:null};}
const els={},sb={};sb.window=sb;sb.console=console;sb.navigator={};sb.setTimeout=()=>0;sb.confirm=()=>true;
sb.Blob=function(p){this.parts=p||[];};sb.FileReader=function(){this.readAsText=function(){};};sb.URL={createObjectURL:()=>"",revokeObjectURL(){}};
const ls={};sb.localStorage={getItem:k=>(k in ls?ls[k]:null),setItem:(k,v)=>{ls[k]=String(v);},removeItem:k=>{delete ls[k];}};
const md=makeEl("matchDate");md.parentNode={parentNode:{insertBefore(){}},nextSibling:null,insertBefore(){}};els["matchDate"]=md;
sb.document={readyState:"complete",body:makeEl("body"),getElementById(id){if(!els[id])els[id]=makeEl(id);return els[id];},createElement(t){return makeEl(t+Math.random());},querySelector(s){if(!els["q:"+s])els["q:"+s]=makeEl(s);return els["q:"+s];},querySelectorAll(){return[];},addEventListener(){}};
vm.createContext(sb);scripts.forEach((s,i)=>vm.runInContext(s,sb,{filename:"s"+i+".js"}));
const S=sb, evX=e=>vm.runInContext(e,sb);
["russian-team-pack.txt","czech-team-pack.txt","hibernian-team-pack.txt","malisheva-team-pack.txt","malisheva-closure-pack.txt","usa-team-pack.txt"].forEach(p=>{
  S.document.getElementById("bpImportText").value=fs.readFileSync("/home/user/packs/"+p,"utf8");
  S.BlueprintEmbed.importData();
});
const st=S.BlueprintEmbed.store();
const cutoff="2026-08-02";
const SKIP={NA:1,unknown:1,"loaded team data":1,"":1};
const byLg={}, teamId={};
Object.keys(st.identities).forEach(k=>{
  const it=st.identities[k];
  (it.leagues||[]).forEach(raw=>{
    const lg=evX("canonLg("+JSON.stringify(raw)+")");
    if(SKIP[lg])return;
    (byLg[lg]=byLg[lg]||[]); if(!teamId[lg+"|"+it.name]){byLg[lg].push(it.name); teamId[lg+"|"+it.name]=k;}
  });
});
// only pack-loaded leagues (outside MODEL)
const PACK=["RPL","FNL","CZ1","CZ2","SC1","KOS","DEN","MLS","USL","USL1"];
console.log("league | teams | pairs | connected | zero-path | coverage");
PACK.forEach(lg=>{
  const ts=(byLg[lg]||[]);
  let conn=0, zero=0, example=null;
  for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){
    const h=teamId[lg+"|"+ts[i]], a=teamId[lg+"|"+ts[j]];
    const ev=S.BlueprintEmbed.analyze(h,a,cutoff);
    if(ev.paths.length>0)conn++; else {zero++; if(!example)example={h:ts[i],a:ts[j],hid:h,aid:a};}
  }
  const tot=conn+zero;
  console.log(lg+" | "+ts.length+" | "+tot+" | "+conn+" | "+zero+" | "+(tot?Math.round(100*conn/tot):0)+"%");
  if(example){
    const per=t=>st.matches.filter(m=>!m.muted&&(m.homeId===t||m.awayId===t)&&m.date<cutoff);
    const nm=id=>st.identities[id]&&st.identities[id].name;
    const mh=per(example.hid), ma=per(example.aid);
    const opps=id=>new Set(st.matches.filter(m=>!m.muted&&(m.homeId===id||m.awayId===id)&&m.date<cutoff).map(m=>m.homeId===id?m.awayId:m.homeId));
    const oh=opps(example.hid), oa=opps(example.aid);
    const inter=[...oh].filter(x=>oa.has(x));
    console.log("   zero-path example: "+example.h+" ("+mh.length+" matches v "+[...oh].map(nm).slice(0,8).join(",")+") vs "+example.a+" ("+ma.length+" matches v "+[...oa].map(nm).slice(0,8).join(",")+") -> common opponents: "+inter.length);
  }
});
// also: zero-path pair standalone form availability
console.log("\nstandalone form on a zero-path pair (perf computed from each side's OWN matches, no connection needed):");
const lg="MLS", ts=byLg[lg];
outer:
for(let i=0;i<ts.length;i++)for(let j=i+1;j<ts.length;j++){
  const h=teamId[lg+"|"+ts[i]], a=teamId[lg+"|"+ts[j]];
  const ev=S.BlueprintEmbed.analyze(h,a,cutoff);
  if(ev.paths.length===0){
    const pr=evX("perfRatings("+JSON.stringify(h)+","+JSON.stringify(a)+","+JSON.stringify(cutoff)+")");
    console.log(ts[i]+" v "+ts[j]+": starH="+pr.starH.toFixed(0)+" starA="+pr.starA.toFixed(0)+
      " homeGames="+(pr.home?pr.home.n:"<3")+" awayGames="+(pr.away?pr.away.n:"<3"));
    break outer;
  }
}
