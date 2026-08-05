const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit351/app-v3.5.1-decoded.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console:{log(){},warn(){},error(){}}, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}}, HTMLAnchorElement:function(){} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});

console.log('=== A. BOOT / SEEDS / SPOTS (regression) ===');
console.log('matches:',s.matches.length,'| identities:',s.identities.length,'| reachable:',PR.ui.filterTeams(s,'').length);
console.log('seed logs:',s.log.filter(l=>l.type==='system'&&l.action==='seed').length,'| ownerApproved mutes:',s.mutes.filter(m=>m.ownerApproved===true).length);
console.log('R1 krasnodar:',JSON.stringify(PR.ui.filterTeams(s,'krasnodar')),'| fakel:',JSON.stringify(PR.ui.filterTeams(s,'fakel')));
const r=PR.compute.selectFixture(s,derived,'CSKA Moscow','Krylia Sovetov Samara',{});
console.log('R4 path:',r.path.kind);

console.log('\n=== B. R10-D9 CONTRACT (verbatim auditor repro) ===');
PR.ui.newCentralRequest(s,derived,'2026-08-02');
let rq=s.artifacts.find(a=>a.kind==='central-request');
console.log('sections:',rq.data.sections.length,'| state:',rq.data.state,'| RPL:',rq.data.sections.find(x=>x.code==='RPL').state);
const other=rq.data.sections.find(x=>x.code!=='RPL');
const retText='BP-TEAM-PACK v2\nMATCH|2026-08-02|Russian Premier League|domestic-league|FC Krasnodar|2|0|Akron Tolyatti|normal|unknown|Krasnodar|Russia||src-ret1\nSOURCE|src-ret1|https://example.com/r1|2026-08-02|results-database|simulated\nEND\n';
const PRr=PR.requests.parseReturn(s,retText,'2026-08-02');
console.log('parseReturn: ok='+PRr.ok,'| codes:',JSON.stringify(PRr.blocks[0].codes),'(contract: ["RPL"])');
const b1={log:s.log.length,matches:s.matches.length,arts:s.artifacts.length};
PR.ui.commitReturn(s,derived,{ name:'central-request-20260802-r1.txt', isReturn:true, returnBlocks:PRr.blocks, requestDate:'2026-08-02', matched:!!PR.requests.openRequest(s) });
console.log('commitReturn: matches',b1.matches,'→',s.matches.length,'(contract 1436→1437) | logDelta:',s.log.length-b1.log);
s.log.slice(b1.log).forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,110)));
rq=s.artifacts.find(a=>a.kind==='central-request');
console.log('D9: RPL section =',rq.data.sections.find(x=>x.code==='RPL').state,'(contract partial) |',other.code,'section =',rq.data.sections.find(x=>x.code===other.code).state,'(contract requested) | overall =',rq.data.state,'(contract partial)');

console.log('\n=== C. R10-D10 CONTRACT (verbatim auditor repro — second identical return) ===');
const rqBefore=s.artifacts.find(a=>a.kind==='central-request');
const stateBefore=JSON.stringify(rqBefore.data)+'|'+s.artifacts.length;
const PRr2=PR.requests.parseReturn(s,retText,'2026-08-02');
const b2={log:s.log.length,matches:s.matches.length,arts:s.artifacts.length};
PR.ui.commitReturn(s,derived,{ name:'central-request-20260802-r1-DUP.txt', isReturn:true, returnBlocks:PRr2.blocks, requestDate:'2026-08-02', matched:!!PR.requests.openRequest(s) });
const logDelta=s.log.slice(b2.log);
console.log('commitReturn(dup): matches',b2.matches,'→',s.matches.length,'(contract +0) | logDelta:',logDelta.length,'(contract 1)');
logDelta.forEach(l=>console.log('  log+:',l.type+'/'+l.action,'|',String(l.summary).slice(0,110)));
const rqAfter=s.artifacts.find(a=>a.kind==='central-request');
const stateAfter=JSON.stringify(rqAfter.data)+'|'+s.artifacts.length;
const d10pass = s.matches.length===b2.matches
  && logDelta.length===1 && logDelta[0].action==='return-commit-skip'
  && !logDelta.some(l=>l.action==='return-commit') && !logDelta.some(l=>l.action==='post-return')
  && stateBefore===stateAfter;
console.log('D10: request state+artifacts untouched?',stateBefore===stateAfter,'| overall still',rqAfter.data.state,'| VERDICT',d10pass?'PASS':'FAIL');

console.log('\n=== D. REGRESSIONS: their R9 fixes still hold ===');
const pack='BP-TEAM-PACK v2\nTEAM|Testington FC|England|Test League|TST||unknown|Testville|England|unknown|unknown|unknown|unknown\nTEAM|Rustown United|England|Test League|TST||unknown|Rustown|England|unknown|unknown|unknown|unknown\nMATCH|2026-07-30|Test League|domestic-league|Testington FC|1|0|Rustown United|normal|unknown|Testville|England||src-t1\nSOURCE|src-t1|https://example.com/t|2026-08-02|results-database|synthetic pin\nEND\n';
const v1=PR.ingest.validate(s,PR.ingest.parsePack(pack),'2026-08-02',{strict:true});
const r1=PR.ingest.commit(s,v1.staged,{packName:'t1',ownerApproved:true});
const bl=s.log.length;
const v2=PR.ingest.validate(s,PR.ingest.parsePack(pack),'2026-08-02',{strict:true});
const r2=PR.ingest.commit(s,v2.staged,{packName:'t1-again',ownerApproved:true});
console.log('ingest D10 (no silentLog): 1st committed='+r1.committed,'2nd committed='+r2.committed,'| 2nd logDelta:',s.log.length-bl,'=',JSON.stringify(s.log.slice(bl).map(l=>l.action)));
const syn=PR.store.empty(); syn.meta.createdAt=new Date().toISOString();
const rows=['BP-TEAM-PACK v2','TEAM|Alpha Wanderers|Testland|Synthetic League|SLG||unknown|Alphaville|Testland|unknown|unknown|unknown|unknown','TEAM|Beta Rovers|Testland|Synthetic League|SLG||unknown|Betatown|Testland|unknown|unknown|unknown|unknown'];
for(let i=1;i<=30;i++){ const d=new Date(2026,0,i).toISOString().slice(0,10); rows.push('MATCH|'+d+'|Synthetic League|domestic-league|Alpha Wanderers|0|'+(1+(i%3))+'|Beta Rovers|normal|unknown|Alphaville|Testland||src-syn'); }
rows.push('SOURCE|src-syn|https://example.com/syn|2026-08-02|results-database|synthetic D9 pin'); rows.push('END\n');
const sv=PR.ingest.validate(syn,PR.ingest.parsePack(rows.join('\n')),'2026-08-02',{strict:true});
PR.ingest.commit(syn,sv.staged,{packName:'syn',seed:true});
const rep=PR.replay.run(syn,PR.derive.derive(syn,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]}));
console.log('replay D9: SLG hitRate =',rep.leagueWins&&rep.leagueWins['SLG']&&rep.leagueWins['SLG'].hitRate,'(contract 100)');
console.log('\nDONE');
