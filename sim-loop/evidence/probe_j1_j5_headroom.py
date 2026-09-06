# falsify-007 probe — do the headroom-0 joints OTHER than j2 (j1, j5) break
# under realistic DR k? All prior falsify iterations measured ONLY j2.
# Claim under test (H9): "headroom-0 joints (j1/j2/j5) do not break under
# realistic DR k≈1.2" — the j1/j5 half is UNMEASURED so far.
#
# Simple point-mass worst-case model, masses/radii verbatim from
# fixtures/giemon_arm6 (same convention as probe_j2_cont_duty.py).
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]   # link1..link6
r     = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]   # cumulative z-offsets
g = 9.81
W = 3.0   # declared velocity limit of j2/j3 (rad/s)

# ---------- j1 (axis z, vertical): gravity torque about z = 0.
# Dynamic load about z comes from coupling with j2 motion (arm swinging up
# while base rotates) — conservative bound: coriolis-style 2*w1*w2*I_z_distal
# plus centrifugal w1^2 * I_z. Arm folded horizontal (worst r_xy).
I_z = sum(m * ri * ri for m, ri in zip(masses, r))     # all distal of j1
w1 = 3.0   # j1 declared velocity limit
w2 = 3.0   # j2 declared velocity limit
coeff_dyn_j1 = 2 * w1 * w2 * I_z          # coriolis worst-case bound
tau0_j1 = 0.0                              # vertical axis: no gravity load
cont_j1, peak_j1 = 40.0, 120.0
I_j1_alpha = I_z                           # I*alpha about z

# ---------- j5 (axis y, wrist pitch): distal = link6 only (mass 0.12, r 0.55)
m6, r6 = masses[5], r[5]
tau0_j5 = m6 * g * r6                      # worst case: arm horizontal
I5 = m6 * r6 * r6
cont_j5, peak_j5 = 10.0, 23.7              # Unitree GO-M8010-6 (from EDN)
# j5 declared velocity 4 rad/s; base yaw w1=3 (j1 limit), wrist roll w6=5
w5, w1b, w6 = 4.0, 3.0, 5.0
coeff_dyn_j5 = (w1b ** 2) * I5 + 2 * w5 * w6 * I5   # centrifugal + coriolis bound

def rms(xs):
    return (sum(x * x for x in xs) / len(xs)) ** 0.5

def cycle_j1(k, alpha):
    # trapezoid: ramp up (I*alpha grows linearly), cruise (coriolis only),
    # ramp down, reverse, rest. Same 20-sample discretisation as falsify-006.
    ramp = W / alpha
    seg = []
    for t in frange(ramp, 20):
        seg.append(k * (I_j1_alpha * alpha * t / ramp) + coeff_dyn_j1)
    seg += [k * 0.0 + coeff_dyn_j1] * max(1, int((w1 / alpha) * 20))
    for t in frange(ramp, 20):
        seg.append(k * (-I_j1_alpha * alpha * t / ramp) + coeff_dyn_j1)
    seg += [0.0] * int(0.2 * 20)
    return seg

def cycle_j5(k, alpha):
    ramp = 4.0 / alpha
    seg = []
    for t in frange(ramp, 20):
        seg.append(k * (tau0_j5 + I5 * alpha * t / ramp) + coeff_dyn_j5)
    seg += [k * tau0_j5 + coeff_dyn_j5] * max(1, int((w5 / alpha) * 20))
    for t in frange(ramp, 20):
        seg.append(k * (tau0_j5 - I5 * alpha * t / ramp) + coeff_dyn_j5)
    # return stroke: gravity assists
    for t in frange(ramp, 20):
        seg.append(k * (-tau0_j5 + I5 * alpha * t / ramp) + coeff_dyn_j5)
    seg += [k * (-tau0_j5) + coeff_dyn_j5] * max(1, int((w5 / alpha) * 20))
    for t in frange(ramp, 20):
        seg.append(k * (-tau0_j5 - I5 * alpha * t / ramp) + coeff_dyn_j5)
    seg += [0.0] * int(0.2 * 20)
    return seg

def frange(stop, n):
    step = stop / n if n > 0 else 0
    return [i * step for i in range(n)] if n > 0 else []

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

print(f"j1: I_z={I_z:.4f} kg m^2  coeff_dyn(w1=3,w2=3)={coeff_dyn_j1:.2f} Nm  cont={cont_j1} peak={peak_j1}")
for alpha in (3.0, 10.0, 30.0):
    k_rms = bisect_cont(cycle_j1, cont_j1, alpha)
    pk = max(cycle_j1(1.0, alpha))
    k_peak = peak_j1 / pk if pk > 0 else float("inf")
    c12 = cycle_j1(1.2, alpha)
    print(f"  alpha={alpha:5.1f}: k_rms@cont40={k_rms:7.2f}  k_peak@120={k_peak:7.2f}  k=1.2 RMS={rms(c12):5.1f} peak={max(c12):6.1f} Nm")

print(f"\nj5: tau0={tau0_j5:.2f} Nm  I5={I5:.5f}  coeff_dyn={coeff_dyn_j5:.3f} Nm  cont={cont_j5} peak={peak_j5}")
for alpha in (8.0, 20.0, 40.0):   # 0.5s / 0.2s / 0.1s ramps to w5=4
    k_rms = bisect_cont(cycle_j5, cont_j5, alpha)
    pk = max(cycle_j5(1.0, alpha))
    k_peak = peak_j5 / pk if pk > 0 else float("inf")
    c12 = cycle_j5(1.2, alpha)
    print(f"  alpha={alpha:5.1f}: k_rms@cont10={k_rms:7.2f}  k_peak@23.7={k_peak:7.2f}  k=1.2 RMS={rms(c12):5.1f} peak={max(c12):6.1f} Nm")

# static reference
print(f"\nstatic: j1 gravity-about-z = 0.00 Nm (vertical axis); j5 static = {tau0_j5:.2f} / {cont_j5} Nm")
