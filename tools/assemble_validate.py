#!/usr/bin/env python3
"""
the_bettor_1 — RPL backfill: assembly + validation pipeline.

Source : https://www.football-data.co.uk/new/RUS.csv  (retrieved 2026-08-02)
Method : The fetch tool returns the source CSV in fixed ~8000-byte slices
         (chunkIndex 0..50). Slices can split records mid-line. The 5 target
         seasons (2021/2022 .. 2025/2026) are fully covered by slices 32..50,
         stored verbatim in .rawchunks/chunk_32.txt .. chunk_50.txt.
         This script concatenates the slices byte-for-byte, re-splits records,
         validates hard, writes the deliverable CSVs, and computes final
         league tables. NO values are altered, imputed or repaired.

Output : data/rpl/RPL-YYYY-YY.csv  (one per season, verbatim rows + header)
         data/rpl/rpl_all_2021-2026.csv
         audit/validation-report.txt
"""

import csv
import hashlib
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = [ROOT / ".rawchunks" / f"chunk_{i}.txt" for i in range(32, 51)]

HEADER = ["Country", "League", "Season", "Date", "Time", "Home", "Away",
          "HG", "AG", "Res", "PSCH", "PSCD", "PSCA",
          "MaxCH", "MaxCD", "MaxCA", "AvgCH", "AvgCD", "AvgCA"]
TARGET_SEASONS = ["2021/2022", "2022/2023", "2023/2024", "2024/2025", "2025/2026"]
SEASON_FILE = {s: f"RPL-{s[:4]}-{s[7:9]}.csv" for s in TARGET_SEASONS}
EXPECTED_ROWS = {"2021/2022": 244, "2022/2023": 244, "2023/2024": 244,
                 "2024/2025": 240, "2025/2026": 240}

report = []
problems = []


def log(msg=""):
    report.append(msg)
    print(msg)


def fail(msg):
    problems.append(msg)
    log(f"  *** FAIL: {msg}")


