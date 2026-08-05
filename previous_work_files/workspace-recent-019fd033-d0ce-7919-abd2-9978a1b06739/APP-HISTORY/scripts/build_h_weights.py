p='/home/user/app-v2.6-cross.html'
s=open(p).read()

# 1) phase weights champion
old="  var PHASE_WEIGHT = {h2h:3, common:2, third:1.5};"
new="""  var PHASE_WEIGHT = {h2h:3, common:3, third:0.75};
  /* CALIBRATION-7 (633-game replay, log-loss primary + zone-quality guardrails,
     split-half validated): common raised 2->3, third cut 1.5->0.75, neutral band
     widened 0.25->0.50. ll 1.1637->1.0728, draw share 23.1% vs 24.3% actual,
     actionable W 59.1->64.3, pair 81.0->84.1, ladder monotone. Runner-up
     3/2/0.5 was within noise; 3/3/0.75 chosen on primary metric. */"""
assert s.count(old)==1; s=s.replace(old,new)

# 2) neutral band constant + use in share allocation (1029, 2936-37)
band_decl="  var NEUTRAL_BAND = 0.50;"
s=s.replace(new, new+"\n"+band_decl, 1)
old1029="      if (p.estimate > 0.25) hW += p.weight; else if (p.estimate < -0.25) aW += p.weight; else dW += p.weight;"
assert s.count(old1029)==1
s=s.replace(old1029,"      if (p.estimate > NEUTRAL_BAND) hW += p.weight; else if (p.estimate < -NEUTRAL_BAND) aW += p.weight; else dW += p.weight;")
old2936="      if(p.estimate>0.25){homeW+=p.weight;homeN++;}\n      else if(p.estimate<-0.25){awayW+=p.weight;awayN++;}"
assert s.count(old2936)==1
s=s.replace(old2936,"      if(p.estimate>NEUTRAL_BAND){homeW+=p.weight;homeN++;}\n      else if(p.estimate<-NEUTRAL_BAND){awayW+=p.weight;awayN++;}")
s=s.replace("engine's own bucket rule (|est|>0.25 home/away, else neutral) so section",
            "engine's own bucket rule (|est|>NEUTRAL_BAND=0.50 home/away, else neutral - CALIBRATION-7) so section")

# 3) version bump
s=s.replace("v2.8.5-cross","v2.8.6-cross")
open(p,'w').write(s)
print("weights+band shipped; v2.8.6 occurrences:", s.count("v2.8.6-cross"))
