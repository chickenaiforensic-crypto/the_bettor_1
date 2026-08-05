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

// recent Czech dates sanity
console.log("recent czech rows:", evX(`(function(){var st=BlueprintEmbed.store();
  return st.matches.filter(function(m){return /Czech|MOL/.test(m.competition||"");}).map(function(m){return m.date;}).sort().slice(-8);})()`).join(","));

function bpGame(homeQ, awayQ, cutoff){
  return evX(`(function(){
    var st=BlueprintEmbed.store();
    function find(q){var k=Object.keys(st.identities).filter(function(x){return x.indexOf(q)>=0;});return k[0];}
    var h=find("${homeQ}"), a=find("${awayQ}");
    if(!h||!a) return {error:"unresolved ${homeQ}/${awayQ}"};
    var ev=BlueprintEmbed.analyze(h,a,"${cutoff}");
    if(!ev||!ev.ag) return {error:"no paths", n:ev?ev.paths.length:0};
    var z=computeZoneCtx(ev.paths,ev.ag,h,a,"${cutoff}");
    var tw=ev.ag.homeW+ev.ag.neuW+ev.ag.awayW;
    return {home:st.identities[h].name, away:st.identities[a].name,
      secs:z.secs.map(function(s){return {name:s.name,h:(100*s.hW/s.W).toFixed(0),d:(100*s.dW/s.W).toFixed(0),a:(100*s.aW/s.W).toFixed(0),W:+s.W.toFixed(1)};}),
      TA:(100*ev.ag.homeW/tw).toFixed(1), D:(100*ev.ag.neuW/tw).toFixed(1), TB:(100*ev.ag.awayW/tw).toFixed(1),
      zone:z.tag, S_:+z.S_.toFixed(1), paths:ev.paths.length, eff:+ev.ag.effective.toFixed(0), agree:+ev.ag.agree.toFixed(2),
      perf:z.perf?{starH:+z.perf.starH.toFixed(0),starA:+z.perf.starA.toFixed(0),coldH:!z.perf.home,coldA:!z.perf.away}:null,
      flags:[z.gatedFrom?"gated:"+z.gatedFrom:null,z.c5From?"draw-risk":null,z.c8From?"perf:"+z.c8From:null,z.c11From?"star:"+z.c11From:null,z.ctxFrom?"ctx:"+z.ctxFrom:null].filter(Boolean)};})()`);
}
const bpSlate = [
 ["cska","krylja|krylya","2026-08-01"],["makhachkala","lokomotiv","2026-08-01"],["baltika","dinamo-moscow","2026-08-01"],
 ["orenburg","zenit","2026-08-02"],["krasnodar","fakel","2026-08-02"],["akhmat","spartak","2026-08-02"],
 ["liberec","teplice","2026-08-01"],["viktoria-plzen|viktoria plzen","zbrojovka","2026-08-01"],
 ["ostrava","slavia","2026-08-01"],["slovacko","artis","2026-08-01"],
 ["sigma","mlada","2026-08-02"],["bohemians","hradec","2026-08-02"],["pardubice","jablonec","2026-08-02"]
];
bpSlate.forEach(g=>{
  // resolve via identity key parts: use name fragment on key (id format country|name norm)
  const out = bpGame(g[0].split("|")[0], g[1].split("|")[0], g[2]);
  console.log("BP", g[2], JSON.stringify(out));
});

const scSlate = [["Falkirk","St Mirren","2026-08-01"],["Aberdeen","Hearts","2026-08-01"],
 ["St Johnstone","Kilmarnock","2026-08-02"],["Hibernian","Motherwell","2026-08-02"],["Celtic","Dundee","2026-08-03"]];
scSlate.forEach(p=>{
  const r = evX(`(function(){var r=rateFixture("SC0","${p[0]}","${p[1]}");
    if(r.error)return r;
    return {H:+(100*r.H).toFixed(1),D:+(100*r.D).toFixed(1),A:+(100*r.A).toFixed(1),lh:+r.lh.toFixed(2),la:+r.la.toFixed(2),
      expScore:r.expScore,stars:[r.starsHome,r.starsAway],tier:r.tier.name,cons:r.consensus?+r.consensus.consensus.toFixed(2):null,
      conf:r.confidence?r.confidence.label:null,top:r.topScores.slice(0,3).map(function(t){return t.s+" "+(100*t.p).toFixed(1)+"%";})};})()`);
  console.log("MODEL", p[2], p[0], "v", p[1], JSON.stringify(r));
});
