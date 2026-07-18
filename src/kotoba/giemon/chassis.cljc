(ns kotoba.giemon.chassis
  "Giemon Caterpillar dual-track UGV chassis contract: differential
  track-drive kinematics (pure, generic — not a joint-chain solver; a
  track-drive base has no revolute joints to walk) plus a chassis-mounted
  cleaning boom that reuses `kotoba.giemon.arm`'s revolute-joint-chain
  forward-kinematics/BOM/torque-validation machinery unchanged, over a
  fixture's `:chassis/boom` sub-structure (e.g.
  `fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn`).

  Track-drive propulsion has no `torque-headroom` analogue: an arm joint's
  design requirement (`:joint/limit :effort`) is a static/quasi-static
  torque a fixed-geometry link needs to hold or move through gravity,
  computable from the chain alone. A track's required propulsion torque
  instead depends on vehicle mass, ground friction, slope and desired
  acceleration — a vehicle-dynamics computation this fixture's data does
  not attempt (see the fixture's `:chassis/realization :unresolved`).
  `:chassis/drive` only records the assigned track-motor part numbers as
  BOM data; they are not validated against a computed torque requirement
  the way boom joints are.

  Pure data in, pure data out: no network, no I/O."
  (:require [kotoba.giemon.arm :as arm]))

;; ---------------------------------------------------------------------------
;; Track-drive (differential-drive) kinematics
;; ---------------------------------------------------------------------------

(defn track-speeds->twist
  "Given `track-width` (m, centerline separation between the two tracks)
  and left/right track linear speeds (m/s, + = forward), return the
  vehicle's instantaneous body-frame twist: linear velocity (m/s,
  + = forward) and angular velocity (rad/s, + = CCW viewed from above)."
  [track-width left right]
  {:twist/linear (/ (+ left right) 2.0)
   :twist/angular (/ (- right left) track-width)})

(defn twist->track-speeds
  "Inverse of `track-speeds->twist`: the left/right track speeds (m/s)
  that produce a desired body-frame `linear` velocity (m/s) and `angular`
  velocity (rad/s) over `track-width` (m)."
  [track-width linear angular]
  (let [half (/ (* angular track-width) 2.0)]
    {:track/left (- linear half)
     :track/right (+ linear half)}))

(defn turning-radius
  "The signed turning radius (m) of the vehicle's path for `track-width`
  (m) and left/right track speeds (m/s): the distance from the
  instantaneous center of rotation to the vehicle's centerline. Returns
  nil for straight-line travel (left = right, radius at infinity) and
  0.0 for a stationary in-place pivot (left = -right)."
  [track-width left right]
  (cond
    (== left right) nil
    (zero? (+ left right)) 0.0
    :else (/ (* track-width (+ left right)) (* 2.0 (- right left)))))

(defn integrate-pose
  "Advance a 2-D `pose` (`{:pose/x :pose/y :pose/theta}`, metres/radians)
  by `dt` seconds under a constant body-frame `linear`/`angular` twist
  (unicycle model — exact for straight-line or in-place-pivot motion, a
  first-order approximation for combined-turn motion; fine-grained `dt`
  keeps the approximation error bounded, the same tradeoff any 2-D
  dead-reckoning integrator makes)."
  [pose linear angular dt]
  (let [{:keys [pose/x pose/y pose/theta]} pose]
    {:pose/x (+ x (* linear (Math/cos theta) dt))
     :pose/y (+ y (* linear (Math/sin theta) dt))
     :pose/theta (+ theta (* angular dt))}))

;; ---------------------------------------------------------------------------
;; Cleaning boom — reuses kotoba.giemon.arm unchanged
;; ---------------------------------------------------------------------------

(defn boom-arm
  "`chassis`'s `:chassis/boom` sub-structure joined with `chassis`'s
  `:chassis/realization` variant map, in the exact shape
  `kotoba.giemon.arm`'s functions expect (`:arm/chain` + `:arm/realization`
  on the same map). Single source of truth: the fixture keeps one
  `:chassis/realization` map (mirroring `giemon_arm6.edn`'s
  `:arm/realization`) instead of a second `:arm/realization` duplicate
  nested under `:chassis/boom` — this join happens here, at read time."
  [chassis]
  (assoc (:chassis/boom chassis) :arm/realization (:chassis/realization chassis)))

(defn boom-forward-kinematics
  "Forward kinematics of the cleaning boom (see `kotoba.giemon.arm/forward-kinematics`)."
  [chassis angles]
  (arm/forward-kinematics (boom-arm chassis) angles))

(defn boom-actuators
  "The boom's default actuator BOM (see `kotoba.giemon.arm/chain-actuators`)."
  [chassis]
  (arm/chain-actuators (boom-arm chassis)))

(defn boom-bom
  "The boom's actuator BOM for a named `:chassis/realization` variant
  (e.g. `:dry-brush-only` / `:wet-spray`; see `kotoba.giemon.arm/bom`)."
  [chassis variant]
  (arm/bom (boom-arm chassis) variant))

(defn boom-torque-headroom
  "Torque headroom for each boom joint (see `kotoba.giemon.arm/torque-headroom`)."
  [chassis]
  (arm/torque-headroom (boom-arm chassis)))

(defn boom-underrated-joints
  "Boom joints whose assigned actuator is under-rated for its design
  requirement (see `kotoba.giemon.arm/underrated-joints`)."
  [chassis]
  (arm/underrated-joints (boom-arm chassis)))
