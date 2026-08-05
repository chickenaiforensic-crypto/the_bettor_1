const fs=require('fs');const {JSDOM}=require('jsdom');
let P=0,F=0;
const ok=(c,m)=>{if(c){P++;console.log('  PASS  '+m);}else{F++;console.log('  FAIL  '+m);}};
const src=fs.readFileSync('/home/user/pitch-rating.html','utf8');
const dom=new JSDOM(src,{runScripts:"dangerously",url:"https://x.test/"});
const w=dom.window,E=s=>w.eval(s);

console.log("\n### B1/B4 — ENGINE CONSTANTS MATCH SPEC ###");
ok(E('RHO')===-0.06,"rho = -0.06");
ok(E('KMAX')===11,"grid 0..10");
ok(E('LR')===0.055,"LR = 0.055");
ok(E('DECAY')===0.0022,"DECAY = 0.0022");
ok(E('HFA_LR')===0.010,"HFA_LR = 0.010");
ok(E('SHRINK')===0.5,"goals shrink k = 0.5");
ok(Math.abs(E('GMU')-2.6186)<1e-9,"GMU = 2.6186");

console.log("\n### B1 — DEF SIGN CONVENTION (higher def = better defence) ###");
const sign=E(`(function(){
 const lg='E0', t=Object.keys(MODEL.teams[lg]);
 // raise a team's def, away goals conceded must FALL
 const orig=MODEL.teams[lg][t[0]].slice();
 const a1=lambdas(lg,t[1],t[0]).la;      // t[0] away... use as defender at home
 const b1=lambdas(lg,t[0],t[1]).la;
 MODEL.teams[lg][t[0]][1]=orig[1]+0.5;   // better defence
 const b2=lambdas(lg,t[0],t[1]).la;
 MODEL.teams[lg][t[0]]=orig;
 return b2<b1;})()`);
ok(sign===true,"raising def LOWERS opponent lambda");

console.log("\n### B1 — LAMBDA CLAMP ###");
ok(/Math\.max\(0\.05,\s*Math\.min\(6/.test(src),"lambda clamped to [0.05, 6.0]");

console.log("\n### C1 — GRID NORMALISATION + DC TAU ###");
const gsum=E(`(function(){const g=scoreGrid(1.7,1.1);let s=0;
 for(let i=0;i<11;i++)for(let j=0;j<11;j++)s+=g[i][j];return s;})()`);
ok(Math.abs(gsum-1)<1e-9,"scoreGrid sums to 1 ("+gsum.toFixed(12)+")");
ok(E('tau(0,0,1.5,1.2)')!==1,"tau modifies 0-0");
ok(E('tau(1,1,1.5,1.2)')!==1,"tau modifies 1-1");
ok(E('tau(3,2,1.5,1.2)')===1,"tau neutral elsewhere");

console.log("\n### C2 — TWO-GRID DESIGN ###");
const two=E(`(function(){const a=scoreGrid(2.4,0.6),b=goalsGrid(2.4,0.6);
 let ta=0,tb=0;
 for(let i=0;i<11;i++)for(let j=0;j<11;j++){ta+=(i+j)*a[i][j];tb+=(i+j)*b[i][j];}
 return JSON.stringify([ta,tb]);})()`);
const [ta,tb]=JSON.parse(two);
ok(Math.abs(tb-2.6186)<Math.abs(ta-2.6186),
   `goalsGrid total (${tb.toFixed(3)}) shrunk toward GMU vs scoreGrid (${ta.toFixed(3)})`);

console.log("\n### D1 — STAR SPEC ###");
ok(E('MODEL.star_min_games')===5 && E('MODEL.star_shrink')===6 && E('MODEL.star_hyst')===0.05,
   "min 5 / shrink 6 / hyst 0.05");
const mono=E(`(function(){
 const lg='E0',o=[];
 for(const t of Object.keys(MODEL.records[lg])){const r=MODEL.records[lg][t];
  o.push([starsFor(lg,t),(3*r[1]+r[2])/r[0]]);}
 o.sort((a,b)=>a[1]-b[1]);
 for(let i=1;i<o.length;i++) if(o[i][0]<o[i-1][0]) return false;
 return true;})()`);
ok(mono===true,"stars monotone in points-per-game (no att+def misranking)");

console.log("\n### D3 — CAP AND PROPORTIONAL SPLIT ###");
const cap=E(`(function(){let worst=0;
 for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
 for(let i=0;i<Math.min(ts.length,14);i++)for(let j=0;j<Math.min(ts.length,14);j++){if(i===j)continue;
 const lam=lambdas(lg,ts[i],ts[j]); if(!lam)continue;
 const g=scoreGrid(lam.lh,lam.la); let D0=0;
 for(let a=0;a<11;a++)D0+=g[a][a];
 const r=rateFixture(lg,ts[i],ts[j]);
 if(r.starAdj) worst=Math.max(worst,Math.abs(r.D-D0));}}
 return worst;})()`);
ok(cap<=0.0200001,"0.02 cap never exceeded (max "+cap.toFixed(5)+")");

console.log("\n### E1 — TIER CUTS ON CALIBRATED PROBABILITY ###");
ok(E("tierFor(0.78).name").indexOf('A+')===0,"0.78 -> A+ Fortress");
ok(E("tierFor(0.30).name").indexOf('E')===0,"0.30 -> E Avoid");
ok(E("Math.round(rateFixture('E0','Liverpool','Everton').H*100)")===E("rateFixture('E0','Liverpool','Everton').points"),
   "points = round(100 x H)");

console.log("\n### G — OUTPUT PROVENANCE (the two-family split) ###");
const prov=E(`(function(){let bad=0,n=0,dnb=0,mono=0;
 for(const lg of Object.keys(MODEL.teams)){const ts=Object.keys(MODEL.teams[lg]);
 for(let i=0;i<ts.length;i++)for(let j=0;j<ts.length;j++){if(i===j)continue;
 const r=rateFixture(lg,ts[i],ts[j]); if(r.error)continue; n++;
 const es=r.expScore;
 if(es.home!==es.away && ((r.H>r.A)!==(es.home>es.away))) bad++;
 if(Math.abs(r.markets.dnb-r.H/(r.H+r.A))>1e-9) dnb++;
 const k=r.markets; if(!(k.o15>=k.o25-1e-9&&k.o25>=k.o35-1e-9)) mono++;}}
 return [n,bad,dnb,mono].join(',');})()`).split(',');
ok(prov[1]==='0',prov[0]+" fixtures: expected scoreline never contradicts 1X2 lean");
ok(prov[2]==='0',"DNB always consistent with corrected H/A");
ok(prov[3]==='0',"over/under monotone despite uncorrected grid");

console.log("\n### PART A — LAYER DISCIPLINE ###");
const rf=src.slice(src.indexOf('function rateFixture'),src.indexOf('function teamRecord'));
ok(rf.indexOf('const gg = goalsGrid')<rf.indexOf('Star draw correction'),
   "goals markets computed BEFORE star correction (documented)");
ok(rf.indexOf('lines.push')<rf.indexOf('Star draw correction'),
   "scorelines computed BEFORE star correction (documented)");
ok(rf.indexOf('Star draw correction')<rf.indexOf('tierFor(H)'),
   "tier computed AFTER star correction");

console.log(`\n=== ENGINE SPEC: ${P} passed, ${F} failed ===`);
process.exit(F?1:0);
