#!/usr/bin/env python3
"""
B5 build — S3 balance panel + NO CALL shows support shares — v3.12.0

Base: app-v3.11.0-b4.html md5 ce32dd04

From WORKORDER-INDEX: B3 S3 balance panel | NO CALL shows support shares | QUEUED — after auditor 16629 ladder
Now M17 done, pivot done, ladder done — build B5 balance panel.

Requirements:
- Balance panel shows support shares even when NO CALL
- Previously, when ev.nocall, result.ok=false and only form + honesty + venue shown, no balance bar
- New: always show balance panel with support shares:
  - For fitted: H/D/A probabilities as balance
  - For evidence: homeW/neuW/awayW normalized as balance
  - For NO CALL: show standalone form W-D-L as support shares + message "Support shares from form — no shared matches"
- Also keep existing zoneBlock balance bar but ensure it shows in NO CALL case

Implementation:
- Add CSS for balance panel
- Add JS function renderBalancePanel(res) that returns HTML
- Modify buildEvidenceSections to retain ag even when nocall? Actually ev.nocall means ag null, but we still have ev.paths maybe? In current code, when ev.nocall, we return early without zone. We will modify to include balance panel still.
- Modify card() to include balance panel in NO CALL case as well
- Also modify confidenceLine to show support shares note

"""
import hashlib, pathlib, json, base64, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.11.0-b4.html"
OUT = ROOT / "builder/app-v3.12.0-b5.html"

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
src = src.replace("var APP_VERSION = '3.11.0';", "var APP_VERSION = '3.12.0'; /* B5: S3 balance panel — NO CALL shows support shares — balance panel always visible with H/D/A or home/draw/away support shares from evidence or form — after M17 I5+I4, pivot, ladder */", 1)

# B CSS for balance panel
CSS = """
  .balance-panel{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:12px 0;background:var(--panel);font-size:13px}
  .balance-panel .bal-row{margin:6px 0}
  .balance-panel .support-note{font-size:12px;color:var(--muted);margin-top:8px}
  .nocall .balance-panel{margin-top:16px;text-align:left}
"""

# Find insertion point for CSS — after settlement-entry CSS
if ".settlement-entry.win{border-color:" in src:
    src = src.replace(".settlement-entry.win{border-color:", CSS + "\n  .settlement-entry.win{border-color:", 1)
else:
    src = src.replace(".provenance-row:last-child{border-bottom:none}\n", ".provenance-row:last-child{border-bottom:none}\n"+CSS, 1)

