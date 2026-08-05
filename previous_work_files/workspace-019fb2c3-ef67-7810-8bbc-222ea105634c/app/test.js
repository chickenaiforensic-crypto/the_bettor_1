const fs=require('fs');const {JSDOM}=require('jsdom');
const html=fs.readFileSync('/home/user/pitch-rating.html','utf8');
let fails=0,pass=0;
const ok=(c,m)=>{if(c)pass++;else{fails++;console.log('  FAIL:',m);}};
const dom=new JSDOM(html,{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,d=w.document,E=s=>w.eval(s);

console.log("=== BOOT ===");
ok(E('typeof MODEL')==='object',"MODEL loaded");
ok(E('typeof rateFixture')==='function',"rateFixture defined");
ok(E('typeof flipCheck')==='function',"flipCheck defined");
ok(d.getElementById('league').options.length===18,"18 leagues");
ok(d.getElementById('homeTeam').options.length>20,"teams populated");
ok(E('MODEL.calibration.n')===150360,"calibration metadata present");

console.log("=== RATE A FIXTURE ===");
const sel=(id,v)=>{const e=d.getElementById(id);e.value=v;e.dispatchEvent(new w.Event('change'));};
sel('homeTeam','Liverpool');sel('awayTeam','Southampton');
const res=d.getElementById('result').innerHTML;
ok(res.includes('home rating'),"rating rendered");
console.log("   points:",d.querySelector('.pts').textContent,"tier:",d.querySelector('.badge').textContent);
ok(res.includes('Over 2.5'),"markets table present");
ok(!res.includes('>Both teams to score<'),"BTTS withheld");
ok(d.getElementById('flipBox').innerHTML.includes('Venue plausible'),"flip ok for valid fixture");

console.log("=== SAVE GATE ===");
ok(d.getElementById('saveBtn').disabled===true,"save DISABLED pre-confirm");
E('saveRating()');
ok(E('logEntries.length')===0,"save blocked without confirmation");
d.getElementById('confirmVenue').checked=true;
d.getElementById('confirmVenue').dispatchEvent(new w.Event('change'));
ok(d.getElementById('saveBtn').disabled===false,"save ENABLED post-confirm");
E('saveRating()');
ok(E('logEntries.length')===1,"saved");

console.log("=== DRAW COUNTS AS A LOSS (audit-01 F4) ===");
E("settle(logEntries[0].id,'draw')");
E("showView('log')");
const st=d.getElementById('logStats').textContent.replace(/\s+/g,'');
ok(st.includes('1settled'),"1 settled");
ok(st.includes('0.0%home-win'),"draw NOT counted as a win -> 0.0%");
ok(st.includes('Brier'),"Brier computed");
console.log("   stats:",d.getElementById('logStats').textContent.replace(/\s+/g,' ').trim());

console.log("=== FLIP DETECTION ===");
ok(E("flipCheck('E0','Barcelona','Arsenal').level")==='error',"never-hosted -> error");
const evenWarn=E("JSON.stringify(flipCheck('E0','Arsenal','Chelsea'))");
console.log("   even matchup:",evenWarn.slice(0,120));
ok(E("flipCheck('E0','Liverpool','Southampton').canAutoDetect")===true,"lopsided flip detectable");

console.log("=== PROBABILITY INTEGRITY (every fixture, all leagues) ===");
const r=E(`(function(){let n=0,bad=0,mk=0;
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
const r=rateFixture(lg,ts[i],ts[j]);n++;
if(Math.abs(r.H+r.D+r.A-1)>1e-6)bad++;
const m=r.markets;
for(const k of ['o15','o25','o35','dnb','dc1x','hm1'])if(!(m[k]>=0&&m[k]<=1))mk++;
if(!(m.o15>=m.o25-1e-9&&m.o25>=m.o35-1e-9))mk++;
if(Math.abs(m.dc1x-(r.H+r.D))>1e-9)mk++;}}
return n+','+bad+','+mk;})()`).split(',').map(Number);
ok(r[1]===0,`H+D+A=1 across ${r[0]} fixtures (${r[1]} bad)`);
ok(r[2]===0,`markets valid+monotone (${r[2]} bad)`);
console.log("   verified",r[0],"fixtures");

console.log("=== CALIBRATION SANITY vs PUBLISHED TIERS ===");
const t=E("JSON.stringify(tierFor(0.78))");
ok(t.includes('A+'),"0.78 -> A+ Fortress");
ok(E("tierFor(0.30).name").indexOf('E')===0,"0.30 -> E Avoid");

console.log("=== XSS ===");
ok(E("esc('<img src=x onerror=alert(1)>')").includes('&lt;img'),"esc escapes");

console.log("=== ABOUT ===");
E("showView('about')");
ok(d.getElementById('aboutTiers').innerHTML.includes('A+ Fortress'),"tiers table");
ok(d.getElementById('aboutHfa').innerHTML.includes('1.36'),"HFA table");
ok(d.getElementById('aboutMarkets').innerHTML.includes('withheld'),"BTTS withheld row");

console.log("=== PERSISTENCE ===");
ok(w.localStorage.getItem('pitchRating:log:v1')!==null,"written to localStorage");

console.log(`\n=== ${pass} passed, ${fails} failed ===`);
process.exit(fails?1:0);
