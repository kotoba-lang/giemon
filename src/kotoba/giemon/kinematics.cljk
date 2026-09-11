(ns kotoba.giemon.kinematics
  "Pure rigid-body 3-D transform kinematics — no network, no I/O.

  A transform is `{:xf/rot <3x3 rotation matrix, row-major> :xf/pos [x y z]}`.
  Rotations are built from axis-angle pairs via Rodrigues' formula, which is
  the primitive `kotoba.giemon.arm` needs to walk a revolute-joint chain
  (each joint contributes a fixed origin offset + a rotation about its
  declared axis).")

(defn v+ [a b] (mapv + a b))
(defn v- [a b] (mapv - a b))
(defn v*s [v s] (mapv #(* % s) v))
(defn dot [a b] (reduce + (map * a b)))

(defn cross [[ax ay az] [bx by bz]]
  [(- (* ay bz) (* az by))
   (- (* az bx) (* ax bz))
   (- (* ax by) (* ay bx))])

(defn norm [v] (Math/sqrt (dot v v)))

(defn normalize
  "Unit vector in the direction of `v`. Returns `v` unchanged if it is
  (numerically) the zero vector."
  [v]
  (let [n (norm v)]
    (if (zero? n) v (v*s v (/ 1.0 n)))))

(def identity-rot [[1.0 0.0 0.0] [0.0 1.0 0.0] [0.0 0.0 1.0]])

(defn mat3-vec
  "Rotation matrix `m` applied to column vector `v`."
  [m v]
  (mapv #(dot % v) m))

(defn mat3-mul
  "Matrix product a*b for two 3x3 row-major matrices."
  [a b]
  (let [bt (apply mapv vector b)]
    (mapv (fn [arow] (mapv #(dot arow %) bt)) a)))

(defn axis-angle->rot
  "Rodrigues' rotation formula: a (not-necessarily-unit) `axis` and an
  `angle` in radians -> a 3x3 rotation matrix."
  [axis angle]
  (let [[x y z] (normalize axis)
        c (Math/cos angle) s (Math/sin angle) t (- 1.0 c)]
    [[(+ c (* t x x))       (- (* t x y) (* s z))   (+ (* t x z) (* s y))]
     [(+ (* t x y) (* s z)) (+ c (* t y y))         (- (* t y z) (* s x))]
     [(- (* t x z) (* s y)) (+ (* t y z) (* s x))   (+ c (* t z z))]]))

(defn transform [rot pos] {:xf/rot rot :xf/pos pos})

(def identity-transform (transform identity-rot [0.0 0.0 0.0]))

(defn combine
  "Compose a `parent` transform with a `child` transform expressed in the
  parent's frame: parent * child, in that order."
  [parent child]
  (transform (mat3-mul (:xf/rot parent) (:xf/rot child))
             (v+ (:xf/pos parent) (mat3-vec (:xf/rot parent) (:xf/pos child)))))

(defn joint-transform
  "The local transform contributed by a single revolute joint: a fixed
  `origin` offset followed by rotation of `angle` radians about `axis`."
  [origin axis angle]
  (transform (axis-angle->rot axis angle) origin))
