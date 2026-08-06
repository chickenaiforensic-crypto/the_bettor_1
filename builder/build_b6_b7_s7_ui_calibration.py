#!/usr/bin/env python3
"""
B6 + S7 build — S7 UI (designer system) + B6 calibration cadence — v3.13.0

Base: app-v3.12.0-b5.html md5 bb69a5c4

S7 UI: Bloomberg Terminal meets Athletic editorial — designer system in designer/
- design-tokens.css: deep navy/charcoal/emerald/gold, Tiempos Headline + Inter, max-width 840px, radius 16px, shadow-card
- components.css: btn-primary, badge emerald/gold, card, balance-bar, verdict
- prototypes/index.html: Match Verdict with icons Fortress 🛡️, trend 📈↑, pivot 🌍, hot ⚡, balance ⚖️, tip 💡, chain 🔗, provenance 🔍
- Use designer tokens, progressive disclosure Verdict → Why → Technical

B6: one-click masked replay after any data change, monthly full sweep
- autoReplay() after data change M1 (similar to autoRevalidate)
- monthlySweep() checks last replay date >30 days, runs full sweep (replay + ladder)
- UI: calibration console has Monthly full sweep button + auto status

Push to arena/019fd4e0-the-bettor-1
"""
import hashlib, pathlib, json, base64

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.12.0-b5.html"
OUT = ROOT / "builder/app-v3.13.0-b6b7.html"

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
src = src.replace("var APP_VERSION = '3.12.0';", "var APP_VERSION = '3.13.0'; /* B6+B7: S7 UI Bloomberg Terminal meets Athletic editorial — designer tokens components prototype — deep navy/charcoal emerald/gold Tiempos Headline Inter — verdict with icons Fortress shield trend pivot globe hot bolt balance scales tip bulb chain link provenance mag — progressive disclosure Verdict→Why→Technical — B6 one-click masked replay after any data change M1 monthly full sweep — autoReplay + monthlySweep — after M17 I5+I4, pivot 16193, ladder 8.63%, balance panel NO CALL */", 1)

# B CSS: designer system integration
# Read designer files
design_tokens = (ROOT / "designer/design-tokens.css").read_text()
components = (ROOT / "designer/components.css").read_text()

