#!/usr/bin/env python3
# Build app-v2.6-cross.html from app-v2.5-final.html
# Part B: BlueprintEmbed ("Data" tab) edits.
# Every replacement is exact-match and counted; failures abort the build.
import re, sys

SRC = "/home/user/app-v2.6-cross.html"   # output of Part A
s = open(SRC, encoding="utf-8").read()
edits = 0

def rep(old, new, count=1, tag=""):
    global s, edits
    n = s.count(old)
    if n != count:
        print("FAIL [%s]: found %d occurrences, expected %d" % (tag, n, count)); sys.exit(1)
    s = s.replace(old, new)
    edits += 1
    print("ok  [%s]" % tag)

def block(start, end, new, tag=""):
    global s, edits
    i = s.find(start); j = s.find(end, i)
    if i == -1 or j == -1:
        print("FAIL [%s]: anchors not found" % tag); sys.exit(1)
    s = s[:i] + new + s[j:]
    edits += 1
    print("ok  [%s]" % tag)

# ---------- 1. version strings ----------
rep("blueprint-embed-v0.5-live", "blueprint-embed-v0.6-live", count=None if False else s.count("blueprint-embed-v0.5-live"), tag="bp version 0.5->0.6")
rep("/*\n  Pitch Rating — Live Blueprint Embed v0.4", "/*\n  Pitch Rating — Live Blueprint Embed v0.6", count=1, tag="embed header comment")
rep("BP={version:'blueprint-embed-v0.4',identities:{}", "BP={version:'blueprint-embed-v0.6-live',identities:{}", count=1, tag="clearData version")

# ---------- 1b. merge-on-add in addIdentity (prevents __AMBIG__ splits) ----------
rep('    var key=idKey(country,name);\n', "    var key=idKey(country,name);\n    /* merge-on-add: the same canonical club arriving via a verified pack with a\n       corrected country (e.g. Wales|Swansea vs heuristic England|Swansea) must\n       not split into a second identity — a split poisons its aliases to\n       __AMBIG__ and hides the club from the evidence engine. Overlap of a\n       league tag plus identical name identifies the same club, and the\n       pack-verified country wins over the league-map heuristic. */\n    if(!BP.identities[key]){\n      var mergeKey=null, nn=norm(name);\n      Object.keys(BP.identities).forEach(function(k){\n        if(mergeKey) return;\n        var it=BP.identities[k];\n        if(norm(it.name)!==nn) return;\n        if(league && (it.leagues||[]).indexOf(league)!==-1) mergeKey=k;\n      });\n      if(mergeKey){\n        var it=BP.identities[mergeKey];\n        if(/^MODEL\\./.test(it.source||'') && !/^MODEL\\./.test(source||'')) it.country=country;\n        it.source=source||it.source;\n        key=mergeKey;\n      }\n    }\n", count=1, tag="merge-on-add")

# ---------- 2. identity dedupe (Swansea Wales/England split) ----------
rep("  function normalizeStore(){", r'''  function dedupeIdentities(){
    /* Same club recorded under two country keys (e.g. a MODEL-bootstrap row
       England|Swansea and a verified pack row Wales|Swansea) aliases to
       __AMBIG__ and becomes invisible to the evidence engine. Merge only when
       the canonical name matches AND league tags overlap — that combination
       identifies the same club, not a foreign namesake. */
    var keys=Object.keys(BP.identities), byName={}, merged=0, k, i, j;
    keys.forEach(function(k){var n=norm(BP.identities[k].name); (byName[n]=byName[n]||[]).push(k);});
    Object.keys(byName).forEach(function(n){
      var arr=byName[n]; if(arr.length<2)return;
      for(i=0;i<arr.length;i++)for(j=i+1;j<arr.length;j++){
        var A=BP.identities[arr[i]], B=BP.identities[arr[j]]; if(!A||!B)continue;
        var overlap=(A.leagues||[]).some(function(l){return (B.leagues||[]).indexOf(l)!==-1;});
        if(!overlap)continue;
        var keep=(/^MODEL\./.test(A.source||'') && !/^MODEL\./.test(B.source||''))?B:A;
        var drop=(keep===A)?B:A;
        (drop.leagues||[]).forEach(function(l){if(keep.leagues.indexOf(l)===-1)keep.leagues.push(l);});
        (drop.aliases||[]).forEach(function(a){if(keep.aliases.indexOf(a)===-1)keep.aliases.push(a);
          var na=norm(a); if(!BP.aliases[na]||BP.aliases[na]==='__AMBIG__')BP.aliases[na]=keep.id;});
        var dk=drop.id;
        BP.matches.forEach(function(m){if(m.homeId===dk)m.homeId=keep.id; if(m.awayId===dk)m.awayId=keep.id;});
        if(BP.teamStats[dk] && !BP.teamStats[keep.id]) BP.teamStats[keep.id]=BP.teamStats[dk];
        delete BP.teamStats[dk];
        if(BP.venues[dk] && !BP.venues[keep.id]) BP.venues[keep.id]=BP.venues[dk];
        delete BP.venues[dk];
        Object.keys(BP.aliases).forEach(function(a){ if(BP.aliases[a]===dk) BP.aliases[a]=keep.id; });
        var nself=norm(drop.name); if(BP.aliases[nself]==='__AMBIG__') BP.aliases[nself]=keep.id;
        delete BP.identities[dk]; merged++; arr[arr.indexOf(dk)]=keep.id;
      }
    });
    if(merged && typeof console!=='undefined' && console.info) console.info('identity dedupe merged', merged);
  }
  function normalizeStore(){''', count=1, tag="dedupeIdentities added")
rep("if(BP.calibration===undefined) BP.calibration=null;\n  }", "if(BP.calibration===undefined) BP.calibration=null;\n    dedupeIdentities();\n  }", count=1, tag="normalizeStore dedupe call")

# ---------- 3. remove forcedLine entirely (no forced probabilities anywhere) ----------
block("  function forcedLine(estimate, spread){", "  function renderBPStatus(){", "", tag="forcedLine removed")
rep("GAP: cross-border calibration tables are not loaded; cross-border percentages must remain withheld except forced line.",
    "GAP: cross-border calibration tables are not loaded; cross-border percentages remain withheld until validated.", count=1, tag="gap text")

# ---------- 4. populateBPTeams -> team request list ----------
block("  function populateBPTeams(){", "  function injectRateCompetitionFields(){", r'''  /* Team list for the Data tab: every rated row plus every loaded identity.
     The Data tab requests/loads TEAM DATA only — never a fixture. Sort order
     is the user's choice: league A-Z (grouped) or team A-Z (flat). */
  function populateBPTeams(){
    var h=document.getElementById('bpTeams'); if(!h||typeof MODEL==='undefined')return;
    var keep={}; var i;
    for(i=0;i<h.options.length;i++) if(h.options[i].selected) keep[h.options[i].value]=1;
    var rated=[];
    Object.keys(MODEL.teams||{}).sort(function(x,y){return MODEL.leagues[x].name.localeCompare(MODEL.leagues[y].name);}).forEach(function(lg){
      Object.keys(MODEL.teams[lg]||{}).sort().forEach(function(t){rated.push({v:lg+'||'+t,label:t+' — '+MODEL.leagues[lg].name});});
    });
    var manual=[];
    Object.keys(BP.identities||{}).forEach(function(k){
      var it=BP.identities[k];
      var appLeague=(it.leagues||[]).some(function(lg){return MODEL.teams&&MODEL.teams[lg]&&MODEL.teams[lg][it.name];});
      if(appLeague) return;
      manual.push({v:'BP::'+it.country+'||'+it.name,label:it.name+' — '+it.country+' / '+((it.leagues&&it.leagues[0])||'loaded team data')});
    });
    manual.sort(function(x,y){return x.label.localeCompare(y.label);});
    var sortEl=document.getElementById('bpTeamSort');
    var mode=sortEl?sortEl.value:'league';
    var all;
    if(mode==='team'){ all=rated.concat(manual).sort(function(x,y){return x.label.localeCompare(y.label);}); }
    else { all=rated.concat(manual); }
    h.innerHTML=all.map(function(x){return '<option value="'+esc(x.v)+'">'+esc(x.label)+'</option>';}).join('');
    for(i=0;i<h.options.length;i++) if(keep[h.options[i].value]) h.options[i].selected=true;
  }

''', tag="populateBPTeams")

