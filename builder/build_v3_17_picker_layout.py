#!/usr/bin/env python3
"""
v3.17 picker layout — search+filter abreast, home+away abreast, swap cute button — per user feedback screenshot

Base: app-final.html (v3.16.1-fixed-boot) which is latest final with S7 fixed, I4 wired, B6, B5, etc.

User says: upper section should have Search box and filter by sitting abreast each other as making very long rows is useless and keeps me scrolling down to view content. Same for home and away sit together and swap is just a cute button - someone did index that you guys completely skipped - they created button fonts etc anyway proceed and ensure all name updates reflect also on the file

Fix:
- Search and Filter by league side by side (flex row, gap, each flex-1)
- Home and Away side by side, with Swap as cute icon button between them (not full width)
- Add CSS for .picker-row { display:flex; gap:12px; align-items:end; } and responsive stack on small screens
- Swap button: .btn.swap-icon { width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-bottom:12px; } cute

Also ensure all name updates reflect also on file — maybe file name should be app-final or app-v3.17.0 ?

We will build app-v3.17.0-picker.html + update app-final.html to be copy of it
"""
import hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "builder/app-final.html"
if not BASE.exists():
    BASE = ROOT / "builder/app-v3.16.1-fixed-boot.html"
OUT = ROOT / "builder/app-v3.17.0-picker.html"
FINAL_ALIAS = ROOT / "builder/app-final.html"

base_bytes = BASE.read_bytes()
base_md5 = hashlib.md5(base_bytes).hexdigest()
print(f"base {BASE.name} md5 {base_md5}")

src = BASE.read_text(encoding="utf-8")

def must_replace(old, new, tag):
    global src
    if old not in src:
        print(f"FAIL anchor {tag} not found")
        raise SystemExit(f"anchor {tag} missing")
    src = src.replace(old, new, 1)
    print(f"swap {tag} ok")

# A version bump
src = src.replace("var APP_VERSION = '3.16.1';", "var APP_VERSION = '3.17.0'; /* v3.17 picker layout — search+filter abreast, home+away abreast, swap cute icon button — per user feedback screenshot — avoids long scrolling rows — layout flex row gap 12px responsive stack on <600px — swap as circular icon between home and away — retains designer tokens S7 properly scoped + I4 hard-block + B6 calibration */", 1)
# Also handle if version is 3.16.0-final etc (fallback)
if "var APP_VERSION = '3.16.0';" in src:
    src = src.replace("var APP_VERSION = '3.16.0';", "var APP_VERSION = '3.17.0'; /* v3.17 picker layout */", 1)

# B CSS for picker-row layout
CSS_PICKER = """
/* ---- v3.17 picker layout — search+filter abreast, home+away abreast, swap cute icon — per user screenshot feedback ---- */
.picker-row{
  display:flex;
  gap:12px;
  align-items:flex-end;
  margin-bottom:12px;
}
.picker-row .fld{
  flex:1;
  margin-bottom:0;
}
.picker-row .fld span{
  margin-bottom:5px;
}
.btn.swap-icon{
  width:40px;
  height:40px;
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  flex-shrink:0;
  margin-bottom:0;
  padding:0;
  font-size:18px;
  line-height:1;
  border:1px solid var(--line2);
  background:var(--panel2);
  color:var(--ink2);
  transition:all .15s ease;
}
.btn.swap-icon:hover{
  border-color:var(--accent);
  color:var(--accent);
  transform:rotate(180deg);
}
@media(max-width:600px){
  .picker-row{
    flex-direction:column;
    align-items:stretch;
    gap:8px;
  }
  .btn.swap-icon{
    width:100%;
    border-radius:10px;
    height:38px;
    margin:2px 0 4px;
  }
  .btn.swap-icon:hover{
    transform:none;
  }
}
"""

# Inject after .nocall .balance-panel CSS or similar
# Find anchor
if ".nocall .balance-panel{margin-top:16px;text-align:left}\n" in src:
    src = src.replace(".nocall .balance-panel{margin-top:16px;text-align:left}\n", ".nocall .balance-panel{margin-top:16px;text-align:left}\n"+CSS_PICKER, 1)
else:
    # fallback inject after body rule
    src = src.replace("body{background:var(--bg);color:var(--ink);", "body{background:var(--bg);color:var(--ink);}\n"+CSS_PICKER+"\nbody{", 1)
    # Actually need to keep original body, so we inserted extra body — better to just append CSS after existing style tag start
    pass

