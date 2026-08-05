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
const r=PR.compute.selectFixture(s,derived,'Atlanta United FC','Austin FC',{});
console.log('GOLDEN-4 okay-diagnosis:');
console.log(' ok:',r.ok,'| path:',JSON.stringify(r.path));
console.log(' honesty:',JSON.stringify(r.honesty,null,1));
r.sections.forEach(sec=>console.log('  section',sec.id,JSON.stringify(sec.content).slice(0,180)));
// how many MLS matches+dates?
const mls=s.matches.filter(m=>/major league/i.test(m.competition||m.leagueName||''));
console.log('MLS matches in store:', mls.length, 'date span:', mls.map(m=>m.dateISO).sort()[0], '→', mls.map(m=>m.dateISO).sort().slice(-1)[0]);
console.log('\nCOMMIT LOG entries:');
s.log.forEach(l=>console.log(' ',l.seq,l.action,'|',String(l.summary).slice(0,110)));
