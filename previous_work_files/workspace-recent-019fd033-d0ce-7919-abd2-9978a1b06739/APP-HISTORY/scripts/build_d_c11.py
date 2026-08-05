#!/usr/bin/env python3
# Build step D: v2.8.1-cross — C11 cold-trailer star guard (CALIBRATION-5.md).
# Demote one rung (STRONG/WIN only) when the zone leader's opponent carries
# Elo-star < 5 (sparse history / newly arrived). Causal (perfRatings chain is
# strictly pre-cutoff), demote-only. Applied after build_c (C8). Exact-match
# replacements, counted; failures abort.
import sys

SRC = "/home/user/app-v2.6-cross.html"
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

# ---------- 1. version strings ----------
rep('v2.8.0-cross</span></h1>', 'v2.8.1-cross</span></h1>', tag="header version")
rep('Pitch Rating v2.8.0-cross &middot; model built 2026-08-01 from match results only',
    'Pitch Rating v2.8.1-cross &middot; model built 2026-08-01 from match results only', tag="footer version")

# ---------- 2. zone ladder notes: post-C11 measured numbers (632 replays) ----------
rep('''measured post-gate+C5+C8: leader won 78%, leader-or-draw 92% (n=59)''',
    '''measured post-gate+C5+C8+C11: leader won 80%, leader-or-draw 93% (n=15)''', tag="note strong")
rep('''measured post-gate+C5+C8: leader won 67%, leader-or-draw 82% (n=118)''',
    '''measured post-gate+C5+C8+C11: leader won 69%, leader-or-draw 89% (n=101)''', tag="note win")
rep('''measured post-gate+C5+C8: leader-or-draw pair covered 75% (n=166)''',
    '''measured post-gate+C5+C8+C11: leader-or-draw pair covered 77% (n=240)''', tag="note windraw")
rep('''measured post-gate+C5+C8: directional only, 47% (n=109)''',
    '''measured post-gate+C5+C8+C11: directional only, 48% (n=116)''', tag="note lean")
rep('''measured post-gate+C5+C8: leader won 45% (n=148) - no side earns it''',
    '''measured post-gate+C5+C8+C11: leader won 38% (n=160) - no side earns it''', tag="note toss")

# ---------- 3. C11 engine: demote block, after C8 block, before CTX flags ----------
rep('''  if (typeof BlueprintEmbed === "undefined" || !BlueprintEmbed.ctxFlagsFor) return zinfo;
  var flags = BlueprintEmbed.ctxFlagsFor(homeId, awayId, date) || [];''',
    '''  /* C11 cold-trailer star guard (CALIBRATION-5.md, measured on the 632-game masked
     replay): a zone leader whose opponent carries Elo-star < 5 (sparse history /
     newly arrived) rode evidence rings that overrate the established side - the
     trailer-star<5 cohort pair-dropped 13 pts below pool and held 17 of the 26
     actionable losses. Demote one rung (STRONG/WIN only); demote-only, never boosts. */
  if (pr && (zinfo.key === "strong" || zinfo.key === "win")) {
    var tStar11 = zinfo.side === "TA" ? pr.starA : pr.starH;
    if (tStar11 < 5) {
      var rungs11 = ["strong", "win", "windraw", "lean", "toss"], i11 = rungs11.indexOf(zinfo.key);
      zinfo.c11From = zinfo.word;
      zinfo.key = rungs11[i11 + 1];
      zinfo.word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[zinfo.key];
    }
  }
  if (typeof BlueprintEmbed === "undefined" || !BlueprintEmbed.ctxFlagsFor) return zinfo;
  var flags = BlueprintEmbed.ctxFlagsFor(homeId, awayId, date) || [];''',
    tag="C11 demote block")

# ---------- 4. tag + badges + flag line ----------
rep('''    (zinfo.c8From ? " (perf drop: tourney form opposes)" : "") +''',
    '''    (zinfo.c8From ? " (perf drop: tourney form opposes)" : "") +
    (zinfo.c11From ? " (star drop: cold opponent)" : "") +''', tag="tag c11")
rep('''  if (zinfo.c8From) flags += '<div class="help" style="margin:2px 0 0">Performance drop: opponent-weighted current-tourney form contradicts the leader - such games won only 38-40% on replay (CALIBRATION-4); demoted from ' + zinfo.c8From + ".</div>";''',
    '''  if (zinfo.c8From) flags += '<div class="help" style="margin:2px 0 0">Performance drop: opponent-weighted current-tourney form contradicts the leader - such games won only 38-40% on replay (CALIBRATION-4); demoted from ' + zinfo.c8From + ".</div>";
  if (zinfo.c11From) flags += '<div class="help" style="margin:2px 0 0">Star drop: opponent strength rating below 5 (sparse history) - such calls pair-dropped 13 pts and held 17 of 26 actionable losses on replay (CALIBRATION-5); demoted from ' + zinfo.c11From + ".</div>";''', tag="flag line c11")
rep(''' + (zinfo.c8From ? " <b>perf</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") +''',
    ''' + (zinfo.c8From ? " <b>perf</b>" : "") + (zinfo.c11From ? " <b>star</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") +''', tag="badge c11")

open(SRC, "w", encoding="utf-8").write(s)
print("BUILD D complete: %d edits -> v2.8.1-cross (C11 shipped)" % edits)
