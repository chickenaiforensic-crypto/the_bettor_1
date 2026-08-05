/* ==========================================================================
   Pitch Rating — UI + log. Football only. No network calls, no odds.
   ========================================================================== */

const LS_KEY = "pitchRating:log:v1";
let logEntries = [];
let currentView = "rate";
let lastRating = null;

/* ---------- storage ------------------------------------------------------ */
function loadLog() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    logEntries = raw ? JSON.parse(raw) : [];
    if (!Array.isArray(logEntries)) logEntries = [];
  } catch (e) { logEntries = []; }
}
function saveLog() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(logEntries));
    return true;
  } catch (e) {
    note("Could not save to this browser's storage. Export to a file to keep your log.");
    return false;
  }
}
function note(msg) {
  const el = document.getElementById("logNote");
  if (el) el.textContent = msg || "";
}

/* ---------- escaping (never inject raw names into HTML) ------------------ */
function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

/* ---------- views -------------------------------------------------------- */
function showView(v) {
  currentView = v;
  document.getElementById("viewRate").className = v === "rate" ? "" : "hidden";
  document.getElementById("viewLog").className = v === "log" ? "" : "hidden";
  document.getElementById("viewAbout").className = v === "about" ? "" : "hidden";
  document.getElementById("tabRate").className = "tab" + (v === "rate" ? " active" : "");
  document.getElementById("tabLog").className = "tab" + (v === "log" ? " active" : "");
  document.getElementById("tabAbout").className = "tab" + (v === "about" ? " active" : "");
  if (v === "log") renderLog();
}

/* ---------- setup -------------------------------------------------------- */
function initLeagues() {
  const sel = document.getElementById("league");
  const keys = Object.keys(MODEL.leagues).sort(function (a, b) {
    return MODEL.leagues[a].name.localeCompare(MODEL.leagues[b].name);
  });
  sel.innerHTML = keys.map(function (k) {
    return '<option value="' + esc(k) + '">' + esc(MODEL.leagues[k].name) + "</option>";
  }).join("");
  sel.value = "E0";
  onLeagueChange();
}

function onLeagueChange() {
  const lg = document.getElementById("league").value;
  const teams = Object.keys(MODEL.teams[lg] || {}).sort();
  const opts = '<option value="">&mdash; select &mdash;</option>' +
    teams.map(function (t) { return '<option value="' + esc(t) + '">' + esc(t) + "</option>"; }).join("");
  document.getElementById("homeTeam").innerHTML = opts;
  document.getElementById("awayTeam").innerHTML = opts;
  onTeamChange();
}

function onTeamChange() {
  document.getElementById("confirmVenue").checked = false;
  const h = document.getElementById("homeTeam").value;
  document.getElementById("confirmHome").textContent = h || "\u2014";
  renderRate();
}

function swapSides() {
  const h = document.getElementById("homeTeam");
  const a = document.getElementById("awayTeam");
  const t = h.value; h.value = a.value; a.value = t;
  onTeamChange();
}