def main():
    log("=" * 78)
    log("the_bettor_1 — RPL 2021/22..2025/26  ASSEMBLY & VALIDATION REPORT")
    log("=" * 78)
    log(f"Script : tools/assemble_validate.py")
    log(f"Run    : {__import__('datetime').datetime.now().isoformat(timespec='seconds')}")
    log(f"Input  : .rawchunks/chunk_32.txt .. chunk_50.txt "
        f"(byte slices of https://www.football-data.co.uk/new/RUS.csv retrieved 2026-08-02)")
    log("")

    # ---------------------------------------------------------------- 1. concat
    raw = b""
    for p in CHUNKS:
        data = p.read_bytes()
        log(f"  read {p.name:14s} {len(data):6d} bytes")
        raw += data
    log(f"  total bytes concatenated: {len(raw)}")
    text = raw.decode("utf-8").replace("\r\n", "\n")

    # -------------------------------------------------- 2. record reassembly
    # A genuine record ALWAYS starts with 'Russia,'.  Any split-line fragment
    # that does not start with 'Russia,' is a continuation of the previous
    # record (or, for the very first fragment, belongs to a 2020/2021 row).
    records, buf = [], ""
    for line in text.split("\n"):
        if line.startswith("Russia,"):
            records.append(buf)
            buf = line
        else:
            buf += line
    records.append(buf)
    leading_dropped = [r for r in records if not r.startswith("Russia,")]
    records = [r for r in records if r.startswith("Russia,")]
    log("")
    log("[2] Record reassembly")
    log(f"  reassembled records            : {len(records)}")
    log(f"  non-'Russia' fragments dropped : {len(leading_dropped)} "
        f"(belong to rows before chunk 32 / outside target span; sizes: "
        f"{[len(r) for r in leading_dropped]})")
    if any(len(r) > 90 for r in leading_dropped):
        fail("a dropped non-Russia fragment is > 90 bytes - unexpected")

    # ------------------------------------------------------- 3. field counts
    log("")
    log(f"[3] Field-count check (every record must split into exactly {len(HEADER)} fields)")
    bad = [r for r in records if len(r.split(",")) != len(HEADER)]
    if bad:
        fail(f"{len(bad)} records do not have 20 fields")
        for r in bad[:10]:
            log(f"      BAD({len(r.split(','))}): {r[:120]}")
    else:
        log(f"  PASS - all {len(records)} records have exactly {len(HEADER)} fields")

    # ------------------------------------------------------------- 4. parse
    rows = []
    for r in records:
        f = r.split(",")
        rows.append(dict(zip(HEADER, f)))
    season_counts_all = Counter(r["Season"] for r in rows)
    log("")
    log("[4] Season distribution in assembled text (before filtering):")
    for s in sorted(season_counts_all):
        log(f"      {s}: {season_counts_all[s]}")

    kept = [r for r in rows if r["Season"] in TARGET_SEASONS]
    dropped_out = [r for r in rows if r["Season"] not in TARGET_SEASONS]
    log(f"  kept rows (2021/2022..2025/2026): {len(kept)}")
    log(f"  rows outside target span dropped: {len(dropped_out)} "
        f"(seasons: {sorted(set(r['Season'] for r in dropped_out))})")

    # boundary rows
    log(f"  first kept row: {kept[0]['Season']} {kept[0]['Date']} "
        f"{kept[0]['Home']} {kept[0]['HG']}-{kept[0]['AG']} {kept[0]['Away']}")
    log(f"  last  kept row: {kept[-1]['Season']} {kept[-1]['Date']} "
        f"{kept[-1]['Home']} {kept[-1]['HG']}-{kept[-1]['AG']} {kept[-1]['Away']}")
    if kept[0]["Date"] != "23/07/2021":
        fail("first kept row is not 23/07/2021 (2021/2022 opening round)")
    if kept[-1]["Date"] != "17/05/2026":
        fail("last kept row is not 17/05/2026 (2025/2026 final round)")

    # ------------------------------------------------- 5. per-season checks
    log("")
    log("[5] Per-season structural validation")
    final_tables = {}
    season_notes = {}
    for s in TARGET_SEASONS:
        srows = [r for r in kept if r["Season"] == s]
        log("")
        log(f"  --- Season {s} ---------------------------------------------")
        exp = EXPECTED_ROWS[s]
        log(f"      rows: {len(srows)} (expected {exp})"
            + ("" if len(srows) == exp else "  <-- MISMATCH"))
        if len(srows) != exp:
            fail(f"{s}: row count {len(srows)} != expected {exp}")

        # dates chronological (source order)?
        from datetime import datetime as dt
        dates = [dt.strptime(r["Date"], "%d/%m/%Y") for r in srows]
        if any(dates[i + 1] < dates[i] for i in range(len(dates) - 1)):
            log("      chronology: out-of-order dates (allowed but noted)")
        else:
            log(f"      chronology: non-decreasing {srows[0]['Date']} .. {srows[-1]['Date']}")

        # duplicates
        keys = [(r["Date"], r["Home"], r["Away"]) for r in srows]
        dup = [k for k, c in Counter(keys).items() if c > 1]
        if dup:
            fail(f"{s}: duplicate fixtures {dup[:5]}")

        # scores / results
        n_bad_score = 0
        for r in srows:
            try:
                hg, ag = int(r["HG"]), int(r["AG"])
            except ValueError:
                n_bad_score += 1
                continue
            want = "H" if hg > ag else ("A" if hg < ag else "D")
            if want != r["Res"]:
                n_bad_score += 1
                log(f"      score/result mismatch: {r['Date']} {r['Home']} "
                    f"{r['HG']}-{r['AG']} {r['Away']} Res={r['Res']}")
        log(f"      score/result integrity: {len(srows) - n_bad_score}/{len(srows)} rows OK")
        if n_bad_score:
            fail(f"{s}: {n_bad_score} bad score/result rows")

        # teams: regular league teams have 30 matches (or 32 if they also
        # played the relegation playoff); FNL playoff guests have exactly 2
        apps = Counter()
        for r in srows:
            apps[r["Home"]] += 1
            apps[r["Away"]] += 1
        regular = sorted(t for t, c in apps.items() if c >= 30)
        playoff_rpl = sorted(t for t, c in apps.items() if c == 32)
        playoff_fnl = sorted(t for t, c in apps.items() if c == 2)
        odd = {t: c for t, c in apps.items() if c not in (2, 30, 32)}
        log(f"      league teams (>=30 matches): {len(regular)}")
        if len(regular) != 16:
            fail(f"{s}: expected 16 league teams, got {len(regular)}")
        if playoff_rpl:
            log(f"      relegation-playoff ties in source: {len(playoff_rpl) + len(playoff_fnl)} teams "
                f"(RPL: {playoff_rpl}, FNL guests: {playoff_fnl})")
        reg_league_counts = set(apps[t] for t in regular)
        if not reg_league_counts <= {30, 32}:
            fail(f"{s}: league teams with odd counts {reg_league_counts}")
        if odd:
            fail(f"{s}: teams with unexpected match counts: {odd}")
        expected_total = 16 * 30 + 2 * len(playoff_rpl) + 2 * len(playoff_fnl)
        if sum(apps.values()) != expected_total:
            fail(f"{s}: appearance total {sum(apps.values())} != {expected_total}")

        # odds pattern buckets
        def bucket(r):
            o = [r[k] for k in HEADER[10:]]
            full = all(x != "" for x in o)
            psc_only = all(x != "" for x in o[0:3]) and all(x == "" for x in o[3:])
            maxavg_only = all(x == "" for x in o[0:3]) and all(x != "" for x in o[3:])
            none = all(x == "" for x in o)
            if full: return "full-12"
            if psc_only: return "PSC-only"
            if maxavg_only: return "MaxC/AvgC-only"
            if none: return "no-odds"
            return "PARTIAL!"
        bk = Counter(bucket(r) for r in srows)
        log(f"      odds completeness: {dict(bk)}")
        if bk.get("PARTIAL!"):
            fail(f"{s}: rows with partially-filled odds blocks")
        # numeric check
        n_nonnum = 0
        for r in srows:
            for k in HEADER[10:]:
                if r[k] != "":
                    try: float(r[k])
                    except ValueError:
                        n_nonnum += 1
                        log(f"      non-numeric odds {k}={r[k]!r} on {r['Date']} {r['Home']}-{r['Away']}")
        if n_nonnum:
            fail(f"{s}: {n_nonnum} non-numeric odds cells")

        # MaxCA==22 glitch listing
        glitch = [r for r in srows if r["MaxCA"] == "22"]
        if glitch:
            log(f"      source glitch 'MaxCA=22' rows kept verbatim: {len(glitch)}")
            for r in glitch:
                log(f"        {r['Date']} {r['Home']} v {r['Away']} "
                    f"(MaxC={r['MaxCH']},{r['MaxCD']},{r['MaxCA']} AvgC={r['AvgCH']},{r['AvgCD']},{r['AvgCA']})")

        # -------------------------------------------------- league table
        regset = set(regular)
        table = {t: dict(P=0, W=0, D=0, L=0, GF=0, GA=0) for t in regular}
        h2h = defaultdict(dict)   # (a,b) -> [gf_a, ga_a, pts_a]
        for r in srows:
            h, a = r["Home"], r["Away"]
            if h not in regset or a not in regset:
                continue  # relegation-playoff row
            hg, ag = int(r["HG"]), int(r["AG"])
            th, ta = table[h], table[a]
            th["P"] += 1; ta["P"] += 1
            th["GF"] += hg; th["GA"] += ag
            ta["GF"] += ag; ta["GA"] += hg
            if hg > ag: ph, pa = 3, 0; th["W"] += 1; ta["L"] += 1
            elif hg < ag: ph, pa = 0, 3; th["L"] += 1; ta["W"] += 1
            else: ph = pa = 1; th["D"] += 1; ta["D"] += 1
            g = h2h[(h, a)]; g["pts"] = g.get("pts", 0) + ph
            g["gf"] = g.get("gf", 0) + hg; g["ga"] = g.get("ga", 0) + ag
            g = h2h[(a, h)]; g["pts"] = g.get("pts", 0) + pa
            g["gf"] = g.get("gf", 0) + ag; g["ga"] = g.get("ga", 0) + hg

        # RPL tiebreak chain: pts, H2H pts, H2H GD, H2H GF, wins, GD, GF
        def rank(subset):
            pts = {t: table[t]["W"] * 3 + table[t]["D"] for t in subset}
            base = sorted(subset, key=lambda t: (-pts[t],))
            # group by pts and resolve recursively
            out = []
            i = 0
            while i < len(base):
                j = i
                while j + 1 < len(base) and pts[base[j + 1]] == pts[base[i]]:
                    j += 1
                group = base[i:j + 1]
                if len(group) > 1:
                    # head-to-head sub-table among group
                    hp = {t: 0 for t in group}; hgd = {t: 0 for t in group}; hgf = {t: 0 for t in group}
                    for t in group:
                        for o in group:
                            if t != o and (t, o) in h2h:
                                hp[t] += h2h[(t, o)]["pts"]
                                hgd[t] += h2h[(t, o)]["gf"] - h2h[(t, o)]["ga"]
                                hgf[t] += h2h[(t, o)]["gf"]
                    group = sorted(group, key=lambda t: (
                        -hp[t], -hgd[t], -hgf[t], -table[t]["W"],
                        -(table[t]["GF"] - table[t]["GA"]), -table[t]["GF"], t))
                out.extend(group)
                i = j + 1
            return out

        order = rank(regular)
        tbl = []
        for pos, t in enumerate(order, 1):
            d = table[t]
            pts = d["W"] * 3 + d["D"]
            tbl.append([pos, t, d["P"], d["W"], d["D"], d["L"],
                        d["GF"], d["GA"], d["GF"] - d["GA"], pts])
        final_tables[s] = tbl
        season_notes[s] = dict(rows=len(srows), buckets=dict(bk),
                               playoff_rpl=playoff_rpl, playoff_fnl=playoff_fnl)

        log(f"      final table (regular season, 3-1-0):")
        log(f"        {'#':>2} {'Team':<20} {'P':>2} {'W':>2} {'D':>2} {'L':>2} "
            f"{'GF':>3} {'GA':>3} {'GD':>4} {'Pts':>3}")
        for row in tbl:
            log(f"        {row[0]:>2} {row[1]:<20} {row[2]:>2} {row[3]:>2} "
                f"{row[4]:>2} {row[5]:>2} {row[6]:>3} {row[7]:>3} {row[8]:>4} {row[9]:>3}")
        checksum = sum(r[9] for r in tbl)
        log(f"      points checksum: {checksum}")
        if checksum <= 0:
            fail(f"{s}: nonsense points total")
        if any(r[2] != 30 for r in tbl):
            fail(f"{s}: not all table rows show 30 played")
        if sum(r[3] + r[4] + r[5] for r in tbl) != 16 * 30:
            fail(f"{s}: W+D+L total mismatch")
        if sum(r[3] for r in tbl) != sum(r[5] for r in tbl):
            fail(f"{s}: total wins != total losses")

    # ------------------------------------------------------- 6. write CSVs
    log("")
    log("[6] Deliverable CSV files (rows verbatim, header added)")
    outdir = ROOT / "data" / "rpl"
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for s in TARGET_SEASONS:
        p = outdir / SEASON_FILE[s]
        body = io.StringIO()
        w = csv.writer(body, lineterminator="\n")
        w.writerow(HEADER)
        for r in kept:
            if r["Season"] == s:
                w.writerow([r[k] for k in HEADER])
        p.write_text(body.getvalue(), encoding="utf-8")
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        written.append((str(p.relative_to(ROOT)), len(body.getvalue().splitlines()) - 1, sha))
    p = outdir / "rpl_all_2021-2026.csv"
    body = io.StringIO()
    w = csv.writer(body, lineterminator="\n")
    w.writerow(HEADER)
    for r in kept:
        w.writerow([r[k] for k in HEADER])
    p.write_text(body.getvalue(), encoding="utf-8")
    written.append((str(p.relative_to(ROOT)), len(kept),
                    hashlib.sha256(p.read_bytes()).hexdigest()))
    for name, n, sha in written:
        log(f"      {name:<34} rows={n:<4} sha256={sha}")

    # machine-readable summary for doc generation
    (ROOT / ".rawchunks" / "tables.json").write_text(json.dumps({
        "tables": final_tables, "notes": season_notes,
        "csv": [{"file": f, "rows": n, "sha256": s_} for f, n, s_ in written],
    }, indent=1), encoding="utf-8")

    # ---------------------------------------------------------------- result
    log("")
    log("=" * 78)
    if problems:
        log(f"RESULT: {len(problems)} PROBLEM(S) - see lines marked FAIL above.")
        sys.exit(1)
    log("RESULT: ALL CHECKS PASSED - dataset structurally sound, rows verbatim.")
    log("=" * 78)


if __name__ == "__main__":
    main()
    (ROOT / "audit").mkdir(exist_ok=True)
    (ROOT / "audit" / "validation-report.txt").write_text("\n".join(report) + "\n",
                                                         encoding="utf-8")
