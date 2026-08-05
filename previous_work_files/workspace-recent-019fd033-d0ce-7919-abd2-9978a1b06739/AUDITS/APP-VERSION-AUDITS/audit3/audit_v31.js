const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('app-v3.1.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
const nBlocks=(html.match(/<script>/g)||[]).length;
console.log('script blocks in verified file:', nBlocks);
for(let i=1;i<=nBlocks;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR;
if(sb.boot){ sb.boot(); } else { console.log('no boot exported; using manual'); }
const s=PR.store.load();
console.log('\n== STORE =='); ['identities','matches','venues','seasons','sources','mutes','log','artifacts','notes'].forEach(t=>console.log(' ',t.padEnd(11),(s[t]||[]).length));
console.log('== LOG ACTIONS =='); s.log.forEach(l=>console.log(' ',l.seq,l.type+'/'+l.action,'|',String(l.summary).slice(0,95)));
console.log('ownerApproved:true in log?', /ownerApproved/.test(JSON.stringify(s.log)));
console.log('mute reasons:', s.mutes.map(m=>m.reason).join(' || '));
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ if(PR.dc&&PR.dc.fit) d.dcFit=PR.dc.fit(st); }]});
// identity categories
function cat(t){ const src=(t.source||t.origin||'').toString()+(t.id||''); if(/model|rated|fitted/i.test(src) || t.modelRated || t.rated) return 'rated'; if(t.declared || (t.fromPack)) return 'declared'; return 'other'; }
const cats={}; s.identities.forEach(t=>cats[cat(t)]=(cats[cat(t)]||0)+1);
console.log('identity categories (best-effort):', JSON.stringify(cats));
// sample rated-looking
const rated=s.identities.filter(t=>/model|rated|fitted/i.test(JSON.stringify(t).slice(0,400))).length;
console.log('rated-flagged identities (loose):', rated);
function probe(h,a,label){
  const r=PR.compute.selectFixture(s,derived,h,a,{});
  console.log('\n==',label,'==');
  console.log(' ok:',r.ok,'| path:',r.path.kind,'|',r.path.label);
  console.log(' sections:',(r.sections||[]).map(x=>x.id).join(', '));
  const out=(r.sections||[]).find(x=>x.id==='probabilities'||x.id==='outlook');
  if(out) console.log(' HDA:',[out.content.H,out.content.D,out.content.A].map(x=>x!=null?Number(x).toFixed(3):'-').join('/'));
  const zn=(r.sections||[]).find(x=>x.id==='zone');
  if(zn&&zn.content.zone) console.log(' zone:',zn.content.zone.tag);
  const pt=(r.sections||[]).find(x=>x.id==='paths');
  if(pt){ (pt.content.secs||[]).forEach(sec=>{ console.log('  ',sec.name+':','h'+sec.hW+' d'+sec.dW+' a'+sec.aW,'W='+sec.W,'lead='+sec.lead, sec.records? '| REC: '+sec.records.slice(0,120) : '| (no records field)'); }); }
  console.log(' confidence:', JSON.stringify(r.confidence));
  console.log(' provenance:', JSON.stringify(r.provenance).slice(0,260));
  (r.honesty&&r.honesty.refusals||[]).forEach(x=>console.log(' REFUSAL:',x));
  (r.honesty&&r.honesty.notes||[]).forEach(x=>console.log(' note:',String(x).slice(0,170)));
  return r;
}
probe('CSKA Moscow','Krylia Sovetov Samara','R4 CSKA v Krylia (expect fitted-online 59.1/23.9/17.0)');
probe('FC Krasnodar','Fakel Voronezh','Krasnodar v Fakel (RPL now fitted?)');
probe('Hibernian','Malisheva','Hibernian v Malisheva (evidence-cross + R3 records)');
probe('Malisheva','Drita','Malisheva v Drita (R3 records example)');
probe('Atlanta United FC','Austin FC','MLS honesty');
probe('Celtic','Rangers','legacy fitted (SC0)');
// R1 search
console.log('\n== SEARCH ==  ');
const ctx=Object.assign(Object.create(null),sb);
let found=[];
try{ found= (PR.ui&&PR.ui.searchTeams)? PR.ui.searchTeams(s, 'krasnodar') : (PR.canon.search? PR.canon.search(s,'krasnodar'):null); }catch(e){ found='ERR '+e.message; }
console.log(' search "krasnodar":', JSON.stringify(found).slice(0,200));
