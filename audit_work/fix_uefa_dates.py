import re
import os

path = "handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt"
output = "handoffs/UEFA-CONNECTOR-2021-2026_BP-TEAM-PACK_v2.txt.fixed"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("MATCH|"):
        parts = line.split("|")
        # MATCH|date|comp|compType|home|hg|ag|away|round|stadium|city|country|tieId|source
        date = parts[1]
        tie_id = parts[12]
        
        # tie_id format e.g. UCL-2223-QF-CHE-REA
        m = re.search(r'-(2[123456])(2[234567])-?', tie_id)
        if m:
            s_yy = int(m.group(1)) # start year
            e_yy = int(m.group(2)) # end year
            
            month = int(date[5:7])
            # Determine correct year
            if month >= 7:
                correct_year = 2000 + s_yy
            else:
                correct_year = 2000 + e_yy
            
            new_date = f"{correct_year}{date[4:]}"
            parts[1] = new_date
            line = "|".join(parts)
            
    new_lines.append(line)

with open(output, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Fixed file saved to {output}")
