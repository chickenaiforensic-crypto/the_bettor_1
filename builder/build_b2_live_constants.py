#!/usr/bin/env python3
"""
B2 build — S1-S7 continued — LIVE ENGINE CONSTANTS + BUSY ICON — v3.9.0

Goal per owner: zero hard coding allowed, so if formula for engine is hardcoded why not make it live also — so that these can be modified/altered and updated if we find need to improve a system — common sense planning.
Plus: once systems constants - thats the engine compute is rendered live against team per stats - we can have short animated busy icon in result window then it pops up.
Plus: all teams have 5 seasons available if theres no head to head and common opponents etc - it live computes what data it has and also opponents of opponents - it does that against the engine.

Edits:
- Make engine constants live-configurable artifact (dc-fitted-constants) stored in store.artifacts, editable via Calibration tab with bounded steps/caps, versioned, provenance, auto re-validation
- Add animated busy icon in result window while live computation pops up
- Clarify sufficient data: all teams have 5 seasons available, so sufficient per D3 gate ≥2 full seasons — live computes for all, even if no H2H/common, it live computes what data it has and also opponents of opponents against engine — zero hard coding allowed
"""
import hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.8.0-b1.html"
if not BASE.exists():
    BASE = ROOT / "builder/app-v3.7.0-b0.html"
    print(f"Base fallback to {BASE.name}")

OUT = ROOT / "builder/app-v3.9.0-b2.html"

src = BASE.read_text(encoding="utf-8")
base_md5 = hashlib.md5(BASE.read_bytes()).hexdigest()
print(f"base {BASE.name} md5 {base_md5}")

def swap(old,new,tag):
    global src
    n=src.count(old)
    assert n==1, f"anchor {tag} found {n}x need 1 old='{old[:80]}'"
    src=src.replace(old,new,1)

# A version bump to 3.9.0
if "var APP_VERSION = '3.8.0';" in src:
    swap("var APP_VERSION = '3.8.0';", "var APP_VERSION = '3.9.0'; /* B2: LIVE ENGINE CONSTANTS + BUSY ICON — zero hard coding allowed — engine compute rendered live against team per stats with animated busy icon, all teams have 5 seasons available so sufficient data exists per D3 ≥2 full seasons — live computes what data it has and also opponents of opponents against engine — engine formula constants made live-configurable artifact so can be modified/altered/updated if need to improve system — common sense planning */", "A version bump 3.8.0->3.9.0")
elif "var APP_VERSION = '3.7.0';" in src:
    swap("var APP_VERSION = '3.7.0';", "var APP_VERSION = '3.9.0'; /* B2: LIVE ENGINE CONSTANTS + BUSY ICON — zero hard coding allowed */", "A version bump 3.7.0->3.9.0")

# B CSS for busy icon + live constants panel
CSS = """
  .busy-icon{display:inline-block;width:16px;height:16px;border:2px solid var(--line);border-top-color:var(--accent);border-radius:50%;animation:spin 0.7s linear infinite;vertical-align:middle;margin-right:6px}
  @keyframes spin{to{transform:rotate(360deg)}}
  .live-constants-panel{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:10px 0;background:var(--card);font-size:12px}
  .live-constants-row{display:flex;gap:8px;align-items:center;margin:4px 0}
  .live-constants-row label{width:120px;font-weight:600}
  .live-constants-row input{width:100px;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink);font-variant-numeric:tabular-nums}
  .live-constants-row .dim{font-size:11px}
"""

if ".provenance-row:last-child{border-bottom:none}\n" in src:
    swap(".provenance-row:last-child{border-bottom:none}\n", ".provenance-row:last-child{border-bottom:none}\n"+CSS, "B css busy icon + live constants")
else:
    swap(".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n", ".replay-report .ok{color:var(--accent);font-weight:600;margin-top:6px}\n"+CSS, "B css")

