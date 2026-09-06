# falsify-002 probe — j2 quasi-dynamic worst case (quasi-static + inertial term, DR mass scale)
# geometry from fixtures/giemon_arm6/giemon_arm6.edn (values verbatim).
# Links stack along +z. j2 axis = [0,1,0]. Horizontal j2 posture: link COMs
# extend along the horizontal arm direction.
# COM offsets used (from joint origins in fixture):
#   link1 COM z +0.03 from j1; j2 sits +0.06 above link1 origin
#   link2 COM z +0.09 from j2; j3 sits +0.18 above link2 origin
#   link3 COM z +0.07 from j3; j4 origin +0.16 above link3 (elbow)
#   link4 COM z +0.05 approx from j4; j5 origin +0.12
#   link5 COM z +0.04; j6 origin +0.09
#   link6 COM z +0.03
# Masses: 0.6, 0.5, 0.35, 0.22, 0.16, 0.12 (fixture verbatim)
masses = [0.6, 0.5, 0.35, 0.22, 0.16, 0.12]
# horizontal distance of each link COM from the j2 axis (shoulder), metres
r = [0.0, 0.09, 0.18+0.07, 0.18+0.16, 0.18+0.16+0.12, 0.18+0.16+0.12+0.09+0.03]
g = 9.81

def gravity_torque(payload_kg=0.0, r_payload=0.55):
    t = sum(m*g*ri for m, ri in zip(masses, r))
    t += payload_kg*g*r_payload
    return t

# inertia about j2 axis (point-mass approx; link ixx/iyy small vs m r^2)
I = sum(m*ri*ri for m, ri in zip(masses, r))

tau_cont = 40.0
tau0 = gravity_torque()

# DR mass scale k (mass x k), fixed trajectory accel alpha on j2
def demand(k, alpha):
    return k*(tau0 + I*alpha)

# alpha that breaks cont=40 at k=1
alpha_break = (tau_cont - tau0)/I
# k that breaks cont=40 at alpha=0 (pure DR mass amplification, static)
k_break_static = tau_cont/tau0
# k that breaks at a modest trajectory alpha=5 rad/s^2
k_break_a5 = tau_cont/(tau0 + I*5.0)
# peak torque margin: peak 120 vs worst cont-bound demand
print(f"I_j2(point-mass) = {I:.4f} kg m^2")
print(f"tau0 (gravity, no payload) = {tau0:.2f} Nm  (falsify-001: 2.73)")
print(f"tau(3kg payload @0.55m) = {gravity_torque(3.0):.2f} Nm (falsify-001: 18.6)")
print(f"alpha to break cont 40 at k=1: {alpha_break:.1f} rad/s^2")
print(f"DR mass scale k to break cont 40, alpha=0: {k_break_static:.2f}x")
print(f"DR mass scale k to break cont 40, alpha=5 rad/s^2: {k_break_a5:.2f}x")
print(f"peak-nm margin at k=2, alpha=5: {120 - demand(2,5):.1f} Nm of 120")