/* ---------- main render -------------------------------------------------- */
function renderRate() {
  const lg = document.getElementById("league").value;
  const h = document.getElementById("homeTeam").value;
  const a = document.getElementById("awayTeam").value;
  const flipBox = document.getElementById("flipBox");
  const out = document.getElementById("result");
  document.getElementById("confirmHome").textContent = h || "\u2014";

  flipBox.innerHTML = "";
  out.innerHTML = "";
  lastRating = null;

  if (!h || !a) {
    out.innerHTML = '<div class="banner ban-info">Select both teams to produce a rating.</div>';
    return;
  }
  if (h === a) {
    out.innerHTML = '<div class="banner ban-err">A team cannot play itself.</div>';
    return;
  }

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
    '<div class="help" style="margin-bottom:9px">' + esc(MODEL.leagues[lg].name) + "</div>" +
    '<div class="pts">' + r.points + "</div>" +
    '<div class="ptslabel">home rating</div>' +
    '<div style="margin-top:9px"><span class="badge ' + badge + '">' + esc(r.tier.name) + "</span></div>" +
    "</div>";

  html += '<div class="bar">' +
    '<div class="bH" style="width:' + (r.H * 100) + '%">' + (r.H > 0.11 ? pct0(r.H) : "") + "</div>" +
    '<div class="bD" style="width:' + (r.D * 100) + '%">' + (r.D > 0.11 ? pct0(r.D) : "") + "</div>" +
    '<div class="bA" style="width:' + (r.A * 100) + '%">' + (r.A > 0.11 ? pct0(r.A) : "") + "</div>" +
    "</div>" +
    '<div class="barlabels"><span>' + esc(h) + " win</span><span>draw</span><span>" +
    esc(a) + " win</span></div>";

  html += '<div class="kv" style="margin-top:12px">' +
    '<span class="k">Expected goals</span><span>' + r.lh.toFixed(2) + " &ndash; " + r.la.toFixed(2) + "</span>" +
    '<span class="k">Historical rate for this tier</span><span>' + pct(r.tier.win) +
      " won &middot; " + pct(r.tier.draw) + " drew &middot; " + pct(r.tier.loss) + " lost</span>" +
    '<span class="k">Tier sample size</span><span>' + r.tier.n.toLocaleString() + " matches</span>" +
    "</div></div>";

  /* markets */
  html += '<div class="card"><h2>Markets</h2>' +
    '<div class="help">Calibration error shown per market. Both-teams-to-score is withheld &mdash; ' +
    'it missed by 6 points in testing and is not trustworthy yet.</div>' +
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
    const lbl = row[3] ? "\u00b1" + err.toFixed(1) + "pt" : "\u00b1" + err.toFixed(1) + "pt \u00b7 caution";
    html += "<tr><td>" + row[0] + '</td><td class="num">' + pct(row[1]) +
      '</td><td class="num">' + (row[1] > 0.004 ? (1 / row[1]).toFixed(2) : "\u2014") +
      '</td><td class="' + cls + '">' + lbl + "</td></tr>";
  });
  html += "</tbody></table></div>";

  /* scorelines */
  html += '<div class="card"><h2>Most likely scorelines</h2>' +
    '<div class="help">Top pick is correct about 13% of the time &mdash; correct-score is inherently low-confidence.</div>' +
    '<div class="scores">';
  r.topScores.forEach(function (s) {
    html += '<div class="score"><b>' + esc(s.s) + "</b> &middot; " + pct(s.p) + "</div>";
  });
  html += "</div></div>";

  /* save */
  html += '<div class="card"><h2>Save to log</h2>';
  if (!confirmed) {
    html += '<div class="banner ban-warn" style="margin:0 0 10px">Confirm the venue above before saving. ' +
      "A rating saved with the sides reversed is worse than no rating.</div>";
  }
  html += '<button class="btn" id="saveBtn" ' + (confirmed ? "" : "disabled") +
    ' onclick="saveRating()">Save this rating</button>' +
    '<span id="saveMsg" class="help" style="margin-left:11px"></span></div>';

  out.innerHTML = html;
}

function tierBadge(name) {
  if (name.indexOf("A+") === 0) return "b-green";
  if (name.indexOf("A ") === 0) return "b-teal";
  if (name.indexOf("B ") === 0) return "b-blue";
  if (name.indexOf("C ") === 0) return "b-amber";
  if (name.indexOf("D ") === 0) return "b-gray";
  return "b-red";
}

/* ---------- saving ------------------------------------------------------- */
function saveRating() {
  if (!lastRating) return;
  if (!document.getElementById("confirmVenue").checked) return;
  const r = lastRating;
  const entry = {
    id: Date.now() + "-" + Math.random().toString(36).slice(2, 7),
    ts: Date.now(),
    date: document.getElementById("matchDate").value || null,
    lg: r.lg, lgName: MODEL.leagues[r.lg].name,
    home: r.homeTeam, away: r.awayTeam,
    points: r.points, tier: r.tier.name,
    H: r.H, D: r.D, A: r.A, lh: r.lh, la: r.la,
    o25: r.markets.o25, dnb: r.markets.dnb,
    topScore: r.topScores[0].s,
    venueConfirmed: true,
    result: null
  };
  logEntries.unshift(entry);
  if (saveLog()) {
    document.getElementById("saveMsg").textContent = "Saved.";
    updateCount();
  }
}

