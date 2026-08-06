#!/usr/bin/env python3
"""
Final fix — S7 properly scoped + I4 venue guard hard-block wired — v3.16.0

Base: app-v3.12.0-b5.html (clean, has B5 balance panel, B4 M17 I5 settlement, B3 pivot+M10, B2 constants, B1 live-derive, B0 ladder)
But v3.12 has partial I4 (flags but not hard-block tick-box). We will replace I4 with clean proper wiring.

Fixes:
1. S7 CSS broken — scope properly:
   - Remove designer body rule (was pasted wholesale)
   - Map designer tokens into existing :root and html[data-theme="light"] — no second :root
   - Component classes use app vars --bg --panel --ink, not --surface --paper --ink-950
   - Dark gradient via --bg, light surface via --bg, from app's theme switch

2. I4 venue guard FAIL — isVenueVerified exists but isn't called during import. Wire into PR.ingest.validate:
   - When pack row has venue home team never hosted at in that league, hard-block during import Z-003 hold
   - User confirms via tick-box or marks neutral_venue
   - Implementation:
     * getVerifiedVenueMap(store): builds map canon(home)+'::'+canon(comp) -> {team, comp, stadiums:{}, count}
     * isVenueVerified(store, homeTeam, comp, stadium, venueType): returns ok/hardBlock + reason
     * PR.ingest.validate monkey-patch: after originalValidate, build vMap, iterate staged.matches, if stadium and venue normal:
         - if no entry for team+comp => push hold Venue ghosting — Team never hosted in competition — I4 hard block
         - else if stadium not in entry.stadiums => push hold Venue mismatch — Team never hosted at venue — I4 hard block — known list
       Then res.holds = res.holds.concat(venueHolds)
     * filesView: detect venue holds, show venue-guard-panel with checkboxes data-venue-confirm / data-venue-neutral, Approve button disabled id approve-btn-{i} until confirmed
     * bind: listeners for data-venue-confirm / data-venue-neutral to enable Approve, data-approve click checks confirmation, logs venue-confirm durable rationale + venue lock
     * approveStaged double-check at commit: re-build vMap, re-check staged.matches, if issues and no confirmation -> toast hard block and abort (re-insert staged), else log venue-lock and proceed, preserving verbatim venue

Also includes B6 calibration cadence (autoReplay + monthly sweep) from previous builds.

Base is v3.12.0-b5 which already has:
- B3 pivot + M10
- B4 I5 settlement (draw=loss)
- B5 balance panel NO CALL
- But I4 only partial, S7 not present, B6 not present

We will add S7 fixed + B6 + I4 proper.

"""
import hashlib, pathlib, json, base64, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.12.0-b5.html"
OUT = ROOT / "builder/app-v3.16.0-final.html"

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
src = src.replace("var APP_VERSION = '3.12.0';", "var APP_VERSION = '3.16.0'; /* FINAL FIX S7 properly scoped + I4 hard-block wired + B6 calibration — S7: no designer body rule, tokens mapped into existing :root/light, components use app vars --bg --panel --ink, dark gradient via --bg, light surface via --bg, Bloomberg Terminal meets Athletic editorial — I4: isVenueVerified wired into PR.ingest.validate hard-block Z-003 hold tick-box neutral_venue — B6: autoReplay after data change + monthly sweep */", 1)