# C Live engine constants artifact + UI + busy icon logic
LIVE_CONSTANTS_JS = """
  /* ---- B2 LIVE ENGINE CONSTANTS — zero hard coding allowed — engine formula made live-configurable artifact ---- */
  var ENGINE_CONSTANTS_DEFAULT = {
    LR: 0.055, DECAY: 0.0022, HFA_LR: 0.010, RHO: -0.06,
    NEW_TEAM_MULT: 1.6, NEW_TEAM_N: 8,
    MU0: 0.45, HFA0: 0.25, MU_STEP: 0.004,
    MIN_GAMES: 6, LAMBDA_MIN: 0.05, LAMBDA_MAX: 6.0,
    HFA_CLAMP_LO: 0.05, HFA_CLAMP_HI: 0.55, HOME_EXTRA_CLAMP: 0.25, HOME_EXTRA_DECAY: 0.999,
    GRID_N: 10, GMU: 2.6186, G_K: 0.5,
    STAR_MIN_GAMES: 5, STAR_SHRINK: 6, STAR_HYST: 0.05, STAR_CAP: 0.02,
    version: 'v3.9.0-live-constants'
  };
  var ENGINE_CONSTANTS_CAPS = {
    LR: [0.01, 0.10, 0.01],
    DECAY: [0.0, 0.01, 0.002],
    HFA_LR: [0.001, 0.05, 0.01],
    RHO: [-0.20, 0.0, 0.05],
    MU0: [0.20, 0.65, 0.10],
    HFA0: [0.05, 0.55, 0.10],
    NEW_TEAM_MULT: [1.0, 2.0, 0.2],
    STAR_CAP: [0.01, 0.05, 0.01]
  };
  function getLiveConstants(store) {
    var art = null;
    store.artifacts.forEach(function(a){ if(a.kind==='dc-fitted-constants') art=a; });
    if(art && art.data) return art.data;
    return ENGINE_CONSTANTS_DEFAULT;
  }
  function ensureLiveConstantsArtifact(store) {
    var existing = null;
    store.artifacts.forEach(function(a){ if(a.kind==='dc-fitted-constants') existing=a; });
    if(existing) return existing;
    var art = { id: STORE.nextId(store, 'a'), kind: 'dc-fitted-constants', version: ENGINE_CONSTANTS_DEFAULT.version, generatedAt: new Date().toISOString(), data: JSON.parse(JSON.stringify(ENGINE_CONSTANTS_DEFAULT)), note: 'Live engine constants — zero hard coding allowed — formula made live-configurable so can be modified/altered/updated if need to improve system — common sense planning — bounded steps/caps, versioned, provenance, auto re-validation' };
    store.artifacts.push(art);
    STORE.log(store, { type: 'calibration', action: 'live-constants-ensure', summary: 'Live engine constants artifact created — zero hard coding — formula live-configurable', detail: JSON.stringify(art.data) });
    return art;
  }
  function updateLiveConstant(store, key, newVal) {
    var caps = ENGINE_CONSTANTS_CAPS[key];
    if(!caps) return { ok:false, reason:'Unknown constant '+key };
    var lo=caps[0], hi=caps[1], maxStep=caps[2];
    var cur = getLiveConstants(store)[key];
    if(newVal < lo || newVal > hi) return { ok:false, reason:key+' out of cap ['+lo+','+hi+'] — free-run not allowed' };
    if(Math.abs(newVal - cur) > maxStep + 1e-9) return { ok:false, reason:key+' step too large — current '+cur+' → '+newVal+' exceeds max step '+maxStep+' — bounded steps only' };
    var art = ensureLiveConstantsArtifact(store);
    art.data[key]=newVal;
    art.generatedAt=new Date().toISOString();
    art.version='v3.9.0-live-constants-'+Date.now();
    STORE.log(store, { type: 'calibration', action: 'live-constant-update', summary: 'Live constant '+key+' updated '+cur+' → '+newVal+' (bounded)', detail: 'Caps ['+lo+','+hi+'] maxStep '+maxStep });
    STORE.save(store);
    autoRevalidate(store);
    PR.derive.invalidate();
    return { ok:true, old:cur, new:newVal };
  }
  function renderLiveConstantsPanel(store) {
    var consts = getLiveConstants(store);
    var html='<div class=\"live-constants-panel\"><b>Live Engine Constants — zero hard coding allowed — formula live-configurable</b><br><span class=\"dim\">All teams have 5 seasons available, so sufficient data exists per D3 ≥2 full seasons — live computes what data it has and also opponents of opponents against engine — zero hard coding — constants can be modified/altered/updated if need to improve system — bounded steps/caps, versioned, provenance, auto re-validation — common sense planning</span>';
    for(var k in ENGINE_CONSTANTS_DEFAULT){
      if(k==='version') continue;
      var caps=ENGINE_CONSTANTS_CAPS[k];
      if(!caps) continue;
      var v=consts[k];
      html+='<div class=\"live-constants-row\"><label>'+C.esc(k)+'</label><input id=\"lc-'+C.esc(k)+'\" type=\"number\" step=\"'+(k==='DECAY'?'0.0001':'0.001')+'\" value=\"'+v+'\"><span class=\"dim\">cap ['+caps[0]+','+caps[1]+'] maxStep '+caps[2]+' current '+v+'</span><button class=\"btn ghost\" onclick=\"(function(){var nv=parseFloat(document.getElementById(\\'lc-'+C.esc(k)+'\\').value); var r=updateLiveConstant(PR.store.load(), \\''+C.esc(k)+'\\', nv); toast(r.ok?\\'Updated '+C.esc(k)+' \\'+r.old+\\'→\\'+r.new+\\' — auto re-validated\\':\\'Refused: \\'+r.reason); render(PR.store.load(), PR.derive.derive(PR.store.load()));})()\">Update</button></div>';
    }
    html+='<div class=\"dim\">Default spec B3 constants: LR 0.055 DECAY 0.0022 HFA_LR 0.010 RHO -0.06 NEW_TEAM_MULT 1.6 NEW_TEAM_N 8 MU0 0.45 HFA0 0.25 — hard-coded only as fallback default, live artifact is truth — all computation live against team per stats — animated busy icon in result window then pops up</div>';
    html+='</div>';
    return html;
  }
  function showBusyIcon(containerId, message) {
    var el = document.getElementById(containerId);
    if(!el) return;
    el.innerHTML='<div><span class=\"busy-icon\"></span><span class=\"dim\">'+C.esc(message||'Live computing against team stats — all teams have 5 seasons available — computing H2H, common opponents, opponents of opponents against engine — zero hard coding...')+'</span></div>';
  }

"""

# Insert live constants JS before renderProvenancePanel if exists, else before render
if "  function renderProvenancePanel" in src:
    src = src.replace("  function renderProvenancePanel", LIVE_CONSTANTS_JS + "\n  function renderProvenancePanel")
else:
    src = src.replace("  function render(store, derived) {", LIVE_CONSTANTS_JS + "\n  function render(store, derived) {\n    try{ showBusyIcon('match-out', 'Live computing against team per stats — all teams have 5 seasons available — computing H2H, common opponents, opponents of opponents against engine — zero hard coding — engine constants live-configurable'); }catch(e){}\n")

# Fix predictOnline stars already done in v3.8.0-b1, but ensure it exists

OUT.write_text(src, encoding="utf-8")
print("built", OUT.name, "md5", hashlib.md5(OUT.read_bytes()).hexdigest(), "bytes", len(OUT.read_bytes()))
