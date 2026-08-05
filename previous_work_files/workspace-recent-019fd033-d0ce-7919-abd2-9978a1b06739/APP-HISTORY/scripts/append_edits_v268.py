#!/usr/bin/env python3
# Append v2.6.8 edits to build_b_edits.py and bump build_a version strings.
a = open('build_a_edits.py', encoding='utf-8').read()
assert a.count('v2.6.7-cross') == 2, 'Part A version refs: %d' % a.count('v2.6.7-cross')
open('build_a_edits.py', 'w', encoding='utf-8').write(a.replace('v2.6.7-cross', 'v2.6.8-cross'))

b = open('build_b_edits.py', encoding='utf-8').read()
anchor = 'open(SRC, "w", encoding="utf-8").write(s)'
assert b.count(anchor) == 1
new_edits = """
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
      esc(hp.name) + " <b>" + pct0(hW / W) + "</b> \\u00b7 draw " + pct0(dW / W) + " \\u00b7 " + esc(ap.name) + " <b>" + pct0(aW / W) + "</b>" +
      ' <span class="help">(\\u03a3w ' + W.toFixed(1) + " \\u00b7 " + ps.length + " path" + (ps.length === 1 ? "" : "s") + ")</span></span></div>";
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
    '<div style="margin:4px 0 0"><b>' + esc(hp.name) + " " + pct0(H) + " \\u00b7 Draw " + pct0(D) + " \\u00b7 " + esc(ap.name) + " " + pct0(A) + "</b></div>" +
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

"""
open('build_b_edits.py', 'w', encoding='utf-8').write(b.replace(anchor, new_edits + anchor))
print('build scripts updated: A=version 2.6.8, B=+3 edits')
