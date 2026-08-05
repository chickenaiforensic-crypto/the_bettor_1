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
  if(/Load blocked/.test(els["bpImportReport"].innerHTML)) console.log("BLOCKED:",f);
});
console.log("store matches:", evX("BlueprintEmbed.store().matches.length"));
// Scotland rated teams?
console.log("SC0 rated teams:", JSON.stringify(evX("Object.keys(MODEL.teams.SC0)")));
// model rated check for the 5 fixtures
[["Falkirk","St Mirren"],["Aberdeen","Hearts"],["St Johnstone","Kilmarnock"],["Hibernian","Motherwell"],["Celtic","Dundee"]].forEach(p=>{
  const r = evX(`(function(){try{var r=rateFixture("SC0","${p[0]}","${p[1]}");return r.error?null:{H:r.pHome,D:r.pDraw,A:r.pAway,keys:Object.keys(r)};}catch(e){return 'ERR '+e;}})()`);
  console.log("MODEL", p[0], "v", p[1], "->", JSON.stringify(r));
});
// czech identity coverage for the round
console.log("czech identities:", JSON.stringify(evX(`(function(){var st=BlueprintEmbed.store();
  return Object.values(st.identities).filter(function(i){return i.country==="Czech Republic";}).map(function(i){return i.name;}).sort();})()`)));
