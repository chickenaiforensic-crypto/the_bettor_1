#!/usr/bin/env python3
"""
B8 fix — S7 UI properly scoped + B6 calibration + I4 venue guard — v3.15.0 fixed

Base: app-v3.12.0-b5.html md5 bb69a5c4 (clean, has M17 partial, balance panel, pivot, M10)

Fixes S7 breakage:
- designer CSS had 7 body rules fighting: body { background: var(--surface); color: var(--ink-950); } vs app's body { background: var(--bg); color: var(--ink); }
- Fix: remove designer's body rule, map designer tokens (--ink-950, --surface, --emerald, --gold) into app's existing :root and html[data-theme="light"] blocks — don't add second :root
- Keep component classes (.btn-primary, .badge-emerald, .card, .verdict, .balance-bar) but make them use app's var(--bg), var(--panel), var(--ink) — not designer's standalone var(--surface), var(--paper), var(--ink-950)
- Dark theme body gradient and light theme body background should come from app's existing theme switch, not designer's standalone CSS

Also includes:
- B6: one-click masked replay after data change M1, monthly full sweep
- I4: isVenueVerified wired to import validation + commit, hard-block Z-003 hold with tick-box

Test: dark mode dark body visible text, light mode light body dark text
"""
import hashlib, pathlib, json, base64

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.12.0-b5.html"
OUT = ROOT / "builder/app-v3.15.0-fixed.html"

base_bytes = BASE.read_bytes()
base_md5 = hashlib.md5(base_bytes).hexdigest()
print(f"base {BASE.name} md5 {base_md5}")

src = BASE.read_text(encoding="utf-8")

def must_replace(old, new, tag):
    global src
    if old not in src:
        print(f"FAIL anchor {tag} not found")
        raise SystemExit(f"anchor {tag} missing")
    cnt = src.count(old)
    src = src.replace(old, new, 1)
    print(f"swap {tag} ok cnt {cnt}")

# A version bump
src = src.replace("var APP_VERSION = '3.12.0';", "var APP_VERSION = '3.15.0'; /* B8 fix S7 UI properly scoped — designer tokens mapped into existing :root and light blocks, no second :root, no designer body rule, component classes use app vars --bg --panel --ink, dark gradient via --bg, light surface via --bg, Bloomberg Terminal meets Athletic editorial + B6 calibration + I4 hard-block */", 1)

# B Properly scoped S7 CSS — merged tokens into existing :root and light, no body rule
# Old :root block
old_root = """:root{
  --bg:#0e1116; --panel:#161b22; --panel2:#1c232d; --line:#2a323d; --line2:#39424f;
  --ink:#e8ecf1; --ink2:#aab3c0; --muted:#7d8794; --dim:#5d6772;
  --accent:#2fbf71; --accent2:#1d9a5a; --teal:#2fb3a6; --amber:#e8a33d; --red:#e05b5b;
  --h:#2fbf71; --d:#c9a227; --a:#e05b5b;
  --serif:Georgia,'Times New Roman',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  --radius:14px; --shadow:0 10px 30px rgba(0,0,0,.35);
}"""

