import re

t = open('fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn',
          encoding='utf-8').read()
out = []
for m in re.finditer(r":inertia\s*\{([^}]*)\}", t):
    head = t[:m.start()]
    names = re.findall(r":name\s*.{0,3}([A-Za-z0-9_]+).{0,3}", head)
    out.append((names[-1] if names else None, m.group(1)[:140]))

lines = []
for n, b in out:
    lines.append(f"{n} -> {b}")
lines.append("---- raw context around each :inertia ----")
for i, m in enumerate(re.finditer(r":inertia\s*\{", t)):
    start = max(0, m.start() - 160)
    lines.append(f"[block {i}] ...{t[start:m.end()]}")

open('/tmp/f9_edn_map.txt', 'w').write("\n".join(lines) + "\n")
print("wrote /tmp/f9_edn_map.txt")
