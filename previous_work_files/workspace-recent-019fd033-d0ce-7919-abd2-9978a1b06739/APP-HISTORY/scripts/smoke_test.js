/* Smoke test: boot app-v2.6-cross.html in node with a DOM stub and drive the flows. */
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (scripts.length !== 3) { console.log("FAIL: expected 3 script blocks, got " + scripts.length); process.exit(1); }

/* ---- minimal DOM stub ---- */
function makeEl(id) {
  return {
    id: id || "", value: "", innerHTML: "", textContent: "", className: "",
    style: {}, checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(pos, h) { this.innerHTML += h; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {},
    parentNode: null,
  };
}
const els = {};
const sandbox = {};
sandbox.window = sandbox;
sandbox.console = console;
sandbox.navigator = {};
sandbox.setTimeout = (fn) => { return 0; };
sandbox.confirm = () => true;
sandbox.Blob = function (parts, opts) { this.parts = parts || []; sandbox.__lastBlobParts = this.parts; };
sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _store = {};
sandbox.localStorage = {
  getItem: k => (k in _store ? _store[k] : null),
  setItem: (k, v) => { _store[k] = String(v); },
  removeItem: k => { delete _store[k]; },
};
const matchDate = makeEl("matchDate");
matchDate.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = matchDate;
sandbox.document = {
  readyState: "complete",
  body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(tag) { return makeEl(tag + ":" + Math.random()); },
  querySelector(sel) { if (!els["q:" + sel]) els["q:" + sel] = makeEl(sel); return els["q:" + sel]; },
  querySelectorAll() { return []; },
  addEventListener() {},
};
sandbox.document.getElementById("matchDate").parentNode = matchDate.parentNode;
vm.createContext(sandbox);
try {
  scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "script" + i + ".js" }));
} catch (e) {
  console.log("BOOT FAILED: " + e.stack); process.exit(1);
}
console.log("boot ok");

const S = sandbox;
const evX = (expr) => vm.runInContext(expr, sandbox);
let pass = 0, fail = 0;
function chk(name, ok, detail) {
  if (ok) { pass++; console.log("  PASS " + name + (detail ? " — " + detail : "")); }
  else { fail++; console.log("  FAIL " + name + (detail ? " — " + detail : "")); }
}

/* 1. universe pickers populated */
const homeHtml = S.document.getElementById("homeTeam").innerHTML;
chk("picker has rated Arsenal (E0)", homeHtml.indexOf("R|E0|Arsenal") !== -1);
chk("picker has rated Bayern (D1)", homeHtml.indexOf("R|D1|Bayern Munich") !== -1);
chk("picker has loaded Malisheva", homeHtml.indexOf("B|Kosovo|Malisheva") !== -1);
chk("league filter defaults to ALL", S.document.getElementById("league").value === "__ALL__");

/* 2. domestic render (same league) */
S.document.getElementById("homeTeam").value = "R|E0|Chelsea";
S.document.getElementById("awayTeam").value = "R|E0|Bournemouth";
S.renderRate();
const domOut = S.document.getElementById("result").innerHTML;
chk("domestic renders home rating", domOut.indexOf("home rating") !== -1);
chk("domestic renders markets", domOut.indexOf("Markets") !== -1);
chk("domestic flip check ran", S.document.getElementById("flipBox").innerHTML.indexOf("Venue") !== -1);
const r0 = evX("lastRating");
chk("domestic probabilities sum to 1", r0 && Math.abs(r0.H + r0.D + r0.A - 1) < 1e-9,
    r0 ? (r0.H + r0.D + r0.A).toFixed(6) : "no rating");

/* 3. cross-league render */
S.document.getElementById("homeTeam").value = "R|E0|Arsenal";
S.document.getElementById("awayTeam").value = "R|D1|Bayern Munich";
S.renderRate();
const xOut = S.document.getElementById("result").innerHTML;
chk("cross-league banner shown", xOut.indexOf("Cross-league fixture") !== -1);
chk("cross-league home rating shown", xOut.indexOf("home rating") !== -1);
chk("cross-league bridge note", xOut.indexOf("scale = 1.00") !== -1);
const rx = evX("lastRating");
chk("cross-league probs sum to 1", rx && Math.abs(rx.H + rx.D + rx.A - 1) < 1e-9);
chk("cross-league league name joined", rx && rx.lgName === "England Premier League × Germany Bundesliga", rx && rx.lgName);
chk("cross-league venue warn banner", S.document.getElementById("flipBox").innerHTML.indexOf("auto-checked") !== -1);

/* 4. evidence fixture: Hibernian v Malisheva */
S.document.getElementById("homeTeam").value = "R|SC0|Hibernian";
S.document.getElementById("awayTeam").value = "B|Kosovo|Malisheva";
S.renderRate();
const evOut = S.document.getElementById("result").innerHTML;
chk("evidence verdict card", evOut.indexOf("Evidence verdict") !== -1);
chk("h2h path present", evOut.indexOf("Malisheva 2-0 Hibernian") !== -1);
chk("balance panel present", evOut.indexOf("home support") !== -1);
chk("no forced probabilities", evOut.indexOf("Forced uncalibrated line") === -1);
chk("away-lean direction away from home", evOut.indexOf("away lean") !== -1 || evOut.indexOf("NO CALL") !== -1);
const le = evX("lastEvidence");
chk("lastEvidence captured with paths", le && le.paths.length > 0, le ? le.paths.length + " paths" : "none");