function updateCount() {
  document.getElementById("logCount").textContent = logEntries.length;
}

/* ---------- log rendering ------------------------------------------------ */
function renderLog() {
  updateCount();
  const q = (document.getElementById("fSearch").value || "").toLowerCase().trim();
  const ft = document.getElementById("fTier").value;
  const fr = document.getElementById("fRes").value;

  const shown = logEntries.filter(function (e) {
    if (ft && e.tier !== ft) return false;
    if (fr === "none" && e.result) return false;
    if (fr && fr !== "none" && e.result !== fr) return false;
    if (q && (e.home + " " + e.away + " " + e.lgName).toLowerCase().indexOf(q) === -1) return false;
    return true;
  });

  /* stats — a draw is a LOSS for a home-win rating, never a push */
  const settled = logEntries.filter(function (e) { return e.result; });
  const won = settled.filter(function (e) { return e.result === "correct"; }).length;
  const drew = settled.filter(function (e) { return e.result === "draw"; }).length;
  const lost = settled.filter(function (e) { return e.result === "incorrect"; }).length;
  let brier = null;
  if (settled.length) {
    let s = 0;
    settled.forEach(function (e) {
      const yH = e.result === "correct" ? 1 : 0;
      const yD = e.result === "draw" ? 1 : 0;
      const yA = e.result === "incorrect" ? 1 : 0;
      s += Math.pow(e.H - yH, 2) + Math.pow(e.D - yD, 2) + Math.pow(e.A - yA, 2);
    });
    brier = s / settled.length;
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
    return '<div class="logrow" id="row-' + e.id + '">' +
      '<div class="loghead" onclick="toggleRow(\'' + e.id + '\')">' +
        '<div class="logmain">' +
          '<div class="logtitle">' + esc(e.home) + " v " + esc(e.away) + "</div>" +
          '<div class="logsub">' + esc(e.lgName) + (e.date ? " &middot; " + esc(e.date) : "") + "</div>" +
        "</div>" + rp +
        '<span class="badge ' + tierBadge(e.tier) + '">' + e.points + "</span>" +
      "</div>" +
      '<div class="logbody">' +
        '<div class="kv" style="margin:11px 0">' +
          '<span class="k">Predicted</span><span>' + pct(e.H) + " / " + pct(e.D) + " / " + pct(e.A) + "</span>" +
          '<span class="k">Expected goals</span><span>' + e.lh.toFixed(2) + " &ndash; " + e.la.toFixed(2) + "</span>" +
          '<span class="k">Tier</span><span>' + esc(e.tier) + "</span>" +
          '<span class="k">Over 2.5</span><span>' + pct(e.o25) + "</span>" +
          '<span class="k">Likeliest score</span><span>' + esc(e.topScore) + "</span>" +
          '<span class="k">Venue confirmed</span><span>yes</span>' +
        "</div>" +
        '<div class="help" style="margin-bottom:6px">Settle this rating &mdash; a draw counts as a loss for a home-win call.</div>' +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'correct\')">Home won</button> ' +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'draw\')">Drew</button> ' +
        '<button class="btn2" onclick="settle(\'' + e.id + '\',\'incorrect\')">Home lost</button> ' +
        (e.result ? '<button class="btnlink" onclick="settle(\'' + e.id + '\',null)">Clear</button>' : "") +
        '<div style="margin-top:9px"><button class="btnred" onclick="delEntry(\'' + e.id + '\')">Delete</button></div>' +
      "</div></div>";
  }).join("");
}

