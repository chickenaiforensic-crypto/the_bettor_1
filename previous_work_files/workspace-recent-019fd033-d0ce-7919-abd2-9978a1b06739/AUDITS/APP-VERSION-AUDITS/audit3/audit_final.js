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
// GOLDEN-4 retry with store names
let r=PR.compute.selectFixture(s,derived,'Atlanta United FC','Austin FC',{});
console.log('GOLDEN-4 retry (Atlanta United FC v Austin FC): ok='+r.ok,'path='+r.path.kind,'label='+r.path.label);
const z=r.sections.find(x=>x.id==='zone');
if(z) console.log('  zone:', JSON.stringify(z.content.zone).slice(0,200));
console.log('  confidence:', JSON.stringify(r.confidence));
// alias/picker surface check: can a user typing "Atlanta United" resolve? try canon.resolveIdentity variants
console.log('resolve "Atlanta United":', !!PR.canon.resolveIdentity(s,'Atlanta United'), '| "atlanta united fc":', !!PR.canon.resolveIdentity(s,'atlanta united fc'), '| "Austin":', !!PR.canon.resolveIdentity(s,'Austin'));
// dated cache-mutation proof (row dated 2026-07-30 — before today, inside form window)
const d1=derived.storeHash;
const f1=r.sections.find(x=>x.id==='form');
const packText='BP-TEAM-PACK v2\nMATCH|2026-07-30|Audit League|other|FC Krasnodar|7|0|Fakel Voronezh|normal|unknown|Krasnodar|Russia||src-audit\nSOURCE|src-audit|https://example.com/audit|2026-08-02|other|audit cache proof row\nEND\n';
const parsed=PR.ingest.parsePack(packText);
const v=PR.ingest.validate(s,parsed,'2026-08-02',{strict:true});
console.log('\nCACHE-PROOF-2 (row dated 2026-07-30): validate ok='+v.ok);
PR.ingest.commit(s,v.staged,{packName:'audit-cache-proof-2',ownerApproved:true}); PR.store.save(s);
const d2=PR.derive.derive(s,{engines:[(st,dd)=>{dd.dcFit=PR.dc.fit(st);}]});
const r2=PR.compute.selectFixture(s,d2,'FC Krasnodar','Fakel Voronezh',{});
console.log('storeHash changed:', String(d1).slice(0,12),'→',String(d2.storeHash).slice(0,12));
const fz1=null; const z1=(r2.sections.find(x=>x.id==='zone')||{}).content;
const f2=r2.sections.find(x=>x.id==='form');
console.log('zone AFTER:', z1.zone? z1.zone.key+' '+z1.zone.tag : '(none)');
console.log('home form AFTER: n='+f2.content.home.n+' w='+f2.content.home.w+' first row '+f2.content.home.rows[0].dateISO+' (expect 07-30 injected row visible)');
// muted rows honored in graph?
console.log('mutes on store:', s.mutes.length, '| sample:', JSON.stringify(s.mutes[0]).slice(0,120));
// rendered vocab check
const appEl=els['app'];
console.log('\n== VOCAB on rendered #app innerHTML ==');
const H=appEl.innerHTML||'(render wrote nothing)';
console.log('render length:', H.length);
['hash','fingerprint','engine','graph rows','localStorage','JSON','store','raw JSON','backend','cache'].forEach(w=>{
  const re=new RegExp(w,'gi'); const cnt=(H.match(re)||[]).length; if(cnt) console.log('  BANNED-WORD hit:',w,'×'+cnt);
});
console.log('contains NO CALL string:', /NO CALL/.test(H));
fs.writeFileSync('audit3/render_initial.html', H);
console.log('\nDONE');