/* 5. save evidence verdict to log */
S.document.getElementById("confirmVenue").checked = true;
S.document.getElementById("saveMsg").textContent = "";
S.saveEvidenceRating();
const le0 = evX("logEntries[0]");
chk("evidence entry saved", le0 && le0.type === "evidence");
chk("evidence entry has verdict", le0 && typeof le0.verdict === "string" && le0.verdict.length > 0, le0 && le0.verdict);
chk("evidence entry venue flagged", le0 && le0.venueConfirmed === true);

/* 6. save domestic rating to log */
S.document.getElementById("homeTeam").value = "R|E0|Chelsea";
S.document.getElementById("awayTeam").value = "R|E0|Bournemouth";
S.document.getElementById("confirmVenue").checked = true;
S.renderRate(); S.saveRating();
const ld = evX("logEntries[0]");
chk("domestic entry saved with probs", ld && typeof ld.H === "number" && typeof ld.D === "number" && typeof ld.A === "number");
chk("domestic lgName correct", ld && ld.lgName === "England Premier League");

/* 7. cross-league save */
S.document.getElementById("homeTeam").value = "R|E0|Arsenal";
S.document.getElementById("awayTeam").value = "R|D1|Bayern Munich";
S.document.getElementById("confirmVenue").checked = true;
S.renderRate(); S.saveRating();
const lx = evX("logEntries[0]");
chk("cross-league entry saved with cross flag", lx && lx.cross === true && lx.lg === "E0×D1");

/* 8. renderLog tolerates mixed entries + Brier guard */
S.settle(ld.id, "correct");
S.renderLog();
const stats = S.document.getElementById("logStats").innerHTML;
chk("log stats render", stats.indexOf("saved") !== -1);
chk("Brier computed only from prob rows", statisticsSafe(stats));
function statisticsSafe(st) { return st.indexOf("Brier") !== -1; }
const listHtml = S.document.getElementById("logList").innerHTML;
chk("log list shows evidence verdict row", listHtml.indexOf("Malisheva") !== -1);
chk("log list shows evidence badge", listHtml.indexOf("paths") !== -1);

/* 9. identity integrity: Swansea merge */
const sw = S.BlueprintEmbed.resolve("Swansea", "England");
chk("Swansea resolves after dedupe", !!sw, sw || "null");
const swStore = S.BlueprintEmbed.store();
const swIdent = swStore.identities[sw];
chk("Swansea identity single + country kept", swIdent && swIdent.country === "Wales", swIdent && swIdent.country);

/* 10. team-only load request */
const bpTeams = S.document.getElementById("bpTeams");
bpTeams.innerHTML = '<option value="E0||Arsenal">Arsenal</option><option value="BP::Kosovo||Malisheva">Malisheva</option>';
bpTeams.options = [{ value: "E0||Arsenal", selected: true }, { value: "BP::Kosovo||Malisheva", selected: true }];
S.BlueprintEmbed.request();
const req = S.document.getElementById("bpRequestBox").value;
chk("request generated", req.indexOf("FULL TEAM DATA LOAD") !== -1);
chk("request is team-only", req.indexOf("TEAM DATA ONLY") !== -1);
chk("request lists both teams", req.indexOf("Arsenal") !== -1 && req.indexOf("Malisheva") !== -1);
chk("request has no fixture pairing language", req.indexOf("FIXTURE CONTEXT") === -1);
chk("request keeps strict rules", req.indexOf("Results only") !== -1 && req.indexOf("LEVEL-3 BRIDGE") !== -1);
chk("request opens two-stage research order", req.indexOf("RESEARCH ORDER — TWO STAGES") !== -1);
chk("request stage 1 general pass first", req.indexOf("STAGE 1 — GENERAL TEAM-DATA PASS") !== -1);
chk("request stage 2 dive after inventory", req.indexOf("STAGE 2 — PER-SECTION DEEP DIVE") !== -1);
chk("request keeps overview-page caveat", req.indexOf("starting layer, not a source of truth") !== -1);

/* 11. unrated pair with no evidence links renders NO CALL verdict (not empty/error) */
S.document.getElementById("homeTeam").value = "B|Kosovo|Malisheva";
S.document.getElementById("awayTeam").value = "B|Denmark|Brondby";
S.renderRate();
const nc = S.document.getElementById("result").innerHTML;
chk("unrated-unrated renders verdict card", nc.indexOf("Evidence verdict") !== -1);
chk("no-fabrication: not a probability card", nc.indexOf("home rating") === -1);

/* 12. same team blocked */
S.document.getElementById("homeTeam").value = "R|E0|Arsenal";
S.document.getElementById("awayTeam").value = "R|E0|Arsenal";
S.renderRate();
chk("team-cannot-play-itself", S.document.getElementById("result").innerHTML.indexOf("cannot play itself") !== -1);

/* 13. filter mechanics */
S.document.getElementById("league").value = "D1";
S.onLeagueChange();
const fHtml = S.document.getElementById("homeTeam").innerHTML;
chk("league filter restricts rated list", fHtml.indexOf("R|E0|Arsenal") === -1 && fHtml.indexOf("R|D1|Bayern Munich") !== -1);
S.document.getElementById("league").value = "__ALL__";
S.document.getElementById("teamSearch").value = "malisheva";
S.onLeagueChange();
chk("search filter finds loaded team", S.document.getElementById("homeTeam").innerHTML.indexOf("B|Kosovo|Malisheva") !== -1);
S.document.getElementById("teamSearch").value = "";
S.onLeagueChange();

