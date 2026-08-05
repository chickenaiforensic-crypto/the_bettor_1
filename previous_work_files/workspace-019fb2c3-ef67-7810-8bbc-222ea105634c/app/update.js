/* ==========================================================================
   RATING UPDATE ENGINE
   Applies the exact same online learning step the Python trainer uses, in the
   browser, from results you paste in. Mathematically identical to a rebuild.
   No network call — CORS blocks direct fetching from data sites.
   ========================================================================== */

const LR = 0.055;        // learning rate  (must match rating.py)
const DECAY = 0.0022;    // per-match shrink toward mean
const HFA_LR = 0.010;    // home-advantage learning rate

/* live overlay applied on top of the shipped MODEL */
let OVERLAY = { teams: {}, leagues: {}, seen: {}, applied: [], lastUpdate: null };

function loadOverlay() {
  try {
    const raw = localStorage.getItem("pitchRating:overlay:v1");
    if (raw) {
      const o = JSON.parse(raw);
      if (o && o.teams) OVERLAY = o;
    }
  } catch (e) { /* keep default */ }
  applyOverlay();
}
function saveOverlay() {
  try {
    localStorage.setItem("pitchRating:overlay:v1", JSON.stringify(OVERLAY));
    return true;
  } catch (e) { return false; }
}

/* rebuild MODEL.teams / MODEL.leagues from base + overlay */
let BASE_TEAMS = null, BASE_LEAGUES = null;
function snapshotBase() {
  if (BASE_TEAMS) return;
  BASE_TEAMS = JSON.parse(JSON.stringify(MODEL.teams));
  BASE_LEAGUES = JSON.parse(JSON.stringify(MODEL.leagues));
}
function applyOverlay() {
  snapshotBase();
  MODEL.teams = JSON.parse(JSON.stringify(BASE_TEAMS));
  MODEL.leagues = JSON.parse(JSON.stringify(BASE_LEAGUES));
  for (const lg in OVERLAY.teams) {
    for (const t in OVERLAY.teams[lg]) {
      if (!MODEL.teams[lg]) MODEL.teams[lg] = {};
      MODEL.teams[lg][t] = OVERLAY.teams[lg][t].slice();
    }
  }
  for (const lg in OVERLAY.leagues) {
    if (MODEL.leagues[lg]) {
      MODEL.leagues[lg].mu = OVERLAY.leagues[lg].mu;
      MODEL.leagues[lg].hfa = OVERLAY.leagues[lg].hfa;
    }
  }
}

/* apply one result — identical maths to the Python trainer */
function applyResult(lg, home, away, hg, ag) {
  if (!MODEL.teams[lg] || !MODEL.teams[lg][home] || !MODEL.teams[lg][away]) {
    return { ok: false, reason: "team not in rated set" };
  }
  const L = MODEL.leagues[lg];
  const H = MODEL.teams[lg][home], A = MODEL.teams[lg][away];

  let lh = Math.exp(L.mu + H[0] - A[1] + L.hfa + H[2]);
  let la = Math.exp(L.mu + A[0] - H[1]);
  lh = Math.max(0.05, Math.min(6, lh));
  la = Math.max(0.05, Math.min(6, la));

  const eh = hg - lh, ea = ag - la;
  const seenH = OVERLAY.seen[lg + "|" + home] || 99;
  const seenA = OVERLAY.seen[lg + "|" + away] || 99;
  const kh = LR * (seenH < 8 ? 1.6 : 1.0);
  const ka = LR * (seenA < 8 ? 1.6 : 1.0);

  H[0] += kh * eh * 0.5;  A[1] -= ka * eh * 0.5;
  A[0] += ka * ea * 0.5;  H[1] -= kh * ea * 0.5;
  L.hfa += HFA_LR * (eh - ea) * 0.02;
  H[2] += HFA_LR * (eh - ea) * 0.010;
  H[2] *= 0.999;
  L.mu += 0.004 * ((eh + ea) / 2);

  H[0] *= (1 - DECAY); H[1] *= (1 - DECAY);
  A[0] *= (1 - DECAY); A[1] *= (1 - DECAY);
  L.hfa = Math.max(0.05, Math.min(0.55, L.hfa));
  H[2] = Math.max(-0.25, Math.min(0.25, H[2]));

  /* persist into overlay */
  if (!OVERLAY.teams[lg]) OVERLAY.teams[lg] = {};
  OVERLAY.teams[lg][home] = H.slice();
  OVERLAY.teams[lg][away] = A.slice();
  OVERLAY.leagues[lg] = { mu: L.mu, hfa: L.hfa };
  OVERLAY.seen[lg + "|" + home] = (OVERLAY.seen[lg + "|" + home] || 99) + 1;
  OVERLAY.seen[lg + "|" + away] = (OVERLAY.seen[lg + "|" + away] || 99) + 1;

  return { ok: true, lh: lh, la: la };
}

