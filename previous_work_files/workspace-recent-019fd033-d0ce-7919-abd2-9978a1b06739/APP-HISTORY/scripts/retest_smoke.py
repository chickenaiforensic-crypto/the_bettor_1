lines = open('smoke_test.js', encoding='utf-8').read().split('\n')
i_ctx = next(i for i, l in enumerate(lines) if l.startswith('const ctxRes'))
assert i_ctx == 273, i_ctx  # 0-based index of grep line 274
lines[i_ctx] = 'const ctxRes = evX("(function(){var ha=BlueprintEmbed.resolve(\'Ctx Alpha\',\'Qland\'),hb=BlueprintEmbed.resolve(\'Ctx Beta\',\'Qland\');var ev=BlueprintEmbed.analyze(ha,hb,\'2026-06-22\');var z0=computeZone(ev.paths,ev.ag);var z1=computeZoneCtx(ev.paths,ev.ag,ha,hb,\'2026-06-22\');var h2h=ev.paths.filter(function(p){return p.phase===\'h2h\';});return {key0:z0.key,key1:z1.key,ctxFrom:z1.ctxFrom||null,hits:z1.ctx&&z1.ctx[0]&&z1.ctx[0].hitsLeader,w:h2h.map(function(p){return p.weight;}),e:h2h.map(function(p){return p.estimate;})};})()");'
lines[i_ctx + 1] = 'chk("h2h weights stay linear w3 (Candidate A rejected on replay)", ctxRes.w.length === 3 && ctxRes.w.every(w => Math.abs(w - 3) < 1e-9), JSON.stringify(ctxRes.w));'
lines[i_ctx + 2] = 'chk("h2h estimates uncorrected (Candidate A rejected on replay)", ctxRes.e.join(",") === "3,4,5", JSON.stringify(ctxRes.e));'
assert 'away meetings venue-corrected' in lines[i_ctx + 3]
del lines[i_ctx + 3]
j = next(i for i, l in enumerate(lines) if 'C4 context flags + Candidate A' in l)
lines[j] = '/* --- v2.7.0: C4 context flags (demote-only) — Candidate A rejected on replay, engine math unchanged from v2.6.9 --- */'
open('smoke_test.js', 'w', encoding='utf-8').write('\n'.join(lines))
print('smoke re-pinned to kept engine')
