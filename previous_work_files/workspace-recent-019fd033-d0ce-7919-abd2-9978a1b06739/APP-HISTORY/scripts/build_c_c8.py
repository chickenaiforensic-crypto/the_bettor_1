#!/usr/bin/env python3
# Build step C: v2.8.0-cross — C8 opponent-quality-weighted current-tourney
# performance rating (CALIBRATION-4.md). Applied onto app-v2.6-cross.html after
# build_a + build_b. Every replacement is exact-match and counted; failures abort.
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
rep('v2.7.1-cross</span></h1>', 'v2.8.0-cross</span></h1>', tag="header version")
rep('Pitch Rating v2.7.1-cross &middot; model built 2026-07-30 from match results only',
    'Pitch Rating v2.8.0-cross &middot; model built 2026-08-01 from match results only', tag="footer version")

# ---------- 2. zone ladder notes describe shipped post-C8 behavior (600 replays) ----------
rep('''  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "measured post-gate: leader won 78%, leader-or-draw 92% (n=60)" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "measured post-gate+C5: leader won 65%, leader-or-draw 80% (n=125)" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "measured post-gate+C5: leader-or-draw pair covered 72% (n=201)" };
  if (S >= 50) return { key: "lean",    zone: "lean",        note: "measured: directional only, 53% (n=97)" };
  return { key: "toss", zone: "TOSS", note: "measured: leader won 43% (n=115) - no side earns it" };''',
    '''  if (S >= 85) return { key: "strong",  zone: "STRONG CALL", note: "measured post-gate+C5+C8: leader won 78%, leader-or-draw 92% (n=59)" };
  if (S >= 65) return { key: "win",     zone: "WIN",         note: "measured post-gate+C5+C8: leader won 67%, leader-or-draw 82% (n=118)" };
  if (S >= 55) return { key: "windraw", zone: "WIN-DRAW",    note: "measured post-gate+C5+C8: leader-or-draw pair covered 75% (n=166)" };
  if (S >= 50) return { key: "lean",    zone: "lean",        note: "measured post-gate+C5+C8: directional only, 47% (n=109)" };
  return { key: "toss", zone: "TOSS", note: "measured post-gate+C5+C8: leader won 45% (n=148) - no side earns it" };''',
    tag="zone notes post-C8")

# ---------- 3. C8 engine: perfRatings before the C4 comment ----------
rep('''/* Context-flag demotion (C4). One rung per flag against the zone leader;''',
    '''/* C8 opponent-quality-weighted current-tourney performance rating (CALIBRATION-4.md,
   audited on the 600-game masked replay; shipped demote-only). Causal Elo chain
   over the whole store below the cutoff (start 1500, K=20, home +65);
   star = clamp((elo - 1420)/2, 0, 100). Current tourney = games on/after the
   season's Jul-1 boundary. SOS = mean star(opponent); Perf = mean
   result(1/.5/0) x star(opponent). Cold start (<3 tourney games) = no reading. */
function tourneyStart(d) { var y = +d.slice(0, 4), mo = +d.slice(5, 7); return (mo >= 7 ? y : y - 1) + "-07-01"; }
function perfRatings(homeId, awayId, cutoff) {
  if (typeof BlueprintEmbed === "undefined" || !BlueprintEmbed.store) return null;
  var ms = (BlueprintEmbed.store().matches || []).filter(function (m) {
    return m.date && m.date < cutoff && typeof m.hg === "number" && typeof m.ag === "number";
  });
  ms.sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });
  var E = {}, K = 20, HF = 65;
  ms.forEach(function (m) {
    var eh = E[m.homeId] || 1500, ea = E[m.awayId] || 1500;
    var p = 1 / (1 + Math.pow(10, -((eh + HF - ea) / 400)));
    var sc = m.hg > m.ag ? 1 : m.hg < m.ag ? 0 : 0.5;
    E[m.homeId] = eh + K * (sc - p);
    E[m.awayId] = ea + K * ((1 - sc) - (1 - p));
  });
  function star(e) { return Math.max(0, Math.min(100, (e - 1420) / 2)); }
  function perf(team) {
    var ss = tourneyStart(cutoff), n = 0, sos = 0, pf = 0;
    ms.forEach(function (m) {
      if (m.date < ss) return;
      var h = m.homeId === team;
      if (!h && m.awayId !== team) return;
      var opp = h ? m.awayId : m.homeId;
      var f = h ? m.hg : m.ag, c = h ? m.ag : m.hg;
      var st = star(E[opp] || 1500);
      sos += st; pf += (f > c ? 1 : f === c ? 0.5 : 0) * st; n++;
    });
    return n >= 3 ? { n: n, sos: sos / n, perf: pf / n } : null;
  }
  return { starH: star(E[homeId] || 1500), starA: star(E[awayId] || 1500), home: perf(homeId), away: perf(awayId) };
}
/* Context-flag demotion (C4). One rung per flag against the zone leader;''',
    tag="C8 perfRatings engine")

