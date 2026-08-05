/* concat_test.js — does ONE combined/pasted block of all three packs yield the
   same store as three sequential Validate cycles? Proves the multi-paste path. */
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
function boot() {
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
  return { sandbox, evX: (e) => vm.runInContext(e, sandbox) };
}

const hib = fs.readFileSync("/home/user/packs/hibernian-team-pack.txt", "utf8");
const mal = fs.readFileSync("/home/user/packs/malisheva-team-pack.txt", "utf8");
const clo = fs.readFileSync("/home/user/packs/malisheva-closure-pack.txt", "utf8");

function fingerprints(S) {
  return S.BlueprintEmbed.store().matches
    .map(m => [m.date, m.competition, m.homeId, m.awayId, m.hg, m.ag, m.venue || "normal"].join("|"))
    .sort().join("\n");
}

/* A: combined single block, one Validate */
const A = boot();
A.sandbox.document.getElementById("bpImportText").value = hib + "\n" + mal + "\n" + clo;
A.evX("BlueprintEmbed.importData()");
const repA = A.sandbox.document.getElementById("bpImportReport").innerHTML;

/* B: three sequential Validate cycles */
const B = boot();
[hib, mal, clo].forEach(p => { B.sandbox.document.getElementById("bpImportText").value = p; B.evX("BlueprintEmbed.importData()"); });

const mA = A.sandbox.BlueprintEmbed.store().matches.length;
const mB = B.sandbox.BlueprintEmbed.store().matches.length;
const blocked = /ban-err/.test(repA);
console.log("combined single-validate rows:", mA, "| sequential rows:", mB);
console.log("combined blocked by errors:", blocked);
console.log("fingerprints identical:", fingerprints(A.sandbox) === fingerprints(B.sandbox));
console.log("61 rows both:", mA === 61 && mB === 61);
process.exit((mA === 61 && mB === 61 && fingerprints(A.sandbox) === fingerprints(B.sandbox) && !blocked) ? 0 : 1);
