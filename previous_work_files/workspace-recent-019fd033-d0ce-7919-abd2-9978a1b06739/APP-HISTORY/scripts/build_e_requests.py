#!/usr/bin/env python3
# Build step E: v2.8.2-cross — auto-audit standby request emitter (AUTO-REQUESTS.md).
# Display-only: emits fixture-specific OPTIONAL data requests from the analysis's own
# gap spots (sparse history / no H2H / cold start / cup-only side / ledger-open gaps /
# section conflict / thin evidence ring). Unanswered requests change nothing.
# Conditions answers parse via existing CTX channel (demote-only, never boosts);
# results answers parse via existing MATCH import (add evidence). Exact-match edits.
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
rep('v2.8.1-cross</span></h1>', 'v2.8.2-cross</span></h1>', tag="header version")
rep('Pitch Rating v2.8.1-cross &middot; model built 2026-08-01 from match results only',
    'Pitch Rating v2.8.2-cross &middot; model built 2026-08-01 from match results only', tag="footer version")

# ---------- 2. emitter function, before evidenceSummationHtml ----------
rep('function evidenceSummationHtml(hp, ap, paths, ag, zinfo) {',
    '''/* Auto-audit standby requests (v2.8.2, AUTO-REQUESTS.md): fixture-specific OPTIONAL
   data requests emitted from the analysis's own gap spots. Display-only - unanswered
   requests change nothing. Conditions answers (CTX lines) are demote-only context and
   never raise a zone; results answers (MATCH rows) add evidence. Both paste via Data
   -> import. No zone, share or gate behavior is altered by this block. */
function gapAuditRequestsHtml(hp, ap, paths, ag, hid, aid, cutoff, zinfo) {
  if (!cutoff) return "";
  var reqs = [], pre = [];
  var comp = "";
  try { comp = (BlueprintEmbed.competition && BlueprintEmbed.competition()) || ""; } catch (e) { comp = ""; }
  var pr = (typeof perfRatings === "function" && cutoff) ? perfRatings(hid, aid, cutoff) : null;
  var h2hN = (ag && ag.phaseCounts && ag.phaseCounts.h2h) || 0;
  function rowCount(teamId, wantLeague) {
    var ms = (BlueprintEmbed.store().matches || []).filter(function (m) {
      return m.date && m.date < cutoff && (m.homeId === teamId || m.awayId === teamId);
    });
    var lg = ms.filter(function (m) {
      var c = String(m.competition || "");
      return /League|Liga/.test(c) && !/Cup|Playoff/.test(c);
    }).length;
    return wantLeague ? lg : ms.length;
  }
  var totH = rowCount(hid, false), lgH = rowCount(hid, true);
  var totA = rowCount(aid, false), lgA = rowCount(aid, true);

  /* 1. sparse-history side (Elo-star < 5): current-squad conditions window */
  function sparseReq(name, star) {
    reqs.push(name + ": sparse evidence history (strength rating " + Math.round(star) + "/100). " +
      "Optional: current-squad conditions - demote-only, never raises the zone.");
    pre.push("CTX|" + name + "|" + cutoff + "|keeper-change/star-absence/new-manager-debut/rotation-risk|detail|source");
  }
  if (pr && pr.starH < 5) sparseReq(hp.name, pr.starH);
  if (pr && pr.starA < 5) sparseReq(ap.name, pr.starA);

  /* 2. no direct H2H evidence */
  if (ag && h2hN === 0) {
    reqs.push("No direct H2H evidence between these sides. Optional: historical mutual results (90-minute scores) as MATCH rows with sources.");
    pre.push("MATCH|YYYY-MM-DD|Competition|domestic-league|Home|HG|AG|Away|normal|unknown|City|Country||source");
  }

  /* 3. cold start: under 3 current-tourney games on either side */
  if (pr && (!pr.home || !pr.away)) {
    var coldName = !pr.home ? hp.name : ap.name;
    reqs.push(coldName + ": cold start (under 3 current-tourney games) - performance guard cannot read this side yet. Optional: early-season or preseason results as MATCH rows.");
  }

  /* 4. cup-only side: results exist but no league-season rows */
  if (totH > 3 && lgH === 0) reqs.push(hp.name + ": cup-only history in store (no league rows). Optional: league season results as MATCH rows (adds evidence).");
  if (totA > 3 && lgA === 0) reqs.push(ap.name + ": cup-only history in store (no league rows). Optional: league season results as MATCH rows (adds evidence).");

  /* 5. ledger-open gaps touching this competition */
  if (/Czech/i.test(comp)) reqs.push("Ledger note: Czech 2.liga rows remain open (R-02, batch rejected twice - resend with self-checked standings checksums).");
  if (/Russian Cup/i.test(comp)) reqs.push("Ledger note: Russian First League (second tier) season rows not loaded - cup-opponent histories are cup-only.");
  if (/Kosovo|Albania/i.test(comp)) reqs.push("Ledger note: R-06 Kosovo/Albania 2025-26 rows need exact match dates (matrices carry none - unusable causally without them).");

  /* 6. section conflict: contra-leading section exists */
  if (zinfo && zinfo.contra && zinfo.contra.length) {
    zinfo.contra.forEach(function (c) {
      var who = c.side === "H" ? hp.name : ap.name;
      reqs.push("Section conflict: " + c.name + " contra-leads " + who + " at " + c.lead.toFixed(1) + "%. Optional: current-squad conditions for " + who + " (demote-only).");
      pre.push("CTX|" + who + "|" + cutoff + "|keeper-change/star-absence/new-manager-debut/rotation-risk|detail|source");
    });
  }

  /* 7. thin evidence ring */
  if (ag && paths.length > 0 && paths.length < 20) {
    reqs.push("Thin evidence ring (" + paths.length + " paths). Optional: additional common-opponent or league rows would firm the summation.");
  }

  if (!reqs.length) return "";
  var uniqPre = [...new Set(pre)];
  return '<div class="card"><h2>Standby optional requests (auto-audit)</h2>' +
    '<div class="help">Optional asks only - unanswered, the analysis stands exactly as computed. ' +
    "Conditions answers (CTX lines) are demote-only context and can never raise a zone. " +
    "Results answers (MATCH rows) add evidence. Paste answers on the Data tab (import).</div>" +
    reqs.map(function (r) { return '<div class="kv" style="margin:4px 0 0"><span class="k">request</span><span>' + esc(r) + "</span></div>"; }).join("") +
    (uniqPre.length ? '<div class="help" style="margin:8px 0 2px">Copy-ready answer templates (fill, then paste back):</div>' +
      '<pre class="help" style="white-space:pre-wrap;margin:4px 0 0">' + esc(uniqPre.join("\\n")) + "</pre>" : "") +
    "</div>";
}
function evidenceSummationHtml(hp, ap, paths, ag, zinfo) {''',
    tag="emitter function")

# ---------- 3. compute zinfo once, render emitter in the analysis card ----------
rep('''  const confirmed = document.getElementById("confirmVenue").checked;

  let html = '<div class="card"><h2>Evidence verdict — cross fixture</h2>' +''',
    '''  const confirmed = document.getElementById("confirmVenue").checked;
  const zinfoMain = ag ? computeZoneCtx(paths, ag, hid, aid, cutoff) : null;

  let html = '<div class="card"><h2>Evidence verdict — cross fixture</h2>' +''',
    tag="zinfoMain declaration")
rep('''    evidenceSummationHtml(hp, ap, paths, ag, ag ? computeZoneCtx(paths, ag, hid, aid, cutoff) : null) +
    PitchEvidenceBalance.render({''',
    '''    evidenceSummationHtml(hp, ap, paths, ag, zinfoMain) +
    gapAuditRequestsHtml(hp, ap, paths, ag, hid, aid, cutoff, zinfoMain) +
    PitchEvidenceBalance.render({''',
    tag="render call")

open(SRC, "w", encoding="utf-8").write(s)
print("BUILD E complete: %d edits -> v2.8.2-cross (auto-audit request emitter)" % edits)
