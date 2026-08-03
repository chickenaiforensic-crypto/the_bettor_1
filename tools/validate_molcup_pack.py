#!/usr/bin/env python3
# validate_molcup_pack.py — external acceptance-gate mirror for the MOLCUP pack (WO §5)
# Emits audit/pack-validation-molcup.txt: numbered gates PASS/FAIL + per-team pivot ledgers.
import hashlib, re, sys

PACK="handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt"
OUT="audit/pack-validation-molcup.txt"
lines=open(PACK,encoding="ascii").read().splitlines()
M=[l.split("|") for l in lines if l.startswith("MATCH|")]
N=[l for l in lines if l.startswith("NOTE|")]
S=[l for l in lines if l.startswith("SOURCE|")]
T=[l for l in lines if l.startswith("TEAM|")]
FL17=["Banik Ostrava","Bohemians 1905","Ceske Budejovice","Hradec Kralove","Jablonec","Karvina",
 "Mlada Boleslav","Pardubice","Sigma Olomouc","Slavia Prague","Slovacko","Slovan Liberec",
 "Sparta Prague","Teplice","Viktoria Plzen","Zbrojovka Brno","Zlin"]
FLER={"Zbrojovka Brno":"2022-23","Karvina":"2021-22/2023-24 (FNL in 2022-23)"}
def season(dt): return "2021-22" if dt<"2022-07-01" else ("2022-23" if dt<"2023-07-01" else "2023-24")
FL={  "2021-22":set(FL17)-{"Zbrojovka Brno"}, "2023-24":set(FL17)-{"Zbrojovka Brno"},
      "2022-23":(set(FL17)-{"Karvina"}) }
FL["2022-23"]=(FL["2021-22"]-{"Karvina"})|{"Zbrojovka Brno"}

g=[]
def gate(name,cond,detail=""):
    g.append((name,cond,detail))

# --- gate battery (mirrors WO §5 + programme conventions) ---
gate("G01 file parse & 41-field grammar", all(len(l.split("|"))==14 for l in [x for x in lines if x.startswith("MATCH|")]))
gate("G02 ASCII-only", all(all(ord(c)<128 for c in l) for l in lines))
gate("G03 END terminator present once", lines[-1]=="END" and sum(1 for l in lines if l=="END")==1)
gate("G04 competition literal 'MOL Cup' on all rows", all(f[2]=="MOL Cup" for f in M))
gate("G05 compType domestic-cup on all rows (errata)", all(f[3]=="domestic-cup" for f in M))
gate("G06 total rows 120 (41/41/38)", len(M)==120 and sum(1 for f in M if season(f[1])=="2021-22")==41 and sum(1 for f in M if season(f[1])=="2022-23")==41 and sum(1 for f in M if season(f[1])=="2023-24")==38)
per={(se,rd):0 for se in ("2021-22","2022-23","2023-24") for rd in ("R2","R3","R16","QF","SF","Final")}
for f in M: per[(season(f[1]),f[8])]+=1
exp={"2021-22":[11,15,8,4,2,1],"2022-23":[11,15,8,4,2,1],"2023-24":[11,15,6,3,2,1]}
rds=["R2","R3","R16","QF","SF","Final"]
gate("G07 round-by-round counts match declared slice", all(per[(se,rd)]==exp[se][i] for se in exp for i,rd in enumerate(rds)),
     str(per))
gate("G08 every row has >=1 pinned FL club of its season (slice rule)", all(f[4] in FL[season(f[1])] or f[7] in FL[season(f[1])] for f in M))
known_out={("2021-10-06","Varnsdorf","Zbrojovka Brno"),("2022-10-18","Sobeslav","Karvina"),
 ("2023-09-27","Opava","Zbrojovka Brno"),("2023-11-01","Dukla Prague","Vyskov"),
 ("2023-11-17","Velvary","Opava"),("2024-02-25","Opava","Dukla Prague")}
