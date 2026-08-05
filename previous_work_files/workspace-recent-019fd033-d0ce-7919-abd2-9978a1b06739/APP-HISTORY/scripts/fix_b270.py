bs = chr(92)  # backslash, built without embedding a literal (JSON layer eats them)
lines = open('build_b_edits.py', encoding='utf-8').read().split('\n')
target = bs*2 + 'd'      # double-backslash-d  (wrong, matches literal \d in JS regex)
good   = bs + 'd'        # single-backslash-d  (correct regex digit class)
for i in (954, 968):
    assert target in lines[i], (i+1, lines[i])
    lines[i] = lines[i].replace(target, good)
    assert target not in lines[i]
print('955 now:', lines[954].strip()[:70])
print('969 now:', lines[968].strip()[:70])
open('build_b_edits.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('written')
