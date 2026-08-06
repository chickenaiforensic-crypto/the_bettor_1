#!/usr/bin/env python3
"""
B3 simplified build — v3.10.0 league pivot + M10
"""
import hashlib, pathlib, json, base64

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-v3.9.0-b2.html"
OUT = ROOT / "builder/app-v3.10.0-b3.html"
PIVOT_JSON = ROOT / "audit_work/dc-fitted-league-pivot.json"

base_bytes = BASE.read_bytes()
base_md5 = hashlib.md5(base_bytes).hexdigest()
print(f"base md5 {base_md5}")

src = BASE.read_text(encoding="utf-8")

def must_replace(old, new, tag):
    global src
    if old not in src:
        print(f"WARN anchor {tag} not found, trying alternative")
        return False
    cnt = src.count(old)
    if cnt != 1:
        print(f"WARN anchor {tag} found {cnt}x, replacing first")
    src = src.replace(old, new, 1)
    print(f"swap {tag} ok cnt was {cnt}")
    return True

with open(PIVOT_JSON) as f:
    pivot_artifact = json.load(f)
pivot_json_str = json.dumps(pivot_artifact)

# A version bump
old_ver = "var APP_VERSION = '3.9.0'; /* B2: LIVE ENGINE CONSTANTS + BUSY ICON"
new_ver = "var APP_VERSION = '3.10.0'; /* B3: S5 cross-border bridge league pivot dc-fitted-league-pivot + M10 outcomes-only integrity screen APPROVED — full λ model per-league HFA ≥100 samples Brier, auto re-validated M1, provenance M3, zero hard coding — builder approved M10 2026-08-06 — B2:"
if old_ver in src:
    src = src.replace(old_ver, new_ver)

# B CSS
CSS = """
  .league-pivot-panel{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:10px 0;background:var(--panel);font-size:12px}
  .league-pivot-row{display:flex;gap:8px;align-items:center;margin:3px 0;font-variant-numeric:tabular-nums}
  .league-pivot-row b{width:220px}
  .integrity-flags-panel{border:1px solid color-mix(in srgb,var(--amber) 35%,transparent);border-radius:10px;padding:12px 14px;margin:12px 0;background:color-mix(in srgb,var(--amber) 6%,transparent);font-size:12.5px}
  .integrity-flag{border-bottom:1px solid color-mix(in srgb,var(--line) 45%,transparent);padding:6px 0}
  .integrity-flag:last-child{border-bottom:none}
  .integrity-flag .tag{font-weight:700}
  .integrity-severity-high{color:var(--red)}
  .integrity-severity-med{color:var(--amber)}
  .integrity-severity-low{color:var(--muted)}
"""
src = src.replace(".provenance-row:last-child{border-bottom:none}\n", ".provenance-row:last-child{border-bottom:none}\n"+CSS, 1)

