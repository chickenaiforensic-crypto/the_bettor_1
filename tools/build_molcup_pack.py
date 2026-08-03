#!/usr/bin/env python3
# build_molcup_pack.py — MOL Cup 2021-2026 BP-TEAM-PACK v2 (WO-MOLCUP-BACKFILL-04, queue ④)
# Rows transcribed from audit/ledger/molcup-*.txt (RSSSF primary + wiki second index + wf third
# index); venues/tiers per audit/ledger/molcup-venues-teams.txt. compType = domestic-cup per
# standing auditor errata ERRATA-2026-08-03 (supersedes the WO grammar's domestic-league line).
import hashlib, re, sys, os

OUT = "handoffs/MOLCUP-2021-2026_BP-TEAM-PACK_v2.txt"

# ---- pinned WO-02 §3 First-League strings (17) with per-season membership ----
FL = {
 "2021-22": ["Bohemians 1905","Ceske Budejovice","Hradec Kralove","Jablonec","Karvina",
   "Mlada Boleslav","Sigma Olomouc","Banik Ostrava","Pardubice","Slavia Prague","Slovacko",
   "Slovan Liberec","Sparta Prague","Teplice","Viktoria Plzen","Zlin"],
 "2022-23": ["Bohemians 1905","Ceske Budejovice","Hradec Kralove","Jablonec","Zbrojovka Brno",
   "Mlada Boleslav","Sigma Olomouc","Banik Ostrava","Pardubice","Slavia Prague","Slovacko",
   "Slovan Liberec","Sparta Prague","Teplice","Viktoria Plzen","Zlin"],
 "2023-24": ["Bohemians 1905","Ceske Budejovice","Hradec Kralove","Jablonec","Karvina",
   "Mlada Boleslav","Sigma Olomouc","Banik Ostrava","Pardubice","Slavia Prague","Slovacko",
   "Slovan Liberec","Sparta Prague","Teplice","Viktoria Plzen","Zlin"],
}
# client-roster CZ2/lower strings (WO-MOLCUP/§3 do-not-redeclare list + Dukla Prague)
ROSTER = ["Zizkov","Vyskov","Jihlava","Trinec","Chrudim","Opava","Taborsko","Usti nad Labem",
  "Varnsdorf","Frydek-Mistek","Loko Praha","Kromeriz","Hlucin","Zapy","Horovice",
  "Police nad Metuji","Uhersky Brod","Benatky nad Jizerou","Brozany","Domazlice",
  "Horni Redice","Lanznot","Hlinsko","Karlovy Vary","Nove Sady","Petrin Plzen","Dukla Prague"]
# 30 new lower-league identities declared in this pack (see TEAMREG ledger)
# fields: name|leagueName|leagueCode|aliases|stadium|city|founded
NEWTEAMS = [
 ("Vysehrad","Bohemian Football League (CFL A)","CZ3",
   "FC Slavoj Vysehrad;Slavoj Vysehrad","Stadion FK Slavoj Vysehrad","Prague","1907"),
 ("Benesov","Bohemian Football League (CFL A)","CZ3","SK Benesov","Mestsky Stadion","Benesov",""),
 ("Hostoun","Bohemian Football League (CFL A)","CZ3","Sokol Hostoun","Stadion Vojtecha Zeithamla","Hostoun",""),
 ("Sedlcany","Czech Fourth Division (Divize A)","CZ4","TJ Tatran Sedlcany","TJ Tatran Sedlcany","Sedlcany",""),
 ("Slavicin","Czech Fourth Division (Divize E)","CZ4","FC TVD Slavicin","Stadion FC TVD Slavicin","Slavicin",""),
 ("Sokolov","Bohemian Football League (CFL A)","CZ3","FK Banik Sokolov 1948;Banik Sokolov","Stadion FK Banik Sokolov","Sokolov",""),
 ("Unicov","Moravian-Silesian Football League","CZ3","SK Unicov","Stadion SK Unicov","Unicov",""),
 ("Zbuzany","Bohemian Football League (CFL B)","CZ3","FK Zbuzany 1953","Stadion FK Zbuzany","Zbuzany",""),
 ("Blansko","Moravian-Silesian Football League","CZ3","FK Blansko","Stadion na Mlynske","Blansko",""),
 ("Brezova","Czech Fourth Division (Divize B)","CZ4","FK Olympie Brezova;TJ Olympie Brezova","TJ Olympie Brezova","Brezova",""),
 ("Vlasim","Czech National Football League","CZ2","FC Sellier & Bellot Vlasim;FC Vlasim","Stadion Kollarova ulice","Vlasim",""),
 ("Pribram","Czech National Football League","CZ2","1. FK Pribram;FK Viagem Pribram","Na Litavce","Pribram",""),
 ("Prepere","Bohemian Football League (CFL B)","CZ3","FK Prepere","Hriste FK Prepere","Prepere",""),
 ("Prostejov","Czech National Football League","CZ2","1. SK Prostejov","Stadion Za Mistnim nadrazim","Prostejov",""),
 ("Lisen","Czech National Football League","CZ2","SK Lisen;SK Lisen 2019;SK Artis Brno (2024+ rename)","Stadion SK Lisen","Brno",""),
 ("Velvary","Bohemian Football League (CFL B)","CZ3","TJ Slovan Velvary;Slovan Velvary","Stadion TJ Slovan Velvary","Velvary",""),
 ("Rokycany","Czech Fourth Division (Divize A)","CZ4","FC Rokycany","Stadion pod Husovymi sady","Rokycany","1903"),
 ("Motorlet Praha","Bohemian Football League (CFL A)","CZ3","FK Motorlet Praha;SK Motorlet Praha","Stadion SK Motorlet","Prague","1912"),
 ("Start Brno","Czech Fourth Division (Divize D)","CZ4","TJ Start Brno","Stadion TJ Start Brno","Brno","1957"),
 ("Rosice","Moravian-Silesian Football League","CZ3","FC Slovan Rosice;Slovan Rosice","Sportovni areal FC Slovan Rosice","Rosice","1909"),
 ("Caslav","Czech Fourth Division (Divize C)","CZ4","FK Caslav","Stadion Pod hradkem","Caslav","1902"),
 ("Chomutov","Czech Fourth Division (Divize B)","CZ4","FC Chomutov","Letni stadion","Chomutov",""),
 ("Chlumec nad Cidlinou","Bohemian Football League (CFL B)","CZ3","FK Chlumec nad Cidlinou;Chlumec",
   "Stadion Mestsky fotbalovy - FK Chlumec nad Cidlinou","Chlumec nad Cidlinou",""),
 ("Velke Hamry","Czech Fourth Division (Divize C)","CZ4","FK Velke Hamry;TJ Sokol Velke Hamry","Hriste TJ Velke Hamry","Velke Hamry",""),
 ("Hlubina","Czech Fourth Division (Divize F)","CZ4","TJ Unie Hlubina;Unie Hlubina","Stadion Hlubina","Ostrava","1919"),
 ("Banik Most-Sous","Bohemian Football League (CFL B)","CZ3","FK Banik Most-Sous;FK Banik Sous","Fotbalovy stadion Josefa Masopusta","Most","2020"),
 ("Admira Praha","Bohemian Football League (CFL A)","CZ3","FK Admira Praha;Admira","Stadion Na Pecich","Prague","1909"),
 ("Sobeslav","Czech Fourth Division (Divize A)","CZ4","FK Spartak Sobeslav;Spartak Sobeslav","Fotbalovy stadion FK Raselina Sobeslav","Sobeslav",""),
 ("Kladno","Czech Fourth Division (Divize B)","CZ4","SK Kladno","Areal Frantiska Kloze","Kladno",""),
 ("Kolin","Bohemian Football League (CFL B)","CZ3","SK Sparta Kolin;Sparta Kolin","Mestsky stadion Kolin","Kolin",""),
 ("Marianske Lazne","Czech Fourth Division (Divize A)","CZ4","FC Viktoria Marianske Lazne;FK Viktoria Marianske Lazne",
   "Sportovni areal Viktoria","Marianske Lazne",""),
]
NEWTEAM_NAMES = [t[0] for t in NEWTEAMS]