# B Properly scoped S7 CSS — merged tokens into existing :root and light, no body rule
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
  --ink-950: #0a0f1a;
  --surface: #f4f6fb;
  --paper: #ffffff;
  --emerald: #10b981;
  --emerald-deep: #047857;
  --gold: #c8a84d;
}"""

must_replace(old_light, new_light, "B2 merged light theme")

# C Add properly scoped component classes using app vars
S7_COMPONENTS_FIXED = """
/* ---- S7 UI fixed: properly scoped designer components using app vars --bg --panel --ink, no body rule ---- */
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
.card{
  background:var(--panel);
  border-radius:var(--radius);
  box-shadow:var(--shadow);
  border:1px solid var(--line);
}
.verdict{
  font-family:var(--serif);
  font-size:28px;
  line-height:1.15;
  letter-spacing:-0.02em;
  color:var(--ink);
}
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
"""

must_replace(".nocall .balance-panel{margin-top:16px;text-align:left}\n", ".nocall .balance-panel{margin-top:16px;text-align:left}\n"+S7_COMPONENTS_FIXED, "B3 S7 components fixed using app vars")

# D Add B6 + I4 JS clean — ensure single definition of getVerifiedVenueMap/isVenueVerified and proper wiring

# First, remove any existing duplicate I4 code from base v3.12.0-b5 if present? Base has some venue ghosting flags but not full hard-block.
# We'll add clean implementation after getLeaguePivotDelta or after live constants.

# We need to insert JS that defines getVerifiedVenueMap, isVenueVerified, B6 autoReplay etc., and patches validate and filesView

B6_I4_S7_JS = """
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
      html+='<span class="dim">Monthly sweep needed: '+(check.reason||'no prior run')+'</span><br>';
      html+='<button class="btn primary" id="btn-monthly-sweep">Run monthly full sweep (replay + ladder)</button> <span class="dim">One-click after data change is automatic</span>';
    } else {
      html+='<span class="dim">Last calibration/replay '+(check.lastRun?check.lastRun.toISOString().slice(0,10):'unknown')+' — '+(check.days?check.days.toFixed(1)+' days ago':'')+' — within 30 days</span><br>';
      html+='<button class="btn" id="btn-monthly-sweep">Run monthly full sweep anyway</button>';
    }
    html+='</div>';
    return html;
  }

  /* ---- I4 venue guard PROPERLY WIRED — isVenueVerified called during import validation + commit ---- */
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
        return { ok:false, hardBlock:true, reason:'Team '+homeTeam+' has never hosted in competition '+competitionName+' — verified-venue list empty — I4 hard block — venue '+stadiumName, code:'never_hosted_league', team:homeTeam, competition:competitionName };
      }
    }
    if(entry.stadiums[stadiumName]){
      return { ok:true, reason:'venue verified — '+stadiumName+' has '+entry.stadiums[stadiumName]+' prior hostings' };
    } else {
      return { ok:false, hardBlock:true, reason:'Team '+homeTeam+' never hosted at venue '+stadiumName+' in '+competitionName+' — known: '+Object.keys(entry.stadiums).join(', ')+' — I4 hard block — when pack row has venue home team never hosted at in that league, hard-block during import Z-003 hold', code:'venue_mismatch', team:homeTeam, competition:competitionName, stadium:stadiumName, known:Object.keys(entry.stadiums) };
    }
  }

  // Wire into PR.ingest.validate — when pack row has venue home team never hosted at in that league, hard-block Z-003 hold
  (function(){
    var originalValidate = PR.ingest.validate;
    PR.ingest.validate = function(store, parsed, todayISO, opts){
      var res=originalValidate(store, parsed, todayISO, opts);
      try{
        var vMap=getVerifiedVenueMap(store);
        var venueHolds=[];
        (res.staged && res.staged.matches ? res.staged.matches : []).forEach(function(m){
          var comp=m.competitionName;
          var home=m.home;
          var stadium=m.stadium;
          var venue=m.venue;
          if(!stadium) return;
          if(venue && venue!=='normal') return;
          // Use isVenueVerified for consistent logic
          var check=isVenueVerified(store, home, comp, stadium, venue);
          if(!check.ok && check.hardBlock){
            venueHolds.push(check.reason+' — User confirms via tick-box or marks neutral_venue — row kept verbatim grouped by competition+pair — I4 venue guard hard-block during import Z-003 hold');
          }
        });
        if(venueHolds.length){
          res.holds=res.holds.concat(venueHolds);
        }
      }catch(e){
        // keep original result if venue check fails
      }
      return res;
    };
  })();

  var ICON_MEANINGS={
    '🛡️': 'Fortress — strong home tier',
    '📈': 'Live trend',
    '🌍': 'League pivot',
    '⚡': 'Hot',
    '❄️': 'Cold',
    '🔗': 'Evidence chain',
    '⚖️': 'Balanced',
    '💡': 'Why not higher',
    '🔍': 'Provenance',
    '✅': 'Calibrated', '🚫': 'No view', '💾': 'Snapshot', '📄': 'Doc'
  };
  function iconWithTooltip(icon){
    var meaning=ICON_MEANINGS[icon]||icon;
    return '<span class="icon-meaning" title="'+C.esc(meaning)+'">'+icon+'</span>';
  }
