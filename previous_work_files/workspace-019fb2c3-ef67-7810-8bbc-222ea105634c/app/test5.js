const fs=require('fs');const {JSDOM}=require('jsdom');
let P=0,F=0;const ok=(c,m)=>{if(c)P++;else{F++;console.log('  FAIL:',m);}};
const dom=new JSDOM(fs.readFileSync('/home/user/pitch-rating.html','utf8'),{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,d=w.document,E=s=>w.eval(s);

console.log("=== CONTAMINATED STARS REMOVED ===");
ok(E('typeof STAR_CUTOFFS')==='undefined',"old att+dfn cutoffs gone");
const src=fs.readFileSync('/home/user/pitch-rating.html','utf8');
ok(!src.includes('STAR_CUTOFFS'),"no reference remains");
ok(E('MODEL.version')==='pitch-rating-v2.0',"version bumped: "+E('MODEL.version'));

console.log("=== STAR v2 = USER SPEC ===");
ok(E('MODEL.star_min_games')===5,"minimum 5 games enforced");
const s=E("starsFor('E0','Arsenal')");
ok(s>=1&&s<=5,"stars in 1-5: Arsenal="+s);
// verify the misranking from Study 08 is fixed
const tbl=E(`(function(){const o={};for(const t of Object.keys(MODEL.records.E0)){
 const r=MODEL.records.E0[t]; o[t]=[starsFor('E0',t),((3*r[1]+r[2])/r[0]).toFixed(2)];}return JSON.stringify(o);})()`);
const T=JSON.parse(tbl);
console.log("   Sunderland:",T['Sunderland'],"(was 1-star under att+dfn)");
console.log("   Nott'm Forest:",T["Nott'm Forest"],"(was 4-star under att+dfn)");
ok(Number(T['Sunderland'][0])>=3,"Sunderland no longer misranked as 1-star");
// monotonic: higher ppg => >= stars
const pairs=Object.values(T).map(x=>[Number(x[0]),Number(x[1])]).sort((a,b)=>a[1]-b[1]);
let mono=true; for(let i=1;i<pairs.length;i++) if(pairs[i][0]<pairs[i-1][0]) mono=false;
ok(mono,"stars monotonic in points-per-game");

console.log("=== DRAW CORRECTION APPLIED ===");
const r=JSON.parse(E("JSON.stringify(rateFixture('E0','Liverpool','Everton'))"));
ok(Math.abs(r.H+r.D+r.A-1)<1e-9,"probabilities sum to 1 after correction");
ok(r.starAdj===true,"draw adjustment fired");
// cap must be respected
const capOk=E(`(function(){let worst=0;
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<Math.min(ts.length,12);i++)for(let j=0;j<Math.min(ts.length,12);j++){if(i===j)continue;
const lam=lambdas(lg,ts[i],ts[j]); if(!lam)continue;
const g=scoreGrid(lam.lh,lam.la); let D0=0;
for(let a=0;a<11;a++)D0+=g[a][a];
const rr=rateFixture(lg,ts[i],ts[j]);
if(rr.starAdj) worst=Math.max(worst,Math.abs(rr.D-D0));}}
return worst;})()`);
console.log("   max draw shift observed:",capOk.toFixed(4),"(cap 0.02)");
ok(capOk<=0.0201,"0.02 cap respected");

console.log("=== CONSENSUS LAYER ===");
const c=JSON.parse(E("JSON.stringify(consensusFor('E0','Liverpool','Everton'))"));
ok(c&&typeof c.consensus==='number',"consensus computed: "+JSON.stringify(c).slice(0,80));
ok(Math.abs(c.consensus-(c.hvh+c.ava)/2)<1e-9,"consensus = mean of HvH and AvA");
ok(Math.abs(c.disagreement-Math.abs(c.hvh-c.ava))<1e-9,"disagreement = |HvH - AvA|");
const lbls=E(`(function(){const o={};
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
const r=rateFixture(lg,ts[i],ts[j]); const k=r.confidence?r.confidence.label:'none';
o[k]=(o[k]||0)+1;}}return JSON.stringify(o);})()`);
console.log("   label distribution:",lbls);
const L=JSON.parse(lbls);
ok(L.STRONG>0&&L.CONFIRMED>0,"STRONG and CONFIRMED both fire");
ok(L.CONFLICTED>0,"CONFLICTED fires");

console.log("=== CONSENSUS MUST NOT ALTER PROBABILITY ===");
const noconf=E(`(function(){let bad=0;
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<Math.min(ts.length,10);i++)for(let j=0;j<Math.min(ts.length,10);j++){if(i===j)continue;
const r=rateFixture(lg,ts[i],ts[j]);
if(Math.abs(r.H+r.D+r.A-1)>1e-6)bad++;}}return bad;})()`);
ok(noconf===0,"all probabilities valid with confidence layer active");
const cf=src.slice(src.indexOf('let confidence = null;'),src.indexOf('return {'));
ok(!/\bH\s*=|\bD\s*=|\bA\s*=/.test(cf),"confidence block never assigns H/D/A");

console.log("=== FULL INTEGRITY SWEEP ===");
const chk=E(`(function(){let n=0,bad=0,mk=0;
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
const r=rateFixture(lg,ts[i],ts[j]);n++;
if(Math.abs(r.H+r.D+r.A-1)>1e-6)bad++;
const m=r.markets;
if(!(m.o15>=m.o25-1e-9&&m.o25>=m.o35-1e-9))mk++;
for(const k of ['o15','o25','o35','dnb','dc1x'])if(!(m[k]>=0&&m[k]<=1))mk++;}}
return n+','+bad+','+mk;})()`).split(',');
ok(chk[1]==='0',chk[0]+" fixtures, "+chk[1]+" invalid");
ok(chk[2]==='0',"markets valid & monotone ("+chk[2]+" bad)");

console.log("=== REGRESSION: EARLIER FEATURES INTACT ===");
ok(E("flipCheck('E0','Barcelona','Arsenal').level")==='error',"flip guard");
ok(d.getElementById('viewUpdate')!==null,"sync tab");
ok(E("typeof parseSyncPayload")==='function',"sync parser");
const sel=(id,v)=>{const e=d.getElementById(id);e.value=v;e.dispatchEvent(new w.Event('change'));};
sel('homeTeam','Liverpool');sel('awayTeam','Everton');
ok(d.getElementById('saveBtn').disabled===true,"save gate still enforced");
ok(d.getElementById('result').innerHTML.includes('Consensus'),"consensus shown in UI");
console.log("   points:",d.querySelector('.pts').textContent,"badges:",
  [...d.querySelectorAll('.badge')].map(b=>b.textContent).join(' | '));

console.log(`\n=== ${P} passed, ${F} failed ===`);
process.exit(F?1:0);
