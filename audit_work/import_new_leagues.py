import json
import os
import sys
from pack_parse import parse_pack

STORE_PATH = "previous_work_files/workspace-recent-019fd033-d0ce-7919-abd2-9978a1b06739/pitch-rating-full-5082-D1D2-2026-08-05.json"
OUTPUT_PATH = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"

def main():
    with open(STORE_PATH, "r") as f:
        data = json.load(f)
    
    store = data['store']
    existing_matches = store['matches']
    fps = set((m['dateISO'], m['homeName'], m['awayName'], m['competitionName']) for m in existing_matches)
    
    new_matches = []
    packs = [
        "handoffs/ITA-2021-2026_BP-TEAM-PACK_v2.txt",
        "handoffs/GER-2021-2026_BP-TEAM-PACK_v2.txt",
        "handoffs/FRA-2021-2026_BP-TEAM-PACK_v2.txt",
        "handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt"
    ]
    
    match_id_counter = 5083
    
    for pack_path in packs:
        p = parse_pack(pack_path)
        for m in p['matches']:
            fp = (m['dateISO'], m['homeName'], m['awayName'], m['competitionName'])
            if fp not in fps:
                # Mint a new match object suitable for the store
                new_m = {
                    "id": f"m:{match_id_counter}",
                    "dateISO": m['dateISO'],
                    "competitionName": m['competitionName'],
                    "compType": m['compType'],
                    "homeName": m['homeName'],
                    "homeGoals": m['homeGoals'],
                    "awayName": m['awayName'],
                    "awayGoals": m['awayGoals'],
                    "venueType": m['venueType'],
                    "stadium": m['stadium'],
                    "city": m['city'],
                    "country": m['country'],
                    "sourceId": m['sourceId'],
                    "muted": False
                }
                new_matches.append(new_m)
                fps.add(fp)
                match_id_counter += 1
                
    store['matches'].extend(new_matches)
    print(f"Added {len(new_matches)} new matches.")
    print(f"Total matches in store: {len(store['matches'])}")
    
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f)
    print(f"New store saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    sys.path.insert(0, 'audit_work')
    main()
