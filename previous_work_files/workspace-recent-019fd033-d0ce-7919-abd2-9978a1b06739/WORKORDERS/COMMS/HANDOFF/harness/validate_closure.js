/* validate_closure.js — load all three packs through the app's real parser and
   verify the closed-chain evidence state for Hibernian v Malisheva 2026-07-30. */
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync("/home/user/app-v2.6-cross.html", "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
function makeEl(id) {
  return { id: id || "", value: "", innerHTML: "", textContent: "", className: "",
    style: {}, checked: false, disabled: false, options: [], placeholder: "",
    appendChild() {}, insertBefore() {}, removeChild() {}, remove() {},
    insertAdjacentHTML(p, h) { this.innerHTML += h; }, querySelector() { return null; },
    querySelectorAll() { return []; }, focus() {}, select() {}, click() {},
    setAttribute() {}, getAttribute() { return null; }, addEventListener() {}, parentNode: null };
}
const els = {}; const sandbox = {}; sandbox.window = sandbox; sandbox.console = console;
sandbox.navigator = {}; sandbox.setTimeout = () => 0; sandbox.confirm = () => true;
sandbox.Blob = function () {}; sandbox.FileReader = function () { this.readAsText = function () {}; };
sandbox.URL = { createObjectURL: () => "", revokeObjectURL() {} };
const st = {};
sandbox.localStorage = { getItem: k => (k in st ? st[k] : null), setItem: (k, v) => { st[k] = String(v); }, removeItem: k => { delete st[k]; } };
const md = makeEl("matchDate"); md.parentNode = { parentNode: { insertBefore() {} }, nextSibling: null, insertBefore() {} };
els["matchDate"] = md;
sandbox.document = { readyState: "complete", body: makeEl("body"),
  getElementById(id) { if (!els[id]) els[id] = makeEl(id); return els[id]; },
  createElement(t) { return makeEl(t + Math.random()); },
  querySelector(s) { if (!els["q:" + s]) els["q:" + s] = makeEl(s); return els["q:" + s]; },
  querySelectorAll() { return []; }, addEventListener() {} };
vm.createContext(sandbox);
try { scripts.forEach((s, i) => vm.runInContext(s, sandbox, { filename: "script" + i + ".js" })); }
catch (e) { console.log("BOOT FAILED: " + e.stack); process.exit(1); }
const S = sandbox, evX = x => vm.runInContext(x, sandbox);
let pass = 0, fail = 0;
const chk = (n, ok, d) => { if (ok) { pass++; console.log("  PASS " + n + (d ? " — " + d : "")); } else { fail++; console.log("  FAIL " + n + (d ? " — " + d : "")); } };
const load = p => { S.document.getElementById("bpImportText").value = fs.readFileSync(p, "utf8"); evX("BlueprintEmbed.importData()"); return S.document.getElementById("bpImportReport").innerHTML; };

const r3 = load("/home/user/packs/hibernian-team-pack.txt");
chk("hib+mal baseline ok", r3.indexOf("Load blocked") === -1);
load("/home/user/packs/malisheva-team-pack.txt");
const rc = load("/home/user/packs/malisheva-closure-pack.txt");
chk("closure pack not blocked", rc.indexOf("Load blocked") === -1, rc.replace(/<[^>]+>/g, " ").slice(0, 200));
console.log("  report:", rc.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 260));

const A = evX(`BlueprintEmbed.analyze(
  BlueprintEmbed.resolve('Hibernian', 'Scotland'),
  BlueprintEmbed.resolve('Malisheva', 'Kosovo'), '2026-07-30')`);
chk("analyze returns", !!A);
chk("label still Lean only (cross cap)", A && A.cl && A.cl.label === "Lean only", A && A.cl && (A.cl.label + " — " + A.cl.reason));
chk("reason changed to cross-calibration wording", A && A.cl && /cross-border\/unrated calibration/.test(A.cl.reason), A && A.cl && A.cl.reason);
chk("20 paths (1 h2h + 19 level-3)", A && A.paths.length === 20, A && ("paths=" + A.paths.length));
chk("phase split", A && A.ag && A.ag.phaseCounts.h2h === 1 && A.ag.phaseCounts.common === 0 && A.ag.phaseCounts.third === 19, A && A.ag && JSON.stringify(A.ag.phaseCounts));
chk("effective independent paths = 3", A && A.ag && A.ag.effective === 3, A && A.ag && ("effective=" + A.ag.effective + " reused=" + A.ag.reusedChains));
chk("aggregate ≈ -1.227 (v2.8.6 C7 rebase)", A && A.ag && Math.abs(A.ag.weighted + 1.227) < 0.005, A && A.ag && A.ag.weighted.toFixed(3));
chk("agreement ≈ 64% (v2.8.6 C7 rebase)", A && A.ag && Math.abs(A.ag.agree - 0.636) < 0.02, A && A.ag && ((A.ag.agree * 100).toFixed(1) + "%"));
chk("balance: home 3.0 / away 10.5 / neutral 3.0 (v2.8.6 C7 rebase)", A && A.ag && A.ag.homeW === 3 && A.ag.awayW === 10.5 && A.ag.neuW === 3, A && A.ag && (A.ag.homeW + "/" + A.ag.awayW + "/" + A.ag.neuW));
const dup = evX(`(function(){var m=BlueprintEmbed.store().matches,s={},o=[];m.forEach(function(x){var k=[x.date,x.homeId,x.awayId,x.hg,x.ag].join('|');if(s[k])o.push(k);s[k]=1;});return {n:m.length,d:o};})()`);
chk("no duplicate rows, 61 total", dup.d.length === 0 && dup.n === 61, "rows=" + dup.n + (dup.d.length ? " DUPS:" + dup.d.join(";") : ""));

S.document.getElementById("homeTeam").value = "R|SC0|Hibernian";
S.document.getElementById("awayTeam").value = "B|Kosovo|Malisheva";
S.document.getElementById("matchDate").value = "2026-07-30";
S.renderRate();
const rr = S.document.getElementById("result").innerHTML;
chk("rate renders evidence card", rr.indexOf("Evidence verdict") !== -1);
chk("rate shows Lean only", rr.indexOf("Lean only") !== -1);
chk("rate shows effective independent 3", rr.indexOf("effective independent 3") !== -1);
chk("no fabricated probabilities", rr.indexOf("home rating") === -1);
/* summary strip — closure state (effective 3): cross-calibration branch */
chk("summary strip present", rr.indexOf("Balance summary.") !== -1);
chk("summary strip states NO PLAY", rr.indexOf("NO PLAY — no recommendation.") !== -1);
chk("summary strip explains no-percentage rule", rr.indexOf("no calibrated cross-border table is loaded") !== -1);
console.log("\nRESULT: " + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