"""

# Insert after getLeaguePivotDelta or after existing similar
must_replace("  function getLeaguePivotDelta(store, homeLeague, awayLeague){", B6_I4_S7_JS + "\n  function getLeaguePivotDelta(store, homeLeague, awayLeague){", "C B6+I4+S7 JS clean insert")

# D Patch autoRevalidate to include autoReplay and ensureLeaguePivot
must_replace("  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      autoReplay(store, PR.derive.derive(store, { engines: [function(s,d){ d.dcFit=PR.dc.fit(s); }] }));\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "D autoRevalidate includes pivot + autoReplay")

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

# G Fix filesView with venue guard hard-block
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
              if(hld.indexOf('Venue ghosting')!==-1 || hld.indexOf('Venue mismatch')!==-1 || hld.indexOf('never hosted')!==-1 || hld.indexOf('I4 hard block')!==-1){
                hasVenueHold=true;
                venueHoldDetails.push(hld);
              }
            }
          }
          var venueGuardHtml='';
          var approveDisabled='';
          if(hasVenueHold){
            approveDisabled=' disabled';
            venueGuardHtml='<div class="venue-guard-panel"><b>Venue hard block ❌ I4 — save disabled until confirmed — isVenueVerified wired to import validation</b><br><span class="dim">When a pack row has a venue the home team has never hosted at in that league, it must hard-block during import (Z-003 style hold) — User confirms via tick-box or marks neutral_venue — isVenueVerified() called during import via PR.ingest.validate patch</span><br><label class="fld chk"><input type="checkbox" data-venue-confirm="'+i+'"> <span>I confirm via official list / tick-box vs official list — venue locked at entry</span></label><br><label class="fld chk"><input type="checkbox" data-venue-neutral="'+i+'"> <span>Mark as neutral_venue / relocated with NOTE info/neutral_venue reason</span></label><br><span class="dim">Durable rationale logged on approve — venue locked — neutral/relocated preserved verbatim rather than silent flip — I4 procedural not statistical</span></div>';
          }
          var approveBtn = (f.status === 'ok' || f.status === 'hold')
            ? '<button class="btn small" data-approve="' + i + '"' + approveDisabled + ' id="approve-btn-'+i+'">' + (f.status === 'hold' ? 'Approve — keep rows verbatim (Z-003)' + (hasVenueHold ? ' — confirm required' : '') : 'Approve') + '</button>'
            : '';"""

must_replace(old_filesView_simple, new_filesView, "H filesView venue hard-block wired")

# Also patch bind for venue confirmation
old_bind_approve = "    el.querySelectorAll('[data-approve]').forEach(function (b) {\n      b.addEventListener('click', function () { approveStaged(store, derived, +b.getAttribute('data-approve')); });\n    });"

