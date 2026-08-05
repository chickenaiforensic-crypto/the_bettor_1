/* AUDIT app-v3.html — real boot in node vm, golden fixtures, cache proof */
const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('uploads/app-v3.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
// scripts: 1=main, 2=fitted, 3=SEED+boot, 4=CF(SKIP)
const s1=block(1), s2=block(2), s3=block(3);
function makeEl(){ const el={innerHTML:'',textContent:'',value:'',style:{},dataset:{},children:[],classList:{add(){},remove(){},toggle(){},contains(){return false}},
 addEventListener(){},removeEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){},focus(){}}; return el; }
const store={}; const els={};
const documentStub={ readyState:'loading', _listeners:{},
 addEventListener(t,f){ (this._listeners[t]=this._listeners[t]||[]).push(f); },
 getElementById(id){ return els[id]||(els[id]=makeEl()); },
 createElement(){ return makeEl(); }, querySelectorAll(){return[]}, querySelector(){return makeEl()},
 body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sandbox={ window:null, document:documentStub,
 localStorage:{ getItem:k=>store[k]||null, setItem:(k,v)=>{store[k]=String(v)}, removeItem:k=>{delete store[k]} },
 setTimeout:(f)=>{ /* do not fire toasts */ }, clearTimeout(){}, console, navigator:{userAgent:'audit'},
 addEventListener(){}, location:{href:'',reload(){}} };
sandbox.window=sandbox; sandbox.globalThis=sandbox;
vm.createContext(sandbox);
vm.runInContext(s1,sandbox,{filename:'main.js'});
vm.runInContext(s2,sandbox,{filename:'fitted.js'});
vm.runInContext(s3,sandbox,{filename:'boot.js'});
const PR=sandbox.PR;
console.log('== PR modules ==', Object.keys(PR).join(','));
// real first boot
sandbox.boot();
const s=PR.store.load();
console.log('\n== STORE COUNTS ==');
['identities','matches','venues','seasons','sources','ctxFlags','mutes','log','artifacts','notes'].forEach(t=>console.log(t.padEnd(12), (s[t]||[]).length));
const skips=s.log.filter(l=>/seed-skip/.test(l.action||''));
console.log('seed-skip log lines:', skips.length); skips.forEach(l=>console.log('  SKIP:',l.summary.slice(0,140)));
console.log('log actions:', s.log.map(l=>l.action).join(' | '));
console.log('seedPacks meta:', (s.meta.seedPacks||[]).join(', '));

// derived
const derived=PR.derive.derive(s,{engines:[function(st,d){ d.dcFit=PR.dc.fit(st); }]});
console.log('\n== DERIVED ==');
console.log('storeHash:', derived.storeHash && String(derived.storeHash).slice(0,16));
const leagues=derived.leagues||derived.leagueRegistry||[];
console.log('leagues derived:', Array.isArray(leagues)? leagues.map(l=>l.name||l).join(' | ') : JSON.stringify(leagues).slice(0,300));

// golden fixtures
function probe(h,a,label){
  const r=PR.compute.selectFixture(s,derived,h,a,{});
  console.log('\n== ',label,' ==');
  console.log('ok:',r.ok,'| path:',r.path.kind,'| label:',r.path.label,'| reasons:',(r.path.reasons||[]).join(' ; '));
  (r.sections||[]).forEach(sec=>{
    const c=sec.content||{};
    let line=sec.id+' ['+(sec.capability||'')+']: ';
    if(c.leader!=null) line+='leader='+JSON.stringify(c.leader)+' ';
    if(c.totals) line+='totals='+JSON.stringify(c.totals)+' ';
    if(c.H!=null) line+='HDA='+[c.H,c.D,c.A].map(x=>x!=null?Number(x).toFixed(3):'-')+' ';
    if(c.expected!=null) line+='expScore='+c.expected+' ';
    if(c.text) line+='text="'+String(c.text).slice(0,90)+'" ';
    if(sec.id==='balances'||sec.id==='summation'||sec.id==='sections') line+=JSON.stringify(c).slice(0,220);
    if(sec.id==='stars') line+=JSON.stringify(c).slice(0,120);
    if(sec.id==='form') line+=JSON.stringify(c).slice(0,180);
    console.log(' ',line);
  });
  if(r.confidence) console.log('  confidence:', JSON.stringify(r.confidence));
  (r.honesty&&r.honesty.refusals||[]).forEach(x=>console.log('  REFUSAL:',x));
  (r.honesty&&r.honesty.warnings||[]).forEach(x=>console.log('  WARNING:',x));
  (r.honesty&&r.honesty.notes||[]).forEach(x=>console.log('  note:',x));
  console.log('  provenance:', JSON.stringify(r.provenance||{}).slice(0,200));
  return r;
}
probe('FC Krasnodar','Fakel Voronezh','GOLDEN-1 Krasnodar v Fakel (evidence, RPL)');
probe('CSKA Moscow','Krylia Sovetov Samara','GOLDEN-2 CSKA v Krylia (evidence, RPL)');
probe('Ross County','St Johnstone','GOLDEN-3 ghost fixture (SC1, 0 matches)');
probe('Atlanta United','Austin','GOLDEN-4 MLS connectivity');
probe('Celtic','Rangers','GOLDEN-5 fitted-path candidates (SC0 params, 0 local rows)');
probe('Hibernian','Malisheva','GOLDEN-6 Hibernian v Malisheva (cross, from packs)');
fs.writeFileSync('audit3/boot_report.json', JSON.stringify({counts:Object.fromEntries(['identities','matches','venues','seasons','sources','mutes','log','artifacts'].map(t=>[t,(s[t]||[]).length])), skips:skips.length, hash:derived.storeHash},null,2));
console.log('\nDONE');