# ---- MATCH row tuples: (season, date, home, hg, ag, away, round, stadium, city, srclabel) ----
# 90-minute doctrine APPLIED: aet/pens ties carry the 90-min score per the splits register.
R = []
def add(s,dt,h,hg,ag,a,rd,stad,city,src): R.append((s,dt,h,hg,ag,a,rd,stad,city,src))

# ================= 2021-22 (41 rows: R2 11, R3 15, R16 8, QF 4, SF 2, F 1) =================
S2122="2021-22"; RS="rsssf-tsje2022-cup"; WK="wiki-molcup-2122"
add(S2122,"2021-08-24","Mlada Boleslav",3,0,"Vysehrad","R2","Lokotrans Arena","Mlada Boleslav",WK)
add(S2122,"2021-08-25","Benesov",0,1,"Teplice","R2","Mestsky Stadion","Benesov",WK)
add(S2122,"2021-08-25","Hlucin",0,0,"Banik Ostrava","R2","Stadion Mestsky Lumira Kota","Hlucin",WK)
add(S2122,"2021-08-25","Hostoun",0,0,"Pardubice","R2","Stadion Vojtecha Zeithamla","Hostoun",WK)
add(S2122,"2021-08-25","Sedlcany",0,6,"Ceske Budejovice","R2","TJ Tatran Sedlcany","Sedlcany",WK)
add(S2122,"2021-08-25","Slavicin",1,5,"Karvina","R2","Stadion FC TVD Slavicin","Slavicin",WK)
add(S2122,"2021-08-25","Sokolov",0,6,"Bohemians 1905","R2","Stadion FK Banik Sokolov","Sokolov",WK)
add(S2122,"2021-08-25","Unicov",2,4,"Sigma Olomouc","R2","Stadion SK Unicov","Unicov",WK)
add(S2122,"2021-08-25","Slovan Liberec",1,2,"Zbuzany","R2","Stadion u Nisy","Liberec",WK)
add(S2122,"2021-09-01","Blansko",1,4,"Zlin","R2","Stadion na Mlynske","Blansko",WK)
add(S2122,"2021-09-01","Brezova",0,2,"Hradec Kralove","R2","TJ Olympie Brezova","Brezova",WK)
add(S2122,"2021-09-21","Vlasim",1,2,"Sigma Olomouc","R3","Stadion Kollarova ulice","Vlasim",WK)
add(S2122,"2021-09-21","Jihlava",2,0,"Pardubice","R3","v Jiraskove ulici","Jihlava",WK)
add(S2122,"2021-09-21","Opava",2,4,"Mlada Boleslav","R3","Stadion v Mestskych sadech","Opava",WK)
add(S2122,"2021-09-21","Viktoria Plzen",2,1,"Pribram","R3","Doosan Arena","Plzen",WK)
add(S2122,"2021-09-22","Karvina",1,0,"Chrudim","R3","Mestsky stadion (Karvina)","Karvina",WK)
add(S2122,"2021-09-22","Prepere",0,1,"Jablonec","R3","Hriste FK Prepere","Prepere",WK)
add(S2122,"2021-09-22","Prostejov",0,4,"Bohemians 1905","R3","Stadion Za Mistnim nadrazim","Prostejov",WK)
add(S2122,"2021-09-22","Trinec",0,1,"Teplice","R3","Stadion Rudolfa Labaje","Trinec",WK)
add(S2122,"2021-09-22","Zapy",0,4,"Hradec Kralove","R3","Stadion TJ Sokol Zapy","Brandys nad Labem",WK)
add(S2122,"2021-09-22","Zbuzany",1,2,"Slovacko","R3","Stadion FK Zbuzany","Zbuzany",WK)
add(S2122,"2021-09-22","Loko Praha",2,2,"Banik Ostrava","R3","Stadion na Plynarne","Prague",WK)
add(S2122,"2021-09-22","Lisen",0,3,"Sparta Prague","R3","Stadion SK Lisen","Brno",WK)
add(S2122,"2021-09-22","Velvary",2,4,"Slavia Prague","R3","Stadion TJ Slovan Velvary","Velvary",WK)
add(S2122,"2021-10-06","Dukla Prague",1,3,"Ceske Budejovice","R3","Stadion Juliska","Prague",WK)
add(S2122,"2021-10-07","Vyskov",1,1,"Zlin","R3","Sportovni areal Drnovice","Vyskov",WK)
add(S2122,"2021-10-26","Bohemians 1905",1,0,"Jihlava","R16","Dolicek","Prague",RS)
add(S2122,"2021-10-27","Banik Ostrava",1,2,"Hradec Kralove","R16","Mestsky stadion (Ostrava)","Ostrava",RS)
add(S2122,"2021-10-27","Teplice",0,2,"Sparta Prague","R16","Na Stinadlech","Teplice",RS)
add(S2122,"2021-10-27","Mlada Boleslav",2,0,"Viktoria Plzen","R16","Lokotrans Arena","Mlada Boleslav",RS)
add(S2122,"2021-11-11","Jablonec",4,0,"Varnsdorf","R16","Stadion Strelnice","Jablonec nad Nisou",RS)
add(S2122,"2021-11-12","Slovacko",1,1,"Karvina","R16","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste","wf-molcup-reports")
add(S2122,"2021-11-23","Ceske Budejovice",1,1,"Sigma Olomouc","R16","Stadion Strelecky ostrov","Ceske Budejovice",RS)
add(S2122,"2021-12-15","Slavia Prague",3,1,"Zlin","R16","Sinobo Stadium","Prague",RS)
add(S2122,"2022-02-09","Sigma Olomouc",0,0,"Slovacko","QF","Andruv stadion","Olomouc",RS)
add(S2122,"2022-02-09","Slavia Prague",0,2,"Sparta Prague","QF","Sinobo Stadium","Prague",RS)
add(S2122,"2022-02-15","Hradec Kralove",1,1,"Bohemians 1905","QF","Lokotrans Arena","Mlada Boleslav",RS)
add(S2122,"2022-02-16","Jablonec",4,0,"Mlada Boleslav","QF","Stadion Strelnice","Jablonec nad Nisou",RS)
add(S2122,"2022-03-02","Sparta Prague",4,3,"Jablonec","SF","Generali Ceska pojistovna Arena","Prague",RS)
add(S2122,"2022-03-25","Hradec Kralove",0,1,"Slovacko","SF","Lokotrans Arena","Mlada Boleslav",RS)
add(S2122,"2022-05-18","Slovacko",3,1,"Sparta Prague","Final","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste",RS)
# ================= 2022-23 (41 rows) =================
S2223="2022-23"; RS="rsssf-tsje2023-cup"; WK="wiki-molcup-2223"
add(S2223,"2022-09-13","Unicov",2,2,"Sigma Olomouc","R2","Stadion SK Unicov","Unicov",WK)
add(S2223,"2022-09-14","Zizkov",1,1,"Teplice","R2","Stadion Viktorie v Seifertove ulici","Prague",WK)
add(S2223,"2022-09-14","Velvary",1,0,"Pardubice","R2","Stadion TJ Slovan Velvary","Velvary",WK)
add(S2223,"2022-09-14","Rokycany",1,5,"Slovan Liberec","R2","Stadion pod Husovymi sady","Rokycany",WK)
add(S2223,"2022-09-14","Motorlet Praha",0,4,"Jablonec","R2","Stadion SK Motorlet","Prague",WK)
add(S2223,"2022-09-14","Start Brno",0,3,"Zlin","R2","Stadion TJ Start Brno","Brno",WK)
add(S2223,"2022-09-14","Rosice",0,4,"Zbrojovka Brno","R2","Sportovni areal FC Slovan Rosice","Rosice",WK)
add(S2223,"2022-09-21","Caslav",0,11,"Hradec Kralove","R2","Stadion Pod hradkem","Caslav",WK)
add(S2223,"2022-09-21","Chomutov",0,5,"Ceske Budejovice","R2","Letni stadion","Chomutov",WK)
add(S2223,"2022-09-21","Usti nad Labem",0,3,"Bohemians 1905","R2","Mestsky stadion","Usti nad Labem",WK)
add(S2223,"2022-09-21","Kromeriz",3,3,"Banik Ostrava","R2","Stadion Jozky Silneho","Kromeriz",WK)
add(S2223,"2022-10-11","Jablonec",0,1,"Vyskov","R3","Stadion Strelnice","Jablonec nad Nisou",WK)
add(S2223,"2022-10-18","Pribram",0,3,"Teplice","R3","Na Litavce","Pribram",WK)
add(S2223,"2022-10-19","Velvary",0,2,"Banik Ostrava","R3","Stadion TJ Slovan Velvary","Velvary",WK)
add(S2223,"2022-10-19","Hlucin",3,2,"Viktoria Plzen","R3","Stadion Mestsky Lumira Kota","Hlucin",WK)
add(S2223,"2022-10-19","Domazlice",1,6,"Sparta Prague","R3","Mestsky stadion Strelnice Domazlice","Domazlice",WK)
add(S2223,"2022-10-19","Zapy",1,3,"Sigma Olomouc","R3","Stadion TJ Sokol Zapy","Brandys nad Labem",WK)
add(S2223,"2022-10-19","Chlumec nad Cidlinou",0,4,"Hradec Kralove","R3","Stadion Mestsky fotbalovy - FK Chlumec nad Cidlinou","Chlumec nad Cidlinou",WK)
add(S2223,"2022-10-19","Dukla Prague",0,4,"Slavia Prague","R3","Stadion Juliska","Prague",WK)
add(S2223,"2022-10-19","Ceske Budejovice",3,1,"Vlasim","R3","Stadion Strelecky ostrov","Ceske Budejovice",WK)
add(S2223,"2022-10-19","Mlada Boleslav",4,0,"Prostejov","R3","Lokotrans Arena","Mlada Boleslav",WK)
add(S2223,"2022-10-19","Bohemians 1905",2,1,"Trinec","R3","Dolicek","Prague",WK)
add(S2223,"2022-10-19","Slovacko",6,0,"Varnsdorf","R3","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste",WK)
add(S2223,"2022-10-19","Taborsko",1,2,"Zbrojovka Brno","R3","Stadion Kvapilova","Tabor",WK)
add(S2223,"2022-10-25","Frydek-Mistek",0,6,"Slovan Liberec","R3","Stovky","Frydek-Mistek",WK)
add(S2223,"2022-10-25","Zlin",2,0,"Jihlava","R3","Letna Stadion","Zlin",WK)
add(S2223,"2022-11-17","Teplice",2,2,"Zbrojovka Brno","R16","Na Stinadlech","Teplice",RS)
add(S2223,"2022-11-17","Zlin",0,1,"Vyskov","R16","Letna Stadion","Zlin",RS)
add(S2223,"2022-11-18","Karvina",0,2,"Slavia Prague","R16","Mestsky stadion (Karvina)","Karvina",RS)
add(S2223,"2022-11-18","Slovacko",1,0,"Mlada Boleslav","R16","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste",RS)
add(S2223,"2022-11-19","Banik Ostrava",2,3,"Sparta Prague","R16","Mestsky stadion (Ostrava)","Ostrava",RS)
add(S2223,"2022-11-19","Bohemians 1905",3,0,"Hlucin","R16","Dolicek","Prague",RS)
add(S2223,"2022-11-26","Slovan Liberec",4,1,"Sigma Olomouc","R16","Stadion u Nisy","Liberec",RS)
add(S2223,"2023-02-01","Ceske Budejovice",2,0,"Hradec Kralove","R16","Stadion Strelecky ostrov","Ceske Budejovice",RS)
add(S2223,"2023-03-01","Slovacko",1,2,"Bohemians 1905","QF","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste",RS)
add(S2223,"2023-03-01","Slovan Liberec",2,2,"Sparta Prague","QF","Stadion u Nisy","Liberec",RS)
add(S2223,"2023-03-01","Ceske Budejovice",2,1,"Zbrojovka Brno","QF","Stadion Strelecky ostrov","Ceske Budejovice",RS)
add(S2223,"2023-03-01","Slavia Prague",4,0,"Vyskov","QF","Fortuna Arena","Prague",RS)
add(S2223,"2023-04-05","Sparta Prague",2,0,"Ceske Budejovice","SF","epet ARENA","Prague",RS)
add(S2223,"2023-04-05","Slavia Prague",2,2,"Bohemians 1905","SF","Fortuna Arena","Prague",RS)
add(S2223,"2023-05-03","Sparta Prague",0,2,"Slavia Prague","Final","epet ARENA","Prague",RS)
# ================= 2023-24 (39 rows: R2 11, R3 15, R16 7, QF 3, SF 2, F 1) =================
S2324="2023-24"; RS="rsssf-tsje2024-cup"; WK="wiki-molcup-2324"
add(S2324,"2023-08-29","Velke Hamry",1,1,"Ceske Budejovice","R2","Hriste TJ Velke Hamry","Velke Hamry",WK)
add(S2324,"2023-08-29","Hlucin",0,2,"Banik Ostrava","R2","Stadion Mestsky Lumira Kota","Hlucin",WK)
add(S2324,"2023-08-30","Trinec",1,4,"Sigma Olomouc","R2","Stadion Rudolfa Labaje","Trinec",WK)
add(S2324,"2023-08-30","Mlada Boleslav",4,2,"Usti nad Labem","R2","Lokotrans Arena","Mlada Boleslav",WK)
add(S2324,"2023-08-30","Banik Most-Sous",0,3,"Pardubice","R2","Fotbalovy stadion Josefa Masopusta","Most",WK)
add(S2324,"2023-08-30","Lanznot",0,1,"Zlin","R2","Fotbalovy stadion Na Slajsi","Lanzhot",WK)
add(S2324,"2023-08-30","Hlubina",0,8,"Slovacko","R2","Stadion Hlubina","Ostrava",WK)
add(S2324,"2023-08-30","Brozany",3,4,"Teplice","R2","Ke Hristi","Brozany nad Ohri",WK)
add(S2324,"2023-09-05","Admira Praha",1,5,"Jablonec","R2","Stadion Na Pecich","Prague",WK)
add(S2324,"2023-09-06","Unicov",1,0,"Karvina","R2","Stadion SK Unicov","Unicov",WK)
add(S2324,"2023-09-06","Sobeslav",2,4,"Hradec Kralove","R2","Fotbalovy stadion FK Raselina Sobeslav","Sobeslav",WK)
add(S2324,"2023-09-26","Kladno",0,2,"Slovan Liberec","R3","Areal Frantiska Kloze","Kladno",WK)
add(S2324,"2023-09-26","Mlada Boleslav",4,2,"Prostejov","R3","Lokotrans Arena","Mlada Boleslav",WK)
add(S2324,"2023-09-27","Zapy",1,2,"Banik Ostrava","R3","Stadion TJ Sokol Zapy","Brandys nad Labem","wf-molcup-reports")
add(S2324,"2023-09-27","Domazlice",1,1,"Jablonec","R3","Mestsky stadion Strelnice Domazlice","Domazlice",WK)
add(S2324,"2023-09-27","Kromeriz",0,2,"Slavia Prague","R3","Stadion Jozky Silneho","Kromeriz",WK)
add(S2324,"2023-09-27","Vyskov",1,0,"Teplice","R3","Sportovni areal Drnovice","Vyskov",WK)
add(S2324,"2023-09-27","Lisen",0,1,"Sparta Prague","R3","Stadion SK Lisen","Brno",WK)
add(S2324,"2023-09-27","Slovacko",3,4,"Dukla Prague","R3","Mestsky fotbalovy stadion Miroslava Valenty","Uherske Hradiste",WK)
add(S2324,"2023-09-27","Jihlava",0,1,"Hradec Kralove","R3","v Jiraskove ulici","Jihlava",WK)
add(S2324,"2023-09-27","Velvary",1,1,"Pardubice","R3","Stadion TJ Slovan Velvary","Velvary",WK)
add(S2324,"2023-10-10","Ceske Budejovice",2,0,"Chrudim","R3","Stadion Strelecky ostrov","Ceske Budejovice",WK)
add(S2324,"2023-10-11","Zizkov",0,1,"Sigma Olomouc","R3","Stadion Viktorie v Seifertove ulici","Prague",WK)
add(S2324,"2023-10-11","Unicov",1,2,"Zlin","R3","Stadion SK Unicov","Unicov",WK)
add(S2324,"2023-10-11","Kolin",1,7,"Bohemians 1905","R3","Mestsky stadion Kolin","Kolin",WK)
add(S2324,"2023-10-12","Marianske Lazne",0,10,"Viktoria Plzen","R3","Sportovni areal Viktoria","Marianske Lazne",WK)
add(S2324,"2023-11-01","Slovan Liberec",1,0,"Mlada Boleslav","R16","Stadion u Nisy","Liberec",RS)
add(S2324,"2023-11-01","Banik Ostrava",0,1,"Zlin","R16","Mestsky stadion (Ostrava)","Ostrava",RS)
add(S2324,"2023-11-01","Bohemians 1905",1,2,"Sparta Prague","R16","Dolicek","Prague",RS)
add(S2324,"2023-11-16","Ceske Budejovice",1,2,"Jablonec","R16","Stadion Strelecky ostrov","Ceske Budejovice",RS)
add(S2324,"2023-11-16","Sigma Olomouc",1,3,"Viktoria Plzen","R16","Andruv stadion","Olomouc",RS)
add(S2324,"2023-12-06","Hradec Kralove",0,0,"Slavia Prague","R16","Malsovicka Arena","Hradec Kralove","wf-molcup-reports")
add(S2324,"2024-02-28","Zlin",1,1,"Slovan Liberec","QF","Letna Stadion","Zlin",RS)
add(S2324,"2024-02-28","Slavia Prague",2,2,"Sparta Prague","QF","Fortuna Arena","Prague",RS)
add(S2324,"2024-04-02","Jablonec",0,3,"Viktoria Plzen","QF","Stadion Strelnice","Jablonec nad Nisou",RS)
add(S2324,"2024-04-03","Opava",0,2,"Sparta Prague","SF","Stadion v Mestskych sadech","Opava",RS)
add(S2324,"2024-04-24","Viktoria Plzen",3,0,"Zlin","SF","Doosan Arena","Plzen",WK)
add(S2324,"2024-05-22","Viktoria Plzen",1,2,"Sparta Prague","Final","Doosan Arena","Plzen",RS)

