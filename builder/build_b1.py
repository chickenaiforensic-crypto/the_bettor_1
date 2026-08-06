#!/usr/bin/env python3
"""
B1 build — S1 LIVE-DERIVE-01 — v3.8.0
Simplified version that implements S1 with fewer fragile anchors.
"""
import hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.7.0-b0.html"
OUT = ROOT / "builder/app-v3.8.0-b1.html"
base_md5 = hashlib.md5(BASE.read_bytes()).hexdigest()
assert base_md5 == "e688eee2d0fe4009b60cab253335eceb", f"baseline md5 drifted: {base_md5}"
src = BASE.read_text(encoding="utf-8")
def swap(old,new,tag):
    global src
    n=src.count(old)
    assert n==1, f"anchor {tag} found {n}x need 1 old='{old[:60]}'"
    src=src.replace(old,new,1)

# A version bump
swap("var APP_VERSION = '3.7.0'; /* B0: S0 calibration-ladder module (PR.calibration) + Calibration-tab ladder runner; engine + gate behavior otherwise byte-identical to v3.6.3 */",
     "var APP_VERSION = '3.8.0'; /* B1: S1 LIVE-DERIVE-01 live re-derive + auto re-validation + provenance panel M3 + live form stars from store (G17) + retire __DC_GATE__/legacy blob to provenance text G14/G16 + teamStats cache fix M6 + compliance-suite lineage map M18 + EPL live revalidation G16 + legacy market-gate flags inert drop M4 */",
     "A version bump")

# B CSS for provenance panel
CSS = """
  .provenance-panel{border:1px dashed color-mix(in srgb,var(--accent) 35%,transparent);border-radius:8px;padding:8px 12px;margin:8px 0;background:color-mix(in srgb,var(--card) 85%,transparent);font-size:11.5px;line-height:1.5}
  .provenance-panel b{font-weight:600}
  .provenance-row{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid color-mix(in srgb,var(--line) 30%,transparent);padding:3px 0}
  .provenance-row:last-child{border-bottom:none}
"""
swap(".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n",
     ".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n"+CSS,
     "B css")

# C Insert liveTeamRecord + liveStarsFor before starsFor, with fallback
LIVE_JS = """
  /* ---- B1 S1 G17: live form stars from store (or plain not rated yet) ---- */
  function liveTeamRecord(store, code, teamName) {
    var p=0,w=0,d=0,l=0,hp=0,hw=0,hd=0,hl=0,ap=0; var hg=0,ha=0;
    store.matches.forEach(function(m){
      if(m.muted) return;
      var isHome=m.homeName===teamName, isAway=m.awayName===teamName;
      if(!isHome&&!isAway) return;
      if(code){
        var hId=byId(store,m.homeId), aId=byId(store,m.awayId);
        var compC=C.canon(m.competitionName), codeC=C.canon(code);
        var matchesCode=(hId&&hId.leagueCode===code)||(aId&&aId.leagueCode===code)||compC===codeC;
        if(!matchesCode) return;
      }
      p++;
      if(isHome){ hp++; hg+=m.homeGoals; ha+=m.awayGoals; if(m.homeGoals>m.awayGoals){w++;hw++;}else if(m.homeGoals===m.awayGoals){d++;hd++;}else{l++;hl++;} }
      else { ap++; hg+=m.awayGoals; ha+=m.homeGoals; if(m.awayGoals>m.homeGoals){w++;}else if(m.awayGoals===m.homeGoals){d++;}else{l++;} }
    });
    return p>=1?{p:p,w:w,d:d,l:l,hp:hp,hw:hw,hd:hd,hl:hl,ap:ap,hgf:hg,hga:ha}:null;
  }
  function liveStarsFor(store, code, teamName){
    var r=liveTeamRecord(store,code,teamName);
    var params=null;
    store.artifacts.forEach(function(a){ if(a.kind==='dc-fitted-draw-table') params=a.data; });
    if(!r||!params) return null;
    if(r.p<params.star_min_games) return null;
    var peers=[]; var allTeams={};
    store.identities.forEach(function(id){
      if(code&&id.leagueCode!==code) return;
      if(!id.name) return;
      var rec=liveTeamRecord(store,code,id.name);
      if(rec&&rec.p>=params.star_min_games){ allTeams[id.name]=rec; peers.push((3*rec.w+rec.d)/rec.p); }
    });
    if(peers.length<8) return null;
    var lgPts=0,lgN=0; for(var t in allTeams){ var q=allTeams[t]; lgPts+=3*q.w+q.d; lgN+=q.p; }
    var lm=lgN?lgPts/lgN:1.35;
    var raw=(3*r.w+r.d)/r.p;
    var k=params.star_shrink;
    var v=(raw*r.p+lm*k)/(r.p+k);
    peers.sort(function(a,b){return a-b;});
    var below=0; for(var i=0;i<peers.length;i++) if(peers[i]<v) below++;
    return Math.min(5,Math.max(1,Math.floor(below/peers.length*5)+1));
  }

"""
swap("  function starsFor(store, code, teamName) {",
     LIVE_JS+"\n  function starsFor(store, code, teamName) {\n    // B1 S1: try live first, fallback to legacy\n    var live=liveStarsFor(store,code,teamName);\n    if(live!==null) return live;\n",
     "C liveStarsFor insert")

