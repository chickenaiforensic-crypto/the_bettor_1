#!/usr/bin/env python3
# v2.6.9: zone confirmation gate (C2) + shared computeZone helper.
a = open('build_a_edits.py', encoding='utf-8').read()
assert a.count('v2.6.8-cross') == 2, 'A refs: %d' % a.count('v2.6.8-cross')
open('build_a_edits.py', 'w', encoding='utf-8').write(a.replace('v2.6.8-cross', 'v2.6.9-cross'))

b = open('build_b_edits.py', encoding='utf-8').read()
anchor = 'open(SRC, "w", encoding="utf-8").write(s)'
assert b.count(anchor) == 1
new_edits = """
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
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \\u00b7 Draw " + pct0(D) + " \\u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
    '<div class="help" style="margin:4px 0 0">Zone: ' + side + " - <b>" + zn.zone + "</b> (leader share " + S_.toFixed(1) + "% - " + esc(zn.note) + ")</div>" +
    "</div>";
}''',
    r'''  var zinfo = computeZone(paths, ag), secs = zinfo.secs;
  var rows = "";
  secs.forEach(function (s) {
    rows += '<div class="kv" style="margin:4px 0 0"><span class="k">' + esc(s.name) + '</span><span>' +
      esc(hp.name) + " <b>" + pct0(s.hW / s.W) + "</b> \\u00b7 draw " + pct0(s.dW / s.W) + " \\u00b7 " + esc(ap.name) + " <b>" + pct0(s.aW / s.W) + "</b>" +
      ' <span class="help">(\\u03a3w ' + s.W.toFixed(1) + ")</span></span></div>";
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
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \\u00b7 Draw " + pct0(D) + " \\u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
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
      esc(hp.name) + " <b>" + pct0(hW / W) + "</b> \\u00b7 draw " + pct0(dW / W) + " \\u00b7 " + esc(ap.name) + " <b>" + pct0(aW / W) + "</b>" +
      ' <span class="help">(\\u03a3w ' + W.toFixed(1) + " \\u00b7 " + ps.length + " path" + (ps.length === 1 ? "" : "s") + ")</span></span></div>";
  }
''',
    r'''function evidenceSummationHtml(hp, ap, paths, ag) {
  if (!ag) return "";
''', count=1, tag="remove old inline sectionRow (moved to sectionShares)")

rep(r'''    zone: ag ? (function(){ var tw = ag.homeW + ag.neuW + ag.awayW; var S_ = Math.max(ag.homeW, ag.awayW) / tw * 100; var zn = zoneLadder(S_); return (ag.homeW >= ag.awayW ? "TA " : "TB ") + zn.zone + " " + S_.toFixed(1) + "%"; })() : null,''',
    r'''    zone: ag ? computeZone(x.paths, ag).tag : null,''', count=1, tag="saved verdict uses gated zone tag")

"""
open('build_b_edits.py', 'w', encoding='utf-8').write(b.replace(anchor, new_edits + anchor))
print('v2.6.9 edits appended')
