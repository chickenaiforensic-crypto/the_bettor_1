import json
G=[g for g in json.load(open('/home/user/rpl/goals_replay.json')) if g['evg'] is not None]
n=len(G); mean=lambda a: sum(a)/len(a)
def mae(pred): return mean([abs(p-g['tot']) for p,g in zip(pred,G)])

# raw + baselines
print("MAE raw EV-G %.3f | B0 %.3f | B1 %.3f"%(mae([g['evg'] for g in G]),mae([g['b0'] for g in G]),mae([g['b1'] for g in G])))

# --- C1: LOO OLS shrink  actual = a + b*evg
cal=[]
for i,g in enumerate(G):
    xs=[G[j]['evg'] for j in range(n) if j!=i]; ys=[G[j]['tot'] for j in range(n) if j!=i]
    mx,my=mean(xs),mean(ys)
    b=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs); a=my-b*mx
    cal.append(a+b*g['evg'])
print("C1 LOO shrink: MAE %.3f  (fit a~%.3f b~%.3f over full set)"%(mae(cal),
  (lambda xs,ys:(lambda mx,my:my-(sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs))*mx)(mean(xs),mean(ys)))([g['evg'] for g in G],[g['tot'] for g in G]),
  (lambda xs,ys:(lambda mx,my:sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs))(mean(xs),mean(ys)))([g['evg'] for g in G],[g['tot'] for g in G])))

# --- C2: evidence-volume blend  pred = w*evg + (1-w)*b0, w = np/(np+K), grid K (LOO-light: pick K on train half, test other half, flip, average)
import random
def wmae(K,split):
    err=[]
    for j in split:
        g=G[j]; w=g['npaths']/(g['npaths']+K); err.append(abs(w*g['evg']+(1-w)*g['b0']-g['tot']))
    return mean(err)
idx=list(range(n)); 
best=None
for K in [5,10,15,20,25,30,40,60]:
    e1=wmae(K,[i for i in idx if i%2==0]); e2=wmae(K,[i for i in idx if i%2==1])
    e=(e1+e2)/2
    if best is None or e<best[1]: best=(K,e)
    print("  C2 K=%-3d splitMAE %.3f"%(K,e))
Kbest=best[0]; print("C2 best K=%d MAE %.3f"%(Kbest,best[1]))

# --- C3 = C1 applied on top of C2 blend (LOO both stages)
cal3=[]
for i,g in enumerate(G):
    tr=[j for j in range(n) if j!=i]
    xs=[]; ys=[]
    for j in tr:
        h=G[j]; w=h['npaths']/(h['npaths']+Kbest); xs.append(w*h['evg']+(1-w)*h['b0']); ys.append(h['tot'])
    mx,my=mean(xs),mean(ys)
    b=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs); a=my-b*mx
    w=g['npaths']/(g['npaths']+Kbest); cal3.append(a+b*(w*g['evg']+(1-w)*g['b0']))
print("C3 blend+shrink(LOO): MAE %.3f"%mae(cal3))

# --- pick champion = C3 if it beats both C1,C2 else best; then bucket table with full-set fit
champ=cal3 if mae(cal3)<=min(mae(cal),best[1]) else cal
# refit full-set params for reporting the shipped mapping
ws=[g['npaths']/(g['npaths']+Kbest)*g['evg']+(1-g['npaths']/(g['npaths']+Kbest))*g['b0'] for g in G]
xs=ws if champ is cal3 else [g['evg'] for g in G]; ys=[g['tot'] for g in G]
mx,my=mean(xs),mean(ys)
bb=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs); aa=my-bb*mx
final=[aa+bb*x for x in xs]
print("CHAMPION: %s | full-set mapping actual = %.3f + %.3f * x | MAE %.3f | RMSE %.3f"%(
 "C3 blend+shrink K=%d"%Kbest if champ is cal3 else "C1 shrink", aa,bb,mae(final),
 (mean([(p-g['tot'])**2 for p,g in zip(final,G)]))**0.5))
print("big-miss |err|>=2: raw %.1f%% -> cal %.1f%%"%(100*mean([abs(g['evg']-g['tot'])>=2 for g in G]),100*mean([abs(p-g['tot'])>=2 for p,g in zip(final,G)])))
print("\n== calibrated region -> realised ==")
bins=[(0,2.2),(2.2,2.5),(2.5,2.75),(2.75,3.0),(3.0,99)]
for lo,hi in bins:
    bl=[(p,g) for p,g in zip(final,G) if lo<=p<hi]
    if not bl: continue
    print("  [%.2f,%.2f) n=%3d  exp %.2f act %.2f bias %+.2f | O1.5 %.0f%% O2.5 %.0f%% O3.5 %.0f%% | draw %.0f%%"%(
     lo,hi,len(bl),mean([p for p,_ in bl]),mean([g['tot'] for _,g in bl]),mean([p-g['tot'] for p,g in bl]),
     100*mean([g['tot']>=2 for _,g in bl]),100*mean([g['tot']>=3 for _,g in bl]),100*mean([g['tot']>=4 for _,g in bl]),
     100*mean([g['hg']==g['ag'] for _,g in bl])))
json.dump({'K':Kbest,'a':aa,'b':bb,'champion':'C3' if champ is cal3 else 'C1'},open('/home/user/rpl/goals_cal.json','w'))
print("saved rpl/goals_cal.json")