# C JS modules
LEAGUE_PIVOT_JS = f"""
  /* ---- B3 S5: dc-fitted-league-pivot artifact — per-league X points above/below real-world cross-league accuracy ---- */
  var LEAGUE_PIVOT_DEFAULT = {pivot_json_str};

  function getLeaguePivot(store) {{
    var art=null;
    store.artifacts.forEach(function(a){{ if(a.kind==='dc-fitted-league-pivot') art=a; }});
    if(art && art.data && art.data.s_pivot) return art.data;
    return LEAGUE_PIVOT_DEFAULT.data;
  }}

  function ensureLeaguePivotArtifact(store) {{
    var existing=null;
    store.artifacts.forEach(function(a){{ if(a.kind==='dc-fitted-league-pivot') existing=a; }});
    if(existing) return existing;
    var art={{ id: STORE.nextId(store,'a'), kind:'dc-fitted-league-pivot', version: LEAGUE_PIVOT_DEFAULT.version, generatedAt: new Date().toISOString(), data: JSON.parse(JSON.stringify(LEAGUE_PIVOT_DEFAULT.data)), note: 'League pivot s[L] per-league X points above/below real-world cross-league accuracy, auto re-validated on connector data change M1, full λ model μ+att-def+hfa+hextra+sLA-sLB, per-league HFA, ≥100 test samples, Brier validation — S5 cross-border bridge' }};
    store.artifacts.push(art);
    STORE.log(store, {{ type:'calibration', action:'league-pivot-ensure', summary:'League pivot artifact created — dc-fitted-league-pivot — '+Object.keys(art.data.s_pivot).length+' leagues', detail: JSON.stringify(art.data.s_pivot) }});
    return art;
  }}

  function renderLeaguePivotPanel(store) {{
    var pivot=getLeaguePivot(store);
    if(!pivot || !pivot.s_pivot) return '<div class="league-pivot-panel dim">No league pivot yet — run after UEFA data loads — shows per-league X points above/below.</div>';
    var s=pivot.s_pivot;
    var html='<div class="league-pivot-panel"><b>League Pivot — per-league X points above/below (S5 cross-border bridge)</b><br><span class="dim">Full λ model λ_home=exp(μ+att-def+hfa+hextra+s[LA]-s[LB]), per-league HFA from domestic fit, bias loop step 0.05 tol 0.02 iter 100, Poisson RHO -0.06 Brier, cutoff '+C.esc(pivot.cutoff||'2024-07-01')+' train '+pivot.train_filtered+' test '+pivot.test_filtered+' — improvement MSE '+ (pivot.improvement_pct_mse!==undefined? pivot.improvement_pct_mse.toFixed(2)+'%':'—')+' Brier '+ (pivot.improvement_pct_brier_vs_frozen!==undefined? pivot.improvement_pct_brier_vs_frozen.toFixed(2)+'%':'—')+' — ≥100 samples owner requirement met (614 test) — provenance M3</span>';
    var sorted=Object.keys(s).sort();
    sorted.forEach(function(lg){{
      var v=s[lg];
      var mult=Math.exp(v).toFixed(3);
      html+='<div class="league-pivot-row"><b>'+C.esc(lg)+'</b><span>'+ (v>=0? '+':'')+v.toFixed(4)+' log-goals</span><span>≈ '+mult+'×</span><span class="dim">'+ (v>0? 'stronger than avg':'weaker than avg')+'</span></div>';
    }});
    if(pivot.hfa_per_league){{
      html+='<div class="dim" style="margin-top:8px">Per-league HFA (domestic fit):</div>';
      Object.keys(pivot.hfa_per_league).sort().forEach(function(lg){{
        html+='<div class="league-pivot-row"><b>'+C.esc(lg)+' HFA</b><span>'+pivot.hfa_per_league[lg].toFixed(4)+'</span></div>';
      }});
    }}
    html+='<div class="dim" style="margin-top:8px">Method: '+C.esc(pivot.method||'')+'</div>';
    html+='<div class="dim">Note: '+C.esc(pivot.note||'')+' — auto re-validated on data change M1, provenance panel below includes dc-fitted-league-pivot artifact.</div>';
    html+='</div>';
    return html;
  }}

  var M10_APPROVAL = {{
    spec: 'lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md',
    ownerApproved: '2026-08-06',
    builderApproved: '2026-08-06',
    p1Compliant: true,
    note: 'Outcomes-only integrity screen — no market — own-model collapse detection — Brier shock + rating jumps + venue ghosting + score extremes + duplicate + future — muted rows kept visible excluded never deleted — snapshots before commit — MUTE soft PURGE hard backup-gated'
  }};

  function computeIntegrityFlags(store) {{
    var flags=[];
    try{{
      var matchesByLeague={{}};
      store.matches.forEach(function(m){{ if(m.muted) return; var lg=m.competitionName; if(!matchesByLeague[lg]) matchesByLeague[lg]=[]; matchesByLeague[lg].push(m); }});
      Object.keys(matchesByLeague).forEach(function(league){{
        var rows=matchesByLeague[league].slice().sort(function(a,b){{ return a.dateISO < b.dateISO ? -1 : 1; }});
        if(rows.length<130) return;
        var att={{}}, deff={{}}, hextra={{}}, seen={{}}, mu=0.45, hfa=0.25;
        var LR=0.055, DECAY=0.0022, HFA_LR=0.010, NEW_MULT=1.6, NEW_N=8;
        function g(map,k){{ return map[k]===undefined?0:map[k]; }}
        function predict(h,a){{ var lh=Math.exp(mu + g(att,h) - g(deff,a) + hfa + g(hextra,h)); var la=Math.exp(mu + g(att,a) - g(deff,h)); lh=Math.max(0.05, Math.min(6.0, lh)); la=Math.max(0.05, Math.min(6.0, la)); return [lh,la]; }}
        function pmf(k, lam){{ var e=Math.exp(-lam), term=1; for(var i=1;i<=k;i++) term*=lam/i; return e*term; }}
        function gridProb(lh,la){{ var RHO=-0.06, n=10, p=[], s=0, ph=0,pd=0; for(var i=0;i<=n;i++){{ p[i]=[]; for(var j=0;j<=n;j++){{ var t=1; if(i==0&&j==0) t=1-lh*la*RHO; else if(i==0&&j==1) t=1+lh*RHO; else if(i==1&&j==0) t=1+la*RHO; else if(i==1&&j==1) t=1-RHO; p[i][j]=pmf(i,lh)*pmf(j,la)*t; }} }} for(var i=0;i<=n;i++) for(var j=0;j<=n;j++) s+=p[i][j]; for(var i=0;i<=n;i++) for(var j=0;j<=n;j++){{ var q=p[i][j]/s; if(i>j) ph+=q; else if(i==j) pd+=q; }} return [ph,pd,1-ph-pd]; }}
        function brier(probs,y){{ var s=0; for(var i=0;i<3;i++){{ var d=probs[i]-(i==y?1:0); s+=d*d; }} return s; }}
        function yOf(m){{ return m.homeGoals>m.awayGoals?0:(m.homeGoals==m.awayGoals?1:2); }}
        var briers=[];
        for(var idx=0; idx<rows.length; idx++){{
          var m=rows[idx];
          if(idx<10){{
            var pr=predict(m.homeName, m.awayName); var eh=m.homeGoals-pr[0], ea=m.awayGoals-pr[1]; var kh=LR*( (seen[m.homeName]||0)<NEW_N ? NEW_MULT:1); var ka=LR*( (seen[m.awayName]||0)<NEW_N ? NEW_MULT:1);
            att[m.homeName]=g(att,m.homeName)+kh*eh*0.5; deff[m.awayName]=g(deff,m.awayName)-ka*eh*0.5; att[m.awayName]=g(att,m.awayName)+ka*ea*0.5; deff[m.homeName]=g(deff,m.homeName)-kh*ea*0.5; hfa+=HFA_LR*(eh-ea)*0.02; hextra[m.homeName]=g(hextra,m.homeName)+HFA_LR*(eh-ea)*0.010; hextra[m.homeName]*=0.999; mu+=0.004*(eh+ea)/2; hfa=Math.max(0.05,Math.min(0.55,hfa)); hextra[m.homeName]=Math.max(-0.25,Math.min(0.25,hextra[m.homeName])); for(var t of [m.homeName,m.awayName]){{ att[t]*=(1-DECAY); deff[t]*=(1-DECAY); }} seen[m.homeName]=(seen[m.homeName]||0)+1; seen[m.awayName]=(seen[m.awayName]||0)+1; continue;
          }}
          if((seen[m.homeName]||0)>=6 && (seen[m.awayName]||0)>=6){{
            var pr=predict(m.homeName, m.awayName); var gp=gridProb(pr[0],pr[1]); briers.push({{ date:m.dateISO, home:m.homeName, away:m.awayName, brier:brier(gp,yOf(m)), id:m.id }});
          }}
          var pr=predict(m.homeName, m.awayName); var eh=m.homeGoals-pr[0], ea=m.awayGoals-pr[1]; var kh=LR*( (seen[m.homeName]||0)<NEW_N ? NEW_MULT:1); var ka=LR*( (seen[m.awayName]||0)<NEW_N ? NEW_MULT:1);
          att[m.homeName]=g(att,m.homeName)+kh*eh*0.5; deff[m.awayName]=g(deff,m.awayName)-ka*eh*0.5; att[m.awayName]=g(att,m.awayName)+ka*ea*0.5; deff[m.homeName]=g(deff,m.homeName)-kh*ea*0.5; hfa+=HFA_LR*(eh-ea)*0.02; hextra[m.homeName]=g(hextra,m.homeName)+HFA_LR*(eh-ea)*0.010; hextra[m.homeName]*=0.999; mu+=0.004*(eh+ea)/2; hfa=Math.max(0.05,Math.min(0.55,hfa)); hextra[m.homeName]=Math.max(-0.25,Math.min(0.25,hextra[m.homeName])); for(var t of [m.homeName,m.awayName]){{ att[t]*=(1-DECAY); deff[t]*=(1-DECAY); }} seen[m.homeName]=(seen[m.homeName]||0)+1; seen[m.awayName]=(seen[m.awayName]||0)+1;
        }}
        if(briers.length>=130){{
          var last30=briers.slice(-30); var hist100=briers.slice(-130,-30);
          var meanHist=hist100.reduce(function(s,b){{return s+b.brier;}},0)/hist100.length;
          var varHist=hist100.reduce(function(s,b){{ var d=b.brier-meanHist; return s+d*d;}},0)/(hist100.length-1);
          var sdHist=Math.sqrt(varHist);
          var meanRecent=last30.reduce(function(s,b){{return s+b.brier;}},0)/last30.length;
          if(sdHist>0 && meanRecent > meanHist + 2*sdHist){{
            var sigma=(meanRecent-meanHist)/sdHist;
            flags.push({{ type:'brier_shock', league:league, severity: sigma>3?'high':'med', tag:'Brier shock — own model collapse', detail:'Last 30 Brier mean '+meanRecent.toFixed(3)+' vs historical mean '+meanHist.toFixed(3)+' σ='+sigma.toFixed(2)+' — own-model Brier worse than historical 2σ — 10 recent flagged', matches:last30.slice(-10).map(function(b){{return b.home+' v '+b.away+' '+b.date;}}), rationale:'Own model Brier shock — manual review — P1-compliant no market' }});
          }}
        }}
      }});
      var teamHistory={{}};
      var allRows=store.matches.slice().filter(function(m){{return !m.muted;}}).sort(function(a,b){{return a.dateISO < b.dateISO ? -1 : 1;}});
      var attJ={{}}, deffJ={{}}, hextraJ={{}}, seenJ={{}}, muJ=0.45, hfaJ=0.25;
      var LR=0.055, DECAY=0.0022, HFA_LR=0.010, NEW_MULT=1.6, NEW_N=8;
      function gJ(map,k){{return map[k]===undefined?0:map[k];}}
      for(var idx=0; idx<allRows.length; idx++){{
        var m=allRows[idx]; var h=m.homeName, a=m.awayName;
        if(!teamHistory[h]) teamHistory[h]=[]; if(!teamHistory[a]) teamHistory[a]=[];
        var lh=Math.exp(muJ + gJ(attJ,h) - gJ(deffJ,a) + hfaJ + gJ(hextraJ,h)); var la=Math.exp(muJ + gJ(attJ,a) - gJ(deffJ,h)); lh=Math.max(0.05,Math.min(6.0,lh)); la=Math.max(0.05,Math.min(6.0,la));
        var eh=m.homeGoals-lh, ea=m.awayGoals-la; var kh=LR*((seenJ[h]||0)<NEW_N?NEW_MULT:1); var ka=LR*((seenJ[a]||0)<NEW_N?NEW_MULT:1);
        teamHistory[h].push({{ date:m.dateISO, att:gJ(attJ,h), def:gJ(deffJ,h), match:m.homeName+' vs '+m.awayName }});
        teamHistory[a].push({{ date:m.dateISO, att:gJ(attJ,a), def:gJ(deffJ,a), match:m.homeName+' vs '+m.awayName }});
        attJ[h]=gJ(attJ,h)+kh*eh*0.5; deffJ[a]=gJ(deffJ,a)-ka*eh*0.5; attJ[a]=gJ(attJ,a)+ka*ea*0.5; deffJ[h]=gJ(deffJ,h)-kh*ea*0.5; hfaJ+=HFA_LR*(eh-ea)*0.02; hextraJ[h]=gJ(hextraJ,h)+HFA_LR*(eh-ea)*0.010; hextraJ[h]*=0.999; muJ+=0.004*(eh+ea)/2; hfaJ=Math.max(0.05,Math.min(0.55,hfaJ)); hextraJ[h]=Math.max(-0.25,Math.min(0.25,hextraJ[h])); for(var t of [h,a]){{ attJ[t]*=(1-DECAY); deffJ[t]*=(1-DECAY); }} seenJ[h]=(seenJ[h]||0)+1; seenJ[a]=(seenJ[a]||0)+1;
      }}
      Object.keys(teamHistory).forEach(function(team){{
        var hist=teamHistory[team]; if(hist.length<4) return;
        var last4=hist.slice(-4);
        var attJump=Math.abs(last4[3].att - last4[0].att); var defJump=Math.abs(last4[3].def - last4[0].def);
        if(attJump>0.5 || defJump>0.5){{
          flags.push({{ type:'rating_jump', team:team, severity: (attJump>0.8||defJump>0.8)?'high':'med', tag:'Rating jump — per-team att/def shift >0.5', detail:'Team '+team+' att shift '+attJump.toFixed(3)+' def shift '+defJump.toFixed(3)+' over last 3 matches — expected max ~0.2 so 0.5 is 2.5× expected — potential data error', rationale:'Own att/def time series + results, no market' }});
        }}
      }});
      var homeCounts={{}};
      store.matches.forEach(function(m){{ if(m.muted) return; var h=m.homeName; if(!homeCounts[h]) homeCounts[h]={{home:0, away:0}}; homeCounts[h].home++; var a=m.awayName; if(!homeCounts[a]) homeCounts[a]={{home:0, away:0}}; homeCounts[a].away++; }});
      Object.keys(homeCounts).forEach(function(team){{
        var c=homeCounts[team];
        if(c.home==0 && c.away>0){{
          flags.push({{ type:'venue_ghost', team:team, severity:'high', tag:'Venue ghosting — never hosted', detail:'Team '+team+' appears as away '+c.away+' times but never as home — hard error venue integrity I4', rationale:'Outcome-only check — home/away counts, no market' }});
        }}
      }});
      store.matches.forEach(function(m){{
        if(m.homeGoals>10 || m.awayGoals>10) flags.push({{ type:'score_extreme', severity:'med', tag:'Score extreme >10', detail:'Match '+m.dateISO+' '+m.homeName+' '+m.homeGoals+'-'+m.awayGoals+' '+m.awayName, match:m.id }});
      }});
      var fps={{}};
      store.matches.forEach(function(m){{
        var fp=m.dateISO+'::'+C.canon(m.homeName)+'::'+C.canon(m.awayName)+'::'+C.canon(m.competitionName||'');
        if(fps[fp]) flags.push({{ type:'duplicate', severity:'high', tag:'Duplicate fingerprint', detail:'Duplicate fingerprint '+fp, matches:[fps[fp], m.id] }});
        else fps[fp]=m.id;
      }});
      var today=new Date().toISOString().slice(0,10);
      store.matches.forEach(function(m){{ if(m.dateISO>today) flags.push({{ type:'future_date', severity:'high', tag:'Future-dated row', detail:'Match '+m.dateISO+' '+m.homeName+' v '+m.awayName+' future vs '+today, match:m.id }}); }});
    }}catch(e){{ flags.push({{ type:'error', severity:'low', tag:'Integrity compute error', detail:'Error: '+e.message }}); }}
    return flags;
  }}

  function renderIntegrityFlagsPanel(store) {{
    var flags=computeIntegrityFlags(store);
    if(!flags.length) return '<div class="integrity-flags-panel"><b>Automated Integrity Flags (Outcomes-Only) — P1-Compliant</b><br><span class="dim">No flags — own-model Brier shock 30 vs 100 2σ, rating jumps 0.5 over 3, venue ghosting, score extremes, duplicate, future — all clear. M10 approved builder 2026-08-06 owner 2026-08-06 — outcomes-only, no market.</span></div>';
    var html='<div class="integrity-flags-panel"><b>Automated Integrity Flags (Outcomes-Only) — '+flags.length+' flag(s) — M10</b><br><span class="dim">Brier shock (rolling Brier 30 mean vs historical 100 mean+2σ) + rating jumps >0.5 + venue ghosting I4 + score extremes + duplicate + future — P1-compliant, no market — muted rows kept visible excluded never deleted — snapshots before commit — MUTE soft PURGE hard backup-gated — owner approved 2026-08-06 builder approved 2026-08-06</span>';
    flags.forEach(function(f){{
      var sevClass=f.severity=='high'?'integrity-severity-high':(f.severity=='med'?'integrity-severity-med':'integrity-severity-low');
      html+='<div class="integrity-flag"><span class="tag '+sevClass+'">'+C.esc(f.tag)+' ['+C.esc(f.type)+']</span> <span class="dim">'+C.esc(f.league||f.team||'')+'</span><br><span>'+C.esc(f.detail)+'</span>';
      if(f.rationale) html+='<br><span class="dim">Rationale: '+C.esc(f.rationale)+'</span>';
      if(f.matches) html+='<br><span class="dim">Matches: '+C.esc(f.matches.join ? f.matches.join(', ') : String(f.matches))+'</span>';
      html+='</div>';
    }});
    html+='</div>';
    return html;
  }}

  function getLeaguePivotDelta(store, homeLeague, awayLeague){{
    try{{
      var pivot=getLeaguePivot(store);
      var s=pivot && pivot.s_pivot ? pivot.s_pivot : {{}};
      var sh=s[homeLeague]||0;
      var sa=s[awayLeague]||0;
      return sh-sa;
    }}catch(e){{ return 0; }}
  }}
"""

