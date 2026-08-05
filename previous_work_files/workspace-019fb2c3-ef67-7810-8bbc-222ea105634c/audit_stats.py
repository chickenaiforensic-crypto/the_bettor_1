from scipy import stats
import math

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n
    d=1+z*z/n
    c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (c-h, c+h)

def cp(k,n):  # Clopper-Pearson
    lo = stats.beta.ppf(0.025,k,n-k+1) if k>0 else 0
    hi = stats.beta.ppf(0.975,k+1,n-k) if k<n else 1
    return lo,hi

print("=== 1. HEADLINE CI CHECK: 31/36 ===")
for name,f in [("Wilson",wilson),("Clopper-Pearson",cp)]:
    lo,hi=f(31,36); print(f"  {name:16s} {31/36:.3f}  [{lo:.3f}, {hi:.3f}]")

print("\n=== 2. Doc's rule (AND) vs xMargin alone ===")
print(f"  AND rule (doc S5):  29/34 = {29/34:.3f}   CI {tuple(round(x,3) for x in wilson(29,34))}")
print(f"  xMargin>=1.0 alone: 31/36 = {31/36:.3f}   CI {tuple(round(x,3) for x in wilson(31,36))}")
print(f"  -> normScore filter REMOVED 2 fixtures, both WINS (36-34=2, 31-29=2)")

print("\n=== 3. 'true rate 75% produces 31/36-or-better ~8% of time' ===")
for p in [0.70,0.75,0.78,0.80]:
    pv=1-stats.binom.cdf(30,36,p)
    print(f"  P(X>=31 | n=36, p={p:.2f}) = {pv:.4f}")

print("\n=== 4. TRUE OUT-OF-SAMPLE = FINLAND ONLY (9/11) ===")
lo,hi=wilson(9,11); print(f"  9/11 = {9/11:.3f}  Wilson [{lo:.3f}, {hi:.3f}]")
lo,hi=cp(9,11);     print(f"          Clopper-Pearson [{lo:.3f}, {hi:.3f}]")
pv=1-stats.binom.cdf(8,11,0.53)
print(f"  vs Finland baseline 53%: P(X>=9|n=11,p=.53) = {pv:.4f}  (one-sided)")

print("\n=== 5. DRAW SUPPRESSION: 1 draw in 36 ===")
for p in [0.21,0.18,0.15,0.12,0.10]:
    pv=stats.binom.cdf(1,36,p)
    print(f"  P(<=1 draw | n=36, true draw rate {p:.0%}) = {pv:.4f}   expected draws {36*p:.1f}")

print("\n=== 6. THRESHOLD SENSITIVITY — implied band performance ===")
cuts={0.6:(70,48),0.8:(54,39),1.0:(36,31),1.2:(26,23)}
print("  stated cuts:")
for c,(n,w) in cuts.items(): print(f"    >={c}: {w}/{n} = {w/n:.3f}")
print("  implied bands (differences):")
bands=[("0.6-0.8",70-54,48-39),("0.8-1.0",54-36,39-31),("1.0-1.2",36-26,31-23),(">=1.2",26,23)]
for nm,n,w in bands:
    lo,hi=wilson(w,n)
    print(f"    {nm:9s} {w:2d}/{n:2d} = {w/n:.3f}  CI [{lo:.2f},{hi:.2f}]")

print("\n=== 7. Is >=1.0 significantly better than the 0.8-1.0 band? ===")
tbl=[[31,5],[8,10]]
odr,p=stats.fisher_exact(tbl)
print(f"  Fisher exact  >=1.0 (31/36) vs 0.8-1.0 (8/18): p={p:.4f}  OR={odr:.2f}")
tbl2=[[31,5],[17,17]]
odr,p=stats.fisher_exact(tbl2)
print(f"  Fisher exact  >=1.0 (31/36) vs 0.6-1.0 (17/34): p={p:.4f}  OR={odr:.2f}")

print("\n=== 8. FINLAND BAND MONOTONICITY ===")
fin=[("-1.0..-0.3",8,3),("-0.3..0.0",7,2),("0.0..0.3",16,6),("0.3..0.6",13,10),("0.6..1.0",7,3),(">=1.0",11,9)]
tot=sum(n for _,n,_ in fin); totw=sum(w for _,_,w in fin)
for nm,n,w in fin:
    lo,hi=wilson(w,n); print(f"  {nm:11s} {w:2d}/{n:2d} = {w/n:.2f}  CI [{lo:.2f},{hi:.2f}]")
