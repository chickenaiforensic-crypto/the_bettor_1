#!/usr/bin/env python3
"""build_ita_venues_ledger.py — emit audit/ledger/ita-venues.txt from the gated
wiki venue extractors (tools/wiki_ita_venues.py) over the five season raws.

Deterministic: extractor output -> roster-string map -> ASCII fold -> VENUE rows
in season table order. Header text is hand-maintained (delta documentation).
Run: python3 tools/build_ita_venues_ledger.py > audit/ledger/ita-venues.txt
"""
import sys, unicodedata
sys.path.insert(0, "tools")
from wiki_ita_venues import parse_wt, parse_md

ROSTER = {  # wiki print -> pinned roster string (WO-ITA section 3)
    "Hellas Verona": "Verona",
    "AC Milan": "Milan",
    "Inter Milan": "Inter",
}
FOLD = str.maketrans({"–": "-", "à": "a", "è": "e", "é": "e", "ì": "i", "ò": "o", "ù": "u"})

SEASONS = [
    ("2021-22", "data/raw/wiki-ita-2021-22-article-raw.txt", "wt"),
    ("2022-23", "data/raw/wiki-ita-2022-23-sections-raw.txt", "md"),
    ("2023-24", "data/raw/wiki-ita-2023-24-sections-raw.txt", "wt"),
    ("2024-25", "data/raw/wiki-ita-2024-25-sections-raw.txt", "wt"),
    ("2025-26", "data/raw/wiki-ita-2025-26-article-raw.txt", "wt"),
]

# per (season, team-print) verbatim note overrides/extras (hand-curated, cites kept)
NOTES = {
    ("2021-22", "Sassuolo"): "print 'Mapei Stadium' + parenthetical '([[Reggio Emilia]])' on the stadium line; cap 21,525. Club home city listed Sassuolo.",
    ("2022-23", "Juventus"): "print 'Juventus Stadium' (link Juventus Stadium) 41,507",
    ("2022-23", "Atalanta"): "print 'Stadio Atleti Azzurri d'Italia' (historical name restored this season's table) 21,000",
    ("2023-24", "Inter Milan"): "print 'Giuseppe Meazza' 75,710 - SAME GROUND as Milan's 'San Siro' print this season (wiki prints the two tenants' own names; one physical stadium)",
    ("2023-24", "AC Milan"): "print 'San Siro' 75,710 (see Inter row: same ground)",
    ("2023-24", "Atalanta"): "print 'Gewiss Stadium' 15,222 (rebuild-phase reduced capacity)",
    ("2024-25", "Empoli"): "print 'Stadio Carlo Castellani - Computer Gross Arena' (sponsor suffix new in table) 16,167",
    ("2025-26", "Atalanta"): "print 'Stadio di Bergamo' 23,439 (official rename of the Gewiss/Atleti Azzurri ground; link Stadio Atleti Azzurri d'Italia)",
    ("2025-26", "Lecce"): "print 'Stadio Via del Mare-Ettore Giardiniero' (sponsor suffix) 30,354",
    ("2025-26", "Pisa"): "print 'Cetilar Arena' (sponsor name; link 'Arena Garibaldi - Stadio Romeo Anconetani') 12,508",
    ("2025-26", "Udinese"): "print 'Bluenergy Stadium' (sponsor name; link Stadio Friuli) 25,132",
    ("2025-26", "Juventus"): "print 'Allianz Stadium' 41,507 (link Juventus Stadium)",
    ("2025-26", "AC Milan"): "rowspan-shared cells with Inter this season (wiki rowspan=2 block); San Siro 75,710 both",
    ("2025-26", "Inter Milan"): "rowspan-shared; see Milan note",
    ("2025-26", "Lazio"): "rowspan-shared cells with Roma; Olimpico 70,634 both",
    ("2025-26", "Roma"): "rowspan-shared; see Lazio note",
}

