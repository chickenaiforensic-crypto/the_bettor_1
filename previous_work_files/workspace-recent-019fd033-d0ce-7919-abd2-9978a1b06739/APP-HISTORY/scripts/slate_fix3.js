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
["packs/russian-team-pack.txt","packs/czech-team-pack.txt","packs/hibernian-team-pack.txt","packs/malisheva-team-pack.txt","packs/malisheva-closure-pack.txt"].forEach(f=>{
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/"+f,"utf8");
  evX("BlueprintEmbed.importData()");
});
function bpGame(homeQ, awayQ, cutoff){
  return evX(`(function(){
    var st=BlueprintEmbed.store();
    function find(q){var k=Object.keys(st.identities).filter(function(x){return x.indexOf(q)>=0;});return k[0];}
    var h=find("${homeQ}"), a=find("${awayQ}");
    var ev=BlueprintEmbed.analyze(h,a,"${cutoff}");
    var z=computeZoneCtx(ev.paths,ev.ag,h,a,"${cutoff}");
    var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
    return {home:st.identities[h].name, away:st.identities[a].name,
      secs:z.secs.map(function(s){return {name:s.name,h:(100*s.hW/s.W).toFixed(0),d:(100*s.dW/s.W).toFixed(0),a:(100*s.aW/s.W).toFixed(0),W:+s.W.toFixed(1)};}),
      TA:(100*ev.ag.homeW/tw).toFixed(1), D:(100*ev.ag.neuW/tw).toFixed(1), TB:(100*ev.ag.awayW/tw).toFixed(1),
      zone:z.tag, S_:+z.S_.toFixed(1), paths:ev.paths.length, eff:+ev.ag.effective.toFixed(0), agree:+ev.ag.agree.toFixed(2),
      perf:z.perf?{starH:+z.perf.starH.toFixed(0),starA:+z.perf.starA.toFixed(0),coldH:!z.perf.home,coldA:!z.perf.away}:null,
      flags:[z.gatedFrom?"gated:"+z.gatedFrom:null,z.c5From?"draw-risk":null,z.c8From?"perf:"+z.c8From:null,z.c11From?"star:"+z.c11From:null,z.ctxFrom?"ctx:"+z.ctxFrom:null].filter(Boolean)};})()`);
}
[["cska","krylya","2026-08-01"],["baltika","dynamo moscow","2026-08-01"],["viktoria plzen","zbrojovka","2026-08-01"]].forEach(g=>{
  console.log("BP", g[2], JSON.stringify(bpGame(g[0], g[1], g[2])));
});
