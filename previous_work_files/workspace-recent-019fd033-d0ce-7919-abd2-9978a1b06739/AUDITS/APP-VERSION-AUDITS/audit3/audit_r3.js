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
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
console.log('PR.ui exports:', Object.keys(PR.ui).join(','));
const r=PR.compute.selectFixture(s,derived,'Malisheva','Drita',{});
const pt=r.sections.find(x=>x.id==='paths');
console.log('\n== R3 records on compute sections (sec.home / sec.away) ==');
(pt.content.secs||[]).forEach(sec=>{
  console.log(' ', sec.name);
  console.log('   HOME:', JSON.stringify(sec.home));
  console.log('   AWAY:', JSON.stringify(sec.away));
});
// Hibernian v Malisheva H2H record sanity
const r2=PR.compute.selectFixture(s,derived,'Hibernian','Malisheva',{});
const pt2=r2.sections.find(x=>x.id==='paths');
(pt2.content.secs||[]).forEach(sec=>{ console.log(' HIB-MAL',sec.name,'HOME:',JSON.stringify(sec.home),'AWAY:',JSON.stringify(sec.away)); });
