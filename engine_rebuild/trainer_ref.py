"""
PITCH RATING ENGINE — REFERENCE TRAINER (Python)
Runs the Dixon-Coles engine from ENGINE_SPEC on the 5,082-row verified store.
Produces baseline numbers for JS engine verification.
Zero market data. Results only.
"""
import pickle, math, json, os
from datetime import datetime
from collections import defaultdict

# Load the 5,082-row converted store
rows = pickle.load(open(os.path.join(os.path.dirname(__file__), 'store_5082_rows.pkl'), 'rb'))
rows.sort(key=lambda r: (r['date'], r['lg'], r['home'], r['away']))
print(f"matches {len(rows):,}")

# ── Model: identical to ENGINE_SPEC Part B ──
class Model:
    """Online Dixon-Coles with per-league HFA. Matches ENGINE_SPEC §B3."""
    def __init__(self, lr=0.055, decay=0.0022, hfa_lr=0.010):
        self.att = defaultdict(float)
        self.dfn = defaultdict(float)
        self.hfa = defaultdict(lambda: 0.26)
        self.thfa = defaultdict(float)
        self.mu = defaultdict(lambda: 0.30)
        self.lr = lr
        self.decay = decay
        self.hfa_lr = hfa_lr
        self.seen = defaultdict(int)

    def lam(self, lg, h, a):
        lh = math.exp(self.mu[lg] + self.att[h] - self.dfn[a] + self.hfa[lg] + self.thfa[h])
        la = math.exp(self.mu[lg] + self.att[a] - self.dfn[h])
        return max(0.05, min(6.0, lh)), max(0.05, min(6.0, la))

    def update(self, m):
        lg, h, a, hg, ag = m['lg'], m['home'], m['away'], m['hg'], m['ag']
        lh, la = self.lam(lg, h, a)
        eh, ea = hg - lh, ag - la
        kh = self.lr * (1.6 if self.seen[h] < 8 else 1.0)
        ka = self.lr * (1.6 if self.seen[a] < 8 else 1.0)
        self.att[h] += kh * eh * 0.5
        self.dfn[a] -= ka * eh * 0.5
        self.att[a] += ka * ea * 0.5
        self.dfn[h] -= kh * ea * 0.5
        self.hfa[lg] += self.hfa_lr * (eh - ea) * 0.02
        self.thfa[h] += self.hfa_lr * (eh - ea) * 0.010
        self.thfa[h] *= 0.999
        self.mu[lg] += 0.004 * ((eh + ea) / 2)
        for t in (h, a):
            self.att[t] *= (1 - self.decay)
            self.dfn[t] *= (1 - self.decay)
        self.seen[h] += 1
        self.seen[a] += 1
        self.hfa[lg] = max(0.05, min(0.55, self.hfa[lg]))
        self.thfa[h] = max(-0.25, min(0.25, self.thfa[h]))

# ── Distribution: ENGINE_SPEC Part C ──
_fact = [math.factorial(i) for i in range(11)]

def dc_tau(i, j, lh, la, rho=-0.06):
    if i == 0 and j == 0: return 1 - lh * la * rho
    if i == 0 and j == 1: return 1 + lh * rho
    if i == 1 and j == 0: return 1 + la * rho
    if i == 1 and j == 1: return 1 - rho
    return 1.0

def probs(lh, la, rho=-0.06, K=11):
    ph = [math.exp(-lh) * lh**i / _fact[i] for i in range(K)]
    pa = [math.exp(-la) * la**j / _fact[j] for j in range(K)]
    H = D = A = 0.0
    grid = {}
    for i in range(K):
        for j in range(K):
            p = ph[i] * pa[j] * dc_tau(i, j, lh, la, rho)
            grid[(i, j)] = p
            if i > j:
                H += p
            elif i == j:
                D += p
            else:
                A += p
    t = H + D + A
    return H / t, D / t, A / t, grid, t

# ── Walk-forward: strict causality ──
model = Model()
preds = []
for m in rows:
    if model.seen[m['home']] >= 6 and model.seen[m['away']] >= 6:
        lh, la = model.lam(m['lg'], m['home'], m['away'])
        H, D, A, _, _ = probs(lh, la)
        preds.append((m, H, D, A, lh, la))
    model.update(m)

print(f"predictions made (both teams >=6 games): {len(preds):,}")

# ── Scoring ──
def brier(ps):
    s = 0.0
    for m, H, D, A, _, _ in ps:
        y = (1 if m['res'] == 'H' else 0, 1 if m['res'] == 'D' else 0, 1 if m['res'] == 'A' else 0)
        s += (H - y[0])**2 + (D - y[1])**2 + (A - y[2])**2
    return s / len(ps)

def logloss(ps):
    s = 0.0
    for m, H, D, A, _, _ in ps:
        p = {'H': H, 'D': D, 'A': A}[m['res']]
        s -= math.log(max(p, 1e-12))
    return s / len(ps)

def direction_hit(ps):
    correct = 0
    for m, H, D, A, _, _ in ps:
        pred = max(('H', H), ('D', D), ('A', A), key=lambda x: x[1])
        if pred[0] == m['res']:
            correct += 1
    return correct / len(ps)

base = (0.446, 0.268, 0.286)
bb = sum((base[0] - (m['res'] == 'H'))**2 + (base[1] - (m['res'] == 'D'))**2 + (base[2] - (m['res'] == 'A'))**2 for m, _, _, _, _, _ in preds) / len(preds)
bl = -sum(math.log({'H': base[0], 'D': base[1], 'A': base[2]}[m['res']]) for m, _, _, _, _, _ in preds) / len(preds)