ADV = [ # advancement NOTEs (20): (season,date,home,away,winner,detail)
 ("2021-22","2021-08-25","Hostoun","Pardubice","Pardubice","aet 0-1"),
 ("2021-22","2021-08-25","Hlucin","Banik Ostrava","Banik Ostrava","aet 0-1"),
 ("2021-22","2021-09-22","Loko Praha","Banik Ostrava","Banik Ostrava","aet 2-5"),
 ("2021-22","2021-10-07","Vyskov","Zlin","Zlin","aet 1-2"),
 ("2021-22","2021-11-12","Slovacko","Karvina","Slovacko","aet 3-1"),
 ("2021-22","2021-11-23","Ceske Budejovice","Sigma Olomouc","Sigma Olomouc","pens 4-5"),
 ("2021-22","2022-02-09","Sigma Olomouc","Slovacko","Slovacko","pens 2-4"),
 ("2021-22","2022-02-15","Hradec Kralove","Bohemians 1905","Hradec Kralove","aet 2-1"),
 ("2022-23","2022-09-13","Unicov","Sigma Olomouc","Sigma Olomouc","aet 2-4"),
 ("2022-23","2022-09-14","Zizkov","Teplice","Teplice","aet 1-2"),
 ("2022-23","2022-09-21","Kromeriz","Banik Ostrava","Banik Ostrava","pens 1-4"),
 ("2022-23","2022-11-17","Teplice","Zbrojovka Brno","Zbrojovka Brno","aet 2-3"),
 ("2022-23","2023-03-01","Slovan Liberec","Sparta Prague","Sparta Prague","pens 3-5"),
 ("2022-23","2023-04-05","Slavia Prague","Bohemians 1905","Slavia Prague","aet 3-2"),
 ("2023-24","2023-08-29","Velke Hamry","Ceske Budejovice","Ceske Budejovice","aet 1-3"),
 ("2023-24","2023-09-27","Domazlice","Jablonec","Jablonec","pens 4-5"),
 ("2023-24","2023-09-27","Velvary","Pardubice","Velvary","pens 5-4"),
 ("2023-24","2023-12-06","Hradec Kralove","Slavia Prague","Slavia Prague","aet 0-2"),
 ("2023-24","2024-02-28","Zlin","Slovan Liberec","Zlin","aet 2-1"),
 ("2023-24","2024-02-28","Slavia Prague","Sparta Prague","Sparta Prague","aet 2-3"),
]

