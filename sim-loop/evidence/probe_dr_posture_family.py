# falsify-016 probe — DR initial-posture worst case x DR mass scale k.
# All prior dynamic break-point probes (falsify-002..007) assumed ONE posture:
# arm fully extended horizontal from j2 (elbow straight, phi=0 — the
# falsify-002..006 form). NEXT (d): measure the break-point family over
# initial postures (elbow angle phi) and re-check per-posture end-effector
# determinism (SEED-PARITY per posture) — the seeded-reproduction combination.
#
# Model (point-mass worst-case, masses/radii verbatim from fixtures/giemon_arm6;
# same convention as probe_j2_cont_duty.py):
#   masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
#   r(phi) = horizontal distance of each link COM from the j2 axis:
#     upper arm (link2):   r2 = 0.09                       (always horizontal segment)
#     forearm/wrist (i>=3): r_i = r3_base + cos(phi) * d_i
#       r3_base = 0.18 (j3 sits 0.18 above j2 in z; at phi=90deg the forearm
#       points vertically so its COMs keep only the j2->j3 horizontal offset)
#       d_i = horizontal offsets beyond j3 when straight:
#             d = [0.07, 0.16, 0.28, 0.37]  (link3..link6 COM, falsify-002 r minus 0.18)
#     phi = 0    : fully extended horizontal (the falsify-002..007 posture)
#     phi = pi/2 : forearm folded vertical (minimum lever arm)
#     phi = pi/4 : intermediate
# Torque demand at j2 (worst-case alignment, point-mass):
#   grav:  tau_g   = k * g * sum m_i r_i(phi)
#   inert: tau_in  = k * I(phi) * alpha
#   cor:   tau_cor = k * 2 * I_distal(phi) * w2 * w3
#   cen:   tau_cen = k * I_distal(phi) * w3^2
# RMS duty evaluation identical to falsify-006 (trapezoid, w=3 rad/s, 20-sample
# ramps, rest segments, brake-hold variant); break point k_bisect per posture.
import math

masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
g = 9.81
tau_cont, tau_peak = 40.0, 120.0
W = 3.0

BASE2 = 0.09      # link2 COM horizontal from j2
R3BASE = 0.18     # j3 horizontal offset from j2 (forearm folded vertical)
D = [0.07, 0.16, 0.28, 0.37]   # link3..link6 COM horizontal offsets beyond j3 (straight)

def radii(phi):
    c = math.cos(phi)
    r = [0.0, BASE2]
    for d in D:
        r.append(R3BASE + c * d)
    return r

def inertiaphi(phi):
    r = radii(phi)
    I = sum(m * ri * ri for m, ri in zip(masses, r))
    I_d = sum(m * ri * ri for m, ri in zip(masses[2:], r[2:]))
    tau0 = sum(m * g * ri for m, ri in zip(masses, r))
    return tau0, I, I_d

def rms(xs):
    return (sum(x * x for x in xs) / len(xs)) ** 0.5

def frange(stop, n):
    if n <= 0:
        return []
    step = stop / n
    return [i * step for i in range(n)]

def cycle(k, phi, ramp, rest, alpha_extra=0.0):
    tau0, I, I_d = inertiaphi(phi)
    a = W / ramp
    coeff_dyn = 2 * I_d * W * W + I_d * W * W   # cor (w2=w3=W) + cent (w3=W)
    T_c = W / a if a > 0 else 0
    seg = []
    seg += [k * (tau0 + I * a + alpha_extra * I) + coeff_dyn for t in frange(ramp, 20)]
    seg += [k * (tau0) + coeff_dyn] * max(1, int(T_c * 20))
    seg += [k * (tau0 - I * a - alpha_extra * I) + coeff_dyn for t in frange(ramp, 20)]
    seg += [k * (-tau0 + I * a) for t in frange(ramp, 20)]
    seg += [k * (-tau0)] * max(1, int(T_c * 20))
    seg += [k * (-tau0 - I * a) for t in frange(ramp, 20)]
    seg += [k * tau0] * int(rest * 20)   # brake hold
    return seg

POSTURES = [
    ("extended-phi0", 0.0),
    ("mid-phi45", math.pi / 4),
    ("folded-phi90", math.pi / 2),
]

print("posture family x DR k break points (j2, cont 40 / peak 120):")
print(f"{'posture':>14} {'tau0':>6} {'I':>7} | {'ramp_s':>6} {'rest_s':>6} | {'k_rms@cont40':>12} {'k_peak@120':>10} | k=1.2 RMS/peak")
worst_rms = (None, float("inf"))
for name, phi in POSTURES:
    tau0, I, I_d = inertiaphi(phi)
    for ramp in (0.02, 0.1, 0.3):
        for rest in (0.2, 1.0):
            lo, hi = 1.0, 60.0
            for _ in range(60):
                mid = (lo + hi) / 2
                c = cycle(mid, phi, ramp, rest)
                if max(c) > 0 and rms(c) < tau_cont:
                    lo = mid
                else:
                    hi = mid
            k_rms = (lo + hi) / 2
            pk = max(cycle(1.0, phi, ramp, rest))
            k_peak = tau_peak / pk if pk > 0 else float("inf")
            c12 = cycle(1.2, phi, ramp, rest)
            if k_rms < worst_rms[1]:
                worst_rms = ((name, ramp, rest), k_rms)
            print(f"{name:>14} {tau0:6.2f} {I:7.4f} | {ramp:6.2f} {rest:6.1f} | {k_rms:12.2f} {k_peak:10.2f} | {rms(c12):6.1f} / {max(c12):6.1f} Nm")

print(f"\nWORST-RMS-BREAK: posture={worst_rms[0]} k={worst_rms[1]:.2f}  (realistic DR k=1.2: "
      f"{'BROKEN' if worst_rms[1] < 1.2 else 'not broken'})")
