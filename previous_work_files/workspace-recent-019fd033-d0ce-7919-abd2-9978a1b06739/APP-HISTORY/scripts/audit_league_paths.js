/* audit_league_paths.js — AUDIT ONLY, no app edits.
   Boots the app, imports all 6 packs, then for every stocked league with >=2
   identities simulates a same-league fixture and records which render path fires.
   Classifies by output markers:
     DOMESTIC  = "home rating" (the standard model card)
     CROSS-DC  = renderCrossLeague markers
     EVID-X    = "Evidence verdict — cross fixture" (evidence-only fallback)
     OTHER/ERR = anything else (printed raw head)
*/
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);

function makeEl(id) {
  return {
    id: id || "", value: "", innerHTML: "", textContent: "", className: "",
    style: {}, checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(pos, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null,
  };
}
const els = {};
const sandbox = {};
sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function (p) { this.parts = p || []; };
sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _ls = {};
sandbox.localStorage = { getItem: k => (k in _ls ? _ls[k] : null), setItem: (k, v) => { _ls[k] = String(v); }, removeItem: k => { delete _ls[k]; } };
const matchDate = makeEl("matchDate");
matchDate.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = matchDate;
sandbox.document = {
  readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(tag) { return makeEl(tag + ":" + Math.random()); },
  querySelector(sel) { if (!els["q:" + sel]) els["q:" + sel] = makeEl(sel); return els["q:" + sel]; },
  querySelectorAll() { return []; }, addEventListener() {},
};
sandbox.document.getElementById("matchDate").parentNode = matchDate.parentNode;
vm.createContext(sandbox);
try { scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "script" + i + ".js" })); }
catch (e) { console.log("BOOT FAILED: " + e.stack); process.exit(1); }
const S = sandbox;
const evX = (expr) => vm.runInContext(expr, sandbox);

/* import all 6 packs in canonical order */
const packs = ["russian-team-pack.txt", "czech-team-pack.txt", "hibernian-team-pack.txt",
  "malisheva-team-pack.txt", "malisheva-closure-pack.txt", "usa-team-pack.txt"];
packs.forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p, "utf8");
  S.BlueprintEmbed.importData();
});
const st = S.BlueprintEmbed.store();
console.log("store: matches=" + st.matches.length + " identities=" + Object.keys(st.identities).length +
  " mutes=" + st.matches.filter(m => m.muted).length);

/* group identities by canon league (skip junk same as packLeagueList) */
const SKIP = { NA: 1, unknown: 1, "loaded team data": 1, "": 1 };
const byLg = {};
const nameKeys = {}; // name -> [identity keys] (dup-pick detector)
Object.keys(st.identities).forEach(k => {
  const it = st.identities[k];
  (nameKeys[it.name] = nameKeys[it.name] || []).push(k);
  (it.leagues || []).forEach(raw => {
    const lg = evX("canonLg(" + JSON.stringify(raw) + ")");
    if (SKIP[lg]) return;
    (byLg[lg] = byLg[lg] || []).push({ name: it.name, country: it.country || "?" });
  });
});
// dedupe by name within league (ordering preserved)
Object.keys(byLg).forEach(lg => {
  const seen = {}, out = [];
  byLg[lg].forEach(t => { if (!seen[t.name]) { seen[t.name] = 1; out.push(t); } });
  byLg[lg] = out;
});
// realistic pick: R if the MODEL has a rated row for this league+name, else B
function pickValue(lg, t) {
  const rated = evX("(MODEL.teams[" + JSON.stringify(lg) + "]||{})[" + JSON.stringify(t.name) + "] ? 1 : 0");
  return rated ? ("R|" + lg + "|" + t.name) : ("B|" + t.country + "|" + t.name);
}

function classify(outH, flipH) {
  if (outH.indexOf("home rating") !== -1) return "DOMESTIC";
  if (outH.indexOf("Standard stats — evidence model.") !== -1) return "LEAGUE-STD";
  if (outH.indexOf("Team form — standalone.") !== -1) return "LEAGUE-STD(standalone-form)";
  if (outH.indexOf("Team form — no data.") !== -1) return "LEAGUE-STD(no-data-ghost)";
  if (outH.indexOf("Pitch rating —") !== -1) return "LEAGUE-STD(unspecified)";
  if (outH.indexOf("Dixon") !== -1 || outH.indexOf("cross-league") !== -1 && outH.indexOf("home rating") !== -1) return "CROSS-DC?";
  if (outH.indexOf("Dixon-Coles bridge") !== -1 || outH.indexOf("cross-league bridge") !== -1) return "CROSS-DC";
  if (outH.indexOf("Evidence verdict") !== -1) return "EVID-X";
  if (outH.indexOf("NO CALL — identity unresolved") !== -1) return "UNRESOLVED";
  if (outH.indexOf("ban-err") !== -1) return "ERR";
  return "OTHER";
}

console.log("\nleague | teams | sample fixture -> path");
const rows = [];
Object.keys(byLg).sort().forEach(lg => {
  const ts = byLg[lg];
  if (ts.length < 2) { rows.push([lg, ts.length, "(single team — no intra-league fixture)", "-"]); return; }
  const h = ts[0], a = ts[1];
  S.document.getElementById("result").innerHTML = "";
  S.document.getElementById("flipBox").innerHTML = "";
  S.document.getElementById("homeTeam").value = pickValue(lg, h);
  S.document.getElementById("awayTeam").value = pickValue(lg, a);
  let err = "";
  try { S.renderRate(); } catch (e) { err = String(e).split("\n")[0]; }
  const outH = S.document.getElementById("result").innerHTML;
  const path = err ? ("THROW: " + err) : classify(outH, S.document.getElementById("flipBox").innerHTML);
  const kinds = pickValue(lg, h).split("|")[0] + "+" + pickValue(lg, a).split("|")[0];
  rows.push([lg, ts.length, h.name + " v " + a.name + " [" + kinds + "]", path]);
});
rows.forEach(r => console.log(r[0] + " | " + r[1] + " | " + r[2] + " -> " + r[3]));

/* league-membership detail for pack leagues: which names are R vs which are B */
console.log("\npack-league R-coverage detail (names offered as R within MODEL leagues; '-' = B-loaded):");
["SC0","RPL","FNL","CZ1","CZ2","SC1","KOS","ALB","DEN","IRL","MLS","USL","USL1"].forEach(lg => {
  const ts = byLg[lg] || [];
  const r = ts.filter(t => pickValue(lg, t)[0] === "R").map(t => t.name);
  const b = ts.filter(t => pickValue(lg, t)[0] === "B").map(t => t.name);
  console.log(lg + ": R=" + r.length + " B=" + b.length + (b.length ? "  B-names: " + b.join(", ") : ""));
});

/* duplicate display names across identity keys (dup-pick class) */
console.log("\nduplicate display names (same name, >1 identity key):");
Object.keys(nameKeys).filter(n => nameKeys[n].length > 1).forEach(n => {
  const lgs = nameKeys[n].map(k => (st.identities[k].leagues || []).join("/") + " @" + (st.identities[k].country || "?"));
  console.log("  " + n + " x" + nameKeys[n].length + "  [" + lgs.join(" | ") + "]");
});

/* also probe one R+R model-league fixture (control) */
S.document.getElementById("result").innerHTML = "";
S.document.getElementById("homeTeam").value = "R|E0|Chelsea";
S.document.getElementById("awayTeam").value = "R|E0|Bournemouth";
S.renderRate();
console.log("\ncontrol R|E0 Chelsea v Bournemouth -> " + classify(S.document.getElementById("result").innerHTML, ""));