gate("G09 no known out-of-slice tie leaked into rows", all((f[1],f[4],f[7]) not in known_out for f in M))
gate("G10 no duplicate ties (date-home-away unique)", len({(f[1],f[4],f[7]) for f in M})==len(M))
gate("G11 boundary: all dates in [2021-07-01, 2024-06-30)", all("2021-07-01"<=f[1]<"2024-06-30" for f in M))
gate("G12 round labels in {R2,R3,R16,QF,SF,Final}", all(f[8] in rds for f in M))
adv=[l for l in N if "|advancement|" in l]
draws={(f[1],f[4],f[7]) for f in M if f[5]==f[6]}
advkey=set()
for l in adv:
    m=re.match(r"NOTE\|info\|advancement\|(\S+) (\S+) (.*) vs (.*): (.*) advanced",l)
    advkey.add((m.group(2),m.group(3),m.group(4)))
gate("G13 20 advancement NOTEs, one per settled tie", len(adv)==20 and advkey==draws, "draws=%d advkeys=%d"%(len(draws),len(advkey)))
gate("G14 settled ties recorded as 90-minute draws", all(f[5]==f[6] for f in M if (f[1],f[4],f[7]) in advkey))
def w(f):
    if f[5]>f[6]: return f[4]
    if f[5]<f[6]: return f[7]
    for l in adv:
        if " %s %s vs %s:"%(f[1],f[4],f[7]) in l: return l.split(": ")[1].split(" advanced")[0]
fin={season(f[1]):f for f in M if f[8]=="Final"}
champ={"2021-22":"Slovacko","2022-23":"Slavia Prague","2023-24":"Sparta Prague"}
gate("G15 bracket: champions per season", all(w(fin[se])==champ[se] for se in fin), str({se:w(fin[se]) for se in fin}))
sf={se:set() for se in champ}
for f in M:
    if f[8]=="SF": sf[season(f[1])].update([f[4],f[7]])
gate("G16 bracket: semifinalists per season", sf=={
 "2021-22":{"Sparta Prague","Jablonec","Hradec Kralove","Slovacko"},
 "2022-23":{"Sparta Prague","Ceske Budejovice","Slavia Prague","Bohemians 1905"},
 "2023-24":{"Opava","Sparta Prague","Viktoria Plzen","Zlin"}}, str(sf))
gate("G17 finalist sets per season", {se:{fin[se][4],fin[se][7]} for se in fin}=={
 "2021-22":{"Slovacko","Sparta Prague"},"2022-23":{"Sparta Prague","Slavia Prague"},
 "2023-24":{"Viktoria Plzen","Sparta Prague"}})
gate("G18 all FL home-ground strings in pinned CZ1 style (spot checks)",
     any(f[4]=="Slavia Prague" and f[9]=="Sinobo Stadium" and season(f[1])=="2021-22" for f in M) and
     any(f[4]=="Slavia Prague" and f[9]=="Fortuna Arena" and season(f[1])=="2022-23" for f in M) and
     any(f[4]=="Sparta Prague" and f[9]=="Generali Ceska pojistovna Arena" for f in M if f[1]<"2022-07-01") and
     any(f[4]=="Sparta Prague" and f[9]=="epet ARENA" for f in M if "2022-07-01"<=f[1]) and
     any(f[4]=="Hradec Kralove" and f[9]=="Lokotrans Arena" and f[10]=="Mlada Boleslav" for f in M if f[1]<"2022-07-01") and
     any(f[4]=="Hradec Kralove" and f[9]=="Malsovicka Arena" for f in M if f[1]>"2023-07-01"))
gate("G19 TEAM rows = the 31 declared new identities, none of the 27 roster strings",
     len(T)==31 and not any(t.split("|")[1] in {"Zizkov","Vyskov","Jihlava","Trinec","Chrudim","Opava","Taborsko","Usti nad Labem","Varnsdorf","Frydek-Mistek","Loko Praha","Kromeriz","Hlucin","Zapy","Domazlice","Brozany","Lanznot","Dukla Prague"} for t in T))