# ---------- 5. team-only load request ----------
block("  function buildTeamLoadRequest(){", "  function exportBPData(){", r'''  function teamFromSelectedOptions(){
    var sel=document.getElementById('bpTeams'), teams=[];
    if(!sel) return teams;
    for(var i=0;i<sel.options.length;i++){
      if(sel.options[i].selected){ var t=teamFromSelectValue(sel.options[i].value); if(t) teams.push(t); }
    }
    return teams;
  }

  function buildTeamLoadRequest(){
    var teams=teamFromSelectedOptions();
    var msg=document.getElementById('bpReqMsg');
    if(!teams.length){ if(msg)msg.textContent='Select one or more teams first.'; return ''; }
    var cutoff=todayISO();
    var names=teams.map(function(t){return t.name+' ('+t.country+')';}).join('; ');
    var L=[];
    L.push('You are preparing a FULL TEAM DATA LOAD for Pitch Rating Live Blueprint.');
    L.push('Return one BP-TEAM-PACK v2 block as plain text only. No prose before or after. No markdown links. No backticks around rows. If your interface auto-formats links, attach a .txt file.');
    L.push('');
    L.push('REQUEST TYPE: TEAM DATA ONLY. This is not a fixture request and implies no pairing or tournament pick. '+(teams.length===1?'One team requested.':teams.length+' teams requested — research each independently and combine into one block.'));
    L.push('TEAMS TO LOAD: '+names);
    L.push('EVIDENCE CUTOFF: '+cutoff+' — only completed matches before this date are evidence.');
    L.push('');
    L.push('STRICT RESEARCH RULES');
    L.push('1. Results only: no odds, predictions, injuries, lineups, suspensions, transfers, or market prices.');
    L.push('2. Use only completed matches before '+cutoff+'. No future fixtures.');
    L.push('3. Dates must be exact ISO YYYY-MM-DD. Do not use placeholder season dates.');
    L.push('4. Scores must be full-time after 90 minutes plus stoppage, not extra time or penalties.');
    L.push('5. Home/away order must be official. Verify venue against an official fixture list where possible.');
    L.push('5b. Every MATCH row records its competition exactly: league, domestic cup, UEFA competition, friendly, or custom tournament.');
    L.push('6. VenueTreatment values: normal, relocated, neutral. Use relocated when a club is listed home but not using its regular home ground.');
    L.push('7. Full team pack means: identity + venue + season aggregate + form aggregate + completed match rows, not just competition table.');
    L.push('8. If uncertain, omit the row and add NOTE|blocker. Do not invent.');
    L.push('9. Self-audit before delivery: season arithmetic, form-vs-match arithmetic, source labels, allowed competitionType, allowed venueTreatment, and plain URLs.');
    L.push('');
    L.push('REQUIRED DATA PER TEAM');
    L.push('- Canonical club identity, country, domestic league, aliases, normal home stadium.');
    L.push('- Most recently completed domestic league season: overall plus home/away W-D-L and GF/GA.');
    L.push('- Current season aggregate if competitive matches have already started; otherwise omit.');
    L.push('- Last 15 completed matches in all competitions before cutoff. Include domestic, cups, and UEFA matches.');
    L.push('- All completed European/cross-border matches in the current and previous 2 seasons if available.');
    L.push('- Direct H2H and common-opponent match rows against any verifiable opponents, so the evidence graph can connect this team to any future opponent.');
    L.push('- LEVEL-3 BRIDGE REQUIREMENT: for the strongest/recent 5 opponents in the last-15 list, add 3-5 recent completed MATCH rows involving those opponents against other teams before cutoff, with SOURCE rows. These allow MainTeam→Opponent→BridgeTeam←Opponent←OtherTeam analysis.');
    L.push('- If no level-3 bridge rows can be verified, add NOTE|warning explaining what was checked.');
    L.push('- Add SOURCE rows for every source used.');
    L.push('');
    L.push('OUTPUT FORMAT — RETURN ONLY THIS PLAIN TEXT BLOCK');
    L.push('BP-TEAM-PACK v2');
    L.push('NOTE|info|research_ack|ACKNOWLEDGED — I verified time-sensitive facts against current sources, used plain URLs only, marked unverifiable items with NOTE blocker instead of guessing, self-audited before delivery, and returned one parseable BP-TEAM-PACK v2 block only.');
    L.push('TEAM|canonical|country|appLeagueContext|appLeagueCode|alias1;alias2|normalStadium|venueCity|venueCountry|surface|capacity|founded|officialWebsite');
    L.push('VENUE|team|stadium|city|country|surface|capacity|notes');
    L.push('SEASON|team|season|competition|scope|P|W|D|L|GF|GA|HP|HW|HD|HL|HGF|HGA|AP|AW|AD|AL|AGF|AGA|pos|pts');
    L.push('FORM|team|scope|throughDate|matches|W|D|L|GF|GA|cleanSheets|failToScore|over25|under25');
    L.push('MATCH|date|competition|competitionType|home|homeGoals|awayGoals|away|venueTreatment|stadium|city|country|tieId|sourceLabel');
    L.push('SOURCE|sourceLabel|url|accessedDate|sourceType|notes');
    L.push('END');
    L.push('');
    L.push('EXAMPLE ROWS — replace with researched data');
    L.push('SEASON|Example FC|2025-26|Example League|domestic league|36|18|5|13|58|50|18|9|2|7|30|27|18|9|3|6|28|23|2|59');
    L.push('FORM|Example FC|last 15 all competitions|'+cutoff+'|15|8|2|5|25|18|4|3|9|6');
    L.push('MATCH|2026-07-23|UECL Q2|uefa-conference-league|Example FC|2|0|Opponent FC|relocated|National Stadium|Capital|Country|EXA-OPP-2026-Q2|source1');
    L.push('SOURCE|source1|https://example.com/match-report|'+cutoff+'|official|official or results page');
    L.push('END');
    if(msg)msg.textContent=teams.length+' team(s) requested — send to the researcher, paste the returned block into the loader below. Loaded teams are selectable immediately on Rate a match.';
    return L.join('\n');
  }

  function generateTeamLoadRequest(){
    var txt=buildTeamLoadRequest();
    var box=document.getElementById('bpRequestBox'); if(box && txt){box.value=txt; box.focus(); box.select();}
  }
  function copyTeamLoadRequest(){
    var box=document.getElementById('bpRequestBox'); if(!box||!box.value)return; box.select();
    try{document.execCommand('copy');}catch(e){}
    if(navigator.clipboard){try{navigator.clipboard.writeText(box.value);}catch(e){}}
    var msg=document.getElementById('bpReqMsg'); if(msg)msg.textContent='Copied.';
  }

''', tag="team load request rewrite")

# ---------- 6. drop getBPCompetition (no competition on Data tab) ----------
block("  function getBPCompetition(){", "  function dedupeIdentities(){", "", tag="getBPCompetition removed")

# ---------- 7. Data tab view: remove fixture context card, team-request card ----------
block("    div.innerHTML=''+", "  function showBlueprint(){", r'''    div.innerHTML=''+
      '<div id="bpStatus" class="banner ban-info"></div>'+
      '<div class="card"><h2>What this page is</h2><div class="help" style="margin:0">This page <b>loads and requests team data only</b>. It is not a fixture page: no pairing, no tournament pick, no analysis. Request data for one team or many teams, paste the returned pack into the loader, then go to <b>Rate a match</b> — every loaded team is immediately selectable there against any other side.</div></div>'+
      '<div class="card"><h2>Team data load request</h2><div class="help">Generates the exact research request for full team packs (identity, venue, season, form, completed match rows, sources). Single-team or multi-team requests.</div>'+
      '<div class="row2" style="margin-bottom:9px"><div><label class="fl">Organise list</label><select id="bpTeamSort" onchange="BlueprintEmbed.refreshTeams()"><option value="league">League A–Z, then team</option><option value="team">Team A–Z</option></select></div><div><label class="fl">Teams to request (one or more — ctrl/cmd-click for several)</label><div class="help" style="margin:3px 0 0">Teams you load appear under their country, and on Rate a match immediately.</div></div></div>'+
      '<select id="bpTeams" multiple size="14" style="width:100%;border:1px solid var(--line);border-radius:7px;padding:7px 9px;font-size:13px;background:#fff;color:var(--ink);font-family:inherit"></select>'+
      '<div style="margin-top:9px;display:flex;gap:9px;flex-wrap:wrap;align-items:center"><button class="btn" onclick="BlueprintEmbed.request()">Generate team data request</button> <button class="btn2" onclick="BlueprintEmbed.copyRequest()">Copy</button> <span class="help" id="bpReqMsg" style="margin:0"></span></div>'+
      '<textarea id="bpRequestBox" rows="12" readonly onclick="this.select()" style="margin-top:10px;width:100%;border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px"></textarea></div>'+
      '<div class="card"><h2>Evidence data loader</h2><div class="help">Load BP-TEAM-PACK or BP-MATCHES rows. Everything is validated before anything is stored; strict evidence cutoff is applied at calculation time.</div>'+
      '<textarea id="bpImportText" rows="8" style="width:100%;border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px" placeholder="BP-TEAM-PACK v1\nTEAM|Malisheva|Kosovo|Kosovo Superliga|FC Malisheva;KF Malisheva|Liman Gegaj Stadium|Malishevë|Kosovo|artificial|1800\nSEASON|Malisheva|2025-26|Kosovo Superliga|domestic league|36|18|5|13|58|50|18|9|2|7|30|27|18|9|3|6|28|23|2|59\nMATCH|2026-07-23|UECL Q2|Malisheva|2|0|Hibernian|relocated|Fadil Vokrri Stadium|Pristina|Kosovo|MAL-HIB-2026-Q2|source1\nSOURCE|source1|https://example.com|2026-07-30|replace with source\nEND"></textarea>'+
      '<div style="margin-top:9px"><button class="btn2" onclick="BlueprintEmbed.importData()">Validate and load data</button> <button class="btn2" onclick="BlueprintEmbed.loadExample()">Insert Hibernian–Malisheva example</button> <button class="btnred" onclick="BlueprintEmbed.clearData()">Clear blueprint match store</button></div><div id="bpImportReport" style="margin-top:10px"></div></div>'+
      '<div class="card"><h2>Blueprint data backup</h2><div class="help">Export before loading large research batches. Import restores identities, team packs, venues, sources, matches and calibration metadata.</div><button class="btn2" onclick="BlueprintEmbed.exportData()">Export blueprint data</button> <button class="btn2" onclick="document.getElementById(\'bpBackupFile\').click()">Import blueprint data</button><input id="bpBackupFile" type="file" accept="application/json" class="hidden" onchange="BlueprintEmbed.importBackup(event)"><div id="bpBackupReport" style="margin-top:10px"></div></div>'+
      '<div class="card"><h2>UI self-test</h2><div class="help">Browser-side audit for the embedded build. Use this instead of manual screenshot checks for basic functionality.</div><button class="btn2" onclick="BlueprintEmbed.selfTest()">Run UI self-test</button><textarea id="bpSelfTestOut" rows="8" readonly style="margin-top:10px;width:100%;border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px"></textarea></div>'+
      '<div class="card"><h2>App team audit</h2><div class="help">Audits rated-team coverage, duplicate names across contexts, and missing app record rows. This is the first gate before full evidence packs are attached.</div><button class="btn2" onclick="BlueprintEmbed.audit()">Run app-team audit</button><textarea id="bpAuditOut" rows="12" readonly style="margin-top:10px;width:100%;border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px"></textarea></div>';
    if(!already) wrap.insertBefore(div, foot);
    populateBPTeams(); renderBPStatus();
  }

''', tag="Data tab cards replaced")

# ---------- 8. remove patchRenderRate (Rate page now dispatches natively) ----------
block("  function patchRenderRate(){", "  function patchShowView(){", "", tag="patchRenderRate removed")
rep("patchRenderRate(); ", "", count=1, tag="patchRenderRate boot call removed")

# ---------- 9. appendRateBlueprintAudit: resolve via new pickers ----------
block("  function appendRateBlueprintAudit(){", "  window.BlueprintEmbed={", r'''  function appendRateBlueprintAudit(){
    try{
      var out=document.getElementById('result'); if(!out) return;
      if(!window.__parsePick) return;
      var hp=window.__parsePick(document.getElementById('homeTeam').value);
      var ap=window.__parsePick(document.getElementById('awayTeam').value);
      if(!hp||!ap) return;
      var hid=resolveName(hp.name,hp.country), aid=resolveName(ap.name,ap.country);
      if(!hid||!aid) return;
      var cutoff=(document.getElementById('matchDate')&&document.getElementById('matchDate').value)||todayISO();
      var paths=buildEvidence(hid,aid,cutoff);
      if(!paths.length) return; // no noisy placebo on main screen
      var ag=aggregate(paths);
      var cl=classify(paths, ag, false); // cross-evidence calibration gate stays honest
      var direction=ag.weighted>0.25?'home lean':ag.weighted<-0.25?'away lean':'draw/neutral lean';
      var html='<div class="card"><h2>Blueprint evidence audit</h2><div class="help">Main-screen audit from loaded team/match data. This supports the rating above; it does not replace calibrated domestic probabilities.</div>'+
        PitchEvidenceBalance.render({home:{weight:ag.homeW,paths:ag.homeN},draw:{weight:ag.neuW,paths:ag.neuN},away:{weight:ag.awayW,paths:ag.awayN},estimate:ag.weighted,alignment:direction+'; agreement '+(ag.agree*100).toFixed(0)+'%',effectivePaths:ag.effective,context:'loaded graph rows '+BP.matches.length,confidence:cl.label,goalRange:{low:null,exact2:null,high:null}})+
        '<details style="margin-top:10px"><summary style="cursor:pointer;font-weight:650">Evidence paths</summary><table><thead><tr><th>Phase</th><th>Path</th><th class="num">Estimate</th><th class="num">Weight</th></tr></thead><tbody>'+paths.map(function(p){return '<tr><td>'+esc(p.phase)+'</td><td>'+esc(p.label)+(p.detail?'<div class="help" style="margin:3px 0 0">'+esc(p.detail)+'</div>':'')+'</td><td class="num">'+p.estimate.toFixed(2)+'</td><td class="num">'+p.weight.toFixed(2)+'</td></tr>';}).join('')+'</tbody></table></details></div>';
      out.insertAdjacentHTML('beforeend', html);
    } catch(e){ /* never break the main rating screen */ }
  }

''', tag="appendRateBlueprintAudit rewrite")