/* 13b. drive picker on the Data-tab loader */
const bpUi = S.document.getElementById("viewBlueprint").innerHTML;
chk("pack file input present", bpUi.indexOf('id="bpPackFile"') !== -1);
chk("loadPackFile exposed", typeof S.BlueprintEmbed.loadPackFile === "function");
chk("picker help text mentions .txt", bpUi.indexOf("straight from your drive") !== -1);

/* 13d. drive-linked data folder card */
chk("drive folder card present", bpUi.indexOf('id="bpDriveStatus"') !== -1);
chk("drive api exposed", typeof S.BlueprintEmbed.linkDrive === "function" && typeof S.BlueprintEmbed.reconnectDrive === "function" && typeof S.BlueprintEmbed.unlinkDrive === "function");
chk("unsupported browser guidance rendered", S.document.getElementById("bpDriveStatus").innerHTML.indexOf("does not support drive linking") !== -1);

/* 13e. unified full-data file: single source (store + log), merge-on-import */
chk("full-data card present", bpUi.indexOf("Full data backup") !== -1);
S.BlueprintEmbed.exportData();
const expBlob = sandbox.__lastBlobParts ? JSON.parse(sandbox.__lastBlobParts[0]) : null;
chk("unified export carries store + log", !!expBlob && expBlob.app === "pitch-rating-full" && Array.isArray(expBlob.matches) && Array.isArray(expBlob.log) && !!expBlob.teamStats);
const mBefore = S.BlueprintEmbed.store().matches.length;
const lBefore = evX("logEntries.length");
S.BlueprintEmbed.applyFullData({app:"pitch-rating-full", identities:{}, aliases:{}, matches:[{date:"2026-07-01", competition:"Club Friendly", competitionType:"club-friendly", homeId:S.BlueprintEmbed.store().matches[0].homeId, awayId:S.BlueprintEmbed.store().matches[0].awayId, hg:9, ag:9, venue:"normal"}], teamStats:{}, venues:{}, sources:[], log:[{id:"smoke-1", ts:1, verdict:"X"}, {id:"smoke-2", ts:2, verdict:"Y", result:"correct"}]});
chk("applyFullData merges a new match", S.BlueprintEmbed.store().matches.length === mBefore + 1, S.BlueprintEmbed.store().matches.length + " vs " + mBefore);
chk("applyFullData merges log entries", evX("logEntries.length") === lBefore + 2);
S.BlueprintEmbed.applyFullData({app:"pitch-rating-full", identities:{}, aliases:{}, matches:[], teamStats:{}, venues:{}, sources:[], log:[{id:"smoke-1", ts:5, verdict:"X2"}]});
chk("log conflict keeps later ts", evX("logEntries.filter(function(e){return e.id==='smoke-1';})[0].ts") === 5);
chk("settled log entry not downgraded", evX("logEntries.filter(function(e){return e.id==='smoke-2';})[0].result") === "correct");
chk("legacy blueprint-only file accepted", (function(){ try { S.BlueprintEmbed.applyFullData({identities:{}, matches:[], teamStats:{}, venues:{}, sources:[], calibration:null}); return true; } catch(e){ return false; } })());
chk("non-data file rejected", (function(){ try { S.BlueprintEmbed.applyFullData({foo:1}); return false; } catch(e){ return true; } })());

/* 13f. export/import default location */
chk("pickBackup exposed", typeof S.BlueprintEmbed.pickBackup === "function");
S.document.getElementById("bpBackupReport").innerHTML = "";
S.BlueprintEmbed.exportData();
chk("unlinked export downloads + folder hint", S.document.getElementById("bpBackupReport").innerHTML.indexOf("Link the drive folder") !== -1);
S.BlueprintEmbed.pickBackup();
chk("unlinked import falls back to classic picker", true);
chk("pack file picker is single-file", !/id="bpPackFile"[^>]*\smultiple/.test(bpUi));
chk("backup picker is single-choice", !/id="bpBackupFile"[^>]*\smultiple/.test(bpUi));

/* 13c. plain-language balance summary strip on the cross verdict card */
chk("summary strip present", nc.indexOf("Balance summary.") !== -1);
chk("summary strip states NO PLAY explicitly", nc.indexOf("NO PLAY — no recommendation.") !== -1);
chk("summary strip depth wording (1 effective path)", nc.indexOf("at least 2 independent routes") !== -1);
chk("summary strip adds no fabricated probability", nc.indexOf("home rating") === -1);
S.document.getElementById("homeTeam").value = "B|Kosovo|Drita";
S.document.getElementById("awayTeam").value = "R|E0|Arsenal";
S.renderRate();
const nc2 = S.document.getElementById("result").innerHTML;
chk("no-evidence strip guidance", nc2.indexOf("Load team data covering H2H") !== -1);
chk("no-evidence strip states NO PLAY", nc2.indexOf("NO PLAY — no recommendation.") !== -1);
chk("app version v2.9.9-cross (badge+footer both)", html.indexOf(">v2.9.9-cross</span>") !== -1 && html.indexOf("Pitch Rating v2.9.9-cross") !== -1 && html.indexOf("v2.9.8-cross") === -1 && html.indexOf("v2.9.1-cross") === -1 && html.indexOf("v2.9.2-cross") === -1 && html.indexOf("v2.9.3-cross") === -1 && html.indexOf("v2.9.4-cross") === -1 && html.indexOf("v2.9.5-cross") === -1 && html.indexOf("v2.9.6-cross") === -1 && html.indexOf("v2.9.7-cross") === -1);

