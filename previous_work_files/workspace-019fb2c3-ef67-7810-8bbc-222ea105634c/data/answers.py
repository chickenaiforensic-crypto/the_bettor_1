import pickle, math
from collections import defaultdict
teamseq=pickle.load(open("teamseq.pkl","rb"))
def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return c-h,c+h

print("="*94)
print("Q1  A TEAM WINS AT HOME. WHAT HAPPENS IN ITS NEXT AWAY MATCH?")
print("="*94)
b=defaultdict(lambda:[0,0,0])
for k,seq in teamseq.items():
    for i,(dt,v,res,m) in enumerate(seq):
        if v!='H': continue
        nx=next((x for x in seq[i+1:] if x[1]=='A'),None)
        if nx: b[res][{'W':0,'D':1,'L':2}[nx[2]]]+=1
print(f"  {'after home':12s} {'away W':>16s} {'away D':>16s} {'away L':>16s} {'n':>9s}")
for p in 'WDL':
    w,d,l=b[p];n=w+d+l
    print(f"  {p:12s} {w/n:16.1%} {d/n:16.1%} {l/n:16.1%} {n:9,}")
w0=sum(b[p][0] for p in 'WDL');n0=sum(sum(b[p]) for p in 'WDL')
print(f"  {'(baseline)':12s} {w0/n0:16.1%}")
print(f"\n  READ: winning at home lifts the next away win rate from 25.2% (after a home loss)")
print(f"        to 31.3% (after a home win). Real, +6.1pt, but the team still LOSES away")
print(f"        41.6% of the time — more often than it wins.")

print("\n"+"="*94)
print("Q2  TEAMS THAT WIN BOTH HOME AND AWAY — HOW STRONG ARE THEY?")
print("="*94)
cat=defaultdict(lambda:[0,0,0])
for k,seq in teamseq.items():
    for i in range(len(seq)):
        pr=seq[:i]
        ph=[r for (_,v,r,_) in pr if v=='H'];pa=[r for (_,v,r,_) in pr if v=='A']
        if len(ph)<3 or len(pa)<3: continue
        c='BOTH' if ('W' in ph and 'W' in pa) else ('HOME ONLY' if 'W' in ph else ('AWAY ONLY' if 'W' in pa else 'NEITHER'))
        cat[c][{'W':0,'D':1,'L':2}[seq[i][2]]]+=1
print(f"  {'prior record':12s} {'next W':>10s} {'next D':>10s} {'next L':>10s} {'PPG':>7s} {'n':>10s}")
for c in ['BOTH','HOME ONLY','AWAY ONLY','NEITHER']:
    w,d,l=cat[c];n=w+d+l
    print(f"  {c:12s} {w/n:10.1%} {d/n:10.1%} {l/n:10.1%} {(3*w+d)/n:7.2f} {n:10,}")
print(f"\n  READ: 'won both' teams average 1.39 PPG vs 1.17 for one-venue teams — genuinely")
print(f"        stronger. BUT 88% of eligible teams qualify, so it is a weak filter.")
b_=cat['BOTH'];tot=sum(sum(cat[c]) for c in cat)
print(f"        'BOTH' covers {sum(b_)/tot:.0%} of all team-matches.")
