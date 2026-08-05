"""
CHAIN SYSTEM — FOUNDATION STEP 2
Find and score opponent chains between any two clubs. Results only.

Output is deliberately verbose: every path, its age, its context mix, and the
SPREAD shown as prominently as the mean. The system is allowed to say
"not usable" — that is a valid and important answer.
"""
import pickle, unicodedata, re
from collections import defaultdict

EDGES = pickle.load(open("/home/user/chain/edges.pkl", "rb"))

def norm(s):
    """Aggressive normaliser: strips accents, club-type prefixes/suffixes, punctuation.
    Merges 'AFC Ajax'/'Ajax', 'ACF Fiorentina'/'Fiorentina' etc. into one identity.
    Fixes the split-identity bug that severed cross-border bridges (Study 22)."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    toks = [t for t in s.split() if t]
    DROP = {'fc','afc','ac','as','sc','sk','fk','nk','hnk','gnk','bk','ik','if','cf','cd','ca',
            'sv','vfl','vfb','fsv','tsv','rc','rcd','ud','sd','ss','ssc','us','acf','sl','cs',
            'csm','fcs','pfc','club','de','the','kv','rsc','sporting','fk.','ff','ifk','og'}
    core = [t for t in toks if t not in DROP]
    if not core:
        core = toks
    return ''.join(core)

# canonical map: normalised key -> shortest display name (built from all edges)
CANON = {}
for _e in EDGES:
    for _c, _n in ((_e[2], _e[3]), (_e[4], _e[5])):
        _k = norm(_n)
        if _k and (_k not in CANON or len(_n) < len(CANON[_k])):
            CANON[_k] = _n

# Explicit aliases: same club, different source spelling. Verified by hand.
ALIASES = {
    "sherifftiraspol": "FC Sheriff",
    "dynamokyiv": "Dinamo Kiev", "dynamokiev": "Dinamo Kiev",
    "floratallinn": "FC Flora",
    "vojvodinanovisad": "Vojvodina",
    "lnz": "FC LNZ Cherkasy", "lnzcherkasy": "FC LNZ Cherkasy",
    "noahyerevan": "FC Noah",
    "zimbruchisinau": "FC Zimbru",
    "zrinjski": "Zrinjski Mostar",
    "valur": "Valur Reykjavik",
    "braga": "Sp Braga",
    "zeleznicarpancevo": "Zeleznicar Pancevo",
    "maccabitelaviv": "Maccabi Tel Aviv",
    "paide": "Paide Linnameeskond",
    "pafos": "Paphos FC", "pafosfc": "Paphos FC",
    "universitateacluj": "Universitatea Cluj",
    "nsirunavik": "NSI Runavik",
    "paksi": "Paksi SE",
    "bateborisov": "BATE Borisov",
    "liepaja": "FK Liepaja",
    "nkvarazdin": "NK Varazdin",
    "hajduksplit": "Hajduk Split",
    "gais": "GAIS",
    "thenewsaints": "The New Saints",
    "zira": "Zira FK",
    "jablonec": "FK Jablonec",
    "koper": "FC Koper",
}

def resolve(name):
    k = norm(name)
    if k in ALIASES:
        a = norm(ALIASES[k])
        if a in CANON:
            return CANON[a]
    if k in CANON:
        return CANON[k]
    # unique prefix match, but only if exactly one candidate qualifies
    cands = [CANON[kk] for kk in CANON
             if (kk.startswith(k) or k.startswith(kk)) and abs(len(kk) - len(k)) <= 4]
    if len(cands) == 1:
        return cands[0]
    return None

# results index: canonical -> opponent -> [(date, gd, comp)]
RES = defaultdict(lambda: defaultdict(list))
for dt, comp, ch, h, ca, a, hg, ag in EDGES:
    H, A = CANON[norm(h)], CANON[norm(a)]
    RES[H][A].append((dt, hg - ag, comp))
    RES[A][H].append((dt, ag - hg, comp))


def recent(lst, since):
    return [x for x in lst if x[0] >= since]


def avg_gd(lst):
    return sum(g for _, g, _ in lst) / len(lst)


def find_chains(team_a, team_b, since="2021-01-01", max_hops=3):
    """Return direct meetings, 2nd-phase and 3rd-phase chains."""
    A, B = resolve(team_a), resolve(team_b)
    if not A or not B:
        return {"error": f"unresolved: {team_a if not A else ''} {team_b if not B else ''}".strip()}

    oppA = {o: recent(v, since) for o, v in RES[A].items() if recent(v, since)}
    oppB = {o: recent(v, since) for o, v in RES[B].items() if recent(v, since)}

    out = {"A": A, "B": B, "since": since,
           "oppA": len(oppA), "oppB": len(oppB),
           "direct": [], "phase2": [], "phase3": []}

    if B in oppA:
        out["direct"] = [(d, g, c) for d, g, c in oppA[B]]

    for x in set(oppA) & set(oppB):
        if x in (A, B):
            continue
        ax, bx = avg_gd(oppA[x]), avg_gd(oppB[x])
        yrs = [d[:4] for d, _, _ in oppA[x]] + [d[:4] for d, _, _ in oppB[x]]
        comps = {c.split(':')[0] for _, _, c in oppA[x]} | {c.split(':')[0] for _, _, c in oppB[x]}
        out["phase2"].append({"via": x, "est": ax - bx, "n": len(oppA[x]) + len(oppB[x]),
                              "y0": min(yrs), "y1": max(yrs), "ctx": "/".join(sorted(comps))})

    shared = set(oppA) & set(oppB)
    for x in oppA:
        if x in shared or x == B:
            continue
        oppX = {o: recent(v, since) for o, v in RES[x].items() if recent(v, since)}
        for y in oppX:
            if y in (A, B, x) or y in shared or y not in oppB:
                continue
            ax, xy, yb = avg_gd(oppA[x]), avg_gd(oppX[y]), avg_gd(oppB[y])
            est = ax + xy - yb
            yrs = ([d[:4] for d, _, _ in oppA[x]] + [d[:4] for d, _, _ in oppX[y]]
                   + [d[:4] for d, _, _ in oppB[y]])
            comps = ({c.split(':')[0] for _, _, c in oppA[x]}
                     | {c.split(':')[0] for _, _, c in oppX[y]}
                     | {c.split(':')[0] for _, _, c in oppB[y]})
            out["phase3"].append({"via": f"{x} > {y}", "est": est,
                                  "n": len(oppA[x]) + len(oppX[y]) + len(oppB[y]),
                                  "y0": min(yrs), "y1": max(yrs),
                                  "ctx": "/".join(sorted(comps))})
    return out


def summarise(chains, label):
    if not chains:
        return None
    v = [c["est"] for c in chains]
    m = sum(v) / len(v)
    sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5 if len(v) > 1 else 0.0
    mixed = sum(1 for c in chains if '/' in c["ctx"])
    return {"label": label, "n": len(chains), "mean": m, "sd": sd,
            "lo": min(v), "hi": max(v), "spread": max(v) - min(v),
            "oldest": min(c["y0"] for c in chains),
            "newest": max(c["y1"] for c in chains),
            "mixed_ctx": mixed}


def verdict(s):
    """Honest usability call. Spread and age decide, not the mean."""
    if s is None:
        return "NO CHAINS", "no path found in the window"
    if s["n"] < 3:
        return "THIN", f"only {s['n']} path(s) — too few to trust"
    if s["spread"] > 4.0:
        return "NOT USABLE", f"paths disagree by {s['spread']:.1f} goals"
    if s["sd"] > 1.5:
        return "WEAK", f"high dispersion (sd {s['sd']:.2f})"
    if int(s["newest"]) < 2021:
        return "STALE", f"newest link {s['newest']}"
    return "USABLE", f"{s['n']} paths, sd {s['sd']:.2f}"


def report(team_a, team_b, since="2021-01-01"):
    r = find_chains(team_a, team_b, since)
    if "error" in r:
        print("  " + r["error"])
        return r
    print("=" * 86)
    print(f"CHAIN ANALYSIS  —  {r['A']}  vs  {r['B']}      (links since {since})")
    print("=" * 86)
    print(f"  opponents in window: {r['A']} {r['oppA']} | {r['B']} {r['oppB']}")

    if r["direct"]:
        print(f"\n  DIRECT MEETINGS ({len(r['direct'])}):")
        for d, g, c in sorted(r["direct"]):
            print(f"    {d}  {c:12s}  GD {g:+d}")
    else:
        print("\n  DIRECT MEETINGS: none")

    for ph, key in [("2nd PHASE (shared opponents)", "phase2"),
                    ("3rd PHASE (opponent-of-opponent)", "phase3")]:
        cs = r[key]
        print(f"\n  {ph}: {len(cs)} path(s)")
        for c in sorted(cs, key=lambda c: -c["est"])[:14]:
            print(f"    {c['via']:44s} {c['est']:+6.2f}  {c['y0']}-{c['y1']}  n={c['n']:2d}  {c['ctx']}")
        if len(cs) > 14:
            print(f"    ... and {len(cs)-14} more")
        s = summarise(cs, ph)
        if s:
            v, why = verdict(s)
            print(f"    ---> MEAN {s['mean']:+.2f}   SD {s['sd']:.2f}   "
                  f"RANGE {s['lo']:+.2f} to {s['hi']:+.2f}   SPREAD {s['spread']:.2f}")
            print(f"    ---> links {s['oldest']}-{s['newest']}, {s['mixed_ctx']}/{s['n']} mixed-context")
            print(f"    ---> VERDICT: {v} — {why}")
    return r


if __name__ == "__main__":
    report("Lech Poznan", "Aarhus")
