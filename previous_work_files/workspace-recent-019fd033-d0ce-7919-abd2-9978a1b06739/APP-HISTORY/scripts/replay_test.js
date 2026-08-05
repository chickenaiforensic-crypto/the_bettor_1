/* replay_test.js — masked-replay backtest of the evidence engine.
   Every completed match in the store is replayed blind: cutoff = match date
   (beforeCutoff m.date < cutoff hides the game itself and everything after).
   Scores, per phase and aggregate, are compared to the actual result. */
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);

function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "", style: {},
    checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(pos, h) { this.innerHTML += h; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    focus() {}, select() {}, click() {}, setAttribute() {}, getAttribute() { return null; },
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
const S = sandbox, evX = (e) => vm.runInContext(e, sandbox);

/* load the three packs (same state as the verified 61-row store) */
["hibernian-team-pack", "malisheva-team-pack", "malisheva-closure-pack"].forEach(p => {
  S.document.getElementById("bpImportText").value = fs.readFileSync("/home/user/packs/" + p + ".txt", "utf8");
  evX("BlueprintEmbed.importData()");
});

const store = S.BlueprintEmbed.store();
const ids = store.identities;
const nameOf = (id) => (ids[id] && ids[id].name) || id;
const matches = store.matches.slice().sort((a, b) => a.date.localeCompare(b.date));

function phaseDir(sumW, sumE) {
  /* direction from weighted mean estimate: >0.25 home, <-0.25 away, else neutral */
  if (!sumW) return "none";
  const m = sumE / sumW;
  return m > 0.25 ? "H" : m < -0.25 ? "A" : "N";
}

const rows = [];
const stat = { total: 0, hit: 0, miss: 0, neutral: 0, nocall: 0, leanhit: 0, leanmiss: 0 };
const phaseStats = { h2h: {n:0,hit:0}, common: {n:0,hit:0}, third: {n:0,hit:0} };

matches.forEach(m => {
  if (!m.homeId || !m.awayId || m.homeId === m.awayId) return;
  const ev = S.BlueprintEmbed.analyze(m.homeId, m.awayId, m.date);
  const actual = m.hg > m.ag ? "H" : m.hg < m.ag ? "A" : "D";
  stat.total++;
  if (!ev.ag) { stat.nocall++; rows.push([m.date, nameOf(m.homeId) + " v " + nameOf(m.awayId), "NO CALL", "-", "-", actual, "no evidence (discipline)"]); return; }
  /* aggregate direction */
  const aggDir = ev.ag.weighted > 0.25 ? "H" : ev.ag.weighted < -0.25 ? "A" : "N";
  let verdict;
  if (aggDir === "N") { stat.neutral++; verdict = "neutral/abstain"; }
  else if (aggDir === actual) { stat.hit++; verdict = "HIT"; if (ev.cl.label !== "NO CALL") stat.leanhit++; }
  else if (actual === "D") { stat.miss++; verdict = "MISS (draw: settle rule = loss)"; stat.leanmiss++; }
  else { stat.miss++; verdict = "MISS"; stat.leanmiss++; }
  /* per-phase sections (superpowers individually) */
  const ph = { h2h: [0, 0], common: [0, 0], third: [0, 0] };
  ev.paths.forEach(p => { const g = ph[p.phase]; if (g) { g[0] += p.weight; g[1] += p.weight * p.estimate; } });
  const sec = [];
  ["h2h", "common", "third"].forEach(k => {
    const d = phaseDir(ph[k][0], ph[k][1]);
    if (d === "none") return;
    phaseStats[k].n++;
    if (d === actual) phaseStats[k].hit++;
    sec.push(k + ":" + d + (d === actual ? "✓" : "✗"));
  });
  rows.push([m.date, nameOf(m.homeId) + " v " + nameOf(m.awayId), ev.cl.label, ev.ag.weighted.toFixed(2), String(ev.ag.effective), actual, verdict + "  [" + sec.join(" ") + "]"]);
});

console.log("date       | fixture                              | label                | est    | eff | actual | verdict [sections h2h/common/third ✓hit ✗miss]");
rows.forEach(r => console.log(r.join(" | ")));
console.log("\n=== aggregate ===");
console.log("replayed:", stat.total, "| NO CALL (no evidence):", stat.nocall, "| neutral/abstain:", stat.neutral,
  "| directional hit:", stat.hit, "| miss:", stat.miss);
const dir = stat.hit + stat.miss;
console.log("directional accuracy (excl NO CALL + neutral):", dir ? (100 * stat.hit / dir).toFixed(1) + "% of " + dir : "n/a");
console.log("\n=== superpower sections individually (direction vs actual, phase present games only) ===");
["h2h", "common", "third"].forEach(k => {
  const s = phaseStats[k]; if (s.n) console.log(k, ":", s.hit + "/" + s.n, "=", (100 * s.hit / s.n).toFixed(0) + "%");
});