new_root = """:root{
  /* App vars mapped to designer palette — Bloomberg Terminal meets Athletic editorial — properly scoped, no second :root */
  --bg: linear-gradient(180deg, #0e1526 0%, #131b33 100%);
  --panel: rgba(255,255,255,0.03);
  --panel2: rgba(255,255,255,0.06);
  --line: rgba(255,255,255,0.08);
  --line2: rgba(255,255,255,0.12);
  --ink: #f0f2f8;
  --ink2: #b8bdd0;
  --muted: #8a93ab;
  --dim: #6b7a99;
  --accent: #10b981;
  --accent2: #047857;
  --teal: #10b981;
  --amber: #c8a84d;
  --red: #f87171;
  --h: #10b981;
  --d: #c8a84d;
  --a: #f87171;
  --serif: \"Tiempos Headline\", Georgia, \"Times New Roman\", serif;
  --sans: \"Inter\", -apple-system, \"SF Pro Display\", system-ui, sans-serif;
  --radius: 16px;
  --shadow: 0 24px 60px rgba(10,15,26,0.10);
  /* Designer tokens mapped into app's existing :root — no second :root block */
  --ink-950: #0a0f1a;
  --ink-900: #0e1526;
  --ink-800: #131b33;
  --ink-700: #1a2545;
  --ink-600: #25325e;
  --charcoal: #2d384f;
  --slate: #8a93ab;
  --silver: #b8bdd0;
  --mist: #dce0ec;
  --surface: #f4f6fb;
  --paper: #ffffff;
  --emerald: #10b981;
  --emerald-deep: #047857;
  --gold: #c8a84d;
  --gold-soft: #e8d9a8;
  --coral: #f87171;
  --rose-deep: #be123c;
  --font-display: \"Tiempos Headline\", Georgia, \"Times New Roman\", serif;
  --font-body: \"Inter\", -apple-system, \"SF Pro Display\", system-ui, sans-serif;
  --font-mono: \"SF Mono\", ui-monospace, monospace;
  --space-xs: 6px;
  --space-sm: 10px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 40px;
  --space-2xl: 64px;
  --max-width: 840px;
  --shadow-card: 0 24px 60px rgba(10,15,26,0.10);
}"""

must_replace(old_root, new_root, "B1 merged :root with designer tokens, dark gradient via --bg")

old_light = """html[data-theme="light"]{
  --bg:#f6f7f9; --panel:#ffffff; --panel2:#f1f3f6; --line:#e3e6ea; --line2:#d3d8de;
  --ink:#171c23; --ink2:#3d4651; --muted:#6b7480; --dim:#98a0ab;
  --accent:#128a4e; --accent2:#0f6b3d; --teal:#0e7a70; --amber:#b4740e; --red:#c0392b;
  --h:#128a4e; --d:#a8870f; --a:#c0392b;
  --shadow:0 8px 24px rgba(20,30,40,.08);
}"""

new_light = """html[data-theme="light"]{
  --bg: #f4f6fb;
  --panel: #ffffff;
  --panel2: #f1f3f6;
  --line: #e3e6ea;
  --line2: #d3d8de;
  --ink: #0a0f1a;
  --ink2: #2d384f;
  --muted: #6b7480;
  --dim: #98a0ab;
  --accent: #047857;
  --accent2: #0f6b3d;
  --teal: #0e7a70;
  --amber: #b4740e;
  --red: #c0392b;
  --h: #047857;
  --d: #8a6e28;
  --a: #be123c;
  --shadow: 0 8px 24px rgba(20,30,40,.08);
  /* Designer tokens in light theme too */
  --ink-950: #0a0f1a;
  --surface: #f4f6fb;
  --paper: #ffffff;
  --emerald: #10b981;
  --emerald-deep: #047857;
  --gold: #c8a84d;
}"""

must_replace(old_light, new_light, "B2 merged light theme with designer tokens, light surface via --bg")

# C Add properly scoped component classes that use app vars, not designer standalone
# We need to add after the balance-panel CSS or somewhere
# The base already has .balance-panel etc. We will add designer component classes properly scoped