SOURCES = [
 ("SOURCE|rsssf-tsje2022-cup|https://www.rsssf.org/tablest/tsje2022.html|2026-08-03|primary-archive|2021-22 Pohar FACR chapter: R16 (1/8 Finals), QF, SF and Final dates+scores in full (primary); transcribed in audit/ledger/molcup-2021-22.txt. Page carries this cup FROM R16 onward only (see source_adaptation)"),
 ("SOURCE|rsssf-tsje2023-cup|https://www.rsssf.org/tablest/tsje2023.html|2026-08-03|primary-archive|2022-23 Pohar FACR chapter: R16, QF, SF, Final dates+scores in full (primary); audit/ledger/molcup-2022-23.txt. R2/R3 not on the page"),
 ("SOURCE|rsssf-tsje2024-cup|https://www.rsssf.org/tablest/tsje2024.html|2026-08-03|primary-archive|2023-24 Pohar FACR chapter: R16, QF, SF, Final dates+scores in full (primary); audit/ledger/molcup-2023-24.txt. R2/R3 not on the page"),

 ("SOURCE|wiki-molcup-2122|https://en.wikipedia.org/wiki/2021%E2%80%9322_Czech_Cup|2026-08-03|second-index|Second/Third-round brackets (all 28 + 16 ties dates+scores = the R2/R3 coverage), Fourth-round diff vs RSSSF identical 8/8, QF/SF/F match boxes (venues + goal minutes + pso), Teams entrant table; audit/ledger/molcup-2ndidx-2021-22.txt"),
 ("SOURCE|wiki-molcup-2223|https://en.wikipedia.org/wiki/2022%E2%80%9323_Czech_Cup|2026-08-03|second-index|Second/Third-round brackets (27 + 16 ties), Fourth-round diff vs RSSSF identical 8/8, QF/SF/F match boxes (venues + goal minutes); audit/ledger/molcup-2ndidx-2022-23.txt"),
 ("SOURCE|wiki-molcup-2324|https://en.wikipedia.org/wiki/2023%E2%80%9324_Czech_Cup|2026-08-03|second-index|Second/Third-round brackets (27 + 16 ties), Fourth-round diff vs RSSSF identical date+score+order on all 8 ties (6 in-slice + Velvary-Opava and Dukla-Vyskov out), QF/SF/F match boxes (SF Plzen-Zlin dated 2024-04-24 18:00); audit/ledger/molcup-2ndidx-2023-24.txt"),
 ("SOURCE|wf-molcup-2122-rounds|https://www.worldfootball.net/schedule/cze-pohar-facr-2021-2022-2-runde/0/|2026-08-03|third-index|2021-22 round pages 2-runde/3-runde/achtelfinale (independent re-list: every R2/R3/R16 date+score verified tie-by-tie against the pack rows)"),
 ("SOURCE|wf-molcup-2223-rounds|https://www.worldfootball.net/schedule/cze-pohar-facr-2022-2023-2-runde/0/|2026-08-03|third-index|2022-23 round pages 2-runde/3-runde/achtelfinale: every pack row's date+score re-verified tie-by-tie"),
 ("SOURCE|wf-molcup-2324-rounds|https://www.worldfootball.net/schedule/cze-pohar-facr-2023-2024-2-runde/0/|2026-08-03|third-index|2023-24 round pages 2-runde/3-runde/achtelfinale: every pack row's date+score re-verified tie-by-tie"),
 ("SOURCE|wf-molcup-reports|https://www.worldfootball.net/match-report/co88/czech-republic-pohar-facr/ma9970847/fc-hradec-kralove_slavia-praha/|2026-08-03|third-index|match-report pages (competition co88): goal timelines for all 20 aet/pens pack ties = the 90-minute splits register (audit/ledger/molcup-venues-teams.txt section B), incl. the silent-aet timing of Slovacko 3-1 Karvina and per-tie Stadium lines (Zapy 2023 att 1150; Hradec-Slavia att 7608)"),
 ("SOURCE|wf-molcup-stadiums|https://www.worldfootball.net/competition/co88/se55490/stadiums/|2026-08-03|third-index|the three season cup stadium indexes se39724 / se46910 / se55490: venue city+capacity evidence for all lower-league home grounds in-window (full listings in audit/ledger/molcup-venues-teams.txt section A)"),
 ("SOURCE|wiki-cz-lower-tiers|https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%A1_fotbalov%C3%A1_liga_2021/2022|2026-08-03|wiki-index|tier/tables evidence for the 30 TEAM rows: cs.wiki season pages CFL A/B + MSFL + Divize A-F 2021/22, 2022/23, 2023/24 and club pages (Motorlet, Start Brno, Rosice, Caslav, Most-Sous, Admira, Rokycany, Hlubina, Vysehrad), en.wiki CNFL season articles 2021-22/2022-23/2023-24 (FNL memberships); transcribed in audit/ledger/molcup-venues-teams.txt sections C/D"),
 ("SOURCE|denik-artis-lisen|https://www.brnensky.denik.cz/|2026-08-03|news-index|Brno press (brnensky.denik.cz + efotbal.cz, found 2026-08-03): SK Lisen 2019 later renamed SK Artis Brno; the 2021 (0-3) and 2023 (0-1) home cup ties v Sparta were hosted by the same club carried here as Lisen"),
 ("SOURCE|wiki-cs-lokopraha|https://cs.wikipedia.org/wiki/FK_Loko_Praha|2026-08-03|wiki-index|FK Loko Praha club page: 'Do cervna roku 2024 nesl jmeno FK Loko Vltavin' - the in-window home tie 2021-09-22 (na Plynarne, att 740 per wf match report) was played under the Vltavin name; client-roster string Loko Praha reused"),
 ("SOURCE|zivevysledky-velke-hamry|https://zivevysledky.cz/stadium/hriste-tj-velke-hamry/|2026-08-03|web-index|stadium index: Hriste TJ Velke Hamry, Velke Hamry (address V.H. 550, grass) carrying the club's 2023-2024 Divize C home fixtures incl. the cup-period season"),
]

