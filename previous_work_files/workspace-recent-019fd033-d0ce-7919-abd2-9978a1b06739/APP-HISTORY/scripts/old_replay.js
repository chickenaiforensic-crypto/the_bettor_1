/* old_replay.js — masked-replay backtest of the OLD match-audit tool's verdict
   engine on the identical 61-matched masked sample as replay_test.js.
   The old computeVerdict() source is extracted UNMODIFIED from
   uploads/match-audit-tool.html and executed here; only its input fields are
   filled, via the pre-registered deterministic mapping (see header of reply).
   Old-app inputs (answers to its own question sections) come strictly from the
   same masked store: cutoff = match date hides the game + everything after. */
const fs = require("fs");
const vm = require("vm");

/* ---------- extract old-app machinery verbatim ---------- */
const oldHtml = fs.readFileSync("/home/user/uploads/match-audit-tool.html", "utf8");
function slice(src, startMark, endMark) {
  const i = src.indexOf(startMark), j = src.indexOf(endMark, i);
  if (i === -1 || j === -1) throw new Error("extraction anchors missing: " + startMark);
  return src.slice(i, j);
}
const subscalesCode = slice(oldHtml, "const SUBSCALES = [", "];\n\nlet state") + "];\n";
const levelsCode = slice(oldHtml, "const LEVELS = [", "];\n\nconst NO_DATA") + "];\n";
const helpersCode = "const NO_DATA = 'no-data';\n" +
  slice(oldHtml, "function sigmoid(", "function badgeClass") +
  "function badgeClass(t){return '';}\n";
const computeCode = slice(oldHtml, "function computeVerdict() {", "\nfunction renderVerdict(");

/* ---------- boot current app to access the masked store ---------- */
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(pos, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, scrollIntoView() {}, setAttribute() {}, getAttribute() { return null; },
    addEventListener() {}, parentNode: null };
}
const els = {}; const sandbox = {};
sandbox.window = sandbox; sandbox.console = console; sandbox.navigator = {};
sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const _store = {};
sandbox.localStorage = { getItem: k => (k in _store ? _store[k] : null), setItem: (k, v) => { _store[k] = String(v); }, removeItem: k => { delete _store[k]; } };
const md = makeEl("matchDate");
md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = md;
sandbox.document = { readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(tag) { return makeEl(tag + ":" + Math.random()); },
  querySelector(sel) { if (!els["q:" + sel]) els["q:" + sel] = makeEl(sel); return els["q:" + sel]; },
  querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sandbox);
scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "script" + i + ".js" }));
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  sandbox.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  vm.runInContext("BlueprintEmbed.importData()", sandbox);
});
const store = sandbox.BlueprintEmbed.store();
const ids = store.identities;
const nameOf = (id) => (ids[id] && ids[id].name) || id;

/* ---------- masked-store helpers (cutoff-disciplined) ---------- */
const matches = store.matches.slice().sort((a, b) => a.date.localeCompare(b.date));
function gdOf(homeId, awayId, hg, ag, fromId) { return fromId === homeId ? hg - ag : ag - hg; }
function meetings(idA, idB, cutoff) { return matches.filter(m => m.date < cutoff && ((m.homeId === idA && m.awayId === idB) || (m.homeId === idB && m.awayId === idA))); }
function avgGdTowards(teamId, oppId, cutoff) {
  const ms = meetings(teamId, oppId, cutoff);
  if (!ms.length) return null;
  return ms.reduce((s, m) => s + gdOf(m.homeId, m.awayId, m.hg, m.ag, teamId), 0) / ms.length;
}
function gamesOf(teamId, cutoff, compFilter) {
  return matches.filter(m => m.date < cutoff && (m.homeId === teamId || m.awayId === teamId) && (!compFilter || m.competition === compFilter));
}
function lvl5(diffOrAvg, strong, favor) {
  if (diffOrAvg >= strong) return "2"; if (diffOrAvg >= favor) return "1";
  if (diffOrAvg > -favor && diffOrAvg < favor) return "0";
  if (diffOrAvg > -strong) return "-1"; return "-2";
}

/* ---------- pre-registered field mapping ---------- */
function oldFields(A, B, cutoff) {
  const f = {};
  /* HEAD_TO_HEAD */
  const h2h = avgGdTowards(A, B, cutoff);
  f.headToHead = h2h === null ? "no-data" : lvl5(h2h, 1.0, 0.3);
  /* COMMON_OPPONENT + SHARED_COUNT */
  const oppA = new Set(), oppB = new Set();
  gamesOf(A, cutoff).forEach(m => oppA.add(m.homeId === A ? m.awayId : m.homeId));
  gamesOf(B, cutoff).forEach(m => oppB.add(m.homeId === B ? m.awayId : m.homeId));
  const shared = [...oppA].filter(x => oppB.has(x) && x !== A && x !== B)
    .map(x => avgGdTowards(A, x, cutoff) - avgGdTowards(B, x, cutoff))
    .filter(v => isFinite(v));
  f.sharedCount = shared.length === 0 ? "0" : shared.length === 1 ? "1" : shared.length <= 3 ? "2-3" : "4+";
  f.commonOpponent = !shared.length ? "no-data" : lvl5(shared.reduce((a, b) => a + b, 0) / shared.length, 1.0, 0.3);
  /* CURRENT_FORM: same competition string, min 3 per side */
  const compOf = matches.find(m => ((m.homeId === A && m.awayId === B) || (m.homeId === B && m.awayId === A)) && m.date >= cutoff) || null;
  const comp = compOf ? compOf.competition : null;
  const curGd = (t) => { const g = gamesOf(t, cutoff, comp); if (g.length < 3) return null; return g.reduce((s, m) => s + gdOf(m.homeId, m.awayId, m.hg, m.ag, t), 0) / g.length; };
  const ca = curGd(A), cb = curGd(B);
  f.currentForm = (ca === null || cb === null) ? "no-data" : lvl5(ca - cb, 0.75, 0.25);
  /* RECENT_FORM: last 8 all comps, points per game */
  const ppg = (t) => { const g = gamesOf(t, cutoff).slice(-8); if (g.length < 3) return null; return g.reduce((s, m) => { const d = gdOf(m.homeId, m.awayId, m.hg, m.ag, t); return s + (d > 0 ? 3 : d === 0 ? 1 : 0); }, 0) / g.length; };
  const pa = ppg(A), pb = ppg(B);
  f.recentForm = (pa === null || pb === null) ? "no-data" : lvl5(pa - pb, 1.0, 0.5);
  /* CONDITIONS_FIT: A is home by construction; relocated venue cancels it */
  const mRel = compOf && compOf.venue === "relocated";
  f.conditionsFit = mRel ? "0" : "1";
  /* fixed honest defaults */
  f.sharedCountFixed = f.sharedCount;
  return f;
}

