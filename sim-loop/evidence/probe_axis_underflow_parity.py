# falsify-017 probe — H19: tiny-magnitude joint AXIS values (double underflow)
# are normalized in double precision; a DR/perturbation pipeline that scales the
# axis (or a URDF importer emitting e.g. 1e-200 components) can underflow a
# nonzero axis to the zero vector, where normalize() returns v UNCHANGED (not a
# unit vector). Then Rodrigues' formula produces a DIFFERENT rotation than the
# same logical axis at full magnitude -> same logical joint state, different
# end-effector => seeded-reproduction / parity break.
# This probe measures that numerically, in pure Python (same math as
# kotoba.giemon.kinematics axis-angle->rot + normalize), using the arm6 j1..j6
# axes verbatim from fixtures/giemon_arm6/giemon_arm6.edn.
# Measurement only — no implementation touched.
import math

def normalize(v):
    n = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if n == 0.0:
        return list(v)
    return [c / n for c in v]

def axis_angle_rot(axis, angle):
    x, y, z = normalize(axis)
    c, s = math.cos(angle), math.sin(angle)
    t = 1.0 - c
    return [
        [c + t*x*x,     t*x*y - s*z,   t*x*z + s*y],
        [t*x*y + s*z,   c + t*y*y,     t*y*z - s*x],
        [t*x*z - s*y,   t*y*z + s*x,   c + t*z*z],
    ]

def rotvec_angle(m):
    # rotation angle of matrix (0..pi) via trace
    tr = m[0][0] + m[1][1] + m[2][2]
    return math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0)))

def maxabs(m):
    return max(abs(x) for row in m for x in row)

AXES = {
    "j1 [0,0,1]": [0.0, 0.0, 1.0],
    "j2 [0,1,0]": [0.0, 1.0, 0.0],
    "j3 [0,1,0]": [0.0, 1.0, 0.0],
    "j5 [0,0,1]": [0.0, 0.0, 1.0],
}
ANGLES = [0.2, 1.5707963267948966, 3.0]

print("H19: tiny-axis underflow changes rotation for the same logical axis?")
fails = 0
for name, ax in AXES.items():
    for ang in ANGLES:
        m_ref = axis_angle_rot(ax, ang)
        a_ref = rotvec_angle(m_ref)
        for scale in (1e-8, 1e-150, 1e-200, 1e-210, 1e-250, 1e-300):
            tiny = [c * scale for c in ax]
            m_tiny = axis_angle_rot(tiny, ang)
            a_tiny = rotvec_angle(m_tiny)
            dev = abs(a_tiny - a_ref)
            flag = "DEVIATES" if dev > 1e-9 else "ok"
            if dev > 1e-9:
                fails += 1
            print(f"{name} ang={ang:6.3f} scale={scale:7.0e} "
                  f"norm(tiny)={math.sqrt(sum(c*c for c in normalize(tiny))):.6f} "
                  f"|ang_ref-a|={dev:.6e} {flag}")

# also: DR-style axis *scaling* (not tiny, but non-unit magnitude) — does
# normalize() absorb it exactly? (magnitude 0.001 .. 1000)
print("\nDR axis magnitude sweep (same direction, non-unit magnitude):")
for name, ax in AXES.items():
    for mag in (1e-6, 1e-3, 1.0, 1e3, 1e6):
        scaled = [c * mag for c in ax]
        d = maxabs([[-a + b for a, b in zip(r1, r2)]
                    for r1, r2 in zip(axis_angle_rot(scaled, 1.0),
                                      axis_angle_rot(ax, 1.0))])
        print(f"{name} mag={mag:7.0e} max|dR|={d:.3e}")

print(f"\nSUMMARY: underflow-deviation cases = {fails}")
