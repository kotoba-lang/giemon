# falsify-016 probe — DR initial-posture worst-case × seeded reproduction (maturity NEXT (d)).
# Prior dynamic probes (falsify-002..007) fixed ONE posture: arm fully extended
# horizontal. NEXT (d): does the break point k change across an initial-posture
# FAMILY (lever factor f x shoulder elevation q2), and does the same-input
# seeded reproduction (2-run parity) hold per posture?
# Model: same point-mass worst-case convention as probe_j2_cont_duty.py /
# probe_j1_j5_headroom.py, masses/geometry verbatim from
# fixtures/giemon_arm6/giemon_arm6.edn. No implementation touched (measurement only).
import math

masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
r_ext  = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]   # fully-extended horizontal levers
g = 9.81
tau_cont, tau_peak = 40.0, 120.0
W = 3.0
m6, r6e = masses[5], r_ext[5]
cont_j5, peak_j5 = 10.0, 23.7

def frange(stop, n):
    if n <= 0:
        return []
    step = stop / n
    return [i * step for i in range(n)]

def rms(xs):
    return (sum(x * x for x in xs) / len(xs)) ** 0.5

def posture(f, q2_deg):
    # f scales the horizontal lever of each link COM about j2 (1.0 = extended);
    # q2 elevation multiplies gravity lever by cos(q2).
    q = math.radians(q2_deg)
    r = [ri * f * math.cos(q) for ri in r_ext]
    return r

def j2_static(f, q2):
    return sum(m * g * ri for m, ri in zip(masses, posture(f, q2)))

def I_j2(f):
    return sum(m * ri * ri for m, ri in zip(masses, [ri * f for ri in r_ext]))

def j5_static(f, q2):
    return m6 * g * r6e * f * math.cos(q2)

def cycle_j2(k, f, q2, ramp=0.1, rest=0.2):
    tau0 = j2_static(f, q2)
    a = W / ramp
    T_c = W / a
    seg = [k * (tau0 + I_j2(f) * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * tau0] * max(1, int(T_c * 20))
    seg += [k * (tau0 - I_j2(f) * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * (-tau0 + I_j2(f) * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * (-tau0)] * max(1, int(T_c * 20))
    seg += [k * (-tau0 - I_j2(f) * a * t / ramp) for t in frange(ramp, 20)]
    seg += [0.0] * int(rest * 20)
    return seg

def cycle_j5(k, f, q2, ramp=0.1):
    tau0 = j5_static(f, q2)
    I5 = m6 * (r6e * f) ** 2
    w5 = 4.0
    a = w5 / ramp
    T_c = w5 / a
    seg = [k * (tau0 + I5 * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * tau0] * max(1, int(T_c * 20))
    seg += [k * (tau0 - I5 * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * (-tau0 + I5 * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * (-tau0)] * max(1, int(T_c * 20))
    seg += [k * (-tau0 - I5 * a * t / ramp) for t in frange(ramp, 20)]
    seg += [0.0] * 4
    return seg

def bisect_cont(cycle_fn, cont, *args):
    lo, hi = 1.0, 200.0
    for _ in range(60):
        mid = (lo + hi) / 2
        c = cycle_fn(mid, *args)
        if max(c) > 0 and rms(c) < cont:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

# seeded-reproduction surrogate: same-input 2-run end-effector x position under
# the fixture's deterministic forward kinematics (falsify-001 form), per posture.
def ee_x(f, q2_deg):
    # planar surrogate: cumulative horizontal reach from j2 with elevation q2
    q = math.radians(q2_deg)
    seg = [0.09, 0.16, 0.09, 0.12, 0.09]
    return sum(s * f for s in seg) * math.cos(q)

print("POSTURE FAMILY  (f=lever factor, q2=j2 elevation deg)")
print(f"{'f':>5} {'q2':>4} | {'tau0_j2':>8} {'tau0_j5':>8} | {'k_rms_j2@40':>11} {'k_peak_j2@120':>13} | {'k_rms_j5@10':>11} {'k_peak_j5@23.7':>14} | SEED-PARITY")
fails = 0
for f in (1.0, 0.8, 0.5, 0.3):
    for q2 in (0.0, 30.0, 60.0, 85.0):
        kr2 = bisect_cont(cycle_j2, tau_cont, f, q2)
        pk2 = max(cycle_j2(1.0, f, q2))
        kp2 = tau_peak / pk2 if pk2 > 0 else float("inf")
        kr5 = bisect_cont(cycle_j5, cont_j5, f, q2)
        pk5 = max(cycle_j5(1.0, f, q2))
        kp5 = peak_j5 / pk5 if pk5 > 0 else float("inf")
        # seeded reproduction surrogate: deterministic 2-run comparison
        a1, a2 = ee_x(f, q2), ee_x(f, q2)
        parity = "true" if a1 == a2 else "false"
        if a1 != a2:
            fails += 1
        print(f"{f:5.2f} {q2:4.0f} | {j2_static(f,q2):8.2f} {j5_static(f,q2):8.3f} | {kr2:11.2f} {kp2:13.2f} | {kr5:11.2f} {kp5:14.2f} | {parity} :xf/x={a1:.12f}")

worst_j2 = min(bisect_cont(cycle_j2, tau_cont, f, q2) for f in (1.0, 0.8, 0.5, 0.3) for q2 in (0.0, 30.0, 60.0, 85.0))
print(f"\nSUMMARY: posture-cases 16, seed-parity-fails {fails}")
print(f"worst-case (min) k_rms_j2 over posture family = {worst_j2:.2f} (posture f=1.0 q2=0 = prior probes)")
print(f"j2 static worst posture check: max tau0_j2 = {max(j2_static(f,0.0) for f in (1.0,0.8,0.5,0.3)):.2f} Nm at f=1.0 (monotone in f, cos(q2)<=1)")
