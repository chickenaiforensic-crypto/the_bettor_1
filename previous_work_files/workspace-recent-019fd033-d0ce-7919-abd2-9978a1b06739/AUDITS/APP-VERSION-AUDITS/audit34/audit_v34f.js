const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit34/app-v3.4.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
// snapshot rows from correct wrapper
const R=PR.requests.createCentralRequest(s,derived,'2026-08-02');
const snap=JSON.parse(R.snapshotJson);
const inner=snap['pitch-rating-v3.store']||snap;
console.log('snapshot: format=',snap.format,'| requestDate=',snap.requestDate,'| storeHash=',snap.storeHash,'| wrapped inner matches=',(inner.matches||snap.matches||[]).length);
// open request first
PR.ui.newCentralRequest(s,derived,'2026-08-02');
// plain-pack return (the real D12-4 shape)
const retText='BP-TEAM-PACK v2\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nMATCH|2026-08-02|Russian Premier League|domestic-league|Zenit St Petersburg|1|1|Spartak Moscow|normal|unknown|St Petersburg|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated MD3 rows\nEND\n';
const r=PR.requests.parseReturn(s,retText,'2026-08-02');
console.log('\nparseReturn(plain pack): ok='+r.ok);
r.blocks.forEach((b,i)=>console.log('  block',i,'ok='+b.ok,'matches='+b.matches,'teams='+b.teams,'codes='+JSON.stringify(b.codes),'errors:',JSON.stringify((b.errors||[]).slice(0,4))));
if(r.ok){
  const open=PR.requests.openRequest(s);
  const f={name:'central-request-20260802-r1.txt',isReturn:true,returnBlocks:r.blocks,requestDate:'2026-08-02',matched:!!open};
  const before={log:s.log.length,matches:s.matches.length};
  PR.ui.commitReturn(s,derived,f);
  console.log('commitReturn: matches',before.matches,'→',s.matches.length,'(+2 expected)');
  s.log.slice(before.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,115)));
  const rq=s.artifacts.find(a=>a.kind==='central-request');
  console.log('request state:',rq.data.state,'| RPL section:',JSON.stringify(rq.data.sections.find(x=>x.code==='RPL')));
}
