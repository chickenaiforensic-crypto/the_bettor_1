bs = chr(92)
line = open('build_b_edits.py', encoding='utf-8').read().split('\n')[954]
j = line.index('/^')
seg = line[j:j+16]
print('segment printable:', seg)
print('char codes:', [ord(c) for c in seg])
print('count dbl+d:', (bs*2+'d') in line)
print('count sgl+d:', (bs+'d') in line)
