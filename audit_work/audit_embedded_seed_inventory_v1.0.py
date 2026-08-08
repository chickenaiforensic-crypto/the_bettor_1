#!/usr/bin/env python3
"""Inventory runtime-embedded BP seed packs in a Pitch Rating HTML app.

This tool does not approve data. It reports embedded runtime data so the
Director control register can quarantine anything without a separate audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def decode_js_string(raw: str) -> str:
    """Decode the double-quoted JavaScript string body used by SEED_PACKS."""
    return json.loads('"' + raw + '"')


def extract_seed_packs(app_text: str) -> list[tuple[str, str]]:
    marker = "var SEED_PACKS = ["
    start = app_text.find(marker)
    if start < 0:
        raise ValueError("SEED_PACKS declaration not found")
    end = app_text.find("];", start)
    if end < 0:
        raise ValueError("SEED_PACKS terminator not found")
    block = app_text[start : end + 2]
    pattern = re.compile(r'\{name:\"([^\"]+)\",text:\"((?:\\.|[^\"])*)"\}', re.S)
    packs = []
    for match in pattern.finditer(block):
        packs.append((match.group(1), decode_js_string(match.group(2))))
    if not packs:
        raise ValueError("No decodable SEED_PACKS entries found")
    return packs


def parse_pack(name: str, text: str) -> dict:
    lines = text.splitlines()
    header = next((line for line in lines if line.startswith("BP-TEAM-PACK")), "")
    v1 = header.endswith("v1")
    prefixes = Counter()
    teams = Counter()
    match_countries = Counter()
    competitions = Counter()
    for line in lines:
        if not line or line.startswith("#"):
            continue
        fields = line.split("|")
        kind = fields[0]
        prefixes[kind] += 1
        if kind == "TEAM" and len(fields) >= 3:
            teams[fields[2] or "<blank>"] += 1
        elif kind == "MATCH":
            # v2 has compType and therefore country is field 11.
            # v1 has no compType and therefore country is field 10.
            country_index = 10 if v1 else 11
            competition_index = 2
            if len(fields) > country_index:
                match_countries[fields[country_index] or "<blank>"] += 1
            if len(fields) > competition_index:
                competitions[fields[competition_index] or "<blank>"] += 1
    return {
        "file_name": name,
        "header": header,
        "decoded_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "line_prefix_counts": dict(sorted(prefixes.items())),
        "team_country_counts": dict(sorted(teams.items())),
        "match_country_counts": dict(sorted(match_countries.items())),
        "competition_counts": dict(sorted(competitions.items())),
        "classification": "UNAPPROVED_EMBEDDED_SEED",
        "rule": "Presence in runtime code is not auditor approval or permission to ingest.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", default="builder/app-v3.17.0-picker.html")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    app = Path(args.app)
    app_bytes = app.read_bytes()
    app_text = app_bytes.decode("utf-8")
    records = [parse_pack(name, text) for name, text in extract_seed_packs(app_text)]
    report = {
        "tool": "audit_embedded_seed_inventory_v1.0",
        "app_path": str(app),
        "app_md5": hashlib.md5(app_bytes).hexdigest(),
        "app_sha256": hashlib.sha256(app_bytes).hexdigest(),
        "seed_pack_count": len(records),
        "status": "QUARANTINE_REQUIRED",
        "packs": records,
    }
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"seed_pack_count": len(records), "status": report["status"]}, indent=2))


if __name__ == "__main__":
    main()