# ---------- 10. BlueprintEmbed public API: add evidence compute + identity ----------
block("  window.BlueprintEmbed={", "\n\n\n  var HIB_MAL_SEED_PACK", r'''  window.BlueprintEmbed={
    calculate:calculateBP,
    importData:importBP,
    audit:auditAppTeams,
    selfTest:runUISelfTest,
    updateCompetitionCustom:updateCompetitionCustom,
    show:showBlueprint,
    appendAudit:function(){ appendRateBlueprintAudit(); },
    resolve:function(name,country){ return resolveName(name,country); },
    competition:function(){ return getRateCompetition(); },
    teamCard:function(hid,aid){ return teamPackCard(hid,aid); },
    analyze:function(hid,aid,cutoff){
      var paths=buildEvidence(hid,aid,cutoff);
      var ag=paths.length?aggregate(paths):null;
      var cl=classify(paths, ag||{}, false);
      return {paths:paths, ag:ag, cl:cl, rows:BP.matches.length};
    },
    clearData:function(){if(!confirm('Clear imported blueprint matches, team packs and manual identities? App ratings remain unchanged.'))return; BP={version:'blueprint-embed-v0.6-live',identities:{},aliases:{},matches:[],teamStats:{},venues:{},sources:[],loadedAt:null,calibration:null}; bootstrapIdentities(); saveStore(); populateBPTeams(); renderBPStatus(); if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}} document.getElementById('bpImportReport').innerHTML='<div class="banner ban-ok">Blueprint match store cleared.</div>';},
    request:generateTeamLoadRequest,
    copyRequest:copyTeamLoadRequest,
    refreshTeams:populateBPTeams,
    exportData:exportBPData,
    importBackup:importBPDataFile,
    loadExample:function(){document.getElementById('bpImportText').value='BP-TEAM-PACK v1\nTEAM|Malisheva|Kosovo|Kosovo Superliga|FC Malisheva;KF Malisheva;KF UV Malisheva|Liman Gegaj Stadium|Malishevë|Kosovo|artificial|1800\nVENUE|Malisheva|Liman Gegaj Stadium|Malishevë|Kosovo|artificial|1800|normal domestic home; European home can be relocated\nSEASON|Malisheva|2025-26|Kosovo Superliga|domestic league|36|18|5|13|58|50|18|9|2|7|30|27|18|9|3|6|28|23|2|59\nFORM|Malisheva|last 10 all competitions|2026-07-30|10|7|1|2|23|10|4|0|6|4\nTEAM|Vllaznia|Albania|Albanian Superliga|Vllaznia Shkoder;KF Vllaznia|Loro Boriçi Stadium|Shkodër|Albania|grass|16000\nMATCH|2026-07-09|UECL Q1|Vllaznia|2|1|Malisheva|normal|Loro Boriçi Stadium|Shkodër|Albania|MAL-VLL-2026-Q1|example\nMATCH|2026-07-15|UECL Q1|Malisheva|5|0|Vllaznia|relocated|Kampi Nacional|Hajvali|Kosovo|MAL-VLL-2026-Q1|example\nMATCH|2026-07-23|UECL Q2|Malisheva|2|0|Hibernian|relocated|Fadil Vokrri Stadium|Pristina|Kosovo|MAL-HIB-2026-Q2|example\nSOURCE|example|research-required|2026-07-30|replace example source rows with real URLs before final audit\nEND';},
    store:function(){return BP;}
  };''', tag="BlueprintEmbed API")

# ---------- 11. refresh Rate pickers after every load/clear/backup ----------
rep("saveStore(); if(typeof populateBPTeams==='function') populateBPTeams(); return out;",
    "saveStore(); if(typeof populateBPTeams==='function') populateBPTeams(); if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}} return out;",
    count=1, tag="v1 parser refresh hook")
rep("BP.loadedAt=todayISO(); saveStore(); applySeasonStatsToModel(); if(typeof populateBPTeams==='function') populateBPTeams();\n    return out;",
    "BP.loadedAt=todayISO(); saveStore(); applySeasonStatsToModel(); if(typeof populateBPTeams==='function') populateBPTeams(); if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}\n    return out;",
    count=1, tag="v2 parser refresh hook")
rep("normalizeStore(); saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus();",
    "normalizeStore(); saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus(); if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}",
    count=1, tag="backup import refresh hook")

# ---------- 12. boot: wire refresh hook ----------
rep("      loadStore(); bootstrapIdentities();\n      patchShowView(); patchSaveRating();",
    "      loadStore(); bootstrapIdentities();\n      window.__bpRefreshPickers=function(){ if(typeof onLeagueChange==='function') onLeagueChange(); };\n      patchShowView(); patchSaveRating();",
    count=1, tag="boot refresh hook")
rep("      renderBPStatus(); populateBPTeams();\n    } catch(e){",
    "      renderBPStatus(); populateBPTeams();\n      if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}\n    } catch(e){",
    count=1, tag="boot final refresh")

# ---------- 13b. restore patchShowView (ordering: it sat between appendRate and API) ----------
rep("  window.BlueprintEmbed={", '''  function patchShowView(){
    if(window.__bpShowViewPatched)return; window.__bpShowViewPatched=true;
    var old=window.showView;
    window.showView=function(v){ var bp=document.getElementById('viewBlueprint'); if(bp)bp.className='hidden'; var tb=document.getElementById('tabBlueprint'); if(tb)tb.className='tab'; return old.apply(this, arguments); };
  }

  window.BlueprintEmbed={''', count=1, tag="patchShowView restored")

# ---------- 13c. self-test updates ----------
rep("      pass('Data-tab competition field exists', !!document.getElementById('bpCompetition'));",
    r'''      pass('Team request selector exists on Data tab', !!document.getElementById('bpTeams'));
      pass('No fixture pickers on Data tab', !document.getElementById('bpHome') && !document.getElementById('bpAway') && !document.getElementById('bpDate') && !document.getElementById('bpCompetition'));
      {
        var hsel=document.getElementById('homeTeam');
        var phtml=hsel?hsel.innerHTML:'';
        pass('Rate picker exposes cross-league rated teams', phtml.indexOf('R|E0|Arsenal')!==-1 && phtml.indexOf('R|D1|Bayern Munich')!==-1);
        pass('Rate picker exposes Data-tab loaded teams', phtml.indexOf('B|Kosovo|Malisheva')!==-1, 'B|Kosovo|Malisheva option');
        pass('Cross-league bridge computes', typeof lambdasCross==='function' && !!lambdasCross('E0','Arsenal','D1','Bayern Munich'));
      }''', count=1, tag="self-test picker checks")

# ---------- 9. loader: pick a pack text file straight from drive (no copy/paste) ----------
rep(r'''Clear blueprint match store</button></div><div id="bpImportReport"''',
    r'''Clear blueprint match store</button></div><div style="margin-top:9px"><input type="file" id="bpPackFile" accept=".txt,text/plain" style="font-size:12.5px" onchange="BlueprintEmbed.loadPackFile(event)"><div class="help" style="margin:6px 0 0">Or pick a BP-TEAM-PACK text file (.txt) straight from your drive — the full text lands in the loader box above. Review it, then click Validate and load data.</div></div><div id="bpImportReport"''',
    count=1, tag="pack file picker markup")
rep('  function importBPDataFile(ev){', r'''  function loadPackFile(ev){
    /* Drive picker for the pack loader: reads a .txt BP-TEAM-PACK file into the
       loader box. Nothing is applied on read — the Validate step stays the
       single point where data enters the store. */
    var f=ev.target.files && ev.target.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(){
      var box=document.getElementById('bpImportText'); if(box) box.value=String(rd.result||'');
      var el=document.getElementById('bpImportReport');
      if(el) el.innerHTML='<div class="banner ban-info">File <b>'+esc(f.name)+'</b> read ('+(box?box.value.length:0)+' characters) into the loader box. Review it, then click <b>Validate and load data</b>.</div>';
      ev.target.value='';
    };
    rd.onerror=function(){ var el=document.getElementById('bpImportReport'); if(el) el.innerHTML='<div class="banner ban-err">Could not read that file.</div>'; ev.target.value=''; };
    rd.readAsText(f);
  }
  function importBPDataFile(ev){''', count=1, tag="loadPackFile function")
rep("    importBackup:importBPDataFile,",
    "    importBackup:importBPDataFile,\n    loadPackFile:loadPackFile,", count=1, tag="loadPackFile api")

# ---------- 10. plain-language balance summary + explicit NO PLAY on the cross verdict card ----------
rep('function renderEvidenceFixture(hp, ap) {', '''/* Plain-language summary strip — mirrors classify() decision order exactly so the
   wording can never drift from the engine. Home-perspective, results-only. The
   NO PLAY statement is explicit: evidence balance is never a recommendation, and
   no percentage is shown without a calibrated table. */
function evidenceSummaryHtml(hp, ap, ag, cl, pathCount) {
  var dirTxt;
  if (!ag) {
    dirTxt = "No evidence path connects these sides, so the balance shows no direction.";
  } else if (ag.weighted > 0.25) {
    dirTxt = "Evidence balance leans " + esc(hp.name) + " (home).";
  } else if (ag.weighted < -0.25) {
    dirTxt = "Evidence balance leans " + esc(ap.name) + " (away).";
  } else {
    dirTxt = "Evidence balance shows no clear side — the margin sits inside the neutral band.";
  }
  var countsTxt = ag ?
    " Weighted support — home " + ag.homeW.toFixed(2) + " · draw " + ag.neuW.toFixed(2) +
    " · away " + ag.awayW.toFixed(2) + " across " + pathCount + " path(s), " +
    ag.effective.toFixed(0) + " effective independent." : "";
  var head, body, stripCls;
  if (!ag || !cl) {
    stripCls = "ban-warn"; head = "NO PLAY — no recommendation.";
    body = "Load team data covering H2H, common opponents or level-3 bridge rows to open evidence.";
  } else if (ag.effective < 2) {
    stripCls = "ban-warn"; head = "NO PLAY — no recommendation.";
    body = "Only " + ag.effective.toFixed(0) + " effective independent evidence path(s); the blueprint requires at least 2 independent routes before any lean is actionable. The lean shown is information, not a call.";
  } else if (ag.agree < 0.60 || Math.abs(ag.weighted) < 0.35) {
    stripCls = "ban-warn"; head = "NO PLAY — no recommendation.";
    body = "Evidence is too split between sides, or the aggregate margin too thin, to carry a call.";
  } else if (cl.label.indexOf("Calibrated") === -1) {
    stripCls = "ban-warn"; head = "NO PLAY — no recommendation.";
    body = "The lean clears the independence bar (" + ag.effective.toFixed(0) + " effective paths), but no calibrated cross-border table is loaded. With no calibrated table there is no percentage, and with no percentage there is no play.";
  } else {
    stripCls = "ban-ok"; head = "Calibrated read available.";
    body = "This fixture sits inside the calibrated domestic model; the match probabilities above carry the recommendation context.";
  }
  return '<div class="banner ' + stripCls + '" style="margin:0 0 10px"><b>Balance summary.</b> ' +
    dirTxt + countsTxt + "<br><b>" + head + "</b> " + body + "</div>";
}

function renderEvidenceFixture(hp, ap) {''', count=1, tag="evidence summary strip function")
rep('''    '<div class="banner ' + bannerCls + '"><b>' + esc(cl.label) + "</b><br>" + esc(cl.reason) + "</div>" +
''', '''    '<div class="banner ' + bannerCls + '"><b>' + esc(cl.label) + "</b><br>" + esc(cl.reason) + "</div>" +
    evidenceSummaryHtml(hp, ap, ag, cl, paths.length) +
''', count=1, tag="evidence summary strip call")

