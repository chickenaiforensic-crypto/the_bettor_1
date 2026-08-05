/* validate_packs.js — parse both BP-TEAM-PACKs through the app's real v2 parser,
   then run the Hibernian v Malisheva 2026-07-30 analysis end-to-end. */
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
sandbox.Blob = function () {};
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

/* 1. Hibernian pack through the real parser */
const hibPack = fs.readFileSync("/home/user/packs/hibernian-team-pack.txt", "utf8");
S.document.getElementById("bpImportText").value = hibPack;
evX("BlueprintEmbed.importData()");
const rep1 = S.document.getElementById("bpImportReport").innerHTML;
chk("hib pack not blocked", rep1.indexOf("Load blocked") === -1, rep1.replace(/<[^>]+>/g, " ").slice(0, 160));
chk("hib pack loaded", /Loaded/.test(rep1));
const cnt1 = rep1.match(/(\d+) teams?.*?(\d+) matches?.*?(\d+) sources?/s);
console.log("  report:", rep1.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 240));

/* 2. Malisheva pack through the real parser */
const malPack = fs.readFileSync("/home/user/packs/malisheva-team-pack.txt", "utf8");
S.document.getElementById("bpImportText").value = malPack;
evX("BlueprintEmbed.importData()");
const rep2 = S.document.getElementById("bpImportReport").innerHTML;
chk("mal pack not blocked", rep2.indexOf("Load blocked") === -1, rep2.replace(/<[^>]+>/g, " ").slice(0, 160));
chk("mal pack loaded", /Loaded/.test(rep2));
console.log("  report:", rep2.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 240));

/* 3. analyze() directly — real shape {paths, ag, cl, rows} */
const A = evX(`BlueprintEmbed.analyze(
  BlueprintEmbed.resolve('Hibernian', 'Scotland'),
  BlueprintEmbed.resolve('Malisheva', 'Kosovo'),
  '2026-07-30')`);
chk("analyze returns", !!A);
chk("label Lean only", A && A.cl && A.cl.label === "Lean only", A && A.cl && (A.cl.label + " — " + A.cl.reason));
const h2hP = A ? A.paths.filter(p => p.phase === "h2h") : [];
chk("exactly one h2h path", h2hP.length === 1, "h2h=" + h2hP.length);
chk("h2h estimate -2.0", h2hP.length === 1 && Math.abs(h2hP[0].estimate + 2) < 1e-9, h2hP[0] && h2hP[0].estimate);
chk("no common-opponent paths", A && A.paths.filter(p => p.phase === "common").length === 0);
const phaseCounts = A && A.ag ? A.ag.phaseCounts : {};
console.log("  paths: total=" + (A ? A.paths.length : 0) + " phases=" + JSON.stringify(phaseCounts));
if (A) A.paths.forEach(p => console.log("   [" + p.phase + " w=" + p.weight + " est=" + (typeof p.estimate === "number" ? p.estimate.toFixed(2) : p.estimate) + "] " + p.label.slice(0, 110)));
if (A && A.ag) console.log("  aggregate: weighted=" + A.ag.weighted.toFixed(3) + " agree=" + (A.ag.agree * 100).toFixed(0) + "% effective=" + A.ag.effective + " reused=" + A.ag.reusedChains);

/* 3b. store duplicate audit — no two rows with same date|teams|score */
const dups = evX(`(function(){
  var m=BlueprintEmbed.store().matches, seen={}, out=[];
  m.forEach(function(x){ var k=[x.date,x.homeId,x.awayId,x.hg,x.ag].join('|');
    if(seen[k]) out.push(k); seen[k]=1; }); return {rows:m.length, dups:out}; })()`);
chk("no duplicate match rows in store", dups.dups.length === 0, "rows=" + dups.rows + (dups.dups.length ? " DUPS: " + dups.dups.join("; ") : ""));
chk("resolve single hib identity", !!evX("BlueprintEmbed.resolve('Hibernian','Scotland')"));
chk("resolve single mal identity", !!evX("BlueprintEmbed.resolve('Malisheva','Kosovo')"));

/* 4. resolve idempotence */
chk("resolve idempotent hib", evX("BlueprintEmbed.resolve('Hibernian','Scotland')") === evX("BlueprintEmbed.resolve('Hibernian','Scotland')"));
chk("resolve idempotent mal", evX("BlueprintEmbed.resolve('Malisheva','Kosovo')") === evX("BlueprintEmbed.resolve('Malisheva','Kosovo')"));

/* 5. full Rate-tab render of the cross fixture */
S.document.getElementById("homeTeam").value = "R|SC0|Hibernian";
S.document.getElementById("awayTeam").value = "B|Kosovo|Malisheva";
S.document.getElementById("matchDate").value = "2026-07-30";
const fc = S.document.getElementById("fixtureCompetition");
if (fc.options && !fc.options.length) {
  evX("BlueprintEmbed.refreshTeams && BlueprintEmbed.refreshTeams()");
}
fc.value = "uefa-conference-league";
S.renderRate();
const rr = S.document.getElementById("result").innerHTML;
chk("rate renders evidence card", rr.indexOf("Evidence verdict") !== -1);
chk("rate shows Lean only", rr.indexOf("Lean only") !== -1);
chk("rate shows h2h row", rr.indexOf("Malisheva 2-0 Hibernian") !== -1);
chk("rate shows balance panel", rr.indexOf("home support") !== -1);
chk("rate shows paths table", rr.indexOf("H2H") !== -1);
chk("no fabricated probabilities", rr.indexOf("home rating") === -1);
const le = evX("lastEvidence");
chk("lastEvidence 13 paths (1 h2h + 12 level-3)", le && le.paths.length === 13, le ? le.paths.length + " paths" : "none");
chk("lastEvidence verdict Lean only", le && le.cl && le.cl.label === "Lean only", le && le.cl && le.cl.label);
chk("lastEvidence aggregate -2.00 toward away", le && le.ag && Math.abs(le.ag.weighted + 2) < 1e-9, le && le.ag && le.ag.weighted);
chk("lastEvidence effective paths 1", le && le.ag && le.ag.effective === 1, le && le.ag && le.ag.effective);

/* summary strip — two-pack state (effective 1): independence-bar branch */
chk("summary strip present", rr.indexOf("Balance summary.") !== -1);
chk("summary strip states NO PLAY", rr.indexOf("NO PLAY — no recommendation.") !== -1);
chk("summary strip explains independence bar", rr.indexOf("at least 2 independent routes") !== -1);

console.log("\nRESULT: " + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
