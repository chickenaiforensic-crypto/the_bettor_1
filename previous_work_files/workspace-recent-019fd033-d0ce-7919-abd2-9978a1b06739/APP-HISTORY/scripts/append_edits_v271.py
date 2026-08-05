#!/usr/bin/env python3
# v2.7.1: C5 draw-risk drop (post-gate WIN + no h2h -> WIN-DRAW), measured in study_c5_age.js.
a = open('build_a_edits.py', encoding='utf-8').read()
assert a.count('v2.7.0-cross') == 2, 'A refs: %d' % a.count('v2.7.0-cross')
open('build_a_edits.py', 'w', encoding='utf-8').write(a.replace('v2.7.0-cross', 'v2.7.1-cross'))

b = open('build_b_edits.py', encoding='utf-8').read()
anchor = 'open(SRC, "w", encoding="utf-8").write(s)'
assert b.count(anchor) == 1
new_edits = """
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

"""
b = b.replace(anchor, new_edits + anchor)
open('build_b_edits.py', 'w', encoding='utf-8').write(b)
print('append_edits_v271 OK')