/* ---- parse pasted results ------------------------------------------------
   Accepts, one per line:
     Arsenal 2-1 Chelsea
     Arsenal 2 - 1 Chelsea
     Arsenal,2,1,Chelsea
     2026-08-15 Arsenal 2-1 Chelsea
   -------------------------------------------------------------------------- */
function parseResults(text, lg) {
  const out = [], bad = [];
  const known = Object.keys(MODEL.teams[lg] || {});
  const lower = {};
  known.forEach(function (t) { lower[t.toLowerCase()] = t; });

  function matchTeam(s) {
    s = s.trim().replace(/\s+/g, " ");
    if (!s) return null;
    if (lower[s.toLowerCase()]) return lower[s.toLowerCase()];
    const ls = s.toLowerCase();
    let best = null, bestLen = 0;
    for (const k in lower) {
      if ((k.indexOf(ls) === 0 || ls.indexOf(k) === 0) && k.length > bestLen) {
        best = lower[k]; bestLen = k.length;
      }
    }
    return best;
  }

  text.split("\n").forEach(function (raw) {
    let line = raw.trim();
    if (!line) return;
    line = line.replace(/^\d{4}-\d{2}-\d{2}\s+/, "");        // strip leading date
    line = line.replace(/^\d{1,2}\/\d{1,2}\/\d{2,4}\s+/, "");

    let m = line.match(/^(.+?)[,\t]\s*(\d+)[,\t]\s*(\d+)[,\t]\s*(.+)$/);   // CSV
    if (!m) m = line.match(/^(.+?)\s+(\d+)\s*[-:–]\s*(\d+)\s+(.+)$/);      // A 2-1 B
    if (!m) { bad.push(raw.trim()); return; }

    const h = matchTeam(m[1]), a = matchTeam(m[4]);
    const hg = parseInt(m[2], 10), ag = parseInt(m[3], 10);
    if (!h || !a || h === a || isNaN(hg) || isNaN(ag) || hg > 20 || ag > 20) {
      bad.push(raw.trim() + (h && a ? "" : "  (team not recognised)"));
      return;
    }
    out.push({ home: h, away: a, hg: hg, ag: ag });
  });
  return { games: out, bad: bad };
}

/* ---- UI plumbing --------------------------------------------------------- */
function initUpdateTab() {
  const sel = document.getElementById("uLeague");
  const keys = Object.keys(BASE_LEAGUES).sort(function (a, b) {
    return BASE_LEAGUES[a].name.localeCompare(BASE_LEAGUES[b].name);
  });
  sel.innerHTML = keys.map(function (k) {
    return '<option value="' + esc(k) + '">' + esc(BASE_LEAGUES[k].name) + "</option>";
  }).join("");
  sel.value = "E0";
  renderUpdateStatus();
}

function renderUpdateStatus() {
  const el = document.getElementById("updStatus");
  const n = OVERLAY.applied.length;
  const built = MODEL.built;
  let msg = "<b>Shipped ratings:</b> built " + esc(built) +
    " from 153,058 matches.<br><b>Results applied since:</b> " + n;
  if (OVERLAY.lastUpdate) msg += " (last " + esc(OVERLAY.lastUpdate) + ")";
  const age = Math.round((Date.now() - Date.parse(built)) / 86400000);
  let cls = "ban-ok";
  if (age > 120) cls = "ban-err"; else if (age > 45) cls = "ban-warn";
  msg += "<br><b>Base age:</b> " + age + " days.";
  if (age > 120) msg += " Ratings are stale — rebuild from source or apply recent results.";
  else if (age > 45) msg += " Getting old — worth topping up with recent results.";
  else msg += " Fresh.";
  el.className = "banner " + cls;
  el.innerHTML = msg;
}

