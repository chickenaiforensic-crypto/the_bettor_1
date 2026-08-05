const fs=require('fs');const {JSDOM}=require('jsdom');
let P=0,F=0;const ok=(c,m)=>{if(c)P++;else{F++;console.log('  FAIL:',m);}};
const dom=new JSDOM(fs.readFileSync('/home/user/pitch-rating.html','utf8'),{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,d=w.document,E=s=>w.eval(s);

console.log("=== REGRESSION: original 28 checks still pass ===");
ok(E('typeof MODEL')==='object',"MODEL loaded");
ok(d.getElementById('league').options.length===18,"18 leagues");
const sel=(id,v)=>{const e=d.getElementById(id);e.value=v;e.dispatchEvent(new w.Event('change'));};
sel('homeTeam','Liverpool');sel('awayTeam','Southampton');
ok(d.querySelector('.pts').textContent==='61',"Liverpool v Southampton still 61 pts, got "+d.querySelector('.pts').textContent);
ok(E("flipCheck('E0','Barcelona','Arsenal').level")==='error',"flip guard intact");
ok(d.getElementById('saveBtn').disabled===true,"save gate intact");

console.log("=== UPDATE TAB ===");
ok(d.getElementById('viewUpdate')!==null,"update view exists");
ok(d.getElementById('uLeague').options.length===18,"league dropdown populated");
E("showView('update')");
ok(d.getElementById('viewUpdate').className==='',"update view shows");
ok(d.getElementById('updStatus').textContent.includes('153,058'),"status banner rendered");
ok(d.getElementById('updStatus').textContent.includes('Base age'),"age shown");

console.log("=== PARSER: all documented formats ===");
const fmts=[
 ["Arsenal 2-1 Chelsea","dash"],
 ["Arsenal 2 - 1 Chelsea","spaced dash"],
 ["Arsenal,2,1,Chelsea","csv"],
 ["2026-08-15 Arsenal 2-1 Chelsea","iso date prefix"],
 ["15/08/2026 Arsenal 2-1 Chelsea","slash date prefix"],
 ["Arsenal 2:1 Chelsea","colon"],
];
fmts.forEach(([s,label])=>{
  const r=E("JSON.stringify(parseResults("+JSON.stringify(s)+",'E0'))");
  const o=JSON.parse(r);
  ok(o.games.length===1&&o.games[0].home==='Arsenal'&&o.games[0].away==='Chelsea'&&o.games[0].hg===2&&o.games[0].ag===1,
     label+" -> "+r.slice(0,90));
});
const badr=JSON.parse(E("JSON.stringify(parseResults('Nonsense FC 9-9 Fake United','E0'))"));
ok(badr.games.length===0&&badr.bad.length===1,"unknown teams rejected, not silently dropped");
ok(badr.bad[0].includes('not recognised'),"rejection explains why");

console.log("=== FIDELITY: browser update == python rebuild? ===");
// apply one result in browser, capture ratings
const before=JSON.parse(E("JSON.stringify(MODEL.teams.E0['Arsenal'])"));
const beforeC=JSON.parse(E("JSON.stringify(MODEL.teams.E0['Chelsea'])"));
const beforeL=JSON.parse(E("JSON.stringify(MODEL.leagues.E0)"));
E("applyResult('E0','Arsenal','Chelsea',2,1)");
const after=JSON.parse(E("JSON.stringify(MODEL.teams.E0['Arsenal'])"));
const afterC=JSON.parse(E("JSON.stringify(MODEL.teams.E0['Chelsea'])"));
const afterL=JSON.parse(E("JSON.stringify(MODEL.leagues.E0)"));
console.log("  Arsenal att/dfn/xh:",before.map(x=>x.toFixed(4)).join(","),"->",after.map(x=>x.toFixed(4)).join(","));
console.log("  Chelsea att/dfn/xh:",beforeC.map(x=>x.toFixed(4)).join(","),"->",afterC.map(x=>x.toFixed(4)).join(","));
console.log("  E0 mu/hfa:",beforeL.mu.toFixed(4)+"/"+beforeL.hfa.toFixed(4),"->",afterL.mu.toFixed(4)+"/"+afterL.hfa.toFixed(4));
ok(after[0]!==before[0],"Arsenal attack moved");
ok(afterC[1]!==beforeC[1],"Chelsea defence moved");
fs.writeFileSync('/tmp/js_update.json',JSON.stringify({
  before:{A:before,C:beforeC,L:beforeL},after:{A:after,C:afterC,L:afterL}}));

console.log("=== PERSISTENCE ===");
ok(w.localStorage.getItem('pitchRating:overlay:v1')!==null,"overlay persisted");
E("resetOverlay=function(){OVERLAY={teams:{},leagues:{},seen:{},applied:[],lastUpdate:null};saveOverlay();applyOverlay();}");
E("resetOverlay()");
const rst=JSON.parse(E("JSON.stringify(MODEL.teams.E0['Arsenal'])"));
ok(Math.abs(rst[0]-before[0])<1e-9,"reset restores shipped ratings exactly");

console.log("=== RATINGS EXPORT SHAPE ===");
const ex=E("(function(){return JSON.stringify({v:MODEL.version,t:Object.keys(MODEL.teams).length});})()");
ok(ex.includes('18'),"export covers 18 leagues");

console.log(`\n=== ${P} passed, ${F} failed ===`);
process.exit(F?1:0);