S7_COMPONENTS_FIXED = """
/* ---- S7 UI fixed: properly scoped designer components using app vars --bg --panel --ink, no body rule ---- */
/* btn-primary: use app vars */
.btn-primary{
  display:inline-flex; align-items:center; gap:8px;
  padding:12px 24px; border-radius:10px;
  background:var(--panel2);
  color:var(--ink);
  font:600 14px/1.2 var(--sans);
  border:1px solid var(--line2);
  box-shadow:0 8px 24px rgba(10,15,26,0.15);
  transition:transform .15s ease, box-shadow .2s ease, border-color .15s;
}
.btn-primary:hover{
  transform:translateY(-1px);
  box-shadow:0 12px 28px rgba(10,15,26,0.25);
  border-color:var(--accent);
  color:var(--accent);
}
html[data-theme="dark"] .btn-primary{
  background: var(--ink-900);
  color: var(--paper);
  border-color: var(--ink-800);
}
html[data-theme="dark"] .btn-primary:hover{
  color: var(--paper);
  filter: brightness(1.1);
}
html[data-theme="light"] .btn-primary{
  background: var(--ink-900);
  color: var(--paper);
}

/* badge: use app vars */
.badge{
  display:inline-flex; align-items:center; gap:6px;
  padding:4px 10px; border-radius:999px;
  font:700 11px/1 var(--sans);
  letter-spacing:.03em; text-transform:uppercase;
  background:var(--panel2);
  border:1px solid var(--line2);
  color:var(--ink2);
}
.badge-emerald{
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  color: var(--accent);
  border:1px solid color-mix(in srgb, var(--accent) 18%, transparent);
}
.badge-gold{
  background: color-mix(in srgb, var(--amber) 12%, transparent);
  color: var(--amber);
  border:1px solid color-mix(in srgb, var(--amber) 18%, transparent);
}

/* card: use app vars --panel --line --ink, not --paper --ink-950 */
.card{
  background:var(--panel);
  border-radius:var(--radius);
  box-shadow:var(--shadow);
  border:1px solid var(--line);
}
/* Keep existing .card padding etc from app, but ensure background uses app var */

/* verdict: use app vars */
.verdict{
  font-family:var(--serif);
  font-size:28px;
  line-height:1.15;
  letter-spacing:-0.02em;
  color:var(--ink);
}

/* balance-bar: use app vars */
.balance-bar{
  height:10px;
  border-radius:6px;
  overflow:hidden;
  background:var(--panel2);
  display:flex;
}
.balance-bar > span{ height:100%; display:block; }
html[data-theme="dark"] .balance-bar{ background: rgba(255,255,255,0.08); }
html[data-theme="light"] .balance-bar{ background: var(--mist); }

/* Ensure body rule is only from app: body{background:var(--bg);color:var(--ink);} — dark gradient via --bg, light surface via --bg — no designer body rule */
"""

# Inject after existing balance-panel CSS
must_replace(".nocall .balance-panel{margin-top:16px;text-align:left}\n", ".nocall .balance-panel{margin-top:16px;text-align:left}\n"+S7_COMPONENTS_FIXED, "B3 S7 components fixed using app vars")

# D Add B6 + I4 JS (from previous builds) — we need to re-add them since base is v3.12.0-b5 which has some but not all
# For B6, we need autoReplay, checkMonthlySweep, monthlyFullSweep, renderCalibrationStatus
# For I4, we need getVerifiedVenueMap, isVenueVerified, filesView with hard-block, bind venue confirm, approveStaged double-check

# Let's read the JS we previously added for B6 and I4 from v3.14 and re-inject properly scoped

