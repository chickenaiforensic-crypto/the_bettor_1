import math
from scipy import stats
from scipy.stats import poisson

def match_probs(lh,la,maxg=12):
    H=D=A=0.0
    for i in range(maxg):
        for j in range(maxg):
            p=poisson.pmf(i,lh)*poisson.pmf(j,la)
            if i>j: H+=p
            elif i==j: D+=p
            else: A+=p
    return H,D,A

print("=== A. WHAT DOES xMargin >= 1.0 IMPLY UNDER POISSON? ===")
print("  Nordic leagues run ~2.8-3.0 goals/game. Split so that lh-la = xMargin.")
print(f"  {'xMargin':>8} {'lh':>5} {'la':>5} | {'P(home)':>8} {'P(draw)':>8} {'P(away)':>8} | {'fair odds':>9}")
for tot in [2.8]:
    for xm in [0.6,0.8,1.0,1.2,1.5,1.72,2.0]:
        lh=(tot+xm)/2; la=(tot-xm)/2
        H,D,A=match_probs(lh,la)
        print(f"  {xm:8.2f} {lh:5.2f} {la:5.2f} | {H:8.1%} {D:8.1%} {A:8.1%} | {1/H:9.2f}")

print("\n=== B. THE DRAW ANOMALY — the central problem ===")
lh,la=1.9,0.9
H,D,A=match_probs(lh,la)
print(f"  A fixture with xMargin=1.0 (lh=1.90, la=0.90) has theoretical draw rate {D:.1%}")
print(f"  Doc observed 1 draw in 36 = 2.8%")
print(f"  Expected draws in 36 such fixtures: {36*D:.1f}")
pv=stats.binom.cdf(1,36,D)
print(f"  P(observing <=1 draw | n=36, p={D:.3f}) = {pv:.5f}")
print(f"  -> odds against ~ 1 in {1/pv:,.0f}")
print("\n  Even for a much stronger favourite (xMargin=1.5, lh=2.15 la=0.65):")
H2,D2,A2=match_probs(2.15,0.65)
print(f"    draw rate {D2:.1%}, expected {36*D2:.1f} draws, P(<=1) = {stats.binom.cdf(1,36,D2):.5f}")
print("\n  For 1 draw in 36 to be UNSURPRISING (p>0.10) the true draw rate must be <= ~10%.")
print("  No football fixture selection achieves a 10% draw rate. Typical floor is 15-18%")
print("  even for heavy favourites. This is the strongest signal in the document.")

print("\n=== C. IS THERE ACTUALLY AN EDGE? (market comparison) ===")
print("  If xMargin>=1.0 fixtures are ~75-80% home wins under Poisson, the market")
print("  prices them near there too. Bookmaker prices for such fixtures: 1.25-1.45.")
print(f"  {'assumed true p':>15} | " + " | ".join(f"{o:>7.2f}" for o in [1.25,1.30,1.35,1.40,1.45]))
for p in [0.861,0.80,0.78,0.75]:
    print(f"  {p:15.1%} | " + " | ".join(f"{(p*o-1):+6.1%} " for o in [1.25,1.30,1.35,1.40,1.45]))
print("\n  Poisson says these fixtures are ~76% home wins. Doc's 86% is 10pt above")
print("  the structural rate -> either genuine selection skill, or small-sample luck.")

print("\n=== D. LEAKAGE TEST: does the doc's xMargin actually use only prior matches? ===")
print("  Formula: H_scored_home = mean goals scored by HOME team in ITS home matches")
print("  Stated filter: 'all league matches with date < fixture date'")
print("  Min requirement: 3 prior home + 3 prior away matches.")
print("  -> With only 3-5 prior home matches, mean goals has enormous variance.")
n_matches=4; goals_var=1.3  # poisson-ish variance per match
se=math.sqrt(goals_var/n_matches)
print(f"  SE of a 4-match mean goals estimate ~ {se:.2f} goals")
print(f"  SE of xMargin (4 components, each ~{se:.2f}) ~ {math.sqrt(4*(0.5**2)*(goals_var/n_matches)):.2f} goals")
print("  -> xMargin=1.0 measured on 4 matches has a ~+/-1.1 95% interval. The")
print("     threshold is inside the noise band of its own estimator early in a season.")

print("\n=== E. NO OPPONENT-STRENGTH ADJUSTMENT ===")
print("  H_scored_home is a RAW mean. A home side whose first 5 home games were")
print("  against the bottom 5 gets an inflated xMargin with no correction.")
print("  Standard fix: Dixon-Coles / bivariate Poisson with attack+defence ratings,")
print("  which estimate team strength NET of schedule. The doc's r=+0.371 with match")
print("  margin is respectable but a fitted DC model typically reaches r=0.45-0.55.")

print("\n=== F. SCHEDULE BIAS IN NORDIC LEAGUES ===")
print("  Allsvenskan/Eliteserien/Veikkausliiga run Mar/Apr -> Oct/Nov (single calendar year).")
print("  Requiring 3 prior home + 3 prior away matches means NO fixture before ~matchweek 7.")
print("  So every graded fixture is from the middle/late season, when:")
print("   - tables have separated (favourites are genuinely stronger)")
print("   - relegation-threatened sides are demotivated late on")
print("  This is a real effect but it is SEASONAL, not predictive skill. It also means")
print("  the 179 'fixtures' are ~60% of each season, matching doc's 57/60/62 counts.")

print("\n=== G. WHAT WOULD FALSIFY THE SYSTEM? ===")
tests=[
 ("Draw rate returns to 15-20% on new data","near-certain","kills the 86%; true rate lands ~70-75%"),
 ("Hit rate on next 50 calls < 75%","live","system is a small-sample artefact"),
 ("Closing odds on fired calls avg < 1.30","likely","no edge even if 86% is real"),
 ("Non-Nordic league hit rate < 70%","untested","Nordic-specific, not football-general"),
]
for t,l,c in tests: print(f"  - {t:45s} [{l:12s}] {c}")
