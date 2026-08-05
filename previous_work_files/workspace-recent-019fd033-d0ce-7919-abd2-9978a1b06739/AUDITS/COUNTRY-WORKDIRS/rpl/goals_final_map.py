import json
G=[g for g in json.load(open('/home/user/rpl/goals_replay.json')) if g['evg'] is not None]
n=len(G); mean=lambda a: sum(a)/len(a)
K=10
for g in G:
    w=g['npaths']/(g['npaths']+K)
    g['c2']=w*g['evg']+(1-w)*g['b0']
print("C2 est: mean %.3f | MAE %.3f"%(mean([g['c2'] for g in G]),mean([abs(g['c2']-g['tot']) for g in G])))
# sweep a LOW threshold and a HIGH threshold for categorical separation
print("\nregion definition sweep (C2 scale):")
for lo,hi in [(2.35,2.75),(2.4,2.8),(2.45,2.85),(2.5,2.9)]:
    low=[g for g in G if g['c2']<lo]; mid=[g for g in G if lo<=g['c2']<hi]; high=[g for g in G if g['c2']>=hi]
    print(" lo=%.2f hi=%.2f | LOW n=%3d U2.5 %.0f%% draw %.0f%% | MID n=%3d O2.5 %.0f%% | HIGH n=%3d O1.5 %.0f%% O2.5 %.0f%%"%(
      lo,hi,len(low),100*mean([g['tot']<=2 for g in low]),100*mean([g['hg']==g['ag'] for g in low]),
      len(mid),100*mean([g['tot']>=3 for g in mid]),
      len(high),100*mean([g['tot']>=2 for g in high]),100*mean([g['tot']>=3 for g in high])))
# lock 2.40 / 2.80
lo,hi=2.40,2.80
low=[g for g in G if g['c2']<lo]; mid=[g for g in G if lo<=g['c2']<hi]; high=[g for g in G if g['c2']>=hi]
def row(name,b):
    print(" %-5s n=%3d exp %.2f act %.2f | O1.5 %.0f%% U2.5 %.0f%% O2.5 %.0f%% O3.5 %.0f%% draw %.0f%% | big-miss %.0f%%"%(
     name,len(b),mean([g['c2'] for g in b]),mean([g['tot'] for g in b]),100*mean([g['tot']>=2 for g in b]),
     100*mean([g['tot']<=2 for g in b]),100*mean([g['tot']>=3 for g in b]),100*mean([g['tot']>=4 for g in b]),
     100*mean([g['hg']==g['ag'] for g in b]),100*mean([abs(g['c2']-g['tot'])>=2 for g in b])))
print("\nFINAL C2 region table (replay 633, thresholds %.2f/%.2f):"%(lo,hi))
row("LOW",low); row("MID",mid); row("HIGH",high)
# categorical call scorecard: UNDER call=LOW region tot<=2 ; OVER15 call=MID+HIGH tot>=2 ; no-call elsewhere
u=[g for g in low if g['tot']<=2]; o=[g for g in mid+high if g['tot']>=2]
print("\nCALLS: UNDER-2.5 in LOW: %d/%d = %.1f%% | OVER-1.5 in MID+HIGH: %d/%d = %.1f%% | coverage %.0f%%"%(
 len(u),len(low),100*len(u)/len(low),len(o),len(mid+high),100*len(o)/len(mid+high),100*(len(low)+len(mid)+len(high))/n))
# determinism re-check of champion on shuffled order
import random
H=G[:]; random.seed(7); random.shuffle(H)
print("MAE shuffled %.3f (must equal 1.301)"%mean([abs(g['c2']-g['tot']) for g in H]))
json.dump({'K':K,'lo':lo,'hi':hi,
 'table':{'LOW':{'n':len(low),'o15':100*mean([g['tot']>=2 for g in low]),'u25':100*mean([g['tot']<=2 for g in low]),'o25':100*mean([g['tot']>=3 for g in low]),'o35':100*mean([g['tot']>=4 for g in low]),'draw':100*mean([g['hg']==g['ag'] for g in low]),'act':mean([g['tot'] for g in low])},
          'MID':{'n':len(mid),'o15':100*mean([g['tot']>=2 for g in mid]),'u25':100*mean([g['tot']<=2 for g in mid]),'o25':100*mean([g['tot']>=3 for g in mid]),'o35':100*mean([g['tot']>=4 for g in mid]),'draw':100*mean([g['hg']==g['ag'] for g in mid]),'act':mean([g['tot'] for g in mid])},
          'HIGH':{'n':len(high),'o15':100*mean([g['tot']>=2 for g in high]),'u25':100*mean([g['tot']<=2 for g in high]),'o25':100*mean([g['tot']>=3 for g in high]),'o35':100*mean([g['tot']>=4 for g in high]),'draw':100*mean([g['hg']==g['ag'] for g in high]),'act':mean([g['tot'] for g in high])}}},
open('/home/user/rpl/goals_final.json','w'))
print("saved rpl/goals_final.json")
