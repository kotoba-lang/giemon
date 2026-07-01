(ns kotoba.giemon.arm
  "Giemon articulated-arm contract — forward kinematics and torque
  validation over an `:arm/chain` EDN spec (e.g. `fixtures/giemon_arm6`).

  Pure data in, pure data out: no network, no I/O — callers read/parse the
  EDN fixture themselves and pass the resulting map in. Mirrors the
  fixture's own header comment: joint design requirement
  (`:joint/limit :effort`) and assigned actuator rating
  (`:joint/actuator :cont-nm`) live at the same place, so torque validation
  reads from a single source instead of a second BOM list."
  (:require [kotoba.giemon.kinematics :as k]))

(defn joint-count [arm] (count (:arm/chain arm)))

(defn within-limits?
  "True when `angle` (radians) is within joint `joint`'s declared
  `:joint/limit` lower/upper bounds."
  [joint angle]
  (let [{:keys [lower upper]} (:joint/limit joint)]
    (and (some? lower) (some? upper) (<= lower angle upper))))

(defn forward-kinematics
  "Given an `arm` spec (`:arm/chain`, a base-first vector of joints) and a
  seq of joint `angles` (radians, one per chain entry), return a vector of
  world-frame transforms — one per joint/child-link, in chain order.

  This is pure kinematics, not the safety gate: an angle outside a joint's
  declared limit still produces a pose. Check `within-limits?` first if
  that matters to the caller."
  [arm angles]
  (loop [chain (:arm/chain arm)
         angles (seq angles)
         parent k/identity-transform
         acc []]
    (if (empty? chain)
      acc
      (let [joint (first chain)
            angle (or (first angles) 0.0)
            local (k/joint-transform (:joint/origin joint) (:joint/axis joint) angle)
            world (k/combine parent local)]
        (recur (rest chain) (rest angles) world (conj acc world))))))

(defn end-effector
  "The final link's world-frame transform."
  [arm angles]
  (last (forward-kinematics arm angles)))

(defn torque-headroom
  "For each joint, the margin (N·m) between its declared design
  requirement (`:joint/limit :effort`) and its assigned actuator's
  continuous rating (`:joint/actuator :cont-nm`). Negative means the
  assigned actuator is under-rated for the joint's design requirement."
  [arm]
  (for [joint (:arm/chain arm)]
    {:joint/name (:joint/name joint)
     :torque/required (get-in joint [:joint/limit :effort])
     :torque/rated (get-in joint [:joint/actuator :cont-nm])
     :torque/headroom (- (get-in joint [:joint/actuator :cont-nm])
                          (get-in joint [:joint/limit :effort]))}))

(defn underrated-joints
  "Joints whose assigned actuator's continuous torque rating falls below
  the joint's design requirement."
  [arm]
  (filter #(neg? (:torque/headroom %)) (torque-headroom arm)))