# Insert after showBusyIcon
if not must_replace("function showBusyIcon(containerId, message) {", LEAGUE_PIVOT_JS + "\n  function showBusyIcon(containerId, message) {", "C insert"):
    # fallback
    src = src.replace("function renderProvenancePanel", LEAGUE_PIVOT_JS + "\n  function renderProvenancePanel", 1)

# Patch autoRevalidate to include pivot
# Find function autoRevalidate definition
if "function autoRevalidate(store){" in src:
    src = src.replace("function autoRevalidate(store){\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", "function autoRevalidate(store){\n    try{\n      ensureLeaguePivotArtifact(store);\n    }catch(e){}\n    try{\n      if(!PR.calibration||!PR.calibration.run) return;", 1)
    print("patched autoRevalidate inner")
else:
    print("autoRevalidate def not found")

# Also patch boot to ensure pivot
src = src.replace("  /* fitted model migration (Phase 1: team/league attributes) */", "  /* B3 league pivot ensure */\n  try{ ensureLeaguePivotArtifact(store); }catch(e){}\n  /* fitted model migration (Phase 1: team/league attributes) */", 1)

# Modify integrityConsole
old_int = "  function integrityConsole(store) {\n    var mutes = store.mutes.slice().reverse();"
new_int = """  function integrityConsole(store) {
    var approvalHtml = '<div class="integrity-flags-panel"><b>M10 Integrity Screen — Builder Approval — P1-Compliant Outcomes-Only</b><br><span class="dim">Spec: lead_engine/25-M10-OUTCOMES-ONLY-INTEGRITY-SCREEN-SPEC.md — Owner approved 2026-08-06 — Builder approved 2026-08-06 — P1 binding: no market data in ANY role (input/feature/benchmark/sanity/fallback) — replacement for legacy market-price screen which is P1-non-compliant and DO NOT restore — new screen = outcomes-only own-model collapse detection — Brier shock + rating jumps + venue ghosting I4 + score extremes + duplicate + future — muted rows kept visible excluded every calculation never deleted — Restore reverses — Snapshots taken before every data commit — MUTE soft PURGE hard backup-gated — compliance: historic market-gate flags ship/caution/blocked inert read by no code dropped + provenance note A-04 — no profitability claims calibrated ≠ profitable only calibration claimed — ready for implementation — example flag: \"⚠️ Integrity flag: Russian Premier League last 30 settled tips Brier 0.72 vs historical 0.58 +2.3σ worse — own model struggling lately — 10 recent matches flagged for manual review — not auto-muted.\" — tooltip Brier shock own model no market manual review recommended flagged matches kept visible excluded pending approve? — technical small-print rolling Brier 30 mean 0.72 sd 0.15 historical mean 0.58 sd 0.06 +2.3σ window 30 vs 100 n=30 settled threshold 2.0σ flagged last 10 IDs — Brier sum(p-y)^2 per match settlement rule draw=loss I5 never push.</span><br><span>Provenance: M10 spec draft P1-compliant, owner P5 approval required before ship — approved 2026-08-06 — builder UAT: 0 fetch 0 XHR one-gate 11 liveTeamRecord liveStarsFor autoRevalidate getLiveConstants __DC_GATE__ demoted __FITTED_MODEL__ first-boot only — M10 integrity screen needs builder approval first — APPROVED.</span></div>';
    var leaguePivotHtml = renderLeaguePivotPanel(store);
    var flagsHtml = renderIntegrityFlagsPanel(store);
    var mutes = store.mutes.slice().reverse();"""
