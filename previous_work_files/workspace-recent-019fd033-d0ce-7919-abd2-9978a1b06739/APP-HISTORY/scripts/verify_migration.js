/* v2.8.4 migration proof: old store ('NA' league tags) -> re-import new pack ->
   league codes land, NA scrubbed, Akron v Rubin replay stays bit-exact. */
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
// simulate the user's CURRENT store: old pack state with 'NA' tags
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/russian-team-pack.txt","utf8")
  .replace(/\|RPL\|/g,"|NA|").replace(/\|FNL\|/g,"|NA|");  // old-format pack
evX("BlueprintEmbed.importData()");
console.log("old import blocked?", /Load blocked/.test(els["bpImportReport"].innerHTML),
  "| leagues before:", JSON.stringify(evX("(function(){var st=BlueprintEmbed.store();var k=Object.keys(st.identities).filter(function(x){return /krylya/.test(x);})[0];return st.identities[k].leagues;})()")));
// user re-imports the NEW pack
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/russian-team-pack.txt","utf8");
evX("BlueprintEmbed.importData()");
console.log("new import blocked?", /Load blocked/.test(els["bpImportReport"].innerHTML));
console.log("leagues after:", JSON.stringify(evX("(function(){var st=BlueprintEmbed.store();var k=Object.keys(st.identities).filter(function(x){return /krylya/.test(x);})[0];return {leagues:st.identities[k].leagues, label:st.identities[k].name+' — '+st.identities[k].country+' / '+st.identities[k].leagues[0]};})()")));
console.log("store matches:", evX("BlueprintEmbed.store().matches.length"));
// bit-exact replay of the settled game (cutoff excludes its own row)
console.log("replay:", JSON.stringify(evX(`(function(){
  var st=BlueprintEmbed.store();
  var h=Object.keys(st.identities).filter(function(k){return /akron/.test(k);})[0];
  var a=Object.keys(st.identities).filter(function(k){return /rubin/.test(k);})[0];
  var ev=BlueprintEmbed.analyze(h,a,"2026-08-01");
  var z=computeZoneCtx(ev.paths,ev.ag,h,a,"2026-08-01");
  var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
  return {TA:(100*ev.ag.homeW/tw).toFixed(1),D:(100*ev.ag.neuW/tw).toFixed(1),TB:(100*ev.ag.awayW/tw).toFixed(1),tag:z.tag,paths:ev.paths.length};})()`)));
