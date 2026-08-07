#!/usr/bin/env python3
# SPA researcher parser: RSSSF Spain Primera Division round-by-round -> ledgers
# Primary source files: span2022..span2025 (local copies from previous session refs)
# Outputs per-season ledger txt + recomputed standings + parsed row list (json)
import re, json, sys, os

MONTHS = {m: i for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

# RSSSF stock name -> workorder section-3 roster string (verbatim)
NAME_MAP = {
    'Madrid': 'Real Madrid',
    'Barcelona': 'Barcelona',
    'Atlético': 'Ath Madrid',
    'Sevilla': 'Sevilla',
    'Betis': 'Betis',
    'Sociedad': 'Sociedad',
    'Villarreal': 'Villarreal',
    'Athletic': 'Ath Bilbao',
    'Valencia': 'Valencia',
    'Osasuna': 'Osasuna',
    'Celta': 'Celta',
    'Rayo Vallecano': 'Vallecano',
    'Elche': 'Elche',
    'Espanyol': 'Espanol',
    'Getafe': 'Getafe',
    'Mallorca': 'Mallorca',
    'Cádiz': 'Cadiz',
    'Granada': 'Granada',
    'Levante': 'Levante',
    'Alavés': 'Alaves',
    'Almería': 'Almeria',
    'Girona': 'Girona',
    'Valladolid': 'Valladolid',
    'Las Palmas': 'Las Palmas',
    'Leganés': 'Leganes',
}

ROSTER = set(NAME_MAP.values())

# Exact official-table club string -> roster string (RSSSF final-table names)
OFFICIAL_MAP = {
    'Real Madrid CF': 'Real Madrid',
    'FC Barcelona': 'Barcelona',
    'Atlético de Madrid': 'Ath Madrid',
    'Sevilla FC': 'Sevilla',
    'Real Betis Balompié (Sevilla)': 'Betis',
    'Real Sociedad (San Sebastián)': 'Sociedad',
    'Villarreal CF': 'Villarreal',
    'Athletic de Bilbao': 'Ath Bilbao',
    'Valencia CF': 'Valencia',
    'CA Osasuna (Pamplona)': 'Osasuna',
    'RC Celta (Vigo)': 'Celta',
    'Rayo Vallecano': 'Vallecano',
    'Elche CF': 'Elche',
    'RCD Espanyol (Barcelona)': 'Espanol',
    'Getafe CF': 'Getafe',
    'RCD Mallorca (Palma de M.)': 'Mallorca',
    'Cádiz CF': 'Cadiz',
    'Granada CF': 'Granada',
    'Levante UD (Valencia)': 'Levante',
    'Deportivo Alavés (Vitoria)': 'Alaves',
    'UD Almería': 'Almeria',
    'Girona FC': 'Girona',
    'Real Valladolid': 'Valladolid',
    'UD Las Palmas': 'Las Palmas',
    'CD Leganés': 'Leganes',
}


def prim_section(lines):
    start = next(i for i, l in enumerate(lines) if 'name="laliga"' in l)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if 'name="segunda"' in lines[i] or 'name="1rfef"' in lines[i]:
            end = i
            break
    return lines[start:end]


def parse_season(path, season_start_year):
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    sec = prim_section(lines)
    rounds = {}
    cur = None
    for l in sec:
        m = re.match(r'^Round (\d+)( \[([A-Za-z]{3}) (\d{1,2})\])?', l)
        if m:
            cur = int(m.group(1))
            rounds.setdefault(cur, [])
            if m.group(3):
                rounds[cur].append({'date': (m.group(3), int(m.group(4)))})
            continue
        if cur is None:
            continue
        m = re.match(r'^\[([A-Za-z]{3}) (\d{1,2})\]', l.strip())
        if m:
            rounds[cur].append({'date': (m.group(1), int(m.group(2)))})
            continue
        # match line: skip table rows (start with position digit+dot)
        if re.match(r'^\s*\d+\.', l):
            continue
        # skip abandoned-match annotation lines ("Granada abd Athletic ...")
        if re.search(r'\s+abd\s+', l, re.IGNORECASE):
            continue
        m = re.match(r'^\s*(.+?)\s+(\d{1,2})-(\d{1,2})\s+(.+?)\s*$', l)
        if m:
            home, hg, ag, away = m.group(1).strip(), int(m.group(2)), int(m.group(3)), m.group(4).strip()
            # strip trailing annotations (bracket notes or wrapped text after 2+ spaces)
            home = re.split(r'\s{2,}', home)[0]
            away = re.split(r'\s{2,}', away)[0]
            home = re.sub(r'\s*\[.*$', '', home).strip()
            away = re.sub(r'\s*\[.*$', '', away).strip()
            if home not in NAME_MAP or away not in NAME_MAP:
                raise SystemExit(f'UNMAPPED TEAM in {path}: "{home}" vs "{away}"')
            rounds[cur].append({
                'home': NAME_MAP[home], 'hg': hg, 'ag': ag,
                'away': NAME_MAP[away], 'raw': l.strip()})

    # resolve dates to ISO
    rows = []
    for r in sorted(rounds):
        block = rounds[r]
        cur_date = None
        for e in block:
            if 'date' in e:
                mon, day = e['date']
                year = season_start_year if mon in ('Aug', 'Sep', 'Oct', 'Nov', 'Dec') else season_start_year + 1
                cur_date = f'{year}-{MONTHS[mon]:02d}-{day:02d}'
                continue
            if cur_date is None:
                raise SystemExit(f'no date for match in round {r}')
            rows.append({
                'season': f'{season_start_year}-{str(season_start_year+1)[2:]}',
                'round': r, 'date': cur_date,
                'home': e['home'], 'hg': e['hg'], 'ag': e['ag'], 'away': e['away']})
    return rows


def standings(rows):
    st = {}
    for x in rows:
        for side in ('home', 'away'):
            st.setdefault(x[side], {'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'Pts': 0})
        h, a = st[x['home']], st[x['away']]
        h['P'] += 1; a['P'] += 1
        h['GF'] += x['hg']; h['GA'] += x['ag']
        a['GF'] += x['ag']; a['GA'] += x['hg']
        if x['hg'] > x['ag']:
            h['W'] += 1; a['L'] += 1; h['Pts'] += 3
        elif x['hg'] < x['ag']:
            a['W'] += 1; h['L'] += 1; a['Pts'] += 3
        else:
            h['D'] += 1; a['D'] += 1; h['Pts'] += 1; a['Pts'] += 1
    return st


def official_table(path):
    """Extract the RSSSF printed final table (club, P, W, D, L, GF-GA, Pts)."""
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    sec = prim_section(lines)
    tbl = []
    in_tbl = False
    for l in sec:
        if 'Final Table' in l:
            in_tbl = True
            continue
        if in_tbl:
            m = re.match(r'^\s*\d+\.(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)', l)
            if m:
                tbl.append((m.group(1).strip(), int(m.group(2)), int(m.group(3)),
                            int(m.group(4)), int(m.group(5)), int(m.group(6)),
                            int(m.group(7)), int(m.group(8))))
                continue
            if l.strip() and not l.strip().startswith('-'):
                if l.strip().startswith('Round'):
                    break
                # annotations etc - keep scanning until Round 1
            if l.strip().startswith('Round'):
                break
    return tbl


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else '.'
    outdir = sys.argv[2] if len(sys.argv) > 2 else '.'
    seasons = [(f'{src}/span2022.txt', 2021), (f'{src}/span2023.txt', 2022),
               (f'{src}/span2024.txt', 2023), (f'{src}/span2025.txt', 2024)]
    for path, sy in seasons:
        rows = parse_season(path, sy)
        tag = f'{sy}-{str(sy+1)[2:]}'
        # gates
        n = len(rows)
        rounds = sorted({r['round'] for r in rows})
        per_round = {r: sum(1 for x in rows if x['round'] == r) for r in rounds}
        bad_rounds = {r: c for r, c in per_round.items() if c != 10}
        dup = len(rows) - len({(x['date'], x['home'], x['away']) for x in rows})
        print(f'--- {tag}: rows={n} rounds={len(rounds)} dupes={dup} '
              f'bad_rounds={bad_rounds if bad_rounds else "none"} '
              f'goals={sum(x["hg"]+x["ag"] for x in rows)} span={rows[0]["date"]}..{rows[-1]["date"]}')
        # ledger output
        with open(f'{outdir}/spa-{tag}-ledger.txt', 'w', encoding='utf-8') as f:
            f.write(f'# SPA {tag} ledger — parsed from RSSSF {path}\n')
            for x in rows:
                f.write(f'MD{x["round"]:>2} {x["date"]} {x["home"]} {x["hg"]}-{x["ag"]} {x["away"]}\n')
        json.dump(rows, open(f'{outdir}/spa-{tag}-rows.json', 'w'), indent=1)
        # official table vs recompute
        ot = official_table(path)
        st = standings(rows)
        # normalize official club names to roster (exact match)
        def norm(name):
            return OFFICIAL_MAP.get(name)
        ok = True
        for i, (club, P, W, D, L, GF, GA, Pts) in enumerate(ot, 1):
            c = norm(club)
            s = st.get(c)
            if s is None:
                print(f'  TABLE MISMATCH {tag} pos{i}: {c} not in recompute')
                ok = False
                continue
            if (s['P'], s['W'], s['D'], s['L'], s['GF'], s['GA'], s['Pts']) != (P, W, D, L, GF, GA, Pts):
                print(f'  TABLE MISMATCH {tag} pos{i} {c}: official {P}/{W}/{D}/{L}/{GF}-{GA}/{Pts} vs recompute '
                      f'{s["P"]}/{s["W"]}/{s["D"]}/{s["L"]}/{s["GF"]}-{s["GA"]}/{s["Pts"]}')
                ok = False
        print(f'  table_reproduction: {"PASS" if ok else "FAIL"} (clubs {len(ot)})')