# ---- pack assembly ----
lines = []
lines.append("NOTE|info|pack_id|MOLCUP-2021-2026_BP-TEAM-PACK_v2 - return of WO-MOLCUP-BACKFILL-04 (issued 2026-08-02; opened after the RPL, RUSCUP and CZ1 returns passed gates, per the owner's one-at-a-time decree). Segment 2021-22/2022-23/2023-24 of the 5-year MOL Cup (Pohar FACR) span; new rows stop at the 2024-06-30 hard cutoff (2024-25 = 32 rows and 2025-26 = 31 rows already held and auditor-verified client-side, current season fills centrally). 120 MATCH rows = 41 + 41 + 38 by the auditor-proven slice rule in WO section-1. Compiled 2026-08-03.")
for s in SOURCES: lines.append(s)
for (name, lg, code, aliases, stadium, city, founded) in NEWTEAMS:
    lines.append("TEAM|%s|Czech Republic|%s|%s|%s|%s|%s|Czech Republic|||%s|" % (
        name, lg, code, aliases, stadium, city, founded))
lines.append("NOTE|info|federation_check|Section-0 federation scan on the finished pack: all 121 rows are MOL Cup (Pohar FACR sponsored name), every club Czech - Sparta Prague / Slavia Prague / Viktoria Plzen with Czech lower-league opponents; not Russia, not Slovakia, no other country's cup. Competition field verbatim 'MOL Cup' on every row.")
lines.append("NOTE|info|comp_class|compType is domestic-cup on EVERY row per the standing auditor errata ERRATA-2026-08-03 ('Cups = domestic-cup going forward'), which supersedes this workorder's section-2 grammar line '<compType>: domestic-league (our existing 63 cup rows use this)' - the supersession is logged here as instructed by the errata application rule used on the RPL/RUSCUP returns. FLAG for the auditor: the client-held 63 cup rows (2024-25 + 2025-26) still carry domestic-league and presumably need the same reclassing.")
lines.append("NOTE|info|slice|WO section-1 rule reproduced per season from the official brackets (every tie from the round where First-League clubs enter onward with >=1 of that season's 16 pinned clubs; ties with no FL club excluded): 2021-22 = 41 rows (R2 11 of 28 ties, R3 15 of 16, R16 8/8, QF 4/4, SF 2/2, Final 1/1); 2022-23 = 41 rows (R2 11 of 27, R3 15 of 16, R16 8/8, QF 4/4, SF 2/2, Final 1/1); 2023-24 = 38 rows (R2 11 of 27, R3 15 of 16, R16 6 of 8 - Velvary 1-2 Opava AND Dukla Prague 3-1 Vyskov have no FL club (Dukla was a CZ2 club in 2023-24; promoted to the top flight for 2024-25), QF 3 of 4 - Opava 2-0 Dukla Prague has no FL club, SF 2/2, Final 1/1). FL clubs enter R2 (non-UEFA) and R3 (the five UEFA entrants) per the wiki Teams tables and the 2023-24 section prose 'The last entrants are the five clubs involved into the European Cups.' FL clubs failing to reach R16 but inside the slice (their ties are rows here): 2021-22 Liberec lost R2 home 1-2 Zbuzany, Pardubice lost R3 at Jihlava 0-2; 2022-23 Pardubice lost R2 at Velvary 0-1, Jablonec lost R3 home 0-1 Vyskov, Viktoria Plzen lost R3 at Hlucin 2-3; 2023-24 Karvina lost R2 at Unicov 0-1, Teplice lost R3 at Vyskov 0-1, Slovacko lost R3 home 3-4 Dukla Prague, Pardubice lost R3 on penalties at Velvary.")
lines.append("NOTE|info|round_counts|Round-by-round in-slice counts tied to the source pages (the auditor recomputes the rule from the same pages): 2021-22 R2 11/28 - en.wikipedia.org/wiki/2021-22 Czech Cup sections 'Second round' (28 ties listed) and rsssf.org/tablest/tsje2022.html#cup for R16 onward; R3 15/16, R16 8, QF 4, SF 2, F 1. 2022-23 R2 11/27, R3 15/16, R16 8, QF 4, SF 2, F 1 (en.wikipedia.org/wiki/2022-23 Czech Cup; rsssf.org/tablest/tsje2023.html#cup). 2023-24 R2 11/27, R3 15/16, R16 6, QF 3, SF 2, F 1 (en.wikipedia.org/wiki/2023-24 Czech Cup; rsssf.org/tablest/tsje2024.html#cup). Pack totals 41 + 41 + 38 = 120.")
lines.append("NOTE|info|source_adaptation|RSSSF = the WO-designated primary, but its Czech season pages carry the cup FROM THE ROUND OF 16 onward only (1/8 Finals header; R2 and R3 are not on the page - raw-fact recorded, not inferred). R2/R3 coverage therefore built from the en.wiki season bracket sections (every tie transcribed) cross-verified tie-by-tie against worldfootball.net round pages (2-runde/3-runde); all dates and scores agree on 100% of the 165 in-scope plus out-of-scope ties checked. All eight R16 ties of each season are identical date+score+order across RSSSF, wiki and wf. Round labels on rows: R2 = the round FL non-UEFA clubs enter (wf '2. Round'), R3 = the round the five UEFA entrants join (wf '3. Round'), R16/QF/SF/Final thereafter. Czech convention in-window: R1-R4 level at 90' goes straight to penalties (no extra time; exception CBudejovice 1-1 Olomouc R16 2021-22 played aet first per RSSSF [aet, 4-5 pen]); QF onward plays extra time first.")
for (season, dt, h, a, w, detail) in ADV:
    outcome = "pens %s after the recorded 90-minute draw" % detail.split(" ",1)[1] if detail.startswith("pens") else "aet %s" % detail.split(" ",1)[1]
    lines.append("NOTE|info|advancement|%s %s %s vs %s: %s advanced (%s)" % (season, dt, h, a, w, outcome))
