#!/usr/bin/env python3
"""INDEPENDENT RSSSF RE-PARSE + pack verification (auditor-owned, fresh code). v2"""
import re, html, unicodedata, datetime, collections, sys, os

REF = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/REFERENCE/rsssf-ref"
PACK_BASE = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/AUDITS/AUDIT-OVERRIDE-2026-08-04"

MONTHS = {m: i+1 for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())

RUS_ALIASES = {
    "rostov":"FC Rostov","fk rostov":"FC Rostov","dinamo":"Dynamo Moscow","dinamo ms":"Dynamo Moscow",
    "dinamo moskva":"Dynamo Moscow","dinamo mh":"Dynamo Makhachkala","dinamo makhachkala":"Dynamo Makhachkala",
    "cska":"CSKA Moscow","cska moskva":"CSKA Moscow","lokomotiv":"Lokomotiv Moscow",
    "lokomotiv moskva":"Lokomotiv Moscow","spartak":"Spartak Moscow","spartak moskva":"Spartak Moscow",
    "zenit":"Zenit St Petersburg","zenit sankt-peterburg":"Zenit St Petersburg","zenit st petersburg":"Zenit St Petersburg",
    "khimki":"FC Khimki","himki":"FC Khimki","fc khimki":"FC Khimki","rubin":"Rubin Kazan","rubin kazan":"Rubin Kazan",
    "arsenal":"Arsenal Tula","arsenal tula":"Arsenal Tula","ufa":"FC Ufa","fc ufa":"FC Ufa",
    "ural":"Ural Yekaterinburg","ural yekaterinburg":"Ural Yekaterinburg",
    "krylya sovetov samara":"Krylia Sovetov Samara","ks samara":"Krylia Sovetov Samara",
    "krylja s.":"Krylia Sovetov Samara","krylia sovetov":"Krylia Sovetov Samara","krylya sovetov":"Krylia Sovetov Samara",
    "krylja sovetov":"Krylia Sovetov Samara","krylja sovetov samara":"Krylia Sovetov Samara",
    "ahmat":"Akhmat Grozny","akhmat":"Akhmat Grozny","ahmat grozny":"Akhmat Grozny","akhmat grozny":"Akhmat Grozny",
    "fakel":"Fakel Voronezh","fakel voronezh":"Fakel Voronezh","sochi":"PFC Sochi","pfc sochi":"PFC Sochi",
    "orenburg":"FC Orenburg","fc orenburg":"FC Orenburg","pari nn":"Pari Nizhny Novgorod",
    "pari nizhniy novgorod":"Pari Nizhny Novgorod","nnovgorod":"Pari Nizhny Novgorod",
    "fc nizhniy novgorod":"Pari Nizhny Novgorod","torpedo":"Torpedo Moscow","torpedo moskva":"Torpedo Moscow",
    "t. moscow":"Torpedo Moscow","baltika":"Baltika Kaliningrad","baltika kaliningrad":"Baltika Kaliningrad",
    "krasnodar":"FC Krasnodar","fc krasnodar":"FC Krasnodar",
    "akron":"Akron Tolyatti","akron togliatti":"Akron Tolyatti","akron tolyatti":"Akron Tolyatti",
    "yenisey":"Yenisey Krasnoyarsk","yenisey krasnoyarsk":"Yenisey Krasnoyarsk","ska":"SKA Khabarovsk",
    "ska khabarovsk":"SKA Khabarovsk","rodina":"Rodina Moscow","rodina moscow":"Rodina Moscow",
    "rodina moskva":"Rodina Moscow","rotor":"Rotor Volgograd","rotor volgograd":"Rotor Volgograd",
    "zenit sankt peterburg":"Zenit St Petersburg","zenit st-peterburg":"Zenit St Petersburg",
    "krasnodar d1":"FC Krasnodar","khimki d1":"FC Khimki",
    "fc sochi":"PFC Sochi","sochi d1":"PFC Sochi","fc soci":"PFC Sochi","soci":"PFC Sochi",
    "fc soci":"PFC Sochi","soci":"PFC Sochi","soči":"PFC Sochi","fc soči":"PFC Sochi",
    "dinamo mahackala":"Dynamo Makhachkala","dinamo mahackalá":"Dynamo Makhachkala",
    # Russian Cup opponents (FNL/D3 clubs facing RPL sides; pack roster strings)
    "alania vladikavkaz":"Alania Vladikavkaz","alania":"Alania Vladikavkaz",
    "chaika peschanokopskoe":"Chaika Peschanokopskoe","chaika":"Chaika Peschanokopskoe",
    "dinamo barnaul":"Dinamo Barnaul","barnaul":"Dinamo Barnaul",
    "dinamo briansk":"Dinamo Bryansk","dinamo bryansk":"Dinamo Bryansk","dinamo brjansk":"Dinamo Bryansk",
    "dinamo stavropol":"Dinamo Stavropol","dinamo stavropol [d3]":"Dinamo Stavropol",
    "fc saransk":"FC Saransk","saransk":"FC Saransk",
    "kamaz":"KAMAZ","kamaz naberezhnyye chelny":"KAMAZ","kamaz naberezhniye chelny":"KAMAZ",
    "kuban krasnodar":"Kuban Krasnodar","kuban":"Kuban Krasnodar",
    "legion-dinamo makhachkala":"Legion-Dinamo Makhachkala","legion makhachkala":"Legion-Dinamo Makhachkala",
    "legion":"Legion-Dinamo Makhachkala","legion (makhachkala)":"Legion-Dinamo Makhachkala",
    "leningradets sankt-peterburg":"Leningradets St-Peterburg","leningradets":"Leningradets St-Peterburg",
    "leningradets st-peterburg":"Leningradets St-Peterburg",
    "metallurg lipetsk":"Metallurg Lipetsk","metallurg":"Metallurg Lipetsk",
    "neftekhimik nizhnekamsk":"Neftekhimik Nizhnekamsk","neftehimik niznekamsk":"Neftekhimik Nizhnekamsk",
    "qayrat moskva":"Qayrat Moskva","qayrat":"Qayrat Moskva",
    "shinnik yaroslavl":"Shinnik Yaroslavl","shinnik":"Shinnik Yaroslavl",
    "sinnik":"Shinnik Yaroslavl","sinnik yaroslavl":"Shinnik Yaroslavl",
    "torpedo vladimir":"Torpedo Vladimir","torpedo vladimir":"Torpedo Vladimir",
    "tyumen":"Tyumen","fc tiumen":"Tyumen","fc tjumen":"Tyumen",
    "veles moskva":"Veles Moskva","veles":"Veles Moskva",
    "volga ulyanovsk":"Volga Ulyanovsk","volga":"Volga Ulyanovsk",
    "volgar astrakhan":"Volgar Astrakhan","volgar":"Volgar Astrakhan",
    "zenit izhevsk":"Zenit Izhevsk","izhevsk":"Zenit Izhevsk",
    "znamya noginsk":"Znamya Noginsk","znamia noginsk":"Znamya Noginsk","znamya":"Znamya Noginsk",
    "zvezda sankt-peterburg":"Zvezda Sankt-Peterburg","zvezda":"Zvezda Sankt-Peterburg",
    "sokol saratov":"Sokol Saratov","sokol":"Sokol Saratov",
}

