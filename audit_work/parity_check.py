import json
import os
import sys

BASELINE_PATH = "audit_work/ladder_baseline_2026-08-05_full.json"
STORE_PATH = "audit_work/pitch-rating-full-10199-new-leagues-2026-08-05.json"
LEAGUES = ("Russian Premier League","Czech First League","England Premier League","Italy Serie A","Germany Bundesliga","France Ligue 1")

def main():
    if not os.path.exists(BASELINE_PATH):
        print("Baseline not found.")
        return

    with open(BASELINE_PATH) as f:
        baseline_data = json.load(f)
    
    sys.path.insert(0, 'audit_work')
    from produce_baseline import run_league as run_league_probs
    
    current_probs = {}
    for lg in LEAGUES:
        current_probs[lg] = run_league_probs(lg)
        
    baseline_probs = baseline_data['baseline']
    
    total_matches = 0
    mismatches = 0
    max_delta = 0.0
    
    for lg in LEAGUES:
        b_lg = baseline_probs.get(lg, [])
        c_lg = current_probs.get(lg, [])
        
        if len(b_lg) != len(c_lg):
            print(f"!! {lg}: length mismatch. Baseline {len(b_lg)} Current {len(c_lg)}")
            mismatches += 1
            continue
            
        for b, c in zip(b_lg, c_lg):
            total_matches += 1
            if b['id'] != c['id']:
                print(f"!! ID mismatch: {b['id']} vs {c['id']}")
                mismatches += 1
                continue
            
            for pb, pc in zip(b['prob'], c['prob']):
                delta = abs(pb - pc)
                max_delta = max(max_delta, delta)
                if delta > 1e-6:
                    mismatches += 1
                    break
    
    print(f"\n=== Parity Check ===")
    print(f"Leagues: {len(LEAGUES)}")
    print(f"Total test matches checked: {total_matches}")
    print(f"Mismatches: {mismatches}")
    print(f"Max Delta: {max_delta:.8f}")
    
    if mismatches == 0 and max_delta < 1e-6:
        print("VERDICT: PASS — FULL PARITY (Δ0.0000)")
    else:
        print("VERDICT: FAIL — PARITY BROKEN")

if __name__ == "__main__":
    main()
