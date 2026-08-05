/* ==========================================================================
   SYNC BRIEF — export full app state as an AI-readable brief, then ingest
   the reply in a strict, validated format. Nothing is trusted blindly.
   ========================================================================== */

const SYNC_VER = "PITCH-SYNC v1";

/* ---- state helpers ------------------------------------------------------- */
function leagueThrough(lg) {
  if (OVERLAY.through && OVERLAY.through[lg]) return OVERLAY.through[lg];
  return MODEL.built;                      /* nothing applied yet -> base build date */
}
function todayISO() {
  const d = new Date();
  return d.getFullYear() + "-" +
    String(d.getMonth() + 1).padStart(2, "0") + "-" +
    String(d.getDate()).padStart(2, "0");
}
function appliedCount(lg) {
  if (!OVERLAY.counts) return 0;
  return OVERLAY.counts[lg] || 0;
}

/* ---- BRIEF GENERATION ---------------------------------------------------- */
function buildSyncBrief(scope) {
  const today = todayISO();
  const codes = scope === "all"
    ? Object.keys(BASE_LEAGUES).sort()
    : [document.getElementById("uLeague").value];

  const L = [];
  L.push("You are updating a football rating model. Fetch real match results and return them");
  L.push("in the exact block format specified at the bottom. Accuracy matters more than volume.");
  L.push("");
  L.push("=== APP STATE ===");
  L.push("Model:            " + MODEL.version);
  L.push("Base built:       " + MODEL.built + "  (from 153,058 matches, 18 leagues, 2003-2026)");
  L.push("Today:            " + today);
  L.push("Results applied:  " + (OVERLAY.applied ? OVERLAY.applied.length : 0) + " since base build");
  L.push("Saved ratings:    " + (typeof logEntries !== "undefined" ? logEntries.length : 0));
  L.push("");
  L.push("=== WHAT I NEED ===");
  L.push("For each league below, every COMPLETED league match played AFTER the 'through' date");
  L.push("and on or before " + today + ". League matches only:");
  L.push("  - EXCLUDE cups, playoffs, friendlies, and any European competition");
  L.push("  - EXCLUDE fixtures not yet played or abandoned");
  L.push("  - If a league is out of season with no new matches, return its block with no rows");
  L.push("");
  L.push("League".padEnd(30) + "code".padEnd(6) + "results through".padEnd(18) + "already applied");
  L.push("-".repeat(72));
  codes.forEach(function (c) {
    const nm = BASE_LEAGUES[c] ? BASE_LEAGUES[c].name : c;
    L.push(nm.padEnd(30) + c.padEnd(6) + leagueThrough(c).padEnd(18) + appliedCount(c));
  });
  L.push("");
  L.push("=== TEAM NAMES — USE THESE EXACT SPELLINGS ===");
  L.push("Any name not on this list is rejected by the parser. If a promoted/unknown club");
  L.push("appears, omit that match and note it in a # comment line.");
  codes.forEach(function (c) {
    const teams = Object.keys(MODEL.teams[c] || {}).sort();
    L.push("");
    L.push("[" + c + "] " + (BASE_LEAGUES[c] ? BASE_LEAGUES[c].name : c) + " (" + teams.length + " rated)");
    L.push("  " + teams.join(" | "));
  });
  L.push("");
  L.push("=== OUTPUT FORMAT — RETURN ONLY THIS, NOTHING ELSE ===");
  L.push("One block per league. Column order is fixed and must not be altered:");
  L.push("");
  L.push("  " + SYNC_VER);
  L.push("  LEAGUE: <code>");
  L.push("  <YYYY-MM-DD>|<HOME TEAM>|<HOME GOALS>|<AWAY GOALS>|<AWAY TEAM>");
  L.push("  ...");
  L.push("  END");
  L.push("");
  L.push("Worked example:");
  L.push("");
  L.push("  " + SYNC_VER);
  L.push("  LEAGUE: E0");
  L.push("  2026-08-15|Arsenal|2|1|Chelsea");
  L.push("  2026-08-16|Liverpool|3|0|Everton");
  L.push("  END");
  L.push("");
  L.push("RULES — a block that breaks any of these is rejected:");
  L.push("  1. THE TEAM LISTED FIRST IS THE HOME TEAM, playing at its own ground.");
  L.push("     Home/away order is the single most important field here. Some sources and");
  L.push("     feeds reverse it. Verify venue against an official fixture list, not a");
  L.push("     betting page or an odds feed.");
  L.push("  2. Goals are full-time scores, whole numbers 0-20, after 90 minutes + stoppage.");
  L.push("     For any match decided by extra time or penalties, report the 90-minute score.");
  L.push("  3. Dates are the actual date played, ISO YYYY-MM-DD, never in the future.");
  L.push("  4. Use the exact team spellings listed above.");
  L.push("  5. No duplicate fixtures. No estimated, predicted or partial results.");
  L.push("  6. If you cannot verify a match, leave it out. Missing data is fine;");
  L.push("     invented data is not. Add '# note: ...' lines for anything you skipped.");
  L.push("  7. Return the blocks only — no commentary before or after.");
  return L.join("\n");
}