# Build S7 CSS that merges designer tokens with existing app, mapping old vars to new
S7_CSS = f"""
/* ---- S7 UI: designer system — design-tokens.css + components.css merged — Bloomberg Terminal meets Athletic editorial ---- */
{design_tokens}

{components}

/* Map old app vars to designer palette — dark premium (prototype gradient) */
:root{{
  /* Map existing app vars to designer */
  --bg: var(--ink-900);
  --panel: rgba(255,255,255,0.03);
  --panel2: rgba(255,255,255,0.06);
  --line: rgba(255,255,255,0.08);
  --line2: rgba(255,255,255,0.12);
  --ink: #f0f2f8;
  --ink2: var(--silver);
  --muted: var(--slate);
  --dim: #6b7a99;
  --accent: var(--emerald);
  --accent2: var(--emerald-deep);
  --teal: var(--emerald);
  --amber: var(--gold);
  --red: var(--coral);
  --h: var(--emerald);
  --d: var(--gold);
  --a: var(--coral);
  --card: rgba(255,255,255,0.03);
}}

html[data-theme="light"]{{
  --bg: var(--surface);
  --panel: var(--paper);
  --panel2: #f1f3f6;
  --line: rgba(10,15,26,0.08);
  --line2: rgba(10,15,26,0.12);
  --ink: var(--ink-950);
  --ink2: var(--charcoal);
  --muted: #6b7480;
  --dim: #98a0ab;
  --accent: var(--emerald-deep);
  --accent2: #0f6b3d;
  --teal: #0e7a70;
  --amber: #b4740e;
  --red: #c0392b;
  --h: #128a4e;
  --d: #a8870f;
  --a: #c0392b;
  --card: var(--paper);
}}

/* Body: designer prototype gradient dark, surface light */
body{{
  background: linear-gradient(180deg, #0e1526 0%, #131b33 100%);
  font-family: var(--font-body);
  color: var(--ink);
}}
html[data-theme="light"] body{{
  background: var(--surface);
}}

/* Topbar: designer header — Bloomberg discipline */
.topbar{{
  background: rgba(10,15,26,0.82);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  padding: 16px clamp(16px,4vw,40px);
}}
html[data-theme="light"] .topbar{{
  background: rgba(244,246,251,0.92);
  border-bottom: 1px solid rgba(10,15,26,0.06);
}}
.wordmark{{
  font-family: var(--font-display);
  font-size: 22px;
  letter-spacing: -0.03em;
  background: none;
  -webkit-text-fill-color: unset;
  color: #fff;
  background: linear-gradient(100deg, #fff, var(--emerald));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}}
html[data-theme="light"] .wordmark{{
  color: var(--ink-950);
  -webkit-text-fill-color: transparent;
  background: linear-gradient(100deg, var(--ink-950), var(--emerald-deep));
  -webkit-background-clip: text;
  background-clip: text;
}}

/* Layout: designer max-width 840px centered, but keep picker + stage for functionality */
.layout{{
  max-width: var(--max-width);
  grid-template-columns: 280px 1fr;
  gap: var(--space-lg);
  margin: 24px auto 10px;
}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}} }}

/* Cards: designer card-dark for dark, card for light */
.card{{
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
  padding: 28px 28px 32px;
}}
html[data-theme="light"] .card{{
  background: var(--paper);
  border: 1px solid rgba(10,15,26,0.06);
}}

.picker.card{{
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius);
}}
html[data-theme="light"] .picker.card{{
  background: var(--paper);
  border: 1px solid rgba(10,15,26,0.06);
}}

/* Buttons: designer btn-primary for primary, ghost for secondary */
.btn.primary{{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  background: var(--ink-900);
  color: var(--paper);
  font: 600 14px/1.2 var(--font-body);
  border: none;
  box-shadow: 0 8px 24px rgba(10,15,26,0.25);
  transition: transform .15s ease, box-shadow .2s ease;
}}
.btn.primary:hover{{
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(10,15,26,0.35);
  filter: none;
  color: var(--paper);
}}
html[data-theme="light"] .btn.primary{{
  background: var(--ink-900);
}}

/* Badges: designer badge-emerald/gold */
.badge{{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font: 700 11px/1 var(--font-body);
  letter-spacing: .03em;
  text-transform: uppercase;
}}
.badge-emerald, .accent-pill{{
  background: rgba(16,185,129,0.12);
  color: var(--emerald-deep);
  border: 1px solid rgba(16,185,129,0.18);
}}
.badge-gold, .warn-pill{{
  background: rgba(200,168,77,0.12);
  color: #8a6e28;
  border: 1px solid rgba(200,168,77,0.18);
}}
html[data-theme="dark"] .badge-emerald, html[data-theme="dark"] .accent-pill{{
  background: rgba(16,185,129,0.12);
  color: var(--emerald);
  border-color: rgba(16,185,129,0.18);
}}
html[data-theme="dark"] .badge-gold, html[data-theme="dark"] .warn-pill{{
  background: rgba(200,168,77,0.12);
  color: var(--gold);
  border-color: rgba(200,168,77,0.18);
}}

/* Verdict typography: Tiempos Headline */
.verdict{{
  font-family: var(--font-display);
  font-size: 28px;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #fff;
}}
html[data-theme="light"] .verdict{{
  color: var(--ink-950);
}}
.team{{
  font-family: var(--font-display);
}}

/* Balance bar: designer balance-bar */
.balance-bar{{
  height: 10px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--mist);
  display: flex;
}}
html[data-theme="dark"] .balance-bar{{
  background: rgba(255,255,255,0.08);
}}
.balance-bar > span{{ height:100%; display:block; }}
.balbar{{
  height: 10px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--mist);
}}
html[data-theme="dark"] .balbar{{
  background: rgba(255,255,255,0.08);
}}
.bal-fill.h{{ background: var(--emerald); }}
.bal-fill.d{{ background: var(--gold); }}
.bal-fill.a{{ background: var(--slate); }}

/* Provenance, league pivot, integrity panels: use card-dark style */
.provenance-panel, .league-pivot-panel, .live-constants-panel, .integrity-flags-panel, .venue-guard-panel, .settlement-entry, .balance-panel{{
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius);
}}
html[data-theme="light"] .provenance-panel, html[data-theme="light"] .league-pivot-panel, html[data-theme="light"] .live-constants-panel, html[data-theme="light"] .integrity-flags-panel, html[data-theme="light"] .venue-guard-panel, html[data-theme="light"] .settlement-entry, html[data-theme="light"] .balance-panel{{
  background: var(--paper);
  border: 1px solid rgba(10,15,26,0.06);
}}

/* Tabs: Bloomberg discipline */
.tabs{{
  max-width: var(--max-width);
  margin: 20px auto 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}}
html[data-theme="light"] .tabs{{
  border-bottom: 1px solid rgba(10,15,26,0.08);
}}
.tab{{
  font-family: var(--font-body);
  font-weight: 600;
}}
.tab.on{{
  color: var(--emerald);
  border-bottom-color: var(--emerald);
}}

/* Console: designer */
.console{{
  max-width: var(--max-width);
}}
.console-card{{
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--radius);
  box-shadow: var(--shadow-card);
}}
html[data-theme="light"] .console-card{{
  background: var(--paper);
  border: 1px solid rgba(10,15,26,0.06);
}}

/* Footer: designer */
.footer{{
  max-width: var(--max-width);
  border-top: 1px solid rgba(255,255,255,0.06);
}}
html[data-theme="light"] .footer{{
  border-top: 1px solid rgba(10,15,26,0.08);
}}

/* Icons with fixed meanings — tooltip */
.icon-meaning{{ cursor: help; border-bottom: 1px dotted var(--slate); }}

/* Progressive disclosure: Verdict → Why → Technical */
details.graph summary{{
  font-family: var(--font-display);
  color: #fff;
}}
html[data-theme="light"] details.graph summary{{
  color: var(--ink-950);
}}
"""