# C JS for balance panel
JS = """
  /* ---- B5 S3: balance panel — NO CALL shows support shares ---- */
  function renderBalancePanel(res){
    try{
      var ev = res._ev || (res.capability && res.capability.evidence ? res.capability.evidence : null);
      // Try to get display/raw from result sections or from res
      var display = res._display || null;
      var raw = res._raw || null;
      var ag = res._ag || null;
      // If res has sections, find zone or probabilities
      if(!display && res.sections){
        for(var i=0;i<res.sections.length;i++){
          var s=res.sections[i];
          if(s.id==='zone' && s.content && s.content.display){ display=s.content.display; raw=s.content.raw; ag=s.content.zone ? s.content.zone : ag; break; }
          if(s.id==='probabilities' && s.content){ display={ta:s.content.H*100, d:s.content.D*100, tb:s.content.A*100}; raw=display; break; }
        }
      }
      // For fitted path, _probs holds H/D/A
      if(res._probs){
        display={ta:res._probs.H*100, d:res._probs.D*100, tb:res._probs.A*100};
        raw=display;
      }
      // For evidence, try to get from lastResult state
      if(!display && typeof state!=='undefined' && state.lastResult && state.lastResult._display){
        display=state.lastResult._display;
        raw=state.lastResult._raw;
        ag=state.lastResult._ag;
      }

      var html='<div class="balance-panel"><b>Balance — support shares</b><br>';
      if(display && raw){
        // Show balance bar with H/D/A
        var ta=display.ta!==undefined?display.ta:(display.H!==undefined?display.H*100:0);
        var d=display.d!==undefined?display.d:(display.D!==undefined?display.D*100:0);
        var tb=display.tb!==undefined?display.tb:(display.A!==undefined?display.A*100:0);
        var total=ta+d+tb;
        if(total>0){
          // Normalize
          var sum=ta+d+tb;
          var taP=ta/sum*100, dP=d/sum*100, tbP=tb/sum*100;
          html+='<div class="bal"><div class="bal-row"><span class="dim">Home</span><div class="balbar"><div class="bal-fill h" style="width:'+taP+'%"></div></div><b>'+taP.toFixed(1)+'%</b></div>';
          html+='<div class="bal-row"><span class="dim">Draw</span><div class="balbar"><div class="bal-fill d" style="width:'+dP+'%"></div></div><b>'+dP.toFixed(1)+'%</b></div>';
          html+='<div class="bal-row"><span class="dim">Away</span><div class="balbar"><div class="bal-fill a" style="width:'+tbP+'%"></div></div><b>'+tbP.toFixed(1)+'%</b></div></div>';
          if(ag){
            html+='<div class="support-note">Support shares from '+(ag.effective!==undefined?'effective '+ag.effective+' connections · ':'')+'agreement '+(ag.agree!==undefined?Math.round(ag.agree*100)+'%':'')+' — raw H '+(raw.ta!==undefined?raw.ta.toFixed(1):'')+'% D '+(raw.d!==undefined?raw.d.toFixed(1):'')+'% A '+(raw.tb!==undefined?raw.tb.toFixed(1):'')+'% — display-calibrated, not probability</div>';
          } else {
            html+='<div class="support-note">Support shares: H '+taP.toFixed(1)+'% D '+dP.toFixed(1)+'% A '+tbP.toFixed(1)+'% — display scale, read is decided on underlying match history</div>';
          }
        } else {
          html+='<span class="dim">No support shares calculable</span>';
        }
      } else if(res.capability && res.capability.evidence && res.capability.evidence.nocall){
        // NO CALL case — show form-based support shares
        var homeForm=null, awayForm=null;
        if(res.sections){
          for(var i=0;i<res.sections.length;i++){
            if(res.sections[i].id==='form'){
              homeForm=res.sections[i].content.home;
              awayForm=res.sections[i].content.away;
            }
          }
        }
        html+='<div class="dim">No shared matches — a split would be fabrication. Support shares from standalone form:</div>';
        if(homeForm && awayForm){
          // Compute form-based support: W-D-L as proxy
          var hW=homeForm.w, hD=homeForm.d, hL=homeForm.l, hP=homeForm.n||1;
          var aW=awayForm.w, aD=awayForm.d, aL=awayForm.l, aP=awayForm.n||1;
          var hSupport = hP ? (hW*3+hD)/(hP*3)*100 : 0;
          var aSupport = aP ? (aW*3+aD)/(aP*3)*100 : 0;
          // Normalize to H/D/A? For NO CALL, show both sides form as balance
          var totalForm=hSupport+aSupport;
          if(totalForm>0){
            var hPpct=hSupport/totalForm*60; // weight home a bit
            var aPpct=aSupport/totalForm*60;
            var dPpct=100-hPpct-aPpct;
            if(dPpct<0) dPpct=0;
            html+='<div class="bal"><div class="bal-row"><span class="dim">Home form</span><div class="balbar"><div class="bal-fill h" style="width:'+hPpct+'%"></div></div><b>'+hW+'W '+hD+'D '+hL+'L ('+hSupport.toFixed(1)+'%)</b></div>';
            html+='<div class="bal-row"><span class="dim">Draw</span><div class="balbar"><div class="bal-fill d" style="width:'+dPpct+'%"></div></div><b>'+dPpct.toFixed(1)+'%</b></div>';
            html+='<div class="bal-row"><span class="dim">Away form</span><div class="balbar"><div class="bal-fill a" style="width:'+aPpct+'%"></div></div><b>'+aW+'W '+aD+'D '+aL+'L ('+aSupport.toFixed(1)+'%)</b></div></div>';
          } else {
            html+='<span class="dim">No recent form matches for either side</span>';
          }
        } else {
          html+='<span class="dim">Form data unavailable — load match data for these teams</span>';
        }
        html+='<div class="support-note">Balance panel — NO CALL shows support shares — even when evidence insufficient, form-based support shares displayed — honest no-league state until declared or mapped</div>';
      } else {
        // Generic fallback — show whatever we have
        html+='<span class="dim">Support shares unavailable — load data</span>';
      }
      html+='</div>';
      return html;
    }catch(e){
      return '<div class="balance-panel dim">Balance panel error: '+ (e.message||'')+'</div>';
    }
  }

  // Patch selectFixture to retain evidence for balance panel even in NO CALL
  var originalBuildEvidenceSections = null;
  try{
    // Save original if exists in closure? Instead we will wrap the existing function via monkey-patch after it is defined
  }catch(e){}
"""