# ---------- 4. wire C8 into computeZoneCtx ----------
rep('''function computeZoneCtx(paths, ag, homeId, awayId, date) {
  var zinfo = computeZone(paths, ag);''',
    '''function computeZoneCtx(paths, ag, homeId, awayId, date) {
  var zinfo = computeZone(paths, ag);
  /* C8: demote one rung when the opponent-weighted current-tourney performance
     of the two sides contradicts the zone leader. Demote-only; never boosts. */
  var pr = date ? perfRatings(homeId, awayId, date) : null;
  if (pr) zinfo.perf = pr;
  if (pr && pr.home && pr.away) {
    var dp8 = pr.home.perf - pr.away.perf;
    if ((zinfo.side === "TA" && dp8 < 0) || (zinfo.side === "TB" && dp8 > 0)) {
      var rungs8 = ["strong", "win", "windraw", "lean", "toss"], i8 = rungs8.indexOf(zinfo.key);
      if (i8 >= 0 && i8 < rungs8.length - 1) {
        zinfo.c8From = zinfo.word;
        zinfo.key = rungs8[i8 + 1];
        zinfo.word = { strong: "STRONG CALL", win: "WIN", windraw: "WIN-DRAW", lean: "lean", toss: "TOSS" }[zinfo.key];
      }
    }
  }''',
    tag="C8 demote in computeZoneCtx")

# ---------- 5. tag assembly gains the C8 suffix ----------
rep('''    (zinfo.c5From ? " (draw-risk drop: no H2H)" : "") +
    (zinfo.ctxFrom ? " (CTX demoted from " + zinfo.ctxFrom + ")" : "");''',
    '''    (zinfo.c5From ? " (draw-risk drop: no H2H)" : "") +
    (zinfo.c8From ? " (perf drop: tourney form opposes)" : "") +
    (zinfo.ctxFrom ? " (CTX demoted from " + zinfo.ctxFrom + ")" : "");''',
    tag="tag keeps C8 suffix")

# ---------- 6. summation renders C8 flag ----------
rep('''  if (zinfo.c5From) flags += '<div class="help" style="margin:2px 0 0">Draw-risk drop: no H2H evidence - post-gate WIN games without H2H drew 31% (measured, n=26); set to WIN-DRAW.</div>';''',
    '''  if (zinfo.c5From) flags += '<div class="help" style="margin:2px 0 0">Draw-risk drop: no H2H evidence - post-gate WIN games without H2H drew 31% (measured, n=26); set to WIN-DRAW.</div>';
  if (zinfo.c8From) flags += '<div class="help" style="margin:2px 0 0">Performance drop: opponent-weighted current-tourney form contradicts the leader - such games won only 38-40% on replay (CALIBRATION-4); demoted from ' + zinfo.c8From + ".</div>";''',
    tag="summation renders C8 flag")

# ---------- 7. zone line perf marker ----------
rep('''(zinfo.c5From ? " <b>draw-risk</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") + "</div>" +''',
    '''(zinfo.c5From ? " <b>draw-risk</b>" : "") + (zinfo.c8From ? " <b>perf</b>" : "") + (zinfo.ctxFrom ? " <b>ctx</b>" : "") + "</div>" +''',
    tag="zone line perf marker")

# ---------- 8. current-tourney status block above Total summation ----------
rep('''    '<div class="help" style="margin:10px 0 2px"><b>Total summation</b></div>' +''',
    '''    (zinfo.perf ? '<div class="help" style="margin:8px 0 2px"><b>Current tourney status</b> - opponent-quality-weighted results this season. Star = strength (0-100); SOS = schedule faced; performance = results weighted by opponent quality. Under 3 tourney games: cold start, rating does not move the zone.</div>' +
      '<div class="kv" style="margin:2px 0 0"><span class="k">' + esc(hp.name) + '</span><span>star <b>' + zinfo.perf.starH.toFixed(0) + '</b>' + (zinfo.perf.home ? ' · ' + zinfo.perf.home.n + ' games · SOS ' + zinfo.perf.home.sos.toFixed(1) + ' · performance <b>' + zinfo.perf.home.perf.toFixed(1) + '</b> · conversion ' + (zinfo.perf.home.sos ? Math.round(100 * zinfo.perf.home.perf / zinfo.perf.home.sos) : 0) + '%' : ' · cold start (under 3 games)') + '</span></div>' +
      '<div class="kv" style="margin:2px 0 0"><span class="k">' + esc(ap.name) + '</span><span>star <b>' + zinfo.perf.starA.toFixed(0) + '</b>' + (zinfo.perf.away ? ' · ' + zinfo.perf.away.n + ' games · SOS ' + zinfo.perf.away.sos.toFixed(1) + ' · performance <b>' + zinfo.perf.away.perf.toFixed(1) + '</b> · conversion ' + (zinfo.perf.away.sos ? Math.round(100 * zinfo.perf.away.perf / zinfo.perf.away.sos) : 0) + '%' : ' · cold start (under 3 games)') + '</span></div>' : '') +
    '<div class="help" style="margin:10px 0 2px"><b>Total summation</b></div>' +''',
    tag="tourney status block")

open(SRC, "w", encoding="utf-8").write(s)
print("\nPART C complete:", edits, "edits applied, %d bytes" % len(s))