# ---------- 11. request brief: two-stage research order (general pass first, then per-section dive) ----------
rep('''    L.push('EVIDENCE CUTOFF: '+cutoff+' — only completed matches before this date are evidence.');
    L.push('');
    L.push('STRICT RESEARCH RULES');''',
    '''    L.push('EVIDENCE CUTOFF: '+cutoff+' — only completed matches before this date are evidence.');
    L.push('');
    L.push('RESEARCH ORDER — TWO STAGES');
    L.push('STAGE 1 — GENERAL TEAM-DATA PASS (do this first, per team). Open one comprehensive team-overview page — one club, every competition, one results list — and take the full inventory: identity and aliases, normal home venue, current season position, and the complete run of results with exact dates, scores, competitions and home/away order (league, cups, UEFA, friendlies). This pass sets the match inventory so nothing is missed. Never start section-by-section searching without the inventory.');
    L.push('STAGE 2 — PER-SECTION DEEP DIVE (only after the Stage 1 inventory exists). Verify and complete each required section against official or cross-check sources: season table plus home/away split, venue surface/capacity cross-check, older cup and European rounds beyond the overview page, and the level-3 bridge rows. Where the overview page and an official source disagree, the official source wins and a NOTE row records the discrepancy.');
    L.push('Stage 1 is a starting layer, not a source of truth. Overview pages can flip home/away order, cache stale rows, collapse competition labels and drop qualifying rounds — never ship a Stage-1-only pack. Known failure modes of going straight to per-section search without Stage 1: missing matches that no single section asks for, and duplicated rows under competing competition labels.');
    L.push('');
    L.push('STRICT RESEARCH RULES');''', count=1, tag="research order two stages")

# ---------- 12. drive-linked data folder: one canonical JSON store on the user drive ----------
rep('''<div id="bpBackupReport" style="margin-top:10px"></div></div>'+
''', '''<div id="bpBackupReport" style="margin-top:10px"></div></div>'+
      '<div class="card"><h2>Drive data folder — auto-load and auto-save</h2><div class="help">Link a folder on your drive and this app keeps one data file in it — <b>pitch-rating-data.json</b> — auto-loading it on open and auto-saving every change. Moving to a freshly downloaded app file no longer loses loaded data: open the new file, click Reconnect last folder, done. Works in Chrome, Edge and Brave. Safari and Firefox cannot write drive files from a page — use the backup card above there.</div><div style="margin-top:9px"><button class="btn2" onclick="BlueprintEmbed.linkDrive()">Link data folder</button> <button class="btn2" onclick="BlueprintEmbed.reconnectDrive()">Reconnect last folder</button> <button class="btn2" onclick="BlueprintEmbed.unlinkDrive()">Unlink</button></div><div id="bpDriveStatus" class="help" style="margin-top:9px">Checking drive-link support…</div></div>'+
''', count=1, tag="drive folder card")
rep('''  function injectUI(){''', r'''  /* ---------- drive-linked data folder (auto-load / auto-save) ----------
     localStorage is browser-local, so a freshly downloaded app file can strand
     loaded data. With the File System Access API (Chromium), the app keeps one
     canonical JSON store in a user-picked folder and syncs every change to it.
     The folder handle lives in IndexedDB (localStorage cannot store handles).
     Conflict rule: the drive file is canonical, drive-wins, and the displaced
     browser copy is backed up into the folder first. An empty drive file never
     erases a non-empty browser store. Unsupported browsers get guidance only. */
  var driveHandle=null, driveGranted=false, driveWriteTimer=null;
  var DRIVE_FILE='pitch-rating-data.json', DRIVE_IDB='pitch-rating-drive', DRIVE_IDB_STORE='handles', DRIVE_IDB_KEY='dataFolder';
  function driveSupported(){ return typeof window!=='undefined' && !!window.showDirectoryPicker && !!window.indexedDB; }
  function idbOpen(){ return new Promise(function(res,rej){ var rq=window.indexedDB.open(DRIVE_IDB,1); rq.onupgradeneeded=function(){ rq.result.createObjectStore(DRIVE_IDB_STORE); }; rq.onsuccess=function(){res(rq.result);}; rq.onerror=function(){rej(rq.error);}; }); }
  function idbPut(v){ return idbOpen().then(function(db){ return new Promise(function(res,rej){ var tx=db.transaction(DRIVE_IDB_STORE,'readwrite'); tx.objectStore(DRIVE_IDB_STORE).put(v,DRIVE_IDB_KEY); tx.oncomplete=function(){res();}; tx.onerror=function(){rej(tx.error);}; }); }); }
  function idbGet(){ return idbOpen().then(function(db){ return new Promise(function(res,rej){ var tx=db.transaction(DRIVE_IDB_STORE,'readonly'); var g=tx.objectStore(DRIVE_IDB_STORE).get(DRIVE_IDB_KEY); g.onsuccess=function(){res(g.result||null);}; g.onerror=function(){rej(g.error);}; }); }); }
  function idbDel(){ return idbOpen().then(function(db){ return new Promise(function(res,rej){ var tx=db.transaction(DRIVE_IDB_STORE,'readwrite'); tx.objectStore(DRIVE_IDB_STORE).delete(DRIVE_IDB_KEY); tx.oncomplete=function(){res();}; tx.onerror=function(){rej(tx.error);}; }); }); }
  function drivePayload(){ return {app:'pitch-rating-blueprint', exported:todayISO(), blueprintVersion:BP.version, identities:BP.identities, aliases:BP.aliases, matches:BP.matches, teamStats:BP.teamStats, venues:BP.venues, sources:BP.sources, calibration:BP.calibration}; }
  function driveSetStatus(h){ var el=document.getElementById('bpDriveStatus'); if(el) el.innerHTML=h; }
  function driveLinkedNote(){ return 'Linked folder: <b>'+esc(driveHandle.name)+'</b> · '+BP.matches.length+' match rows'; }
  async function driveReadStoreFile(){
    try{ var fh=await driveHandle.getFileHandle(DRIVE_FILE,{create:false}); var f=await fh.getFile(); var t=await f.text(); var d=JSON.parse(t); return (d && d.identities && Array.isArray(d.matches)) ? d : null; }catch(e){ return null; }
  }
  async function driveWriteStoreFile(){
    if(!driveHandle || !driveGranted) return false;
    try{ var fh=await driveHandle.getFileHandle(DRIVE_FILE,{create:true}); var w=await fh.createWritable(); await w.write(JSON.stringify(drivePayload(),null,2)); await w.close(); return true; }
    catch(e){ driveGranted=false; driveSetStatus('<b>Drive link needs permission.</b> Click Reconnect last folder. ('+esc(e.message||e)+')'); return false; }
  }
  function scheduleDriveWrite(){
    if(!driveHandle || !driveGranted) return;
    if(driveWriteTimer) clearTimeout(driveWriteTimer);
    driveWriteTimer=setTimeout(function(){ driveWriteTimer=null; driveWriteStoreFile().then(function(ok){ if(ok) driveSetStatus(driveLinkedNote()+' · auto-saved '+new Date().toLocaleTimeString()); }); },700);
  }
  async function adoptDriveData(d){
    /* drive is canonical — but an EMPTY drive file never erases a non-empty browser store */
    if(!d.matches.length && BP.matches.length) return false;
    if(BP.matches.length){
      try{ var ts=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19); var bh=await driveHandle.getFileHandle('pitch-rating-data-browser-backup-'+ts+'.json',{create:true}); var w=await bh.createWritable(); await w.write(JSON.stringify(drivePayload(),null,2)); await w.close(); }catch(e){}
    }
    BP={version:d.blueprintVersion||'blueprint-embed-v0.6-live', identities:d.identities||{}, aliases:d.aliases||{}, matches:d.matches||[], teamStats:d.teamStats||{}, venues:d.venues||{}, sources:d.sources||[], loadedAt:todayISO(), calibration:d.calibration||null};
    normalizeStore(); saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus();
    if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
    driveSetStatus('Loaded '+BP.matches.length+' match rows from <b>'+DRIVE_FILE+'</b> in '+driveLinkedNote()+'. The drive copy differed from this browser, so the drive copy won — the browser copy was backed up into the folder first. Every change now auto-saves.');
    return true;
  }
  async function driveConnectFlow(h){
    driveHandle=h; var perm='granted';
    try{ perm=await h.queryPermission({mode:'readwrite'}); if(perm!=='granted') perm=await h.requestPermission({mode:'readwrite'}); }catch(e){}
    if(perm!=='granted'){ driveGranted=false; driveSetStatus('<b>'+esc(h.name)+'</b> is known but needs permission. Click <b>Reconnect last folder</b> and allow access.'); return; }
    driveGranted=true;
    var d=await driveReadStoreFile();
    if(d){
      if(d.matches.length===BP.matches.length){ driveSetStatus(driveLinkedNote()+' match this browser · auto-save on.'); }
      else await adoptDriveData(d);
    } else {
      var ok=await driveWriteStoreFile();
      if(ok) driveSetStatus(driveLinkedNote()+' · created <b>'+DRIVE_FILE+'</b> from your currently loaded data. Every change now auto-saves.');
    }
  }
  function linkDriveFolder(){
    if(!driveSupported()){ driveSetStatus('This browser does not support drive linking. Use <b>Export blueprint data</b> before changing app files and <b>Import blueprint data</b> after.'); return; }
    window.showDirectoryPicker({mode:'readwrite'}).then(function(h){ return idbPut(h).catch(function(){}).then(function(){ return driveConnectFlow(h); }); }).catch(function(e){ if(e && e.name!=='AbortError') driveSetStatus('Could not link that folder: '+esc(e.message||e)); });
  }
  function reconnectDriveFolder(){
    if(!driveSupported()){ driveSetStatus('This browser does not support drive linking. Use the backup card above.'); return; }
    idbGet().then(function(h){ if(!h){ driveSetStatus('No folder linked yet — click <b>Link data folder</b> first.'); return null; } return driveConnectFlow(h); }).catch(function(e){ driveSetStatus('Reconnect failed: '+esc(e.message||e)+' — link again.'); });
  }
  function unlinkDrive(){
    driveHandle=null; driveGranted=false; if(driveWriteTimer){clearTimeout(driveWriteTimer); driveWriteTimer=null;}
    if(driveSupported()){ idbDel().catch(function(){}); }
    driveSetStatus('Drive link removed. Data stays in this browser storage only.');
  }
  function initDriveLink(){
    var el=document.getElementById('bpDriveStatus'); if(!el) return;
    if(!driveSupported()){ el.innerHTML='This browser does not support drive linking (needs Chrome, Edge or Brave). Use <b>Export blueprint data</b> / <b>Import blueprint data</b> on the backup card above when you change app files.'; return; }
    idbGet().then(function(h){
      if(!h){ driveSetStatus('No folder linked. Data lives only in this browser storage — click <b>Link data folder</b> to carry it across app versions.'); return; }
      driveHandle=h;
      h.queryPermission({mode:'readwrite'}).then(function(p){
        if(p==='granted'){ driveConnectFlow(h); }
        else driveSetStatus('Folder <b>'+esc(h.name)+'</b> was linked before — click <b>Reconnect last folder</b> to resume auto-load and auto-save.');
      });
    }).catch(function(){ driveSetStatus('No folder linked. Data lives only in this browser storage — click <b>Link data folder</b>.'); });
  }

  function injectUI(){''', count=1, tag="drive folder module")
rep('''  function saveStore(){try{localStorage.setItem(LS, JSON.stringify(BP));}catch(e){}}''',
    '''  function saveStore(){try{localStorage.setItem(LS, JSON.stringify(BP));}catch(e){} scheduleDriveWrite();}''', count=1, tag="saveStore drives drive-write")