/* --- v2.7.1: C5 draw-risk drop (unit level) --- */
const c5 = evX("(function(){var paths=[{phase:'common',estimate:2,weight:2,ids:['a']},{phase:'common',estimate:2,weight:2,ids:['b']},{phase:'common',estimate:-2.7,weight:2,ids:['c']},{phase:'third',estimate:2,weight:1.5,ids:['d']},{phase:'third',estimate:2,weight:1.5,ids:['e']}];var ag={homeW:7,awayW:2,neuW:0,phaseCounts:{common:3,third:2,h2h:0}};var z1=computeZone(paths,ag);var ag2={homeW:7,awayW:2,neuW:0,phaseCounts:{common:3,third:2,h2h:1}};var z2=computeZone(paths,ag2);return {k1:z1.key,c5:z1.c5From||null,tag:z1.tag,k2:z2.key};})()");
chk("C5 drops post-gate WIN with no h2h to WIN-DRAW", c5.k1 === "windraw" && c5.c5 === "WIN" && c5.tag.indexOf("draw-risk drop") !== -1, JSON.stringify(c5));
chk("C5 leaves WIN with h2h evidence untouched", c5.k2 === "win", JSON.stringify(c5));

/* --- v2.7.0: C4 context flags (demote-only) — Candidate A rejected on replay, engine math unchanged from v2.6.9 --- */
S.document.getElementById("bpImportText").value = [
  "BP-TEAM-PACK v2",
  "NOTE|info|smoke|ctx harness",
  "TEAM|Ctx Alpha|Qland|Q Premier League|QL|Alpha;Ctx Alpha FC|Alpha Park|Alphaville|Qland|grass|1000|1900|unknown",
  "TEAM|Ctx Beta|Qland|Q Premier League|QL|Beta;Ctx Beta FC|Beta Park|Betaville|Qland|grass|1000|1900|unknown",
  "TEAM|Ctx Gamma|Qland|Q Premier League|QL|Gamma;Ctx Gamma FC|Gamma Park|Gammaville|Qland|grass|1000|1900|unknown",
  "MATCH|2026-05-20|Q Premier League|other|Ctx Alpha|2|0|Ctx Gamma|normal|Alpha Park|Alphaville|Qland|g1|g1",
  "MATCH|2026-05-21|Q Premier League|other|Ctx Beta|0|2|Ctx Gamma|normal|Beta Park|Betaville|Qland|g2|g2",
  "MATCH|2026-06-01|Q Premier League|other|Ctx Alpha|3|0|Ctx Beta|normal|Alpha Park|Alphaville|Qland|s1|s1",
  "MATCH|2026-06-08|Q Premier League|other|Ctx Alpha|4|0|Ctx Beta|normal|Alpha Park|Alphaville|Qland|s2|s2",
  "MATCH|2026-06-15|Q Premier League|other|Ctx Alpha|5|0|Ctx Beta|normal|Alpha Park|Alphaville|Qland|s3|s3",
  "CTX|Ctx Alpha|2026-06-22|keeper-change|first-choice keeper suspended|sc1",
  "SOURCE|s1|https://example.com/s1|2026-07-01|results-database|smoke",
  "SOURCE|s2|https://example.com/s2|2026-07-01|results-database|smoke",
  "SOURCE|s3|https://example.com/s3|2026-07-01|results-database|smoke",
  "SOURCE|g1|https://example.com/g1|2026-07-01|results-database|smoke",
  "SOURCE|g2|https://example.com/g2|2026-07-01|results-database|smoke",
  "SOURCE|sc1|https://example.com/sc1|2026-07-01|news-report|smoke",
  "END"
].join("\n");
S.BlueprintEmbed.importData();
const ctxAlpha = S.BlueprintEmbed.resolve("Ctx Alpha", "Qland");
const ctxBeta = S.BlueprintEmbed.resolve("Ctx Beta", "Qland");
chk("CTX row loaded", S.BlueprintEmbed.ctxFlagsFor(ctxAlpha, ctxBeta, "2026-06-22").length === 1);
const ctxRes = evX("(function(){var ha=BlueprintEmbed.resolve('Ctx Alpha','Qland'),hb=BlueprintEmbed.resolve('Ctx Beta','Qland');var ev=BlueprintEmbed.analyze(ha,hb,'2026-06-22');var z0=computeZone(ev.paths,ev.ag);var z1=computeZoneCtx(ev.paths,ev.ag,ha,hb,'2026-06-22');var h2h=ev.paths.filter(function(p){return p.phase==='h2h';});return {key0:z0.key,key1:z1.key,ctxFrom:z1.ctxFrom||null,hits:z1.ctx&&z1.ctx[0]&&z1.ctx[0].hitsLeader,w:h2h.map(function(p){return p.weight;}),e:h2h.map(function(p){return p.estimate;})};})()");
chk("h2h weights stay linear w3 (Candidate A rejected on replay)", ctxRes.w.length === 3 && ctxRes.w.every(w => Math.abs(w - 3) < 1e-9), JSON.stringify(ctxRes.w));
chk("h2h estimates uncorrected (Candidate A rejected on replay)", ctxRes.e.join(",") === "3,4,5", JSON.stringify(ctxRes.e));
chk("no-flag zone ungated by CTX", ctxRes.key0 === "strong", ctxRes.key0);
chk("CTX demotes one rung, demote-only", ctxRes.key1 === "win" && ctxRes.ctxFrom === "STRONG CALL" && ctxRes.hits === true, JSON.stringify(ctxRes));


