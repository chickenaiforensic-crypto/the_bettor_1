#!/usr/bin/env python3
# v2.7.0: Candidate A (venue-corrected H2H + saturation) + C4 (context flags, demote-only).
a = open('build_a_edits.py', encoding='utf-8').read()
assert a.count('v2.6.9-cross') == 2, 'A refs: %d' % a.count('v2.6.9-cross')
open('build_a_edits.py', 'w', encoding='utf-8').write(a.replace('v2.6.9-cross', 'v2.7.0-cross'))

b = open('build_b_edits.py', encoding='utf-8').read()
anchor = 'open(SRC, "w", encoding="utf-8").write(s)'
assert b.count(anchor) == 1
new_edits = """
# --- v2.7.0: Candidate A — venue-corrected H2H + saturation shrinkage (AUDIT-DISTRIBUTION.md)
rep(r'''  function buildEvidence(homeId, awayId, cutoff){
    var paths=[];
    BP.matches.filter(function(m){return beforeCutoff(m,cutoff)&&involves(m,homeId)&&involves(m,awayId);}).forEach(function(m){
      var est=gdFor(m,homeId);
      paths.push({phase:'h2h', estimate:est, weight:PHASE_WEIGHT.h2h*venueFactor(m.venue), ids:[m.id], label:m.date+' '+teamName(m.homeId)+' '+m.hg+'-'+m.ag+' '+teamName(m.awayId)+' ('+venueLabel(m.venue)+')', context:m.competition});
    });''',
    r'''  /* Candidate A (v2.7.0, AUDIT-DISTRIBUTION.md): venue-corrected H2H + saturation.
     Each H2H meeting is restated to the focal-home-venue equivalent: strip the venue
     edge the meeting actually carried (H2H_HFA*venueFactor, sign by who hosted), add
     the fixture's own edge (H2H_HFA). Away wins count more, away losses count less.
     Total H2H section weight saturates at H2H_SAT_FULL meeting-equivalents, so deep
     one-sided H2H piles no longer drown the other sections. */
  var H2H_HFA=0.35;   /* measured venue edge, RPL replay universe 2024-26: +0.34 */
  var H2H_SAT_FULL=2; /* meeting-equivalents at which H2H section weight caps */
  function h2hVenueCorrection(m, homeId, awayId){
    var vf=venueFactor(m.venue);
    if(m.homeId===homeId) return H2H_HFA*(1-vf);
    if(m.homeId===awayId) return H2H_HFA*(1+vf);
    return 0;
  }
  function buildEvidence(homeId, awayId, cutoff){
    var paths=[];
    var h2hMs=BP.matches.filter(function(m){return beforeCutoff(m,cutoff)&&involves(m,homeId)&&involves(m,awayId);});
    var hShrink=h2hMs.length?Math.min(1,H2H_SAT_FULL/h2hMs.length):1;
    h2hMs.forEach(function(m){
      var est=gdFor(m,homeId)+h2hVenueCorrection(m,homeId,awayId);
      paths.push({phase:'h2h', estimate:est, weight:PHASE_WEIGHT.h2h*venueFactor(m.venue)*hShrink, ids:[m.id], label:m.date+' '+teamName(m.homeId)+' '+m.hg+'-'+m.ag+' '+teamName(m.awayId)+' ('+venueLabel(m.venue)+')', context:m.competition});
    });''', count=1, tag="Candidate A venue-corrected H2H + saturation")

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

rep(r'''    '<div class="help" style="margin:0 0 4px"><b>Percentage analysis</b> - evidence-weight distribution per section and total, out of 100%. Evidence shares, not win probability.</div>' +''',
    r'''    '<div class="help" style="margin:0 0 4px"><b>Percentage analysis</b> - evidence-weight distribution per section and total, out of 100%. Evidence shares, not win probability. H2H rows are venue-corrected to this fixture\'s venue and H2H weight saturates beyond two meetings.</div>' +''', count=1, tag="summation note: Candidate A disclosure")

# --- v2.7.0: C4 — render + save flows use computeZoneCtx
rep(r'''    evidenceSummationHtml(hp, ap, paths, ag) +''',
    r'''    evidenceSummationHtml(hp, ap, paths, ag, ag ? computeZoneCtx(paths, ag, hid, aid, cutoff) : null) +''', count=1, tag="render passes demoted zone")

rep(r'''    zone: ag ? computeZone(x.paths, ag).tag : null,''',
    r'''    zone: ag ? computeZoneCtx(x.paths, ag, x.hid, x.aid, x.cutoff).tag : null,''', count=1, tag="saved verdict uses ctx-aware zone tag")

"""
b = b.replace(anchor, new_edits + anchor)
open('build_b_edits.py', 'w', encoding='utf-8').write(b)
print('append_edits_v270 OK')