# city-in-parentheses disambiguator (RSSSF accented transliterations)
CITY_MAP = {
    "mahačkalá":"Dynamo Makhachkala","mahackala":"Dynamo Makhachkala",
    "n.novgorod":"Pari Nizhny Novgorod","niznij novgorod":"Pari Nizhny Novgorod",
    "nížnij nóvgorod":"Pari Nizhny Novgorod","n.nóvgorod":"Pari Nizhny Novgorod",
    "togliatti":"Akron Tolyatti","krasnoyarsk":"Yenisey Krasnoyarsk",
    "voronezh":"Fakel Voronezh","volgograd":"Rotor Volgograd",
}
CZE_ALIASES = {
    "jablonec":"Jablonec","fk jablonec":"Jablonec","fk jablonec 97":"Jablonec","ostrava":"Banik Ostrava",
    "banik ostrava":"Banik Ostrava","fc banik ostrava":"Banik Ostrava","pardubice":"Pardubice",
    "fk pardubice":"Pardubice","karvina":"Karvina","mfk karvina":"Karvina","mfk okd karvina":"Karvina",
    "hradec kralove":"Hradec Kralove","fc hradec kralove":"Hradec Kralove",
    "bohemians":"Bohemians 1905","bohemians 1905":"Bohemians 1905","fc bohemians 1905 praha":"Bohemians 1905",
    "bohemians praha 1905":"Bohemians 1905","bohemians 1905 praha":"Bohemians 1905",
    "sparta":"Sparta Prague","ac sparta praha":"Sparta Prague","sparta praha":"Sparta Prague",
    "olomouc":"Sigma Olomouc","sigma olomouc":"Sigma Olomouc","sk sigma olomouc":"Sigma Olomouc",
    "plzen":"Viktoria Plzen","viktoria plzen":"Viktoria Plzen","fc viktoria plzen":"Viktoria Plzen",
    "mlada boleslav":"Mlada Boleslav","fk mlada boleslav":"Mlada Boleslav",
    "ceske budejovice":"Ceske Budejovice","sk dynamo ceske budejovice":"Ceske Budejovice",
    "dynamo ceske budejovice":"Ceske Budejovice","teplice":"Teplice","fk teplice":"Teplice",
    "liberec":"Slovan Liberec","slovan liberec":"Slovan Liberec","fc slovan liberec":"Slovan Liberec",
    "slovacko":"Slovacko","1. fc slovacko":"Slovacko","1.fc slovacko":"Slovacko","zlin":"Zlin",
    "fc zlin":"Zlin","fc fastav zlin":"Zlin","trinity zlin":"Zlin","slavia":"Slavia Prague",
    "slavia praha":"Slavia Prague","sk slavia praha":"Slavia Prague","zbrojovka":"Zbrojovka Brno",
    "zbrojovka brno":"Zbrojovka Brno","1. fc zbrojovka brno":"Zbrojovka Brno","1.fc zbrojovka brno":"Zbrojovka Brno",
    "dukla":"Dukla Prague","fk dukla praha":"Dukla Prague","vyskov":"Vyskov","mfk vyskov":"Vyskov",
    "taborsko":"Taborsko","fk mas taborsko":"Taborsko","vlasim":"Vlasim",
    "fc sellier & bellot vlasim":"Vlasim","pribram":"Pribram","1. fk pribram":"Pribram",
    "1.fk pribram":"Pribram","opava":"Opava","slezsky fc opava":"Opava","sfc opava":"Opava",
    "chrudim":"Chrudim","mfk chrudim":"Chrudim","lisen":"Lisen","sk lisen 2019":"Lisen","sk lisen":"Lisen",
    "artis brno":"Artis Brno","sigma olomouc b":"Sigma Olomouc B","slavia praha b":"Slavia Prague B",
    "banik ostrava b":"Banik Ostrava B","ac sparta praha b":"Sparta Prague B",
    "brno":"Zbrojovka Brno","fc zbrojovka brno":"Zbrojovka Brno",
}

