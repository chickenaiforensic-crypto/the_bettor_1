"""Does the user's weighted scale beat plain goal difference as a chain metric?
Blueprint T5: test the user's construction as specified. T1: paired. T3: rolling origin."""
import pickle, re, glob, math
from collections import defaultdict
import chain as C
from weighted import wscore

# rebuild RES carrying the actual scoreline so wscore can be applied
RESW = defaultdict(lambda: defaultdict(list))
for dt, comp, ch, h, ca, a, hg, ag in C.EDGES:
    H, A = C.CANON[C.norm(h)], C.CANON[C.norm(a)]
    RESW[H][A].append((dt, hg, ag, comp))
    RESW[A][H].append((dt, ag, hg, comp))

line_re = re.compile(r'^\s*(?:\d{1,2}:\d{2}\s+)?(.+?)\s+\((\w{3})\)\s+v\s+(.+?)\s+\((\w{3})\)\s+(\d+)-(\d+)')
ties = []
for f in sorted(glob.glob("/home/user/chain/ucl/champions-league-master/*/*.txt")):
    yr = int(f.split('/')[-2][:4])
    if yr < 2021: continue
    for ln in open(f, encoding='utf-8', errors='replace'):
        m = line_re.match(ln.strip('\r\n'))
        if m and m.group(2) != m.group(4):
            ties.append((yr, m.group(1).strip(), m.group(3).strip(),
                         int(m.group(5)), int(m.group(6))))

def links(t, since, cut):
    out = {}
    for o, v in RESW[t].items():
        f = [x for x in v if since <= x[0] <= cut]
        if f: out[o] = f
    return out

def avg_gd(l):  return sum(a-b for _,a,b,_ in l)/len(l)
def avg_ws(l):  return sum(wscore(a,b) for _,a,b,_ in l)/len(l)

rows = []
for yr, h, a, hg, ag in ties:
    A, B = C.resolve(h), C.resolve(a)
    if not A or not B: continue
    since, cut = f"{yr-5}-01-01", f"{yr}-06-29"   # season-stamped: exclude the tie's own season
    oA, oB = links(A, since, cut), links(B, since, cut)
    if not oA or not oB: continue
    sh = set(oA) & set(oB)
    gd_e, ws_e = [], []
    for x in sh:
        gd_e.append(avg_gd(oA[x]) - avg_gd(oB[x]))
        ws_e.append(avg_ws(oA[x]) - avg_ws(oB[x]))
    if not sh:
        for x in oA:
            if x in sh or x == B: continue
            oX = links(x, since, cut)
            for y in oX:
                if y in (A, B, x) or y in sh or y not in oB: continue
                gd_e.append(avg_gd(oA[x]) + avg_gd(oX[y]) - avg_gd(oB[y]))
                ws_e.append(avg_ws(oA[x]) + avg_ws(oX[y]) - avg_ws(oB[y]))
    if len(gd_e) < 2: continue
    rows.append((sum(gd_e)/len(gd_e), sum(ws_e)/len(ws_e),
                 'H' if hg>ag else ('D' if hg==ag else 'A'), hg-ag, len(gd_e)))

print(f"scoreable fixtures: {len(rows):,}")

def corr(x, y):
    n=len(x); mx=sum(x)/n; my=sum(y)/n
    a=sum((p-mx)*(q-my) for p,q in zip(x,y))
    b=math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
    return a/b if b else 0

def wil(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h

act = [r[3] for r in rows]
print("\n" + "="*78)
print("HEAD TO HEAD — plain goal difference vs user's weighted scale")
print("="*78)
for lbl, i in [("plain goal difference", 0), ("USER weighted scale", 1)]:
    est = [r[i] for r in rows]
    dec = [r for r in rows if r[2] != 'D']
    hit = sum(1 for r in dec if (r[i] > 0) == (r[2] == 'H'))
    lo, up = wil(hit, len(dec))
    print(f"  {lbl:26s} r={corr(est,act):+.4f}   direction {hit}/{len(dec)} = {hit/len(dec):.1%}  CI [{lo:.1%},{up:.1%}]")

# paired test on direction agreement
both = [(r[0]>0)==(r[2]=='H') for r in rows if r[2]!='D']
bothw = [(r[1]>0)==(r[2]=='H') for r in rows if r[2]!='D']
diff = [1 if (w and not g) else (-1 if (g and not w) else 0) for g,w in zip(both,bothw)]
n_w = sum(1 for d in diff if d>0); n_g = sum(1 for d in diff if d<0)
print(f"\n  disagreements: weighted right/gd wrong = {n_w} | gd right/weighted wrong = {n_g}")
if n_w+n_g > 0:
    p = sum(math.comb(n_w+n_g,k)*0.5**(n_w+n_g) for k in range(min(n_w,n_g)+1))*2
    print(f"  McNemar exact p = {min(p,1):.4f}")

print("\n" + "="*78)
print("DRAW DETECTION — does separating 0-0 from 1-1 help?")
print("="*78)
for lbl, i in [("plain GD", 0), ("weighted", 1)]:
    band = [r for r in rows if abs(r[i]) < (0.35 if i==0 else 1.0)]
    if len(band) < 20: continue
    d = sum(1 for r in band if r[2]=='D')
    lo,up = wil(d,len(band))
    print(f"  {lbl:12s} level band n={len(band):4d}  draw rate {d/len(band):.1%}  CI [{lo:.1%},{up:.1%}]")
base = sum(1 for r in rows if r[2]=='D')/len(rows)
print(f"  baseline draw rate: {base:.1%}")
pickle.dump(rows, open('/home/user/chain/weighted_test.pkl','wb'))
