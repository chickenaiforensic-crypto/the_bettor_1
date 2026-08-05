const fs=require('fs');const {JSDOM}=require('jsdom');
let P=0,F=0;const ok=(c,m)=>{if(c)P++;else{F++;console.log('  FAIL:',m);}};
const dom=new JSDOM(fs.readFileSync('/home/user/pitch-rating.html','utf8'),{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,d=w.document,E=s=>w.eval(s);
const J=s=>JSON.parse(E("JSON.stringify("+s+")"));

console.log("=== REGRESSION ===");
ok(d.getElementById('league').options.length===18,"18 leagues");
const sel=(id,v)=>{const e=d.getElementById(id);e.value=v;e.dispatchEvent(new w.Event('change'));};
sel('homeTeam','Liverpool');sel('awayTeam','Southampton');
ok(d.querySelector('.pts').textContent==='61',"Liverpool v Soton still 61");

console.log("=== BRIEF GENERATION ===");
E("showView('update')");
E("generateBrief('one')");
const brief=d.getElementById('briefBox').value;
ok(brief.includes('PITCH-SYNC v1'),"brief has protocol header");
ok(brief.includes('Base built:'),"states base build date");
ok(brief.includes('results through'),"states per-league through date");
ok(brief.includes('Arsenal'),"lists exact team spellings");
ok(brief.includes('THE TEAM LISTED FIRST IS THE HOME TEAM'),"home/away rule stated prominently");
ok(brief.includes('90-minute score'),"ET/pens rule stated");
ok(brief.includes('EXCLUDE cups'),"scope rule stated");
console.log("   single-league brief:",brief.length,"chars");
E("generateBrief('all')");
const briefAll=d.getElementById('briefBox').value;
ok(briefAll.includes('[SP1]')&&briefAll.includes('[I1]'),"all-league brief covers every league");
console.log("   all-league brief:",briefAll.length,"chars");

console.log("=== HAPPY PATH ===");
const good=`PITCH-SYNC v1
LEAGUE: E0
2026-07-15|Arsenal|2|1|Chelsea
2026-07-16|Liverpool|3|0|Everton
END`;
let r=J("parseSyncPayload("+JSON.stringify(good)+")");
ok(r.rows.length===2&&r.errors.length===0,"2 clean rows, 0 errors");
ok(r.rows[0].home==='Arsenal'&&r.rows[0].hg===2,"fields mapped correctly");

console.log("=== ADVERSARIAL: each must be REJECTED ===");
const bad=[
 ["no header","LEAGUE: E0\n2026-07-15|Arsenal|2|1|Chelsea\nEND","not a sync block"],
 ["future date","PITCH-SYNC v1\nLEAGUE: E0\n2099-01-01|Arsenal|2|1|Chelsea\nEND","future"],
 ["bad date fmt","PITCH-SYNC v1\nLEAGUE: E0\n15/08/2026|Arsenal|2|1|Chelsea\nEND","bad date"],
 ["unknown league","PITCH-SYNC v1\nLEAGUE: ZZ9\n2026-07-15|Arsenal|2|1|Chelsea\nEND","unknown league"],
 ["unknown team","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Fake United|2|1|Chelsea\nEND","not in"],
 ["wrong field count","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Arsenal|2|Chelsea\nEND","expected 5 fields"],
 ["absurd score","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Arsenal|99|1|Chelsea\nEND","bad score"],
 ["negative score","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Arsenal|-2|1|Chelsea\nEND","bad score"],
 ["team plays itself","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Arsenal|2|1|Arsenal\nEND","cannot play itself"],
 ["row before LEAGUE","PITCH-SYNC v1\n2026-07-15|Arsenal|2|1|Chelsea\nEND","before any LEAGUE"],
 ["dup in paste","PITCH-SYNC v1\nLEAGUE: E0\n2026-07-15|Arsenal|2|1|Chelsea\n2026-07-15|Arsenal|2|1|Chelsea\nEND","duplicate"],
];
bad.forEach(([label,payload,expect])=>{
  const rr=J("parseSyncPayload("+JSON.stringify(payload)+")");
  const errtxt=(rr.errors||[]).join(" ").toLowerCase();
  const caught=errtxt.includes(expect.toLowerCase());
  ok(caught,label+" -> expected '"+expect+"', got: "+(rr.errors[0]||"NO ERROR, rows="+rr.rows.length));
});

console.log("=== FLIP GUARD ON IMPORTED DATA ===");
const flip=`PITCH-SYNC v1
LEAGUE: E0
2026-07-15|Barcelona|2|1|Arsenal
END`;
r=J("parseSyncPayload("+JSON.stringify(flip)+")");
ok(r.errors.length>0||r.rows.some(x=>x.flip),"cross-league/never-hosted team caught");
console.log("   ->",(r.errors[0]||"flagged flip=true"));

console.log("=== FUZZY NAME MATCH IS FLAGGED, NOT SILENT ===");
const fuzzy=`PITCH-SYNC v1
LEAGUE: E0
2026-07-15|Arsenal|2|1|Chelsea FC
END`;
r=J("parseSyncPayload("+JSON.stringify(fuzzy)+")");
if(r.rows.length){ok(r.rows[0].renamedA!==null||r.rows[0].away==='Chelsea',"fuzzy match recorded: "+r.rows[0].away+" (was "+r.rows[0].renamedA+")");}
else{ok(r.errors.length>0,"or rejected outright");}

console.log("=== IDEMPOTENCY: applying twice must not double-count ===");
E("OVERLAY={teams:{},leagues:{},seen:{},applied:[],lastUpdate:null,fp:{},through:{},counts:{}};saveOverlay();applyOverlay();");
const before=J("MODEL.teams.E0['Arsenal']");
d.getElementById('syncBox').value=good;
E("validateSync()"); E("applySync()");
const after1=J("MODEL.teams.E0['Arsenal']");
ok(after1[0]!==before[0],"first apply changed ratings");
d.getElementById('syncBox').value=good;
E("validateSync()");
const r2=J("__lastSync");
ok(r2.rows.every(x=>x.dup),"second paste: all rows flagged as duplicates");
ok(d.getElementById('applySyncBtn').disabled===true,"apply button disabled for pure-duplicate paste");
E("applySync()");
const after2=J("MODEL.teams.E0['Arsenal']");
ok(Math.abs(after2[0]-after1[0])<1e-12,"ratings UNCHANGED after re-paste (idempotent)");

console.log("=== STATE TRACKING ===");
const thr=J("OVERLAY.through");
ok(thr.E0==='2026-07-16',"through-date advanced to latest match: "+thr.E0);
ok(J("OVERLAY.counts").E0===2,"per-league applied count = 2");
E("generateBrief('one')");
ok(d.getElementById('briefBox').value.includes('2026-07-16'),"next brief reports the new through-date");

console.log("=== CHRONOLOGICAL ORDER ===");
E("OVERLAY={teams:{},leagues:{},seen:{},applied:[],lastUpdate:null,fp:{},through:{},counts:{}};saveOverlay();applyOverlay();");
const fwd=`PITCH-SYNC v1
LEAGUE: E0
2026-07-15|Arsenal|2|1|Chelsea
2026-07-22|Arsenal|1|0|Everton
END`;
d.getElementById('syncBox').value=fwd; E("validateSync()"); E("applySync()");
const ordered=J("MODEL.teams.E0['Arsenal']")[0];
E("OVERLAY={teams:{},leagues:{},seen:{},applied:[],lastUpdate:null,fp:{},through:{},counts:{}};saveOverlay();applyOverlay();");
const rev=`PITCH-SYNC v1
LEAGUE: E0
2026-07-22|Arsenal|1|0|Everton
2026-07-15|Arsenal|2|1|Chelsea
END`;
d.getElementById('syncBox').value=rev; E("validateSync()"); E("applySync()");
const reordered=J("MODEL.teams.E0['Arsenal']")[0];
ok(Math.abs(ordered-reordered)<1e-12,"out-of-order paste sorted by date before applying");

console.log("=== INTEGRITY AFTER SYNC ===");
const chk=E(`(function(){let n=0,bad=0;for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;const r=rateFixture(lg,ts[i],ts[j]);n++;
if(Math.abs(r.H+r.D+r.A-1)>1e-6)bad++;}}return n+','+bad;})()`).split(',');
ok(chk[1]==='0',chk[0]+" fixtures valid after sync, "+chk[1]+" bad");

console.log("=== NOTES PASSED THROUGH ===");
r=J("parseSyncPayload('PITCH-SYNC v1\\nLEAGUE: E0\\n# note: Burnley promoted, not rated\\nEND')");
ok(r.notes.length===1,"# comment captured as a note");

console.log(`\n=== ${P} passed, ${F} failed ===`);
process.exit(F?1:0);
