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
const R=PR.requests.buildRequest(s,derived,'2026-08-02');
const out=PR.requests.renderRequestText(s,derived,R);
console.log('renderRequestText →', typeof out, out&&out.text?('keys: '+Object.keys(out).join(',')):'');
const txt=typeof out==='string'?out:out.text;
fs.writeFileSync('audit34/central-request-sample.txt',txt);
console.log('\n== CENTRAL REQUEST FILE ==');
console.log('bytes:',txt.length);
console.log('header:', JSON.stringify(txt.split('\n').slice(0,6)));
console.log('SECTION lines:',(txt.match(/^SECTION\|/gm)||[]).length,'| excluded:',(txt.match(/^excluded\|/gim)||[]).length);
console.log('first SECTION:', (txt.match(/^SECTION\|.*/m)||['none'])[0].slice(0,120));
const teams=[...txt.matchAll(/^team\|([^|]+)\|([^|]+)\|/gm)];
console.log('team lines:',teams.length);
let ok=0,bad=[];
for(const t of teams){ const nm=t[1],claimed=t[2]; const id=s.identities.find(x=>x.name===nm); if(!id){bad.push(nm+':NO-ID');continue}
  const ms=s.matches.filter(m=>m.homeId===id.id||m.awayId===id.id).map(m=>m.dateISO).sort(); const last=ms[ms.length-1];
  if(last===claimed||(ms.length===0&&claimed==='none')) ok++; else bad.push(nm+': claimed '+claimed+' actual '+last); }
console.log('team-date truth: EXACT',ok,'/',teams.length, bad.length?(' MISMATCHES('+bad.length+'): '+bad.slice(0,5).join(' ; ')):'');
console.log('\nsample team lines:'); teams.slice(0,4).forEach(t=>console.log('  ',t[0].slice(0,110)));
if(out&&out.files) console.log('companion files:', Object.keys(out.files).join(', '));
if(out&&out.snapshot) console.log('snapshot bytes:', out.snapshot.length);
console.log('\nDONE');