def build_resolver(alias_map):
    return {norm(k): v for k, v in alias_map.items()}

def resolve(name, resolver):
    n = norm(name)
    if n in resolver:
        return resolver[n]
    # parenthesised city disambiguator (e.g. Dinámo (Mahačkalá))
    m = re.search(r'\(([^)]*)\)', name)
    if m:
        city = norm(m.group(1))
        if city in CITY_MAP:
            return CITY_MAP[city]
    # paren-stripped fallback
    np = norm(re.sub(r'\([^)]*\)', '', name))
    if np != n:
        if np in resolver:
            return resolver[np]
        np2 = re.sub(r'^(fc|sk|fk|sc|tsv|1\.?fc|1\.?sk|1\.?fk)\s*', '', np)
        if np2 in resolver:
            return resolver[np2]
    n2 = re.sub(r'^(fc|sk|fk|sc|tsv|1\.?fc|1\.?sk|1\.?fk)\s*', '', n)
    if n2 in resolver:
        return resolver[n2]
    return None

DATE_RE = re.compile(r'\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2})')
MATCH_RE = re.compile(r'^\s*(.*?)\s+(\d{1,2})\s*-\s*(\d{1,2})\s+(.*?)\s*$')
SECTION_ANCHORS = {
    'a name="kubok"': 'cup', 'a name="cupdet"': 'cup', 'a name="sup"': 'sup',
    'a name="prorel"': 'prorel', 'a name="middle"': 'evropu', 'a name="releg"': 'zachranu',
    'a name="cup"': 'cup',
}

