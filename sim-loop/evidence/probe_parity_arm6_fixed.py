#!/usr/bin/env python3
"""Falsification probe (fresh, corrected parser): URDF <-> EDN parity for
fixtures/giemon_arm6.

Replaces the stale probe_parity_arm6.py whose slice-anchor regex
(`:joint/name "(jN)" ... }} {:joint/axis...`) coupled joint boundaries on a
brace+space lookahead, dropped the preceding axis/origin from each slice, and
PARSE-ERR'd (exit 1; falsify-037). This version splits the EDN :arm/chain on
the per-joint literal marker `:joint/axis [` (each joint map in this fixture
begins that way), so the preceding axis/origin are captured and no brace-lookahead
is needed. It uses plain str.find/str.split — no regex backslash escaping in the
EDN path — robust to quoting/escaping layers. (Regex survives only in the URDF
XML path, where the markup is well-formed.)

Measurement only. Compares every numeric field URDF exposes (joint
origin/axis/damping/limit, link inertial origin/mass/inertia incl. off-diag)
against the EDN :arm/chain blob. Exit 1 on any mismatch or parse failure.
Deterministic — pure text parsing, no sim run. Host-load independent.
"""
import re
import sys

A6 = "/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon/fixtures/giemon_arm6"
urdf_txt = open(A6 + "/giemon_arm6.urdf").read()
edn_txt = open(A6 + "/giemon_arm6.edn").read()

fails = []

# ---------------- URDF parse ----------------
joints = {}
for m in re.finditer(r'<joint name="(j\d)" type="revolute">(.*?)</joint>', urdf_txt, re.S):
    name, body = m.group(1), m.group(2)
    xyz, rpy = re.search(r'<origin xyz="([^"]+)" rpy="([^"]+)"', body).groups()
    axis = re.search(r'<axis xyz="([^"]+)"', body).group(1).split()
    damp = re.search(r'damping="([^"]+)"', body).group(1)
    lim = re.search(r'lower="([^"]+)" upper="([^"]+)" effort="([^"]+)" velocity="([^"]+)"', body).groups()
    joints[name] = dict(origin=xyz.split(), rpy=rpy.split(), axis=axis,
                        lower=float(lim[0]), upper=float(lim[1]),
                        effort=float(lim[2]), velocity=float(lim[3]),
                        damping=float(damp))

links = {}
for m in re.finditer(r'<link name="(\w+)">\s*<inertial>\s*<origin xyz="([^"]+)"[^/]*/>\s*<mass value="([^"]+)"/>\s*<inertia ([^/]*)/>', urdf_txt):
    name, org, mass, inert = m.groups()
    links[name] = dict(origin=org.split(), mass=float(mass),
                       inertia={k: float(v) for k, v in
                                re.findall(r'(ixx|iyy|izz|ixy|ixz|iyz)="([^"]+)"', inert)})

# ---------------- EDN parse (plain string ops) ----------------
chain = edn_txt[edn_txt.index(':arm/chain') : edn_txt.index(':arm/name')]
axis_marker = ':joint/axis ['
starts = []
i = 0
while True:
    i = chain.find(axis_marker, i)
    if i < 0:
        break
    starts.append(i)
    i += len(axis_marker)
n_joint = len(starts)

def cut(s, marker, term):
    p = s.find(marker)
    if p < 0:
        return None
    q = s.find(term, p + len(marker))
    if q < 0:
        return None
    return s[p + len(marker):q].strip()

def cut_tokens(s, marker, term):
    tok = cut(s, marker, term)
    return tok.split() if tok is not None else None

def to_float(seq):
    return [float(x) for x in seq]