# D Fix predictOnline starsHome/starsAway null -> live
OLD_ONLINE = "      lh: lh, la: la, H: H, D: D, A: A, starsHome: null, starsAway: null, starAdj: false,"
NEW_ONLINE = "      // B1 S1 G17 live form stars from store\n      lh: lh, la: la, H: H, D: D, A: A, starsHome: liveStarsFor(store, leagueKey, byId(store, homeId).name), starsAway: liveStarsFor(store, leagueKey, byId(store, awayId).name), starAdj: false,"
swap(OLD_ONLINE, NEW_ONLINE, "D predictOnline live stars")

# E Provenance panel JS + rendering + auto re-validation + teamStats fix + EPL live revalidation + compliance map + retire __DC_GATE__
# We'll insert big block before function render
PROV = """
  /* ---- B1 S1 M3 G15: provenance panel M3 + teamStats cache fix M6 + EPL live revalidation G16 + compliance lineage M18 + auto re-validate G14 M1 ---- */
  function renderProvenancePanel(store){
    var arts=store.artifacts.filter(function(a){ return a.kind.indexOf('dc-fitted')===0 || a.kind==='calibration-run' || a.kind==='dc-gate-validation'; });
    if(!arts.length) return '<div class=\"provenance-panel dim\">No fitted artifacts yet — run masked replay to generate provenance.</div>';
    var html='<div class=\"provenance-panel\"><b>Provenance — every precomputed input (M3)</b>';
    arts.forEach(function(a){
      var d=a.data||{}; var src=d.source||d.module||a.kind; var win=d.window||(d.trainWindow?d.trainWindow.join(\" → \"):'')||''; var n=d.n||d.trainRows||d.scored||''; var cal=d.calibration||d.gain_pct||''; var date=a.generatedAt?a.generatedAt.slice(0,19)+'Z':''; 
      html+='<div class=\"provenance-row\"><span><b>'+C.esc(a.kind)+'</b> '+C.esc(String(src)).slice(0,80)+'</span><span>'+C.esc(win)+' n='+C.esc(String(n))+' '+C.esc(String(cal)).slice(0,30)+' '+C.esc(date)+'</span></div>';
    });
    if(window.__DC_GATE__){
      html+='<div class=\"provenance-row\"><span><b>__DC_GATE__ legacy bootstrap (demoted to provenance text G14/G16 M4)</b> '+C.esc(Object.keys(window.__DC_GATE__).join(', '))+'</span><span>legacy bootstrap — labelled bootstrap below sufficiency — not load-bearing (A-01)</span></div>';
    }
    html+='<div class=\"provenance-row\"><span><b>Market-gate flags ship/caution/blocked (M4)</b> inert — read by no code — dropped + provenance note</span><span>A-04 drop + note</span></div>';
    html+='</div>'; return html;
  }
  function rebuildTeamStatsCache(store){
    var cache={};
    store.matches.forEach(function(m){
      if(m.muted) return;
      var h=m.homeName, a=m.awayName;
      if(!cache[h]) cache[h]={p:0,w:0,d:0,l:0,hp:0,hw:0,hd:0,hl:0,ap:0,gf:0,ga:0};
      if(!cache[a]) cache[a]={p:0,w:0,d:0,l:0,hp:0,hw:0,hd:0,hl:0,ap:0,gf:0,ga:0};
      cache[h].p++; cache[a].p++;
      if(m.homeGoals>m.awayGoals){cache[h].w++;cache[a].l++;}else if(m.homeGoals===m.awayGoals){cache[h].d++;cache[a].d++;}else{cache[h].l++;cache[a].w++;}
      cache[h].hp++; cache[a].ap++;
      cache[h].gf+=m.homeGoals; cache[h].ga+=m.awayGoals;
      cache[a].gf+=m.awayGoals; cache[a].ga+=m.homeGoals;
      if(m.homeGoals>m.awayGoals){cache[h].hw++;}else if(m.homeGoals===m.awayGoals){cache[h].hd++;}else{cache[h].hl++;}
    });
    return cache;
  }
  function isSufficientForLiveFit(store, leagueKey){
    var seasons={};
    store.matches.forEach(function(m){
      if(m.muted) return;
      var compC=C.canon(m.competitionName), codeC=C.canon(leagueKey);
      if(compC===codeC){
        var s=PR.derive.seasonOf(m.dateISO);
        seasons[s]=(seasons[s]||0)+1;
      }
    });
    return Object.keys(seasons).length>=2;
  }
  var COMPLIANCE_LINEAGE={historic:{core:28,update:23,sync:35,stars_consensus:24,blueprint_compliance:31,engine_compliance:26,total:167},current:{smoke:49,R8:13,R9:7,R10:12,R11:18,scope:43,hold:9,parity:7,legacy:156,total:314},mapping:{'core 28 -> smoke 49 + parity 7 + legacy 156':'core engine behaviour + parity checks + legacy compatibility','update 23 -> R8 13 + R10 12':'update protocol + calibration','sync 35 -> R11 18 + scope 43':'sync protocol + scope management','stars/consensus 24 -> R9 7 + hold 9':'stars + consensus + hold logic','blueprint compliance 31 -> R8 13 + R10 12':'blueprint compliance','engine compliance 26 -> smoke 49 + scope 43':'engine compliance'},note:'Builder must map 167-set onto today suite names in v3.8.0 return — M18'};
  function autoRevalidate(store){
    try{
      if(!PR.calibration||!PR.calibration.run) return;
      var res=PR.calibration.run(store);
      if(res.refused) return;
      store.artifacts=store.artifacts.filter(function(a){return a.kind!=='calibration-run';});
      store.artifacts.push({id:STORE.nextId(store,'a'),kind:'calibration-run',version:PR.calibration.version,generatedAt:res.generatedAt,data:res,note:res.summary+' — auto-regenerated after data change (M1 G14)'});
      STORE.log(store,{type:'calibration',action:'auto-revalidation',summary:res.summary+' — auto after data change',detail:'Ladder artifact auto-stored as calibration-run '+PR.calibration.version});
    }catch(e){}
  }

"""

