# falsify-005 probe — falsify-004's peak-120 break at k≈1.04x rests entirely on
# a 0.1 s ramp assumption (alpha = w2/0.1 = 30 rad/s^2). falsify-004 itself
# noted ramp 0.3 s drops inert to ≈12.2 N·m (cont unmet). Question: over the
# FULL family of plausible trapezoid ramps, where does the peak-120 break
# point k actually sit, and what ramp time makes k=1.2 (±20% DR) safe?
# Same point-mass worst-case model as probe_j2_limit_vel.py:
#   tau = k*(tau0 + I*alpha^2? -> I*alpha) ... NOTE: probe_j2_limit_vel uses
#   inert = k*I*alpha*alpha — that is dimensionally wrong (N·m requires
#   I*alpha, not I*alpha^2). This probe measures BOTH forms to quantify how
#   much of falsify-004's red depends on that model form.
#
# Geometry/masses verbatim from fixtures/giemon_arm6/giemon_arm6.edn.
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
g = 9.81
tau_cont = 40.0
tau_peak = 120.0
W2_LIM = 3.0

tau0 = sum(m*g*ri for m, ri in zip(masses, r))
I = sum(m*ri*ri for m, ri in zip(masses, r))
I_distal = sum(m*ri*ri for m, ri in zip(masses[2:], r[2:]))
coeff_dyn = 2*I_distal*W2_LIM*W2_LIM + I_distal*W2_LIM*W2_LIM  # cor+cent at w=limits

def k_peak_ramp(alpha_form, form):
    # total(k) = k*(tau0 + inert + coeff_dyn) ; break peak when total > 120
    inert = I*alpha_form**2 if form == "squared" else I*alpha_form
    denom = tau0 + inert + coeff_dyn
    return tau_peak/denom

print(f"tau0={tau0:.2f} Nm  I={I:.4f}  I_distal={I_distal:.4f}  coeff_dyn(w=3,3)={coeff_dyn:.4f}")
print(f"{'ramp_s':>7} {'alpha':>7} | {'k_peak(sq)':>10} {'k_peak(lin)':>11} | {'k_cont(lin)':>11}")
ramps = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0, 2.0]
for t in ramps:
    a = W2_LIM/t
    ks = k_peak_ramp(a, "squared")
    kl = k_peak_ramp(a, "linear")
    kc = (tau_cont - 0)/ (tau0 + I*a + coeff_dyn)  # linear form, cont
    print(f"{t:7.2f} {a:7.1f} | {ks:10.2f} {kl:11.2f} | {kc:11.2f}")

# ramp time at which k=1.2 (±20% DR) stays under peak, linear (correct) form
t = 0.01
while t < 2.0:
    a = W2_LIM/t
    if tau_peak/(tau0 + I*a + coeff_dyn) > 1.2:
        print(f"\nlinear form: k=1.2 safe under peak for ramp >= {t:.3f} s")
        break
    t += 0.005
else:
    print("\nlinear form: k=1.2 never safe in scanned range")

# how much of falsify-004's red is the squared-inertia artifact?
a30 = 30.0
print(f"\nat alpha=30 (0.1s ramp): inert(squared)={I*a30**2:.1f} Nm  inert(linear)={I*a30:.1f} Nm")
print(f"  total(k=1, squared) = {tau0 + I*a30**2 + coeff_dyn:.1f} Nm (falsify-004: 115.9)")
print(f"  total(k=1, linear)  = {tau0 + I*a30 + coeff_dyn:.1f} Nm -> peak_break={tau0 + I*a30 + coeff_dyn > tau_peak}")
