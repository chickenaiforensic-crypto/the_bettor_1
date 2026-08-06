#!/usr/bin/env python3
"""B0 evidence — packages handoff deliverables and writes
handoffs/B0-EVIDENCE-2026-08-05.json. Deterministic re-derivation:
b64 of the built app, md5 pre/post with decode round-trip, full gate tables.
Run AFTER build_b0.py and b0_selfcheck.js.
"""
import base64, hashlib, json, pathlib, subprocess, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "builder/app-v3.7.0-b0.html"
BASE = ROOT / "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/APP-V3.6.3/app-v3.6.3.html"
STORE5082 = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json"
HAND = ROOT / "handoffs"

def md5b(b): return hashlib.md5(b).hexdigest()
def shab(b): return hashlib.sha256(b).hexdigest()

built = APP.read_bytes()
pre_md5, pre_sha = md5b(built), shab(built)

# ---- b64 handoff file (76-col wrap, canonical) ----
b64 = base64.b64encode(built).decode("ascii")
lines = [b64[i:i+76] for i in range(0, len(b64), 76)]
b64_txt = "\n".join(lines) + "\n"
b64_name = f"B0-v3.7.0-{pre_md5[:8]}.b64.txt"
b64_path = HAND / b64_name
b64_path.write_text(b64_txt, encoding="ascii")
b64_md5 = md5b(b64_path.read_bytes())
decoded = base64.b64decode(b64_txt)
roundtrip_ok = md5b(decoded) == pre_md5 and decoded == built

# ---- artifact example: exactly what the app stores in store.artifacts ----
NODE_DUMP = r'''
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync('builder/app-v3.7.0-b0.html','utf8');
const m=html.match(/\/\* ==== calibration\.js ==== \*\/[\s\S]*?\n\}\)\(\);\n/)[0];
const s={}; s.window=s; vm.createContext(s); vm.runInContext(m,s);
const store=JSON.parse(fs.readFileSync(process.argv[1],'utf8')).store;
const res=s.window.PR.calibration.run(store);
console.log(JSON.stringify(res));
'''
dump = subprocess.run(
    ["node", "-e", NODE_DUMP, STORE5082], cwd=ROOT, capture_output=True, text=True, timeout=600)
assert dump.returncode == 0, dump.stderr[:500]
run_data = json.loads(dump.stdout)
artifact_example = {
    "shape": "as stored in store.artifacts by the app's Run test-run ladder button (id assigned by STORE.nextId at run time)",
    "kind": "calibration-run", "version": run_data["module"].split()[-1],
    "generatedAt": run_data["generatedAt"], "note": run_data["summary"],
    "data": run_data
}

# ---- gate tables ----
def cnt(pat, text): return len(re.findall(pat, text))
base_txt = BASE.read_text(encoding="utf-8"); new_txt = APP.read_text(encoding="utf-8")
mod_sec = re.search(r"/\* ==== calibration\.js ==== \*/(.*?)/\* ==== compute\.js ==== \*/", new_txt, re.S).group(1)
greps = {
    "fetch (code call)":        {"pat": r"\bfetch\s*\(", },
    "XMLHttpRequest":           {"pat": r"XMLHttpRequest"},
    "odds (case-insensitive)":  {"pat": r"(?i)odds"},
    "http":                     {"pat": r"http"},
    "<script src":              {"pat": r"<script[^>]+src"},
    "import(" :                 {"pat": r"import\s*\("},
}
grep_table = {}
for k, g in greps.items():
    cb, cn, cm = cnt(g["pat"], base_txt), cnt(g["pat"], new_txt), cnt(g["pat"], mod_sec)
    grep_table[k] = {"baseline_app_v3.6.3": cb, "built_app_v3.7.0": cn, "inside_new_module": cm,
                     "ok": cn == cb and cm == 0,
                     "note": "baseline matches sit inside embedded seed-pack NOTE/SOURCE text; code-call count 0" if cb else None}
one_gate = {"PR.ingest": {"baseline": cnt(r"PR\.ingest", base_txt), "built": cnt(r"PR\.ingest", new_txt)},
            "PR.ingest.commit": {"baseline": cnt(r"PR\.ingest\.commit", base_txt), "built": cnt(r"PR\.ingest\.commit", new_txt)}}
one_gate["ok"] = one_gate["PR.ingest"]["baseline"] == one_gate["PR.ingest"]["built"] and one_gate["PR.ingest.commit"]["baseline"] == one_gate["PR.ingest.commit"]["built"]

# ---- byte diff stats ----
diff_path = ROOT / "builder/b0_byte_diff.txt"
diff_txt = diff_path.read_text(encoding="utf-8")
hunks = [l for l in diff_txt.splitlines() if re.match(r"^\d", l)]
added = len([l for l in diff_txt.splitlines() if l.startswith(">")])
removed = len([l for l in diff_txt.splitlines() if l.startswith("<")])
byte_diff = {
    "file": "builder/b0_byte_diff.txt", "hunks": hunks,
    "lines_added": added, "lines_removed": removed,
    "intended_edits": [
        "228a229,234 → CSS rules .ladder-tbl/.ladder-note (presentational)",
        "380c386 → APP_VERSION '3.6.3' → '3.7.0' (+B0 comment)",
        "2341a2348,2806 → new module section /* ==== calibration.js ==== */ (PR.calibration, S0)",
        "3518c3983 → artifact kind list: 'calibration-run' registered in Calibration tab",
        "3526c3991,3994 → Calibration tab: test-run ladder section (button + explainer + output div)",
        "3604a4073,4074 → event bindings #btn-ladder / #btn-ladder-dl",
        "3855a4326,4384 → runLadder + downloadLadderArtifact + fmt helpers (ui.js)",
    ],
    "ok": added == 532 and removed == 3 and len(hunks) == 7,
}

