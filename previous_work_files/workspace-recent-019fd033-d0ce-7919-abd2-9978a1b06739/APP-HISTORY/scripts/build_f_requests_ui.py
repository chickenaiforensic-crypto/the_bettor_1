#!/usr/bin/env python3
# Build step F: v2.8.3-cross — executive redesign of the standby request block.
# Collapsed <details> by default, typed request items, [Copy templates] and
# [Download .txt] actions producing an identical formatted request file.
# Display-only (no zone/gate/ladder behavior). Exact-match edits; failures abort.
import sys

SRC = "/home/user/app-v2.6-cross.html"
s = open(SRC, encoding="utf-8").read()
edits = 0

def rep(old, new, count=1, tag=""):
    global s, edits
    n = s.count(old)
    if n != count:
        print("FAIL [%s]: found %d occurrences, expected %d" % (tag, n, count)); sys.exit(1)
    s = s.replace(old, new)
    edits += 1
    print("ok  [%s]" % tag)

# ---------- 1. version strings ----------
rep('v2.8.2-cross</span></h1>', 'v2.8.3-cross</span></h1>', tag="header version")
rep('Pitch Rating v2.8.2-cross &middot; model built 2026-08-01 from match results only',
    'Pitch Rating v2.8.3-cross &middot; model built 2026-08-01 from match results only', tag="footer version")

# ---------- 2. replace the renderer tail with the executive component ----------
old_tail = '''  if (!reqs.length) return "";
  var uniqPre = [...new Set(pre)];
  return '<div class="card"><h2>Standby optional requests (auto-audit)</h2>' +
    '<div class="help">Optional asks only - unanswered, the analysis stands exactly as computed. ' +
    "Conditions answers (CTX lines) are demote-only context and can never raise a zone. " +
    "Results answers (MATCH rows) add evidence. Paste answers on the Data tab (import).</div>" +
    reqs.map(function (r) { return '<div class="kv" style="margin:4px 0 0"><span class="k">request</span><span>' + esc(r) + "</span></div>"; }).join("") +
    (uniqPre.length ? '<div class="help" style="margin:8px 0 2px">Copy-ready answer templates (fill, then paste back):</div>' +
      '<pre class="help" style="white-space:pre-wrap;margin:4px 0 0">' + esc(uniqPre.join("\\\\n")) + "</pre>" : "") +
    "</div>";
}'''
new_tail = '''  if (!reqs.length) return "";
  var uniqPre = [...new Set(pre)];
  function reqType(r) {
    if (/ledger note/i.test(r)) return "LEDGER NOTE";
    if (/conditions|demote-only/i.test(r)) return "CONDITIONS \\u00b7 demote-only";
    if (/MATCH rows/.test(r)) return "RESULTS \\u00b7 adds evidence";
    return "COVERAGE";
  }
  var fixtureLine = hp.name + " v " + ap.name + " \\u00b7 " + cutoff;
  var txt = "PITCH RATING \\u00b7 STANDBY OPTIONAL REQUESTS\\n" + fixtureLine + "\\n\\n" +
    "Unanswered requests change nothing. Conditions answers are demote-only and never\\n" +
    "raise a zone. Results answers add evidence. Paste answers on the Data tab (import).\\n\\n" +
    reqs.map(function (r, i) { return "[" + (i + 1) + "] " + reqType(r) + "\\n" + r; }).join("\\n\\n") +
    (uniqPre.length ? "\\n\\nANSWER TEMPLATES (fill, then paste back):\\n" + uniqPre.join("\\n") : "");
  var domId = "gapreq-" + (++window.__gapReqSeq || (window.__gapReqSeq = 1));
  var fname = ("requests-" + hp.name + "-v-" + ap.name + "-" + cutoff).toLowerCase().replace(/[^a-z0-9]+/g, "-") + ".txt";
  return '<div class="card"><h2>Standby optional requests <span class="help" style="font-weight:400">(' + reqs.length + ")</span></h2>" +
    '<div class="help">Optional gap-spot asks for <b>' + esc(fixtureLine) + "</b>. Unanswered = the analysis stands exactly as computed. " +
    "Conditions answers are demote-only and never raise a zone; results answers add evidence.</div>" +
    '<div style="margin:8px 0 0">' +
      '<button class="btn2" type="button" data-f="' + esc(fname) + '" onclick="gapReqAct(\\'' + domId + '\\',\\'copy\\',this)">Copy templates</button> ' +
      '<button class="btn2" type="button" data-f="' + esc(fname) + '" onclick="gapReqAct(\\'' + domId + '\\',\\'download\\',this)">Download .txt</button>' +
    "</div>" +
    '<details style="margin:8px 0 0"><summary style="cursor:pointer"><b>View all ' + reqs.length + " request" + (reqs.length > 1 ? "s" : "") + " (auto-audit)</b></summary>" +
      reqs.map(function (r, i) {
        return '<div class="kv" style="margin:6px 0 0"><span class="k">' + (i + 1) + " \\u00b7 " + esc(reqType(r)) + "</span><span>" + esc(r) + "</span></div>";
      }).join("") +
      '<div class="help" style="margin:10px 0 2px">Answer file below is identical to the download:</div>' +
      '<pre id="' + domId + '" class="help" style="white-space:pre-wrap;margin:4px 0 0;padding:8px;border:1px solid #e2e8f0;border-radius:6px;background:#f8fafc">' + esc(txt) + "</pre>" +
    "</details></div>";
}
function gapReqAct(domId, mode, btn) {
  var el = document.getElementById(domId);
  if (!el) return;
  var text = el.textContent || "";
  if (mode === "copy") {
    if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text); }
    else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (e) {} ta.remove(); }
    if (btn) { var oldB = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = oldB; }, 1200); }
    return;
  }
  var b = new Blob([text], { type: "text/plain" });
  var u = URL.createObjectURL(b), a = document.createElement("a");
  a.href = u; a.download = (btn && btn.getAttribute("data-f")) || "requests.txt"; a.click();
  setTimeout(function () { URL.revokeObjectURL(u); }, 2000);
}'''
rep(old_tail, new_tail, tag="executive renderer")

open(SRC, "w", encoding="utf-8").write(s)
print("BUILD F complete: %d edits -> v2.8.3-cross (request block UI)" % edits)