lines.append("NOTE|warning|source_conflict|Slovacko v Karvina 2021-11-12 (R16) is printed by BOTH bracket sources (RSSSF tsje2022 and the en.wiki Fourth-round bracket) as a plain 3-1 with no aet flag - but the worldfootball match report proves extra time (Jurecka equalized at 90', Cicilia 105' pen + 108'): the row carries the 90-minute score 1-1 with the advancement NOTE (Slovacko advanced aet 3-1) under the 90-minute doctrine; the wrongly-unflagged bracket printouts are documented here, not propagated (only silent-aet case found; all other aet/pso flags align across the three indexes).")
lines.append("NOTE|warning|source_conflict|Viktoria Plzen v Zlin (SF) date: RSSSF tsje2024 prints header [Apr 4] against the wiki match box 2024-04-24 18:00 and worldfootball 24.04.2024 18:00 - two independent indexes agree on 2024-04-24, so the row carries 2024-04-24 and RSSSF's Apr 4 is documented here (a griefing of the RFC hierarchy avoided: this is the one cell where RSSSF is contradicted by both independent indexes).")
lines.append("NOTE|info|identity|First-League clubs use the 17 pinned WO-02 section-3 strings verbatim incl. era renames (FC Fastav Zlin -> FC Trinity Zlin sponsor era, always Zlin; MFK Karvina = Karvina - FL 2021-22, FNL 2022-23, FL again 2023-24; FC Zbrojovka Brno = FL 2022-23 only, FNL in 2021-22 and 2023-24 - its 2022-23 R16/QF cup ties are in-slice, its 2021-22 and 2023-24 ties were out and are not rows). Reused client-roster identities (NOT re-declared as TEAM rows per section-3): Jihlava, Vyskov, Opava, Taborsko, Usti nad Labem, Varnsdorf, Trinec, Chrudim, Zizkov, Kromeriz, Frydek-Mistek, Loko Praha, Zapy, Domazlice, Hlucin, Brozany, Lanznot, Dukla Prague. Dukla Prague is legitimate here (CZ2 club 2021-24; the WO-02 anti-appear list does NOT apply to the cup per this workorder's explicit section-3 correction): its 2023-24 ties enter the slice only where an FL club participates (home 3-4 win at Slovacko in R3; its R16 and QF ties are out-of-slice all-CZ2 affairs). Loko Praha = the 2021-22 tie was played under the era name FK Loko Vltavin (club renamed FK Loko Praha June 2024 per cs.wiki); Lisen = the club renamed SK Artis Brno after the window (Brno press, Dec 2025) - worldfootball back-renames it 'SK Artis Brno' on ALL historical cup pages (documented wf quirk), rows carry Lisen; New TEAM rows declared only for the 31 genuinely-unknown clubs (TEAMREG ledger), each with tier evidence for the in-window season(s).")
lines.append("NOTE|info|venue_policy|Stadium/city per MATCH row: FL home grounds reuse the exact CZ1-pack strings per the standing consistency decree (incl. Sinobo Stadium 2021-22 -> Fortuna Arena for Slavia, Generali Ceska pojistovna Arena 2021-22 -> epet ARENA for Sparta, and Hradec Kralove's 2021-22 staging at Lokotrans Arena, MLADA BOLESLAV - applied to the QF 2022-02-15 and SF 2022-03-25 home cup ties per the wiki match boxes, city field follows the actual match location as in the league pack). Lower-league home grounds taken from the worldfootball season cup stadium indexes, else club/league pages: Vyskov carried as Sportovni areal Drnovice (the CZ1-file string; wf lists the same ground as 'Stadion FK Drnovice', Drnovice 6400); Hradec-Slavia R16 2023-12-06 carried at Malsovicka Arena (wf labels the ground 'FINEP Arena', its developer working name, capacity 9300 - alias documented); Brozany's ground has no published formal name - carried as Ke Hristi (the club's pitch address per sportmap.cz) with city Brozany nad Ohri; Usti nad Labem's Mestsky stadion per the club article. Final venues (neutral, wiki boxes): 2022 at Mestsky fotbalovy stadion Miroslava Valenty, Uherske Hradiste (att 7991); 2023 at epet ARENA, Prague (att 17037); 2024 at Doosan Arena, Plzen (att 10647).")
lines.append("NOTE|info|tier_codes|leagueCode on the 30 TEAM rows = the club's code in the in-window season it appears (membership transcribed in audit/ledger/molcup-venues-teams.txt section C from the cs.wiki CFL/MSFL/Divize season tables + en.wiki CNFL articles): CZ2 (FNL) = Vlasim, Pribram, Prostejov, Lisen; CZ3 (CFL A/B or MSFL) = Benesov, Hostoun, Sokolov, Prepere, Velvary, Zbuzany, Unicov, Blansko, Motorlet Praha, Rosice, Chlumec nad Cidlinou, Banik Most-Sous, Admira Praha, Kolin, Vysehrad (CFL A entrant 2021-22 reassigned to Prazsky prebor over the 2020-corruption-scandal ruling - 0 league matches recorded, cup tie of 2021-08-24 predates the reassignment); CZ4 (Divize) = Sedlcany (A), Slavicin (E), Brezova (B), Rokycany (A), Start Brno (D), Caslav (C), Chomutov (B), Velke Hamry (C), Hlubina (F), Sobeslav (A), Marianske Lazne (A), Kladno (B).")
lines.append("NOTE|info|spot_audit|Gate re-list, one full round per season with its source URL. 2021-22 R3 (wiki 'Third round' section, verified vs worldfootball.net/competition/co88/se39724 3-runde page): Vlasim 1-2 Sigma Olomouc; Jihlava 2-0 Pardubice; Opava 2-4 Mlada Boleslav; Viktoria Plzen 2-1 Pribram; Karvina 1-0 Chrudim; Prepere 0-1 Jablonec; Prostejov 0-4 Bohemians 1905; Trinec 0-1 Teplice; Zapy 0-4 Hradec Kralove; Zbuzany 1-2 Slovacko; Loko Praha 2-2 Banik Ostrava; Lisen 0-3 Sparta Prague; Velvary 2-4 Slavia Prague; Dukla Prague 1-3 Ceske Budejovice; Vyskov 1-1 Zlin (plus the out-of-slice Varnsdorf 4-2 Zbrojovka Brno). 2022-23 R3: Jablonec 0-1 Vyskov; Pribram 0-3 Teplice; Velvary 0-2 Banik Ostrava; Hlucin 3-2 Viktoria Plzen; Domazlice 1-6 Sparta Prague; Zapy 1-3 Sigma Olomouc; Chlumec nad Cidlinou 0-4 Hradec Kralove; Dukla Prague 0-4 Slavia Prague; Ceske Budejovice 3-1 Vlasim; Mlada Boleslav 4-0 Prostejov; Bohemians 1905 2-1 Trinec; Slovacko 6-0 Varnsdorf; Taborsko 1-2 Zbrojovka Brno; Frydek-Mistek 0-6 Slovan Liberec; Zlin 2-0 Jihlava (plus out-of-slice Sobeslav 0-2 Karvina). 2023-24 R3: Kladno 0-2 Slovan Liberec; Mlada Boleslav 4-2 Prostejov; Zapy 1-2 Banik Ostrava; Domazlice 1-1 Jablonec; Kromeriz 0-2 Slavia Prague; Vyskov 1-0 Teplice; Lisen 0-1 Sparta Prague; Slovacko 3-4 Dukla Prague; Jihlava 0-1 Hradec Kralove; Velvary 1-1 Pardubice; Ceske Budejovice 2-0 Chrudim; Zizkov 0-1 Sigma Olomouc; Unicov 1-2 Zlin; Kolin 1-7 Bohemians 1905; Marianske Lazne 0-10 Viktoria Plzen (plus out-of-slice Opava 3-2 Zbrojovka Brno).")
lines.append("NOTE|info|continuity|Boundary for the federation gap-free-span diff: rows begin 2021-08-24 (2021-22 R2 opening) and end 2024-05-22 (2023-24 Final) - all three finals played in May sit inside the window; no row at or after the 2024-06-30 hard cutoff. Held client rows 2024-25 (32) and 2025-26 (31) continue the chain; no official in-slice tie of the three compiled seasons is stored nowhere. Out-of-slice exclusions (ties with no FL club, per the rule) itemized for the auditor's recompute: 2021-22 R2 seventeen exclusions of 28 (full list in audit/ledger/molcup-2ndidx-2021-22.txt) + R3 Varnsdorf 4-2 Zbrojovka Brno; 2022-23 R2 sixteen exclusions of 27 + R3 Sobeslav 0-2 Karvina; 2023-24 R2 sixteen exclusions of 27 + R3 Opava 3-2 Zbrojovka Brno + R16 Dukla Prague 3-1 Vyskov + R16 Velvary 1-2 Opava + QF Opava 2-0 Dukla Prague.")
# ---- MATCH lines season-blocked date-sorted ----
COMP="MOL Cup"; CT="domestic-cup"
for season in ("2021-22","2022-23","2023-24"):
    block = sorted([r for r in R if r[0]==season], key=lambda x:(x[1],x[2],x[5]))
    for (s,dt,h,hg,ag,a,rd,stad,city,src) in block:
        lines.append("MATCH|%s|%s|%s|%s|%d|%d|%s|%s|%s|%s|Czech Republic||%s" % (dt,COMP,CT,h,hg,ag,a,rd,stad,city,src))