selfcheck = json.loads((ROOT / "builder/b0_selfcheck_result.json").read_text())

# ---- t-dist cross-check (fresh Simpson integration, recomputed here) ----
import math
def t_pdf(t, v):
    lg = math.lgamma((v+1)/2) - math.lgamma(v/2)
    return math.exp(lg - 0.5*math.log(v*math.pi) - (v+1)/2*math.log1p(t*t/v))
def p_two(t, v):
    a, b, n = -20.0, abs(t), 100000
    h = (b-a)/n; s = t_pdf(a, v) + t_pdf(b, v)
    for i in range(1, n): s += (4 if i % 2 else 2)*t_pdf(a+i*h, v)
    return 2*(1 - s*h/3)
tdist_xcheck = {
    "method": "independent Simpson integration of the t pdf (fresh code; table points t=2.26216 df=9 → 0.05, t=1.959964 df=1e5 → 0.05 verified)",
    "table_points": {"t=2.26216,df=9": round(p_two(2.26216, 9), 5), "t=1.959964,df=100000": round(p_two(1.959964, 100000), 5)},
    "leagues": {lg: {"t": m["paired"]["t"], "df": m["paired"]["df"],
                     "p_module": m["paired"]["pTwo"], "p_reference": p_two(m["paired"]["t"], m["paired"]["df"]),
                     "abs_diff": abs(m["paired"]["pTwo"] - p_two(m["paired"]["t"], m["paired"]["df"]))}
                for lg, m in selfcheck["fullMetrics"].items()},
}

evidence = {
    "workorder": "WORKORDER-BUILDER-B0-HARNESS (Engine masterplan S0)",
    "date": "2026-08-05",
    "builder": "Arena builder session — branch arena/019fd227-the-bettor-1 (session-fixed; the relay's arena/019fd213 line refers to the Lead Planner's session)",
    "pins_pre": {
        "baseline_app": {"path": "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/APP-V3.6.3/app-v3.6.3.html",
                          "md5": md5b(BASE.read_bytes()), "sha256": shab(BASE.read_bytes()), "bytes": BASE.stat().st_size},
        "store_5082": {"path": STORE5082,
                        "md5": md5b((ROOT/STORE5082).read_bytes()), "sha256": shab((ROOT/STORE5082).read_bytes()),
                        "rows": run_data["storeRows"]},
    },
    "pins_post": {"built_app": {"file": "builder/app-v3.7.0-b0.html", "version": "3.7.0",
                                 "md5": pre_md5, "sha256": pre_sha, "bytes": len(built)}},
    "harness_rerun_gate": {
        "backtest_harness_5000store": open("/tmp/harness_rerun_5000.txt").read().strip().splitlines(),
        "ladder_run_5082store_rerun_artifact_identical": True,
        "note": "python3 audit_work/backtest_harness.py reproduces masterplan §5.2 exactly; python3 audit_work/ladder_run.py on the 5,082 store rewrites ladder_baseline_2026-08-05.json byte-identically (diff empty)",
    },
    "acceptance": {
        "parity_5082_full_last_omitted_season": selfcheck["parity"],
        "ladder_33_rows_vs_baseline_4dp": [c for c in selfcheck["checks"] if c["name"] == "ladder.exact_4dp"][0],
        "bounded_constants_gate": [c for c in selfcheck["checks"] if c["name"].startswith("caps.") or c["name"] == "run.freerun_refusal"],
        "full_metrics_T1_T2_T4_FULL_rows": selfcheck["fullMetrics"],
        "tdist_independent_crosscheck": tdist_xcheck,
    },
    "gates": {
        "byte_diff_vs_baseline": byte_diff,
        "p1_no_market_no_network_greps": {"table": grep_table, "ok": all(g["ok"] for g in grep_table.values())},
        "one_gate_grep": one_gate,
        "harness_rerun": "see harness_rerun_gate",
        "syntax_all_script_blocks": "node --check on all 4 inline <script> blocks: OK (extracted after build)",
        "js_module_harness_parity": {"script": "builder/b0_selfcheck.js", "result_file": "builder/b0_selfcheck_result.json",
                                      "ok": selfcheck["ok"], "summary": selfcheck["summary"]},
    },
    "artifact_example": artifact_example,
    "deliverables": {
        "app_b64": {"file": f"handoffs/{b64_name}", "md5_b64_file": b64_md5,
                     "decoded_md5": md5b(decoded), "roundtrip_md5_matches_pre": roundtrip_ok},
        "evidence": {"file": "handoffs/B0-EVIDENCE-2026-08-05.json"},
        "repo_evidence": ["builder/calibration_module.js", "builder/build_b0.py", "builder/b0_selfcheck.js",
                            "builder/b0_selfcheck_result.json", "builder/b0_byte_diff.txt", "builder/app-v3.7.0-b0.html"],
    },
    "versioning_note": "B0 ships v3.7.0 (policy: every ship bumps upward). Docs that queued 'v3.6.4' for S1/LIVE-DERIVE-01 should re-pin that label to the next bump after 3.7.0 — flagging for the planner, no silent rewrite.",
}

ev_path = HAND / "B0-EVIDENCE-2026-08-05.json"
ev_path.write_text(json.dumps(evidence, indent=1) + "\n", encoding="utf-8")
print("pre  md5 (built app)   :", pre_md5)
print("post md5 (b64 decoded) :", md5b(decoded), "| roundtrip:", roundtrip_ok)
print("b64 file               :", b64_name, "| md5:", b64_md5)
print("evidence md5           :", md5b(ev_path.read_bytes()))
print("all grep gates         :", all(g["ok"] for g in grep_table.values()), "| one-gate:", one_gate["ok"], "| byte-diff ok:", byte_diff["ok"])
