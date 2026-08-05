const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit35/app-v3.5-decoded.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){ return this._a?this._a:null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console:{log(){},warn(){},error(){}}, navigator:{}, addEventListener(){}, location:{href:''},
 URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}}, HTMLAnchorElement:function(){} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();

console.log('=== A. BOOT / COUNTS / SEEDS ===');
const idents=s.identities.length;
const reachable=PR.ui.filterTeams(s,'').length;
console.log('matches:',s.matches.length,'| identities:',idents,'| picker-reachable:',reachable,'| ghosts(flags):',(s.flags||[]).length);
const seedLogs=s.log.filter(l=>l.type==='system'&&l.action==='seed').length;
const ownerApprovedMutes=s.mutes.filter(m=>m.ownerApproved===true).length;
console.log('seed logs (system/seed):',seedLogs,'| seed mutes w/ ownerApproved===true:',ownerApprovedMutes,'| mute reasons sample:',JSON.stringify((s.mutes[0]||{}).reason));

console.log('\n=== B. R1 picker + R4 gate re-probe ===');
console.log('search "krasnodar":',JSON.stringify(PR.ui.filterTeams(s,'krasnodar')));
console.log('search "fakel":',JSON.stringify(PR.ui.filterTeams(s,'fakel')));
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
const r=PR.compute.selectFixture(s,derived,'CSKA Moscow','Krylia Sovetov Samara',{});
console.log('R4/R7 spot:',r.path.kind,'| fitted provenance:',(r.sections.find(x=>x.id==='fit')||{}).content ? 'fit section present' : '(no fit section)');
const fitSec=r.sections.find(x=>x.id==='fit'||x.id==='fitted');
if(fitSec) console.log('  fit content keys:',Object.keys(fitSec.content||{}).slice(0,10).join(','));

console.log('\n=== C. MY D9 REPRO — routine return, EXISTING teams only → section must flip ===');
PR.ui.newCentralRequest(s,derived,'2026-08-02');
const rqArt=s.artifacts.find(a=>a.kind==='central-request');
console.log('open request: state='+rqArt.data.state,'sections='+rqArt.data.sections.length,'| RPL section:',JSON.stringify(rqArt.data.sections.find(x=>x.code==='RPL')));
const retText='BP-TEAM-PACK v2\nSECTION|Russian Premier League|RPL\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated\nEND\n';
const PRr=PR.requests.parseReturn(s,retText,'2026-08-02');
console.log('parseReturn: ok='+PRr.ok,'blocks:',JSON.stringify(PRr.blocks.map(b=>({ok:b.ok,matches:b.matches,codes:b.codes}))));
const open=PR.requests.openRequest(s);
const f={ name:'central-request-20260802-r1.txt', isReturn:true, returnBlocks:PRr.blocks, requestDate:'2026-08-02', matched:!!open };
const before={log:s.log.length,matches:s.matches.length};
PR.ui.commitReturn(s,derived,f);
console.log('commitReturn: matches',before.matches,'→',s.matches.length,'(+1 expected)');
s.log.slice(before.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,115)));
const rq2=s.artifacts.find(a=>a.kind==='central-request');
const sec=rq2.data.sections.find(x=>x.code==='RPL');
console.log('VERDICT D9-mine: RPL section state =',sec&&sec.state,'(PASS if "partial") | overall =',rq2.data.state,'| codes seen in log:',/RPL/.test(JSON.stringify(s.log.slice(before.log))));

console.log('\n=== D. MY D10 REPRO — all-duplicate return → must NOT log return-commit/post-return ===');
const PRr2=PR.requests.parseReturn(s,retText,'2026-08-02');
const openB=PR.requests.openRequest(s);
const f2={ name:'central-request-20260802-r1-DUP.txt', isReturn:true, returnBlocks:PRr2.blocks, requestDate:'2026-08-02', matched:!!openB };
const b2={log:s.log.length,matches:s.matches.length,arts:s.artifacts.length};
PR.ui.commitReturn(s,derived,f2);
console.log('commitReturn(dup): matches',b2.matches,'→',s.matches.length,'(+0 expected)');
s.log.slice(b2.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,115)));
const badCommit=s.log.slice(b2.log).some(l=>l.action==='return-commit');
const badStamp=s.log.slice(b2.log).some(l=>l.action==='post-return');
console.log('VERDICT D10-mine: return-commit logged?',badCommit,'| post-return stamped?',badStamp,'(PASS if BOTH false)');

