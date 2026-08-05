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
// R8 build + correct render call
const R=PR.requests.buildRequest(s,derived,'2026-08-02');
console.log('buildRequest keys:', Object.keys(R).join(','));
const txt=PR.requests.renderRequestText(s,derived,R);
fs.writeFileSync('audit34/central-request-sample.txt',txt);
console.log('R8 file bytes:',txt.length,'| header ok:',/^PITCH-RATING CENTRAL-REQUEST v1/.test(txt));
console.log('request-date:',/^request-date\|2026-08-02/m.test(txt),'| snapshot line:',/^system-snapshot\|/m.test(txt),'| return-to:',/^return-to\|/m.test(txt));
console.log('SECTIONs:',(txt.match(/^SECTION\|/gm)||[]).length,'| excluded:',(txt.match(/^excluded\|/gim)||[]).length,'| END:',/\nEND\s*$/.test(txt));
const teams=[...txt.matchAll(/^team\|([^|]+)\|([^|]+)\|/gm)];
console.log('team lines:',teams.length);
let ok=0,bad=[];
for(const t of teams){ const nm=t[1],claimed=t[2]; const id=s.identities.find(x=>x.name===nm); if(!id){bad.push(nm+':noid');continue}
  const ms=s.matches.filter(m=>m.homeId===id.id||m.awayId===id.id).map(m=>m.dateISO).sort(); const last=ms[ms.length-1];
  if(last===claimed||(ms.length===0&&claimed==='none')) ok++; else if(ok+bad.length<6) bad.push(nm+': claimed '+claimed+' actual '+last); }
console.log('team-date verification: exact',ok,'of',teams.length, bad.length?('| sample mismatches: '+bad.slice(0,4).join(' ; ')):'| ALL EXACT');
// R8 return flow: one-approval commitReturn
const retPack='BP-TEAM-PACK v2\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated return row for R8 acceptance\nEND\n';
const parsed=PR.ingest.parsePack(retPack);
const v=PR.ingest.validate(s,parsed,'2026-08-02',{strict:true});
console.log('\nRETURN validate ok:',v.ok, v.ok?'':JSON.stringify(v.errors).slice(0,200));
if(v.ok){
  const before={log:s.log.length,matches:s.matches.length,arts:s.artifacts.length};
  PR.ui.commitReturn(s,derived,{name:'central-request-2026-08-02-r1.txt',payload:v.staged,isReturn:true});
  console.log('after commitReturn: log',before.log,'→',s.log.length,'| matches',before.matches,'→',s.matches.length,'| artifacts',before.arts,'→',s.artifacts.length);
  s.log.slice(before.log).forEach(l=>console.log('  new log:',l.type+'/'+l.action,'|',String(l.summary).slice(0,110)));
  const snaps=s.artifacts.filter(a=>/snapshot/i.test(a.kind||''));
  console.log('snapshot artifacts total:',snaps.length, snaps.length?('latest: '+snaps[snaps.length-1].kind):'');
}
console.log('\nDONE');