/* ---------- old-app runtime ---------- */
let captured = null;
const oldCtx = {
  console, Math, JSON,
  SUBSCALES: null, LEVELS: null,
  getNames: null, todayISO: () => "2099-01-01",
  pickedGameDate: null,
  saveLogEntry: (v) => { captured = v; },
  renderVerdict: () => {},
  document: null,
};
vm.createContext(oldCtx);
const elsOld = {};
oldCtx.document = { getElementById: (id) => { if (!elsOld[id]) elsOld[id] = makeEl(id); return elsOld[id]; } };
vm.runInContext(levelsCode + "\n" + subscalesCode + "\n" + helpersCode + "\n" + computeCode, oldCtx);

function setOldEls(f, A, B, Aname, Bname, compName) {
  const set = (id, v) => { const el = elsOld[id] || (elsOld[id] = makeEl(id)); el.value = v; return el; };
  const setCk = (id, v) => { const el = elsOld[id] || (elsOld[id] = makeEl(id)); el.checked = v; return el; };
  ["commonOpponent", "currentForm", "recentForm", "conditionsFit", "headToHead"].forEach(k => set("sub_" + k, f[k]));
  set("sharedCount", f.sharedCount); set("qualityProxy", "not-applicable");
  set("baseline", "no-signal"); set("resilience", "neutral");
  setCk("anomalyA", false); setCk("anomalyB", false); setCk("availabilityA", false); setCk("availabilityB", false);
  set("oddsA", ""); set("oddsB", ""); set("oddsDraw", "");
  set("tournament", compName || "");
  oldCtx.getNames = () => ({ sport: "football", A: Aname, B: Bname });
}

/* ---------- replay all 61 ---------- */
const rows = [];
const stat = { total: 0, abstain: 0, hit: 0, miss: 0 };
const tiers = {};
matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  stat.total++;
  const f = oldFields(m.homeId, m.awayId, m.date);
  setOldEls(f, m.homeId, m.awayId, nameOf(m.homeId), nameOf(m.awayId), m.competition);
  captured = null;
  vm.runInContext("computeVerdict()", oldCtx);
  const v = captured;
  if (!v) { rows.push([m.date, nameOf(m.homeId) + " v " + nameOf(m.awayId), "ERROR", "-", actual, "no verdict"]); return; }
  tiers[v.tier] = (tiers[v.tier] || 0) + 1;
  const dir = v.leader === "A" ? "H" : v.leader === "B" ? "A" : "N";
  let verdict;
  if (v.tier === "PASS" || v.tier === "INSUFFICIENT_DATA" || v.tier === "TIDE_MATCH") { stat.abstain++; verdict = "abstain (" + v.tier + ")"; }
  else if (dir === actual) { stat.hit++; verdict = "HIT"; }
  else if (actual === "D") { stat.miss++; verdict = "MISS (draw: loss by settle rule)"; }
  else { stat.miss++; verdict = "MISS"; }
  const subs = ["commonOpponent:" + f.commonOpponent, "currentForm:" + f.currentForm, "recentForm:" + f.recentForm, "headToHead:" + f.headToHead, "cond:" + f.conditionsFit, "shared:" + f.sharedCount].join(" ");
  rows.push([m.date, nameOf(m.homeId) + " v " + nameOf(m.awayId), v.tier, dir + " p=" + (v.probA !== null && v.probA !== undefined ? v.probA.toFixed(2) : "-"), actual, verdict + "  [" + subs + "]"]);
});

console.log("date       | fixture | tier | lean | actual | verdict [subscale values]");
rows.forEach(r => console.log(r.join(" | ")));
console.log("\n=== OLD APP aggregate (masked, identical 61-game sample) ===");
console.log("replayed:", stat.total, "| abstain (PASS/INSUFFICIENT/TIDE):", stat.abstain, "| directional:", stat.hit + stat.miss, "| hit:", stat.hit, "| miss:", stat.miss);
const dir = stat.hit + stat.miss;
console.log("directional accuracy (excl abstain):", dir ? (100 * stat.hit / dir).toFixed(1) + "% of " + dir : "n/a");
console.log("tier distribution:", JSON.stringify(tiers));