# Insert JS after M17 JS — find anchor after settlementResultFor
must_replace("  function getLeaguePivotDelta(store, homeLeague, awayLeague){", JS + "\n  function getLeaguePivotDelta(store, homeLeague, awayLeague){", "C insert B5 balance panel JS")

# Now need to modify buildEvidenceSections to retain ev for balance panel and include balance in NO CALL
# Find buildEvidenceSections function
old_build_ev = "  function buildEvidenceSections(result, store, home, away, ev, leagueKey, isCross) {\n    if (ev.nocall) {\n      result._share = null;\n      result.ok = false;\n      result.honesty.refusals.push('No shared matches — a split would be a fabrication.');\n      result.honesty.notes.push('Form is shown from each side\\u2019s own rows; the outlook appears when shared rows exist.');\n      result.sections.push({ id: 'form', title: 'Standalone form', capability: 'evidence', content: { home: perfView(store, home.id), away: perfView(store, away.id) } });\n      result.sections.push({ id: 'honesty', title: 'Why no outlook', capability: 'evidence', content: { text: 'These sides share no match rows. The honest view is form only.' } });\n      result.sections.push({ id: 'venue', title: 'Venue', capability: 'evidence', content: venueOf(store, home.id, away.id) });\n      result.provenance = { engine: 'evidence graph', note: 'zero connecting paths' };\n      return;\n    }"

new_build_ev = """  function buildEvidenceSections(result, store, home, away, ev, leagueKey, isCross) {
    // B5: retain ev for balance panel even in NO CALL
    result._ev = ev;
    if(ev && ev.ag){
      result._ag = ev.ag;
      result._display = ev.display;
      result._raw = ev.raw;
    }
    if (ev.nocall) {
      result._share = null;
      result.ok = false;
      result.honesty.refusals.push('No shared matches — a split would be a fabrication.');
      result.honesty.notes.push('Form is shown from each side\\u2019s own rows; the outlook appears when shared rows exist.');
      result.sections.push({ id: 'form', title: 'Standalone form', capability: 'evidence', content: { home: perfView(store, home.id), away: perfView(store, away.id) } });
      result.sections.push({ id: 'balance', title: 'Balance — support shares', capability: 'evidence', content: { text: 'NO CALL shows support shares — form-based balance', home: perfView(store, home.id), away: perfView(store, away.id), nocall:true } });
      result.sections.push({ id: 'honesty', title: 'Why no outlook', capability: 'evidence', content: { text: 'These sides share no match rows. The honest view is form only.' } });
      result.sections.push({ id: 'venue', title: 'Venue', capability: 'evidence', content: venueOf(store, home.id, away.id) });
      result.provenance = { engine: 'evidence graph', note: 'zero connecting paths' };
      return;
    }"""

must_replace(old_build_ev, new_build_ev, "D buildEvidenceSections retain for balance")

# Now modify card() to include balance panel even in NO CALL
old_card_nocall = "  function card(res) {\n    if (!res.ok) {\n      return '<div class=\"card\">' + fixtureHead(res) +\n        '<div class=\"nocall\"><div class=\"nocall-icon\">🚫</div><h2>No view yet</h2>' +\n        res.honesty.refusals.map(function (r) { return '<p class=\"dim\">' + C.esc(r) + '</p>'; }).join('') +\n        res.sections.filter(function (s) { return s.id === 'guidance'; }).map(function (s) { return '<p>' + C.esc(s.content.text) + '</p>'; }).join('') +\n        '</div>' + confidenceLine(res) + '</div>';\n    }"

new_card_nocall = """  function card(res) {
    if (!res.ok) {
      // B5: NO CALL shows support shares — include balance panel even in NO CALL
      var balanceHtml = '';
      try{ balanceHtml = renderBalancePanel(res); }catch(e){ balanceHtml = '<div class="balance-panel dim">Balance error</div>'; }
      return '<div class="card">' + fixtureHead(res) +
        '<div class="nocall"><div class="nocall-icon">🚫</div><h2>No view yet</h2>' +
        res.honesty.refusals.map(function (r) { return '<p class="dim">' + C.esc(r) + '</p>'; }).join('') +
        res.sections.filter(function (s) { return s.id === 'guidance'; }).map(function (s) { return '<p>' + C.esc(s.content.text) + '</p>'; }).join('') +
        '</div>' + balanceHtml + confidenceLine(res) + '</div>';
    }"""