function generateBrief(scope) {
  const t = buildSyncBrief(scope);
  const el = document.getElementById("briefBox");
  el.value = t;
  document.getElementById("briefWrap").className = "";
  document.getElementById("briefMsg").textContent =
    t.length.toLocaleString() + " characters. Copy this into your AI, then paste its reply below.";
}

function copyBrief() {
  const b = document.getElementById("briefBox");
  b.select();
  try { document.execCommand("copy"); } catch (e) {}
  if (navigator.clipboard) { try { navigator.clipboard.writeText(b.value); } catch (e) {} }
  document.getElementById("briefMsg").textContent = "Copied.";
}

/* ---- STRICT PARSER ------------------------------------------------------- */
function parseSyncPayload(text) {
  const res = { blocks: [], rows: [], errors: [], notes: [], ok: false };
  if (!text || !text.trim()) { res.errors.push("Nothing pasted."); return res; }

  const clean = text.replace(/```[a-z]*/gi, "").trim();
  if (clean.toUpperCase().indexOf("PITCH-SYNC") === -1) {
    res.errors.push('Missing the "' + SYNC_VER + '" header — this is not a sync block.');
    return res;
  }

  const lines = clean.split("\n");
  let curLg = null, lineNo = 0, seenInPayload = {};

  lines.forEach(function (raw) {
    lineNo++;
    let line = raw.trim();
    if (!line) return;
    if (/^#/.test(line)) { res.notes.push(line.replace(/^#\s*/, "")); return; }
    if (/^PITCH-SYNC/i.test(line)) return;
    if (/^END$/i.test(line)) { curLg = null; return; }

    const lm = line.match(/^LEAGUE:\s*([A-Za-z0-9]+)\s*$/i);
    if (lm) {
      const code = lm[1].toUpperCase();
      if (!BASE_LEAGUES[code]) {
        res.errors.push("line " + lineNo + ": unknown league code \"" + code + "\"");
        curLg = null;
      } else {
        curLg = code;
        res.blocks.push(code);
      }
      return;
    }

    if (!curLg) {
      res.errors.push("line " + lineNo + ": data row before any LEAGUE: header — \"" + line.slice(0, 60) + "\"");
      return;
    }

    const parts = line.split("|").map(function (s) { return s.trim(); });
    if (parts.length !== 5) {
      res.errors.push("line " + lineNo + ": expected 5 fields separated by |, found " +
        parts.length + " — \"" + line.slice(0, 60) + "\"");
      return;
    }
    const [dt, hRaw, hgRaw, agRaw, aRaw] = parts;

    if (!/^\d{4}-\d{2}-\d{2}$/.test(dt)) {
      res.errors.push("line " + lineNo + ": bad date \"" + dt + "\" (need YYYY-MM-DD)");
      return;
    }
    if (dt > todayISO()) {
      res.errors.push("line " + lineNo + ": date " + dt + " is in the future — not a completed match");
      return;
    }

    const hg = Number(hgRaw), ag = Number(agRaw);
    if (!/^\d{1,2}$/.test(hgRaw) || !/^\d{1,2}$/.test(agRaw) || hg > 20 || ag > 20) {
      res.errors.push("line " + lineNo + ": bad score \"" + hgRaw + "-" + agRaw + "\"");
      return;
    }

    const roster = MODEL.teams[curLg] || {};
    const h = resolveTeam(hRaw, roster), a = resolveTeam(aRaw, roster);
    if (!h) { res.errors.push("line " + lineNo + ': home team "' + hRaw + '" not in the ' + curLg + " roster"); return; }
    if (!a) { res.errors.push("line " + lineNo + ': away team "' + aRaw + '" not in the ' + curLg + " roster"); return; }
    if (h === a) { res.errors.push("line " + lineNo + ": a team cannot play itself"); return; }

    const fp = curLg + "|" + dt + "|" + h + "|" + a;
    if (seenInPayload[fp]) { res.errors.push("line " + lineNo + ": duplicate row inside this paste"); return; }
    seenInPayload[fp] = 1;

    const row = { lg: curLg, date: dt, home: h, away: a, hg: hg, ag: ag, fp: fp,
      renamedH: h !== hRaw ? hRaw : null, renamedA: a !== aRaw ? aRaw : null };

    /* venue plausibility — the flip guard, applied to imported data too */
    const hosted = MODEL.hosted[curLg] || [];
    row.flip = hosted.length && hosted.indexOf(h) === -1;

    /* already applied previously? */
    row.dup = !!(OVERLAY.fp && OVERLAY.fp[fp]);

    res.rows.push(row);
  });

  res.ok = res.rows.length > 0;
  return res;
}

function resolveTeam(name, roster) {
  if (!name) return null;
  if (roster[name]) return name;
  const keys = Object.keys(roster);
  const ls = name.toLowerCase().replace(/\s+/g, " ").trim();
  for (let i = 0; i < keys.length; i++) if (keys[i].toLowerCase() === ls) return keys[i];
  let best = null, bl = 0;
  for (let i = 0; i < keys.length; i++) {
    const k = keys[i].toLowerCase();
    if ((k.indexOf(ls) === 0 || ls.indexOf(k) === 0) && k.length > bl) { best = keys[i]; bl = k.length; }
  }
  return best;
}

/* ---- VALIDATE (dry run) -------------------------------------------------- */
function validateSync() {
  const r = parseSyncPayload(document.getElementById("syncBox").value);
  const el = document.getElementById("syncReport");
  window.__lastSync = r;
  let h = "";

  const fresh = r.rows.filter(function (x) { return !x.dup; });
  const dups = r.rows.filter(function (x) { return x.dup; });
  const flips = fresh.filter(function (x) { return x.flip; });
  const renamed = fresh.filter(function (x) { return x.renamedH || x.renamedA; });

  if (r.errors.length) {
    h += '<div class="banner ban-err"><b>' + r.errors.length + " row(s) rejected</b><br>" +
      r.errors.slice(0, 12).map(esc).join("<br>") +
      (r.errors.length > 12 ? "<br>&hellip; and " + (r.errors.length - 12) + " more" : "") + "</div>";
  }
  if (flips.length) {
    h += '<div class="banner ban-err"><b>Possible home/away flip &mdash; ' + flips.length +
      " match(es)</b><br>These home sides have never hosted in that league in 23 seasons:<br>" +
      flips.map(function (x) { return esc(x.date + "  " + x.home + " v " + x.away); }).join("<br>") +
      "<br>Check the source before applying.</div>";
  }
  if (renamed.length) {
    h += '<div class="banner ban-warn"><b>' + renamed.length + " name(s) auto-matched</b><br>" +
      renamed.slice(0, 8).map(function (x) {
        return esc((x.renamedH ? x.renamedH + " \u2192 " + x.home : "") +
                   (x.renamedA ? (x.renamedH ? "; " : "") + x.renamedA + " \u2192 " + x.away : ""));
      }).join("<br>") + "</div>";
  }
  if (dups.length) {
    h += '<div class="banner ban-info">' + dups.length +
      " match(es) already applied &mdash; they will be skipped, so pasting twice is safe.</div>";
  }
  if (r.notes.length) {
    h += '<div class="banner ban-info"><b>Notes from the source:</b><br>' +
      r.notes.slice(0, 8).map(esc).join("<br>") + "</div>";
  }

  if (fresh.length) {
    const byLg = {};
    fresh.forEach(function (x) { byLg[x.lg] = (byLg[x.lg] || 0) + 1; });
    h += '<div class="banner ban-ok"><b>' + fresh.length + " new result(s) ready to apply</b><br>" +
      Object.keys(byLg).map(function (k) {
        return esc((BASE_LEAGUES[k] ? BASE_LEAGUES[k].name : k) + ": " + byLg[k]);
      }).join("<br>") + "</div>";
    h += "<table><thead><tr><th>Date</th><th>Home</th><th class='num'>Score</th><th>Away</th>" +
      "<th class='num'>Home pts now</th></tr></thead><tbody>";
    fresh.slice(0, 40).forEach(function (x) {
      const r0 = rateFixture(x.lg, x.home, x.away);
      h += "<tr><td>" + esc(x.date) + "</td><td>" + esc(x.home) + "</td><td class='num'>" +
        x.hg + "&ndash;" + x.ag + "</td><td>" + esc(x.away) + "</td><td class='num'>" +
        (r0.error ? "&mdash;" : r0.points) + "</td></tr>";
    });
    h += "</tbody></table>";
    if (fresh.length > 40) h += '<div class="help">&hellip; and ' + (fresh.length - 40) + " more.</div>";
  } else if (!r.errors.length) {
    h += '<div class="banner ban-info">No new results in this paste.</div>';
  }

  document.getElementById("applySyncBtn").disabled = fresh.length === 0;
  el.innerHTML = h;
}

/* ---- APPLY --------------------------------------------------------------- */
function applySync() {
  const r = window.__lastSync;
  if (!r || !r.rows.length) return;
  const fresh = r.rows.filter(function (x) { return !x.dup; });
  if (!fresh.length) return;

  /* chronological order matters: ratings are sequential */
  fresh.sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });

  if (!OVERLAY.fp) OVERLAY.fp = {};
  if (!OVERLAY.through) OVERLAY.through = {};
  if (!OVERLAY.counts) OVERLAY.counts = {};

  let applied = 0, failed = 0;
  fresh.forEach(function (x) {
    const out = applyResult(x.lg, x.home, x.away, x.hg, x.ag);
    if (out.ok) {
      applied++;
      OVERLAY.fp[x.fp] = 1;
      OVERLAY.counts[x.lg] = (OVERLAY.counts[x.lg] || 0) + 1;
      if (!OVERLAY.through[x.lg] || x.date > OVERLAY.through[x.lg]) OVERLAY.through[x.lg] = x.date;
      OVERLAY.applied.push(x.fp + "|" + x.hg + "-" + x.ag);
    } else { failed++; }
  });
  OVERLAY.lastUpdate = todayISO();
  saveOverlay();

  document.getElementById("syncBox").value = "";
  document.getElementById("syncReport").innerHTML =
    '<div class="banner ban-ok"><b>Applied ' + applied + " result(s).</b>" +
    (failed ? " " + failed + " failed." : "") +
    " Ratings, tiers and every market are now up to date." +
    "<br>Leagues now current through: " +
    Object.keys(OVERLAY.through).map(function (k) {
      return esc((BASE_LEAGUES[k] ? BASE_LEAGUES[k].name : k) + " \u2192 " + OVERLAY.through[k]);
    }).join("<br>") + "</div>";
  document.getElementById("applySyncBtn").disabled = true;
  renderUpdateStatus();
  onLeagueChange();
}