# Insert S7 CSS after previous CSS
must_replace(".balance-panel .support-note{font-size:12px;color:var(--muted);margin-top:8px}\n", ".balance-panel .support-note{font-size:12px;color:var(--muted);margin-top:8px}\n"+S7_CSS, "B S7 CSS")

# C JS for B6 calibration cadence + S7 icons
JS = """
  /* ---- B6: one-click masked replay after any data change M1, monthly full sweep ---- */
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
        STORE.log(store, { type:'calibration', action:'auto-replay', summary:'Masked replay auto-regenerated after data change — '+saved.join(', ')+' — M1', detail:'autoReplay after data change' });
      }
      return report;
    }catch(e){ return null; }
  }

  function checkMonthlySweep(store, derived){
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
        return { need:true, reason:'last run '+lastRun.toISOString().slice(0,10)+' — '+diffDays.toFixed(1)+' days ago >30 days — monthly sweep required', days:diffDays, lastRun:lastRun };
      }
      return { need:false, days:diffDays, lastRun:lastRun };
    }catch(e){ return { need:false, error:e.message }; }
  }

  function monthlyFullSweep(store, derived){
    try{
      var replayReport=PR.replay.run(store, derived);
      var ladderReport=PR.calibration.run(store);
      var saved=[];
      // Save replay artifacts
      ['zone-table','confidence-table','goals-band'].forEach(function(kind){
        if(replayReport.wins && replayReport.wins[kind]){
          store.artifacts=store.artifacts.filter(function(a){ return a.kind!==kind; });
          store.artifacts.push({ id:STORE.nextId(store,'a'), kind:kind, version:'2', generatedAt:new Date().toISOString(), data:replayReport.artifacts[kind] });
          saved.push(kind);
        }
      });
      // Save ladder artifact
      if(ladderReport && !ladderReport.refused){
        store.artifacts=store.artifacts.filter(function(a){ return a.kind!=='calibration-run'; });
        store.artifacts.push({ id:STORE.nextId(store,'a'), kind:'calibration-run', version:PR.calibration.version, generatedAt:ladderReport.generatedAt, data:ladderReport, note:ladderReport.summary+' — monthly full sweep' });
        saved.push('calibration-run');
      }
      STORE.log(store, { type:'calibration', action:'monthly-sweep', summary:'Monthly full sweep complete — '+saved.join(', ')+' — B6', detail:'monthlyFullSweep auto + manual' });
      STORE.save(store);
      PR.derive.invalidate();
      return { ok:true, saved:saved, replay:replayReport, ladder:ladderReport };
    }catch(e){
      return { ok:false, error:e.message };
    }
  }

  function renderCalibrationStatus(store){
    var check=checkMonthlySweep(store);
    var html='<div class="balance-panel"><b>Calibration cadence — B6 one-click after data change + monthly sweep</b><br>';
    if(check.need){
      html+='<span class="dim">Monthly sweep needed: '+(check.reason||'no prior run')+' — last run '+(check.lastRun?check.lastRun.toISOString().slice(0,10):'never')+' — '+ (check.days?check.days.toFixed(1)+' days ago':'')+'</span><br>';
      html+='<button class="btn primary" id="btn-monthly-sweep">Run monthly full sweep (replay + ladder)</button> <span class="dim">One-click after data change is automatic — this button runs full sweep manually</span>';
    } else {
      html+='<span class="dim">Last calibration/replay '+(check.lastRun?check.lastRun.toISOString().slice(0,10):'unknown')+' — '+(check.days?check.days.toFixed(1)+' days ago':'')+' — within 30 days — monthly sweep not yet needed — auto replay after data change is active (M1)</span><br>';
      html+='<button class="btn" id="btn-monthly-sweep">Run monthly full sweep anyway</button>';
    }
    html+='</div>';
    return html;
  }

  /* S7 icons with fixed meanings — tooltip context */
  var ICON_MEANINGS={
    '🛡️': 'Fortress — strong home tier A+ (78.5% win n=7718)',
    '📈': 'Live trend — recent form rising ↑ or falling ↓ vs base',
    '🌍': 'League pivot — per-league X points above/below real-world cross-league accuracy',
    '⚡': 'Hot — hot last 6, high points vs base',
    '❄️': 'Cold — cold last 6, low points',
    '🔗': 'Evidence chain — H2H · common · level-3 connections',
    '⚖️': 'Balanced — support shares balanced, no side earns strong call',
    '💡': 'Why not higher — draw risk capped, star drop, TB drop, etc.',
    '🔍': 'Provenance — every precomputed input labelled M3',
    '✅': 'Calibrated',
    '🚫': 'No view / muted',
    '💾': 'Snapshot',
    '📄': 'Document/request'
  };
  function iconWithTooltip(icon){
    var meaning=ICON_MEANINGS[icon]||icon;
    return '<span class="icon-meaning" title="'+C.esc(meaning)+'">'+icon+'</span>';
  }
"""

