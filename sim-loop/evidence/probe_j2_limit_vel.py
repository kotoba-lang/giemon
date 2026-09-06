# falsify-004 probe — j2 full-dynamic worst case RESTRICTED to the fixture's
# own declared :joint/limit :velocity envelope. falsify-003's break points
# (k≈1.4x at w2=5/w3=10) used velocities ABOVE the fixture's declared limits
# (j2 :velocity 3, j3 :velocity 3). Question: does cont 40 still break at
# realistic DR mass scale k when every joint runs at or below its declared
# velocity limit? Same point-mass worst-case model as probe_j2_coriolis.py
# (gravity + j2 own inertia + Coriolis 2*w2*w3 + centrifugal w3^2), plus an
# alpha term from worst-case trapezoid ramp (alpha = w2 / 0.1 s, 0.1 s ramp
# to limit speed — generous).
#
# Geometry/masses verbatim from fixtures/giemon_arm6/giemon_arm6.edn:
#   masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
#   horizontal COM distance r_i from j2 axis (shoulder), metres:
#     r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
# Declared limits (fixture): j2 {effort 40, velocity 3}, j3 {effort 30, velocity 3}.
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
g = 9.81
tau_cont_j2 = 40.0   # fixture j2 :cont-nm 40, :effort 40
tau_peak_j2 = 120.0  # fixture j2 :peak-nm 120
W2_LIM = 3.0         # fixture j2 :velocity
W3_LIM = 3.0         # fixture j3 :velocity

tau0 = sum(m*g*ri for m, ri in zip(masses, r))
I = sum(m*ri*ri for m, ri in zip(masses, r))
I_distal = sum(m*ri*ri for m, ri in zip(masses[2:], r[2:]))
alpha_ramp = W2_LIM / 0.1  # worst-case 0.1 s ramp to declared limit speed

def demand(k, w2, w3, alpha=0.0):
    grav = k*tau0
    inert = k*I*alpha*alpha
    cor = k*2*I_distal*w2*w3
    cen = k*I_distal*w3*w3
    return grav, inert, cor, cen

print(f"tau0={tau0:.2f} Nm  I={I:.4f}  I_distal={I_distal:.4f} kg m^2")
print(f"declared limits: w2<={W2_LIM} j2, w3<={W3_LIM} j3, alpha_ramp={alpha_ramp:.1f} rad/s^2")

print("\n-- worst case AT declared velocity limits (w2=3, w3=3), steady state --")
for k in (1.0, 1.2, 2.0, 5.0, 8.0):
    gv, iv, cv, cf = demand(k, W2_LIM, W3_LIM)
    tot = gv + iv + cv + cf
    print(f"k={k}: grav={gv:.1f} cor={cv:.1f} cent={cf:.1f} total={tot:.1f} "
          f"cont_break={tot > tau_cont_j2} peak_break={tot > tau_peak_j2}")

print("\n-- ramp worst case (alpha = 30 rad/s^2, w2=3, w3=3) --")
for k in (1.0, 2.0, 5.0, 8.0):
    gv, iv, cv, cf = demand(k, W2_LIM, W3_LIM, alpha_ramp)
    tot = gv + iv + cv + cf
    print(f"k={k}: grav={gv:.1f} inert={iv:.1f} cor={cv:.1f} cent={cf:.1f} "
          f"total={tot:.1f} cont_break={tot > tau_cont_j2} peak_break={tot > tau_peak_j2}")

# minimal k breaking cont/peak at the declared-limit envelope, steady and ramp
coeff_steady = I*0 + 2*I_distal*W2_LIM*W3_LIM + I_distal*W3_LIM*W3_LIM
coeff_ramp = I*alpha_ramp*alpha_ramp + coeff_steady
print(f"\nk_break_cont (steady, w=limits)   = {(tau_cont_j2 - tau0)/coeff_steady:.2f}x")
print(f"k_break_cont (ramp, w=limits)     = {(tau_cont_j2 - tau0)/coeff_ramp:.2f}x")
print(f"k_break_peak  (ramp, w=limits)    = {(tau_peak_j2 - tau0)/coeff_ramp:.2f}x")

# falsify-003 comparison: their w2=5/w3=10 and w2=3/w3=6 exceed j3's limit (3)
for w2, w3 in ((3.0, 6.0), (5.0, 10.0)):
    over = "ABOVE j3 limit 3.0" if w3 > W3_LIM else "within j3 limit"
    over2 = "ABOVE j2 limit 3.0" if w2 > W2_LIM else "within j2 limit"
    print(f"falsify-003 speed pair w2={w2} ({over2}) w3={w3} ({over})")