def parse_file(fname, y1, resolver):
    y2 = y1 + 1
    with open(f"{REF}/{fname}", encoding='utf-8-sig', errors='replace') as f:
        text = html.unescape(f.read())
    lines = text.splitlines()
    out, warnings = [], []
    section = 'other'
    cur_date = None
    cur_date2 = None
    last_date = datetime.date(y1, 6, 30)
    league_done = False
    n = len(lines); i = 0

    def reset():
        nonlocal cur_date, cur_date2, last_date
        cur_date = None
        cur_date2 = None
        last_date = datetime.date(y1, 6, 30)

    def resolve_date(mon, day):
        # Season-structural rule: Jul-Dec -> year1, Jan-Jun -> year2.
        # (RSSSF prints postponed matches inside their round block, so file
        #  order is NOT chronological; a rolling anchor is therefore wrong.)
        return datetime.date(y2 if mon <= 6 else y1, mon, day)

    while i < n:
        raw = lines[i]
        line = raw.strip()
        low = line.lower()

        anchored = False
        for k, s in SECTION_ANCHORS.items():
            if k in low:
                section = s
                reset()
                if s == 'cup':
                    league_done = True
                anchored = True
                break
        if anchored:
            i += 1; continue

        mr = re.match(r'^round\s+(\d{1,2})', low)
        if mr:
            rn = int(mr.group(1))
            if section == 'cup':
                pass  # cup round labels
            elif rn <= 30 and not league_done:
                section = 'league'
            elif rn <= 30:
                section = 'other'  # details re-listing after league done
            elif section in ('zachranu',):
                section = 'zachranu'
            elif section == 'evropu':
                section = 'evropu'
            elif not league_done:
                section = 'titul'
            else:
                section = 'other'
            m = DATE_RE.search(line)
            if m:
                cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
            i += 1; continue

        if section == 'league' and low.startswith('total games played'):
            league_done = True
            section = 'other'
            i += 1; continue

        if section in ('evropu','prorel') and re.match(r'^(first leg|second leg|first legs|second legs|final)\b', low):
            m = DATE_RE.search(line)
            if m:
                cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
            i += 1; continue
        # combined two-leg line in prorel/cup: "Home 1-2 3-1 Away [agg ...]"
        if section in ('prorel','cup') and re.match(r'^\s*(.+?)\s+(\d{1,2})-(\d{1,2})\s+(\d{1,2})-(\d{1,2})\s+(.+?)\s*$', raw):
            cm = re.match(r'^\s*(.+?)\s+(\d{1,2})-(\d{1,2})\s+(\d{1,2})-(\d{1,2})\s+(.+?)\s*$', raw)
            h_raw = html.unescape(cm.group(1)).strip()
            a_raw = html.unescape(cm.group(6)).strip()
            a_raw = re.sub(r'\s*\[[^\]]*\]\s*$', '', a_raw).strip()
            h = resolve(h_raw, resolver)
            a = resolve(a_raw, resolver)
            if h and a and cur_date:
                out.append({"date": cur_date.isoformat(), "home": h, "away": a,
                            "hg": int(cm.group(2)), "ag": int(cm.group(3)), "section": section, "raw": raw.strip()})
                if cur_date2 is not None:
                    out.append({"date": cur_date2.isoformat(), "home": h, "away": a,
                                "hg": int(cm.group(4)), "ag": int(cm.group(5)), "section": section, "raw": raw.strip()})
            i += 1; continue

        if low == '</pre>' and section in ('prorel','cup','sup'):
            section = 'other'
            i += 1; continue

        if re.match(r'^(first round|second round|third round|fourth round|round of 16|1/8 finals|quarterfinals|semifinals|final|rpl path|fnl path|group stage|upper bracket|lower bracket)', low) and section == 'cup':
            m = DATE_RE.search(line)
            if m:
                cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
                mm2 = re.search(r'\[(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2}\s*,\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+)?(\d{1,2})\]', line)
                if mm2:
                    mon2 = MONTHS[mm2.group(1).split()[0]] if mm2.group(1) else MONTHS[m.group(1)]
                    cur_date2 = resolve_date(mon2, int(mm2.group(2)))
                else:
                    cur_date2 = None
            i += 1; continue

        m = DATE_RE.search(line)
        if m and (line.startswith('[') or section == 'cup'):
            cur_date = resolve_date(MONTHS[m.group(1)], int(m.group(2)))
            # two-date header like "[May 20, 23]" (same month, second bare day)
            dm2 = re.findall(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2})', line)
            if len(dm2) >= 2:
                cur_date2 = resolve_date(MONTHS[dm2[1][0]], int(dm2[1][1]))
            else:
                mm2 = re.search(r'\[(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2}\s*,\s*(\d{1,2})\]', line)
                if mm2:
                    cur_date2 = resolve_date(MONTHS[m.group(1)], int(mm2.group(1)))
                else:
                    cur_date2 = None
            i += 1; continue

        mm = MATCH_RE.match(raw)
        if mm and section in ('league','titul','zachranu','evropu','cup','prorel','sup'):
            h_raw = html.unescape(mm.group(1)).strip()
            a_raw = html.unescape(mm.group(4)).strip()
            h_raw = re.sub(r'\s*\[[^\]]*\]\s*', ' ', h_raw).strip()
            a_raw = re.sub(r'\s*\[[^\]]*\]\s*', ' ', a_raw).strip()
            h = resolve(h_raw, resolver)
            a = resolve(a_raw, resolver)
            if h is None or a is None:
                i += 1; continue
            if cur_date is None:
                warnings.append(f"NO DATE: {fname} {h_raw} {mm.group(2)}-{mm.group(3)} {a_raw}")
                i += 1; continue
            out.append({"date": cur_date.isoformat(), "home": h, "away": a,
                        "hg": int(mm.group(2)), "ag": int(mm.group(3)),
                        "section": section, "raw": raw.strip()})
        i += 1
    return out, warnings