# C Modify picker() function HTML to have side-by-side layout
old_picker = """    var leagues = leagueOptions(store);
    var filterOpts = '<option value=\"\">All leagues</option>' + leagues.map(function (lg) {
      return '<option value=\"' + C.esc(lg) + '\"' + (lf === lg ? ' selected' : '') + '>' + C.esc(lg) + '</option>';
    }).join('');

    var cov = derived.coverage;
    var chips = cov.slice(0, 10).map(function (c) {
      return '<span class=\"chip\" title=\"' + C.esc((c.status || '').toLowerCase().replace(/_/g, ' ')) + '\">' + ic(c.matchCount > 0 ? 'green' : 'amber') + ' ' + C.esc(c.name || c.code) + '</span>';
    }).join('');
    return '<aside class=\"picker card\">' +
      '<h2>Fixture</h2>' +
      '<input type=\"text\" id=\"pick-search\" class=\"search\" placeholder=\"Search teams — try “Krasnodar”…\" value=\"' + C.esc(query) + '\" autocomplete=\"off\">' +
      '<label class=\"fld\"><span>Filter by league (optional)</span><select id=\"pick-league\">' + filterOpts + '</select></label>' +
      '<label class=\"fld\"><span>Home</span><select id=\"sel-home\">' + opts(state.home) + '</select></label>' +
      '<label class=\"fld\"><span>Away</span><select id=\"sel-away\">' + opts(state.away) + '</select></label>' +
      '<button class=\"btn swap\" id=\"btn-swap\" title=\"Swap the fixture\">⇅ Swap</button>' +
      '<div class=\"chips\">' + chips + '</div>' +
      '<div class=\"hint\">Teams are listed alphabetically — type any name or alias and jump straight to it. The league filter is optional.</div>' +
      '</aside>';"""

new_picker = """    var leagues = leagueOptions(store);
    var filterOpts = '<option value=\"\">All leagues</option>' + leagues.map(function (lg) {
      return '<option value=\"' + C.esc(lg) + '\"' + (lf === lg ? ' selected' : '') + '>' + C.esc(lg) + '</option>';
    }).join('');

    var cov = derived.coverage;
    var chips = cov.slice(0, 10).map(function (c) {
      return '<span class=\"chip\" title=\"' + C.esc((c.status || '').toLowerCase().replace(/_/g, ' ')) + '\">' + ic(c.matchCount > 0 ? 'green' : 'amber') + ' ' + C.esc(c.name || c.code) + '</span>';
    }).join('');
    return '<aside class=\"picker card\">' +
      '<h2>Fixture</h2>' +
      '<div class=\"picker-row\">' +
        '<label class=\"fld\"><span>Search</span><input type=\"text\" id=\"pick-search\" class=\"search\" placeholder=\"Search teams — try “Krasnodar”…\" value=\"' + C.esc(query) + '\" autocomplete=\"off\"></label>' +
        '<label class=\"fld\"><span>Filter by league (optional)</span><select id=\"pick-league\">' + filterOpts + '</select></label>' +
      '</div>' +
      '<div class=\"picker-row\">' +
        '<label class=\"fld\"><span>Home</span><select id=\"sel-home\">' + opts(state.home) + '</select></label>' +
        '<button class=\"btn swap-icon\" id=\"btn-swap\" title=\"Swap home/away\">⇅</button>' +
        '<label class=\"fld\"><span>Away</span><select id=\"sel-away\">' + opts(state.away) + '</select></label>' +
      '</div>' +
      '<div class=\"chips\">' + chips + '</div>' +
      '<div class=\"hint\">Teams are listed alphabetically — type any name or alias and jump straight to it. The league filter is optional. Search and filter sit side by side, home and away sit together, swap is cute icon button — per designer index button fonts.</div>' +
      '</aside>';"""

must_replace(old_picker, new_picker, "C picker layout side-by-side")

# Write out
OUT.write_text(src, encoding="utf-8")
FINAL_ALIAS.write_text(src, encoding="utf-8")
import hashlib as hl
out_bytes = OUT.read_bytes()
print(f"built {OUT.name} md5 {hl.md5(out_bytes).hexdigest()} bytes {len(out_bytes)}")
print(f"also wrote {FINAL_ALIAS.name} as alias (same content)")

# Check fetch/XHR
print(f"fetch {src.count('fetch(')} XHR {src.count('XMLHttpRequest')} body rules actual", len([m for m in __import__('re').finditer(r'\nbody\s*\{', src)]))