def numtok(tok):
    mm = re.search(r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', tok)
    return mm.group(0) if mm else None

edn_joints = {}
for k in range(n_joint):
    start = starts[k]
    end = starts[k+1] if k+1 < n_joint else chain.rindex(']')
    seg = chain[start:end]
    axis = cut_tokens(seg, ':joint/axis [', ']')
    origin = cut_tokens(seg, ':joint/origin [', ']')
    damp_t = cut(seg, ':joint/damping ', ',')
    lim_t = cut(seg, ':joint/limit ', '}')
    org2 = cut_tokens(seg, ':inertial {:origin [', ']')
    mass_t = cut(seg, ':mass ', ',')
    ia = cut_tokens(seg, ':ixx ', ',')
    ib = cut_tokens(seg, ':iyy ', ',')
    ic = cut_tokens(seg, ':izz ', '}')
    missing = []
    if axis is None: missing.append("axis")
    if origin is None: missing.append("origin")
    if damp_t is None: missing.append("damping")
    if lim_t is None: missing.append("limit")
    if org2 is None: missing.append("child.inertial.origin")
    if mass_t is None: missing.append("child.mass")
    if ia is None or ib is None or ic is None: missing.append("child.inertia")
    if missing:
        fails.append(f"joint index {k}: EDN missing {missing}")
        continue
    vals = [float(t) for t in (numtok(x) for x in lim_t.replace(':', ' ').split()) if t is not None]
    if len(vals) < 4:
        fails.append(f"joint index {k}: limit values unparsable: {lim_t!r}")
        continue
    edn_joints[k] = dict(axis=to_float(axis), origin=to_float(origin),
                         damping=float(damp_t),
                         lower=vals[0], upper=vals[1], effort=vals[2],
                         velocity=vals[3],
                         corigin=to_float(org2), cmass=float(mass_t),
                         cinertia=[float(ia[0]), float(ib[0]), float(ic[0])])

# EDN base link
b = edn_txt[edn_txt.index(':arm/base'):]
b_origin = cut_tokens(b, ':origin [', ']')
b_mass = cut(b, ':mass ', ',')
b_ixx = cut(b, ':ixx ', ',')
b_iyy = cut(b, ':iyy ', ',')
b_izz = cut(b, ':izz ', ',')
b_ixy = cut(b, ':ixy ', ',')
b_ixz = cut(b, ':ixz ', ',')
b_iyz = cut(b, ':iyz ', '}')
edn_base = None
if all(v is not None for v in [b_origin, b_mass, b_ixx, b_iyy, b_izz, b_ixy, b_ixz, b_iyz]):
    edn_base = dict(origin=to_float(b_origin), mass=float(b_mass),
                    ixx=float(b_ixx), iyy=float(b_iyy), izz=float(b_izz),
                    ixy=float(b_ixy), ixz=float(b_ixz), iyz=float(b_iyz))
else:
    fails.append("base_link: EDN base inertial incomplete/absent")

# ---------------- compare ----------------
TOL = 1e-12
def fcmp(label, a, b):
    try:
        if abs(float(a) - float(b)) > TOL:
            fails.append(f"{label}: urdf={a} edn={b}")
    except Exception as e:
        fails.append(f"{label}: cmp error {e} urdf={a!r} edn={b!r}")

def lcmp3(label, ua, ea):
    if ua is None or ea is None:
        fails.append(f"{label}: missing urdf={ua} edn={ea}"); return
    if len(ua) != len(ea):
        fails.append(f"{label}: len urdf={ua} edn={ea}"); return
    if to_float(ua) != to_float(ea):
        fails.append(f"{label}: urdf={ua} edn={ea}")

edn_joint_names = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
for k, name in enumerate(edn_joint_names):
    u = joints.get(name)
    e = edn_joints.get(k)
    if u is None:
        fails.append(f"joint {name}: missing in URDF"); continue
    if e is None:
        fails.append(f"joint {name}: missing in EDN"); continue
    lcmp3(f"{name}.axis", u["axis"], e["axis"])
    lcmp3(f"{name}.origin", u["origin"], e["origin"])
    fcmp(f"{name}.damping", u["damping"], e["damping"])
    fcmp(f"{name}.lower", u["lower"], e["lower"])
    fcmp(f"{name}.upper", u["upper"], e["upper"])
    fcmp(f"{name}.effort", u["effort"], e["effort"])
    fcmp(f"{name}.velocity", u["velocity"], e["velocity"])
    ln = name.replace('j', 'link')
    lu = links.get(ln)
    if lu is None:
        fails.append(f"{name} child link {ln}: missing in URDF"); continue
    lcmp3(f"{ln}.inertial.origin", lu["origin"], e["corigin"])
    fcmp(f"{ln}.mass", lu["mass"], e["cmass"])
    fcmp(f"{ln}.inertia.ixx", lu["inertia"]["ixx"], e["cinertia"][0])
    fcmp(f"{ln}.inertia.iyy", lu["inertia"]["iyy"], e["cinertia"][1])
    fcmp(f"{ln}.inertia.izz", lu["inertia"]["izz"], e["cinertia"][2])

ub = links.get("base_link")
if ub is None:
    fails.append("base_link: missing in URDF")
elif edn_base is None:
    fails.append("base_link: missing in EDN")
else:
    lcmp3("base_link.inertial.origin", ub["origin"], edn_base["origin"])
    fcmp("base_link.mass", ub["mass"], edn_base["mass"])
    for kk in ("ixx", "iyy", "izz", "ixy", "ixz", "iyz"):
        fcmp(f"base_link.inertia.{kk}", ub["inertia"][kk], edn_base[kk])

print(f"joints compared: {len(joints)} URDF / {n_joint} EDN")
print(f"links compared: {len(links)} URDF (incl base_link)")
print(f"mismatches: {len(fails)}")
for f_ in fails:
    print("MISMATCH:", f_)
sys.exit(1 if fails else 0)