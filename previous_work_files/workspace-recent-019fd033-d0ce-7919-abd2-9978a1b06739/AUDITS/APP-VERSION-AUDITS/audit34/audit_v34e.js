const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit34/app-v3.4.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){ return this._a?this._a:null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const downloads=[];
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''},
 URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}},
 HTMLAnchorElement: function(){}, };
sb.window=sb; sb.globalThis=sb;
// capture downloads: their download() likely creates <a> with click()
vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
// D12-1: the button
const out=PR.ui.newCentralRequest(s,derived,'2026-08-02');
console.log('D12-1 button →', JSON.stringify(out));
const rqArt=s.artifacts.find(a=>a.kind==='central-request');
console.log('open request artifact:', rqArt?('state='+rqArt.data.state+' file='+rqArt.data.requestFile+' snapshot='+rqArt.data.snapshotFile+' sections='+rqArt.data.sections.length):'NONE');
console.log('request log:', s.log[s.log.length-1].type+'/'+s.log[s.log.length-1].action,'|',String(s.log[s.log.length-1].summary).slice(0,100));
// snapshot json check
const R=PR.requests.createCentralRequest(s,derived,'2026-08-02');
const snap=JSON.parse(R.snapshotJson);
console.log('\nsnapshot file:',R.snapshotFile,'| bytes:',R.snapshotJson.length,'| keys:',Object.keys(snap.meta!==undefined? snap : store).slice(0,8).join(','),'| requestDate:',snap.meta&&snap.meta.requestDate,'| storeHash:',snap.meta&&snap.meta.storeHash);
console.log('snapshot matches rows:', (snap.matches||[]).length, '(expect 1436)');
// D12-4: return (simulate: researcher returns RPL section)
const retText='BP-TEAM-PACK v2\nSECTION|Russian Premier League|RPL\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated\nEND\n';
const PRr=PR.requests.parseReturn(s,retText,'2026-08-02');
console.log('\nparseReturn: ok='+PRr.ok,'blocks:',PRr.blocks.map(b=>({ok:b.ok,matches:b.matches,codes:b.codes})));
const open=PR.requests.openRequest(s);
const f={ name:'central-request-20260802-r1.txt', isReturn:true, returnBlocks:PRr.blocks, requestDate:'2026-08-02', matched:!!open };
const before={log:s.log.length,matches:s.matches.length};
PR.ui.commitReturn(s,derived,f);
console.log('commitReturn: matches',before.matches,'→',s.matches.length);
s.log.slice(before.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,115)));
const rq2=s.artifacts.find(a=>a.kind==='central-request');
console.log('request state after return:', rq2.data.state,'| RPL section:', JSON.stringify(rq2.data.sections.find(x=>x.code==='RPL')));