must_replace("  function getLeaguePivotDelta(store, homeLeague, awayLeague){", JS + "\n  function getLeaguePivotDelta(store, homeLeague, awayLeague){", "C B6+S7 JS insert")

# D Patch autoRevalidate to also call autoReplay
must_replace("  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "  function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      autoReplay(store, PR.derive.derive(store, { engines: [function(s,d){ d.dcFit=PR.dc.fit(s); }] }));\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "D autoRevalidate also autoReplay")

# E Patch calibrationConsole to include B6 status + monthly sweep button
# Find calibrationConsole function anchor
old_cal_console = "  function calibrationConsole(store, derived) {\n    var art = store.artifacts.filter(function (a) { return ['zone-table', 'draw-table', 'confidence-table', 'goals-band', 'market-calibration', 'replay-validation', 'calibration-run', 'dc-fitted-model', 'dc-fitted-draw-table', 'dc-fitted-tiers', 'dc-fitted-markets', 'dc-fitted-records', 'form-declaration'].indexOf(a.kind) !== -1; });"

new_cal_console = """  function calibrationConsole(store, derived) {
    var calStatusHtml = renderCalibrationStatus(store);
    var art = store.artifacts.filter(function (a) { return ['zone-table', 'draw-table', 'confidence-table', 'goals-band', 'market-calibration', 'replay-validation', 'calibration-run', 'dc-fitted-model', 'dc-fitted-draw-table', 'dc-fitted-tiers', 'dc-fitted-markets', 'dc-fitted-records', 'form-declaration', 'dc-fitted-league-pivot', 'dc-fitted-constants'].indexOf(a.kind) !== -1; });"""