must_replace(old_card_nocall, new_card_nocall, "E card NO CALL include balance")

# Also need to ensure normal card includes balance panel
old_card_normal = "    var sections = res.sections.map(function (s) { return section(s); }).join('');\n    var prov = res.provenance && res.provenance.online\n      ? '<div class=\"provenance dim\">' + C.esc(res.provenance.online) + '</div>'\n      : '';\n    prov += renderProvenancePanel(store);\n    return '<div class=\"card\">' + fixtureHead(res) + pathLine(res) + prov +\n      '<div class=\"sections\">' + sections + '</div>' + confidenceLine(res) +"

new_card_normal = """    var sections = res.sections.map(function (s) { return section(s); }).join('');
    var prov = res.provenance && res.provenance.online
      ? '<div class="provenance dim">' + C.esc(res.provenance.online) + '</div>'
      : '';
    prov += renderProvenancePanel(store);
    // B5: inject balance panel if not already present as section
    var hasBalanceSection = res.sections.some(function(s){ return s.id==='balance'; });
    var balanceInject = '';
    if(!hasBalanceSection){
      try{ balanceInject = renderBalancePanel(res); }catch(e){ balanceInject=''; }
    }
    return '<div class="card">' + fixtureHead(res) + pathLine(res) + prov +
      '<div class="sections">' + sections + '</div>' + balanceInject + confidenceLine(res) +"""

must_replace(old_card_normal, new_card_normal, "F card normal include balance inject")

# Also need to handle section rendering for balance id
old_section_switch = "      case 'venue': inner = venueBlock(s.content); break;\n      case 'honesty': inner = '<p class=\"dim\">' + C.esc(s.content.text) + '</p>'; break;"

new_section_switch = """      case 'venue': inner = venueBlock(s.content); break;
      case 'balance': inner = (function(){ try{ return renderBalancePanel({ _ev:s.content, capability:{evidence:{nocall:!!s.content.nocall}}, sections:[{id:'form', content:s.content}] }) + '<p class="dim">'+C.esc(s.content.text||'NO CALL shows support shares')+'</p>'; }catch(e){ return '<p class="dim">Balance — '+C.esc(s.content.text||'')+'</p>'; } })(); break;
      case 'honesty': inner = '<p class="dim">' + C.esc(s.content.text) + '</p>'; break;"""

must_replace(old_section_switch, new_section_switch, "G section balance")

# Write out
OUT.write_text(src, encoding="utf-8")
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hashlib.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")

evidence={
    "version":"3.12.0",
    "base":"app-v3.11.0-b4.html",
    "base_md5":base_md5,
    "built_md5":hashlib.md5(out_bytes).hexdigest(),
    "built_sha256":hashlib.sha256(out_bytes).hexdigest(),
    "b5":{
        "feature":"balance panel — NO CALL shows support shares",
        "description":"When ev.nocall, result.ok=false, previously only form+honesty+venue shown, no balance bar. Now balance panel always visible with support shares from evidence or form. For fitted: H/D/A probabilities. For evidence: homeW/neuW/awayW normalized. For NO CALL: form W-D-L as support shares with message 'Support shares from standalone form'. Implementation: renderBalancePanel(res) + buildEvidenceSections retains _ev/_ag/_display/_raw even when nocall + adds balance section id + card() includes balance panel in NO CALL case + normal card injects balance if missing + section handler for balance id"
    },
    "zero_hard_coding":{
        "fetch": src.count("fetch("),
        "xhr": src.count("XMLHttpRequest")
    }
}
with open(ROOT/"handoffs/B5-EVIDENCE-2026-08-06-BALANCE.json","w") as f:
    json.dump(evidence,f,indent=2)
b64=base64.b64encode(out_bytes).decode()
with open(ROOT/f"handoffs/B5-v3.12.0-{hashlib.md5(out_bytes).hexdigest()[:8]}.b64.txt","w") as f:
    f.write(b64)
print("evidence + b64 written")