rep('''    loadPackFile:loadPackFile,
''', '''    loadPackFile:loadPackFile,
    linkDrive:linkDriveFolder,
    reconnectDrive:reconnectDriveFolder,
    unlinkDrive:unlinkDrive,
''', count=1, tag="drive api exposure")
rep('''      renderBPStatus(); populateBPTeams();
      if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
    } catch(e){''',
    '''      renderBPStatus(); populateBPTeams();
      try{ initDriveLink(); }catch(e){}
      if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
    } catch(e){''', count=1, tag="boot initDriveLink")

# ---------- 13. unified single-source data file (evidence store + saved log), merge-on-import ----------
rep('<h2>Blueprint data backup</h2>', '<h2>Full data backup — evidence store + saved log (single file)</h2>', count=1, tag="backup card heading")
rep('Export before loading large research batches. Import restores identities, team packs, venues, sources, matches and calibration metadata.',
    'One single JSON carries everything: the evidence store (identities, team packs, venues, sources, match rows, calibration) AND your saved log with verdicts and settlements. Export before changing app files or devices. Import <b>merges into current data</b> — nothing you already have is deleted, duplicates are skipped by the existing dedupe keys, and settled/later log entries win. The drive folder below writes this same file automatically in Chrome, Edge and Brave.', count=1, tag="backup card help")
rep('Export blueprint data</button>', 'Export full data</button>', count=1, tag="export full btn")
rep('Import blueprint data</button>', 'Import full data (merge)</button>', count=1, tag="import merge btn")
rep('''  function exportBPData(){''', r'''  /* ---------- unified full-data file: single source for store + log ----------
     Mirrors the old match-audit tool pattern: one JSON holds ALL previous data,
     and importing MERGES it into what is here (union, dedupe-keyed) instead of
     replacing — so a file always contains every previous plus newly updated row.
     Accepts both the unified file and legacy blueprint-only exports. */
  function fullDataPayload(){
    return {app:'pitch-rating-full', format:1, exported:todayISO(), blueprintVersion:BP.version,
      identities:BP.identities, aliases:BP.aliases, matches:BP.matches, teamStats:BP.teamStats,
      venues:BP.venues, sources:BP.sources, calibration:BP.calibration,
      log:(typeof logEntries!=='undefined'?logEntries:[])};
  }
  function mergeIdentityRecord(rec){
    if(!rec || !rec.name) return false;
    var before=Object.keys(BP.identities).length;
    var leagues=Array.isArray(rec.leagues)&&rec.leagues.length?rec.leagues:[rec.league||''];
    for(var i=0;i<leagues.length;i++) addIdentity(rec.name, rec.country, leagues[i]||'', rec.aliases||[], rec.source||'import');
    return Object.keys(BP.identities).length>before;
  }
  function mergeLogEntries(incoming){
    var out={added:0, updated:0};
    if(!Array.isArray(incoming) || typeof logEntries==='undefined') return out;
    incoming.forEach(function(e){
      if(!e || !e.id) return;
      var i=-1; for(var k=0;k<logEntries.length;k++){ if(logEntries[k].id===e.id){ i=k; break; } }
      if(i===-1){ logEntries.push(e); out.added++; return; }
      var cur=logEntries[i];
      var takeIn = (!!e.result && !cur.result) || (!!e.result===!!cur.result && (e.ts||0)>(cur.ts||0));
      if(takeIn){ logEntries[i]=e; out.updated++; }
    });
    logEntries.sort(function(a,b){ return (b.ts||0)-(a.ts||0); });
    return out;
  }
  function mergeStoreData(d){
    var out={matches:0, identities:0, seasons:0, forms:0, venues:0, sources:0};
    if(!d) return out;
    var ids=d.identities||{}; Object.keys(ids).forEach(function(k){ if(mergeIdentityRecord(ids[k])) out.identities++; });
    (d.matches||[]).forEach(function(m){ if(addMatch(m)) out.matches++; });
    var ts=d.teamStats||{}; Object.keys(ts).forEach(function(tid){
      var pack=ts[tid]||{};
      (pack.seasons||[]).forEach(function(r){ if(addSeasonStat(tid,r)) out.seasons++; });
      (pack.forms||[]).forEach(function(r){ if(addFormStat(tid,r)) out.forms++; });
    });
    var v=d.venues||{}; Object.keys(v).forEach(function(tid){ if(!BP.venues[tid]){ BP.venues[tid]=v[tid]; out.venues++; } });
    (d.sources||[]).forEach(function(s){ if(s && addSource(s.label,s.url,s.accessed,s.notes)) out.sources++; });
    if(BP.calibration==null && d.calibration!=null) BP.calibration=d.calibration;
    return out;
  }
  function applyFullDataObject(d){
    /* Union merge — never an erase. Existing rows keep precedence via the same
       dedupe keys the parsers use; log conflicts keep the settled/later entry. */
    if(!d || !d.identities || !Array.isArray(d.matches)) throw new Error('not a Pitch Rating full-data or blueprint backup file');
    var ms=mergeStoreData(d);
    dedupeIdentities(); normalizeStore();
    var lg=mergeLogEntries(d.log);
    BP.loadedAt=todayISO();
    saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus();
    if(typeof saveLog==='function') saveLog();
    if(typeof updateCount==='function') updateCount();
    if(typeof renderLog==='function'){ try{ renderLog(); }catch(e){} }
    if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
    return 'Merged into current data: +'+ms.matches+' match row(s), +'+ms.identities+' identitie(s), +'+ms.seasons+' season, +'+ms.forms+' form, +'+ms.venues+' venue, +'+ms.sources+' source · log: '+lg.added+' added, '+lg.updated+' updated · duplicates skipped.';
  }
  function patchSaveLogForDrive(){
    /* Every log mutation (save/settle/delete) also schedules a drive write, so
       the folder file always holds the newest state of store AND log. */
    try{
      if(typeof saveLog==='function' && !window.saveLog.__driveWrapped){
        var orig=window.saveLog;
        window.saveLog=function(){ var r=orig.apply(this,arguments); scheduleDriveWrite(); return r; };
        window.saveLog.__driveWrapped=true;
      }
    }catch(e){}
  }

  function exportBPData(){''', count=1, tag="unified full-data module")
rep('''    var data={app:'pitch-rating-blueprint', exported:todayISO(), blueprintVersion:BP.version, identities:BP.identities, aliases:BP.aliases, matches:BP.matches, teamStats:BP.teamStats, venues:BP.venues, sources:BP.sources, calibration:BP.calibration};''',
    '''    var data=fullDataPayload();''', count=1, tag="export unified payload")
rep("a.download='pitch-rating-blueprint-data-'+todayISO()+'.json';", "a.download='pitch-rating-full-data-'+todayISO()+'.json';", count=1, tag="export filename")
rep('''  function importBPDataFile(ev){
    var f=ev.target.files && ev.target.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(){
      var el=document.getElementById('bpBackupReport');
      try{
        var d=JSON.parse(rd.result);
        if(!d.identities || !Array.isArray(d.matches)) throw new Error('not a blueprint data backup');
        BP={version:d.blueprintVersion||'blueprint-embed-v0.6-live', identities:d.identities||{}, aliases:d.aliases||{}, matches:d.matches||[], teamStats:d.teamStats||{}, venues:d.venues||{}, sources:d.sources||[], loadedAt:todayISO(), calibration:d.calibration||null};
        normalizeStore(); saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus(); if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
        if(el) el.innerHTML='<div class="banner ban-ok">Imported blueprint backup: '+Object.keys(BP.identities).length+' identities, '+BP.matches.length+' matches, '+Object.keys(BP.teamStats||{}).length+' team stat packs.</div>';
      } catch(e){ if(el) el.innerHTML='<div class="banner ban-err">Import failed: '+esc(e.message)+'</div>'; }
      ev.target.value='';
    };
    rd.readAsText(f);
  }''', '''  function importBPDataFile(ev){
    var f=ev.target.files && ev.target.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(){
      var el=document.getElementById('bpBackupReport');
      try{
        var d=JSON.parse(rd.result);
        if(!d.identities || !Array.isArray(d.matches)) throw new Error('not a Pitch Rating data file — expected a full-data or blueprint backup JSON');
        if(!confirm('Import will MERGE this file into your current data (evidence store + saved log). Nothing you have is deleted; duplicates are skipped; settled/later log entries win. Continue?')){ ev.target.value=''; return; }
        var rep=applyFullDataObject(d);
        if(el) el.innerHTML='<div class="banner ban-ok">'+esc(rep)+'</div>';
      } catch(e){ if(el) el.innerHTML='<div class="banner ban-err">Import failed: '+esc(e.message)+'</div>'; }
      ev.target.value='';
    };
    rd.readAsText(f);
  }''', count=1, tag="import merges instead of replaces")
rep("  function drivePayload(){ return {app:'pitch-rating-blueprint', exported:todayISO(), blueprintVersion:BP.version, identities:BP.identities, aliases:BP.aliases, matches:BP.matches, teamStats:BP.teamStats, venues:BP.venues, sources:BP.sources, calibration:BP.calibration}; }",
    "  function drivePayload(){ return fullDataPayload(); }", count=1, tag="drive payload unified")
rep('''  async function adoptDriveData(d){
    /* drive is canonical — but an EMPTY drive file never erases a non-empty browser store */
    if(!d.matches.length && BP.matches.length) return false;
    if(BP.matches.length){
      try{ var ts=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19); var bh=await driveHandle.getFileHandle('pitch-rating-data-browser-backup-'+ts+'.json',{create:true}); var w=await bh.createWritable(); await w.write(JSON.stringify(drivePayload(),null,2)); await w.close(); }catch(e){}
    }
    BP={version:d.blueprintVersion||'blueprint-embed-v0.6-live', identities:d.identities||{}, aliases:d.aliases||{}, matches:d.matches||[], teamStats:d.teamStats||{}, venues:d.venues||{}, sources:d.sources||[], loadedAt:todayISO(), calibration:d.calibration||null};
    normalizeStore(); saveStore(); applySeasonStatsToModel(); populateBPTeams(); renderBPStatus();
    if(window.__bpRefreshPickers){try{window.__bpRefreshPickers();}catch(e){}}
    driveSetStatus('Loaded '+BP.matches.length+' match rows from <b>'+DRIVE_FILE+'</b> in '+driveLinkedNote()+'. The drive copy differed from this browser, so the drive copy won — the browser copy was backed up into the folder first. Every change now auto-saves.');
    return true;
  }''', '''  async function adoptDriveData(d){
    /* UNION merge, never an erase: the folder file merges into the browser
       store. When both sides hold data and differ, the browser copy is first
       snapshotted into the folder as a restore point. */
    var logNow=(typeof logEntries!=='undefined'?logEntries.length:0);
    if((BP.matches.length||logNow) && (d.matches.length!==BP.matches.length || (d.log||[]).length!==logNow)){
      try{ var ts=new Date().toISOString().replace(/[:.]/g,'-').slice(0,19); var bh=await driveHandle.getFileHandle('pitch-rating-data-browser-backup-'+ts+'.json',{create:true}); var w=await bh.createWritable(); await w.write(JSON.stringify(fullDataPayload(),null,2)); await w.close(); }catch(e){}
    }
    var rep=applyFullDataObject(d);
    driveSetStatus('Folder file merged — '+esc(rep)+' Every change now auto-saves to the folder.');
    return true;
  }''', count=1, tag="drive adopt union merge")
rep('''      if(d.matches.length===BP.matches.length){ driveSetStatus(driveLinkedNote()+' match this browser · auto-save on.'); }''',
    '''      if(d.matches.length===BP.matches.length && (d.log||[]).length===(typeof logEntries!=='undefined'?logEntries.length:0)){ driveSetStatus(driveLinkedNote()+' match this browser · auto-save on.'); }''', count=1, tag="drive connect same-check includes log")
