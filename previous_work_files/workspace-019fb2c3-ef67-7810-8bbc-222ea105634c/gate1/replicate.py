"""
Gate 1 — independent reimplementation of FOOTBALL_HOME_SYSTEM.md v1.0 spec,
run against football-data.co.uk data (independent of the original transcription).

Spec (doc section 3):
  P = all league matches with date < fixture date
  H_scored_home   = mean goals scored by HOME team in its home matches
  H_conceded_home = mean goals conceded by HOME team in its home matches
  A_scored_away   = mean goals scored by AWAY team in its away matches
  A_conceded_away = mean goals conceded by AWAY team in its away matches
  S6 = 0.5*H_scored_home + 0.5*A_conceded_away
  S7 = 0.5*A_scored_away + 0.5*H_conceded_home
  xMargin = S6 - S7
  Min: >=3 prior home matches for H, >=3 prior away matches for A
  Fire CLEAR_WIN when xMargin >= 1.0
"""
import csv, math
from datetime import datetime
from collections import defaultdict

LEAGUES = {"SWE": "Allsvenskan", "NOR": "Eliteserien", "FIN": "Veikkausliiga"}
MINPRIOR = 3
THRESH = 1.0

def load(code, season="2026"):
    rows = []
    with open(f"/home/user/gate1/{code}.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["Season"] != season: continue
            if not r["HG"] or not r["AG"]: continue
            try:
                d = datetime.strptime(r["Date"], "%d/%m/%Y")
            except ValueError:
                continue
            def fl(k):
                v = r.get(k, "")
                try: return float(v)
                except: return None
            rows.append(dict(
                date=d, home=r["Home"].strip(), away=r["Away"].strip(),
                hg=int(r["HG"]), ag=int(r["AG"]), res=r["Res"],
                psch=fl("PSCH"), pscd=fl("PSCD"), psca=fl("PSCA"),
                avgch=fl("AvgCH"), avgcd=fl("AvgCD"), avgca=fl("AvgCA"),
                maxch=fl("MaxCH"),
            ))
    rows.sort(key=lambda x: x["date"])
    return rows

def xmargin(rows, i):
    """xMargin for fixture i using only matches strictly before its date."""
    fx = rows[i]
    prior = [m for m in rows if m["date"] < fx["date"]]
    H, A = fx["home"], fx["away"]
    h_home = [m for m in prior if m["home"] == H]
    a_away = [m for m in prior if m["away"] == A]
    if len(h_home) < MINPRIOR or len(a_away) < MINPRIOR:
        return None, len(h_home), len(a_away)
    H_sc = sum(m["hg"] for m in h_home)/len(h_home)
    H_cc = sum(m["ag"] for m in h_home)/len(h_home)
    A_sc = sum(m["ag"] for m in a_away)/len(a_away)
    A_cc = sum(m["hg"] for m in a_away)/len(a_away)
    S6 = 0.5*H_sc + 0.5*A_cc
    S7 = 0.5*A_sc + 0.5*H_cc
    return S6 - S7, len(h_home), len(a_away)

allfired, allgraded = [], []
print("="*78)
print("GATE 1 — INDEPENDENT REPLICATION  (football-data.co.uk, 2026 season)")
print("="*78)

for code, lname in LEAGUES.items():
    rows = load(code)
    fired, graded = [], 0
    for i, fx in enumerate(rows):
        xm, nh, na = xmargin(rows, i)
        if xm is None: continue
        graded += 1
        rec = dict(lg=code, **fx, xm=xm, nh=nh, na=na)
        allgraded.append(rec)
        if xm >= THRESH:
            fired.append(rec); allfired.append(rec)
    w = sum(1 for f in fired if f["res"]=="H")
    d = sum(1 for f in fired if f["res"]=="D")
    l = sum(1 for f in fired if f["res"]=="A")
    base = sum(1 for m in rows if m["res"]=="H")/len(rows)
    print(f"\n{lname:15s} matches {len(rows):3d} | gradeable {graded:3d} | FIRED {len(fired):2d}"
          f" -> {w}W {d}D {l}L = {w/len(fired):.1%}" if fired else f"\n{lname}: no fires")
    print(f"{'':15s} home-win baseline {base:.1%}")

W = sum(1 for f in allfired if f["res"]=="H")
D = sum(1 for f in allfired if f["res"]=="D")
L = sum(1 for f in allfired if f["res"]=="A")
N = len(allfired)
print("\n" + "="*78)
print(f"COMBINED: {N} fired  |  {W}W  {D}D  {L}L")
print(f"  Hit rate (draw = LOSS, correct method) : {W}/{N} = {W/N:.1%}")
print(f"  Hit rate (draw EXCLUDED, the app's bug): {W}/{W+L} = {W/(W+L):.1%}")
print(f"  DRAW RATE among fired selections       : {D}/{N} = {D/N:.1%}")
print("="*78)
print(f"\nDoc claims: 36 fired, 31W 1D 4L, draw rate 2.8%")
print(f"Replication: {N} fired, {W}W {D}D {L}L, draw rate {D/N:.1%}")

import pickle
pickle.dump((allfired, allgraded), open("/home/user/gate1/results.pkl","wb"))
