const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit34/app-v3.4.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p,o){this.p=p;this.o=o}} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR; sb.boot&&sb.boot();
const s=PR.store.load();
console.log('== STORE ==', 'matches',s.matches.length,'identities',s.identities.length,'mutes',s.mutes.length,'log',s.log.length,'artifacts',s.artifacts.length);
console.log('== R6a MUTE REASONS =='); s.mutes.forEach(m=>console.log('  ', m.reason, '| src:', m.sourceId));
console.log('== log actions ==', s.log.map(l=>l.type+'/'+l.action).join(' | '));
const derived=PR.derive.derive(s,{engines:[(st,d)=>{ d.dcFit=PR.dc.fit(st); }]});
// R7: fitted card carries graph details
const r=PR.compute.selectFixture(s,derived,'CSKA Moscow','Krylia Sovetov Samara',{});
console.log('\n== R4/R7 CSKA ==','path:',r.path.kind,'| sections:',r.sections.map(x=>x.id).join(','));
const out=r.sections.find(x=>x.id==='probabilities'); console.log('  HDA:',[out.content.H,out.content.D,out.content.A].map(Number.prototype.toFixed? x=>Number(x).toFixed(3):x).join('/'));
console.log('  graph section present:', !!r.sections.find(x=>/graph|h2h|evidence|paths/.test(x.id)), '| honesty notes:', (r.honesty.notes||[]).length);
// R8: central request build — verify header, dates
if(sb.PR.requests && PR.requests.buildRequest){
  const req=PR.requests.buildRequest(s,derived,'2026-08-02');
  const txt=(PR.requests.renderRequestText?PR.requests.renderRequestText(req):req.text)||'';
  fs.writeFileSync('audit34/central-request-sample.txt', txt);
  console.log('\n== R8 CENTRAL REQUEST ==','bytes:',txt.length);
  console.log('  header ok:', /^PITCH-RATING CENTRAL-REQUEST v1/.test(txt));
  console.log('  request-date line:', /^request-date\|2026-08-02/m.test(txt));
  console.log('  return-to line present:', /return-to\|/.test(txt));
  console.log('  SECTION count:', (txt.match(/^SECTION\|/gm)||[]).length);
  console.log('  excluded lines:', (txt.match(/^excluded\|/gim)||[]).length);
  const teams=[...txt.matchAll(/^team\|([^|]+)\|(\d{4}-\d{2}-\d{2})\|/gm)];
  console.log('  team lines:', teams.length);
  // spot-check 5 team last-game dates vs store
  let ok=0, bad=[];
  for(const t of teams.slice(0,5)){
    const nm=t[1], claimed=t[2];
    const id=s.identities.find(x=>x.name===nm); if(!id){bad.push(nm+':noid');continue}
    const ms=s.matches.filter(m=>m.homeId===id.id||m.awayId===id.id).map(m=>m.dateISO).sort();
    const last=ms[ms.length-1];
    if(last===claimed||(!last&&claimed==='none')) ok++; else bad.push(nm+' claimed '+claimed+' actual '+last);
  }
  console.log('  spot-check 5 team dates:', ok+'/5 exact', bad.length?('MISMATCH: '+bad.join(' ; ')):'');
}
console.log('\nDONE');