rep('''      try{ initDriveLink(); }catch(e){}
''', '''      try{ initDriveLink(); }catch(e){}
      try{ patchSaveLogForDrive(); }catch(e){}
''', count=1, tag="boot patchSaveLogForDrive")
rep('''    unlinkDrive:unlinkDrive,
''', '''    unlinkDrive:unlinkDrive,
    applyFullData:applyFullDataObject,
''', count=1, tag="applyFullData api")

# ---------- 14. export location = import default location (wired to linked drive folder) ----------
rep('''  function exportBPData(){
    var data=fullDataPayload();
    var b=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    var u=URL.createObjectURL(b), a=document.createElement('a');
    a.href=u; a.download='pitch-rating-full-data-'+todayISO()+'.json'; a.click();
    setTimeout(function(){URL.revokeObjectURL(u);},2000);
  }''', '''  function driveDownloadPayload(data){
    var b=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    var u=URL.createObjectURL(b), a=document.createElement('a');
    a.href=u; a.download='pitch-rating-full-data-'+todayISO()+'.json'; a.click();
    setTimeout(function(){URL.revokeObjectURL(u);},2000);
  }
  function exportBPData(){
    var data=fullDataPayload();
    /* Export location defaults to the linked drive folder: the file is written
       there instead of downloaded, and the Import picker opens in that same
       folder — so the export/import loop runs through one known location. */
    if(driveHandle && driveGranted){
      (async function(){
        try{
          var name='pitch-rating-full-data-'+todayISO()+'.json';
          var fh=await driveHandle.getFileHandle(name,{create:true});
          var w=await fh.createWritable(); await w.write(JSON.stringify(data,null,2)); await w.close();
          var el=document.getElementById('bpBackupReport'); if(el) el.innerHTML='<div class="banner ban-ok">Export written to linked folder <b>'+esc(driveHandle.name)+'</b> as <b>'+esc(name)+'</b> — Import opens in the same place.</div>';
        }catch(e){ driveDownloadPayload(data); }
      })();
      return;
    }
    driveDownloadPayload(data);
    var el=document.getElementById('bpBackupReport'); if(el) el.innerHTML='<div class="banner ban-info">Exported as a download. <b>Link the drive folder below</b> and exports write straight there — Import then opens in that folder too.</div>';
  }''', count=1, tag="export defaults to linked folder")
rep('''  function importBPDataFile(ev){
    var f=ev.target.files && ev.target.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(){
      var el=document.getElementById('bpBackupReport');
      try{
        var d=JSON.parse(rd.result);
        if(!d.identities || !Array.isArray(d.matches)) throw new Error('not a Pitch Rating data file — expected a full-data or blueprint backup JSON');
        if(!confirm('Import will MERGE this file into your current data (evidence store + saved log). Nothing you have is deleted; duplicates are skipped; settled/later log entries win. Continue?')){ ev.target.value=''; return; }
        var rep=applyFullDataObject(d);
        if(el) el.innerHTML='<div class="banner ban-ok">'+esc(rep)+'</div>';
      } catch(e){ if(el) el.innerHTML='<div class="banner ban-err">Import failed: '+esc(e.message)+'</div>'; }
      ev.target.value='';
    };
    rd.readAsText(f);
  }''', '''  function importBackupFromFile(f){
    var rd=new FileReader();
    rd.onload=function(){
      var el=document.getElementById('bpBackupReport');
      try{
        var d=JSON.parse(rd.result);
        if(!d.identities || !Array.isArray(d.matches)) throw new Error('not a Pitch Rating data file — expected a full-data or blueprint backup JSON');
        if(!confirm('Import will MERGE this file into your current data (evidence store + saved log). Nothing you have is deleted; duplicates are skipped; settled/later log entries win. Continue?')) return;
        var rep=applyFullDataObject(d);
        if(el) el.innerHTML='<div class="banner ban-ok">'+esc(rep)+'</div>';
      } catch(e){ if(el) el.innerHTML='<div class="banner ban-err">Import failed: '+esc(e.message)+'</div>'; }
    };
    rd.readAsText(f);
  }
  function pickBackup(){
    /* Import defaults to the export location: when a drive folder is linked and
       granted, the file picker opens inside it. Classic input otherwise. */
    if(driveSupported() && driveHandle && driveGranted && window.showOpenFilePicker){
      window.showOpenFilePicker({startIn:driveHandle, multiple:false, types:[{description:'Pitch Rating data', accept:{'application/json':['.json']}}]})
        .then(function(hs){ return hs && hs[0] ? hs[0].getFile() : null; })
        .then(function(f){ if(f) importBackupFromFile(f); })
        .catch(function(){});
      return;
    }
    var el=document.getElementById('bpBackupFile'); if(el) el.click();
  }
  function importBPDataFile(ev){ var f=ev.target.files && ev.target.files[0]; if(!f) return; importBackupFromFile(f); ev.target.value=''; }''', count=1, tag="import picker defaults to linked folder")
rep(r'''onclick="document.getElementById(\'bpBackupFile\').click()">Import full data (merge)</button>''',
    r'''onclick="BlueprintEmbed.pickBackup()">Import full data (merge)</button>''', count=1, tag="import button uses pickBackup")
rep('The drive folder below writes this same file automatically in Chrome, Edge and Brave.',
    'The drive folder below writes this same file automatically in Chrome, Edge and Brave — linking it also sends manual exports there and opens imports from there.', count=1, tag="backup card folder loop note")
rep('''    applyFullData:applyFullDataObject,
''', '''    applyFullData:applyFullDataObject,
    pickBackup:pickBackup,
''', count=1, tag="pickBackup api")


# --- v2.6.8: percentage summation + zone read (zones v0.2, 600-game calibration)
rep(r'''function evidenceSummaryHtml(hp, ap, ag, cl, pathCount) {''',
    r'''/* Zone ladder v0.2 - tuned on the 600-game masked replay (replay_zones.js,
   ZONES.md). Zones state the reading; they are computation output, not advice. */
function zoneLadder(S){
  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "measured: leader won 73%, draw 12% (n=74)" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "measured: leader won 61%, leader-or-draw 80% (n=166)" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "measured: leader-or-draw pair covered 72% (n=146)" };
  if (S >= 50) return { key: "lean",    zone: "lean",        note: "measured: directional only, 53% (n=97)" };
  return { key: "toss", zone: "TOSS", note: "measured: leader won 43% (n=115) - no side earns it" };
}
/* Percentage analysis per section + total summation out of 100%, using the
   engine's own bucket rule (|est|>0.25 home/away, else neutral) so section
   shares and the aggregate always reconcile. Pure computation, no wording. */
function evidenceSummationHtml(hp, ap, paths, ag) {
  if (!ag) return "";
  function sectionRow(name, ps) {
    var hW = 0, dW = 0, aW = 0, W = 0;
    ps.forEach(function (p) {
      W += p.weight;
      if (p.estimate > 0.25) hW += p.weight; else if (p.estimate < -0.25) aW += p.weight; else dW += p.weight;
    });
    if (!W) return "";
    return '<div class="kv" style="margin:4px 0 0"><span class="k">' + esc(name) + '</span><span>' +
      esc(hp.name) + " <b>" + pct0(hW / W) + "</b> \u00b7 draw " + pct0(dW / W) + " \u00b7 " + esc(ap.name) + " <b>" + pct0(aW / W) + "</b>" +
      ' <span class="help">(\u03a3w ' + W.toFixed(1) + " \u00b7 " + ps.length + " path" + (ps.length === 1 ? "" : "s") + ")</span></span></div>";
  }
  var rows = "";
  [["H2H", "h2h"], ["Common opponents", "common"], ["Level-3 chains", "third"]].forEach(function (s) {
    var ps = paths.filter(function (p) { return p.phase === s[1]; });
    if (ps.length) rows += sectionRow(s[0], ps);
  });
  var totalW = ag.homeW + ag.neuW + ag.awayW;
  var H = ag.homeW / totalW, D = ag.neuW / totalW, A = ag.awayW / totalW;
  var S_ = Math.max(H, A) * 100, zn = zoneLadder(S_);
  var side = H >= A ? "TA (" + esc(hp.name) + ")" : "TB (" + esc(ap.name) + ")";
  return '<div style="margin:12px 0 0">' +
    '<div class="help" style="margin:0 0 4px"><b>Percentage analysis</b> - evidence-weight distribution per section and total, out of 100%. Evidence shares, not win probability.</div>' +
    rows +
    '<div class="help" style="margin:10px 0 2px"><b>Total summation</b></div>' +
    ratingBarHtml(hp.name, ap.name, H, D, A) +
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \u00b7 Draw " + pct0(D) + " \u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
    '<div class="help" style="margin:4px 0 0">Zone: ' + side + " - <b>" + zn.zone + "</b> (leader share " + S_.toFixed(1) + "% - " + esc(zn.note) + ")</div>" +
    "</div>";
}
function evidenceSummaryHtml(hp, ap, ag, cl, pathCount) {''', count=1, tag="zone ladder + summation block")

rep(r'''    evidenceSummaryHtml(hp, ap, ag, cl, paths.length) +
    PitchEvidenceBalance.render({''',
    r'''    evidenceSummaryHtml(hp, ap, ag, cl, paths.length) +
    evidenceSummationHtml(hp, ap, paths, ag) +
    PitchEvidenceBalance.render({''', count=1, tag="summation call site")

rep(r'''    homeW: ag ? ag.homeW : 0, neuW: ag ? ag.neuW : 0, awayW: ag ? ag.awayW : 0,
    venueConfirmed: true,''',
    r'''    homeW: ag ? ag.homeW : 0, neuW: ag ? ag.neuW : 0, awayW: ag ? ag.awayW : 0,
    zone: ag ? (function(){ var tw = ag.homeW + ag.neuW + ag.awayW; var S_ = Math.max(ag.homeW, ag.awayW) / tw * 100; var zn = zoneLadder(S_); return (ag.homeW >= ag.awayW ? "TA " : "TB ") + zn.zone + " " + S_.toFixed(1) + "%"; })() : null,
    venueConfirmed: true,''', count=1, tag="saved verdict zone tag")