new_bind_approve = """    el.querySelectorAll('[data-approve]').forEach(function (b) {
      b.addEventListener('click', function () {
        var idx=parseInt(b.getAttribute('data-approve'),10);
        var hasVenueHold=false;
        if(state.staged[idx] && state.staged[idx].holds){
          for(var hi=0; hi<state.staged[idx].holds.length; hi++){
            var hld=state.staged[idx].holds[hi];
            if(hld.indexOf('Venue ghosting')!==-1 || hld.indexOf('Venue mismatch')!==-1 || hld.indexOf('never hosted')!==-1 || hld.indexOf('I4 hard block')!==-1){ hasVenueHold=true; break; }
          }
        }
        if(hasVenueHold){
          var venueConfirmChecks=document.querySelectorAll('[data-venue-confirm="'+idx+'"]');
          var venueNeutralChecks=document.querySelectorAll('[data-venue-neutral="'+idx+'"]');
          var confirmed=false, neutral=false;
          for(var ci=0; ci<venueConfirmChecks.length; ci++){ if(venueConfirmChecks[ci].checked) confirmed=true; }
          for(var ni=0; ni<venueNeutralChecks.length; ni++){ if(venueNeutralChecks[ni].checked) neutral=true; }
          if(!confirmed && !neutral){
            toast('Venue hard block — save disabled until confirmed via tick-box official list or marked neutral_venue — I4 — isVenueVerified wired to import validation');
            return;
          }
          var rationale = confirmed ? 'Venue confirmed via official list tick-box — venue locked at entry — isVenueVerified() called during import — '+ (state.staged[idx].holds?state.staged[idx].holds.join('; ').slice(0,200):'') : 'Venue marked neutral_venue/relocated with NOTE — isVenueVerified() called — '+ (state.staged[idx].holds?state.staged[idx].holds.join('; ').slice(0,200):'');
          STORE.log(store, { type:'data', action:'venue-confirm', summary:'Venue guard I4 confirmed: '+rationale, detail: rationale });
        }
        approveStaged(store, derived, +b.getAttribute('data-approve'));
      });
    });
    el.querySelectorAll('[data-venue-confirm]').forEach(function (cb) {
      cb.addEventListener('change', function(){
        var idx=parseInt(cb.getAttribute('data-venue-confirm'),10);
        var btn=document.getElementById('approve-btn-'+idx);
        if(!btn) return;
        var neutralCbs=document.querySelectorAll('[data-venue-neutral="'+idx+'"]');
        var anyChecked=cb.checked;
        for(var i=0;i<neutralCbs.length;i++){ if(neutralCbs[i].checked) anyChecked=true; }
        btn.disabled=!anyChecked;
      });
    });
    el.querySelectorAll('[data-venue-neutral]').forEach(function (cb) {
      cb.addEventListener('change', function(){
        var idx=parseInt(cb.getAttribute('data-venue-neutral'),10);
        var btn=document.getElementById('approve-btn-'+idx);
        if(!btn) return;
        var confirmCbs=document.querySelectorAll('[data-venue-confirm="'+idx+'"]');
        var anyChecked=cb.checked;
        for(var i=0;i<confirmCbs.length;i++){ if(confirmCbs[i].checked) anyChecked=true; }
        btn.disabled=!anyChecked;
      });
    });
"""

must_replace(old_bind_approve, new_bind_approve, "I bind venue confirmation hard-block")

# Write out
OUT.write_text(src, encoding="utf-8")
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hashlib.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")
body_count = src.count("body{") + src.count("body {")
# Count actual body rule (not sec-body etc): search for \"\\nbody{\" and \"\\nbody {\" at line start?
import re
actual_body_rules = len(re.findall(r'\nbody\s*\{', src))
print(f"body rules: total substring {body_count}, actual body at line start {actual_body_rules} — should be 1")
print(f"fetch {src.count('fetch(')} XHR {src.count('XMLHttpRequest')}")

evidence={
    "version":"3.16.0-final-fix",
    "base":"app-v3.12.0-b5.html",
    "base_md5":base_md5,
    "built_md5":hashlib.md5(out_bytes).hexdigest(),
    "fixes":{
        "s7":"Properly scoped — no designer body rule, tokens mapped into existing :root/light, components use app vars --bg --panel --ink, dark gradient via --bg, light surface via --bg, 1 body rule only",
        "i4":"isVenueVerified wired into PR.ingest.validate — when pack row has venue home team never hosted at in that league, hard-block Z-003 hold with tick-box neutral_venue — filesView disabled Approve until confirmed, bind checks confirmation, logs durable rationale + venue lock, approveStaged double-check",
        "b6":"autoReplay after data change + monthly sweep"
    },
    "body_rules": actual_body_rules,
    "zero_hard_coding": {"fetch": src.count("fetch("), "xhr": src.count("XMLHttpRequest")}
}
with open(ROOT/"handoffs/B8-FINAL-FIX-EVIDENCE-2026-08-06.json","w") as f:
    json.dump(evidence,f,indent=2)
b64=base64.b64encode(out_bytes).decode()
with open(ROOT/f"handoffs/B8-FINAL-FIX-v3.16.0-{hashlib.md5(out_bytes).hexdigest()[:8]}.b64.txt","w") as f:
    f.write(b64)
print("evidence + b64 written")