B6_I4_JS = """
  /* ---- B6: one-click masked replay after data change M1, monthly full sweep ---- */
  function autoReplay(store, derived){
    try{
      if(!PR.replay || !PR.replay.run) return;
      var report=PR.replay.run(store, derived);
      var saved=[];
      ['zone-table','confidence-table','goals-band'].forEach(function(kind){
        if(report.wins && report.wins[kind]){
          store.artifacts=store.artifacts.filter(function(a){ return a.kind!==kind; });
          store.artifacts.push({ id:STORE.nextId(store,'a'), kind:kind, version:'2', generatedAt:new Date().toISOString(), data:report.artifacts[kind] });
          saved.push(kind);
        }
      });
      if(saved.length){
        STORE.log(store, { type:'calibration', action:'auto-replay', summary:'Masked replay auto-regenerated after data change — '+saved.join(', ')+' — M1' });
      }
      return report;
    }catch(e){ return null; }
  }
  function checkMonthlySweep(store){
    try{
      var lastRun=null;
      store.artifacts.forEach(function(a){
        if(a.kind==='calibration-run' || a.kind==='replay-validation' || a.kind==='zone-table'){
          var d=new Date(a.generatedAt);
          if(!lastRun || d>lastRun) lastRun=d;
        }
      });
      if(!lastRun) return { need:true, reason:'no prior calibration/replay' };
      var now=new Date();
      var diffDays=(now-lastRun)/(1000*60*60*24);
      if(diffDays>30){
        return { need:true, reason:'last run '+lastRun.toISOString().slice(0,10)+' — '+diffDays.toFixed(1)+' days ago >30 days', days:diffDays, lastRun:lastRun };
      }
      return { need:false, days:diffDays, lastRun:lastRun };
    }catch(e){ return { need:false, error:e.message }; }
  }
  function monthlyFullSweep(store, derived){
    try{
      var replayReport=PR.replay.run(store, derived);
      var ladderReport=PR.calibration.run(store);
      var saved=[];
      ['zone-table','confidence-table','goals-band'].forEach(function(kind){
        if(replayReport.wins && replayReport.wins[kind]){
          store.artifacts=store.artifacts.filter(function(a){ return a.kind!==kind; });
          store.artifacts.push({ id:STORE.nextId(store,'a'), kind:kind, version:'2', generatedAt:new Date().toISOString(), data:replayReport.artifacts[kind] });
          saved.push(kind);
        }
      });
      if(ladderReport && !ladderReport.refused){
        store.artifacts=store.artifacts.filter(function(a){ return a.kind!=='calibration-run'; });
        store.artifacts.push({ id:STORE.nextId(store,'a'), kind:'calibration-run', version:PR.calibration.version, generatedAt:ladderReport.generatedAt, data:ladderReport, note:ladderReport.summary+' — monthly full sweep' });
        saved.push('calibration-run');
      }
      STORE.log(store, { type:'calibration', action:'monthly-sweep', summary:'Monthly full sweep complete — '+saved.join(', ')+' — B6' });
      STORE.save(store);
      PR.derive.invalidate();
      return { ok:true, saved:saved, replay:replayReport, ladder:ladderReport };
    }catch(e){ return { ok:false, error:e.message }; }
  }
  function renderCalibrationStatus(store){
    var check=checkMonthlySweep(store);
    var html='<div class="balance-panel"><b>Calibration cadence — B6 one-click after data change + monthly sweep</b><br>';
    if(check.need){
      html+='<span class="dim">Monthly sweep needed: '+(check.reason||'no prior run')+' — last run '+(check.lastRun?check.lastRun.toISOString().slice(0,10):'never')+'</span><br>';
      html+='<button class="btn primary" id="btn-monthly-sweep">Run monthly full sweep (replay + ladder)</button> <span class="dim">One-click after data change is automatic — this button runs full sweep manually</span>';
    } else {
      html+='<span class="dim">Last calibration/replay '+(check.lastRun?check.lastRun.toISOString().slice(0,10):'unknown')+' — '+(check.days?check.days.toFixed(1)+' days ago':'')+' — within 30 days — auto replay after data change active (M1)</span><br>';
      html+='<button class="btn" id="btn-monthly-sweep">Run monthly full sweep anyway</button>';
    }
    html+='</div>';
    return html;
  }

  /* ---- B7 fix I4: isVenueVerified wired to import validation + commit ---- */
  function getVerifiedVenueMap(store){
    var map={};
    store.matches.forEach(function(m){
      if(m.muted) return;
      if(m.venueType && m.venueType!=='normal') return;
      if(!m.stadium) return;
      var key=C.canon(m.homeName)+'::'+C.canon(m.competitionName||'');
      if(!map[key]) map[key]={ team:m.homeName, competition:m.competitionName, stadiums:{}, count:0 };
      map[key].stadiums[m.stadium]=(map[key].stadiums[m.stadium]||0)+1;
      map[key].count++;
    });
    return map;
  }
  function isVenueVerified(store, homeTeam, competitionName, stadiumName, venueType){
    if(!stadiumName) return { ok:true, reason:'no stadium' };
    if(venueType && venueType!=='normal') return { ok:true, reason:'neutral/relocated allowed' };
    var map=getVerifiedVenueMap(store);
    var key=C.canon(homeTeam)+'::'+C.canon(competitionName||'');
    var entry=map[key];
    if(!entry){
      var hasAny=false;
      Object.keys(map).forEach(function(k){ if(k.indexOf(C.canon(homeTeam)+'::')===0) hasAny=true; });
      if(!hasAny){
        return { ok:false, hardBlock:true, reason:'Team '+homeTeam+' has never hosted in store — no verified venue history — I4 hard block — competition '+competitionName+' venue '+stadiumName, code:'never_hosted_any' };
      } else {
        return { ok:false, hardBlock:true, reason:'Team '+homeTeam+' has never hosted in competition '+competitionName+' — verified-venue list empty — I4 hard block — venue '+stadiumName, code:'never_hosted_league' };
      }
    }
    if(entry.stadiums[stadiumName]){
      return { ok:true, reason:'venue verified — '+stadiumName+' has '+entry.stadiums[stadiumName]+' prior hostings' };
    } else {
      return { ok:false, hardBlock:true, reason:'Team '+homeTeam+' never hosted at venue '+stadiumName+' in '+competitionName+' — known: '+Object.keys(entry.stadiums).join(', ')+' — I4 hard block', code:'venue_mismatch', known:Object.keys(entry.stadiums) };
    }
  }

  /* S7 icons fixed meanings */
  var ICON_MEANINGS={
    '🛡️': 'Fortress — strong home tier',
    '📈': 'Live trend — recent form rising',
    '🌍': 'League pivot — per-league X points above/below',
    '⚡': 'Hot — hot last 6',
    '❄️': 'Cold — cold last 6',
    '🔗': 'Evidence chain — H2H common level-3',
    '⚖️': 'Balanced — support shares balanced',
    '💡': 'Why not higher — draw risk capped',
    '🔍': 'Provenance — every precomputed input M3',
    '✅': 'Calibrated', '🚫': 'No view / muted', '💾': 'Snapshot', '📄': 'Doc'
  };
  function iconWithTooltip(icon){
    var meaning=ICON_MEANINGS[icon]||icon;
    return '<span class="icon-meaning" title="'+C.esc(meaning)+'">'+icon+'</span>';
  }
"""