lines.append("END")

# ---- gates ----
errs=[]
def chk(cond,msg):
    if not cond: errs.append(msg)
setrset = set()
ALLOWED_FIELDS = 14
for i,l in enumerate(lines):
    if not all(ord(c)<128 for c in l): errs.append("non-ASCII line %d"%i)
    if l.startswith("MATCH|"):
        f=l.split("|")
        chk(len(f)==ALLOWED_FIELDS,"MATCH field count %d line %d"%(len(f),i))
        _,dt,comp,ct,h,hg,ag,a,rd,stad,city,country,blank,src = f
        chk(comp==COMP,"competition literal line %d"%i)
        chk(ct==CT,"compType line %d"%i)
        chk(re.fullmatch(r"20\d\d-\d\d-\d\d",dt) is not None,"date format line %d"%i)
        chk("2021-07-01"<=dt<"2024-06-30","boundary line %d"%i)
        chk(rd in ("R2","R3","R16","QF","SF","Final"),"round label line %d"%i)
        chk(blank=="" and country=="Czech Republic","country/blank line %d"%i)
        key=(dt,h,a)
        chk(key not in setrset,"duplicate tie %s line %d"%(key,i)); setrset.add(key)
# row counts
m=[l for l in lines if l.startswith("MATCH|")]
chk(len(m)==120,"total MATCH rows %d != 120"%len(m))
per={"2021-22":0,"2022-23":0,"2023-24":0}; rper={}
for l in m:
    dt=l.split("|")[1]; rd=l.split("|")[8]
    se = "2021-22" if dt<"2022-07-01" else ("2022-23" if dt<"2023-07-01" else "2023-24")
    per[se]+=1; rper[(se,rd)]=rper.get((se,rd),0)+1
