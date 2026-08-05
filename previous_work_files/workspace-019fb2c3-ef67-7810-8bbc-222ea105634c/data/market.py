"""THE TEST THAT MATTERS: does any of this beat the closing price?
Also: is 'won both home and away' anything more than a proxy for being good?"""
import pickle, math
from collections import defaultdict
rows=pickle.load(open("all_matches.pkl","rb"))
teamseq=pickle.load(open("teamseq.pkl","rb"))

def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return c-h,c+h
def devig(oh,od,oa):
    t=1/oh+1/od+1/oa; return (1/oh)/t,(1/od)/t,(1/oa)/t

# index each match -> prior venue-form of both teams
key=lambda m:(m['lg'],m['season'],m['date'],m['home'],m['away'])
prior_state={}
for k,seq in teamseq.items():
    lg,seas,team=k
    for i,(dt,v,res,m) in enumerate(seq):
        prior=seq[:i]
        ph=[r for (_,vv,r,_) in prior if vv=='H']; pa=[r for (_,vv,r,_) in prior if vv=='A']
        pts=sum(3 if r=='W' else (1 if r=='D' else 0) for (_,_,r,_) in prior)
        ppg=pts/len(prior) if prior else None
        prior_state[(key(m),team)]=dict(nh=len(ph),na=len(pa),wh=('W' in ph),wa=('W' in pa),
            ppg=ppg,n=len(prior),
            hppg=sum(3 if r=='W' else (1 if r=='D' else 0) for r in ph)/len(ph) if ph else None,
            appg=sum(3 if r=='W' else (1 if r=='D' else 0) for r in pa)/len(pa) if pa else None)

MINH,MINA=3,3
elig=[]
for m in rows:
    if not(m['oh'] and m['od'] and m['oa']): continue
    hs=prior_state.get((key(m),m['home'])); as_=prior_state.get((key(m),m['away']))
    if not hs or not as_: continue
    if hs['nh']<MINH or hs['na']<MINA or as_['nh']<MINH or as_['na']<MINA: continue
    elig.append((m,hs,as_))
print(f"Eligible matches (both teams >=3 prior home & >=3 prior away, odds present): {len(elig):,}")

print("\n"+"="*100)
print("A. 'WON BOTH H&A' — IS IT A REAL SIGNAL OR JUST A PROXY FOR BEING GOOD?")
print("="*100)
both=[x for x in elig if x[1]['wh'] and x[1]['wa']]
notboth=[x for x in elig if not(x[1]['wh'] and x[1]['wa'])]
print(f"  HOME team has won both H&A: n={len(both):,}  mean prior PPG {sum(x[1]['ppg'] for x in both)/len(both):.2f}")
print(f"  HOME team has NOT         : n={len(notboth):,}  mean prior PPG {sum(x[1]['ppg'] for x in notboth)/len(notboth):.2f}")
print("  -> the categories differ enormously in raw quality. Any raw comparison is confounded.")

print("\n"+"="*100)
print("B. THE DECISIVE TEST — actual vs de-vigged closing price, by category")
print("="*100)
def report(label, subset, outcome='H'):
    if len(subset)<200: print(f"  {label:44s} n={len(subset):,} too small"); return
    act=sum(1 for m,_,_ in subset if m['res']==outcome)/len(subset)
    mk=sum(devig(m['oh'],m['od'],m['oa'])[{'H':0,'D':1,'A':2}[outcome]] for m,_,_ in subset)/len(subset)
    o={'H':'oh','D':'od','A':'oa'}[outcome]
    roi=sum((m[o]-1) if m['res']==outcome else -1 for m,_,_ in subset)/len(subset)
    lo,hi=wilson(sum(1 for m,_,_ in subset if m['res']==outcome),len(subset))
    flag=" <<<" if abs(act-mk)>0.02 and len(subset)>2000 else ""
    print(f"  {label:44s} n={len(subset):7,} act {act:6.1%} mkt {mk:6.1%} edge {act-mk:+6.1%} ROI {roi:+6.2%}{flag}")

print("  Betting the HOME team:")
report("all eligible", elig)
report("home won both H&A prior", both)
report("home NOT won both", notboth)
report("home won H only", [x for x in elig if x[1]['wh'] and not x[1]['wa']])
report("home won neither", [x for x in elig if not x[1]['wh'] and not x[1]['wa']])

