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
// CORRECT call: (store, derived, dateString)
const out=PR.requests.renderRequestText(s,derived,'2026-08-02');
const txt=out.text||out;
console.log('output shape:', typeof out==='string'?'string':('object keys '+Object.keys(out).join(',')));
fs.writeFileSync('audit34/central-request-sample.txt',txt);
console.log('header block:');
txt.split('\n').slice(0,6).forEach(l=>console.log('  ',l));
console.log('SECTIONs:',(txt.match(/^SECTION\|/gm)||[]).length,'| excluded:',(txt.match(/^excluded\|/gim)||[]).length,'| ends END:',/\nEND\s*$/.test(txt));
const teams=[...txt.matchAll(/^team\|([^|]+)\|([^|]+)\|/gm)];
let ok=0,bad=[],placeholders=0;
for(const t of teams){ const nm=t[1],claimed=t[2];
  if(/^\(all /.test(nm)){ placeholders++; continue }
  const id=s.identities.find(x=>x.name===nm); if(!id){bad.push(nm+':NO-ID');continue}
  const ms=s.matches.filter(m=>m.homeId===id.id||m.awayId===id.id).map(m=>m.dateISO).sort(); const last=ms[ms.length-1];
  if(last===claimed||(ms.length===0&&claimed==='none')) ok++; else bad.push(nm+': '+claimed+' vs '+last); }
console.log('real team lines:',ok,'EXACT of',teams.length-placeholders,'(placeholders:',placeholders,')', bad.length?('| MISMATCHES: '+bad.slice(0,5).join(' ; ')):'');
// return flow
const retPack='BP-TEAM-PACK v2\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated return row for R8 acceptance\nEND\n';
const v=PR.ingest.validate(s,PR.ingest.parsePack(retPack),'2026-08-02',{strict:true});
console.log('\nreturn validate ok:',v.ok);
const before={log:s.log.length,matches:s.matches.length,arts:s.artifacts.length};
PR.ui.commitReturn(s,derived,{name:'central-request-20260802-r1.txt',payload:v.staged,isReturn:true});
console.log('commitReturn: log',before.log,'→',s.log.length,'| matches',before.matches,'→',s.matches.length,'| artifacts',before.arts,'→',s.artifacts.length);
s.log.slice(before.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,120)));
const snaps=s.artifacts.filter(a=>/snapshot/i.test(a.kind||''));
console.log('snapshot artifacts:',snaps.length, snaps.map(x=>x.kind).slice(-2).join(', '));
