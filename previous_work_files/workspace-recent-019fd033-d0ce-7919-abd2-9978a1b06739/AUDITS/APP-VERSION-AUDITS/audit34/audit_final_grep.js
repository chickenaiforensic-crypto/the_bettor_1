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
console.log('R1 re-probe: "krasnodar" →', JSON.stringify(PR.ui.filterTeams(s,'krasnodar')), '| empty:', PR.ui.filterTeams(s,'').length);
const r=PR.compute.selectFixture(s,PR.derive.derive(s,{engines:[(st,d)=>{d.dcFit=PR.dc.fit(st)}]}),'CSKA Moscow','Krylia Sovetov Samara',{});
console.log('R4/R7 spot:', r.path.kind, '| HDA', [r.sections.find(x=>x.id==='probabilities').content.H, r.sections.find(x=>x.id==='probabilities').content.D, r.sections.find(x=>x.id==='probabilities').content.A].map(x=>Number(x).toFixed(3)).join('/'), '| graph section:', !!r.sections.find(x=>x.id==='graph'));