function toggleRow(id) {
  const el = document.getElementById("row-" + id);
  if (el) el.className = el.className.indexOf("open") === -1 ? "logrow open" : "logrow";
}
function settle(id, res) {
  const e = logEntries.find(function (x) { return x.id === id; });
  if (!e) return;
  e.result = res;
  saveLog();
  renderLog();
  const el = document.getElementById("row-" + id);
  if (el) el.className = "logrow open";
}
function delEntry(id) {
  logEntries = logEntries.filter(function (x) { return x.id !== id; });
  saveLog(); renderLog();
}
function clearLog() {
  if (!logEntries.length) return;
  if (!confirm("Delete all " + logEntries.length + " saved ratings? This cannot be undone.")) return;
  logEntries = []; saveLog(); renderLog();
  note("Log cleared.");
}

/* ---------- export / import --------------------------------------------- */
function exportLog() {
  const blob = new Blob([JSON.stringify({
    app: "pitch-rating", version: 1, exported: new Date().toISOString(), entries: logEntries
  }, null, 1)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "pitch-rating-log-" + new Date().toISOString().slice(0, 10) + ".json";
  a.click();
  setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  note("Exported " + logEntries.length + " entries.");
}

function importLog(ev) {
  const f = ev.target.files && ev.target.files[0];
  if (!f) return;
  const rd = new FileReader();
  rd.onload = function () {
    try {
      const d = JSON.parse(rd.result);
      const inc = Array.isArray(d) ? d : (d.entries || []);
      let added = 0;
      inc.forEach(function (e) {
        if (!e || !e.id) return;
        if (logEntries.some(function (x) { return x.id === e.id; })) return;
        logEntries.push(e); added++;
      });
      logEntries.sort(function (a, b) { return b.ts - a.ts; });
      saveLog(); renderLog();
      note("Imported " + added + " new entries (" + (inc.length - added) + " already present).");
    } catch (err) {
      note("Could not read that file: " + err.message);
    }
    ev.target.value = "";
  };
  rd.readAsText(f);
}

/* ---------- about tables ------------------------------------------------- */
function initAbout() {
  document.getElementById("aboutTiers").innerHTML = MODEL.tiers.map(function (t) {
    return "<tr><td><span class='badge " + tierBadge(t[0]) + "'>" + esc(t[0]) + "</span></td>" +
      "<td class='num'>" + Math.round(t[1] * 100) + "+</td>" +
      "<td class='num'>" + pct(t[2]) + "</td><td class='num'>" + pct(t[3]) + "</td>" +
      "<td class='num'>" + pct(t[4]) + "</td><td class='num'>" + t[5].toLocaleString() + "</td></tr>";
  }).join("");

  const labels = { "1X2": "Home / draw / away", DC: "Double chance", DNB: "Draw no bet",
    O15: "Over / under 1.5", O25: "Over / under 2.5", O35: "Over / under 3.5",
    "H-1": "Home \u22121 handicap", BTTS: "Both teams to score" };
  document.getElementById("aboutMarkets").innerHTML = Object.keys(MODEL.markets).map(function (k) {
    const v = MODEL.markets[k];
    const st = MODEL.ship.indexOf(k) !== -1 ? "<span class='mkt-ship'>shown</span>"
      : MODEL.caution.indexOf(k) !== -1 ? "<span class='mkt-caution'>shown with caution</span>"
      : "<span style='color:#b91c1c;font-weight:600'>withheld</span>";
    return "<tr><td>" + (labels[k] || k) + "</td><td class='num'>\u00b1" + v.toFixed(1) + "pt</td><td>" + st + "</td></tr>";
  }).join("");

  const hfa = Object.keys(MODEL.leagues).map(function (k) {
    return { n: MODEL.leagues[k].name, m: Math.exp(MODEL.leagues[k].hfa) };
  }).sort(function (a, b) { return b.m - a.m; });
  document.getElementById("aboutHfa").innerHTML = hfa.map(function (x) {
    return "<tr><td>" + esc(x.n) + "</td><td class='num'>" + x.m.toFixed(2) + "\u00d7</td></tr>";
  }).join("");
}

/* ---------- boot --------------------------------------------------------- */
loadLog();
initLeagues();
initAbout();
updateCount();
renderRate();
