t = open('fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn',
         encoding='utf-8').read()
i = t.find('base_link')
seg = t[i-6:i]
codes = [ord(c) for c in seg]
lines = [
    'chars before base_link: ' + repr(seg),
    'ord codes: ' + str(codes),
    '92=backslash 34=quote',
]
open('/tmp/f9_ord.txt', 'w').write(chr(10).join(lines) + chr(10))