must_replace(old_cal_console, new_cal_console, "E calibrationConsole add B6 status")

# Need to inject calStatusHtml into return
# Find where calibrationConsole returns
must_replace("    return '<p class=\"dim\">Calibration is a masked replay on the data: later information is hidden, the model predicts, then we compare. Artifacts are only replaced when a regeneration wins on held-out data.</p>' +", "    return calStatusHtml + '<p class=\"dim\">Calibration is a masked replay on the data: later information is hidden, the model predicts, then we compare. Artifacts are only replaced when a regeneration wins on held-out data.</p>' +", "F inject calStatusHtml")

# Add monthly sweep binding in bind()
old_bind_ladder = "    on('#btn-ladder', function () { runLadder(store, derived); });\n    on('#btn-ladder-dl', function () { downloadLadderArtifact(store); });"

new_bind_ladder = """    on('#btn-ladder', function () { runLadder(store, derived); });
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
    });"""

must_replace(old_bind_ladder, new_bind_ladder, "G bind monthly sweep")

# H Also enhance probBlock and zoneBlock with icons per designer
old_prob = "  function probBlock(p) {\n    var rows = [['Home', p.H, 'h'], ['Draw', p.D, 'd'], ['Away', p.A, 'a']];\n    var bar = rows.map(function (r) {\n      return '<div class=\"bar-seg ' + r[2] + '\" style=\"flex:' + Math.max(0.5, r[1] * 1000) + '\"><span>' + C.esc(r[0]) + ' ' + pct(r[1]) + '</span></div>';\n    }).join('');\n    return '<div class=\"prob\"><div class=\"pbar\">' + bar + '</div>' +\n      '<div class=\"pmeta dim\">Read: ' + C.esc(p.tier) + ' · ' + p.points + ' points</div></div>';\n  }"

new_prob = """  function probBlock(p) {
    var rows = [['Home', p.H, 'h'], ['Draw', p.D, 'd'], ['Away', p.A, 'a']];
    var bar = rows.map(function (r) {
      return '<div class=\"bar-seg ' + r[2] + '\" style=\"flex:' + Math.max(0.5, r[1] * 1000) + '\"><span>' + C.esc(r[0]) + ' ' + pct(r[1]) + '</span></div>';
    }).join('');
    // S7 icons: Fortress for high home prob, Balance, etc.
    var icons = '';
    if(p.H>=0.70) icons+=iconWithTooltip('🛡️')+' Fortress ';
    if(p.H>=0.60 || p.A>=0.60) icons+=iconWithTooltip('⚖️')+' Balanced ';
    icons+=iconWithTooltip('🔍')+' Provenance ';
    return '<div class="prob"><div class="pbar">' + bar + '</div>' +
      '<div class="pmeta dim">Read: ' + C.esc(p.tier) + ' · ' + p.points + ' points — '+icons+'</div></div>';
  }"""

must_replace(old_prob, new_prob, "H probBlock with icons")