model_b = brier(preds)
model_ll = logloss(preds)
model_dir = direction_hit(preds)

print("\n" + "=" * 80)
print("REFERENCE ENGINE — 5,082-row verified store")
print("=" * 80)
print(f"  {'':30s} {'Brier':>10s} {'LogLoss':>10s} {'Direction':>10s}")
print(f"  {'base rate (44.6/26.8/28.6)':30s} {bb:10.4f} {bl:10.4f} {'—':>10s}")
print(f"  {'rating model':30s} {model_b:10.4f} {model_ll:10.4f} {model_dir:10.4f}")
print(f"  improvement: Brier {(bb - model_b) / bb:+.1%}  LogLoss {(bl - model_ll) / bl:+.1%}")

# ── Per-league breakdown ──
print("\n── PER-LEAGUE ──")
for lg in sorted(set(m['lg'] for m, _, _, _, _, _ in preds)):
    lp = [p for p in preds if p[0]['lg'] == lg]
    if len(lp) < 10:
        continue
    b_b = sum((base[0] - (m['res'] == 'H'))**2 + (base[1] - (m['res'] == 'D'))**2 + (base[2] - (m['res'] == 'A'))**2 for m, _, _, _, _, _ in lp) / len(lp)
    b_m = brier(lp)
    d_m = direction_hit(lp)
    print(f"  {lg:6s}: n={len(lp):5d}  Brier model={b_m:.4f}  base={b_b:.4f}  gain={(b_b-b_m)/b_b:+.1%}  direction={d_m:.2%}")

# ── Produce training-only, predict last season (for harness baseline comparison) ──
print("\n── HARNESS: TRAIN 2021-22..2024-25, PREDICT 2025-26 ──")
cutoff = datetime(2025, 7, 1)  # 2025-26 season start
train_rows = [r for r in rows if r['date'] < cutoff]
test_rows = [r for r in rows if r['date'] >= cutoff]

model2 = Model()
train_preds = []
for m in train_rows:
    model2.update(m)
for m in test_rows:
    if model2.seen[m['home']] >= 6 and model2.seen[m['away']] >= 6:
        lh, la = model2.lam(m['lg'], m['home'], m['away'])
        H, D, A, _, _ = probs(lh, la)
        train_preds.append((m, H, D, A, lh, la))
    model2.update(m)

print(f"train: {len(train_rows):,}  test: {len(test_rows):,}  predictions: {len(train_preds):,}")

leagues_5082 = sorted(set(r['lg'] for r in rows))
for lg in leagues_5082:
    tp = [p for p in train_preds if p[0]['lg'] == lg]
    if len(tp) < 5:
        continue
    b_b = sum((base[0] - (m['res'] == 'H'))**2 + (base[1] - (m['res'] == 'D'))**2 + (base[2] - (m['res'] == 'A'))**2 for m, _, _, _, _, _ in tp) / len(tp)
    b_m = brier(tp)
    d_m = direction_hit(tp)
    refused = len([r for r in test_rows if r['lg'] == lg]) - len(tp)
    print(f"  {lg:6s}: train={sum(1 for r in train_rows if r['lg']==lg):4d} test={len(tp):3d} refused={refused} Brier={b_m:.4f} vs base={b_b:.4f} gain={(b_b-b_m)/b_b:+.1%} dir={d_m:.2%}")

# ── Save reference artifact ──
artifact = {
    'engine': 'Dixon-Coles reference trainer (Python)',
    'spec': 'ENGINE_SPEC.md v1.0',
    'store': 'pitch-rating-full-5082-D1D2-2026-08-05.json',
    'store_rows': len(rows),
    'predictions_full': len(preds),
    'brier_model': round(model_b, 6),
    'brier_base': round(bb, 6),
    'brier_gain_pct': round((bb - model_b) / bb * 100, 2),
    'logloss_model': round(model_ll, 6),
    'logloss_base': round(bl, 6),
    'direction': round(model_dir, 4),
    'constants': {
        'LR': 0.055, 'DECAY': 0.0022, 'HFA_LR': 0.010,
        'new_team_mult': 1.6, 'new_team_games': 8,
        'home_extra_decay': 0.999, 'min_games': 6,
        'RHO': -0.06, 'lambda_clamp': [0.05, 6.0],
        'hfa_clamp': [0.05, 0.55], 'home_extra_clamp': [-0.25, 0.25]
    },
    'per_league_harness': {}
}

for lg in leagues_5082:
    tp = [p for p in train_preds if p[0]['lg'] == lg]
    if len(tp) < 5:
        continue
    b_b = sum((base[0] - (m['res'] == 'H'))**2 + (base[1] - (m['res'] == 'D'))**2 + (base[2] - (m['res'] == 'A'))**2 for m, _, _, _, _, _ in tp) / len(tp)
    b_m = brier(tp)
    refused = len([r for r in test_rows if r['lg'] == lg]) - len(tp)
    artifact['per_league_harness'][lg] = {
        'train': sum(1 for r in train_rows if r['lg'] == lg),
        'scored': len(tp),
        'refused': refused,
        'brier_dc': round(b_m, 4),
        'brier_base': round(b_b, 4),
        'gain_pct': round((b_b - b_m) / b_b * 100, 1),
        'direction': round(direction_hit(tp), 3)
    }

os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'audit_work'), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), '..', 'audit_work', 'engine_reference_artifact.json'), 'w') as f:
    json.dump(artifact, f, indent=2)
print("\nReference artifact saved to audit_work/engine_reference_artifact.json")
