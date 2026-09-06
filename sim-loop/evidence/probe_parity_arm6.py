#!/usr/bin/env python3
"""Falsification probe: URDF <-> EDN parity for fixtures/giemon_arm6.
Measurement only — compares every numeric field the URDF exposes
(joint origin/axis/damping/limits, child-link inertial) against the
:arm/chain blob in the EDN fixture. Exit 1 on any mismatch."""
import re, sys

d = "/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon/fixtures/giemon_arm6"
urdf = open(f"{d}/giemon_arm6.urdf").read()
edn = open(f"{d}/giemon_arm6.edn").read()

# --- parse URDF ---
joints = {}
for m in re.finditer(r'<joint name="(j\d)" type="revolute">(.*?)</joint>', urdf, re.S):
    name, body = m.group(1), m.group(2)
    xyz = re.search(r'<origin xyz="([^"]+)" rpy="([^"]+)"', body).groups()
    axis = re.search(r'<axis xyz="([^"]+)"', body).group(1)
    lim = re.search(r'lower="([^"]+)" upper="([^"]+)" effort="([^"]+)" velocity="([^"]+)"', body).groups()
    damp = re.search(r'damping="([^"]+)"', body).group(1)
    joints[name] = dict(origin=xyz[0].split(), axis=axis.split(),
                        lower=float(lim[0]), upper=float(lim[1]),
                        effort=float(lim[2]), velocity=float(lim[3]),
                        damping=float(damp))
links = {}
for m in re.finditer(r'<link name="(link\d)">\s*<inertial>\s*<origin xyz="([^"]+)"[^/]*/>\s*<mass value="([^"]+)"/>\s*<inertia ([^/]*)/>', urdf):
    name, org, mass, inert = m.groups()
    links[name] = dict(origin=org.split(), mass=float(mass),
                       inertia={k: float(v) for k, v in
                                re.findall(r'(ixx|iyy|izz|ixy|ixz|iyz)="([^"]+)"', inert)})
base = re.search(r'<link name="base_link">\s*<inertial>\s*<origin xyz="([^"]+)"[^/]*/>\s*<mass value="([^"]+)"/>\s*<inertia ([^/]*)/>', urdf)
links["base_link"] = dict(origin=base.group(1).split(), mass=float(base.group(2)),
                          inertia={k: float(v) for k, v in
                                   re.findall(r'(ixx|iyy|izz|ixy|ixz|iyz)="([^"]+)"', base.group(3))})

# --- unescape the EDN :arm/chain blob (file stores \\\" inside pr-str blob) ---
chain = edn[edn.index(':arm/chain'):edn.index(', :arm/name')].replace('\\"', '"')
rjoints, rlinks, rbase = {}, {}, {}
for jm in re.finditer(r':joint/name "(j\d)"(.{0,1200}?)\}\} (?=\{:joint/axis|\Z)', chain, re.S):
    name, body = jm.group(1), jm.group(2)
    rjoints[name] = dict(
        origin=re.search(r':joint/origin \[([^\]]+)\]', body).group(1).split(),
        axis=re.search(r':joint/axis \[([^\]]+)\]', body).group(1).split(),
        damping=float(re.search(r':joint/damping ([\d.]+)', body).group(1)),
        lower=re.search(r':limit \{:lower (-?[\d.]+), :upper (-?[\d.]+), :effort (-?[\d.]+), :velocity ([\d.]+)\}', body).groups())
    cm = re.search(r':child/link #:link\{:name "(link\d)", :inertial \{:origin \[([^\]]+)\], :mass ([\d.eE+-]+), :inertia \{:ixx ([\d.eE+-]+), :iyy ([\d.eE+-]+), :izz ([\d.eE+-]+)\}', body)
    if cm:
        rlinks[cm.group(1)] = dict(origin=cm.group(2).split(), mass=float(cm.group(3)),
                                   inertia=dict(ixx=float(cm.group(4)), iyy=float(cm.group(5)),
                                                izz=float(cm.group(6))))
b = edn[edn.index(':arm/base'):]
bm = re.search(r':origin \[([^\]]+)\], :mass ([\d.]+), :inertia \{:ixx ([\d.eE+-]+), :iyy ([\d.eE+-]+), :izz ([\d.eE+-]+), :ixy ([\d.eE+-]+), :ixz ([\d.eE+-]+), :iyz ([\d.eE+-]+)\}', b)
rbase = dict(origin=bm.group(1).split(), mass=float(bm.group(2)),
             inertia=dict(ixx=float(bm.group(3)), iyy=float(bm.group(4)), izz=float(bm.group(5)),
                          ixy=float(bm.group(6)), ixz=float(bm.group(7)), iyz=float(bm.group(8))))

fails = []
def numcmp(label, a, b):
    try:
        fa = float(a[0]) if isinstance(a, (tuple, list)) else float(a)
    except (TypeError, ValueError):
        fails.append(f"{label}: unparseable urdf={a!r} edn={b!r}"); return
    if abs(fa - b) > 1e-12:
        fails.append(f"{label}: urdf={fa} edn={b}")

def cmp(label, a, b):
    if isinstance(b, dict):
        for k in b:
            cmp(f"{label}.{k}", (a or {}).get(k), b[k])
    elif isinstance(b, (list, tuple)):
        if a is None or [float(x) for x in a] != [float(x) for x in b]:
            fails.append(f"{label}: urdf={a} edn={b}")
    else:
        numcmp(label, a, b)

for j, u in joints.items():
    r = rjoints.get(j)
    if not r:
        fails.append(f"joint {j}: missing in EDN"); continue
    cmp(f"{j}.origin", r["origin"], u["origin"])
    cmp(f"{j}.axis", r["axis"], u["axis"])
    cmp(f"{j}.damping", r["damping"], u["damping"])
    cmp(f"{j}.lower", r["lower"][0], u["lower"])
    cmp(f"{j}.upper", r["lower"][1], u["upper"])
    cmp(f"{j}.effort", r["lower"][2], u["effort"])
    cmp(f"{j}.velocity", r["lower"][3], u["velocity"])
for l, u in links.items():
    r = rbase if l == "base_link" else rlinks.get(l)
    if not r:
        fails.append(f"link {l}: missing in EDN"); continue
    cmp(f"{l}.inertial.origin", r["origin"], u["origin"])
    cmp(f"{l}.mass", r["mass"], u["mass"])
    cmp(f"{l}.inertia", r["inertia"], u["inertia"])

print(f"joints compared: {len(joints)}, links compared: {len(links)}")
print(f"mismatches: {len(fails)}")
for f in fails:
    print("MISMATCH:", f)
sys.exit(1 if fails else 0)