# --- v2.6.9: C2 confirmation gate on WIN/STRONG zones (CALIBRATION-2.md)
rep(r'''/* Percentage analysis per section + total summation out of 100%, using the
   engine's own bucket rule (|est|>0.25 home/away, else neutral) so section
   shares and the aggregate always reconcile. Pure computation, no wording. */''',
    r'''/* Zone confirmation gate (C2, measured in CALIBRATION-2.md):
   WIN/STRONG zones require >=2 of 3 sections agreeing with the leader at >=55%
   section share; fail and the zone demotes to WIN-DRAW. Contra-leading sections
   are flagged. Gated quality (600 replays): STRONG 78% win / 91% w-or-d. */
function sectionShares(paths) {
  var out = [];
  [["H2H", "h2h"], ["Common opponents", "common"], ["Level-3 chains", "third"]].forEach(function (s) {
    var ps = paths.filter(function (p) { return p.phase === s[1]; });
    if (!ps.length) return;
    var hW = 0, dW = 0, aW = 0, W = 0;
    ps.forEach(function (p) {
      W += p.weight;
      if (p.estimate > 0.25) hW += p.weight; else if (p.estimate < -0.25) aW += p.weight; else dW += p.weight;
    });
    if (W) out.push({ name: s[0], phase: s[1], hW: hW, dW: dW, aW: aW, W: W,
      side: hW >= aW ? "H" : "A", lead: Math.max(hW, aW) / W * 100 });
  });
  return out;
}
function computeZone(paths, ag) {
  var tw = ag.homeW + ag.neuW + ag.awayW;
  var S_ = Math.max(ag.homeW, ag.awayW) / tw * 100;
  var leaderSide = ag.homeW >= ag.awayW ? "H" : "A";
  var zn = zoneLadder(S_), key = zn.key, gatedFrom = null;
  var secs = sectionShares(paths), agree = 0, contra = [];
  secs.forEach(function (s) {
    if (s.lead >= 55) {
      if (s.side === leaderSide) agree++;
      else contra.push(s);
    }
  });
  if ((key === "strong" || key === "win") && agree < 2) { gatedFrom = zn.zone; key = "windraw"; }
  var word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[key];
  var side = leaderSide === "H" ? "TA" : "TB";
  return { S_: S_, key: key, word: word, side: side, agree: agree, contra: contra,
           gatedFrom: gatedFrom, secs: secs,
           tag: side + " " + word + " " + S_.toFixed(1) + "%" + (gatedFrom ? " (gated from " + gatedFrom + ")" : "") };
}
/* Percentage analysis per section + total summation out of 100%, using the
   engine's own bucket rule (|est|>0.25 home/away, else neutral) so section
   shares and the aggregate always reconcile. Pure computation, no wording. */''', count=1, tag="computeZone gate helper")

rep(r'''  var rows = "";
  [["H2H", "h2h"], ["Common opponents", "common"], ["Level-3 chains", "third"]].forEach(function (s) {
    var ps = paths.filter(function (p) { return p.phase === s[1]; });
    if (ps.length) rows += sectionRow(s[0], ps);
  });
  var totalW = ag.homeW + ag.neuW + ag.awayW;
  var H = ag.homeW / totalW, D = ag.neuW / totalW, A = ag.awayW / totalW;
  var S_ = Math.max(H, A) * 100, zn = zoneLadder(S_);
  var side = H >= A ? "TA (" + esc(hp.name) + ")" : "TB (" + esc(ap.name) + ")";
  return '<div style="margin:12px 0 0">' +
    '<div class="help" style="margin:0 0 4px"><b>Percentage analysis</b> - evidence-weight distribution per section and total, out of 100%. Evidence shares, not win probability.</div>' +
    rows +
    '<div class="help" style="margin:10px 0 2px"><b>Total summation</b></div>' +
    ratingBarHtml(hp.name, ap.name, H, D, A) +
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \u00b7 Draw " + pct0(D) + " \u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
    '<div class="help" style="margin:4px 0 0">Zone: ' + side + " - <b>" + zn.zone + "</b> (leader share " + S_.toFixed(1) + "% - " + esc(zn.note) + ")</div>" +
    "</div>";
}''',
    r'''  var zinfo = computeZone(paths, ag), secs = zinfo.secs;
  var rows = "";
  secs.forEach(function (s) {
    rows += '<div class="kv" style="margin:4px 0 0"><span class="k">' + esc(s.name) + '</span><span>' +
      esc(hp.name) + " <b>" + pct0(s.hW / s.W) + "</b> \u00b7 draw " + pct0(s.dW / s.W) + " \u00b7 " + esc(ap.name) + " <b>" + pct0(s.aW / s.W) + "</b>" +
      ' <span class="help">(\u03a3w ' + s.W.toFixed(1) + ")</span></span></div>";
  });
  var totalW = ag.homeW + ag.neuW + ag.awayW;
  var H = ag.homeW / totalW, D = ag.neuW / totalW, A = ag.awayW / totalW;
  var sideName = zinfo.side === "TA" ? esc(hp.name) : esc(ap.name);
  var flags = "";
  if (zinfo.gatedFrom) flags += '<div class="help" style="margin:2px 0 0">Confirmation gate: demoted from ' + zinfo.gatedFrom + " - only " + zinfo.agree + "/3 sections confirm the leader.</div>";
  zinfo.contra.forEach(function (s) { flags += '<div class="help" style="margin:2px 0 0">Flag: ' + esc(s.name) + " section contra-leads at " + s.lead.toFixed(1) + "%.</div>"; });
  return '<div style="margin:12px 0 0">' +
    '<div class="help" style="margin:0 0 4px"><b>Percentage analysis</b> - evidence-weight distribution per section and total, out of 100%. Evidence shares, not win probability.</div>' +
    rows +
    '<div class="help" style="margin:10px 0 2px"><b>Total summation</b></div>' +
    ratingBarHtml(hp.name, ap.name, H, D, A) +
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \u00b7 Draw " + pct0(D) + " \u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
    '<div class="help" style="margin:4px 0 0">Zone: ' + zinfo.side + " (" + sideName + ") - <b>" + zinfo.word + "</b> (leader share " + zinfo.S_.toFixed(1) + "%)" + (zinfo.gatedFrom ? " <b>gated</b>" : "") + "</div>" +
    flags +
    "</div>";
}''', count=1, tag="gated summation render")

rep(r'''function evidenceSummationHtml(hp, ap, paths, ag) {
  if (!ag) return "";
  function sectionRow(name, ps) {
    var hW = 0, dW = 0, aW = 0, W = 0;
    ps.forEach(function (p) {
      W += p.weight;
      if (p.estimate > 0.25) hW += p.weight; else if (p.estimate < -0.25) aW += p.weight; else dW += p.weight;
    });
    if (!W) return "";
    return '<div class="kv" style="margin:4px 0 0"><span class="k">' + esc(name) + '</span><span>' +
      esc(hp.name) + " <b>" + pct0(hW / W) + "</b> \u00b7 draw " + pct0(dW / W) + " \u00b7 " + esc(ap.name) + " <b>" + pct0(aW / W) + "</b>" +
      ' <span class="help">(\u03a3w ' + W.toFixed(1) + " \u00b7 " + ps.length + " path" + (ps.length === 1 ? "" : "s") + ")</span></span></div>";
  }
''',
    r'''function evidenceSummationHtml(hp, ap, paths, ag) {
  if (!ag) return "";
''', count=1, tag="remove old inline sectionRow (moved to sectionShares)")

rep(r'''    zone: ag ? (function(){ var tw = ag.homeW + ag.neuW + ag.awayW; var S_ = Math.max(ag.homeW, ag.awayW) / tw * 100; var zn = zoneLadder(S_); return (ag.homeW >= ag.awayW ? "TA " : "TB ") + zn.zone + " " + S_.toFixed(1) + "%"; })() : null,''',
    r'''    zone: ag ? computeZone(x.paths, ag).tag : null,''', count=1, tag="saved verdict uses gated zone tag")



# --- v2.7.0: C4 — context flag store fields
rep(r'''  var BP = {version:'blueprint-embed-v0.6-live', identities:{}, aliases:{}, matches:[], teamStats:{}, venues:{}, sources:[], loadedAt:null, calibration:null};''',
    r'''  var BP = {version:'blueprint-embed-v0.6-live', identities:{}, aliases:{}, matches:[], teamStats:{}, venues:{}, sources:[], ctxFlags:[], loadedAt:null, calibration:null};''', count=1, tag="BP store gains ctxFlags")

rep(r'''    BP.teamStats=BP.teamStats||{}; BP.venues=BP.venues||{}; BP.sources=Array.isArray(BP.sources)?BP.sources:[];''',
    r'''    BP.teamStats=BP.teamStats||{}; BP.venues=BP.venues||{}; BP.sources=Array.isArray(BP.sources)?BP.sources:[];
    BP.ctxFlags=Array.isArray(BP.ctxFlags)?BP.ctxFlags:[];''', count=1, tag="normalizeStore migrates ctxFlags")

rep(r'''    BP.teamStats[teamId].seasons.push(row); BP.teamStats[teamId].loadedAt=todayISO(); return true;
  }''',
    r'''    BP.teamStats[teamId].seasons.push(row); BP.teamStats[teamId].loadedAt=todayISO(); return true;
  }

  /* C4 context flags: results-external facts about ONE named fixture
     (keeper change, star absence, new-manager debut, rotation risk).
     Demote-only tripwires: a flag against the zone leader drops the zone one
     rung each; a flag against the trailing side is listed but never raises
     confidence (LIVE-BLUEPRINT: context gates may only demote confidence).
     They cannot be back-fit from replay data — they arm when packs feed them. */
  var CTX_FLAGS={'keeper-change':1,'star-absence':1,'new-manager-debut':1,'rotation-risk':1};
  function addCtxFlag(f){
    if(!f||!f.teamId||!CTX_FLAGS[f.flag]||!/^\d{4}-\d{2}-\d{2}$/.test(f.date||'')) return false;
    var key=[f.teamId,f.date,f.flag,f.detail||''].join('|');
    if(BP.ctxFlags.some(function(x){return [x.teamId,x.date,x.flag,x.detail||''].join('|')===key;})) return false;
    BP.ctxFlags.push(f); return true;
  }''', count=1, tag="addCtxFlag + CTX_FLAGS registry")

# --- v2.7.0: C4 — legacy parser CTX row
rep(r'''    var out={teams:0,matches:0,seasons:0,forms:0,venues:0,sources:0,errors:[],notes:[]};''',
    r'''    var out={teams:0,matches:0,seasons:0,forms:0,venues:0,sources:0,ctx:0,errors:[],notes:[]};''', count=1, tag="legacy parser ctx counter")

rep(r'''        } else if(/^MATCH$/i.test(parts[0])){''',
    r'''        } else if(/^CTX$/i.test(parts[0])){
          // CTX|team|date|flag|detail|source - context flag for one named fixture (demote-only)
          if(parts.length<5) throw new Error('CTX needs CTX|team|date|flag|detail|source');
          if(!/^\d{4}-\d{2}-\d{2}$/.test(parts[2])) throw new Error('CTX date must be ISO YYYY-MM-DD');
          if(!CTX_FLAGS[parts[3]]) throw new Error('invalid CTX flag '+parts[3]+' (keeper-change|star-absence|new-manager-debut|rotation-risk)');
          var cx=resolveName(parts[1]); if(!cx) throw new Error('unresolved ctx team '+parts[1]);
          if(addCtxFlag({teamId:cx,date:parts[2],flag:parts[3],detail:parts[4]||'',source:parts[5]||'BP-TEAM-PACK'})) out.ctx++;
        } else if(/^MATCH$/i.test(parts[0])){''', count=1, tag="legacy CTX row")

# --- v2.7.0: C4 — strict v2 parser CTX row
rep(r'''    var out={teams:0,matches:0,seasons:0,forms:0,venues:0,sources:0,errors:[],warnings:[],notes:[]};''',
    r'''    var out={teams:0,matches:0,seasons:0,forms:0,venues:0,sources:0,ctx:0,errors:[],warnings:[],notes:[]};''', count=1, tag="strict parser ctx counter")

rep(r'''        } else if(typ==='MATCH'){''',
    r'''        } else if(typ==='CTX'){
          if(parts.length<5||parts.length>6) throw new Error('CTX needs CTX|team|date|flag|detail|sourceId');
          if(!iso(parts[2])) throw new Error('CTX date must be ISO');
          if(!CTX_FLAGS[parts[3]]) throw new Error('invalid CTX flag '+parts[3]);
          var cx=resolveName(parts[1]); if(!cx) throw new Error('unresolved CTX team '+parts[1]);
          if(addCtxFlag({teamId:cx,date:parts[2],flag:parts[3],detail:parts[4]||'',source:parts[5]||'BP-TEAM-PACK-v2'})) out.ctx++;
          if(parts[5]) refs.push(parts[5]);
        } else if(typ==='MATCH'){''', count=1, tag="strict CTX row")

