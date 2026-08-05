"""
PHASE 10 — prediction log with Brier scoring.
Persists every call so it can be scored against the real result later.
Results only. No market data.
"""
import json, os, math

LOG = "/home/user/chain/predictions_log.json"


def _load():
    if os.path.exists(LOG):
        return json.load(open(LOG))
    return []


def _save(rows):
    json.dump(rows, open(LOG, "w"), indent=1)


def record(d, date, note=""):
    """Store one fixture analysis. Idempotent on (fixture, date)."""
    rows = _load()
    key = (d["fixture"], date)
    rows = [r for r in rows if (r["fixture"], r["date"]) != key]
    entry = {
        "fixture": d["fixture"], "date": date, "domain": d["domain"],
        "verdict": d.get("verdict"), "grade": d.get("grade"),
        "tier": d.get("tier", {}).get("name") if d.get("tier") else None,
        "tier_rate": d.get("tier", {}).get("H") if d.get("tier") else None,
        "est": d.get("est"), "sd": d.get("sd"),
        "paths": (d.get("n2", 0) + d.get("n3", 0) + d.get("n4", 0)),
        "H": d.get("H"), "D": d.get("D"), "A": d.get("A"),
        "extrapolated": d.get("extrapolated"),
        "result": None, "note": note,
    }
    rows.append(entry)
    _save(rows)
    return entry


def settle(fixture_substr, date, hg, ag):
    """Attach the real scoreline and Brier-score the call."""
    rows = _load()
    hit = None
    for r in rows:
        if fixture_substr.lower() in r["fixture"].lower() and r["date"] == date:
            hit = r
            break
    if not hit:
        return None
    res = "H" if hg > ag else ("D" if hg == ag else "A")
    hit["result"] = {"hg": hg, "ag": ag, "res": res}
    if hit["H"] is not None:
        y = (1.0 if res == "H" else 0.0, 1.0 if res == "D" else 0.0,
             1.0 if res == "A" else 0.0)
        hit["brier"] = ((hit["H"] - y[0]) ** 2 + (hit["D"] - y[1]) ** 2
                        + (hit["A"] - y[2]) ** 2)
        hit["direction_correct"] = (res != "D") and ((hit["est"] > 0) == (res == "H"))
    _save(rows)
    return hit


def summary():
    rows = [r for r in _load() if r.get("result")]
    if not rows:
        return "no settled predictions yet"
    b = [r["brier"] for r in rows if "brier" in r]
    dec = [r for r in rows if r.get("direction_correct") is not None
           and r["result"]["res"] != "D"]
    hit = sum(1 for r in dec if r["direction_correct"])
    out = [f"settled: {len(rows)}"]
    if b:
        out.append(f"mean Brier: {sum(b)/len(b):.4f}")
    if dec:
        out.append(f"direction: {hit}/{len(dec)} = {hit/len(dec):.1%}")
    return " | ".join(out)
