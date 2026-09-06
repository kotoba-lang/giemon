# falsify-006 probe — is the remaining red from falsify-005 (cont 40 break at
# k≈1.6–2.9x under 0.02–0.05 s ramps) an EFFECTIVE violation?
#
# falsify-004/005 compared INSTANTANEOUS torque against cont 40. cont is the
# CONTINUOUS (thermal) rating: the meaningful test is RMS torque over a duty
# cycle (heating ~ tau^2). Hypothesis H8: the instantaneous cont break at
# k≈1.6–2.9x translates into an effective violation under realistic duty.
#
# Duty-cycle model (trapezoid move to declared vel limit w=3 rad/s and back,
# rest between moves):
#   accel ramp T_r:    tau = k*(tau0_pos + I*alpha + coeff_dyn)   (grav assists on return)
#   cruise T_c = w/a:  tau = k*(tau0_pos + coeff_dyn)
#   decel ramp T_r:    tau = k*(tau0_pos - I*alpha) + coeff_dyn   (braking, grav still loaded)
#   return move: gravity torque reverses sign (tau0 negative), same ramps
#   rest T_rest: tau = 0 (holding brake engaged) and holding variant tau = k*tau0
# RMS over cycle vs cont 40; peak vs 120.
#
# Geometry/masses verbatim from fixtures/giemon_arm6/giemon_arm6.edn.
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
g = 9.81
tau_cont, tau_peak = 40.0, 120.0
W = 3.0  # declared velocity limit j2 (rad/s)

tau0 = sum(m * g * ri for m, ri in zip(masses, r))
I = sum(m * ri * ri for m, ri in zip(masses, r))
I_distal = sum(m * ri * ri for m, ri in zip(masses[2:], r[2:]))
coeff_dyn = 3 * I_distal * W * W  # cor+cent worst at w2=w3=3 (falsify-003/004 form)

def rms(xs):
    return (sum(x * x for x in xs) / len(xs)) ** 0.5

def cycle(k, ramp, rest, brake_hold):
    a = W / ramp
    T_c = W / a if a > 0 else 0
    tau0_neg = tau0  # return stroke reverses gravity sign
    seg = []
    # outbound
    seg += [k * (tau0 + I * a) + coeff_dyn] * 1  # ramp segment (per-sample below)
    seg = [k * (tau0 + I * a * t / ramp) + coeff_dyn for t in frange(ramp, 20)]
    seg += [k * (tau0) + coeff_dyn] * max(1, int(T_c * 20))
    seg += [k * (tau0 - I * a * t / ramp) + coeff_dyn for t in frange(ramp, 20)]
    # return (gravity assists)
    seg += [k * (-tau0 + I * a * t / ramp) for t in frange(ramp, 20)]
    seg += [k * (-tau0)] * max(1, int(T_c * 20))
    seg += [k * (-tau0 - I * a * t / ramp) for t in frange(ramp, 20)]
    # rest
    seg += [k * tau0 if brake_hold else 0.0] * int(rest * 20)
    return seg

def frange(stop, n):
    if n <= 0:
        return []
    step = stop / n
    return [i * step for i in range(n)]

print(f"tau0={tau0:.2f} Nm  I={I:.4f}  coeff_dyn(w=3,3)={coeff_dyn:.2f}")
print(f"{'ramp_s':>7} {'rest_s':>6} {'hold':>5} | {'k_rms@cont40':>12} {'k_peak@120':>10} | k=1.2 RMS / peak")
for ramp in (0.02, 0.05, 0.1, 0.3):
    for rest in (0.2, 1.0):
        for hold in (False, True):
            # binary search k where RMS == cont 40
            lo, hi = 1.0, 60.0
            for _ in range(60):
                mid = (lo + hi) / 2
                if max(cycle(mid, ramp, rest, hold)) > 0 and rms(cycle(mid, ramp, rest, hold)) < tau_cont:
                    lo = mid
                else:
                    hi = mid
            k_rms = (lo + hi) / 2
            # k for peak
            pk = max(cycle(1.0, ramp, rest, hold))
            k_peak = tau_peak / pk if pk > 0 else float("inf")
            c12 = cycle(1.2, ramp, rest, hold)
            print(f"{ramp:7.2f} {rest:6.1f} {str(hold):>5} | {k_rms:12.2f} {k_peak:10.2f} | {rms(c12):6.1f} / {max(c12):6.1f} Nm")

# instantaneous-only comparison (falsify-005 numbers) for reference
print("\nreference (instantaneous, falsify-005 form):")
for ramp in (0.02, 0.05, 0.1):
    a = W / ramp
    print(f"  ramp={ramp}: k_cont_inst = {tau_cont/(tau0 + I*a + coeff_dyn):.2f}")
