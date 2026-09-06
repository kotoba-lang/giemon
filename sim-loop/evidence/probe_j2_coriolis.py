# falsify-003 probe — j2 full-dynamic worst case: Coriolis/centrifugal from distal
# joint velocity, under DR mass scale k. Extends probe_j2_dynamic.py (quasi-static
# + inertial term only, falsify-002) with the terms it lacked.
# Geometry/masses verbatim from fixtures/giemon_arm6 (same model as probe_j2_dynamic.py):
#   masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
#   horizontal COM distance r_i from j2 axis (shoulder), metres:
#     r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
# Model (worst-case alignment, point-mass):
#   gravity:            tau_g   = g * sum m_i r_i
#   j2 own angular accel (proxy a2 = w2^2 over a half-cycle):
#                       tau_in  = sum m_i r_i^2 * w2^2
#   Coriolis (distal mass swinging with w3 about j3 while j2 rotates w2,
#   a = 2 w2 w3 r, torque = m a r):
#                       tau_cor = 2 * sum_{i>=3} m_i r_i^2 * w2 * w3
#   Centrifugal from w3 swing, worst case horizontal (gravity-like arm):
#                       tau_cen = sum_{i>=3} m_i r_i^2 * w3^2
# All demand terms scale linearly with DR mass scale k.
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
r = [0.0, 0.09, 0.25, 0.34, 0.46, 0.55]
g = 9.81
tau_cont = 40.0
tau_peak = 120.0

tau0 = sum(m*g*ri for m, ri in zip(masses, r))
I = sum(m*ri*ri for m, ri in zip(masses, r))
I_distal = sum(m*ri*ri for m, ri in zip(masses[2:], r[2:]))

def demand(k, w2, w3):
    grav = k*tau0
    inert = k*I*w2*w2
    cor = k*2*I_distal*w2*w3
    cen = k*I_distal*w3*w3
    return grav, inert, cor, cen

print(f"tau0={tau0:.2f} Nm  I={I:.4f}  I_distal={I_distal:.4f} kg m^2")
for k in (1.0, 2.0, 5.0):
    for w2, w3 in ((2.0, 5.0), (5.0, 10.0), (10.0, 20.0)):
        gv, iv, cv, cf = demand(k, w2, w3)
        tot = gv + iv + cv + cf
        print(f"k={k} w2={w2} w3={w3}: grav={gv:.1f} inert={iv:.1f} "
              f"cor={cv:.1f} cent={cf:.1f} total={tot:.1f} "
              f"cont_break={tot > tau_cont} peak_break={tot > tau_peak}")

# minimal k breaking cont at realistic wrist speeds
for w2, w3 in ((3.0, 6.0), (5.0, 10.0)):
    coeff = I*w2*w2 + 2*I_distal*w2*w3 + I_distal*w3*w3
    print(f"w2={w2} w3={w3}: k_break_cont = {(tau_cont - tau0)/coeff:.2f}")
