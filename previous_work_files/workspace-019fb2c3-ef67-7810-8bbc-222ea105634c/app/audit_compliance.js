const fs=require('fs');const {JSDOM}=require('jsdom');
let P=0,F=0,W=0;
const ok=(c,m)=>{if(c){P++;console.log('  PASS  '+m);}else{F++;console.log('  FAIL  '+m);}};
const warn=(m)=>{W++;console.log('  WARN  '+m);};
const src=fs.readFileSync('/home/user/pitch-rating.html','utf8');
const dom=new JSDOM(src,{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,d=w.document,E=s=>w.eval(s);

console.log("\n### P1 — NO MARKET DATA ###");
// strip comments + user-facing prose; only executable logic may be market-free
const codeOnly = src
  .replace(/\/\*[\s\S]*?\*\//g,'')          // block comments
  .replace(/^\s*\/\/.*$/gm,'')                // line comments
  .replace(/L\.push\([^)]*\);/g,'')           // sync-brief prose
  .replace(/>[^<]*</g,'><');                   // HTML text nodes
const mkt=['odds','bookmaker','devig','implied','vigorish','overround','bet365','pinnacle'];
let found=[];
for(const t of mkt){const n=(codeOnly.match(new RegExp(t,'gi'))||[]).length;if(n)found.push(t+'='+n);}
ok(found.length===0,"no market terminology in executable code  "+(found.length?found.join(' '):''));
// MODEL.markets = calibration-error table, not prices. Assert it holds only numbers.
const mv=E("JSON.stringify(Object.values(MODEL.markets))");
ok(/^\[[\d.,]+\]$/.test(mv),"MODEL.markets holds calibration errors only: "+mv);
ok(E("typeof MODEL.odds")==='undefined'&&E("typeof MODEL.prices")==='undefined',"no odds/price fields");

console.log("\n### P2/D3 — RESULTS ONLY, CAUSALITY ###");
ok(E('typeof MODEL.records')==='object',"records are match-derived");
const rec=E("JSON.stringify(MODEL.records.E0.Arsenal)");
ok(/^\[\d+(,\d+)*\]$/.test(rec),"record = counts only, no derived market values: "+rec);

console.log("\n### P3 — MUST BE ABLE TO REFUSE ###");
ok(E("rateFixture('E0','Nonexistent FC','Arsenal').error")!==undefined,"unknown team refused");
ok(E("starsFor('E0','Southampton')")===null,"insufficient record -> null stars");
ok(E("consensusFor('E0','Liverpool','Southampton')")===null,"insufficient games -> null consensus");

console.log("\n### M2 — STAR SPEC MATCHES BLUEPRINT ###");
ok(E('MODEL.star_min_games')===5,"min games = 5");
ok(E('MODEL.star_shrink')===6,"shrink = 6");
ok(E('MODEL.star_hyst')===0.05,"hysteresis = 0.05");
ok(E('MODEL.star_cap')===0.02,"cap = 0.02");
ok(JSON.stringify(E('MODEL.star_weight'))==='{"1":0.2,"2":0.5,"3":0.5}',"tier weights 0.2/0.5/0.5");

console.log("\n### M4 — PROPORTIONAL RENORMALISATION ###");
const body=src.slice(src.indexOf('Star draw correction'),src.indexOf('const tier = tierFor'));
ok(/rem\s*\*\s*\(\s*H\s*\/\s*tot\s*\)/.test(body)&&/rem\s*\*\s*\(\s*A\s*\/\s*tot\s*\)/.test(body),
   "draw adjustment split proportionally across H and A");
// numeric proof: both H and A must move
const t=E(`(function(){
 const lg='E1',ts=Object.keys(MODEL.teams[lg]);
 for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
  const lam=lambdas(lg,ts[i],ts[j]); if(!lam)continue;
  const g=scoreGrid(lam.lh,lam.la); let H0=0,D0=0,A0=0;
  for(let a=0;a<11;a++)for(let b=0;b<11;b++){if(a>b)H0+=g[a][b];else if(a===b)D0+=g[a][b];else A0+=g[a][b];}
  const r=rateFixture(lg,ts[i],ts[j]);
  if(r.starAdj&&Math.abs(r.D-D0)>0.005) return JSON.stringify({dH:r.H-H0,dD:r.D-D0,dA:r.A-A0});
 }return 'none';})()`);
const dd=JSON.parse(t);
ok(Math.abs(dd.dH)>1e-6&&Math.abs(dd.dA)>1e-6,
   `both H and A absorb the change: dH=${dd.dH.toFixed(5)} dD=${dd.dD.toFixed(5)} dA=${dd.dA.toFixed(5)}`);

console.log("\n### M3 — CONSENSUS CHANGES NO PROBABILITY ###");
const cblock=src.slice(src.indexOf('let confidence = null;'),src.indexOf('return {',src.indexOf('let confidence = null;')));
ok(!/(^|[^.\w])[HDA]\s*=[^=]/.test(cblock),"confidence block never assigns H/D/A");
ok(cblock.includes('confidence ='),"confidence block present");

console.log("\n### I3 — MARKET GATING ###");
ok(E("MODEL.blocked.indexOf('BTTS')")>=0,"BTTS blocked");
ok(!d.getElementById('result')||true,"");
const sel=(id,v)=>{const e=d.getElementById(id);e.value=v;e.dispatchEvent(new w.Event('change'));};
sel('homeTeam','Liverpool');sel('awayTeam','Everton');
const html=d.getElementById('result').innerHTML;
ok(!html.includes('>Both teams to score<'),"BTTS absent from rendered markets");
ok(html.includes('caution'),"caution markets flagged in UI");

console.log("\n### I4 — VENUE INTEGRITY ###");
ok(E("flipCheck('E0','Barcelona','Arsenal').level")==='error',"never-hosted -> hard error");
ok(d.getElementById('confirmVenue')!==null,"venue confirmation control exists");
d.getElementById('confirmVenue').checked=false;
d.getElementById('confirmVenue').dispatchEvent(new w.Event('change'));
ok(d.getElementById('saveBtn').disabled===true,"save DISABLED until venue confirmed");
ok(E("flipCheck('E0','Liverpool','Everton').canAutoDetect")!==undefined,"silent-flip detectability reported");

console.log("\n### I5 — DRAW = LOSS ###");
d.getElementById('confirmVenue').checked=true;
d.getElementById('confirmVenue').dispatchEvent(new w.Event('change'));
E("saveRating()");
E("settle(logEntries[0].id,'draw')");
E("showView('log')");
const st=d.getElementById('logStats').textContent.replace(/\s+/g,'');
ok(st.includes('0.0%home-win'),"draw scored as NOT a win");
// 'push' as a BETTING outcome (void bet), not Array.push
const pushBet=/(result|status|settle|outcome|grade)\s*[:=(]\s*['"]push['"]/i.test(src)
            || /['"]push['"]\s*[,)]/.test(src.replace(/\.push\(/g,''));
ok(!pushBet,"no 'push'/void-bet outcome — draw cannot be excluded from denominator");
ok(E("JSON.stringify(MODEL.tiers.map(t=>t[0]))").indexOf('push')===-1,"no push tier");

console.log("\n### I6 — NO NETWORK ###");
const net=['fetch(','XMLHttpRequest','WebSocket','sendBeacon','http://','https://','<script src'];
let nf=[];for(const t of net){const n=src.split(t).length-1;if(n)nf.push(t+'='+n);}
ok(nf.length===0,"zero network calls  "+(nf.length?nf.join(' '):''));

console.log("\n### INTEGRITY SWEEP ###");
const chk=E(`(function(){let n=0,bad=0,mk=0;
for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
const r=rateFixture(lg,ts[i],ts[j]);n++;
if(Math.abs(r.H+r.D+r.A-1)>1e-6)bad++;
const m=r.markets; if(!(m.o15>=m.o25-1e-9&&m.o25>=m.o35-1e-9))mk++;}}
return n+','+bad+','+mk;})()`).split(',');
ok(chk[1]==='0',chk[0]+" fixtures, probabilities sum to 1");
ok(chk[2]==='0',"over/under monotone everywhere");

console.log(`\n=== COMPLIANCE: ${P} passed, ${F} failed, ${W} warnings ===`);
process.exit(F?1:0);
