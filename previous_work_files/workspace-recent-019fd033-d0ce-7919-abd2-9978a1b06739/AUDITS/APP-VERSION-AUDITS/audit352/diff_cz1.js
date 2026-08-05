const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('audit352/app-v3.5.2-decoded.html','utf8');
function block(n){ const re=/<script>([\s\S]*?)<\/script>/g; let m,i=0; while((m=re.exec(html))){ i++; if(i===n) return m[1]; } }
function makeEl(){ return {innerHTML:'',textContent:'',value:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){},contains(){return false}},addEventListener(){},querySelectorAll(){return[]},querySelector(){return makeEl()},appendChild(){},remove(){},setAttribute(){},getAttribute(){return null},click(){}}; }
const store={}; const els={};
const documentStub={ readyState:'loading', addEventListener(){}, getElementById(id){ return els[id]||(els[id]=makeEl()); }, createElement(){return makeEl()}, querySelectorAll(){return[]}, querySelector(){return makeEl()}, body:{appendChild(){},classList:{add(){},remove(){}}}, documentElement:{setAttribute(){},style:{}} };
const sb={ window:null, document:documentStub, localStorage:{getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=String(v)},removeItem:k=>{delete store[k]}}, setTimeout(){}, console:{log(){},warn(){},error(){}}, navigator:{}, addEventListener(){}, location:{href:''}, URL:{createObjectURL(){return 'blob:x'}, revokeObjectURL(){}}, Blob:class{constructor(p){this.p=p}}, HTMLAnchorElement:function(){} };
sb.window=sb; sb.globalThis=sb; vm.createContext(sb);
for(let i=1;i<=4;i++) vm.runInContext(block(i),sb,{filename:'s'+i});
const PR=sb.PR;
const R=PR.store.deserialize(fs.readFileSync('/home/user/uploads/pitch-rating-full-data-2026-08-02.json','utf8'));
PR.store.save(R.store); sb.boot();
const s=PR.store.load();
function seasonOf(d){ const y=+d.slice(0,4), mo=+d.slice(5,7); return mo>=7? y+'-'+(y+1) : (y-1)+'-'+y; }
const XTRA=['Artis Brno','Zbrojovka Brno'];
s.matches.filter(m=>m.competitionName==='Czech First League'&&(XTRA.includes(m.homeName)||XTRA.includes(m.awayName))).forEach(m=>console.log('INTRUDER? '+m.dateISO+' '+m.homeName+' '+m.homeGoals+'-'+m.awayGoals+' '+m.awayName));
const OFF={
 '2024-2025':{groups:{'Slavia Prague':[29,3,3,77,18,90],'Viktoria Plzen':[23,5,7,71,36,74],'Banik Ostrava':[22,5,8,58,34,71],'Sparta Prague':[19,6,10,61,44,63],'Jablonec':[19,6,10,60,33,63],'Sigma Olomouc':[12,9,14,48,53,45],'Teplice':[12,8,15,41,45,44],'Mlada Boleslav':[11,8,16,48,48,41],'Slovacko':[9,11,15,31,56,38],'Dukla Prague':[8,10,17,34,55,34],'Pardubice':[6,7,22,25,56,25],'Ceske Budejovice':[0,6,29,16,86,6]}, placement:{'Hradec Kralove':34,'Bohemians 1905':34,'Karvina':32,'Slovan Liberec':32}},
 '2025-2026':{groups:{'Slavia Prague':[24,8,3,74,31,80],'Sparta Prague':[23,7,5,69,34,76],'Viktoria Plzen':[18,9,8,60,38,63],'Hradec Kralove':[16,8,11,50,41,56],'Jablonec':[16,7,12,45,47,55],'Slovan Liberec':[12,10,13,45,39,46],'Teplice':[10,12,13,40,42,42],'Zlin':[11,8,16,43,56,41],'Mlada Boleslav':[9,13,13,49,57,40],'Slovacko':[7,9,19,30,51,30],'Banik Ostrava':[7,8,20,32,49,29],'Dukla Prague':[5,11,19,23,51,26]}, placement:{'Sigma Olomouc':34,'Karvina':34,'Pardubice':32,'Bohemians 1905':32}}
};
Object.keys(OFF).forEach(S=>{
  const rows=s.matches.filter(m=>m.competitionName==='Czech First League'&&seasonOf(m.dateISO)===S&&!XTRA.includes(m.homeName)&&!XTRA.includes(m.awayName));
  const T={};
  rows.forEach(m=>{ [m.homeName,m.awayName].forEach(n=>T[n]=T[n]||{p:0,w:0,d:0,l:0,gf:0,ga:0});
    const H=T[m.homeName],A=T[m.awayName]; H.p++;A.p++; H.gf+=m.homeGoals;H.ga+=m.awayGoals; A.gf+=m.awayGoals;A.ga+=m.homeGoals;
    if(m.homeGoals>m.awayGoals){H.w++;A.l++;} else if(m.homeGoals<m.awayGoals){A.w++;H.l++;} else {H.d++;A.d++;} });
  let gmis=0, pmis=0;
  Object.entries(OFF[S].groups).forEach(([n,ref])=>{
    const t=T[n]; if(!t){console.log('  '+S+' MISSING '+n); gmis++; return;}
    const ours=[t.w,t.d,t.l,t.gf,t.ga,t.w*3+t.d];
    if(JSON.stringify(ours)!==JSON.stringify(ref)){ gmis++; console.log('  '+S+' MISMATCH '+n+': ours '+ours.join('/')+' vs RSSSF '+ref.join('/')); }
  });
  Object.entries(OFF[S].placement).forEach(([n,c])=>{ const t=T[n]; if(!t||t.p!==c){ pmis++; console.log('  '+S+' placement '+n+': ours '+(t?t.p:'absent')+'p vs expected '+c+'p'); } });
  console.log('=== CZ1 '+S+': 12 group clubs (35-game tables) -> '+(gmis===0?'ALL 12 EXACT':gmis+' MISMATCHES')+' | placement counts -> '+(pmis===0?'ALL 4 EXACT':pmis+' OFF')+' ===');
});
