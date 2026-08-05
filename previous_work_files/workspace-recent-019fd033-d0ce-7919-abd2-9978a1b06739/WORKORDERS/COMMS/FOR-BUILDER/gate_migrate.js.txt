const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit351/app-v3.5.1-decoded.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console:{log(){},warn(){},error(){}}, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}}, HTMLAnchorElement:function(){} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR;

console.log('=== M1 PROOF — owner drops the .json into the Data tab ===');
const fileText=fs.readFileSync('/home/user/uploads/pitch-rating-full-data-2026-08-02.json','utf8');
const parsed=PR.ingest.parsePack(fileText);
console.log('parsePack(json) → valid:',parsed.valid,'(false = the UI stages it as "Not a pack file" — intake gap)');

console.log('\n=== MIGRATION GATE — STORE.deserialize on the real export ===');
const R=PR.store.deserialize(fileText);
console.log('ok:',R.ok, R.error||'');
const rep=R.report, s=R.store;
console.log('report:',JSON.stringify({rowsIn:rep.rowsIn,rowsOut:rep.rowsOut,identitiesMerged:rep.identitiesMerged,mutesPreserved:rep.mutesPreserved,unmapped:rep.unmapped,notes:rep.notes}));
console.log('migrated store: matches',s.matches.length,'| identities',s.identities.length,'| venues',s.venues.length,'| sources',s.sources.length,'| mutes',s.mutes.length,'| seasons',s.seasons.length,'| log',s.log.length);
console.log('migration log line:',JSON.stringify(s.log.find(l=>l.action==='migration')));

console.log('\n=== RECONCILIATION vs source (no-abolition audit) ===');
const src=JSON.parse(fileText);
const srcIdKeys=Object.keys(src.identities);
console.log('identities:',srcIdKeys.length,'in →',s.identities.length,'out', srcIdKeys.length===s.identities.length?'✓ ALL CARRIED':'✗ DELTA '+(s.identities.length-srcIdKeys.length));
console.log('matches:',src.matches.length,'in →',s.matches.length,'out', src.matches.length===s.matches.length?'✓ ALL CARRIED':'✗ DELTA '+(s.matches.length-src.matches.length));
console.log('venues:',Object.keys(src.venues).length,'in →',s.venues.length,'out');
console.log('sources:',src.sources.length,'in →',s.sources.length,'out');
// per-row spot integrity: 3 sampled matches fully equal after mapping?
let bad=0, checked=0;
const byId={}; s.matches.forEach(m=>byId[m.id]=m);
src.matches.forEach(m=>{ const d=byId[m.id]; if(!d){bad++;return;} checked++;
  const hn=(src.identities[m.homeId]||{}).name, an=(src.identities[m.awayId]||{}).name;
  if(d.homeName!==hn||d.awayName!==an||d.homeGoals!==m.hg||d.awayGoals!==m.ag||d.dateISO!==m.date||d.competitionName!==m.competition) bad++; });
console.log('match row integrity: '+checked+' resolvable, '+bad+' mismatched (name/score/date/comp)');
// sourceId loss
const lostSrc=s.matches.filter(m=>!m.sourceId).length;
console.log('M2: migrated matches with NULL sourceId:',lostSrc,'/',s.matches.length,'(source key was "source" — mapper reads only "sourceId")');
const lostISrc=s.identities.filter(t=>!(t.sourceIds&&t.sourceIds.length)).length;
console.log('M3: migrated identities with empty sourceIds:',lostISrc,'/',s.identities.length,'(key was "source")');
const multi=s.identities.filter(t=>{const o=src.identities[t.id]; return o&&Array.isArray(o.leagues)&&o.leagues.length>1;});
const multiLost=multi.filter(t=>!t.leagueCode).length;
console.log('M3b: multi-league identities:',multi.length,'| of those leagueCode=null:',multiLost);
// alias coverage: identity aliases carried?
const aliasCarried=s.identities.reduce((n,t)=>n+(t.aliases?t.aliases.length:0),0);
console.log('identity-level aliases carried:',aliasCarried,'| top-level aliases map entries:',Object.keys(src.aliases).length,'(unmapped — derivable)');

console.log('\n=== BOOT-CHECKS on the migrated store ===');
console.log('picker reachable:',PR.ui.filterTeams(s,'').length);
console.log('search krasnodar:',JSON.stringify(PR.ui.filterTeams(s,'krasnodar')),'| hibernian:',JSON.stringify(PR.ui.filterTeams(s,'hibernian')));
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
try{
  const r=PR.compute.selectFixture(s,derived,'CSKA Moscow','Krylia Sovetov Samara',{});
  console.log('CSKA-Krylia path:',r.path.kind);
}catch(e){ console.log('CSKA-Krylia THREW:',e.message); }
try{
  const r2=PR.compute.selectFixture(s,derived,'Hibernian','Malisheva',{});
  const prob=r2.sections.find(x=>x.id==='probabilities');
  console.log('Hibernian-Malisheva path:',r2.path.kind,'| H/D/A:',prob?[prob.content.H,prob.content.D,prob.content.A].map(x=>Number(x).toFixed(3)).join('/'):'?');
}catch(e){ console.log('Hibernian probe THREW:',e.message); }
try{
  const req=PR.requests.createCentralRequest(s,derived,'2026-08-02');
  const teamLines=req.requestText.split('\n').filter(l=>l.startsWith('team|'));
  console.log('central request builds: sections',req.sections.length,'| team lines',teamLines.length);
}catch(e){ console.log('request THREW:',e.message); }
console.log('\nDONE');
