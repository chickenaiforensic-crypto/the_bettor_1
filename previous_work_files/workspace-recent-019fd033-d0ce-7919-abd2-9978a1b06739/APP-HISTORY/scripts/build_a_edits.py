#!/usr/bin/env python3
# Build app-v2.6-cross.html from uploads/app-v2.5-final.html
# Part A: strip contamination, front-page (Rate) + Log edits.
import re, sys, shutil

SRC = "/home/user/uploads/app-v2.5-final.html"
DST = "/home/user/app-v2.6-cross.html"
shutil.copyfile(SRC, DST)
s = open(DST, encoding="utf-8").read()
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

# ---------- 0. strip Cloudflare challenge artifacts (page-save contamination) ----------
before = s
s = re.sub(r'<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>', '', s, flags=re.S)
n = len(re.findall(r'challenge-platform', before)) - len(re.findall(r'challenge-platform', s))
if s.count('challenge-platform') != 0:
    print("FAIL [cf strip]: artifacts remain"); sys.exit(1)
edits += 1
print("ok  [cf strip: removed %d artifact lines]" % n)

# ---------- 1. version labels ----------
rep('v2.1-live</span></h1>', 'v2.7.1-cross</span></h1>', tag="header version")
rep('Football home-match rating &middot; built from 153,058 results &middot; no bookmaker data',
    'Football match rating &middot; any team v any team &middot; built from 153,058 results &middot; no bookmaker data', tag="header sub")
rep('Pitch Rating v2.1-live &middot; model built 2026-07-30 from match results only',
    'Pitch Rating v2.7.1-cross &middot; model built 2026-07-30 from match results only', tag="footer version")

# ---------- 2. Fixture card: league becomes a filter, add search ----------
rep(r'''      <h2>Fixture</h2>
      <div class="help">Pick the league, then the home and away side. Only rated teams appear.</div>
      <div style="margin-bottom:11px">
        <label class="fl">League</label>
        <select id="league" onchange="onLeagueChange()"></select>
      </div>''',
    r'''      <h2>Fixture</h2>
      <div class="help">Pick any two sides — every rated league team and every team loaded through the Data tab. The league box and search only filter the lists; they never restrict what you can rate.</div>
      <div class="row2" style="margin-bottom:11px">
        <div>
          <label class="fl">Filter by league (optional)</label>
          <select id="league" onchange="onLeagueChange()"></select>
        </div>
        <div>
          <label class="fl">Search teams (optional)</label>
          <input type="text" id="teamSearch" placeholder="Type to filter both lists&hellip;" oninput="onLeagueChange()">
        </div>
      </div>''', tag="fixture card")

# ---------- 3. league-country map + cross-league engine helpers ----------
rep("const FACT = [1,1,2,6,24,120,720,5040,40320,362880,3628800];",
    r'''const LEAGUE_COUNTRY = {B1:"Belgium", D1:"Germany", D2:"Germany", E0:"England", E1:"England",
  E2:"England", E3:"England", F1:"France", F2:"France", G1:"Greece", I1:"Italy", I2:"Italy",
  N1:"Netherlands", P1:"Portugal", SC0:"Scotland", SP1:"Spain", SP2:"Spain", T1:"Turkey"};

/* --- cross-league expected goals — blueprint §3 approved working baseline:
   unweighted bridge scale = 1.00. Each side contributes its own league's
   parameters; home advantage and home form come from the home league. ------ */
function lambdasCross(lgH, homeTeam, lgA, awayTeam) {
  const L1 = MODEL.leagues[lgH], L2 = MODEL.leagues[lgA];
  const T1 = MODEL.teams[lgH], T2 = MODEL.teams[lgA];
  if (!L1 || !L2 || !T1 || !T2 || !T1[homeTeam] || !T2[awayTeam]) return null;
  const [ah, dh, xh] = T1[homeTeam];
  const [aa, da] = T2[awayTeam];
  let lh = Math.exp(L1.mu + ah - da + L1.hfa + xh);
  let la = Math.exp(L2.mu + aa - dh);
  lh = Math.max(0.05, Math.min(6, lh));
  la = Math.max(0.05, Math.min(6, la));
  return { lh, la };
}

/* consensus lens across leagues: each side's GD/game from its own league records */
function consensusCross(lgH, homeTeam, lgA, awayTeam) {
  const H = teamRecord(lgH, homeTeam), A = teamRecord(lgA, awayTeam);
  if (!H || !A) return null;
  const mg = MODEL.consensus.min_games;
  if (H.hp < mg || A.hp < mg || H.ap < mg || A.ap < mg) return null;
  const hvh = (H.hgf - H.hga)/H.hp - (A.hgf - A.hga)/A.hp;
  const ava = (H.agf - H.aga)/H.ap - (A.agf - A.aga)/A.ap;
  return { hvh: hvh, ava: ava, consensus: (hvh + ava)/2, disagreement: Math.abs(hvh - ava) };
}

const FACT = [1,1,2,6,24,120,720,5040,40320,362880,3628800];''', tag="cross-league helpers")

