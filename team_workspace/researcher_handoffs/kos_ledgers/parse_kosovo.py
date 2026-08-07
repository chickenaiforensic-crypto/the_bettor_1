#!/usr/bin/env python3
"""Parse Kosovo Superliga + Kupa e Kosoves from RSSSF transcriptions (2021-22..2024-25)
and the worldfootball carrier for 2025-26. Emits per-season JSON rows + ledgers + gates."""
import json, re, datetime
from collections import Counter

LEDGER = 'team_workspace/researcher_handoffs/kos_ledgers'

CANON = {
    'Ballkani': 'KF Ballkani', 'Drita': 'Drita', 'Gjilani': 'Gjilani', 'Llapi': 'Llapi',
    'Prishtina': 'Prishtina', 'Drenica': 'Drenica Skenderaj', 'Dukagjini': 'Dukagjini',
    'Malisheva': 'Malisheva', 'Ferizaj': 'Ferizaj', 'Ulpiana': 'Ulpiana',
    'Feronikeli': 'Feronikeli', "Trepca'89": "Trepça'89", 'Fushe Kosova': 'Fushë Kosova',
    'Liria': 'Liria', 'Suhareka': 'Suhareka', 'Prisht. e Re': 'Prishtina E Re',
    'Prishtina e Re': 'Prishtina E Re', "Ph'nix-Banje": 'Phoenix-Banje',
    'Prishtina KF': 'Prishtina', 'Drenica KF': 'Drenica Skenderaj',
}

MEMBERSHIP = {
    '2021-22': {'KF Ballkani','Drita','Gjilani','Llapi','Prishtina','Drenica Skenderaj',
                'Dukagjini','Malisheva','Ulpiana','Feronikeli'},
    '2022-23': {'KF Ballkani','Drita','Gjilani','Dukagjini','Prishtina','Malisheva','Llapi',
                'Ferizaj',"Trepça'89",'Drenica Skenderaj'},
    '2023-24': {'KF Ballkani','Llapi','Drita','Malisheva','Prishtina','Gjilani','Dukagjini',
                'Feronikeli','Fushë Kosova','Liria'},
    '2024-25': {'Drita','KF Ballkani','Malisheva','Gjilani','Ferizaj','Prishtina','Dukagjini',
                'Llapi','Suhareka','Feronikeli'},
    '2025-26': {'Drita','Malisheva','KF Ballkani','Dukagjini','Gjilani','Drenica Skenderaj',
                'Prishtina','Llapi','Ferizaj','Prishtina E Re'},
}

MONTHS = {m: i for i, m in enumerate(['Jan','Feb','Mar','Apr','May','Jun',
                                      'Jul','Aug','Sep','Oct','Nov','Dec'], 1)}
NAME = re.compile(r"^([A-Za-z\.\' \-]+?)\s+")

def norm(s):
    s = s.strip()
    return CANON.get(s, s)

def parse_rsssf_league(path, season):
    lines = open(path, encoding='utf-8').read().splitlines()
    rounds = {}
    cur = None
    for l in lines:
        t = l.strip()
        if t.startswith('Promotion/Relegation Playoff') or t.startswith('Kupa'):
            break
        m = re.match(r'^Round (\d+)( \[([A-Za-z]{3}) (\d{1,2})\])?', t)
        if m:
            cur = int(m.group(1))
            rounds.setdefault(cur, [])
            if m.group(3):
                rounds[cur].append(('date', m.group(3), int(m.group(4))))
            continue
        if cur is None:
            continue
        m = re.match(r'^\[([A-Za-z]{3}) (\d{1,2})\]', t)
        if m:
            rounds[cur].append(('date', m.group(1), int(m.group(2))))
            continue
        m = re.match(r'^([\w\.\' \&\-]+?)\s+awd\s+([\w\.\' \&\-]+)\s*(.*)$', t)
        if m:
            home, away, note = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            am = re.search(r'awarded\s+(\d+)-(\d+)', note)
            hg, ag = (am.group(1), am.group(2)) if am else ('3', '0')
            rounds[cur].append(('match', home, hg, ag, away, t, f'awarded {hg}-{ag}; {note}'))
            continue
        m = re.match(r'^([\w\.\' \&\-]+?)\s+(\d+)-(\d+)\s+([\w\.\' \&\-]+)\s*(.*)$', t)
        if m:
            home, hg, ag, away, note = (m.group(i).strip() for i in (1, 2, 3, 4, 5))
            rounds[cur].append(('match', home, hg, ag, away, t, note))
            continue
    rows = []
    y0 = int(season[:4])
    for r in sorted(rounds):
        cur_date = None
        for e in rounds[r]:
            if e[0] == 'date':
                mon, day = e[1], e[2]
                year = y0 if mon in ('Aug','Sep','Oct','Nov','Dec') else y0 + 1
                cur_date = f'{year}-{MONTHS[mon]:02d}-{day:02d}'
                continue
            _, home, hg, ag, away, raw, note = e
            if cur_date is None:
                raise SystemExit(f'no date for match in round {r} of {season}: {raw}')
            rows.append({'season': season, 'round': r, 'date': cur_date,
                         'home': norm(home), 'hg': hg, 'ag': ag, 'away': norm(away),
                         'raw': raw, 'note': note})
    return rows

