import json
G = json.load(open('/home/user/rpl/goals_replay.json'))
G = [g for g in G if g['evg'] is not None]
n=len(G)
mean=lambda a: sum(a)/len(a) if a else float('nan')
print("games:",n,"| actual O1.5 %.1f%% O2.5 %.1f%% O3.5 %.1f%% | draw %.1f%% | mean tot %.2f"%(
 100*mean([g['tot']>=2 for g in G]),100*mean([g['tot']>=3 for g in G]),100*mean([g['tot']>=4 for g in G]),
 100*mean([g['hg']==g['ag'] for g in G]),mean([g['tot'] for g in G])))

# --- bucket table by EV-G region
bins=[(0,2.2,'<2.2 LOW'),(2.2,2.5,'2.2-2.5'),(2.5,2.8,'2.5-2.8'),(2.8,3.2,'3.0-3.2'),(3.2,99,'>3.2 HIGH')]
print("\n== EV-G region -> realised ==")
print("%-11s %4s %6s %6s %6s %6s %6s %6s %6s"%("region","n","exp","act","bias","O1.5%","O2.5%","O3.5%","draw%"))
for lo,hi,lab in bins:
    b=[g for g in G if lo<=g['evg']<hi]
    if not b: continue
    print("%-11s %4d %6.2f %6.2f %+6.2f %6.1f %6.1f %6.1f %6.1f"%(lab,len(b),mean([g['evg'] for g in b]),mean([g['tot'] for g in b]),
      mean([g['evg']-g['tot'] for g in b]),100*mean([g['tot']>=2 for g in b]),100*mean([g['tot']>=3 for g in b]),
      100*mean([g['tot']>=4 for g in b]),100*mean([g['hg']==g['ag'] for g in b])))

# --- failure classes: big miss |err|>=2
big=[g for g in G if abs(g['evg']-g['tot'])>=2]
print("\n== big miss |err|>=2: n=%d (%.1f%%) ==" % (len(big),100*len(big)/n))
over=[g for g in big if g['evg']>g['tot']]; under=[g for g in big if g['evg']<g['tot']]
print("over-predict (shootout expected, low landed): %d | under-predict: %d"%(len(over),len(under)))
def cohort(name,f):
    c=[g for g in G if f(g)]
    if not c: return
    bmc=[g for g in c if abs(g['evg']-g['tot'])>=2]
    print("  %-34s n=%3d  big-miss %.1f%%  MAE %.3f  bias %+.2f"%(name,len(c),100*len(bmc)/len(c),mean([abs(g['evg']-g['tot']) for g in c]),mean([g['evg']-g['tot'] for g in c])))
print("\n== cohort failure rates ==")
cohort("cup games (CUP)", lambda g:'CUP' in str(g['comp']).upper() or 'Cup' in str(g['comp']))
cohort("league games (RPL)", lambda g:g['comp']=='RPL')
cohort("cold start (either side)", lambda g:g['cold'])
cohort("no H2H section", lambda g:g['h2hN']==0)
cohort("thin paths (<20)", lambda g:g['npaths']<20)
cohort("zone strong/win (confident)", lambda g:g['zone'] in ('strong','win'))
cohort("zone toss", lambda g:g['zone']=='toss')
cohort("expected HIGH >3.2", lambda g:g['evg']>=3.2)
cohort("expected LOW <2.2", lambda g:g['evg']<2.2)
# cup detail: pens draws at 90min
cup=[g for g in G if 'CUP' in str(g['comp']).upper() or 'Cup' in str(g['comp'])]
print("  cup bucket: n=%d mean exp %.2f mean act %.2f draw%% %.1f"%(len(cup),mean([g['evg'] for g in cup]),mean([g['tot'] for g in cup]),100*mean([g['hg']==g['ag'] for g in cup])))

# --- worst 12 misses
print("\n== worst misses ==")
for g in sorted(G,key=lambda x:-abs(x['evg']-x['tot']))[:12]:
    print("  %s %-26s exp %.2f -> %d-%d (tot %d) err %+.1f zone=%s"%(g['date'],(str(g['h'])+' v '+str(g['a'])),g['evg'],g['hg'],g['ag'],g['tot'],g['evg']-g['tot'],g['zone']))
