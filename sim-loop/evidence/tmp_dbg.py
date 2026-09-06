import re
t = open('fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn',
         encoding='utf-8').read()
BS = chr(92)
Q = chr(34)
out = []
try:
    pat = re.compile(':name\\s*\\' + BS + Q + '([A-Za-z0-9_]+)\\' + BS + Q)
    ms = pat.findall(t)
    out.append('v5: %d %s' % (len(ms), ms[:8]))
except Exception as e:
    out.append('v5 ERR: %r' % e)
try:
    pat6 = re.compile(':name\\s*\\\\?[A-Za-z0-9_\\\\"]')
    out.append('v6 hits: %d' % len(pat6.findall(t)))
except Exception as e:
    out.append('v6 ERR: %r' % e)
open('/tmp/f9_dbg3.txt', 'w').write(chr(10).join(out) + chr(10))