def load_pack_rows(fname, comp_include=None):
    sys.path.insert(0, 'audit_work')
    from pack_parse import parse_pack
    p = parse_pack(f"{PACK_BASE}/{fname}")
    rows = []
    for m in p['matches']:
        if comp_include and m['competitionName'] not in comp_include:
            continue
        rows.append({"date": m['dateISO'], "home": m['homeName'], "away": m['awayName'],
                     "hg": m['homeGoals'], "ag": m['awayGoals'], "comp": m['competitionName']})
    return rows

def compare(pack_rows, rsssf_rows, label, expect_extra=0):
    rs = collections.defaultdict(list)
    for r in rsssf_rows:
        rs[(r['date'], r['home'], r['away'])].append((r['hg'], r['ag']))
    exact = miss = score = 0
    score_list, missing_list = [], []
    for p in pack_rows:
        k = (p['date'], p['home'], p['away'])
        if k in rs:
            if any(hg == p['hg'] and ag == p['ag'] for hg, ag in rs[k]):
                exact += 1
            else:
                score += 1
                score_list.append((p, rs[k]))
        else:
            k2 = (p['date'], p['away'], p['home'])
            if k2 in rs and any(ag == p['hg'] and hg == p['ag'] for hg, ag in rs[k2]):
                exact += 1
            else:
                miss += 1
                missing_list.append(p)
    pk_set = set()
    for p in pack_rows:
        pk_set.add((p['date'], p['home'], p['away']))
        pk_set.add((p['date'], p['away'], p['home']))
    extra = [r for r in rsssf_rows if (r['date'], r['home'], r['away']) not in pk_set]
    print(f"== {label} ==")
    print(f"  pack rows: {len(pack_rows)} | rsssf parsed: {len(rsssf_rows)} | EXACT: {exact} | SCORE-MISMATCH: {score} | MISSING: {miss} | rsssf-extra: {len(extra)}")
    for p, s in score_list[:8]:
        print(f"    SCORE-MISMATCH: pack {p['date']} {p['home']} {p['hg']}-{p['ag']} {p['away']} ({p['comp']}) | rsssf {s}")
    for p in missing_list[:8]:
        print(f"    MISSING: pack {p['date']} {p['home']} {p['hg']}-{p['ag']} {p['away']} ({p['comp']})")
    ex = collections.Counter((r['section']) for r in extra)
    print(f"    extra by section: {dict(ex)}")
    return exact, score, miss

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all","rpl"):
        res = build_resolver(RUS_ALIASES)
        for y1, fn, season in [(2021,"rus2022.txt","2021-22"),(2022,"rus2023.txt","2022-23"),
                               (2023,"rus2024.txt","2023-24"),(2024,"rus2025.txt","2024-25"),
                               (2025,"rus2026.txt","2025-26")]:
            rows, warns = parse_file(fn, y1, res)
            rel = [r for r in rows if r['section'] in ('league','prorel')]
            pack = load_pack_rows("RPL-2021-2026.txt", {"Russian Premier League","Russian Relegation Playoffs"})
            pk = [p for p in pack if (p['date'].startswith(f"{y1}-") and p['date'][5:7] >= '07') or (p['date'].startswith(f"{y1+1}-") and p['date'][5:7] <= '06')]
            compare(pk, rel, f"RPL {season} (league+playoff) vs rsssf")
            if warns: print("   warns:", warns[:4])
    if which in ("all","cz1"):
        res = build_resolver(CZE_ALIASES)
        for y1, fn, season in [(2021,"tsje2022.txt","2021-22"),(2022,"tsje2023.txt","2022-23"),
                               (2023,"tsje2024.txt","2023-24"),(2024,"tsje2025.txt","2024-25"),
                               (2025,"tsje2026.txt","2025-26")]:
            rows, warns = parse_file(fn, y1, res)
            rel = [r for r in rows if r['section'] in ('league','titul','zachranu','evropu','prorel')]
            pack = load_pack_rows("CZ1-2021-2026.txt", {"Czech First League","Czech Relegation Playoffs"})
            pk = [p for p in pack if (p['date'].startswith(f"{y1}-") and p['date'][5:7] >= '07') or (p['date'].startswith(f"{y1+1}-") and p['date'][5:7] <= '06')]
            compare(pk, rel, f"CZ1 {season} vs rsssf")
            if warns: print("   warns:", warns[:4])