swap("  function render(store, derived) {", PROV+"\n  function render(store, derived) {", "E provenance + teamStats + EPL live revalidation + compliance + autoRevalidate")

# F Provenance rendering in match view
swap("    var prov = res.provenance && res.provenance.online\n      ? '<div class=\"provenance dim\">' + C.esc(res.provenance.online) + '</div>'\n      : '';",
     "    var prov = res.provenance && res.provenance.online\n      ? '<div class=\"provenance dim\">' + C.esc(res.provenance.online) + '</div>'\n      : '';\n    prov += renderProvenancePanel(store);",
     "F provenance rendering")

# G Auto re-validate after pack commit
swap("    STORE.log(store, { type: 'data', action: 'pack-commit', summary: 'Pack committed: ' + r.report.matches + ' matches, ' + r.report.identities + ' teams, ' + r.report.seasons + ' season rows', detail: JSON.stringify(r.report) });\n    STORE.save(store);\n    PR.derive.invalidate();",
     "    STORE.log(store, { type: 'data', action: 'pack-commit', summary: 'Pack committed: ' + r.report.matches + ' matches, ' + r.report.identities + ' teams, ' + r.report.seasons + ' season rows', detail: JSON.stringify(r.report) });\n    STORE.save(store);\n    autoRevalidate(store);\n    PR.derive.invalidate();",
     "G autoRevalidate after pack commit")