print("\n  Betting the AWAY team:")
report("away won both H&A prior", [x for x in elig if x[2]['wh'] and x[2]['wa']], 'A')
report("away NOT won both", [x for x in elig if not(x[2]['wh'] and x[2]['wa'])], 'A')

print("\n  BOTH teams have won H&A (two strong sides):")
report("both teams 'BOTH' -> home", [x for x in elig if x[1]['wh'] and x[1]['wa'] and x[2]['wh'] and x[2]['wa']])
report("both teams 'BOTH' -> draw", [x for x in elig if x[1]['wh'] and x[1]['wa'] and x[2]['wh'] and x[2]['wa']],'D')

print("\n"+"="*100)
print("C. CONTROLLING FOR STRENGTH — within narrow market-price bands")
print("="*100)
print("  If 'won both H&A' is only a quality proxy, the edge vanishes once price is held fixed.")
print(f"  {'price band':16s} {'category':22s} {'n':>8s} {'actual':>8s} {'market':>8s} {'edge':>8s}")
for lo_,hi_ in [(1.0,1.5),(1.5,1.8),(1.8,2.2),(2.2,2.8),(2.8,10)]:
    band=[x for x in elig if lo_<=x[0]['oh']<hi_]
    for lbl,sub in [("home BOTH",[x for x in band if x[1]['wh'] and x[1]['wa']]),
                    ("home not BOTH",[x for x in band if not(x[1]['wh'] and x[1]['wa'])])]:
        if len(sub)<300: continue
        act=sum(1 for m,_,_ in sub if m['res']=='H')/len(sub)
        mk=sum(devig(m['oh'],m['od'],m['oa'])[0] for m,_,_ in sub)/len(sub)
        print(f"  [{lo_:.1f},{hi_:4.1f})       {lbl:22s} {len(sub):8,} {act:8.1%} {mk:8.1%} {act-mk:+8.1%}")

print("\n"+"="*100)
print("D. AWAY-FORM SPECIFIC: does a strong AWAY record predict away wins beyond price?")
print("="*100)
print(f"  {'away team prior away PPG':28s} {'n':>8s} {'away win':>9s} {'market':>8s} {'edge':>8s} {'ROI':>8s}")
for lo_,hi_ in [(0,0.5),(0.5,1.0),(1.0,1.5),(1.5,2.0),(2.0,3.1)]:
    sub=[x for x in elig if x[2]['appg'] is not None and lo_<=x[2]['appg']<hi_]
    if len(sub)<300: continue
    act=sum(1 for m,_,_ in sub if m['res']=='A')/len(sub)
    mk=sum(devig(m['oh'],m['od'],m['oa'])[2] for m,_,_ in sub)/len(sub)
    roi=sum((m['oa']-1) if m['res']=='A' else -1 for m,_,_ in sub)/len(sub)
    print(f"  away PPG [{lo_:.1f},{hi_:.1f})           {len(sub):8,} {act:9.1%} {mk:8.1%} {act-mk:+8.1%} {roi:+8.2%}")

print("\n"+"="*100)
print("E. HOME/AWAY SPLIT ASYMMETRY — teams unusually better at home than away")
print("="*100)
print("  split = prior home PPG - prior away PPG. Does an extreme split predict beyond price?")
print(f"  {'home team H-A split':28s} {'n':>8s} {'home win':>9s} {'market':>8s} {'edge':>8s} {'ROI':>8s}")
for lo_,hi_ in [(-3,-0.5),(-0.5,0.3),(0.3,1.0),(1.0,1.8),(1.8,4)]:
    sub=[x for x in elig if x[1]['hppg'] is not None and x[1]['appg'] is not None
         and lo_<=(x[1]['hppg']-x[1]['appg'])<hi_]
    if len(sub)<300: continue
    act=sum(1 for m,_,_ in sub if m['res']=='H')/len(sub)
    mk=sum(devig(m['oh'],m['od'],m['oa'])[0] for m,_,_ in sub)/len(sub)
    roi=sum((m['oh']-1) if m['res']=='H' else -1 for m,_,_ in sub)/len(sub)
    print(f"  split [{lo_:5.1f},{hi_:4.1f})          {len(sub):8,} {act:9.1%} {mk:8.1%} {act-mk:+8.1%} {roi:+8.2%}")
pickle.dump(elig,open("elig.pkl","wb"))