# --- v2.7.0: C4 — import report shows flags
rep(r'''        html+='<div class="banner ban-ok">Loaded '+r.teams+' team row(s), '+r.seasons+' season row(s), '+r.forms+' form row(s), '+r.venues+' venue row(s), '+r.matches+' new match row(s), '+r.sources+' source row(s).</div>';''',
    r'''        html+='<div class="banner ban-ok">Loaded '+r.teams+' team row(s), '+r.seasons+' season row(s), '+r.forms+' form row(s), '+r.venues+' venue row(s), '+r.matches+' new match row(s), '+r.sources+' source row(s), '+(r.ctx||0)+' context flag(s).</div>';''', count=1, tag="import report counts ctx")

# --- v2.7.0: C4 — public API exposes fixture flags
rep(r'''    analyze:function(hid,aid,cutoff){
      var paths=buildEvidence(hid,aid,cutoff);''',
    r'''    ctxFlagsFor:function(hid,aid,date){ if(!date||!BP.ctxFlags) return []; return BP.ctxFlags.filter(function(f){return f.date===date&&(f.teamId===hid||f.teamId===aid);}).map(function(f){return {teamId:f.teamId,date:f.date,flag:f.flag,detail:f.detail||''};}); },
    analyze:function(hid,aid,cutoff){
      var paths=buildEvidence(hid,aid,cutoff);''', count=1, tag="ctxFlagsFor in API")

# --- v2.7.0: C4 — clearData resets ctxFlags too
rep(r'''BP={version:'blueprint-embed-v0.6-live',identities:{},aliases:{},matches:[],teamStats:{},venues:{},sources:[],loadedAt:null,calibration:null};''',
    r'''BP={version:'blueprint-embed-v0.6-live',identities:{},aliases:{},matches:[],teamStats:{},venues:{},sources:[],ctxFlags:[],loadedAt:null,calibration:null};''', count=1, tag="clearData resets ctxFlags")

# --- v2.7.0: C4 — computeZoneCtx wrapper (top-level, demote-only)
rep(r'''           tag: side + " " + word + " " + S_.toFixed(1) + "%" + (gatedFrom ? " (gated from " + gatedFrom + ")" : "") };
}''',
    r'''           tag: side + " " + word + " " + S_.toFixed(1) + "%" + (gatedFrom ? " (gated from " + gatedFrom + ")" : "") };
}
/* Context-flag demotion (C4). One rung per flag against the zone leader;
   flags against the trailing side are listed and never raise confidence. */
function computeZoneCtx(paths, ag, homeId, awayId, date) {
  var zinfo = computeZone(paths, ag);
  if (typeof BlueprintEmbed === "undefined" || !BlueprintEmbed.ctxFlagsFor) return zinfo;
  var flags = BlueprintEmbed.ctxFlagsFor(homeId, awayId, date) || [];
  if (!flags.length) return zinfo;
  var rungs = ["strong", "win", "windraw", "lean", "toss"];
  var demote = 0;
  zinfo.ctx = flags.map(function (f) {
    var hitsLeader = (f.teamId === homeId) === (zinfo.side === "TA");
    if (hitsLeader) demote++;
    return { flag: f.flag, detail: f.detail, teamId: f.teamId, hitsLeader: hitsLeader };
  });
  var i = rungs.indexOf(zinfo.key);
  if (demote && i >= 0) {
    var ni = Math.min(rungs.length - 1, i + demote);
    if (ni !== i) {
      zinfo.ctxFrom = zinfo.word;
      zinfo.key = rungs[ni];
      zinfo.word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[zinfo.key];
    }
  }
  zinfo.tag = zinfo.side + " " + zinfo.word + " " + zinfo.S_.toFixed(1) + "%" +
    (zinfo.gatedFrom ? " (gated from " + zinfo.gatedFrom + ")" : "") +
    (zinfo.ctxFrom ? " (CTX demoted from " + zinfo.ctxFrom + ")" : "");
  return zinfo;
}''', count=1, tag="computeZoneCtx wrapper")

# --- v2.7.0: C4 — summation render takes an optional pre-computed zone (with CTX)
rep(r'''function evidenceSummationHtml(hp, ap, paths, ag) {
  if (!ag) return "";
  var zinfo = computeZone(paths, ag), secs = zinfo.secs;''',
    r'''function evidenceSummationHtml(hp, ap, paths, ag, zinfo) {
  if (!ag) return "";
  zinfo = zinfo || computeZone(paths, ag);
  var secs = zinfo.secs;''', count=1, tag="summation accepts zone override")

rep(r'''  zinfo.contra.forEach(function (s) { flags += '<div class="help" style="margin:2px 0 0">Flag: ' + esc(s.name) + " section contra-leads at " + s.lead.toFixed(1) + "%.</div>"; });''',
    r'''  zinfo.contra.forEach(function (s) { flags += '<div class="help" style="margin:2px 0 0">Flag: ' + esc(s.name) + " section contra-leads at " + s.lead.toFixed(1) + "%.</div>"; });
  (zinfo.ctx || []).forEach(function (c) {
    var who = c.hitsLeader ? (zinfo.side === "TA" ? hp.name : ap.name) : (zinfo.side === "TA" ? ap.name : hp.name);
    flags += '<div class="help" style="margin:2px 0 0">Context flag (demote-only): ' + esc(who) + " - " + esc(c.flag.replace(/-/g, " ")) + (c.detail ? " - " + esc(c.detail) : "") + (c.hitsLeader ? ". Zone demoted." : ". Against trailing side: noted, no boost.") + "</div>";
  });
  if (zinfo.ctxFrom) flags += '<div class="help" style="margin:2px 0 0">Context demotion: ' + esc(zinfo.ctxFrom) + " -> " + esc(zinfo.word) + ".</div>";''', count=1, tag="summation renders ctx flags")

rep(r'''    '<div class="help" style="margin:4px 0 0">Zone: ' + zinfo.side + " (" + sideName + ") - <b>" + zinfo.word + "</b> (leader share " + zinfo.S_.toFixed(1) + "%)" + (zinfo.gatedFrom ? " <b>gated</b>" : "") + "</div>" +''',
    r'''    '<div class="help" style="margin:4px 0 0">Zone: ' + zinfo.side + " (" + sideName + ") - <b>" + zinfo.word + "</b> (leader share " + zinfo.S_.toFixed(1) + "%)" + (zinfo.gatedFrom ? " <b>gated</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") + "</div>" +''', count=1, tag="zone line ctx marker")


# --- v2.7.0: C4 — render + save flows use computeZoneCtx
rep(r'''    evidenceSummationHtml(hp, ap, paths, ag) +''',
    r'''    evidenceSummationHtml(hp, ap, paths, ag, ag ? computeZoneCtx(paths, ag, hid, aid, cutoff) : null) +''', count=1, tag="render passes demoted zone")

rep(r'''    zone: ag ? computeZone(x.paths, ag).tag : null,''',
    r'''    zone: ag ? computeZoneCtx(x.paths, ag, x.hid, x.aid, x.cutoff).tag : null,''', count=1, tag="saved verdict uses ctx-aware zone tag")


# --- v2.7.1: C5 draw-risk drop in computeZone (CALIBRATION-3.md)
rep(r'''  if ((key === "strong" || key === "win") && agree < 2) { gatedFrom = zn.zone; key = "windraw"; }
  var word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[key];
  var side = leaderSide === "H" ? "TA" : "TB";
  return { S_: S_, key: key, word: word, side: side, agree: agree, contra: contra,
           gatedFrom: gatedFrom, secs: secs,
           tag: side + " " + word + " " + S_.toFixed(1) + "%" + (gatedFrom ? " (gated from " + gatedFrom + ")" : "") };''',
    r'''  if ((key === "strong" || key === "win") && agree < 2) { gatedFrom = zn.zone; key = "windraw"; }
  /* C5 draw-risk drop (CALIBRATION-3.md, measured on 600 replays): a post-gate WIN
     with no H2H evidence drew 31% vs the 18% pool rate — those games belong in the
     WIN-DRAW pair zone. STRONG untouched: its no-H2H cohort wins 80% (n=20). */
  var h2hN = (ag.phaseCounts && ag.phaseCounts.h2h) || 0;
  var c5From = null;
  if (key === "win" && h2hN === 0) { c5From = "WIN"; key = "windraw"; }
  var word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[key];
  var side = leaderSide === "H" ? "TA" : "TB";
  return { S_: S_, key: key, word: word, side: side, agree: agree, contra: contra,
           gatedFrom: gatedFrom, c5From: c5From, secs: secs,
           tag: side + " " + word + " " + S_.toFixed(1) + "%" + (gatedFrom ? " (gated from " + gatedFrom + ")" : "") + (c5From ? " (draw-risk drop: no H2H)" : "") };''', count=1, tag="C5 draw-risk drop in computeZone")

rep(r'''  zinfo.tag = zinfo.side + " " + zinfo.word + " " + zinfo.S_.toFixed(1) + "%" +
    (zinfo.gatedFrom ? " (gated from " + zinfo.gatedFrom + ")" : "") +
    (zinfo.ctxFrom ? " (CTX demoted from " + zinfo.ctxFrom + ")" : "");''',
    r'''  zinfo.tag = zinfo.side + " " + zinfo.word + " " + zinfo.S_.toFixed(1) + "%" +
    (zinfo.gatedFrom ? " (gated from " + zinfo.gatedFrom + ")" : "") +
    (zinfo.c5From ? " (draw-risk drop: no H2H)" : "") +
    (zinfo.ctxFrom ? " (CTX demoted from " + zinfo.ctxFrom + ")" : "");''', count=1, tag="CTX tag keeps C5 suffix")

rep(r'''  if (zinfo.gatedFrom) flags += '<div class="help" style="margin:2px 0 0">Confirmation gate: demoted from ' + zinfo.gatedFrom + " - only " + zinfo.agree + "/3 sections confirm the leader.</div>";''',
    r'''  if (zinfo.gatedFrom) flags += '<div class="help" style="margin:2px 0 0">Confirmation gate: demoted from ' + zinfo.gatedFrom + " - only " + zinfo.agree + "/3 sections confirm the leader.</div>";
  if (zinfo.c5From) flags += '<div class="help" style="margin:2px 0 0">Draw-risk drop: no H2H evidence - post-gate WIN games without H2H drew 31% (measured, n=26); set to WIN-DRAW.</div>';''', count=1, tag="summation renders C5 flag")

rep(r'''(zinfo.gatedFrom ? " <b>gated</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") + "</div>" +''',
    r'''(zinfo.gatedFrom ? " <b>gated</b>" : "") + (zinfo.c5From ? " <b>draw-risk</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") + "</div>" +''', count=1, tag="zone line draw-risk marker")

# --- v2.7.1: zone notes now describe the shipped post-gate post-C5 behavior
rep(r'''  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "measured: leader won 73%, draw 12% (n=74)" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "measured: leader won 61%, leader-or-draw 80% (n=166)" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "measured: leader-or-draw pair covered 72% (n=146)" };''',
    r'''  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "measured post-gate: leader won 78%, leader-or-draw 92% (n=60)" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "measured post-gate+C5: leader won 65%, leader-or-draw 80% (n=125)" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "measured post-gate+C5: leader-or-draw pair covered 72% (n=201)" };''', count=1, tag="zone notes post-gate post-C5")

open(SRC, "w", encoding="utf-8").write(s)
print("\nPART B complete:", edits, "edits applied, %d bytes" % len(s))