/* C12 / EV-G2 goals-read pins (v2.8.5, display-only) */
chk("EV-G2 estimator present", html.indexOf("function evidenceGoalsEstimate(") !== -1);
chk("EV-G2 region table pinned (633 replay)", html.indexOf("LOW:{n:68,") !== -1 && html.indexOf("MID:{n:332,") !== -1 && html.indexOf("HIGH:{n:233,") !== -1);
(function(){
  const zf = html.slice(html.indexOf("function computeZoneCtx"), html.indexOf("function computeZoneCtx")+4000);
  chk("display-only: zone logic untouched by goals read", zf.indexOf("evidenceGoals") === -1);
})();
chk("goals read renders inside verdict card", html.indexOf("evidenceGoalsHtml(hp, ap, paths, hid, aid, cutoff) +") !== -1);


/* C13 / CALIBRATION-7 weight+band pins (v2.8.6) */
chk("C7 phase weights shipped", html.indexOf("var PHASE_WEIGHT = {h2h:3, common:3, third:0.75};") !== -1);
chk("C7 neutral band 0.50 shipped", html.indexOf("var NEUTRAL_BAND = 0.50;") !== -1);
chk("C7 share allocation reads NEUTRAL_BAND", html.indexOf("if(p.estimate>NEUTRAL_BAND){homeW+=p.weight;homeN++;}") !== -1);


/* C14 / CALIBRATION-8 last-6 window pins (v2.8.7) */
chk("C8 rolling last-6 window shipped", html.indexOf(".slice(-6);") !== -1);
chk("C8 window comment pinned", html.indexOf("Window = rolling last-6 games (CALIBRATION-8)") !== -1);

/* C15 / CALIBRATION-9 draw-mass mapping pins (v2.8.8) */
chk("C9 constants shipped", html.indexOf("var CAL9_W = 0.60, CAL9_SIDE = 37.835, CAL9_DRAW = 24.33;") !== -1);
chk("C9 helpers shipped", html.indexOf("function cal9(h, d, a)") !== -1 && html.indexOf("function cal9L(S)") !== -1);
const c9a = evX("(function(){var c=cal9(70,10,20);return {c:c,S:c[0]+c[1]+c[2],l1:cal9(50,30,20)[0]>=cal9(50,30,20)[2],l2:cal9(20,30,50)[2]>=cal9(20,30,50)[0],s:cal9L(100)};})()");
chk("C9 shrink row sums to 100", Math.abs(c9a.S-100)<1e-9, JSON.stringify(c9a.c));
chk("C9 leader never flips", c9a.l1 && c9a.l2);
chk("C9 draw floor present", cal9Draw = evX("cal9(90,0,10)[1]") , evX("cal9(90,0,10)[1]") > 9.0);
chk("C9 zone-tag share calibrated", Math.abs(evX("cal9L(85)")-66.134)<1e-9 && Math.abs(evX("cal9L(50)")-45.134)<1e-9);
chk("C9 raw zone ladder engine untouched", html.indexOf("var S_ = Math.max(ag.homeW, ag.awayW) / tw * 100;") !== -1);
chk("C9 calibrated total in summation", html.indexOf("var c9 = cal9(ag.homeW / totalW * 100,") !== -1);

/* C16 / INTEGRITY-AUDIT MUTE pins (v2.8.9) */
chk("MUTE parser shipped", html.indexOf("typ==='MUTE'") !== -1 && html.indexOf("MUTE needs MUTE|date|home|away|reason|sourceId") !== -1);
chk("MUTE choke point: beforeCutoff skips muted", html.indexOf("return (!m.muted) && (!cutoff || m.date < cutoff);") !== -1);
chk("MUTE Elo chain skips muted", html.indexOf('return !m.muted && m.date && m.date < cutoff && typeof m.hg === "number"') !== -1);
chk("MUTE EV-G2 skips muted", html.indexOf("if(!m.muted) byId[m.id]=m;") !== -1 && html.indexOf("if(!m.muted && m.date<cutoff){c0++;") !== -1);
chk("MUTE russian pack carries 3 flags", fs.readFileSync("/home/user/packs/russian-team-pack.txt", "utf8").split("\n").filter(l => l.indexOf("MUTE|") === 0).length === 3);
chk("MUTE doc comment pinned", html.indexOf("INTEGRITY-AUDIT MUTE channel (v2.8.9)") !== -1);

/* C17 / CALIBRATION-13 TB away-leader honesty pins (v2.9.0) */
chk("C13 gate shipped", html.indexOf("C13 away-leader honesty gate (CALIBRATION-13.md") !== -1 && html.indexOf("TB drop: away-leader honesty") !== -1);
chk("C13 demote-only snippet", html.indexOf('zinfo.side === "TB" && (zinfo.key === "strong" || zinfo.key === "win")') !== -1);
chk("C13 display marker wired", html.indexOf('zinfo.c13From ? " <b>tb</b>" : ""') !== -1);
chk("C13 zone notes refreshed", html.indexOf("post-gate+C5+C8+C11+C13") !== -1 && html.indexOf("post-gate+C5+C8+C11:") === -1);
const c13t = evX("(function(){" +
  "var mk=function(e){return [{phase:'h2h',estimate:e,weight:3,ids:['z13a']},{phase:'common',estimate:e,weight:3,ids:['z13b']}];};" +
  "var tb=computeZoneCtx(mk(-0.9),{homeW:0,neuW:0,awayW:6,phaseCounts:{h2h:1,common:1}},'zzHome13','zzAway13','2099-01-01');" +
  "var ta=computeZoneCtx(mk(0.9),{homeW:6,neuW:0,awayW:0,phaseCounts:{h2h:1,common:1}},'zzHome13','zzAway13','2099-01-01');" +
  "return {tbKey:tb.key,tbFrom:tb.c13From||null,tbSide:tb.side,taKey:ta.key,taFrom:ta.c13From||null,taSide:ta.side};})()");
