#!/usr/bin/env python3
"""falsify-035 (H36) parity probe — URDF <-> EDN for fixtures/giemon_arm6.
Fresh, robust parser (unlike the shipped probe_parity_arm6.py which crashes on
the current double-backslash-escaped blob). Measurement only.
Output: joints=6 links=7 mismatches=0, exit 0 on full parity."""
import re, sys
d = "/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon/fixtures/giemon_arm6"
urdf = open(d + "/giemon_arm6.urdf").read(); edn = open(d + "/giemon_arm6.edn").read()
def uf(x): return [float(v) for v in x.split()]
J, L = {}, {}
for m in re.finditer('<joint name="(j\\d)" type="revolute">(.*?)</joint>', urdf, re.S):
    b = m.group(2)
    o = re.search('<origin xyz="([^"]+)" rpy="([^"]+)"', b); a = re.search('<axis xyz="([^"]+)"', b)
    im = re.search('lower="([^"]+)" upper="([^"]+)" effort="([^"]+)" velocity="([^"]+)"', b); dm = re.search('dynamics damping="([^"]+)"', b)
    if not (o and a and im and dm): print("UERR", m.group(1)); sys.exit(2)
    J[m.group(1)] = dict(origin=uf(o.group(1)), axis=uf(a.group(1)), lower=float(im.group(1)),
        upper=float(im.group(2)), effort=float(im.group(3)), velocity=float(im.group(4)), damping=float(dm.group(1)))
for m in re.finditer('<link name="(link\\d)">\\s*<inertial>\\s*<origin xyz="([^"]+)"[^>]*/>\\s*<mass value="([^"]+)"/>\\s*<inertia ([^/]*)/>', urdf):
    L[m.group(1)] = dict(origin=uf(m.group(2)), mass=float(m.group(3)), inertia={k: float(v) for k, v in re.findall(r'(ixx|iyy|izz|ixy|ixz|iyz)="([^"]+)"', m.group(4))})
bm = re.search('<link name="base_link">\\s*<inertial>\\s*<origin xyz="([^"]+)"[^>]*/>\\s*<mass value="([^"]+)"/>\\s*<inertia ([^/]*)/>', urdf)
if not bm: print("UERR base"); sys.exit(2)
L["base_link"] = dict(origin=uf(bm.group(1)), mass=float(bm.group(2)), inertia={k: float(v) for k, v in re.findall(r'(ixx|iyy|izz|ixy|ixz|iyz)="([^"]+)"', bm.group(3))})

seg = edn[edn.index(':arm/chain'):edn.index(', :arm/name')]
chain = seg
for _ in range(3): chain = chain.replace('\\"', '"').replace('\\\\"', '"')
starts = [ss.start() for ss in re.finditer(r'\{:joint/axis', chain)]; starts.sort()
if len(starts) != 6: print("ERR joints %d" % len(starts)); sys.exit(2)
def js(i): return chain[starts[i]:(starts[i+1] if i+1 < len(starts) else chain.rindex(']'))]
EJ, EL = {}, {}
for i in range(len(starts)):
    sl = js(i)
    n = re.search(':joint/name "j(\\d)"', sl); o = re.search(':joint/origin \\[([^\\]]+)\\]', sl)
    a = re.search(':joint/axis \\[([^\\]]+)\\]', sl); dm = re.search(':joint/damping ([\\d.]+)', sl)
    lm = re.search(':joint/limit \\{:lower (-?[\\d.]+), :upper (-?[\\d.]+), :effort (-?[\\d.]+), :velocity ([\\d.]+)\\}', sl)
    cl = re.search(':child/link #:link\\{:name "(link\\d)", :inertial \\{:origin \\[([^\\]]+)\\], :mass ([\\d.eE+-]+), :inertia \\{:ixx ([\\d.eE+-]+), :iyy ([\\d.eE+-]+), :izz ([\\d.eE+-]+)', sl)
    if not all([n, o, a, dm, lm, cl]): print("ESLICE", i); sys.exit(2)
    nm_ = "j" + n.group(1)
    EJ[nm_] = dict(axis=uf(a.group(1)), origin=uf(o.group(1)), damping=float(dm.group(1)),
        lower=float(lm.group(1)), upper=float(lm.group(2)), effort=float(lm.group(3)), velocity=float(lm.group(4)))
    EL[cl.group(1)] = dict(origin=uf(cl.group(2)), mass=float(cl.group(3)), ixx=float(cl.group(4)), iyy=float(cl.group(5)), izz=float(cl.group(6)))
bx = edn[edn.index(':arm/base'):]
b2 = re.search(':origin \\[([^\\]]+)\\], :mass ([\\d.]+), :inertia \\{:ixx ([\\d.eE+-]+), :iyy ([\\d.eE+-]+), :izz ([\\d.eE+-]+)', bx)

fails = []
def nmc(l, u, e):
    if abs(u - e) > 1e-12: fails.append(l + ": u=%r e=%r" % (u, e))
def lst(l, u, e):
    if [float(x) for x in u] != [float(x) for x in e]: fails.append(l + ": u=%r e=%r" % (u, e))
for j, u in J.items():
    r = EJ.get(j)
    if not r: fails.append("joint %s missing" % j); continue
    lst(j + ".origin", u["origin"], r["origin"]); lst(j + ".axis", u["axis"], r["axis"])
    nmc(j + ".damping", u["damping"], r["damping"]); nmc(j + ".lower", u["lower"], r["lower"])
    nmc(j + ".upper", u["upper"], r["upper"]); nmc(j + ".effort", u["effort"], r["effort"])
    nmc(j + ".velocity", u["velocity"], r["velocity"])
for l, u in L.items():
    if l == "base_link":
        if not b2: fails.append("base unparseable"); continue
        lst(l + ".origin", u["origin"], uf(b2.group(1))); nmc(l + ".mass", u["mass"], float(b2.group(2)))
        nmc(l + ".ixx", u["inertia"]["ixx"], float(b2.group(3))); nmc(l + ".iyy", u["inertia"]["iyy"], float(b2.group(4)))
        nmc(l + ".izz", u["inertia"]["izz"], float(b2.group(5)))
        continue
    r = EL.get(l)
    if not r: fails.append("link %s missing" % l); continue
    lst(l + ".origin", u["origin"], r["origin"]); nmc(l + ".mass", u["mass"], r["mass"])
    nmc(l + ".ixx", u["inertia"]["ixx"], r["ixx"]); nmc(l + ".iyy", u["inertia"]["iyy"], r["iyy"])
    nmc(l + ".izz", u["inertia"]["izz"], r["izz"])
print("joints=%d links=%d mismatches=%d" % (len(J), len(L), len(fails)))
for f in fails: print("MISMATCH:", f)
sys.exit(1 if fails else 0)