def parse_rsssf_table(path, season):
    lines = open(path, encoding='utf-8').read().splitlines()
    tbl = {}
    for l in lines:
        m = re.match(r'^\s*\d+\.(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)', l)
        if m:
            club = re.sub(r'\s*\(.*\)\s*$', '', m.group(1).strip())
            if club not in CANON:
                print(f'  !! table club not mapped: "{club}" ({season})')
                continue
            tbl[CANON[club]] = tuple(int(m.group(i)) for i in range(2, 9))
    return tbl

def parse_playoff(path, season):
    lines = open(path, encoding='utf-8').read().splitlines()
    out = []
    in_po = False
    for l in lines:
        t = l.strip()
        if t.startswith('Promotion/Relegation Playoff'):
            in_po = True
            continue
        if in_po:
            if t.startswith('Kupa') or t.startswith('Liga e'):
                break
            m = re.match(r'^(Semifinal|Final)( \[([A-Za-z]{3}) (\d{1,2})(, [^\]]+)?\])?', t)
            if m:
                out.append({'stage': m.group(1)})
                if m.group(3):
                    out[-1]['date_raw'] = (m.group(3), int(m.group(4)))
                    out[-1]['venue_raw'] = m.group(5)
                continue
            m = re.match(r'^([\w\.\' \&\-]+?)\s+(\d+)-(\d+)\s+([\w\.\' \&\-]+)\s*(.*)$', t)
            if m and out and 'home' not in out[-1]:
                out[-1]['home'] = norm(m.group(1).strip())
                out[-1]['hg'] = m.group(2)
                out[-1]['ag'] = m.group(3)
                out[-1]['away'] = norm(m.group(4).strip())
                out[-1]['note'] = m.group(5).strip()
    y0 = int(season[:4])
    rows = []
    for t in out:
        if 'home' not in t:
            continue
        mon, day = t['date_raw']
        year = y0 if mon in ('Aug','Sep','Oct','Nov','Dec') else y0 + 1
        t['date'] = f'{year}-{MONTHS[mon]:02d}-{day:02d}'
        rows.append(t)
    return rows