# ---------- 4. initLeagues + universal pickers ----------
block("function initLeagues() {", "function onTeamChange() {", r'''function initLeagues() {
  const sel = document.getElementById("league");
  const keys = Object.keys(MODEL.leagues).sort(function (a, b) {
    return MODEL.leagues[a].name.localeCompare(MODEL.leagues[b].name);
  });
  sel.innerHTML = '<option value="__ALL__">All teams — cross fixture (any team v any team)</option>' +
    keys.map(function (k) {
      return '<option value="' + esc(k) + '">' + esc(MODEL.leagues[k].name) + "</option>";
    }).join("");
  sel.value = "__ALL__";
  onLeagueChange();
}

/* ---------- universal team universe ---------------------------------------
   Every rated row, grouped by league (a name that rates in two leagues is two
   separate rating rows and stays two options), plus every identity loaded via
   the Data tab that has no rated row, grouped by country. Any option may be
   picked against any other — selection is never restricted. */
function teamUniverse() {
  const rated = [], bpOnly = [];
  Object.keys(MODEL.teams).sort(function (a, b) {
    return MODEL.leagues[a].name.localeCompare(MODEL.leagues[b].name);
  }).forEach(function (lg) {
    Object.keys(MODEL.teams[lg]).sort().forEach(function (t) {
      rated.push({ value: "R|" + lg + "|" + t, label: t + " — " + MODEL.leagues[lg].name,
        group: MODEL.leagues[lg].name, lg: lg, name: t });
    });
  });
  try {
    const BPx = (window.BlueprintEmbed && BlueprintEmbed.store) ? BlueprintEmbed.store() : null;
    if (BPx && BPx.identities) {
      Object.keys(BPx.identities).forEach(function (k) {
        const it = BPx.identities[k];
        if (!it || !it.name) return;
        const hasRatedRow = (it.leagues || []).some(function (lg) {
          return MODEL.teams[lg] && MODEL.teams[lg][it.name];
        });
        if (hasRatedRow) return;
        bpOnly.push({ value: "B|" + (it.country || "?") + "|" + it.name,
          label: it.name + " — " + (it.country || "?") + " / " + ((it.leagues && it.leagues[0]) || "loaded team data"),
          group: "Loaded teams — " + (it.country || "?"), country: it.country,
          leagues: it.leagues || [], name: it.name });
      });
    }
  } catch (e) { /* blueprint store not ready — rated teams still work */ }
  bpOnly.sort(function (a, b) { return a.label.localeCompare(b.label); });
  return rated.concat(bpOnly);
}

function parsePick(v) {
  const p = String(v || "").split("|");
  if (p[0] === "R" && p.length === 3) {
    return { kind: "R", lg: p[1], name: p[2], country: LEAGUE_COUNTRY[p[1]] || p[1], value: v };
  }
  if (p[0] === "B" && p.length >= 3) {
    return { kind: "B", country: p[1], name: p.slice(2).join("|"), value: v };
  }
  return null;
}
window.__parsePick = parsePick;

function pickOptionsHtml(list) {
  let html = '<option value="">&mdash; select &mdash;</option>', grp = null;
  list.forEach(function (x) {
    if (x.group !== grp) {
      if (grp !== null) html += "</optgroup>";
      html += '<optgroup label="' + esc(x.group) + '">';
      grp = x.group;
    }
    html += '<option value="' + esc(x.value) + '">' + esc(x.label) + "</option>";
  });
  if (grp !== null) html += "</optgroup>";
  return html;
}

function onLeagueChange() {
  const flt = document.getElementById("league").value;
  const sBox = document.getElementById("teamSearch");
  const q = ((sBox && sBox.value) || "").toLowerCase().trim();
  const hSel = document.getElementById("homeTeam"), aSel = document.getElementById("awayTeam");
  const keepH = hSel.value, keepA = aSel.value;
  let list = teamUniverse();
  if (flt !== "__ALL__") {
    list = list.filter(function (x) {
      return x.lg === flt || (x.leagues && x.leagues.indexOf(flt) !== -1);
    });
  }
  if (q) list = list.filter(function (x) { return x.label.toLowerCase().indexOf(q) !== -1; });
  const html = pickOptionsHtml(list);
  hSel.innerHTML = html; aSel.innerHTML = html;
  /* restore previous picks when still visible */
  if (keepH && list.some(function (x) { return x.value === keepH; })) hSel.value = keepH;
  if (keepA && list.some(function (x) { return x.value === keepA; })) aSel.value = keepA;
  onTeamChange();
}

''', tag="universal pickers")

# teamSearch box doesn't exist until fixture card edit — guard already in place.

