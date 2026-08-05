import re
p='/home/user/app-v2.6-cross.html'
s=open(p).read()
orig=s

GOALS_FN = '''
/* EV-G2 evidence goals estimate — CALIBRATION-6. Results-only, causal (date<cutoff),
   display-only: never feeds the zone, agreement, gates or confidence.
   est = w*EV + (1-w)*B0 with w = npaths/(npaths+10): per-side weighted mean of total
   goals in matches touching each side (path-id weights, max-wins dedupe), B0 = rolling
   store mean <cutoff. Replay 633: MAE 1.301 (beats EV raw 1.315, B0 flat 1.323,
   last-10 1.325). Regions calibrated on same replay:
   LOW <2.40 (n=72): act 2.32, U2.5 59.7%, draw 26%; MID (n=341): act 2.55, 50/50;
   HIGH >=2.80 (n=220): act 3.01, O1.5 82%, O2.5 55%. */
var EVG2_K=10, EVG2_LO=2.40, EVG2_HI=2.80;
var EVG2_TABLE={
  LOW:{n:72, act:2.32, o15:65, u25:60, o25:40, o35:17, draw:26, txt:"under 2.5 landed 59.7% (n=72) · draw 26%"},
  MID:{n:341,act:2.55, o15:72, u25:50, o25:50, o35:25, draw:22, txt:"2.5 line is a true coin-flip (n=341) - no totals edge"},
  HIGH:{n:220,act:3.01, o15:82, u25:45, o25:55, o35:35, draw:28, txt:"over 1.5 landed 82% · over 2.5 55% (n=220)"}};
function evidenceGoalsEstimate(paths, hid, aid, cutoff){
  if (typeof BlueprintEmbed === "undefined" || !BlueprintEmbed.store) return null;
  var ms = (BlueprintEmbed.store().matches)||[];
  var byId={}; ms.forEach(function(m){ byId[m.id]=m; });
  var hM={}, aM={};
  (paths||[]).forEach(function(p){
    var w=p.weight||1;
    (p.ids||[]).forEach(function(id){
      var m=byId[id]; if(!m) return; var t=(+m.hg)+(+m.ag);
      if(m.homeId===hid||m.awayId===hid){ if(!hM[id]||w>hM[id].w) hM[id]={w:w,t:t}; }
      if(m.homeId===aid||m.awayId===aid){ if(!aM[id]||w>aM[id].w) aM[id]={w:w,t:t}; }
    });
  });
  function meanOf(map){ var sw=0,st=0,k; for(k in map){sw+=map[k].w;st+=map[k].w*map[k].t;} return sw?st/sw:null; }
  var evh=meanOf(hM), eva=meanOf(aM);
  var ev = (evh!==null&&eva!==null)?(evh+eva)/2:(evh!==null?evh:eva);
  var c0=0,sg=0;
  ms.forEach(function(m){ if(m.date<cutoff){c0++;sg+=(+m.hg)+(+m.ag);} });
  if(!c0) return null;
  var b0=sg/c0;
  if(ev===null) ev=b0;
  var np=(paths&&paths.length)||0, w=np/(np+EVG2_K);
  var est=w*ev+(1-w)*b0;
  var region = est<EVG2_LO ? "LOW" : est>=EVG2_HI ? "HIGH" : "MID";
  return {est:est, region:region, ev:ev, b0:b0, w:w, npaths:np};
}
function evidenceGoalsHtml(hp, ap, paths, hid, aid, cutoff){
  var g=evidenceGoalsEstimate(paths, hid, aid, cutoff);
  if(!g) return "";
  var R=EVG2_TABLE[g.region];
  return '<div class="help" style="margin:10px 0 0"><b>Total goals read (evidence-calibrated)</b> - display-only, never feeds the zone. '+
    'Measured on the 633-game masked replay (CALIBRATION-6); shares are replay hit-rates, not win probabilities.</div>'+
    '<div class="kv" style="margin:2px 0 0"><span class="k">Estimated total goals</span><span><b>'+g.est.toFixed(2)+'</b>'+
    ' &nbsp;<b>'+g.region+'</b> region &nbsp;<span class="help">(replay mean '+R.act.toFixed(2)+' · '+R.txt+'; O1.5 '+R.o15+'% · U2.5 '+R.u25+'% · O2.5 '+R.o25+'% · O3.5 '+R.o35+'%)</span></span></div>';
}
'''

# 1) insert the functions before gapAuditRequestsHtml definition
anchor = "function gapAuditRequestsHtml(hp, ap, paths, ag, hid, aid, cutoff, zinfo) {"
assert anchor in s, "anchor missing"
s = s.replace(anchor, GOALS_FN.strip()+"\n"+anchor, 1)

# 2) render call right before the requests card
call_old = "    gapAuditRequestsHtml(hp, ap, paths, ag, hid, aid, cutoff, zinfoMain) +"
call_new = "    evidenceGoalsHtml(hp, ap, paths, hid, aid, cutoff) +\n    gapAuditRequestsHtml(hp, ap, paths, ag, hid, aid, cutoff, zinfoMain) +"
assert call_old in s, "call anchor missing"
s = s.replace(call_old, call_new, 1)

# 3) version bump
assert "v2.8.4-cross" in s
s = s.replace("v2.8.4-cross","v2.8.5-cross")
open(p,'w').write(s)
print("edits applied; version occurrences v2.8.5-cross:", s.count("v2.8.5-cross"))