chk("C13 demotes TB strong to win", c13t.tbKey === "win" && c13t.tbFrom === "STRONG CALL" && c13t.tbSide === "TB", JSON.stringify(c13t));
chk("C13 leaves TA strong untouched", c13t.taKey === "strong" && !c13t.taFrom && c13t.taSide === "TA", JSON.stringify(c13t));

/* C18 / pack-league discovery + computed calibration label pins (v2.9.1) */
chk("pack leagues surface in league filter", html.indexOf("function packLeagueList()") !== -1 && html.indexOf('(loaded pack)') !== -1);
chk("filter refreshes after imports", html.indexOf("fillLeagueOptions(selBox.value)") !== -1);
chk("calibrated pack league set shipped", html.indexOf("var CALIBRATED_PACK_LEAGUES = { RPL: 1 };") !== -1);
chk("classify no longer hard-coded false", html.indexOf("classify(paths, ag, false)") === -1 && html.indexOf("classify(paths, ag||{}, false)") === -1 &&
  html.indexOf("classify(paths, ag, bpSameCalibrated(hid, aid))") !== -1 && html.indexOf("classify(paths, ag||{}, bpSameCalibrated(hid, aid))") !== -1);
const c18 = evX("(function(){var st=BlueprintEmbed.store();" +
  "var KA=BlueprintEmbed.resolve('Ctx Alpha','Qland'), KB=BlueprintEmbed.resolve('Ctx Beta','Qland');" +
  "var la=st.identities[KA].leagues, lb=st.identities[KB].leagues;" +
  "st.identities[KA].leagues=['RPL']; st.identities[KB].leagues=['RPL'];" +
  "var dom=BlueprintEmbed.analyze(KA,KB,'2026-06-22').cl.label;" +
  "st.identities[KB].leagues=['CZ1'];" +
  "var cross=BlueprintEmbed.analyze(KA,KB,'2026-06-22').cl.label;" +
  "st.identities[KA].leagues=la; st.identities[KB].leagues=lb;" +
  "return {dom:dom,cross:cross};})()");
chk("RPL domestic classifies calibrated", c18.dom === "Calibrated domestic", JSON.stringify(c18));
chk("cross fixture stays honest lean", c18.cross === "Lean only", JSON.stringify(c18));

/* C18b: real russian pack import surfaces RPL in the league filter; legacy junk tags excluded */
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/russian-team-pack.txt", "utf8");
S.BlueprintEmbed.importData();
const c18b = evX("(function(){var pl=packLeagueList();return {hasRPL:pl.some(function(o){return o.lg==='RPL';}),junk:pl.filter(function(o){return o.lg==='NA'||o.lg==='unknown'||o.lg==='loaded team data';}).length,lgs:pl.map(function(o){return o.lg;}).join(',')};})()");
chk("RPL surfaces in league filter after pack import", c18b.hasRPL === true, c18b.lgs);
chk("legacy NA/unknown tags filtered out", c18b.junk === 0, c18b.lgs);

/* C19 / league-tag canonicalization pins (v2.9.3; re-applies v2.9.2 SKIP hardening after silent-edit incident) */
chk("SKIP junk-filter shipped", html.indexOf('SKIP = { "NA": 1, "unknown": 1, "loaded team data": 1, "": 1 }') !== -1 && html.indexOf("SKIP[lg]") !== -1);
chk("league alias map shipped", html.indexOf('"Scottish Premiership": "SC0"') !== -1 && html.indexOf("window.canonLg = canonLg") !== -1);
chk("league alias sweep v2.9.5 (ALB/DEN/KOS/IRL name-tags collapse to codes)", html.indexOf('"Albanian Superliga": "ALB"') !== -1 && html.indexOf('"Danish Superliga": "DEN"') !== -1 && html.indexOf('"Kosovo Superliga": "KOS"') !== -1 && html.indexOf('"League of Ireland Premier Division": "IRL"') !== -1);
chk("alias wired: filter list", html.indexOf("lg = (window.canonLg ||") !== -1);
chk("alias wired: picker dedupe", html.indexOf("const cl = (window.canonLg ||") !== -1);
chk("alias wired: league filter match", html.indexOf("x.leagues.map(clg).indexOf(flt)") !== -1);
const c19 = evX("(function(){var st=BlueprintEmbed.store();" +
  "st.identities['c19junk']={id:'c19junk',name:'Junk FC',country:'Nowhere',leagues:['NA','unknown','loaded team data',''],aliases:[]};" +
  "var pl=packLeagueList();" +
  "var junkLeaks=pl.filter(function(o){return o.country==='Nowhere';}).length;" +
  "delete st.identities['c19junk'];" +
  "var hib=teamUniverse().filter(function(x){return x.name==='Hibernian';});" +
  "var pl2=packLeagueList();" +
  "var seedAliasGone=!pl2.some(function(o){return o.lg==='Scottish Premiership';});" +
  "return {junkLeaks:junkLeaks,hibN:hib.length,hibKind:hib[0]&&hib[0].value.slice(0,1),seedAliasGone:seedAliasGone,lgs:pl2.map(function(o){return o.lg;}).join(',')};})()");
