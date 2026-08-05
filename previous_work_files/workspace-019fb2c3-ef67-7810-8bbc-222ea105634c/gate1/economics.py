import pickle, math
from scipy import stats
AF,AG=pickle.load(open("/home/user/gate1/multi.pkl","rb"))

print("="*84)
print("A. IS 2026's LOW DRAW RATE A LEAGUE-WIDE EFFECT OR SELECTION-SPECIFIC?")
print("="*84)
print(f"{'season':8s} {'ALL graded fixtures':>22s} {'FIRED subset':>20s}")
print(f"{'':8s} {'n':>6} {'draw%':>8} {'home%':>7} {'n':>6} {'draw%':>8} {'home%':>7}")
for s in sorted(set(x['season'] for x in AG)):
    g=[x for x in AG if x['season']==s]; f=[x for x in AF if x['season']==s]
    gd=sum(1 for x in g if x['res']=='D')/len(g); gh=sum(1 for x in g if x['res']=='H')/len(g)
    fd=sum(1 for x in f if x['res']=='D')/len(f); fh=sum(1 for x in f if x['res']=='H')/len(f)
    mark=" <<<" if s=="2026" else ""
    print(f"{s:8s} {len(g):6d} {gd:8.1%} {gh:7.1%} {len(f):6d} {fd:8.1%} {fh:7.1%}{mark}")

g26=[x for x in AG if x['season']=='2026']
d26=sum(1 for x in g26 if x['res']=='D')
gall=[x for x in AG if x['season']!='2026']
dall=sum(1 for x in gall if x['res']=='D')/len(gall)
print(f"\n2026 ALL graded fixtures draw rate: {d26}/{len(g26)} = {d26/len(g26):.1%}")
print(f"Historical ALL graded draw rate   : {dall:.1%}")
print(f"-> 2026 league-wide draw rate is {'LOW' if d26/len(g26)<dall-0.03 else 'NORMAL'}")
print(f"   So the 1-in-36 is {'partly league-wide' if d26/len(g26)<dall-0.03 else 'SELECTION-SPECIFIC luck'}")

print("\n"+"="*84)
print("B. ECONOMICS — closing odds on fired selections")
print("="*84)
wo=[x for x in AF if x['ch']]
print(f"Fired selections with closing odds: {len(wo)}/{len(AF)}")
mean_odds=sum(x['ch'] for x in wo)/len(wo)
print(f"Mean closing home price: {mean_odds:.3f}  (implied {1/mean_odds:.1%})")
med=sorted(x['ch'] for x in wo)[len(wo)//2]
print(f"Median closing home price: {med:.3f}")
W=sum(1 for x in wo if x['res']=='H')
print(f"Actual home-win rate: {W}/{len(wo)} = {W/len(wo):.1%}")

pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in wo)
print(f"\nFLAT-STAKE ROI backing every fired selection at closing price:")
print(f"  staked {len(wo)} units, P&L {pnl:+.2f} units, ROI {pnl/len(wo):+.2%}")

# devigged market prob vs actual
dv=[]
for x in wo:
    if x['cd'] and x['ca']:
        t=1/x['ch']+1/x['cd']+1/x['ca']
        dv.append((1/x['ch'])/t)
if dv:
    print(f"\nMean de-vigged market P(home) on fired: {sum(dv)/len(dv):.1%}")
    print(f"Actual                                : {W/len(wo):.1%}")
    print(f"EDGE vs market: {W/len(wo)-sum(dv)/len(dv):+.1%}")

print("\n"+"="*84)
print("C. ROI BY THRESHOLD — is ANY cut profitable at closing prices?")
print("="*84)
print(f"{'cut':>6} {'n':>6} {'hit':>8} {'meanOdds':>9} {'ROI':>9} {'vs devig':>9}")
for cut in [0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]:
    v=[x for x in AG if x['xm']>=cut and x['ch'] and x['cd'] and x['ca']]
    if len(v)<20: continue
    w=sum(1 for x in v if x['res']=='H')
    pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
    mo=sum(x['ch'] for x in v)/len(v)
    dvp=sum((1/x['ch'])/(1/x['ch']+1/x['cd']+1/x['ca']) for x in v)/len(v)
    print(f"{cut:6.1f} {len(v):6d} {w/len(v):8.1%} {mo:9.3f} {pnl/len(v):+8.2%} {w/len(v)-dvp:+8.1%}")

print("\n"+"="*84)
print("D. 2026 ALONE — would it have been profitable?")
print("="*84)
v=[x for x in AF if x['season']=='2026' and x['ch']]
w=sum(1 for x in v if x['res']=='H')
pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
print(f"  {len(v)} bets, {w} wins ({w/len(v):.1%}), mean odds {sum(x['ch'] for x in v)/len(v):.3f}")
print(f"  P&L {pnl:+.2f} units, ROI {pnl/len(v):+.1%}")
print("  ^ this is why the doc looks good. One season.")

print("\n"+"="*84)
print("E. THE HONEST NUMBER")
print("="*84)
def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n
    c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h,c+h
W=sum(1 for x in AF if x['res']=='H');N=len(AF)
lo,hi=wilson(W,N)
print(f"  xMargin>=1.0, 15 seasons, 3 leagues: {W}/{N} = {W/N:.1%}  CI [{lo:.1%},{hi:.1%}]")
print(f"  Doc's claim: 86% CI [75%,97%]")
print(f"  The doc's CI does NOT contain the true value. It was never a 86% system.")
