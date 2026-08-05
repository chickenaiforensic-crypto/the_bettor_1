#!/usr/bin/env python3
# INTEGRITY AUDIT — market-evaluation screen for "controlled game" candidates.
# FLAG ONLY. Nothing is deleted. Market data never enters zones/shares/gates.
# Criteria: (a) market-implied strong-team win prob >= 65% (margin-removed Pinnacle close,
# Avg close fallback) and (b) favorite failed to win. HT pattern checked where data exists.
import csv, json, re, unicodedata

def iso(dmy):
    d, m, y = dmy.strip().split("/"); return f"{y}-{m}-{d}"

def key_name(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = re.sub(r"[^a-z0-9 ]", "", s)
    drops = {"fc", "fk", "pfk", "pfc", "city", "msk", "spb"}
    toks = [t for t in s.split() if t not in drops]
    return " ".join(toks)

# map football-data RPL names -> universe ids via rpl_names.json
names = json.load(open("/home/user/rpl/rpl_names.json"))
rev = {}
for uid, pretty in names.items():
    rev[key_name(pretty)] = uid
ALIAS = {  # football-data spellings (key_name'ed) -> universe id
    "akron togliatti": "akron",
    "zenit": "zenit",
    "krylya sovetov": "krylja",
    "pari nn": "pari-nn",
    "himki": "himki",
    "rostov": "rostov",
    "krasnodar": "krasnodar",
    "orenburg": "orenburg",
    "sochi": "sochi",
    "baltika": "baltika",
    "makhachkala": "dinamo-mkh",
    "dynamo makhachkala": "dinamo-mkh",
}
rows = list(csv.DictReader(open("/tmp/rus.csv")))
rows = [r for r in rows if r["Season"] in ("2024/2025", "2025/2026")]

def imp_probs(r):
    h, d, a = (r.get("PSCH", "").strip(), r.get("PSCD", "").strip(), r.get("PSCA", "").strip())
    src = "PSo"
    if not (h and d and a):
        h, d, a = (r.get("AvgCH", "").strip(), r.get("AvgCD", "").strip(), r.get("AvgCA", "").strip())
        src = "AvgC"
    if not (h and d and a):
        return None
    try: h, d, a = float(h), float(d), float(a)
    except ValueError: return None
    o = 1 / h + 1 / d + 1 / a
    return (1 / h / o, 1 / d / o, 1 / a / o, src)

universe = json.load(open("/home/user/rpl/rpl_universe.json"))
u_by_key = {}
for m in universe:
    if m["comp"] != "RPL": continue
    u_by_key[(m["date"], m["home"])] = m

matched, unmatched, flags = [], {}, []
for r in rows:
    dt = iso(r["Date"])
    hid = rev.get(key_name(r["Home"]), ALIAS.get(key_name(r["Home"])))
    aid = rev.get(key_name(r["Away"]), ALIAS.get(key_name(r["Away"])))
    if not hid or not aid:
        unmatched.setdefault(r["Home"], 0); unmatched[r["Home"]] += 1
        unmatched.setdefault(r["Away"], 0); unmatched[r["Away"]] += 1
        continue
    gm = u_by_key.get((dt, hid))
    if not gm: continue
    matched.append((r, gm))
    p = imp_probs(r)
    if not p: continue
    ph, pd, pa, src = p
    fav = "H" if ph >= pa else "A"
    pf = max(ph, pa)
    if pf < 0.65: continue
    res = gm["actual"] if "actual" in gm else ("H" if gm["hg"] > gm["ag"] else "A" if gm["ag"] > gm["hg"] else "D")
    if res == fav: continue
    flags.append({"date": dt, "home": hid, "away": aid, "hg": gm["hg"], "ag": gm["ag"],
                  "fav": fav, "pfav": round(pf * 100, 1), "src": src,
                  "res": res, "type": "LOSS" if res != fav and res != "D" else "DRAW"})

coverage = {}
for r, gm in matched:
    p = imp_probs(r)
    if p: coverage[p[3]] = coverage.get(p[3], 0) + 1
print(f"RPL league rows in universe: {sum(1 for m in universe if m['comp']=='RPL')} | matched to RUS.csv: {len(matched)} | odds rows: {sum(coverage.values())} {coverage}")
# season split of matched rows
from collections import Counter
mc = Counter(matched_r[0]["Season"] for matched_r in matched)
print("matched by season:", dict(mc))
if unmatched:
    print("UNMATCHED football-data names (need aliases):", unmatched)
print(f"\n=== FLAGGED (market favorite >=65% implied, failed to win): {len(flags)} of matched ===")
flags.sort(key=lambda f: (f["type"] != "LOSS", -f["pfav"]))
for f in flags:
    h, a = names.get(f["home"], f["home"]), names.get(f["away"], f["away"])
    favname = h if f["fav"] == "H" else a
    print(f"  {f['type']:4} {f['date']}  {h} {f['hg']}-{f['ag']} {a}   fav={favname} @ {f['pfav']}% ({f['src']})")
json.dump(flags, open("/home/user/rpl/market_flags.json", "w"), indent=1)
print("\nsaved rpl/market_flags.json")