chk(per["2021-22"]==41,"2021-22 rows %d"%per["2021-22"])
chk(per["2022-23"]==41,"2022-23 rows %d"%per["2022-23"])
chk(per["2023-24"]==38,"2023-24 rows %d"%per["2023-24"])
for se,expect in (("2021-22",{"R2":11,"R3":15,"R16":8,"QF":4,"SF":2,"Final":1}),
                  ("2022-23",{"R2":11,"R3":15,"R16":8,"QF":4,"SF":2,"Final":1}),
                  ("2023-24",{"R2":11,"R3":15,"R16":6,"QF":3,"SF":2,"Final":1})):
    for rd,n in expect.items():
        chk(rper.get((se,rd),0)==n,"%s %s rows %d != %d"%(se,rd,rper.get((se,rd),0),n))
# slice gate: every row has >=1 FL club of its season
for l in m:
    f=l.split("|"); dt=f[1]; h=f[4]; a=f[7]
    se = "2021-22" if dt<"2022-07-01" else ("2022-23" if dt<"2023-07-01" else "2023-24")
    chk(h in FL[se] or a in FL[se],"slice: no FL club in row %s %s v %s"%(dt,h,a))
    # FL membership correctness: only season-appropriate FL strings
    for side in (h,a):
        if side in FL["2021-22"]+FL["2022-23"]+FL["2023-24"]:
            pass
chk(set(h for h in [l.split('|')[4] for l in m]) | set(a for a in [l.split('|')[7] for l in m]) <= set(FL['2021-22']+ROSTER+NEWTEAM_NAMES+['Zbrojovka Brno']) - set([]),
    "identity universe mismatch")
# identity: every used string is pinned-FL (season-mapped by the slice gate), roster or a declared TEAM
# TEAM rows: declared set == the 30 new, none of the roster 26 declared
tm=[l.split("|")[1] for l in lines if l.startswith("TEAM|")]
chk(sorted(tm)==sorted(NEWTEAM_NAMES),"TEAM rows set mismatch")
chk(not (set(tm)&set(ROSTER)),"TEAM row re-declares roster identity")
# non-FL strings used in rows must be Roster, a new TEAM, or Zbrojovka Brno
used=set()
for l in m:
    f=l.split("|"); used.add(f[4]); used.add(f[7])
ok=set(FL["2021-22"]+FL["2022-23"]+FL["2023-24"]+ROSTER+NEWTEAM_NAMES+["Zbrojovka Brno"])
chk(used<=ok,"unknown strings used: %s"%(used-ok))
# every new TEAM actually used
chk(all(t in used for t in NEWTEAM_NAMES),"TEAM declared but unused: %s"%([t for t in NEWTEAM_NAMES if t not in used]))
# advancement gate: 20 NOTEs, one per settled tie, names coherent, recorded draw in 90'
adv=[l for l in lines if "|advancement|" in l]
chk(len(adv)==20,"advancement NOTE count %d"%len(adv))
# settled-tie check against the ADV registry:
advkeys={(dt,h,a) for (se,dt,h,a,w,d) in ADV}
draws=[(l.split("|")[1],l.split("|")[4],l.split("|")[7]) for l in m if l.split("|")[5]==l.split("|")[6]]
# only draws that were settled by aet/pens belong to ADV (single-leg knockout draws cannot stand without resolution)
for dk in draws:
    chk(dk in advkeys,"settled draw without advancement NOTE: %s"%(dk,))
for (dt,h,a) in advkeys:
    chk((dt,h,a) in draws,"advancement NOTE for a non-draw row: %s"%((dt,h,a),))
for (se,dt,h,a,w,d) in ADV:
    row=[l for l in m if l.split("|")[1]==dt and l.split("|")[4]==h and l.split("|")[7]==a][0]
    chk(h in row.split("|")[4],"advancement home mismatch")
# bracket gate: champions + finalists + semifinalists per season
def winner(row):
    f=row.split("|"); hg,ag=int(f[5]),int(f[6])
    if hg>ag: return f[4]
    if hg<ag: return f[7]
    dt,h,a=f[1],f[4],f[7]
    for (se,adt,ah,aa,w,d) in ADV:
        if (adt,ah,aa)==(dt,h,a): return w
    return None
br={}
for l in m:
    f=l.split("|"); dt=f[1]
    se = "2021-22" if dt<"2022-07-01" else ("2022-23" if dt<"2023-07-01" else "2023-24")
    br.setdefault(se,[]).append((f[8],l))
for se,champ,finalists,sfs in (("2021-22","Slovacko",{"Slovacko","Sparta Prague"},
        {"Sparta Prague","Jablonec","Hradec Kralove","Slovacko"}),
    ("2022-23","Slavia Prague",{"Sparta Prague","Slavia Prague"},
        {"Sparta Prague","Ceske Budejovice","Slavia Prague","Bohemians 1905"}),
    ("2023-24","Sparta Prague",{"Viktoria Plzen","Sparta Prague"},
        {"Opava","Sparta Prague","Viktoria Plzen","Zlin"})):
    finals=[l for (rd,l) in br[se] if rd=="Final"]
    chk(len(finals)==1,"%s Final rows %d"%(se,len(finals)))
    f=finals[0].split("|"); chk({f[4],f[7]}==finalists,"%s finalists %s"%(se,(f[4],f[7])))
    chk(winner(finals[0])==champ,"%s champion %s"%(se,winner(finals[0])))
    got=set()
    for (rd,l) in br[se]:
        if rd=="SF":
            ff=l.split("|"); got.add(ff[4]); got.add(ff[7])
    chk(got==sfs,"%s semifinalists %s"%(se,got))
# END + source labels used exist
srclabels={l.split("|")[1] for l in lines if l.startswith("SOURCE|")}
for l in m:
    chk(l.split("|")[-1] in srclabels,"row source label not declared: %s"%l.split("|")[-1])
chk(lines[-1]=="END","END terminator")
chk(len([l for l in lines if l.startswith("MATCH|")])==len(set((l.split('|')[1],l.split('|')[4],l.split('|')[7]) for l in m)),"dupes")

txt="\n".join(lines)+"\n"
if errs:
    print("GATE FAILURES (%d):"%len(errs))
    for e in errs: print(" -",e)
    sys.exit(1)
os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,"w",encoding="ascii").write(txt)
h=hashlib.sha256(txt.encode("ascii")).hexdigest()
print("OK %d lines, %d MATCH, %d TEAM, %d SOURCE, %d NOTE -> sha256 %s"%(
    len(lines),len(m),len(tm),len([l for l in lines if l.startswith('SOURCE|')]),
    len([l for l in lines if l.startswith('NOTE|')]),h))