def parse_cup(path, season):
    lines = open(path, encoding='utf-8').read().splitlines()
    items = []          # ('stage',...) headers / ('date', mon, day) / tie dicts
    stage = None
    leg = None
    in_cup = False
    for l in lines:
        t = l.strip()
        if t.startswith('Kupa'):
            in_cup = True
            continue
        if not in_cup:
            continue
        if t.startswith('Liga e') or t.startswith('Promotion/Relegation Playoff'):
            break
        m = re.match(r'^\[([A-Za-z]{3}) (\d{1,2})\]', t)
        if m:
            items.append(('date', m.group(1), int(m.group(2))))
            continue
        m = re.match(r'^(Preliminary Round [0-9]+|Preliminary Round|Round 1|1/16 Finals|1/8 Finals|Quarterfinals|Semifinals|Final)( \[([A-Za-z]{3}) (\d{1,2})(, [^\]]+)?\])?', t)
        if m:
            stage = m.group(1).strip()
            leg = None
            if m.group(3):
                items.append(('date', m.group(3), int(m.group(4))))
            continue
        m = re.match(r'^(First Legs|Second Legs)( \[([A-Za-z]{3}) (\d{1,2})\])?', t)
        if m:
            leg = m.group(1)
            if m.group(3):
                items.append(('date', m.group(3), int(m.group(4))))
            continue
        m = re.match(r'^([\w\.\' \&\-]+?)\s+awd\s+([\w\.\' \&\-]+)\s*(.*)$', t)
        if m and stage:
            home, away, note = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            am = re.search(r'awarded\s+(\d+)-(\d+)', note)
            hg, ag = (am.group(1), am.group(2)) if am else ('3', '0')
            items.append({'stage': stage, 'leg': leg, 'home': norm(home), 'hg': hg, 'ag': ag,
                          'away': norm(away), 'note': f'awarded {hg}-{ag}; {note}', 'raw': t})
            continue
        m = re.match(r'^([\w\.\' \&\-]+?)\s+(\d+)-(\d+)\s+([\w\.\' \&\-]+)\s*(.*)$', t)
        if m and stage:
            home, hg, ag, away, note = (m.group(i).strip() for i in (1, 2, 3, 4, 5))
            items.append({'stage': stage, 'leg': leg, 'home': norm(home), 'hg': hg, 'ag': ag,
                          'away': norm(away), 'note': note, 'raw': t})
            continue
        m = re.match(r'^([\w\.\' \&\-]+?)\s+o/w\s+([\w\.\' \&\-]+)\s*$', t)
        if m and stage:
            home, away = m.group(1).strip(), m.group(2).strip()
            items.append({'stage': stage, 'leg': leg, 'home': norm(home), 'hg': '0', 'ag': '3',
                          'away': norm(away), 'note': 'walkover (o/w per RSSSF)', 'raw': t})
            continue
    y0 = int(season[:4])
    last_date = None
    out = []
    for it in items:
        if isinstance(it, tuple) and it[0] == 'date':
            mon, day = it[1], it[2]
            year = y0 if mon in ('Aug','Sep','Oct','Nov','Dec') else y0 + 1
            last_date = f'{year}-{MONTHS[mon]:02d}-{day:02d}'
            continue
        it['date'] = last_date
        out.append(it)
    return out

def table_check(rows, official, tag):
    st = {}
    for x in rows:
        for side in ('home','away'):
            st.setdefault(x[side], {'W':0,'D':0,'L':0,'GF':0,'GA':0,'Pts':0})
        h, a = st[x['home']], st[x['away']]
        hg, ag = int(x['hg']), int(x['ag'])
        h['GF'] += hg; h['GA'] += ag; a['GF'] += ag; a['GA'] += hg
        if hg > ag: h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif hg < ag: a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else: h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    ok = True
    for club, (P, W, D, L, GF, GA, Pts) in official.items():
        s = st.get(club)
        if s is None or (s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (W, D, L, GF, GA, Pts):
            print(f'  TABLE MISMATCH {tag} {club}: official {W}-{D}-{L} {GF}-{GA} {Pts} vs {s}')
            ok = False
    return ok

if __name__ == '__main__':
    seasons = [
        ('rsssf-2021-22.txt', '2021-22'),
        ('rsssf-2022-23.txt', '2022-23'),
        ('rsssf-2023-24.txt', '2023-24'),
        ('rsssf-2024-25.txt', '2024-25'),
    ]
    for fname, tag in seasons:
        path = f'{LEDGER}/{fname}'
        rows = parse_rsssf_league(path, tag)
        official = parse_rsssf_table(path, tag)
        playoff = parse_playoff(path, tag)
        cup = parse_cup(path, tag)
        n = len(rows)
        per_round = Counter(r['round'] for r in rows)
        bad = {r: c for r, c in per_round.items() if c != 5}
        dup = n - len({(r['date'], r['home'], r['away']) for r in rows})
        goals = sum(int(r['hg']) + int(r['ag']) for r in rows)
        print(f'--- {tag}: rows={n} rounds={len(per_round)} bad_rounds={bad or "none"} dupes={dup} '
              f'goals={goals} span={rows[0]["date"]}..{rows[-1]["date"]} '
              f'playoff={len(playoff)} cup_ties={len(cup)}')
        ok = table_check(rows, official, tag)
        print(f'  table reproduction: {"PASS" if ok else "FAIL"} ({len(official)} clubs)')
        mem = set()
        for r in rows:
            mem.add(r['home']); mem.add(r['away'])
        extra = mem - MEMBERSHIP[tag]
        print(f'  membership: {"PASS" if not extra else extra}')
        json.dump(rows, open(f'{LEDGER}/kos-{tag}-league.json', 'w'), indent=1)
        json.dump(playoff, open(f'{LEDGER}/kos-{tag}-playoff.json', 'w'), indent=1)
        json.dump(cup, open(f'{LEDGER}/kos-{tag}-cup.json', 'w'), indent=1)
