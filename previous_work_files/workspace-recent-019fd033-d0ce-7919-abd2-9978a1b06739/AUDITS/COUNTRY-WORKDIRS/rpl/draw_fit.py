#!/usr/bin/env python3
# CALIBRATION-9 step B: candidate calibration maps for the displayed 3-way balance.
# Split-half discipline: fit on half A -> test on half B, and reverse. Date-sorted halves.
import json, math
games = json.load(open("/home/user/rpl/draw_replay.json"))
games.sort(key=lambda g: g["date"])
n = len(games)
half = n // 2
IA, IB = list(range(0, half)), list(range(half, n))
base = [0.0, 0.0, 0.0]
for g in games: base["HDA".index(g["actual"])] += 1
base = [x / n for x in base]

def raw(g): return [g["balH"] / 100, g["balD"] / 100, g["balA"] / 100]
def llrow(p, g): return -math.log(max(p["HDA".index(g["actual"])], 1e-9))
def llset(dist_fn, idx): return sum(llrow(dist_fn(games[i]), games[i]) for i in idx) / len(idx)
def llraw(idx): return llset(raw, idx)
def brier(p, g):
    y = [1.0 if g["actual"] == k else 0.0 for k in "HDA"]
    return sum((p[i] - y[i]) ** 2 for i in range(3))

print(f"pool n={n} half={half}  base={['%.3f'%b for b in base]}")
print(f"RAW  log-loss A {llraw(IA):.4f}  B {llraw(IB):.4f}  ALL {llraw(list(range(n))):.4f}")
print(f"FLAT log-loss ALL {llset(lambda g: base, list(range(n))):.4f}")

# C1: shrink-to-base blend, single weight w fit on fit-half
def mk_c1(w):
    return lambda g: [w * x + (1 - w) * b for x, b in zip(raw(g), base)]
print("\nC1 shrink-to-base  p' = w*p + (1-w)*base")
print("    w     llA(fit) llB(test) | fit on B -> test A")
for w10 in range(1, 11):
    w = w10 / 10
    a, b = llset(mk_c1(w), IA), llset(mk_c1(w), IB)
    print(f"  {w:.1f}    {a:.4f}   {b:.4f}")

# pick best w on A, best on B
bestA = min(range(1, 11), key=lambda w: llset(mk_c1(w / 10), IA)) / 10
bestB = min(range(1, 11), key=lambda w: llset(mk_c1(w / 10), IB)) / 10
print(f"  best on A w={bestA} -> testB {llset(mk_c1(bestA), IB):.4f}   best on B w={bestB} -> testA {llset(mk_c1(bestB), IA):.4f}")

# C2: temperature p'^t normalized
def mk_c2(t):
    def f(g):
        p = [max(x, 1e-9) ** t for x in raw(g)]
        s = sum(p)
        return [x / s for x in p]
    return f
print("\nC2 temperature p'^t / sum")
for t in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    print(f"  t={t:.1f}    {llset(mk_c2(t), IA):.4f}   {llset(mk_c2(t), IB):.4f}")

# C3: draw-only affine D' = clip(a+b*D, 4, 48); remainder split by raw H:A ratio
def fit_affine(idx):
    xs = [games[i]["balD"] for i in idx]
    ys = [1.0 if games[i]["actual"] == "D" else 0.0 for i in idx]
    mx = sum(xs) / len(xs); my = sum(ys) / len(ys)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return my - b * mx, b
def mk_c3(a, b):
    def f(g):
        p = raw(g)
        D = min(max(a + b * p[1] * 100, 4.0), 48.0) / 100
        rest = 1 - D
        hs = p[0] + p[2]
        H = rest * (p[0] / hs if hs else 0.5)
        A = rest - H
        return [H, D, A]
    return f
aA, bA = fit_affine(IA); aB, bB = fit_affine(IB)
print(f"\nC3 draw-only affine: fitA a={aA*100:.2f} b={bA:.2f} -> testB {llset(mk_c3(aA,bA), IB):.4f}")
print(f"                    fitB a={aB*100:.2f} b={bB:.2f} -> testA {llset(mk_c3(aB,bB), IA):.4f}")
print(f"                    pooled a={ (aA+aB)/2*100:.2f} b={(bA+bB)/2:.2f} -> ALL {llset(mk_c3((aA+aB)/2,(bA+bB)/2), list(range(n))):.4f}")

# C4: draw-affine + side temperature (draw fixed by C3, sides softened toward side base 58/42)
def mk_c4(a, b, w):
    c3 = mk_c3(a, b)
    def f(g):
        p = c3(g)
        H = w * p[0] + (1 - w) * (p[0] + p[2]) * (base[0] / (base[0] + base[2]))
        return [H, p[1], p[0] + p[2] - H]
    return f
print("\nC4 = C3 + sides shrunk toward home/away base split")
for w10 in range(2, 11, 2):
    w = w10 / 10
    fa = mk_c4(aA, bA, w); fb = mk_c4(aB, bB, w)
    print(f"  w={w:.1f}  Afit->{llset(fa,IA):.4f}/Btest->{llset(fa,IB):.4f}   Bfit->{llset(fb,IB):.4f}/Atest->{llset(fb,IA):.4f}")

# realized-draw check for a candidate (calibration curve after mapping)
def curve(fn, idx, label):
    print(f"\n{label}")
    rows = []
    for i in idx:
        p = fn(games[i]); rows.append((p[1] * 100, games[i]["actual"]))
    rows.sort()
    m = len(rows); step = m // 6
    for k in range(6):
        seg = rows[k * step: (k + 1) * step if k < 5 else m]
        dd = [1 if a == "D" else 0 for _, a in seg]
        print(f"  dispD {seg[0][0]:5.1f}-{seg[-1][0]:5.1f}  n={len(seg):>3}  mean {sum(s[0] for s in seg)/len(seg):5.1f}%  realized {100*sum(dd)/len(dd):5.1f}%")
curve(lambda g: raw(g), list(range(n)), "RAW draw curve (sextiles)")
curve(mk_c1(bestA), IB, f"C1 w={bestA} (fitA) draw curve on test B")