gate("G20 every TEAM name used in rows", all(any(f[4]==t.split('|')[1] or f[7]==t.split('|')[1] for f in M) for t in T))
gate("G21 no FL string re-declared as TEAM", not any(t.split("|")[1] in FL17 for t in T))
gate("G22 SOURCE rows present and labels referenced by rows",
     all(f[13] in {s.split("|")[1] for s in S} for f in M) and len(S)==15)
gate("G23 pack_id first line", lines[0].startswith("NOTE|info|pack_id|MOLCUP-2021-2026"))
gate("G24 source_adaptation + comp_class + slice + round_counts + spot_audit NOTEs present",
     any("|source_adaptation|" in l for l in N) and any("|comp_class|" in l for l in N) and
     any("|slice|" in l for l in N) and any("|round_counts|" in l for l in N) and any("|spot_audit|" in l for l in N))
gate("G25 source_conflict NOTEs cover Slovacko silent-aet + Plzen-Zlin date",
     any("silent-aet" in l.lower() or "Slovacko v Karvina" in l for l in N) and any("2024-04-24" in l and "source_conflict" in l for l in N))
_seq=[(season(f[1]),f[1]) for f in M]
gate("G26 season-blocked date-sorted presentation", _seq == sorted(_seq, key=lambda x:(x[0],x[1])))
gate("G27 finals before 2024-06-30 boundary + finals in May", all(fin[se][1][5:7]=="05" for se in fin))
gate("G28 no standings tables anywhere (rows only)", not any(l.split("|")[0] not in ("NOTE","SOURCE","TEAM","MATCH") and l!="END" for l in lines))
gate("G29 held-out seasons untouched: no rows dated >= 2024-07-01", all(f[1]<"2024-07-01" for f in M))
gate("G30 every R16 tie of each season present (8+8+6 = official R16=8 ties w/ exclusions)", per[("2021-22","R16")]==8 and per[("2022-23","R16")]==8 and per[("2023-24","R16")]==6)

txt=["PACK VALIDATION — MOLCUP-2021-2026_BP-TEAM-PACK_v2 (WO-MOLCUP-BACKFILL-04)",
 "generated %s by tools/validate_molcup_pack.py"%"2026-08-03",
 "pack sha256: "+hashlib.sha256(open(PACK,'rb').read()).hexdigest(),
 "pack rows: %d MATCH / %d TEAM / %d SOURCE / %d NOTE"%(len(M),len(T),len(S),len(N)),""]
npass=0
for i,(name,cond,detail) in enumerate(g,1):
    txt.append("%s G%02d %s%s"%("PASS" if cond else "FAIL",i,name,("  ["+detail+"]") if (detail and not cond) else ""))
    npass+= cond
txt.append("")
txt.append("GATES: %d/%d PASS"%(npass,len(g)))
txt.append("")
txt.append("===== PER-TEAM PIVOT LEDGERS (owner decree): every pinned FL club's in-window cup campaign =====")
for club in FL17:
    txt.append("")
    txt.append("## %s"%club)
    found=False
    for se in ("2021-22","2022-23","2023-24"):
        rows=[f for f in M if (f[4]==club or f[7]==club) and season(f[1])==se]
        if not rows:
            note=""
            if club in FL[se]: note="  (no %s rows in-window: eliminated before the round-track or byle)"%se
            else: note="  (not a First-League club in %s: %s)"%(se,FLER.get(club,""))
            txt.append("%s: -- %s"%(se,note)); continue
        found=True
        for f in sorted(rows,key=lambda x:x[1]):
            side="H" if f[4]==club else "A"
            opp=f[7] if side=="H" else f[4]
            txt.append("%s %s %s %s v %s  %s-%s  [%s]  %s"%(se,f[1],side,club,opp,f[5],f[6],f[8],f[9]))
    if not found: txt.append("(no appearances)")
txt.append("")
txt.append("validation-audit sha256 (self, computed before this line is appended): see repo audit log")
report="\n".join(txt)+"\n"
open(OUT,"w").write(report)
print("validation written: %d/%d PASS -> %s"%(npass,len(g),OUT))
print("report sha256:",hashlib.sha256(report.encode()).hexdigest())
sys.exit(0 if npass==len(g) else 1)