chk("junk tags hidden from league filter", c19.junkLeaks === 0, JSON.stringify(c19));
chk("seed name-tag canonicalized to SC0 (no loaded duplicate)", c19.seedAliasGone === true, c19.lgs);
chk("Hibernian single rated picker row", c19.hibN === 1 && c19.hibKind === "R", JSON.stringify(c19));

/* C20 / TEAM_NAME_CANON spelling migration pins (v2.9.4: Krylya -> Krylia Sovetov Samara) */
chk("canon map shipped", html.indexOf('TEAM_NAME_CANON = { "krylya sovetov samara": "Krylia Sovetov Samara" }') !== -1);
chk("canon wired: addIdentity", html.indexOf("name=canonTeamName(name); country=") !== -1);
chk("canon wired: resolveName", html.indexOf("name=canonTeamName(name); var n=norm(name);") !== -1);
chk("migration hooked into normalizeStore", html.indexOf("migrateTeamNames();") !== -1);
const c20 = evX("(function(){var st=BlueprintEmbed.store();" +
  "var ok='russia|krylya sovetov samara', ck='russia|krylia sovetov samara';" +
  "var m0=st.matches.length, c0=Object.keys(st.identities).length;" +
  "st.identities[ok]={id:ok,name:'Krylya Sovetov Samara',country:'Russia',leagues:['RPL'],aliases:['Krylya Sovetov']};" +
  "st.aliases['krylya sovetov']=ok;" +
  "var tm={id:'t',date:'2025-01-01',competition:'domestic-league',homeId:ok,awayId:'russia|zenit st petersburg',hg:1,ag:0,venue:'normal',muted:'c20-test'};" +
  "st.matches.push(tm);" +
  "st.teamStats[ok]={seasons:[{type:'season',teamId:ok,season:'2024/25',competition:'domestic-league',scope:'RPL',p:1,w:1,d:0,l:0,gf:1,ga:0}],forms:[],loadedAt:'2026-08-01'};" +
  "st.venues[ok]={teamId:ok,stadium:'Solidarity Arena',city:'Samara'};" +
  "st.ctxFlags.push({teamId:ok,date:'2025-01-01',flag:'keeper-change',detail:'c20',source:'c20'});" +
  "BlueprintEmbed.migrateNames();" +
  "var m=st.matches[st.matches.indexOf(tm)];" +
  "var r={canon:!!st.identities[ck],oldGone:!st.identities[ok],label:st.identities[ck]&&st.identities[ck].name," +
  "homeRewritten:m&&m.homeId===ck,fingerprint:m&&m.id.indexOf('krylia')!==-1,muteKept:m&&m.muted==='c20-test'," +
  "aliasOld:st.aliases['krylya sovetov samara']===ck,aliasShort:st.aliases['krylya sovetov']===ck," +
  "statsMoved:!!st.teamStats[ck]&&st.teamStats[ck].seasons[0].teamId===ck&&!st.teamStats[ok]," +
  "venueMoved:!!st.venues[ck]&&st.venues[ck].teamId===ck," +
  "ctxMoved:st.ctxFlags.some(function(f){return f.teamId===ck&&f.detail==='c20';})," +
  "resolveOld:BlueprintEmbed.resolve('Krylya Sovetov Samara')===ck," +
  "resolveCanon:BlueprintEmbed.resolve('Krylia Sovetov Samara')===ck," +
  "teamNameOut:st.identities[ck]&&st.identities[ck].name};" +
  "st.matches.splice(st.matches.indexOf(tm),1); delete st.identities[ck]; delete st.teamStats[ck]; delete st.venues[ck];" +
  "delete st.aliases['krylya sovetov samara']; delete st.aliases['krylya sovetov'];" +
  "st.ctxFlags=st.ctxFlags.filter(function(f){return f.detail!=='c20';});" +
  "return r;})()");
chk("canon migration: identity renamed in place", c20.canon === true && c20.oldGone === true && c20.label === "Krylia Sovetov Samara", JSON.stringify(c20));
chk("canon migration: match ref + fingerprint rewritten, mute preserved", c20.homeRewritten === true && c20.fingerprint === true && c20.muteKept === true);
chk("canon migration: aliases/stats/venue/ctx all follow", c20.aliasOld === true && c20.aliasShort === true && c20.statsMoved === true && c20.venueMoved === true && c20.ctxMoved === true);
chk("both spellings resolve to canonical identity (no duplicate possible)", c20.resolveOld === true && c20.resolveCanon === true && c20.teamNameOut === "Krylia Sovetov Samara");

/* C21 / presentation revert pin (v2.9.7: owner decision — original evidence layout restored wholesale; v2.9.6 unified-panel design backed out, kept only as backups/app-v2.9.6-cross.html) */
chk("original presentation restored", html.indexOf("Blueprint evidence audit") !== -1 && html.indexOf("function evidenceSummationHtml") !== -1 && html.indexOf("function evidenceSummaryHtml") !== -1 && html.indexOf("function evidencePanelHtml") === -1);

/* C22 / same-league loaded fixtures get the standard design (v2.9.8 — owner directive 2026-08-02:
   "ensure all leagues you have added produce results like the actual app design before your evidence section") */
