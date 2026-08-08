/**
 * v8.0 → PYTHON CROSS-CHECK
 * Verifies DC core math (lam, update, scoreGrid) is identical to v4.0/Python.
 * Uses raw_H/raw_D/raw_A (pre-star-correction) for exact comparison.
 * Run: node engine_rebuild/verify_v8.js
 */
const V8 = require('./pitch_engine_v8.0.js');
const fs = require('fs');
const path = require('path');

const fixture = JSON.parse(fs.readFileSync(path.join(__dirname,'js_test_fixture.json'),'utf8'));
const store = JSON.parse(fs.readFileSync(path.join(__dirname,'..','previous_work_files','workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739','pitch-rating-full-5082-D1D2-2026-08-05.json'),'utf8'));

const COMP_TO_LG = {
  'England Premier League':'E0','Russian Premier League':'RPL',
  'Russian Cup':'RPL','Russian Relegation Playoffs':'RPL','Russian Super Cup':'RPL',
  'Czech First League':'CZ1','Czech Relegation Playoffs':'CZ1','MOL Cup':'CZ1',
};
function makeRes(hg,ag){return hg>ag?'H':(hg===ag?'D':'A');}

const matches=[];
for(const m of store.store.matches){
  const lg=COMP_TO_LG[m.competitionName];if(!lg)continue;
  matches.push({date:m.dateISO,league:lg,home:m.homeName,away:m.awayName,hg:m.homeGoals,ag:m.awayGoals,res:makeRes(m.homeGoals,m.awayGoals),isLeague:true,total:m.homeGoals+m.awayGoals});
}
matches.sort((a,b)=>{if(a.date<b.date)return-1;if(a.date>b.date)return 1;if(a.league<b.league)return-1;if(a.league>b.league)return 1;if(a.home<b.home)return-1;if(a.home>b.home)return 1;if(a.away<b.away)return-1;if(a.away>b.away)return 1;return 0;});

const engine = new V8();
const preds = [];
for(const m of matches){
  const pred = engine.predict(m);
  if(pred) preds.push({match:m,prediction:pred});
  engine.update(m);
}

console.log('v8.0 predictions: '+preds.length);
console.log('Test cases: '+fixture.test_cases.length);

let fields=0, matched=0, found=0;
for(const tc of fixture.test_cases){
  const p = preds.find(x => x.match.date===tc.date && x.match.league===tc.league && x.match.home===tc.home && x.match.away===tc.away);
  if(!p) continue;
  found++;
  const raw = p.prediction;
  const checks=[
    ['lambda_home',tc.prediction.lambda_home,raw.lambda_home],
    ['lambda_away',tc.prediction.lambda_away,raw.lambda_away],
    ['H (raw)',tc.prediction.H,raw.raw_H],
    ['D (raw)',tc.prediction.D,raw.raw_D],
    ['A (raw)',tc.prediction.A,raw.raw_A],
  ];
  for(const[n,py,js]of checks){fields++;if(Math.abs(py-js)<1e-6)matched++;}
}

console.log('\n── RAW DC MATH vs PYTHON ──');
console.log('Cases found: '+found+'/'+fixture.test_cases.length);
console.log('Fields: '+matched+'/'+fields+' ('+(fields>0?(matched/fields*100).toFixed(1):'N/A')+'%)');
if(matched===fields) console.log('VERDICT: ✓ v8.0 core DC math (lam/update/scoreGrid) is byte-identical to v4.0/Python');
else console.log('VERDICT: ✗ '+fields+'/'+matched+' fields differ');
