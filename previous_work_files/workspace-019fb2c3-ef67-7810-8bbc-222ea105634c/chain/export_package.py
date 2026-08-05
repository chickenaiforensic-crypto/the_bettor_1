"""
EXPORT PACKAGE — converts internal artefacts into the requested schema.
Every field the spec asks for is emitted; fields we do not hold are written
as NULL rather than invented.
"""
import pickle, csv, json, os
import chain as C

OUT = "/home/user/export"
os.makedirs(OUT, exist_ok=True)

COMP_MAP = {
    'CL': 'EUR_CL', 'CLQ': 'EUR_CL', 'EL': 'EUR_EL', 'ELQ': 'EUR_EL',
    'CONF': 'EUR_CONF', 'CONFQ': 'EUR_CONF',
}

edges = pickle.load(open("/home/user/chain/edges.pkl", "rb"))

# ---------- 1. MATCH GRAPH in requested schema ----------
with open(f"{OUT}/01_matches.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "home_team", "away_team", "home_goals", "away_goals",
                "competition", "league_or_country", "context_type",
                "date_precision", "round", "venue", "neutral_flag",
                "extra_time", "penalties"])
    for dt, comp, ch, h, ca, a, hg, ag in edges:
        kind, code = comp.split(":")
        if kind == "DOM":
            ctx, lg, prec = "DOMESTIC", ch, "EXACT"
        else:
            ctx, lg, prec = COMP_MAP.get(code, "EUR_OTHER"), f"{ch}v{ca}", "SEASON_ONLY"
        w.writerow([dt, h, a, hg, ag, comp, lg, ctx, prec,
                    "", "", "", "", ""])
print(f"01_matches.csv           {len(edges):,} rows")

# ---------- 2. CROSS-BORDER FILE ----------
eur = [e for e in edges if e[1].startswith("EUR")]
with open(f"{OUT}/02_cross_border.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "season", "competition", "round", "home_team", "away_team",
                "home_country", "away_country", "home_goals", "away_goals",
                "venue", "neutral_or_relocated_flag", "date_precision"])
    for dt, comp, ch, h, ca, a, hg, ag in eur:
        code = comp.split(":")[1]
        w.writerow([dt, dt[:4], COMP_MAP.get(code, code), "", h, a, ch, ca,
                    hg, ag, "", "", "SEASON_ONLY"])
print(f"02_cross_border.csv      {len(eur):,} rows")

# ---------- 3. DOMESTIC FOR THE TWO CLUBS ----------
A, B = C.resolve("Maccabi Tel Aviv"), C.resolve("Sheriff Tiraspol")
rows = []
for dt, comp, ch, h, ca, a, hg, ag in edges:
    H, Aw = C.CANON[C.norm(h)], C.CANON[C.norm(a)]
    if A in (H, Aw) or B in (H, Aw):
        rows.append([dt, comp, h, a, hg, ag, dt[:4],
                     "DOMESTIC" if comp.startswith("DOM") else "EUROPEAN"])
rows.sort()
with open(f"{OUT}/03_two_clubs_all_matches.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "competition", "home_team", "away_team",
                "home_goals", "away_goals", "season", "context_type"])
    w.writerows(rows)
print(f"03_two_clubs_all_matches.csv  {len(rows):,} rows")

# ---------- 4. CALIBRATION OUTPUTS ----------
seg = pickle.load(open("/home/user/chain/segment_rows.pkl", "rb"))
with open(f"{OUT}/04a_segmentation_rows.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["seg", "est", "n", "phase", "res", "gd", "eur_frac"])
    w.writeheader()
    w.writerows(seg)
print(f"04a_segmentation_rows.csv     {len(seg):,} rows")

cal = pickle.load(open("/home/user/chain/chain_calib.pkl", "rb"))
with open(f"{OUT}/04b_chain_calibration.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cal[0].keys()))
    w.writeheader()
    w.writerows(cal)
print(f"04b_chain_calibration.csv     {len(cal):,} rows")

wt = pickle.load(open("/home/user/chain/weighted_test.pkl", "rb"))
with open(f"{OUT}/04c_weighted_scale_test.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["est_plain_gd", "est_user_weighted", "result", "actual_gd", "n_paths"])
    w.writerows(wt)
print(f"04c_weighted_scale_test.csv   {len(wt):,} rows")

fx = pickle.load(open("/home/user/chain/fix30_merged.pkl", "rb"))
clean = []
for d in fx:
    clean.append({k: (v if not isinstance(v, dict) else v.get("name"))
                  for k, v in d.items() if k not in ("g", "top")})
json.dump(clean, open(f"{OUT}/04d_fixture_outputs.json", "w"), indent=1, default=str)
print(f"04d_fixture_outputs.json      {len(clean)} fixtures")

ls, ctry = pickle.load(open("/home/user/chain/league_strength.pkl", "rb"))
with open(f"{OUT}/04e_league_strength.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["country", "euro_gd_per_match"])
    for k, v in sorted(ls.items(), key=lambda x: -x[1]):
        w.writerow([k, round(v, 4)])
print(f"04e_league_strength.csv       {len(ls)} countries")

# ---------- 5. IDENTITY MAP ----------
with open(f"{OUT}/05_identity_map.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["normalised_key", "canonical_name"])
    for k, v in sorted(C.CANON.items()):
        w.writerow([k, v])
with open(f"{OUT}/05_aliases.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["alias_key", "maps_to"])
    for k, v in sorted(C.ALIASES.items()):
        w.writerow([k, v])
print(f"05_identity_map.csv           {len(C.CANON):,} identities")
print(f"05_aliases.csv                {len(C.ALIASES)} manual aliases")
