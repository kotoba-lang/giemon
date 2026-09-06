t = open('fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn',
         encoding='utf-8').read()
i = t.find('base_link')
seg = t[i-40:i+20]
lines = [repr(seg), '---', repr(t[i-10:i+10])]
import re
lines.append('name-pat hits: %d' % len(re.findall(r':name', t)))
lines.append('bs-quote count: %d' % t.count(chr(92) + chr(34)))
lines.append(repr(t[i-2:i+2]))
open('/tmp/f9_bytes.txt', 'w').write(chr(10).join(lines) + chr(10))