print(f"  totals {totw}/{tot} = {totw/tot:.3f}  (doc states Finland baseline 53%)")
print("  NON-MONOTONIC: 0.3-0.6 scores .77 but 0.6-1.0 scores .43")
odr,p=stats.fisher_exact([[10,3],[3,4]])
print(f"  Fisher 0.3-0.6 (10/13) vs 0.6-1.0 (3/7): p={p:.4f}")

print("\n=== 9. CELL TABLE ARITHMETIC (S5) ===")
print(f"  stated cells: 34 + 37 + 105 = {34+37+105}   vs 179 fixtures -> missing {179-(34+37+105)}")
print(f"  missing cell (normScore<0.30 AND xMargin>=1.0) = 36-34 = 2 -> {34+37+105+2} of 179, still short 1")

print("\n=== 10. ECONOMICS — what odds are needed? ===")
print("  break-even decimal odds = 1/p")
for p,lab in [(0.861,"86.1% point est"),(0.78,"78% doc's plan"),(0.75,"75% CI lower")]:
    print(f"    {lab:18s}需 odds > {1/p:.3f}")
print("\n  EV per unit staked at various offered prices:")
print(f"  {'odds':>6} {'implied':>8} | " + " | ".join(f"EV@{p:.0%}" for p in [0.861,0.78,0.75]))
for o in [1.15,1.20,1.25,1.30,1.35,1.40,1.50,1.60]:
    row=f"  {o:6.2f} {1/o:8.1%} | "
    row+=" | ".join(f"{(p*o-1):+7.1%}" for p in [0.861,0.78,0.75])
    print(row)

print("\n=== 11. ACCUMULATOR + VIG ===")
print("  4-leg acca, each leg true p, priced at fair-minus-margin (5% overround/leg):")
for p in [0.861,0.78]:
    fair=1/p; priced=fair*0.95
    accp=p**4; accodds=priced**4
    print(f"    p={p:.3f}: acca hit {accp:.3f}, odds {accodds:.2f}, EV {(accp*accodds-1):+.1%}")
    # with correlation, hit rate lower
    print(f"      if legs correlated (effective p^3.5): hit {p**3.5:.3f}, EV {(p**3.5*accodds-1):+.1%}")

print("\n=== 12. SAMPLE SIZE PLANNING (how many calls to pin the rate) ===")
for n in [36,75,150,300,500]:
    k=round(0.86*n); lo,hi=wilson(k,n)
    print(f"  n={n:4d} at 86%: CI [{lo:.3f},{hi:.3f}]  width {hi-lo:.3f}")
print("\n  Calls needed to DISTINGUISH 86% from 75% (80% power, alpha .05, one-sided):")
from scipy.stats import norm as N
p0,p1=0.75,0.86
za,zb=N.ppf(0.95),N.ppf(0.80)
nreq=((za*math.sqrt(p0*(1-p0))+zb*math.sqrt(p1*(1-p1)))/(p1-p0))**2
print(f"    n ≈ {math.ceil(nreq)} calls  (= {math.ceil(nreq)/0.20:.0f} fixtures at 20% coverage)")
p0=0.70
nreq=((N.ppf(0.95)*math.sqrt(p0*(1-p0))+zb*math.sqrt(p1*(1-p1)))/(0.86-p0))**2
print(f"    vs 70%: n ≈ {math.ceil(nreq)} calls")

print("\n=== 13. COVERAGE / VOLUME REALITY ===")
print(f"  doc: 36 calls / 179 fixtures = {36/179:.1%} coverage")
print(f"  300 calls at that rate = {300/(36/179):.0f} fixtures")
print(f"  doc claims 1500 fixtures -> implies {300/1500:.0%} coverage (consistent-ish)")
print("  Allsvenskan full season = 16 teams x 30 = 240 matches; doc graded 57 (24%)")
print("  Eliteserien full season = 16 x 30 = 240; doc graded 60 (25%)")
print("  Veikkausliiga = 12 x 27 = ~162 (+ championship round); doc graded 62 (38%)")
