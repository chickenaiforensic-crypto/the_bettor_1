#!/usr/bin/env python3
"""wiki_ita_venues.py — extract season venue tables from the wiki ITA raw archives
into `VENUE|season|team|city|stadium|cap|format` rows for audit/ledger/ita-venues.txt.

INPUT artifacts (data/raw/, all fetch-verified raws. SEE ITS OWN HEADERS FOR SCOPES):
  wiki-ita-2021-22-article-raw.txt   wikitext escaped (\| \[ ...) stadium table, 20 rows
  wiki-ita-2022-23-sections-raw.txt  RENDERED markdown stadium table, 20 rows
  wiki-ita-2023-24-sections-raw.txt  wikitext escaped stadium table, 20 rows
  wiki-ita-2024-25-sections-raw.txt  wikitext escaped stadium table, 20 rows (pending)
  wiki-ita-2025-26-article-raw.txt   wikitext escaped stadium table, 20 rows (pending)
Usage: python3 tools/wiki_ita_venues.py <raw> <season> <FMT:wt|md>
Gates inside: exactly 20 rows; print table; non-20 = loud exit(2).

2026-08-05 REWRITE of parse_wt: the first draft's composite raw-string regex
('^\\\\\\| ...') tokenised as an accidental top-level alternation; it happened to
match most cells but silently dropped the Sassuolo row (parenthetical stadium
variant) in 2021-22. Rewritten with a literal-prefix check + explicit escaped-
bracket pattern; gated clean on 2021-22/2022-23(md)/2023-24 the same day.
"""
import re, sys

# cell line, literal escaped form (backslashes are REAL chars in the file):
#   '\| \[\[X\]\]'  or  '\| \[\[Article\|Display\]\]'  optionally + ' (\[\[Y\]\])'
WT_OB = "\\[\\["   # the 4 real chars \ [ \ [
WT_CB = "\\]\\]"   # the 4 real chars \ ] \ ]
# capacity anywhere on the line (chunk joins can leave mid-word starts
# like 'yle="text-align...' from a '\| st'+'yle=' splice)
RE_WT_NTS = re.compile("{{Nts" + "\\\\\\|" + "([\\d,]+)}}")  # literal {{Nts\|<digits>}}


def wt_cell(rest):
    """parse one escaped link cell (rest = line after the '\| ' prefix).
    Returns the display text, or None if not exactly a link cell."""
    if not rest.startswith(WT_OB):
        return None
    j = rest.find(WT_CB, len(WT_OB))
    if j < 0:
        return None
    inner = rest[len(WT_OB):j]
    tail = rest[j + len(WT_CB):]
    if tail:
        # only a single trailing parenthetical link is legal: ' (\[\[Y\]\])'
        if not (tail.startswith(" (") and tail.endswith(")")
                and tail[2:-1].startswith(WT_OB) and tail[2:-1].endswith(WT_CB)):
            return None
    return inner.split("\\|")[-1]  # Article\|Display -> Display


def parse_wt(d):
    """wikitext-escaped stadium table: rows of 5 fields across consecutive lines.
    Cell lines start with the literal 3-char prefix backslash-pipe-space.
    2025-26 variant: shared cells via 'rowspan="2"' -
      '\| rowspan="2" \| \[\[Milan\]\]' (city/stadium) and
      '\| rowspan="2" style=... \| {{Nts\|...}}'   (capacity),
    then the partner row carries the team cell ONLY ('\| \[\[Inter Milan\]\]'
    immediately followed by '\|-'). Handled by remembering the last completed
    (city,stadium,cap) triple and emitting it for a dangling single team cell
    flushed at the '\|-'/'\|}' separator."""
    rows = []
    cur = []
    last_full = None  # (city, stadium, cap) of the most recent complete row

    def flush_dangling():
        nonlocal cur
        if len(cur) == 1 and last_full is not None:
            rows.append((cur[0], last_full[0], last_full[1], last_full[2]))
        cur = []

    for ln in d.split("\n"):
        s = ln.rstrip()
        if s in ("\\|-", "\\|}"):
            flush_dangling()
            continue
        cell = None
        if s.startswith('\\| rowspan="'):
            # strip up to the next real cell marker after the rowspan attribute
            k = s.find(" \\| ", 2)
            if k != -1:
                rest = s[k + 4:]
                if rest.startswith("\\[\\["):
                    cell = wt_cell(rest)
                else:
                    m2 = re.match(r'^style="[^"]*" ?\\\\?\\| ?', rest)
                    if m2:
                        rest2 = rest[m2.end():]
                        if rest2.startswith("\\[\\["):
                            cell = wt_cell(rest2)
        elif s.startswith("\\| "):
            cell = wt_cell(s[3:])
        if cell is not None:
            cur.append(cell)
            continue
        m = RE_WT_NTS.search(s)
        if m and len(cur) >= 3:
            team, city, stad = cur[-3], cur[-2], cur[-1]
            rows.append((team, city, stad, m.group(1)))
            last_full = (city, stad, m.group(1))
            cur = []
    flush_dangling()
    return rows


def parse_md(d):
    """rendered markdown rows: | [Team](url "X") | [City](url "Y") | [Stadium](url "Z") | cap |"""
    rows = []
    for ln in d.split("\n"):
        if not ln.startswith("| ["):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        def lab(c):
            m = re.match(r"^\[([^\]]+)\]\(", c)
            return m.group(1) if m else None
        t = lab(cells[0]); city = lab(cells[1]); stad = lab(cells[2])
        cap = cells[3]
        if t and city and stad and re.match(r"^[\d,]+$", cap):
            rows.append((t, city, stad, cap))
    return rows


def main():
    path, season, fmt = sys.argv[1], sys.argv[2], sys.argv[3]
    d = open(path, encoding="utf-8").read()
    rows = parse_wt(d) if fmt == "wt" else parse_md(d)
    print(f"# {path} season={season} fmt={fmt}: {len(rows)} venue rows")
    for t, city, stad, cap in rows:
        print(f"VENUE|{season}|{t}|{city}|{stad}|{cap}|{fmt}")
    if len(rows) != 20:
        print(f"# GATE FAIL: expected 20 rows, got {len(rows)}", file=sys.stderr)
        sys.exit(2)
    print("# GATE OK: 20/20 venue rows")


if __name__ == "__main__":
    main()