# ---------- 5. onTeamChange: confirm label resolves parsed pick ----------
OLD_OTC = (
'function onTeamChange() {\n'
+ '  document.getElementById(%sconfirmVenue%s).checked = false;\n' % (chr(34), chr(34))
+ '  const h = document.getElementById(%shomeTeam%s).value;\n' % (chr(34), chr(34))
+ '  document.getElementById(%sconfirmHome%s).textContent = h || %s%su2014%s;\n' % (chr(34), chr(34), chr(34), chr(92), chr(34))
+ '  renderRate();\n'
+ '}')
NEW_OTC = OLD_OTC.replace(
  'const h = document.getElementById(%shomeTeam%s).value;' % (chr(34), chr(34)),
  'const h = parsePick(document.getElementById(%shomeTeam%s).value);' % (chr(34), chr(34)))
NEW_OTC = NEW_OTC.replace('h || %s%su2014%s' % (chr(34), chr(92), chr(34)), 'h ? h.name : %s%su2014%s' % (chr(34), chr(92), chr(34)))
rep(OLD_OTC, NEW_OTC, tag="onTeamChange")


# ---------- 6. renderRate: dispatch domestic / cross-league / evidence ----------
block("function renderRate() {", "function tierBadge(name) {", r'''function renderRate() {
  const hp = parsePick(document.getElementById("homeTeam").value);
  const ap = parsePick(document.getElementById("awayTeam").value);
  const flipBox = document.getElementById("flipBox");
  const out = document.getElementById("result");
  document.getElementById("confirmHome").textContent = hp ? hp.name : "—";

  flipBox.innerHTML = "";
  out.innerHTML = "";
  lastRating = null;
  lastEvidence = null;

  if (!hp || !ap) {
    out.innerHTML = '<div class="banner ban-info">Select both teams to produce a rating — any two sides, including cross-league, cross-border, international-tournament and Data-tab loaded teams.</div>';
    return;
  }
  if (document.getElementById("homeTeam").value === document.getElementById("awayTeam").value) {
    out.innerHTML = '<div class="banner ban-err">A team cannot play itself.</div>';
    return;
  }

  if (hp.kind === "R" && ap.kind === "R" && hp.lg === ap.lg) {
    renderDomesticRate(hp.lg, hp.name, ap.name);
    if (window.BlueprintEmbed && BlueprintEmbed.appendAudit) BlueprintEmbed.appendAudit();
    return;
  }

  /* cross fixtures: no league host history to auto-check against */
  flipBox.innerHTML = '<div class="banner ban-warn"><b>Venue cannot be auto-checked for this fixture.</b><br>' +
    "Cross-league, cross-border and loaded-team fixtures have no shared league host history in the model. " +
    "Confirm the venue by hand before saving — a saved rating with the sides reversed is worse than no rating.</div>";

  if (hp.kind === "R" && ap.kind === "R") {
    renderCrossLeague(hp, ap);
    if (window.BlueprintEmbed && BlueprintEmbed.appendAudit) BlueprintEmbed.appendAudit();
  } else {
    renderEvidenceFixture(hp, ap);
  }
}

/* ---------- domestic: the original calibrated pipeline, unchanged -------- */
function renderDomesticRate(lg, h, a) {
  const flipBox = document.getElementById("flipBox");
  const out = document.getElementById("result");

  /* flip detection runs before anything else */
  const flip = flipCheck(lg, h, a);
  if (flip.messages.length) {
    const cls = flip.level === "error" ? "ban-err" : "ban-warn";
    const title = flip.level === "error" ? "Likely home/away flip" : "Flip cannot be auto-detected";
    flipBox.innerHTML = '<div class="banner ' + cls + '"><b>' + title + "</b><br>" +
      flip.messages.map(esc).join("<br>") + "</div>";
  } else {
    flipBox.innerHTML = '<div class="banner ban-ok">Venue plausible: ' + esc(h) +
      " regularly hosts in this league, and the sides are far enough apart that a flip would be visible.</div>";
  }

  const r = rateFixture(lg, h, a);
  if (r.error) {
    out.innerHTML = '<div class="banner ban-err">' + esc(r.error) + "</div>";
    return;
  }
  lastRating = r;

  const confirmed = document.getElementById("confirmVenue").checked;
  const badge = tierBadge(r.tier.name);

  let html = "";

  html += '<div class="card"><div class="verdict">' +
    '<div class="fixture">' + esc(h) + " v " + esc(a) + "</div>" +
    (r.starsHome ? '<div style="font-size:13px;color:#b45309;letter-spacing:1px;margin-bottom:3px">' +
      starStr(r.starsHome) + '<span style="color:#6b7280"> v </span>' + starStr(r.starsAway) + "</div>" : "") +
    '<div class="help" style="margin-bottom:9px">' + esc(MODEL.leagues[lg].name) + "</div>" +
    '<div class="pts">' + r.points + "</div>" +
    '<div class="ptslabel">home rating</div>' +
    '<div style="margin-top:9px"><span class="badge ' + badge + '">' + esc(r.tier.name) + "</span>" +
      (r.confidence ? ' <span class="badge ' + r.confidence.cls + '">' + esc(r.confidence.label) + "</span>" : "") +
      "</div>" +
    (r.confidence && r.confidence.rate
       ? '<div class="help" style="margin:6px 0 0">Historically ' + pct(r.confidence.rate) +
         (r.confidence.label === "DRAW-LEAN" ? " drew" : " won") + " from this position</div>"
       : (r.confidence ? '<div class="help" style="margin:6px 0 0">Model favours the home side but the venue records disagree — treat with caution</div>' : "")) +
    "</div>";

  html += ratingBarHtml(h, a, r.H, r.D, r.A);
  html += ratingKvHtml(r);
  html += marketsHtml(r);
  html += scorelinesHtml(r);
  html += saveCardHtml(confirmed, "saveRating()", "Save this rating");
  out.innerHTML = html;
}

/* ---------- cross-league: both sides rated, different leagues -------------
   Dixon–Coles combination at the blueprint §3 approved unweighted bridge
   (scale = 1.00). Standard model output; cross-league consensus badges and
   the intra-league star draw adjustment are withheld by design. ------------ */
function renderCrossLeague(hp, ap) {
  const out = document.getElementById("result");
  const lam = lambdasCross(hp.lg, hp.name, ap.lg, ap.name);
  if (!lam) {
    out.innerHTML = '<div class="banner ban-err">Cross-league rating unavailable: a rating row is missing for one side.</div>';
    return;
  }
  const { lh, la } = lam;
  const g = scoreGrid(lh, la);
  let H = 0, D = 0, A = 0;
  for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) {
    if (i > j) H += g[i][j]; else if (i === j) D += g[i][j]; else A += g[i][j];
  }
  const gg = goalsGrid(lh, la);
  let o15 = 0, o25 = 0, o35 = 0, hm1 = 0;
  for (let i = 0; i < KMAX; i++) for (let j = 0; j < KMAX; j++) {
    const p = gg[i][j], s2 = i + j;
    if (s2 > 1.5) o15 += p;
    if (s2 > 2.5) o25 += p;
    if (s2 > 3.5) o35 += p;
    if (i - j > 1) hm1 += p;
  }
  const lines = [];
  for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) lines.push({ s: i + "-" + j, p: g[i][j] });
  lines.sort((a, b) => b.p - a.p);

  const tier = tierFor(H);
  const es = expectedScore(g);
  const con = consensusCross(hp.lg, hp.name, ap.lg, ap.name);
  const sH = starsFor(hp.lg, hp.name), sA = starsFor(ap.lg, ap.name);
  const lgName = MODEL.leagues[hp.lg].name + " × " + MODEL.leagues[ap.lg].name;

  const r = {
    lg: hp.lg + "×" + ap.lg, lgName: lgName, homeTeam: hp.name, awayTeam: ap.name,
    lh, la, H, D, A, starsHome: sH, starsAway: sA, starAdj: false,
    consensus: con, confidence: null, expScore: es,
    points: Math.round(H * 100), tier, cross: true,
    markets: {
      dc1x: H + D, dc12: H + A, dcx2: D + A, dnb: H / (H + A),
      o15, u15: 1 - o15, o25, u25: 1 - o25, o35, u35: 1 - o35, hm1,
    },
    topScores: lines.slice(0, 5),
  };
  lastRating = r;

  const confirmed = document.getElementById("confirmVenue").checked;
  const badge = tierBadge(tier.name);

  let html = '<div class="banner ban-info"><b>Cross-league fixture.</b> Dixon–Coles ratings combined at the ' +
    "blueprint §3 approved baseline bridge (unweighted scale = 1.00). Standard model calibration tiers shown; " +
    "cross-league confidence badges and the intra-league star draw adjustment are withheld by design.</div>";

  html += '<div class="card"><div class="verdict">' +
    '<div class="fixture">' + esc(hp.name) + " v " + esc(ap.name) + "</div>" +
    (sH ? '<div style="font-size:13px;color:#b45309;letter-spacing:1px;margin-bottom:3px">' +
      starStr(sH) + '<span style="color:#6b7280"> v </span>' + starStr(sA) + "</div>" : "") +
    '<div class="help" style="margin-bottom:9px">' + esc(lgName) + "</div>" +
    '<div class="pts">' + r.points + "</div>" +
    '<div class="ptslabel">home rating</div>' +
    '<div style="margin-top:9px"><span class="badge ' + badge + '">' + esc(tier.name) + "</span></div>" +
    "</div>";

  html += ratingBarHtml(hp.name, ap.name, H, D, A);
  html += ratingKvHtml(r);
  html += marketsHtml(r);
  html += scorelinesHtml(r);
  html += saveCardHtml(confirmed, "saveRating()", "Save this rating");
  out.innerHTML = html;
}

/* ---------- evidence fixtures: one or both sides outside the rated set ----
   Fully computational — every pairing produces the evidence-engine verdict:
   H2H / common-opponent / level-3 paths, aggregate, classification, balance
   panel. NO CALL is a verdict and is displayed with its balance, never an
   empty screen or a substituted fixture. ---------------------------------- */
let lastEvidence = null;
function renderEvidenceFixture(hp, ap) {
  const out = document.getElementById("result");
  if (!window.BlueprintEmbed || !BlueprintEmbed.analyze) {
    out.innerHTML = '<div class="banner ban-err">Evidence engine not loaded — cannot compute this fixture.</div>';
    return;
  }
  const hid = BlueprintEmbed.resolve(hp.name, hp.country);
  const aid = BlueprintEmbed.resolve(ap.name, ap.country);
  if (!hid || !aid) {
    const missing = !hid ? hp.name : ap.name;
    out.innerHTML = '<div class="banner ban-err"><b>NO CALL — identity unresolved.</b><br>' +
      esc(missing) + " cannot be resolved to a canonical identity. Load its team data on the Data tab first. " +
      "No substitute fixture is used.</div>";
    return;
  }
  const cutoff = document.getElementById("matchDate").value ||
    (function(){const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");})();
  const ev = BlueprintEmbed.analyze(hid, aid, cutoff);
  const paths = ev.paths, ag = ev.ag, cl = ev.cl;
  lastEvidence = { hp, ap, hid, aid, cutoff, paths, ag, cl };

  const direction = !ag ? "no evidence" :
    ag.weighted > 0.25 ? "home lean" : ag.weighted < -0.25 ? "away lean" : "draw/neutral lean";
  const competition = (BlueprintEmbed.competition && BlueprintEmbed.competition()) || "";
  const bannerCls = cl.label.indexOf("NO CALL") !== -1 ? "ban-warn" :
    cl.label.indexOf("Calibrated") !== -1 ? "ban-ok" : "ban-info";
  const confirmed = document.getElementById("confirmVenue").checked;

  let html = '<div class="card"><h2>Evidence verdict — cross fixture</h2>' +
    '<div class="fixture">' + esc(hp.name) + " v " + esc(ap.name) + "</div>" +
    '<div class="help">Fixture context: ' + esc(competition || "cross fixture") +
    " &nbsp;|&nbsp; Evidence from loaded match data (graph rows " + ev.rows +
    "). One or both sides sit outside the calibrated domestic model, so this is the evidence-engine output.</div>" +
    '<div class="banner ' + bannerCls + '"><b>' + esc(cl.label) + "</b><br>" + esc(cl.reason) + "</div>" +
    PitchEvidenceBalance.render({
      home: { weight: ag ? ag.homeW : null, paths: ag ? ag.homeN : 0 },
      draw: { weight: ag ? ag.neuW : null, paths: ag ? ag.neuN : 0 },
      away: { weight: ag ? ag.awayW : null, paths: ag ? ag.awayN : 0 },
      estimate: ag ? ag.weighted : null,
      alignment: direction + (ag ? "; agreement " + (ag.agree * 100).toFixed(0) + "%" : ""),
      effectivePaths: ag ? ag.effective : null,
      context: "cross fixture · graph rows " + ev.rows,
      confidence: cl.label,
      goalRange: { low: null, exact2: null, high: null }
    });

  if (ag) {
    html += '<div class="balance-row"><span>unweighted estimate</span><b>' + ag.unweighted.toFixed(2) + "</b></div>" +
      '<div class="balance-row"><span>estimate spread</span><b>' + (ag.spread == null ? "?" : ag.spread.toFixed(2)) + "</b></div></div>";
  } else { html += "</div>"; }

  html += BlueprintEmbed.teamCard(hid, aid);

  if (paths.length) {
    html += '<div class="card"><h2>Evidence paths</h2>' +
      "<table><thead><tr><th>Phase</th><th>Path</th><th class='num'>Estimate</th><th class='num'>Weight</th></tr></thead><tbody>" +
      paths.map(function (p) {
        return "<tr><td>" + esc(p.phase) + "</td><td>" + esc(p.label) +
          (p.detail ? '<div class="help" style="margin:3px 0 0">' + esc(p.detail) + "</div>" : "") +
          '</td><td class="num">' + p.estimate.toFixed(2) + '</td><td class="num">' + p.weight.toFixed(2) + "</td></tr>";
      }).join("") + "</tbody></table>" +
      '<div class="help">Path count ' + paths.length + " · H2H " + (ag.phaseCounts.h2h || 0) +
      " · common " + (ag.phaseCounts.common || 0) + " · level-3 " + (ag.phaseCounts.third || 0) +
      " · effective independent " + ag.effective + " · reused chains " + ag.reusedChains + ".</div></div>";
  } else {
    html += '<div class="card"><h2>Evidence paths</h2><div class="help">No completed match rows connect these sides yet. ' +
      "Load team data (Data tab) covering H2H, common opponents, or level-3 bridge rows to open evidence.</div></div>";
  }

  html += saveCardHtml(confirmed, "saveEvidenceRating()", "Save this verdict");
  out.innerHTML = html;
}

function saveEvidenceRating() {
  if (!lastEvidence) return;
  if (!document.getElementById("confirmVenue").checked) return;
  const x = lastEvidence, ag = x.ag, cl = x.cl;
  const entry = {
    id: Date.now() + "-" + Math.random().toString(36).slice(2, 7),
    ts: Date.now(),
    date: document.getElementById("matchDate").value || null,
    type: "evidence",
    lg: "BP", lgName: (BlueprintEmbed.competition && BlueprintEmbed.competition()) || "Cross fixture",
    home: x.hp.name, away: x.ap.name,
    verdict: cl.label, reason: cl.reason,
    estimate: ag ? Number(ag.weighted.toFixed(4)) : null,
    unweighted: ag ? Number(ag.unweighted.toFixed(4)) : null,
    spread: ag && ag.spread != null ? Number(ag.spread.toFixed(4)) : null,
    paths: x.paths.length, effective: ag ? ag.effective : 0,
    agree: ag ? Number(ag.agree.toFixed(4)) : 0,
    homeW: ag ? ag.homeW : 0, neuW: ag ? ag.neuW : 0, awayW: ag ? ag.awayW : 0,
    venueConfirmed: true,
    result: null
  };
  logEntries.unshift(entry);
  if (saveLog()) {
    document.getElementById("saveMsg").textContent =
      "Saved as reference. It is not fed back into ratings — settle it with the actual score later.";
    updateCount();
  }
}

/* ---------- shared rating-card fragments -------------------------------- */
function ratingBarHtml(h, a, H, D, A) {
  return '<div class="bar">' +
    '<div class="bH" style="width:' + (H * 100) + '%">' + (H > 0.11 ? pct0(H) : "") + "</div>" +
    '<div class="bD" style="width:' + (D * 100) + '%">' + (D > 0.11 ? pct0(D) : "") + "</div>" +
    '<div class="bA" style="width:' + (A * 100) + '%">' + (A > 0.11 ? pct0(A) : "") + "</div>" +
    "</div>" +
    '<div class="barlabels"><span>' + esc(h) + " win</span><span>draw</span><span>" + esc(a) + " win</span></div>";
}

function ratingKvHtml(r) {
  return '<div class="kv" style="margin:12px 0 0">' +
    '<span class="k">Expected goals</span><span>' + r.lh.toFixed(2) + " &ndash; " + r.la.toFixed(2) + "</span>" +
    '<span class="k">Likeliest scoreline</span><span>' + r.expScore.home + "&ndash;" + r.expScore.away +
      " (" + pct(r.expScore.p) + " of the time)</span>" +
    (r.starsHome ? '<span class="k">Star rating</span><span>' + r.starsHome + "★ v " + r.starsAway +
       "★" + (r.starAdj ? " (draw adjusted)" : "") + "</span>" : "") +
    (r.consensus ? '<span class="k">Consensus (HvH / AvA)</span><span>' +
       r.consensus.consensus.toFixed(2) + "  (" + r.consensus.hvh.toFixed(2) + " / " +
       r.consensus.ava.toFixed(2) + ")</span>" : "") +
    '<span class="k">Historical rate for this tier</span><span>' + pct(r.tier.win) +
      " won &middot; " + pct(r.tier.draw) + " drew &middot; " + pct(r.tier.loss) + " lost</span>" +
    '<span class="k">Tier sample size</span><span>' + r.tier.n.toLocaleString() + " matches</span>" +
    "</div></div>";
}

function marketsHtml(r) {
  let html = '<div class="card"><h2>Markets</h2>' +
    '<div class="help">Calibration error shown per market. Both-teams-to-score is withheld &mdash; ' +
    "it missed by 6 points in testing and is not trustworthy yet.</div>" +
    "<table><thead><tr><th>Market</th><th class='num'>Probability</th><th class='num'>Fair odds</th>" +
    "<th>Confidence</th></tr></thead><tbody>";
  const m = r.markets;
  const mk = [
    ["Home win", r.H, "1X2", true],
    ["Draw", r.D, "1X2", true],
    ["Away win", r.A, "1X2", true],
    ["Home or draw (1X)", m.dc1x, "DC", true],
    ["Home win, draw no bet", m.dnb, "DNB", true],
    ["Over 1.5 goals", m.o15, "O15", true],
    ["Under 1.5 goals", m.u15, "O15", true],
    ["Over 2.5 goals", m.o25, "O25", true],
    ["Under 2.5 goals", m.u25, "O25", true],
    ["Over 3.5 goals", m.o35, "O35", false],
    ["Home &minus;1 handicap", m.hm1, "H-1", false],
  ];
  mk.forEach(function (row) {
    const err = MODEL.markets[row[2]];
    const cls = row[3] ? "mkt-ship" : "mkt-caution";
    const lbl = row[3] ? "±" + err.toFixed(1) + "pt" : "±" + err.toFixed(1) + "pt · caution";
    html += "<tr><td>" + row[0] + '</td><td class="num">' + pct(row[1]) +
      '</td><td class="num">' + (row[1] > 0.004 ? (1 / row[1]).toFixed(2) : "—") +
      '</td><td class="' + cls + '">' + lbl + "</td></tr>";
  });
  html += "</tbody></table></div>";
  return html;
}

function scorelinesHtml(r) {
  let html = '<div class="card"><h2>Most likely scorelines</h2>' +
    '<div class="help">Top pick is correct about 13% of the time &mdash; correct-score is inherently low-confidence.</div>' +
    '<div class="scores">';
  r.topScores.forEach(function (s) {
    html += '<div class="score"><b>' + esc(s.s) + "</b> &middot; " + pct(s.p) + "</div>";
  });
  html += "</div></div>";
  return html;
}

function saveCardHtml(confirmed, fn, label) {
  let html = '<div class="card"><h2>Save to log</h2>';
  if (!confirmed) {
    html += '<div class="banner ban-warn" style="margin:0 0 10px">Confirm the venue above before saving. ' +
      "A rating saved with the sides reversed is worse than no rating.</div>";
  }
  html += '<button class="btn" id="saveBtn" ' + (confirmed ? "" : "disabled") +
    ' onclick="' + fn + '">' + label + "</button>" +
    '<span id="saveMsg" class="help" style="margin-left:11px"></span></div>';
  return html;
}

''', tag="renderRate dispatch")

