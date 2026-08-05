/* replay_losses.js — extract every STRONG/WIN zone call from the 632-game masked replay
   where the zone LEADER actually lost. Bit-exact replication of zone_tally_ctx.js pool. */
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
const RPL=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_universe.json","utf8"));
const NAMES=JSON.parse(fs.readFileSync("/home/user/rpl/rpl_names.json","utf8"));
const st=S.BlueprintEmbed.store();
[...new Set(RPL.flatMap(m=>[m.home,m.away]))].forEach(s=>{if(!st.identities[s])st.identities[s]={id:s,name:NAMES[s]||s};});
RPL.forEach(m=>st.matches.push({id:[m.date,m.comp,m.home,m.away,m.hg,m.ag,"home"].join("|"),date:m.date,competition:m.comp,homeId:m.home,awayId:m.away,hg:m.hg,ag:m.ag,venue:"home"}));
const matches=st.matches.slice().sort((a,b)=>a.date.localeCompare(b.date));
const out=[];
matches.forEach(m=>{
  if(!m.homeId||!m.awayId||m.homeId===m.awayId)return;
  const r=evX("(function(){var ev=BlueprintEmbed.analyze("+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "if(!ev||!ev.ag)return null;var z=computeZoneCtx(ev.paths,ev.ag,"+JSON.stringify(m.homeId)+","+JSON.stringify(m.awayId)+","+JSON.stringify(m.date)+");"+
    "return {key:z.key,side:z.side,S_:z.S_,agree:z.agree,contra:z.contra.map(function(c){return {name:c.name,lead:c.lead};}),gatedFrom:z.gatedFrom,c5From:z.c5From,c8From:z.c8From,"+
    "secs:z.secs.map(function(s){return {name:s.name,hW:s.hW,dW:s.dW,aW:s.aW,W:s.W,side:s.side,lead:s.lead};}),"+
    "perf:z.perf||null,pc:ev.ag.phaseCounts||null,n:ev.paths.length};})()");
  if(!r)return;
  if(r.key!=="strong"&&r.key!=="win")return;
  const actual=m.hg>m.ag?"H":m.hg<m.ag?"A":"D";
  const leader=r.side==="TA"?"H":"A";
  if(actual===leader||actual==="D")return;           /* losses only */
  const lg=leader==="H"?m.hg:m.ag, wg=leader==="H"?m.ag:m.hg;
  out.push({date:m.date,home:m.homeId,away:m.awayId,score:m.hg+"-"+m.ag,
    leader:leader==="H"?m.homeId:m.awayId,winner:leader==="H"?m.awayId:m.homeId,
    margin:wg-lg,zone:(r.side==="TA"?"TA ":"TB ")+(r.key==="strong"?"STRONG ":"WIN ")+r.S_.toFixed(1)+"%",
    key:r.key,agree:r.agree,contra:r.contra,gatedFrom:r.gatedFrom,c5From:r.c5From,c8From:r.c8From,
    secs:r.secs.map(s=>({name:s.name,bal:(100*s.hW/s.W).toFixed(1)+"/"+(100*s.dW/s.W).toFixed(1)+"/"+(100*s.aW/s.W).toFixed(1),leadSide:s.side,lead:+s.lead.toFixed(1)})),
    perf:r.perf?{starH:+r.perf.starH.toFixed(1),starA:+r.perf.starA.toFixed(1),
      h:r.perf.home?{n:r.perf.home.n,sos:+r.perf.home.sos.toFixed(1),perf:+r.perf.home.perf.toFixed(1)}:null,
      a:r.perf.away?{n:r.perf.away.n,sos:+r.perf.away.sos.toFixed(1),perf:+r.perf.away.perf.toFixed(1)}:null}:null,
    paths:r.n,pc:r.pc});
});
out.sort((a,b)=>b.margin-a.margin||a.date.localeCompare(b.date));
fs.writeFileSync("/home/user/rpl/replay_losses.json",JSON.stringify(out,null,1));
console.log("leader-loss games on STRONG+WIN:",out.length);
out.forEach(g=>{
  const secs=g.secs.map(s=>s.name+" "+s.bal+" (lead "+s.leadSide+" "+s.lead+")").join(" | ");
  const perf=g.perf?("stars "+g.perf.starH+"/"+g.perf.starA+" perf "+(g.perf.h?g.perf.h.perf:"-")+"/"+(g.perf.a?g.perf.a.perf:"-")):"no-perf";
  console.log(g.date,g.home+" "+g.score+" "+g.away,"| margin",g.margin,"|",g.zone,"| agree",g.agree,
    (g.c8From?"C8demoted-from-"+g.c8From:""),(g.gatedFrom?"gated":""),(g.c5From?"c5":""));
  console.log("   secs:",secs);
  console.log("   ",perf,"paths",g.paths,"contra:",JSON.stringify(g.contra));
});