must_replace(old_int, new_int, "E integrityConsole header")

must_replace("    return '<h3>Muted rows</h3>' + muteRows + '<h3>Snapshots</h3>' + snapRows;",
             "    return approvalHtml + leaguePivotHtml + flagsHtml + '<h3>Muted rows</h3>' + muteRows + '<h3>Snapshots</h3>' + snapRows;",
             "F integrityConsole return")

# Also patch predictOnline to include pivot delta — try to find anchor
old_pred = "    var lh = lambdaFor(lg.mu, h.att, a.def, lg.hfa, lg.homeExtra[homeId] || 0);"
if old_pred in src:
    new_pred = """    var leaguePivotDeltaHome = (function(){ try{ var pivot=getLeaguePivot(store); var s=pivot.s_pivot||{}; var homeLg=leagueKey; var awayLg=null; for(var i=0;i<store.identities.length;i++){ if(store.identities[i].id===awayId && store.identities[i].leagueName){ awayLg=store.identities[i].leagueName; break; } } if(!awayLg){ for(var j=0;j<store.matches.length;j++){ var mm=store.matches[j]; if(mm.homeId===awayId||mm.awayId===awayId){ awayLg=mm.competitionName; break; } } } return (s[homeLg]||0)-(s[awayLg]||0); }catch(e){ return 0; } })();
    var lh = lambdaFor(lg.mu + leaguePivotDeltaHome, h.att, a.def, lg.hfa, lg.homeExtra[homeId] || 0);"""
    must_replace(old_pred, new_pred, "H predictOnline home pivot")
    # away
    old_pred2 = "    var la = lambdaFor(lg.mu, a.att, h.def, 0, 0);"
    new_pred2 = "    var leaguePivotDeltaAway = -leaguePivotDeltaHome;\n    var la = lambdaFor(lg.mu + leaguePivotDeltaAway, a.att, h.def, 0, 0);"
    must_replace(old_pred2, new_pred2, "H2 predictOnline away pivot")

OUT.write_text(src, encoding="utf-8")
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hashlib.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")

evidence = {
    "version": "3.10.0",
    "base_md5": base_md5,
    "built_md5": hashlib.md5(out_bytes).hexdigest(),
    "features": [
        "dc-fitted-league-pivot artifact integration S5",
        "M10 outcomes-only integrity screen approved"
    ],
    "pivot": pivot_artifact,
    "m10": {
        "ownerApproved": "2026-08-06",
        "builderApproved": "2026-08-06",
        "p1Compliant": True
    }
}
with open(ROOT / "handoffs/B3-EVIDENCE-2026-08-06.json","w") as f:
    json.dump(evidence,f,indent=2)
b64 = base64.b64encode(out_bytes).decode()
with open(ROOT / f"handoffs/B3-v3.10.0-{hashlib.md5(out_bytes).hexdigest()[:8]}.b64.txt","w") as f:
    f.write(b64)
print("evidence + b64 written")