console.log('\n=== E. THEIR D10 — duplicate pack commit → commit-skip, committed:false ===');
PR.store.save(s);
const pack='BP-TEAM-PACK v2\nTEAM|Testington FC|England|Test League|TST||unknown|Testville|England|unknown|unknown|unknown|unknown\nTEAM|Rustown United|England|Test League|TST||unknown|Rustown|England|unknown|unknown|unknown|unknown\nMATCH|2026-07-30|Test League|domestic-league|Testington FC|1|0|Rustown United|normal|unknown|Testville|England||src-t1\nSOURCE|src-t1|https://example.com/t|2026-08-02|results-database|synthetic pin\nEND\n';
const parsed=PR.ingest.parsePack(pack);
const v1=PR.ingest.validate(s,parsed,'2026-08-02',{strict:true});
const r1=PR.ingest.commit(s,v1.staged,{packName:'t1',ownerApproved:true});
console.log('first commit: ok='+r1.ok,'committed='+r1.committed,'matches='+r1.report.matches);
const v2=PR.ingest.validate(s,PR.ingest.parsePack(pack),'2026-08-02',{strict:true});
const blog=s.log.length;
const r2=PR.ingest.commit(s,v2.staged,{packName:'t1-again',ownerApproved:true});
console.log('second commit: ok='+r2.ok,'committed='+r2.committed,'matches='+r2.report.matches);
s.log.slice(blog).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,110)));
console.log('VERDICT their-D10: committed===false?',r2.committed===false,'| commit-skip logged?',s.log.slice(blog).some(l=>l.action==='commit-skip'),'| no "Pack committed: 0"?',!s.log.slice(blog).some(l=>/Pack committed: 0/.test(l.summary)));

console.log('\n=== F. THEIR D9 — replay TB-led league hitRate ===');
const syn=PR.store.empty();
syn.meta.createdAt=new Date().toISOString();
const synPackRows=['BP-TEAM-PACK v2',
'TEAM|Alpha Wanderers|Testland|Synthetic League|SLG||unknown|Alphaville|Testland|unknown|unknown|unknown|unknown',
'TEAM|Beta Rovers|Testland|Synthetic League|SLG||unknown|Betatown|Testland|unknown|unknown|unknown|unknown'];
for(let i=1;i<=30;i++){ const d=new Date(2026,0,i).toISOString().slice(0,10); synPackRows.push('MATCH|'+d+'|Synthetic League|domestic-league|Alpha Wanderers|0|'+(1+(i%3))+'|Beta Rovers|normal|unknown|Alphaville|Testland||src-syn'); }
synPackRows.push('SOURCE|src-syn|https://example.com/syn|2026-08-02|results-database|synthetic D9 pin'); synPackRows.push('END\n');
const sp=PR.ingest.parsePack(synPackRows.join('\n'));
const sv=PR.ingest.validate(syn,sp,'2026-08-02',{strict:true});
if(!sv.ok){ console.log('synthetic pack validation failed:',JSON.stringify(sv.errors&&sv.errors.slice(0,3))); }
else{
  PR.ingest.commit(syn,sv.staged,{packName:'syn',seed:true});
  const sd=PR.derive.derive(syn,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
  const rep=PR.replay.run(syn,sd);
  console.log('replay n:',rep.n,'| leagueWins:',JSON.stringify(rep.leagueWins));
  const lw=rep.leagueWins&&rep.leagueWins['SLG'];
  console.log('VERDICT their-D9: SLG hitRate =',lw&&lw.hitRate,'(PASS if 100; pre-fix ≈0)');
}
console.log('\nDONE');