function previewUpdate() {
  const lg = document.getElementById("uLeague").value;
  const txt = document.getElementById("uText").value;
  const r = parseResults(txt, lg);
  const el = document.getElementById("uPreview");
  if (!r.games.length && !r.bad.length) { el.innerHTML = ""; return; }
  let h = "";
  if (r.games.length) {
    h += '<div class="help" style="margin:10px 0 4px"><b>' + r.games.length +
      " result(s) recognised:</b></div><table><thead><tr><th>Home</th><th class='num'>Score</th>" +
      "<th>Away</th><th class='num'>Rating shift</th></tr></thead><tbody>";
    r.games.forEach(function (g) {
      const before = rateFixture(lg, g.home, g.away);
      h += "<tr><td>" + esc(g.home) + "</td><td class='num'>" + g.hg + "&ndash;" + g.ag +
        "</td><td>" + esc(g.away) + "</td><td class='num'>" +
        (before.error ? "&mdash;" : before.points + " pts now") + "</td></tr>";
    });
    h += "</tbody></table>";
  }
  if (r.bad.length) {
    h += '<div class="banner ban-warn" style="margin-top:10px"><b>Not recognised (' +
      r.bad.length + "):</b><br>" + r.bad.slice(0, 8).map(esc).join("<br>") +
      (r.bad.length > 8 ? "<br>&hellip;" : "") + "</div>";
  }
  el.innerHTML = h;
}

function commitUpdate() {
  const lg = document.getElementById("uLeague").value;
  const txt = document.getElementById("uText").value;
  const r = parseResults(txt, lg);
  if (!r.games.length) { document.getElementById("uMsg").textContent = "Nothing to apply."; return; }
  let applied = 0;
  r.games.forEach(function (g) {
    const res = applyResult(lg, g.home, g.away, g.hg, g.ag);
    if (res.ok) {
      applied++;
      OVERLAY.applied.push(lg + "|" + g.home + "|" + g.away + "|" + g.hg + "-" + g.ag);
    }
  });
  OVERLAY.lastUpdate = new Date().toISOString().slice(0, 10);
  saveOverlay();
  document.getElementById("uMsg").textContent =
    "Applied " + applied + " result(s). Ratings updated.";
  document.getElementById("uText").value = "";
  document.getElementById("uPreview").innerHTML = "";
  renderUpdateStatus();
  onLeagueChange();
}

function resetOverlay() {
  if (!confirm("Discard all applied results and return to the shipped ratings?")) return;
  OVERLAY = { teams: {}, leagues: {}, seen: {}, applied: [], lastUpdate: null };
  saveOverlay();
  applyOverlay();
  renderUpdateStatus();
  onLeagueChange();
  document.getElementById("uMsg").textContent = "Reset to shipped ratings.";
}

function exportRatings() {
  const data = {
    version: MODEL.version, base_built: MODEL.built,
    exported: new Date().toISOString(),
    results_applied: OVERLAY.applied.length,
    teams: MODEL.teams, leagues: MODEL.leagues
  };
  const b = new Blob([JSON.stringify(data, null, 1)], { type: "application/json" });
  const u = URL.createObjectURL(b);
  const a = document.createElement("a");
  a.href = u; a.download = "pitch-ratings-current.json"; a.click();
  setTimeout(function () { URL.revokeObjectURL(u); }, 2000);
}

function importRatings(ev) {
  const f = ev.target.files && ev.target.files[0];
  if (!f) return;
  const rd = new FileReader();
  rd.onload = function () {
    try {
      const d = JSON.parse(rd.result);
      if (!d.teams || !d.leagues) throw new Error("not a ratings file");
      OVERLAY.teams = {}; OVERLAY.leagues = {};
      for (const lg in d.teams) OVERLAY.teams[lg] = d.teams[lg];
      for (const lg in d.leagues) {
        OVERLAY.leagues[lg] = { mu: d.leagues[lg].mu, hfa: d.leagues[lg].hfa };
      }
      OVERLAY.applied = new Array(d.results_applied || 0).fill("imported");
      OVERLAY.lastUpdate = (d.exported || "").slice(0, 10);
      saveOverlay(); applyOverlay(); renderUpdateStatus(); onLeagueChange();
      document.getElementById("uMsg").textContent =
        "Imported ratings (base " + esc(d.base_built || "?") + ").";
    } catch (e) {
      document.getElementById("uMsg").textContent = "Could not read that file: " + e.message;
    }
    ev.target.value = "";
  };
  rd.readAsText(f);
}