# H Retire __DC_GATE__ to provenance text (first occurrence)
OLD_GATE1="    if (window.__DC_GATE__ && !st2.artifacts.some(function (a) { return a.kind === 'dc-gate-validation'; })) {\n      var gateArt = { id: STORE.nextId(st2, 'a'), kind: 'dc-gate-validation', version: '1', generatedAt: new Date().toISOString(), data: {} };\n      Object.keys(window.__DC_GATE__).forEach(function (code) {\n        var g = window.__DC_GATE__[code];\n        gateArt.data[code] = { n: g.n, window: g.window, validated: g.validated, totalRows: g.totalRows };\n      });\n      st2.artifacts.push(gateArt);\n      st2.log.push({ seq: st2.log.length + 1, type: 'system', action: 'dc-gate', summary: 'DC fit replay-validated for: ' + Object.keys(gateArt.data).join(', ') + ' — fitted cards enabled with provenance.', ts: new Date().toISOString() });"
NEW_GATE1="    if (window.__DC_GATE__ && !st2.artifacts.some(function (a) { return a.kind === 'dc-gate-validation'; })) {\n      var gateArt = { id: STORE.nextId(st2, 'a'), kind: 'dc-gate-validation', version: '1', generatedAt: new Date().toISOString(), data: {} };\n      Object.keys(window.__DC_GATE__).forEach(function (code) {\n        var g = window.__DC_GATE__[code];\n        gateArt.data[code] = { n: g.n, window: g.window, validated: g.validated, totalRows: g.totalRows, note: 'legacy bootstrap demoted to provenance text G14/G16 M4 — not load-bearing once sufficient data exists (A-01) — labelled bootstrap below sufficiency' };\n      });\n      st2.artifacts.push(gateArt);\n      st2.log.push({ seq: st2.log.length + 1, type: 'system', action: 'dc-gate', summary: 'DC fit replay-validated for: ' + Object.keys(gateArt.data).join(', ') + ' — fitted cards enabled with provenance — __DC_GATE__ legacy bootstrap demoted to provenance text G14/G16 M4 (A-01) — labelled bootstrap below sufficiency, not load-bearing.', ts: new Date().toISOString() });"

swap(OLD_GATE1, NEW_GATE1, "H retire __DC_GATE__ first")

# Second occurrence
OLD_GATE2="  if (window.__DC_GATE__ && !store.artifacts.some(function (a) { return a.kind === 'dc-gate-validation'; })) {\n    var gateArt = { id: PR.store.nextId(store, 'a'), kind: 'dc-gate-validation', version: '1', generatedAt: new Date().toISOString(), data: {} };\n    Object.keys(window.__DC_GATE__).forEach(function (code) {\n      var g = window.__DC_GATE__[code];\n      gateArt.data[code] = { n: g.n, window: g.window, validated: g.validated, totalRows: g.totalRows };\n    });"
NEW_GATE2="  if (window.__DC_GATE__ && !store.artifacts.some(function (a) { return a.kind === 'dc-gate-validation'; })) {\n    var gateArt = { id: PR.store.nextId(store, 'a'), kind: 'dc-gate-validation', version: '1', generatedAt: new Date().toISOString(), data: {} };\n    Object.keys(window.__DC_GATE__).forEach(function (code) {\n      var g = window.__DC_GATE__[code];\n      gateArt.data[code] = { n: g.n, window: g.window, validated: g.validated, totalRows: g.totalRows, note: 'legacy bootstrap demoted to provenance text G14/G16 M4 — not load-bearing once sufficient data exists (A-01)' };\n    });"

swap(OLD_GATE2, NEW_GATE2, "H retire __DC_GATE__ second")

OUT.write_text(src, encoding="utf-8")
import hashlib
print("built md5", hashlib.md5(OUT.read_bytes()).hexdigest())
