import pickle,math,random
from scipy import stats
AF,AG=pickle.load(open("/home/user/gate1/multi.pkl","rb"))
seasons=sorted(set(x['season'] for x in AG))
random.seed(1)

# reproduce walk-forward, collect individual bets
bets=[]
for i in range(5,len(seasons)):
    tr=[x for x in AG if x['season']<seasons[i] and x['ch']]
    te=[x for x in AG if x['season']==seasons[i] and x['ch']]
    best,bestroi=None,-9
    for cut in [0.8,1.0,1.2,1.4,1.6,1.8,2.0]:
        v=[x for x in tr if x['xm']>=cut]
        if len(v)<30: continue
        r=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)/len(v)
        if r>bestroi: bestroi,best=r,cut
    bets+=[x for x in te if x['xm']>=best]

pnl=sum((x['ch']-1) if x['res']=='H' else -1 for x in bets)
n=len(bets); roi=pnl/n
print(f"Walk-forward: n={n}, ROI {roi:+.1%}  (I mislabelled this 'negative' — it is POSITIVE)")
boots=[]
for _ in range(50000):
    s=[random.choice(bets) for _ in bets]
    boots.append(sum((x['ch']-1) if x['res']=='H' else -1 for x in s)/len(s))
boots.sort()
print(f"  bootstrap 95% CI: [{boots[1250]:+.1%}, {boots[48750]:+.1%}]")
print(f"  P(ROI<=0) under bootstrap: {sum(1 for b in boots if b<=0)/len(boots):.3f}")

# how much of it is 2024/2025/2026 (tiny n, huge ROI)?
late=[x for x in bets if x['season'] in ('2024','2025','2026')]
early=[x for x in bets if x['season'] not in ('2024','2025','2026')]
for nm,v in [("2017-2023",early),("2024-2026",late)]:
    p=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
    print(f"  {nm}: n={len(v):3d} ROI {p/len(v):+.1%}")
print("  -> 12 of 68 bets (2024-26) carry the result. Strip them and it's marginal.")

# Is the 1.8+ effect stable across leagues?
print("\nxMargin>=1.8 by league, all seasons:")
for lg in ['SWE','NOR','FIN']:
    v=[x for x in AG if x['xm']>=1.8 and x['lg']==lg and x['ch']]
    if not v: continue
    w=sum(1 for x in v if x['res']=='H'); p=sum((x['ch']-1) if x['res']=='H' else -1 for x in v)
    print(f"  {lg}: n={len(v):2d} hit {w/len(v):6.1%} ROI {p/len(v):+7.1%}")

# how many 1.8+ per season - is it even bettable volume?
print("\nxMargin>=1.8 fires per season:")
cnt={}
for x in AG:
    if x['xm']>=1.8: cnt[x['season']]=cnt.get(x['season'],0)+1
print("  "+", ".join(f"{s}:{cnt.get(s,0)}" for s in seasons))
print(f"  mean {sum(cnt.values())/len(seasons):.1f} fires/season across ALL THREE leagues")