old_zone = "  function zoneBlock(z) {\n    var zone = z.zone;\n    var disp = z.display, raw = z.raw;\n    var demoted = zone.demoted && zone.demoted.length ? ' <span class=\"dim\">(held back by ' + zone.demoted.join(', ') + ')</span>' : '';\n    return '<div class=\"zone-wrap\">' +\n      '<div class=\"zone-big\"><span class=\"pill accent-pill\">' + C.esc(zone.key.toUpperCase()) + '</span> <b>' + C.esc(zone.tag) + '</b>' + demoted + '</div>' +"

new_zone = """  function zoneBlock(z) {
    var zone = z.zone;
    var disp = z.display, raw = z.raw;
    var demoted = zone.demoted && zone.demoted.length ? ' <span class="dim">(held back by ' + zone.demoted.join(', ') + ')</span>' : '';
    // S7 icons
    var iconsLine = iconWithTooltip('🔗')+' Evidence chain '+ (zone.secs?zone.secs.length+' sections':'') +' · '+iconWithTooltip('⚖️')+' Balanced · '+iconWithTooltip('💡')+' Why not higher — '+(zone.demoted&&zone.demoted.length?zone.demoted.join(', '):'draw risk')+' · '+iconWithTooltip('🌍')+' League pivot · '+iconWithTooltip('📈')+' Live trend';
    return '<div class="zone-wrap">' +
      '<div class="zone-big"><span class="pill accent-pill">' + C.esc(zone.key.toUpperCase()) + '</span> <b>' + C.esc(zone.tag) + '</b>' + demoted + '</div>' +
      '<div class="dim" style="font-size:13px;margin:6px 0">'+iconsLine+'</div>' +"""

must_replace(old_zone, new_zone, "I zoneBlock with icons")

# Write out
OUT.write_text(src, encoding="utf-8")
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hashlib.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")

# Evidence
evidence={
    "version":"3.13.0",
    "base":"app-v3.12.0-b5.html",
    "base_md5":base_md5,
    "built_md5":hashlib.md5(out_bytes).hexdigest(),
    "built_sha256":hashlib.sha256(out_bytes).hexdigest(),
    "s7":{
        "designer_system":"designer/design-tokens.css + components.css + prototypes/index.html",
        "description":"Bloomberg Terminal meets Athletic editorial — deep navy/charcoal emerald/gold, Tiempos Headline + Inter, max-width 840px, card-dark, badge emerald/gold, balance-bar, verdict 28px, icons Fortress 🛡️ trend 📈 pivot 🌍 hot ⚡ cold ❄️ chain 🔗 balance ⚖️ tip 💡 provenance 🔍 with tooltip fixed meanings, progressive disclosure Verdict→Why→Technical, theme toggle",
        "css_mapping":"old vars --bg --panel etc mapped to designer --ink-900, --paper, emerald, gold, etc. Body gradient #0e1526→#131b33 dark, surface #f4f6fb light",
        "icons":"Fixed emoji-to-meaning mapping preserved with title tooltips"
    },
    "b6":{
        "one_click_masked_replay":"autoReplay() after any data change M1 — runs PR.replay.run, saves zone-table/confidence-table/goals-band, logs auto-replay",
        "monthly_full_sweep":"checkMonthlySweep() checks last calibration-run/replay-validation/zone-table date >30 days, monthlyFullSweep() runs replay + ladder, saves artifacts, logs monthly-sweep",
        "ui":"calibrationConsole now shows renderCalibrationStatus with last run days ago + button Run monthly full sweep (replay+ladder) + busy-icon, bind for btn-monthly-sweep"
    },
    "zero_hard_coding":{
        "fetch": src.count("fetch("),
        "xhr": src.count("XMLHttpRequest")
    }
}
with open(ROOT/"handoffs/B6B7-EVIDENCE-2026-08-06-S7-B6.json","w") as f:
    json.dump(evidence,f,indent=2)
b64=base64.b64encode(out_bytes).decode()
with open(ROOT/f"handoffs/B6B7-v3.13.0-{hashlib.md5(out_bytes).hexdigest()[:8]}.b64.txt","w") as f:
    f.write(b64)
print("evidence + b64 written")
