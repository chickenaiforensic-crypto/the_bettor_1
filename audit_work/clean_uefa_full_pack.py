#!/usr/bin/env python3
"""Clean UEFA-FULL pack: strip the 436 fabricated ClubA/ClubB MATCH rows.
Keeps all real UEFA rows (2,764) + header NOTE/SOURCE/TEAM rows + END.
Preserves 14-field grammar. Adds a cleanup NOTE. Auditor verifies from fresh parse.
"""
import re, sys

SRC = "handoffs/UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt"
DST = "handoffs/UEFA-FULL-2021-2026_BP-TEAM-PACK_v2.txt"  # replace in place (per relay)

def is_fake(line):
    if not line.startswith("MATCH"):
        return False
    f = line.split("|")
    # fake rows: homeName/awayName == ClubA<num>/ClubB<num>
    home, away = f[4], f[7]
    return bool(re.match(r"^Club[A-Z]\d+$", home) and re.match(r"^Club[A-Z]\d+$", away))

def main():
    lines = open(SRC, encoding="utf-8").read().splitlines()
    out = []
    fake_count = 0
    real_count = 0
    inserted_note = False
    for ln in lines:
        if is_fake(ln):
            fake_count += 1
            continue
        if ln.startswith("MATCH"):
            real_count += 1
        if not inserted_note and (ln.startswith("END") or ln.strip()==""):
            # insert cleanup note just before END
            out.append("NOTE|info|cleanup_2026-08-06|436 fabricated rows (ClubA1-ClubA436, synthetic 1-0, Stadium/City/Europe, empty sourceId) removed from this pack by researcher on 2026-08-06. This pack now contains only real UEFA rows (%d). See Supervior/updates/FINDING-UCL-FABRICATED-ROWS-2026-08-06.md." % real_count)
            inserted_note = True
        out.append(ln)
    if not inserted_note:
        out.append("NOTE|info|cleanup_2026-08-06|436 fabricated rows removed. Real UEFA rows: %d." % real_count)
    content = "\n".join(out) + "\n"
    open(DST, "w", encoding="utf-8").write(content)
    print("fake removed:", fake_count)
    print("real kept:", real_count)
    print("total MATCH lines now:", sum(1 for x in out if x.startswith("MATCH")))
    return fake_count, real_count

if __name__ == "__main__":
    main()
