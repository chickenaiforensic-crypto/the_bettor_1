"""1) Strict held-out test. 2) Home/away FLIP detector for the 1xbet problem."""
import pickle, math
preds=pickle.load(open("preds.pkl","rb"))

print("="*86)
print("STRICT HELD-OUT TEST — model never saw 2024/25 & 2025/26 when predicting them")
print("="*86)
print("(walk-forward is already causal: each prediction used only prior matches)")
for seas in ['2223','2324','2425','2526']:
    s=[p for p in preds if p[0]['season']==seas]
    if len(s)<500: continue
    n=len(s)
    b=sum((p[1]-(p[0]['res']=='H'))**2+(p[2]-(p[0]['res']=='D'))**2+(p[3]-(p[0]['res']=='A'))**2 for p in s)/n
    base=(0.446,0.268,0.286)
    bb=sum((base[0]-(p[0]['res']=='H'))**2+(base[1]-(p[0]['res']=='D'))**2+(base[2]-(p[0]['res']=='A'))**2 for p in s)/n
    pr=sum(p[1] for p in s)/n; ac=sum(1 for p in s if p[0]['res']=='H')/n
    print(f"  {seas}: n={n:6,}  Brier {b:.4f} vs base {bb:.4f} ({(bb-b)/bb:+.1%})  "
          f"pred home {pr:.1%} actual {ac:.1%} (err {ac-pr:+.1%})")

print("\n"+"="*86)
print("FLIP DETECTOR — catching 1xbet-style home/away reversal")
print("="*86)
print("""
The problem: a feed lists 'Team A v Team B' but has the venue reversed, or an
AI parse swaps the sides. If undetected, the model rates the wrong side at home.

Detection without any market data:
  1. FIXTURE CHECK   - does the league calendar have this pair with this venue?
  2. SYMMETRY TEST   - compute P(home) both ways. If reversing the order gives a
                       much more plausible result vs the model's own prior, flag it.
  3. GROUND HISTORY  - has the stated home team ever hosted in this league?
""")

# demonstrate: how often would a flip be detectable by rating asymmetry?
import random
random.seed(3)
sample=random.sample(preds,20000)
detect=0; ambiguous=0
for m,H,D,A,lh,la in sample:
    # simulate the flip: pretend the away team was listed at home
    # model would then predict P(home) for the WRONG side
    # detectable if the two orderings differ a lot
    if abs(H-A)>0.15: detect+=1
    else: ambiguous+=1
print(f"  Of 20,000 fixtures: {detect/len(sample):.1%} have a large enough rating gap")
print(f"  that a flip produces an obviously wrong probability (|P(H)-P(A)|>15pt).")
print(f"  {ambiguous/len(sample):.1%} are near-even and a flip would be silent -> those")
print(f"  MUST be verified against a fixture list, not inferred.")
print()
print("  => Rule for the app: NEVER trust parsed venue. Always confirm the home team")
print("     against an official fixture source before rating. The model can flag")
print("     suspicious cases but cannot fix a flip on an even matchup.")

print("\n"+"="*86)
print("WORKED EXAMPLES — what the system outputs per fixture")
print("="*86)
ex=[p for p in preds if p[0]['season']=='2526'][:6]
print(f"  {'fixture':44s} {'pts':>4s} {'tier':>4s} {'H/D/A predicted':>22s} {'actual':>7s}")
for m,H,D,A,lh,la in ex:
    pts=round(100*H)
    tier='A+' if H>=.70 else 'A' if H>=.60 else 'B' if H>=.52 else 'C' if H>=.45 else 'D' if H>=.35 else 'E'
    fx=f"{m['home'][:20]} v {m['away'][:20]}"
    print(f"  {fx:44s} {pts:4d} {tier:>4s}   {H:.0%}/{D:.0%}/{A:.0%}  ({lh:.2f}-{la:.2f})  {m['res']:>5s}")
