const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit352/app-v3.5.2-decoded.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
let approveBtns=[];
function makeEl(){ const el={innerHTML:'',textContent:'',value:'',files:null,style:{},dataset:{},
 classList:{add(){},remove(){},toggle(){},contains(){return false}},
 addEventListener(t,fn){ (this._ls=this._ls||{})[t]=fn; },
 querySelectorAll(sel){ if(sel==='[data-approve]'){ const b=makeEl(); b.getAttribute=()=> '0'; approveBtns.push(b); return [b]; } return []; },
 querySelector(){return makeEl()}, appendChild(){}, remove(){}, setAttribute(){}, getAttribute(){return null}, click(){}, focus(){}};
 return el; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
class FileReaderStub{ readAsText(f){ this.result=f.text; if(this.onload) this.onload(); } }
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console:{log(){},warn(){},error(){}}, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}}, HTMLAnchorElement:function(){}, FileReader:FileReaderStub };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR;
function latestBtn(){ return approveBtns[approveBtns.length-1]; }
function stagedText(){ return Object.values(els).map(e=>e.innerHTML||'').join('\n'); }

console.log('=== A. FRESH BOOT REGRESSION (seeds side) ===');
sb.boot();
const s0=PR.store.load();
console.log('seeds:',s0.matches.length,'matches |',s0.identities.length,'ids | reachable:',PR.ui.filterTeams(s0,'').length,'| krasnodar:',JSON.stringify(PR.ui.filterTeams(s0,'krasnodar')));
const d0=PR.derive.derive(s0,{engines:[(st,d)=>{d.dcFit=PR.dc.fit(st)}]});
console.log('seed CSKA path:',PR.compute.selectFixture(s0,d0,'CSKA Moscow','Krylia Sovetov Samara',{}).path.kind);

console.log('\n=== B. M1 — OWNER DROP-IN SIMULATION (real export through the file input) ===');
const fi=els['file-input'];
if(!fi||!fi._ls||!fi._ls.change){ console.log('FATAL: file-input change listener not wired'); process.exit(1); }
fi.files=[{name:'pitch-rating-full-data-2026-08-02.json', text:fs.readFileSync('/home/user/uploads/pitch-rating-full-data-2026-08-02.json','utf8')}];
approveBtns.length=0;
fi._ls.change();
console.log('migration card staged:', /Store migration — 1432 matches · 792 teams · 86 venues · 215 sources · REPLACES the current store/.test(stagedText()), '| old "Rejected — 38877" trap gone:', !/Rejected — 38877/.test(stagedText()), '| approve button offered:', !!latestBtn()&&!!(latestBtn()._ls&&latestBtn()._ls.click));

console.log('\n=== C. APPROVE — one click → real migration commit ===');
const b=latestBtn(); if(b&&b._ls&&b._ls.click) b._ls.click(); else console.log('FATAL: no approve listener');
const s1=PR.store.load();
console.log('store after approve: matches',s1.matches.length,'| identities',s1.identities.length,'| venues',s1.venues.length,'| sources',s1.sources.length);
console.log('log tail:',JSON.stringify(s1.log.slice(-3).map(l=>l.type+'/'+l.action)));
console.log('artifacts:',s1.artifacts.map(a=>a.kind).join(','));
console.log('M2: matches with null sourceId:',s1.matches.filter(m=>!m.sourceId).length,'(pin 0) | M3: identities with empty sourceIds:',s1.identities.filter(t=>!(t.sourceIds&&t.sourceIds.length)).length,'(pin 0)');
const d1=PR.derive.derive(s1,{engines:[(st,d)=>{d.dcFit=PR.dc.fit(st)}]});
const r=PR.compute.selectFixture(s1,d1,'CSKA Moscow','Krylia Sovetov Samara',{});
const ga=s1.artifacts.find(a=>a.kind==='dc-gate-validation');
console.log('CSKA migrated path:',r.path.kind,'| gate keys:',ga?Object.keys(ga.data).join(','):'NONE');
// row-integrity on the POST-APPROVE persisted store (contract: all 1,432 identical)
const src=JSON.parse(fs.readFileSync('/home/user/uploads/pitch-rating-full-data-2026-08-02.json','utf8'));
const byId={}; s1.matches.forEach(m=>byId[m.id]=m);
let bad=0,res=0; src.matches.forEach(m=>{ const d=byId[m.id]; if(!d)return; res++;
 if(d.homeGoals!==m.hg||d.awayGoals!==m.ag||d.dateISO!==m.date||d.competitionName!==m.competition) bad++; });
console.log('row integrity post-approve:',res+'/'+src.matches.length,'resolvable,',bad,'mismatched (pin 0)');

console.log('\n=== D. SOUTHAMPTON PACK THROUGH THE SAME DOOR ===');
const before=s1.matches.length;
fi.files=[{name:'Southampton_BP-TEAM-PACK_v2.txt', text:fs.readFileSync('audit352/southampton-pack.txt','utf8')}];
approveBtns.length=0;
fi._ls.change();
const card=/(\d+) matches · (\d+) teams · (\d+) season rows/.exec(stagedText());
console.log('pack staged card:',card?card[0]:'(not found)');
const b2=latestBtn(); if(b2&&b2._ls&&b2._ls.click) b2._ls.click();
const s2=PR.store.load();
console.log('matches',before,'→',s2.matches.length,'(+15 expected)','| tail:',JSON.stringify(s2.log.slice(-1).map(l=>l.type+'/'+l.action)));

console.log('\n=== E. M3b PIN — null-code multi-league identities still count for gate seasons ===');
const syn=PR.store.empty(); syn.meta.createdAt=new Date().toISOString();
const rows=['BP-TEAM-PACK v2','TEAM|Gamma City|Testland|Synthetic League|SLG||unknown|Gamma|Testland|unknown|unknown|unknown|unknown','TEAM|Delta Town|Testland|Synthetic League|SLG||unknown|Delta|Testland|unknown|unknown|unknown|unknown'];
for(let i=1;i<=20;i++){ const d=new Date(2024,6,i).toISOString().slice(0,10); rows.push('MATCH|'+d+'|Synthetic League|domestic-league|Gamma City|1|0|Delta Town|normal|unknown|Gamma|Testland||src-g1'); }
for(let i=1;i<=20;i++){ const d=new Date(2025,6,i).toISOString().slice(0,10); rows.push('MATCH|'+d+'|Synthetic League|domestic-league|Delta Town|0|1|Gamma City|normal|unknown|Delta|Testland||src-g1'); }
rows.push('SOURCE|src-g1|https://example.com|2026-08-02|results-database|syn'); rows.push('END\n');
const sv=PR.ingest.validate(syn,PR.ingest.parsePack(rows.join('\n')),'2026-08-02',{strict:true});
PR.ingest.commit(syn,sv.staged,{packName:'syn',seed:true});
syn.identities.forEach(t=>{ t.leagueCode=null; });   // simulate legacy multi-league arrivals
const g=PR.dc.d3Gate(syn,{code:'SLG',key:PR.canon.canon('Synthetic League'),name:'Synthetic League'});
console.log('d3Gate:',JSON.stringify(g),'(pin: seasons >= 2 via competition-name fallback)');
console.log('\nDONE');
