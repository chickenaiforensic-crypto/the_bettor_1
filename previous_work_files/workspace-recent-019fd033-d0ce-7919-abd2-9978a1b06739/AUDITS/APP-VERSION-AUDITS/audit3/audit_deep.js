const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('uploads/app-v3.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
vm.runInContext(block(1),sb); vm.runInContext(block(2),sb); vm.runInContext(block(3),sb);
const PR=sb.PR; sb.boot();
const s=PR.store.load();
const derived=PR.derive.derive(s,{engines:[(st,d)=>{d.dcFit=PR.dc.fit(st);}]});
// 1) duplicate leagues
console.log('== LEAGUE REGISTRY ROWS ==');
(derived.leagues||[]).forEach(l=>{
  if(typeof l==='string') return;
  const nm=l.name||l.leagueName, cd=l.code||l.leagueCode||'';
  console.log((cd||'--').padEnd(4), String(nm).padEnd(28), 'teams:', l.teams?l.teams.length:(l.count!=null?l.count:'?'));
});
// 2) MLS identities
console.log('\n== MLS-ish identities ==');
s.identities.filter(t=>/mls|major league/i.test(t.leagueName||'')).slice(0,8).forEach(t=>console.log(' ', t.name, '| canon:', t.canonName, '| aliases:', JSON.stringify((t.aliases||[]).slice(0,3))));
// 3) GOLDEN-1 full raw sections
const r=PR.compute.selectFixture(s,derived,'FC Krasnodar','Fakel Voronezh',{});
console.log('\n== GOLDEN-1 raw section contents ==');
r.sections.forEach(sec=>console.log('--', sec.id, JSON.stringify(sec.content).slice(0,400)));
// 4) cache proof
console.log('\n== CACHE PROOF ==');
const h1=derived.storeHash;
const zone1=r.confidence.zone?r.confidence.zone.tag:null;
const packText='BP-TEAM-PACK v2\nMATCH|2026-08-02|Audit League|other|FC Krasnodar|7|0|Fakel Voronezh|normal|unknown|Krasnodar|Russia||src-audit\nSOURCE|src-audit|https://example.com/audit|2026-08-02|other|audit cache proof row\nEND\n';
const parsed=PR.ingest.parsePack(packText);
const v=PR.ingest.validate(s,parsed,'2026-08-02',{strict:true});
console.log('validate ok:', v.ok, v.ok?'':JSON.stringify(v.errors).slice(0,200));
if(v.ok){ PR.ingest.commit(s,v.staged,{packName:'audit-cache-proof',ownerApproved:true}); PR.store.save(s);
  const d2=PR.derive.derive(s,{engines:[(st,d)=>{d.dcFit=PR.dc.fit(st);}]});
  const r2=PR.compute.selectFixture(s,d2,'FC Krasnodar','Fakel Voronezh',{});
  console.log('storeHash before/after:', String(h1).slice(0,12),'→',String(d2.storeHash).slice(0,12),'| changed:', String(h1)!==String(d2.storeHash));
  console.log('zone before:', zone1);
  console.log('zone after :', r2.confidence.zone? r2.confidence.zone.tag : '(none)');
  const formAfter=(r2.sections.find(x=>x.id==='form')||{}).content;
  console.log('home form after: n='+formAfter.home.n+' w='+formAfter.home.w+' (expect n=7,w+1 if cache invalidated)');
}
console.log('\nDONE');
