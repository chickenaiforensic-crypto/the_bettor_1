const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('app-v3.1.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();
console.log('R1 flow pins:');
console.log(' empty query →', PR.ui.filterTeams(s,'').length, 'teams (expect 539)');
console.log(' "krasnodar"   →', JSON.stringify(PR.ui.filterTeams(s,'krasnodar')));
console.log(' "fakel"       →', JSON.stringify(PR.ui.filterTeams(s,'fakel')));
console.log(' "ross county" →', JSON.stringify(PR.ui.filterTeams(s,'ross county')));
console.log(' "hibs" (alias)→', JSON.stringify(PR.ui.filterTeams(s,'hibs')));
console.log(' "austin"      →', JSON.stringify(PR.ui.filterTeams(s,'austin')));
const idx=PR.ui.teamSearchIndex(s, s.identities.find(t=>t.name==='FC Krasnodar'));
console.log(' Krasnodar index league group:', idx.league);