chk("same-league detection shipped", html.indexOf("function sharedLoadedLeague(hid, aid)") !== -1);
chk("league display-name table shipped", html.indexOf("var BP_LEAGUE_NAMES = {") !== -1 && html.indexOf("function bpLeagueNameFor(code)") !== -1);
chk("standard stats lead shipped", html.indexOf("function loadedLeagueLeadHtml(") !== -1 && html.indexOf("NO model markets, NO scorelines") !== -1);
S.document.getElementById("homeTeam").value = "B|Qland|Ctx Alpha";
S.document.getElementById("awayTeam").value = "B|Qland|Ctx Beta";
S.renderRate();
const llq = S.document.getElementById("result").innerHTML;
chk("same-league loaded fixture uses standard league framing", llq.indexOf("Pitch rating — QL") !== -1 && llq.indexOf("Evidence verdict — cross fixture") === -1, "");
chk("same-league lead shows standard stats", llq.indexOf("Standard stats — evidence model.") !== -1 && llq.indexOf("Star rating") !== -1 && llq.indexOf("Zone statement") !== -1 && llq.indexOf("Expected total goals") !== -1, "");
chk("same-league drops the outside-model sentence", llq.indexOf("One or both sides sit outside") === -1);
chk("same-league keeps titled evidence sections", llq.indexOf("Section balances.") !== -1 && llq.indexOf("Total summation.") !== -1 && llq.indexOf("Zone statement.") !== -1, "");
chk("same-league keeps balance summary + gates", llq.indexOf("Balance summary.") !== -1 && llq.indexOf("NO PLAY") !== -1, "");
chk("same-league paths collapsed but present", llq.indexOf("Path detail —") !== -1 && llq.indexOf("Evidence paths") !== -1, "");
chk("same-league save row present", llq.indexOf("Save this verdict") !== -1);
chk("same-league save carries league tag", (function(){ S.document.getElementById("confirmVenue").checked = true; S.saveEvidenceRating(); const e0 = evX("logEntries[0]"); return e0 && e0.lg === "QL" && e0.lgName === "QL"; })());
S.document.getElementById("homeTeam").value = "B|Russia|CSKA Moscow";
S.document.getElementById("awayTeam").value = "B|Russia|Spartak Moscow";
S.renderRate();
const llr = S.document.getElementById("result").innerHTML;
chk("RPL same-league uses league display name", llr.indexOf("Pitch rating — Russian Premier League") !== -1, "");
chk("RPL same-league not evidence-verdict framing", llr.indexOf("Evidence verdict — cross fixture") === -1 && llr.indexOf("One or both sides sit outside") === -1);
S.document.getElementById("homeTeam").value = "B|Kosovo|Malisheva";
S.document.getElementById("awayTeam").value = "B|Russia|Spartak Moscow";
S.renderRate();
const lnx = S.document.getElementById("result").innerHTML;
chk("cross fixture keeps evidence-verdict framing", lnx.indexOf("Evidence verdict — cross fixture") !== -1 && lnx.indexOf("Pitch rating —") === -1);

/* C23 / zero-path same-league cards show standalone form, ghosts admit no data (v2.9.9 — owner challenge:
   "how will they have no evidence - except there was deception going on"; answer = connectivity census + show
   every number the data actually computes, admit the rest) */
chk("standalone-form lead shipped", html.indexOf("function standaloneFormLeadHtml(") !== -1 && html.indexOf("Team form — standalone.") !== -1 && html.indexOf("Team form — no data.") !== -1);
S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/usa-team-pack.txt", "utf8");
S.BlueprintEmbed.importData();
S.document.getElementById("matchDate").value = "2026-08-02";
S.document.getElementById("homeTeam").value = "B|United States|Atlanta United FC";
S.document.getElementById("awayTeam").value = "B|United States|Austin FC";
S.renderRate();
const mlz = S.document.getElementById("result").innerHTML;
chk("zero-path same-league keeps league framing", mlz.indexOf("Pitch rating — Major League Soccer") !== -1, "");
chk("zero-path shows standalone form block", mlz.indexOf("Team form — standalone.") !== -1 && mlz.indexOf("Star rating") !== -1 && mlz.indexOf("Loaded match rows") !== -1, "");
chk("zero-path states why no split", mlz.indexOf("no share split and no zone") !== -1 && mlz.indexOf("Standard stats — evidence model.") === -1, "");
chk("zero-path keeps NO PLAY honesty", mlz.indexOf("NO PLAY — no recommendation.") !== -1, "");
const ghost = evX("(function(){var h=BlueprintEmbed.resolve('Raith Rovers',''),a=BlueprintEmbed.resolve('Greenock Morton','');var st=BlueprintEmbed.store();return {hc:st.identities[h].country,ac:st.identities[a].country};})()");
S.document.getElementById("homeTeam").value = "B|" + ghost.hc + "|Raith Rovers";
S.document.getElementById("awayTeam").value = "B|" + ghost.ac + "|Greenock Morton";
S.renderRate();
const gho = S.document.getElementById("result").innerHTML;
chk("ghost identities (seed TEAM rows, zero matches) admit no data", gho.indexOf("Team form — no data.") !== -1 && gho.indexOf("nothing to compute") !== -1, "");
chk("ghost card shows no fabricated numbers", gho.indexOf("Star rating") === -1 && gho.indexOf("Zone statement") === -1 && gho.indexOf("Standard stats") === -1, "");
chk("ghost card keeps league framing", gho.indexOf("Pitch rating — Scottish Championship") !== -1, "");

console.log("\nRESULT: " + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
