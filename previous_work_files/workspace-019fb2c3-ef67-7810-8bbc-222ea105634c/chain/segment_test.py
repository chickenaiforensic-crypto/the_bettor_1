"""
EXHAUSTIVE SEGMENTATION TEST
Question: does chain accuracy depend on WHERE the links come from?

Segments every chain by link context:
  EUR-only   : every link in the chain is a European tie
  MIXED      : chain combines European ties and domestic league matches
  DOM-heavy  : majority of links are domestic

Reports direction accuracy and tier rates SEPARATELY per segment.
No prediction is produced. This only judges whether the existing tier table is sound.
"""
import pickle, re, glob, math
from collections import defaultdict
import chain as C

# ---------- load cross-border ties ----------
line = re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ties = []
for f in sorted(glob.glob("/home/user/chain/ucl/champions-league-master/*/*.txt")):
    yr = int(f.split('/')[-2][:4])
    if yr < 2021:
        continue
    for ln in open(f, encoding='utf-8', errors='replace'):
        m = line.match(ln.strip('\r\n'))
        if m and m.group(2) != m.group(4):
            ties.append((yr, m.group(1).strip(), m.group(3).strip(),
                         int(m.group(5)), int(m.group(6))))
print(f"cross-border ties 2021+: {len(ties):,}")


def links(t, since, cut):
    out = {}
    for k, v in C.RES[t].items():
        f = [e for e in v if since <= e[0] <= cut]
        if f:
            out[k] = f
    return out


def gd(l):
    return sum(g for _, g, _ in l)/len(l)


def ctx_of(l):
    """'E' if every match on this link is European, 'D' if all domestic, else 'M'."""
    e = sum(1 for _, _, c in l if c.startswith('EUR'))
    if e == len(l):
        return 'E'
    if e == 0:
        return 'D'
    return 'M'


rows = []
for yr, h, a, hg, ag in ties:
    A, B = C.resolve(h), C.resolve(a)
    if not A or not B:
        continue
    since, cut = f"{yr-5}-01-01", f"{yr}-06-29"
    oA, oB = links(A, since, cut), links(B, since, cut)
    if not oA or not oB:
        continue
    sh = set(oA) & set(oB)
    paths = []          # (phase, estimate, context_string)
    for x in sh:
        paths.append(('p2', gd(oA[x]) - gd(oB[x]), ctx_of(oA[x]) + ctx_of(oB[x])))
    if not sh:
        for x in oA:
            if x == B:
                continue
            oX = links(x, since, cut)
            for y in oX:
                if y in (A, B, x) or y not in oB:
                    continue
                paths.append(('p3', gd(oA[x]) + gd(oX[y]) - gd(oB[y]),
                              ctx_of(oA[x]) + ctx_of(oX[y]) + ctx_of(oB[y])))
    if len(paths) < 2:
        continue
    ests = [p[1] for p in paths]
    est = sum(ests)/len(ests)
    allctx = ''.join(p[2] for p in paths)
    nE = allctx.count('E'); nD = allctx.count('D'); nM = allctx.count('M')
    tot = nE + nD + nM
    if nE == tot:
        seg = 'EUR-only'
    elif nD + nM*0.5 > tot*0.5:
        seg = 'DOM-heavy'
    else:
        seg = 'MIXED'
    rows.append(dict(seg=seg, est=est, n=len(paths),
                     phase='p2' if paths[0][0] == 'p2' else 'p3',
                     res='H' if hg > ag else ('D' if hg == ag else 'A'),
                     gd=hg-ag, eur_frac=nE/tot))
print(f"scoreable fixtures: {len(rows):,}")
pickle.dump(rows, open('/home/user/chain/segment_rows.pkl', 'wb'))


def wil(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k/n
    d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return c-h, c+h


def corr(x, y):
    n = len(x)
    mx, my = sum(x)/n, sum(y)/n
    a = sum((p-mx)*(q-my) for p, q in zip(x, y))
    b = math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
    return a/b if b else 0


print("\n" + "="*84)
print("SEGMENT 1 — DIRECTION ACCURACY BY LINK CONTEXT")
print("="*84)
print(f"  {'segment':12s} {'fixtures':>9s} {'decisive':>9s} {'direction':>10s} {'95% CI':>18s} {'r w/ GD':>9s}")
for seg in ['EUR-only', 'MIXED', 'DOM-heavy']:
    s = [r for r in rows if r['seg'] == seg]
    if len(s) < 25:
        print(f"  {seg:12s} {len(s):9d}  too few")
        continue
    dec = [r for r in s if r['res'] != 'D']
    hit = sum(1 for r in dec if (r['est'] > 0) == (r['res'] == 'H'))
    lo, up = wil(hit, len(dec))
    r_ = corr([r['est'] for r in s], [r['gd'] for r in s])
    print(f"  {seg:12s} {len(s):9d} {len(dec):9d} {hit/len(dec):10.1%}  [{lo:.1%},{up:.1%}] {r_:+9.4f}")

print("\n" + "="*84)
print("SEGMENT 2 — TIER TABLE REBUILT PER SEGMENT")
print("="*84)
BANDS = [(-99, -1.0), (-1.0, -0.35), (-0.35, 0.35), (0.35, 1.0), (1.0, 2.0), (2.0, 99)]
NAMES = ['CH-F', 'CH-E', 'CH-D', 'CH-C', 'CH-B', 'CH-A']
for seg in ['EUR-only', 'MIXED', 'DOM-heavy', 'ALL']:
    s = rows if seg == 'ALL' else [r for r in rows if r['seg'] == seg]
    if len(s) < 60:
        continue
    print(f"\n  {seg}  (n={len(s)})")
    print(f"    {'tier':6s} {'band':16s} {'n':>5s} {'HOME':>7s} {'DRAW':>7s} {'AWAY':>7s}")
    for (lo_, hi_), nm in zip(BANDS, NAMES):
        b = [r for r in s if lo_ <= r['est'] < hi_]
        if len(b) < 20:
            continue
        H = sum(1 for r in b if r['res'] == 'H')
        D = sum(1 for r in b if r['res'] == 'D')
        print(f"    {nm:6s} [{lo_:6.2f},{hi_:6.2f}) {len(b):5d} {H/len(b):7.1%} "
              f"{D/len(b):7.1%} {(len(b)-H-D)/len(b):7.1%}")

print("\n" + "="*84)
print("SEGMENT 3 — DOES THE EUROPEAN FRACTION OF A CHAIN PREDICT ITS RELIABILITY?")
print("="*84)
print(f"  {'euro fraction':16s} {'n':>6s} {'direction':>10s} {'95% CI':>18s}")
for lo_, hi_ in [(0, 0.34), (0.34, 0.67), (0.67, 0.99), (0.99, 1.01)]:
    s = [r for r in rows if lo_ <= r['eur_frac'] < hi_]
    dec = [r for r in s if r['res'] != 'D']
    if len(dec) < 25:
        continue
    hit = sum(1 for r in dec if (r['est'] > 0) == (r['res'] == 'H'))
    lo, up = wil(hit, len(dec))
    print(f"  [{lo_:.2f},{hi_:.2f})      {len(s):6d} {hit/len(dec):10.1%}  [{lo:.1%},{up:.1%}]")
