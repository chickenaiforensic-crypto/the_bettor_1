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
const games=[["cska","krylya","2026-08-01"],["makhachkala","lokomotiv","2026-08-01"],["baltika","dynamo moscow","2026-08-01"],
 ["orenburg","zenit","2026-08-02"],["krasnodar","fakel","2026-08-02"],["akhmat","spartak","2026-08-02"],
 ["liberec","teplice","2026-08-01"],["viktoria plzen","zbrojovka","2026-08-01"],["ostrava","slavia","2026-08-01"],
 ["slovacko","artis","2026-08-01"],["sigma","mlada","2026-08-02"],["bohemians","hradec","2026-08-02"],["pardubice","jablonec","2026-08-02"]];
games.forEach(g=>{
  const r=evX(`(function(){var st=BlueprintEmbed.store();
    function find(q){return Object.keys(st.identities).filter(function(x){return x.indexOf(q)>=0;})[0];}
    var h=find("${g[0]}"),a=find("${g[1]}");
    var ev=BlueprintEmbed.analyze(h,a,"${g[2]}");
    var gr=evidenceGoalsEstimate(ev.paths,h,a,"${g[2]}");
    return {h:st.identities[h].name,a:st.identities[a].name,est:+gr.est.toFixed(2),region:gr.region,ev:+gr.ev.toFixed(2),b0:+gr.b0.toFixed(2),npaths:gr.npaths};})()`);
  console.log(JSON.stringify(r));
});
// settled-game sanity: Akron-Rubin (actual 3 goals)
console.log("SETTLED:", evX(`(function(){var st=BlueprintEmbed.store();
  var h=Object.keys(st.identities).filter(function(k){return /akron/.test(k);})[0];
  var a=Object.keys(st.identities).filter(function(k){return /rubin/.test(k);})[0];
  var ev=BlueprintEmbed.analyze(h,a,"2026-08-01");var gr=evidenceGoalsEstimate(ev.paths,h,a,"2026-08-01");
  return "Akron-Rubin est "+gr.est.toFixed(2)+" "+gr.region+" (actual 3)";})()`));