# ---------- 7. saveRating: cross-league name + flag ----------
rep("    lg: r.lg, lgName: MODEL.leagues[r.lg].name,",
    "    lg: r.lg, lgName: r.lgName || MODEL.leagues[r.lg].name,", tag="saveRating lgName")
rep("    confidence: r.confidence ? r.confidence.label : null,",
    "    confidence: r.confidence ? r.confidence.label : null,\n    cross: !!r.cross,", tag="saveRating cross flag")

# ---------- 8. renderLog: tolerate evidence entries; Brier only over probability rows ----------
block("function renderLog() {", "function toggleRow(id) {", r'''function renderLog() {
  updateCount();
  const q = (document.getElementById("fSearch").value || "").toLowerCase().trim();
  const ft = document.getElementById("fTier").value;
  const fr = document.getElementById("fRes").value;

  const shown = logEntries.filter(function (e) {
    if (ft && e.tier !== ft) return false;
    if (fr === "none" && e.result) return false;
    if (fr && fr !== "none" && e.result !== fr) return false;
    if (q && ((e.home || "") + " " + (e.away || "") + " " + (e.lgName || "")).toLowerCase().indexOf(q) === -1) return false;
    return true;
  });

  /* stats — a draw is a LOSS for a home-win rating, never a push.
     Brier is computed only over entries that carry probabilities;
     evidence verdicts are reference rows, not probability rows. */
  const settled = logEntries.filter(function (e) { return e.result; });
  const won = settled.filter(function (e) { return e.result === "correct"; }).length;
  const drew = settled.filter(function (e) { return e.result === "draw"; }).length;
  const lost = settled.filter(function (e) { return e.result === "incorrect"; }).length;
  let brier = null;
  const scored = settled.filter(function (e) {
    return typeof e.H === "number" && typeof e.D === "number" && typeof e.A === "number";
  });
  if (scored.length) {
    let s = 0;
    scored.forEach(function (e) {
      const yH = e.result === "correct" ? 1 : 0;
      const yD = e.result === "draw" ? 1 : 0;
      const yA = e.result === "incorrect" ? 1 : 0;
      s += Math.pow(e.H - yH, 2) + Math.pow(e.D - yD, 2) + Math.pow(e.A - yA, 2);
    });
    brier = s / scored.length;
  }
  document.getElementById("logStats").innerHTML =
    "<div><b>" + logEntries.length + "</b>saved</div>" +
    "<div><b>" + settled.length + "</b>settled</div>" +
    "<div><b>" + won + "</b>home won</div>" +
    "<div><b>" + drew + "</b>drew</div>" +
    "<div><b>" + lost + "</b>home lost</div>" +
    (settled.length ? "<div><b>" + ((won / settled.length) * 100).toFixed(1) +
      "%</b>home-win rate</div>" : "") +
    (brier !== null ? "<div><b>" + brier.toFixed(4) + "</b>Brier score</div>" : "");

  /* tier filter options */
  const fT = document.getElementById("fTier");
  if (fT.options.length <= 1) {
    MODEL.tiers.forEach(function (t) {
      const o = document.createElement("option");
      o.value = t[0]; o.textContent = t[0];
      fT.appendChild(o);
    });
  }

  const list = document.getElementById("logList");
  if (!logEntries.length) {
    list.innerHTML = '<div class="card"><div class="help" style="margin:0">' +
      "Nothing saved yet. Rate a match and save it here.</div></div>";
    return;
  }
  if (!shown.length) {
    list.innerHTML = '<div class="card"><div class="help" style="margin:0">No entries match those filters.</div></div>';
    return;
  }

  list.innerHTML = shown.map(function (e) {
    const rp = e.result
      ? '<span class="res-pill ' + (e.result === "correct" ? "r-correct" :
          e.result === "draw" ? "r-draw" : "r-incorrect") + '">' +
        (e.result === "correct" ? "home won" : e.result === "draw" ? "drew" : "home lost") + "</span>"
      : "";
    const headBadge = e.type === "evidence"
      ? '<span class="badge b-blue">' + (e.estimate != null ? (e.estimate >= 0 ? "+" : "") + Number(e.estimate).toFixed(2) : "EV") + "</span>"
      : '<span class="badge ' + tierBadge(e.tier) + '">' + e.points + "</span>";
    const bodyKv = e.type === "evidence"
      ? '<span class="k">Verdict</span><span>' + esc(e.verdict || "—") + "</span>" +
        (e.reason ? '<span class="k">Basis</span><span>' + esc(e.reason) + "</span>" : "") +
        (e.estimate != null ? '<span class="k">Aggregate estimate</span><span>' + Number(e.estimate).toFixed(2) + " (unweighted " + Number(e.unweighted).toFixed(2) + ")</span>" : "") +
        '<span class="k">Evidence</span><span>' + (e.paths || 0) + " paths · " + (e.effective || 0) +
          " independent · agreement " + (((e.agree || 0) * 100).toFixed(0)) + "%</span>" +
        '<span class="k">Balance (H/N/A weight)</span><span>' + Number(e.homeW).toFixed(1) + " / " +
          Number(e.neuW).toFixed(1) + " / " + Number(e.awayW).toFixed(1) + "</span>" +
        '<span class="k">Reference only</span><span>not fed back into ratings</span>'
      : '<span class="k">Predicted</span><span>' + pct(e.H) + " / " + pct(e.D) + " / " + pct(e.A) + "</span>" +
        '<span class="k">Expected goals</span><span>' + e.lh.toFixed(2) + " &ndash; " + e.la.toFixed(2) + "</span>" +
        '<span class="k">Tier</span><span>' + esc(e.tier) + (e.cross ? " · cross-league" : "") + "</span>" +
        '<span class="k">Over 2.5</span><span>' + pct(e.o25) + "</span>" +
        '<span class="k">Likeliest score</span><span>' + esc(e.topScore) + "</span>" +
        '<span class="k">Venue confirmed</span><span>yes</span>' +
        (e.stars ? '<span class="k">Stars</span><span>' + esc(e.stars) + "</span>" : "") +
        (e.confidence ? '<span class="k">Confidence</span><span>' + esc(e.confidence) +
          (e.consensus !== null && e.consensus !== undefined ? " (" + e.consensus + ")" : "") + "</span>" : "");
    return '<div class="logrow" id="row-' + e.id + '">' +
      '<div class="loghead" onclick="toggleRow(\'' + e.id + '\')">' +
        '<div class="logmain">' +
          '<div class="logtitle">' + esc(e.home) + " v " + esc(e.away) + "</div>" +
          '<div class="logsub">' + esc(e.lgName) + (e.date ? " &middot; " + esc(e.date) : "") + "</div>" +
        "</div>" + rp + headBadge +
      "</div>" +
      '<div class="logbody">' +
        '<div class="kv" style="margin:11px 0">' + bodyKv + "</div>" +
        '<div class="help" style="margin-bottom:6px">Settle this ' +
          (e.type === "evidence" ? "verdict" : "rating") +
          " &mdash; a draw counts as a loss for a home-win call.</div>" +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'correct\')">Home won</button> ' +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'draw\')">Drew</button> ' +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'incorrect\')">Home lost</button> ' +
        (e.result ? '<button class="btnlink" onclick="settle(\'' + e.id + '\',null)">Clear</button>' : "") +
        '<div style="margin-top:9px"><button class="btnred" onclick="delEntry(\'' + e.id + '\')">Delete</button></div>' +
      "</div></div>";
  }).join("");
}

''', tag="renderLog")

# ---------- 9. expose audit append hook path (no-op guard already in renderRate) ----------

open(DST, "w", encoding="utf-8").write(s)
print("\nPART A complete:", edits, "edits applied, %d bytes -> %s" % (len(s), DST))