HDR = """# ITA VENUES 2021-22..2025-26 (WO-ITA-SPAN-14) - transcribed 2026-08-05 from the Wikipedia
# season articles' \"Stadiums and locations\" tables (fetched 2026-08-05 via fetch_page;
# action=raw wikitext for 2021-22/2023-24/2024-25/2025-26, rendered markdown for 2022-23
# whose wikitext capture was thrown away in the controller-abort - its venue layer was
# re-verified against the rendered table 20/20 plus capacities; matrices never come from
# rendered pages). Independent of RSSSF fixtures = venue second index.
# VENUE|<season>|<roster-string>|<stadium-canonical (as printed per season, ASCII-folded)>|<city>|<cap as printed, commas folded>|<verbatim wiki notes>
# Roster map: Hellas Verona->Verona, AC Milan->Milan, Inter Milan->Inter (pinned section-3
# strings; Inter never Internazionale, Milan never AC Milan, Verona never Hellas).
# Epochs are era data (FRA sponsor-epoch decree analogue): Juventus 'Allianz Stadium'
# 2021-22 -> 'Juventus Stadium' 2022-23..2024-25 -> 'Allianz Stadium' 2025-26; Atalanta
# 'Gewiss Stadium' 19,768 (2021-22) -> 'Stadio Atleti Azzurri d'Italia' 21,000 (2022-23)
# -> 'Gewiss Stadium' 15,222 rebuild-reduced (2023-24) -> 23,439 (2024-25) -> renamed
# 'Stadio di Bergamo' 23,439 (2025-26). Capacity prints shift by season and are carried
# VERBATIM per season table (wiki re-count waves incl. 2023-24 San Siro/Meazza 75,923->
# 75,710, Olimpico 70,634->67,585, Ferraris 36,599->33,205, OGT 28,958->28,177; 2025-26
# Olimpico print swings BACK to 70,634 - source reprints, not structural changes).
# 2023-24 SAME-GROUND SPLIT PRINT: Inter 'Giuseppe Meazza' vs Milan 'San Siro' (one
# stadium, both 75,710). 2025-26 rowspan=2 shared cells Milan/Inter + Lazio/Roma.
# Sassuolo home ground is in Reggio Emilia (Mapei Stadium - Citta del Tricolore) while the
# club city prints Sassuolo all five window seasons (2026-27 boundary article prints
# 'Reggio Emilia' - post-window, NOTE-only).
# ASCII folds in canonical fields: Mapei Stadium - Citta del Tricolore (<- Città/en-dash).
"""


def main():
    print(HDR.rstrip())
    for season, path, fmt in SEASONS:
        d = open(path, encoding="utf-8").read()
        rows = parse_wt(d) if fmt == "wt" else parse_md(d)
        assert len(rows) == 20, (season, len(rows))
        for team, city, stad, cap in rows:
            stock = ROSTER.get(team, team)
            assert stock in ("Atalanta Bologna Cagliari Como Cremonese Empoli Fiorentina Frosinone Genoa Inter Juventus Lazio Lecce Milan Monza Napoli Parma Pisa Roma Salernitana Sampdoria Sassuolo Spezia Torino Udinese Venezia Verona").split(), stock
            capd = cap.replace(",", "")
            note = NOTES.get((season, team), f"print '{stad}' {cap}")
            print(f"VENUE|{season}|{stock}|{stad.translate(FOLD)}|{city.translate(FOLD)}|{capd}|{note}")
        if season == "2022-23":
            print("VENUE|2022-23|PLAYOFF-NEUTRAL|Mapei Stadium - Citta del Tricolore|Reggio Emilia|21515|"
                  "Relegation tie-breaker 'spareggio' 2023-06-11 Spezia 1-3 Verona at NEUTRAL Reggio Emilia "
                  "(wiki box: Mapei Stadium - Citta del Tricolore, attendance 15,000, ref Daniele Orsato, "
                  "20:45 CEST; report legaseriea.it/en/match/2022-23aspareuni1spever). Cap carried from the "
                  "2022-23 season table print.")


if __name__ == "__main__":
    main()