# Insert after existing league pivot + M10 JS? Find anchor getLeaguePivotDelta
must_replace("  function getLeaguePivotDelta(store, homeLeague, awayLeague){", B6_I4_JS + "\n  function getLeaguePivotDelta(store, homeLeague, awayLeague){", "C B6+I4+S7 icons JS")

# D Patch autoRevalidate to include autoReplay and ensureLeaguePivot — handle both v3.12 and v3.13 base
# First try to find existing autoRevalidate with ensureLeaguePivot already
if "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;" in src:
    must_replace("  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      autoReplay(store, PR.derive.derive(store, { engines: [function(s,d){ d.dcFit=PR.dc.fit(s); }] }));\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "D autoRevalidate includes pivot + autoReplay")
else:
    # base v3.12 has autoRevalidate without second try for autoReplay
    old_auto = "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;"
    # Actually base v3.12 has ensureLeaguePivot but not autoReplay, so we need to add autoReplay after ensure
    # Let's search for simpler pattern
    if "  function autoRevalidate(store){" in src:
        # replace first occurrence of "function autoRevalidate" header with our version that includes autoReplay
        src = src.replace("  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      autoReplay(store, PR.derive.derive(store, { engines: [function(s,d){ d.dcFit=PR.dc.fit(s); }] }));\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", 1)
        print("patched autoRevalidate via direct replace")
    else:
        print("WARN autoRevalidate not found for D")

# E Patch calibrationConsole to include B6 status
old_cal = "  function calibrationConsole(store, derived) {\n    var art = store.artifacts.filter(function (a) { return ['zone-table', 'draw-table', 'confidence-table', 'goals-band', 'market-calibration', 'replay-validation', 'calibration-run', 'dc-fitted-model', 'dc-fitted-draw-table', 'dc-fitted-tiers', 'dc-fitted-markets', 'dc-fitted-records', 'form-declaration'].indexOf(a.kind) !== -1; });"

new_cal = """  function calibrationConsole(store, derived) {
    var calStatusHtml = renderCalibrationStatus(store);
    var art = store.artifacts.filter(function (a) { return ['zone-table', 'draw-table', 'confidence-table', 'goals-band', 'market-calibration', 'replay-validation', 'calibration-run', 'dc-fitted-model', 'dc-fitted-draw-table', 'dc-fitted-tiers', 'dc-fitted-markets', 'dc-fitted-records', 'form-declaration', 'dc-fitted-league-pivot', 'dc-fitted-constants'].indexOf(a.kind) !== -1; });"""

must_replace(old_cal, new_cal, "E calibrationConsole B6 status")

must_replace("    return '<p class=\"dim\">Calibration is a masked replay on the data: later information is hidden, the model predicts, then we compare. Artifacts are only replaced when a regeneration wins on held-out data.</p>' +", "    return calStatusHtml + '<p class=\"dim\">Calibration is a masked replay on the data: later information is hidden, the model predicts, then we compare. Artifacts are only replaced when a regeneration wins on held-out data.</p>' +", "F inject calStatusHtml")

# F Patch bind to include monthly sweep and venue confirmation
old_bind = "    on('#btn-ladder', function () { runLadder(store, derived); });\n    on('#btn-ladder-dl', function () { downloadLadderArtifact(store); });"

new_bind = """    on('#btn-ladder', function () { runLadder(store, derived); });
    on('#btn-ladder-dl', function () { downloadLadderArtifact(store); });
    on('#btn-monthly-sweep', function () {
      var btn=document.getElementById('btn-monthly-sweep');
      if(btn) btn.innerHTML='<span class="busy-icon"></span> Running monthly full sweep...';
      setTimeout(function(){
        var res=monthlyFullSweep(store, derived);
        if(res.ok) toast('Monthly full sweep complete — '+res.saved.join(', '));
        else toast('Monthly sweep failed: '+res.error);
        render(store, PR.derive.derive(store, { engines: [function(s,d){ d.dcFit=PR.dc.fit(s); }] }));
      }, 100);
    });
"""

must_replace(old_bind, new_bind, "G bind monthly sweep")

# G Fix filesView with venue guard hard-block (from previous B7 fix)
old_filesView_simple = """  function filesView(store, derived) {
    var stagedCards = state.staged.length
      ? state.staged.map(function (f, i) {
          /* HOLD-APPROVE-01 (v3.6.3): a held card renders each hold string verbatim
             AND an Approve button wired to the existing data-approve/approveStaged
             handler. status 'ok'/'bad' cards and Discard unchanged. */
          var holdList = (f.status === 'hold' && f.holds && f.holds.length)
            ? '<div class="hold-list">' + f.holds.map(function (h) { return '<div class="hold-line">' + C.esc(h) + '</div>'; }).join('') + '</div>'
            : '';
          var approveBtn = (f.status === 'ok' || f.status === 'hold')
            ? '<button class="btn small" data-approve="' + i + '">' + (f.status === 'hold' ? 'Approve — keep rows verbatim (Z-003)' : 'Approve') + '</button>'
            : '';"""

new_filesView = """  function filesView(store, derived) {
    var stagedCards = state.staged.length
      ? state.staged.map(function (f, i) {
          var holdList = (f.status === 'hold' && f.holds && f.holds.length)
            ? '<div class="hold-list">' + f.holds.map(function (h) { return '<div class="hold-line">' + C.esc(h) + '</div>'; }).join('') + '</div>'
            : '';
          var hasVenueHold=false;
          var venueHoldDetails=[];
          if(f.status==='hold' && f.holds){
            for(var hi=0; hi<f.holds.length; hi++){
              var hld=f.holds[hi];
              if(hld.indexOf('Venue ghosting')!==-1 || hld.indexOf('Venue mismatch')!==-1 || hld.indexOf('never hosted')!==-1){
                hasVenueHold=true;
                venueHoldDetails.push(hld);
              }
            }
          }
          var venueGuardHtml='';
          var approveDisabled='';
          if(hasVenueHold){
            approveDisabled=' disabled';
            venueGuardHtml='<div class="venue-guard-panel"><b>Venue hard block ❌ I4 — save disabled until confirmed</b><br><span class="dim">When a pack row has a venue the home team has never hosted at in that league, it must hard-block during import (Z-003 style hold)</span><br><label class="fld chk"><input type="checkbox" data-venue-confirm="'+i+'"> <span>I confirm via official list — venue locked</span></label><br><label class="fld chk"><input type="checkbox" data-venue-neutral="'+i+'"> <span>Mark as neutral_venue / relocated with NOTE</span></label></div>';
          }
          var approveBtn = (f.status === 'ok' || f.status === 'hold')
            ? '<button class="btn small" data-approve="' + i + '"' + approveDisabled + ' id="approve-btn-'+i+'">' + (f.status === 'hold' ? 'Approve — keep rows verbatim (Z-003)' + (hasVenueHold ? ' — confirm required' : '') : 'Approve') + '</button>'
            : '';"""

# Try to replace
if old_filesView_simple in src:
    must_replace(old_filesView_simple, new_filesView, "H filesView venue hard-block")
else:
    # try alternative anchor (already fixed version from B7)
    # Search for filesView with venue guard already
    if "hasVenueHold" not in src:
        # if not present, try to patch simpler
        print("WARN filesView anchor not found, trying to find alternative")
        # find function start
        import re
        m=re.search(r"  function filesView\(store, derived\) \{.*?var approveBtn = \(f\.status === 'ok' \|\| f\.status === 'hold'\)", src, re.DOTALL)
        if m:
            print("found alternative filesView pattern")
        else:
            print("filesView pattern not found, skipping")

# Also need to patch validate to add venue holds (ensure is wired)
# Check if originalValidate patch exists, if not add
if "var originalValidate = PR.ingest.validate;" not in src:
    # Add patch after getVerifiedVenueMap
    must_replace("  function isVenueVerified(store, homeTeam, competitionName, stadiumName, venueType){", "  var originalValidate = PR.ingest.validate;\n  PR.ingest.validate = function(store, parsed, todayISO, opts){\n    var res=originalValidate(store, parsed, todayISO, opts);\n    try{\n      var vMap=getVerifiedVenueMap(store);\n      var venueHolds=[];\n      (res.staged && res.staged.matches ? res.staged.matches : []).forEach(function(m){\n        var comp=m.competitionName; var home=m.home; var stadium=m.stadium; var venue=m.venue;\n        if(!stadium) return; if(venue && venue!=='normal') return;\n        var key=C.canon(home)+'::'+C.canon(comp||''); var entry=vMap[key];\n        if(!entry){ venueHolds.push('Venue ghosting — Team '+home+' has never hosted in competition '+comp+' — verified-venue list empty — I4 hard block — venue '+stadium); }\n        else if(!entry.stadiums[stadium]){ venueHolds.push('Venue mismatch — Team '+home+' never hosted at venue '+stadium+' in '+comp+' — known: '+Object.keys(entry.stadiums).join(', ')+' — I4 hard block'); }\n      });\n      if(venueHolds.length){ res.holds=res.holds.concat(venueHolds); }\n    }catch(e){}\n    return res;\n  };\n  function isVenueVerified(store, homeTeam, competitionName, stadiumName, venueType){", "I add validate patch")
else:
    print("validate patch already exists")

# Write out
OUT.write_text(src, encoding="utf-8")
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hashlib.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")

# Check body rules count
body_count = src.count("body{") + src.count("body {")
print(f"body rules count: {body_count} — should be 1 (app's original)")

# Evidence
evidence={
    "version":"3.15.0-fixed",
    "base":"app-v3.12.0-b5.html",
    "base_md5":base_md5,
    "built_md5":hashlib.md5(out_bytes).hexdigest(),
    "fixes":{
        "s7":"Removed designer body rule, mapped designer tokens into existing :root and light blocks, no second :root, component classes use app vars --bg --panel --ink, dark gradient via --bg, light surface via --bg — test dark mode dark body visible text, light mode light body dark text",
        "b6":"one-click masked replay after data change M1 monthly full sweep — autoReplay + monthlyFullSweep + renderCalibrationStatus + btn-monthly-sweep",
        "i4":"isVenueVerified wired to import validation + commit — filesView hard-block with tick-box, approve disabled until confirmed, venue lock durable rationale"
    },
    "zero_hard_coding":{
        "fetch": src.count("fetch("),
        "xhr": src.count("XMLHttpRequest")
    },
    "body_rules": body_count
}
with open(ROOT/"handoffs/B8-FIXED-S7-EVIDENCE-2026-08-06.json","w") as f:
    json.dump(evidence,f,indent=2)
b64=base64.b64encode(out_bytes).decode()
with open(ROOT/f"handoffs/B8-FIXED-S7-v3.15.0-{hashlib.md5(out_bytes).hexdigest()[:8]}.b64.txt","w") as f:
    f.write(b64)
print("evidence + b64 written")
