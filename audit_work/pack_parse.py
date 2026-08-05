#!/usr/bin/env python3
"""Independent BP-TEAM-PACK v2 parser + store comparison (auditor-owned, fresh)."""
import json, sys, re, collections

def parse_pack(path):
    """Parse a BP-TEAM-PACK v2 .txt. Returns dict of lists: matches, teams, notes, sources."""
    out = {"matches": [], "teams": [], "notes": [], "sources": []}
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        parts = [p.strip() for p in line.split("|")]
        kind = parts[0]
        if kind == "MATCH":
            # MATCH|date|comp|compType|home|hg|ag|away|venueType|stadium|city|country|sourceId|[tieId]
            m = {
                "dateISO": parts[1],
                "competitionName": parts[2],
                "compType": parts[3],
                "homeName": parts[4],
                "homeGoals": int(parts[5]),
                "awayGoals": int(parts[6]),
                "awayName": parts[7],
                "venueType": parts[8] if len(parts) > 8 else "",
                "stadium": parts[9] if len(parts) > 9 else "",
                "city": parts[10] if len(parts) > 10 else "",
                "country": parts[11] if len(parts) > 11 else "",
                "tieId": parts[12] if len(parts) > 12 else None,
                "sourceId": parts[13] if len(parts) > 13 else "",
            }
            out["matches"].append(m)
        elif kind == "TEAM":
            out["teams"].append(parts)
        elif kind == "NOTE":
            out["notes"].append("|".join(parts[1:]))
        elif kind == "SOURCE":
            out["sources"].append(parts)
        elif kind in ("END", "PITCH-RATING"):
            pass
        else:
            # multi-line NOTE continuation (NOTE|info|...\n continuation lines)
            if kind.startswith("NOTE"):
                pass
            else:
                out["notes"].append("UNPARSED|" + line)
        i += 1
    return out

def fingerprint(m, norm_home=None, norm_away=None):
    h = (norm_home or m["homeName"]).strip().lower()
    a = (norm_away or m["awayName"]).strip().lower()
    return (m["dateISO"], h, a, m["competitionName"])

def load_store(path):
    with open(path) as f:
        data = json.load(f)
    return data["store"]

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    packs = {
        "EPL": "EPL-2021-2026.txt",
        "CZ1": "CZ1-2021-2026.txt",
        "MOLCUP120": "MOLCUP-2021-2026.txt",
        "RPL": "RPL-2021-2026.txt",
        "RUSCUP": "RUSCUP-2021-2026.txt",
        "ADDENDUM": "RUS-ADDENDUM-2026.txt",
    }
    for key, fn in packs.items():
        p = parse_pack(f"{base}/{fn}")
        print(f"{key}: {len(p['matches'])} MATCH | {len(p['teams'])} TEAM | {len(p['notes'])} NOTE | {len(p['sources'])} SOURCE")
        # internal duplicate check
        fps = [fingerprint(m) for m in p["matches"]]
        dups = [k for k, v in collections.Counter(fps).items() if v > 1]
        if dups:
            print(f"  !! internal duplicate fingerprints: {len(dups)}")
            for d in dups[:5]:
                print("   ", d)
        # date sanity
        dates = [m["dateISO"] for m in p["matches"]]
        print(f"  date range: {min(dates)} .. {max(dates)} | future(>2026-08-05): {sum(1 for d in dates if d > '2026-08-05')}")
