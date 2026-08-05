import pickle, math
from scipy import stats
AF,AG=pickle.load(open("/home/user/gate1/multi.pkl","rb"))

print("="*84); print("F. ARE THE HIGH CUTS REAL, OR THE SAME TRAP AGAIN?"); print("="*84)
def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
for cut in [1.6,1.8,2.0]:
    v=[x for x in AG if x['xm']>=cut and x['ch']]
    w=sum(1 for x in v if x['res']=='H'); pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
    lo,hi=wilson(w,len(v))
    # ROI standard error via bootstrap
    import random; random.seed(0)
    boots=[]
    for _ in range(20000):
        s=[random.choice(v) for _ in v]
        boots.append(sum((x['ch']-1) if x['res']=='H' else -1 for x in s)/len(s))
    boots.sort()
    print(f"  cut {cut}: n={len(v):3d} hit {w/len(v):.1%} CI[{lo:.1%},{hi:.1%}] ROI {pnl/len(v):+.1%} "
          f"boot95[{boots[500]:+.1%},{boots[19500]:+.1%}]")
print("  -> ROI confidence intervals all straddle zero. No cut is demonstrably profitable.")

print("\n"+"="*84); print("G. WALK-FORWARD: pick best cut on past seasons, apply to next"); print("="*84)
seasons=sorted(set(x['season'] for x in AG))
tot_n=tot_pnl=0
print(f"{'test yr':8s} {'cut chosen':>10s} {'n':>4} {'hit':>7} {'ROI':>8}")
for i in range(5,len(seasons)):
    tr=[x for x in AG if x['season']<seasons[i] and x['ch']]
    te=[x for x in AG if x['season']==seasons[i] and x['ch']]
    best,bestroi=None,-9
    for cut in [0.8,1.0,1.2,1.4,1.6,1.8,2.0]:
        v=[x for x in tr if x['xm']>=cut]
        if len(v)<30: continue
        r=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)/len(v)
        if r>bestroi: bestroi,best=r,cut
    v=[x for x in te if x['xm']>=best]
    if not v: continue
    w=sum(1 for x in v if x['res']=='H'); pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
    tot_n+=len(v); tot_pnl+=pnl
    print(f"{seasons[i]:8s} {best:10.1f} {len(v):4d} {w/len(v):7.1%} {pnl/len(v):+7.1%}")
print(f"{'TOTAL':8s} {'':10s} {tot_n:4d} {'':7s} {tot_pnl/tot_n:+7.1%}")
print("  -> This is the honest simulation of actually USING the method. Negative.")

print("\n"+"="*84); print("H. DOES xMargin BEAT THE MARKET ANYWHERE? (calibration by market price)"); print("="*84)
print("  Grouping fired-eligible fixtures by market price, does high xMargin add info?")
wo=[x for x in AG if x['ch'] and x['cd'] and x['ca']]
print(f"  {'odds band':14s} {'n':>5} {'devig P':>8} {'actual':>8} {'edge':>7}  {'hi-xM n':>8} {'hi-xM act':>10} {'edge':>7}")
for lo_,hi_ in [(1.0,1.3),(1.3,1.5),(1.5,1.8),(1.8,2.2),(2.2,3.0),(3.0,99)]:
    v=[x for x in wo if lo_<=x['ch']<hi_]
    if len(v)<30: continue
    dv=sum((1/x['ch'])/(1/x['ch']+1/x['cd']+1/x['ca']) for x in v)/len(v)
    act=sum(1 for x in v if x['res']=='H')/len(v)
    hx=[x for x in v if x['xm']>=1.0]
    if len(hx)>=20:
        dvh=sum((1/x['ch'])/(1/x['ch']+1/x['cd']+1/x['ca']) for x in hx)/len(hx)
        acth=sum(1 for x in hx if x['res']=='H')/len(hx)
        print(f"  [{lo_:4.1f},{hi_:4.1f})   {len(v):5d} {dv:8.1%} {act:8.1%} {act-dv:+7.1%}  {len(hx):8d} {acth:10.1%} {acth-dvh:+7.1%}")
    else:
        print(f"  [{lo_:4.1f},{hi_:4.1f})   {len(v):5d} {dv:8.1%} {act:8.1%} {act-dv:+7.1%}  {'--':>8}")
print("  -> Within each price band, high-xMargin fixtures do NOT outperform the price.")
print("     The market has fully absorbed everything xMargin knows.")

print("\n"+"="*84); print("I. SUMMARY TABLE"); print("="*84)
W=sum(1 for x in AF if x['res']=='H'); N=len(AF); D=sum(1 for x in AF if x['res']=='D')
lo,hi=wilson(W,N)
rows=[("Doc claim (2026 only, n=36)","86.1%","2.8%","[75%,97%]","+22.6% (1 season)"),
      ("Replication of 2026 (exact)","86.1%","2.8%","[71%,94%]","+22.6%"),
      ("15 seasons, same spec, n=997",f"{W/N:.1%}",f"{D/N:.1%}",f"[{lo:.1%},{hi:.1%}]","-4.7%"),
      ("Walk-forward, cut re-chosen yearly","--","--","--",f"{tot_pnl/tot_n:+.1%}")]
print(f"  {'basis':36s} {'hit':>7} {'draw':>7} {'95% CI':>14} {'ROI':>18}")
for r in rows: print(f"  {r[0]:36s} {r[1]:>7} {r[2]:>7} {r[3]:>14} {r[4]:>18}")
