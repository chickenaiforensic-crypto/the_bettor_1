"""Remove the two Candidate A rep blocks from build_b_edits.py (measured rejection:
replay_variants.js + replay_ab_check.js — no gain on any audit motive, pocket worse).
C4 context-flag reps are untouched. Rebuild reverts the engine to v2.6.9 evidence math."""
s = open('build_b_edits.py', encoding='utf-8').read()

start1 = s.index('# --- v2.7.0: Candidate A')
end1 = s.index('tag="Candidate A venue-corrected H2H + saturation")') + len('tag="Candidate A venue-corrected H2H + saturation")\n')
s = s[:start1] + s[end1:]

tag2 = 'tag="summation note: Candidate A disclosure")'
end2 = s.index(tag2) + len(tag2) + 1
start2 = s.rfind('rep(', 0, end2)
assert start2 != -1 and start2 > s.index('zone line ctx marker')
s = s[:start2] + s[end2:]

assert 'Candidate A' not in s
open('build_b_edits.py', 'w', encoding='utf-8').write(s)
print('reverted: Candidate A reps removed')
