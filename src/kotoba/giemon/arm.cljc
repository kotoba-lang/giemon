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

(defn chain-actuators
  "The default (`:all-qdd`) actuator BOM: the actuators inlined on
  `:arm/chain` (`:joint/actuator`), one entry per joint that has one.
  This *is* the default BOM — ported from `kami-articulated-scene`'s
  `chain_actuators_from_edn`/`default_bom_from_edn`, which are the same
  function under two names because there is no separate `:bom` list to
  keep in sync (single source of truth, per the fixture's own header
  comment)."
  [arm]
  (into []
        (keep (fn [joint]
                (when-let [a (:joint/actuator joint)]
                  {:joint (:joint/name joint)
                   :model (:model a)
                   :cont-nm (:cont-nm a)
                   :peak-nm (:peak-nm a)})))
        (:arm/chain arm)))

(defn bom
  "The actuator BOM for a named `variant` of `arm`'s `:arm/realization`.

  The base is `chain-actuators`. `arm`'s `:arm/realization :default`
  variant returns it unchanged; any other named variant applies that
  variant's `:arm/realization :variants <variant> :override` (a
  `{joint-name actuator}` map, joint names as strings) on top, replacing
  the matching joint's actuator or appending it if the joint wasn't
  already in the base BOM. Returns nil for a variant that is neither the
  default nor present under `:variants` (ported from
  `kami-articulated-scene`'s `bom_from_edn`)."
  [arm variant]
  (let [real (:arm/realization arm)
        base (chain-actuators arm)]
    (when real
      (if (= variant (:default real))
        base
        (when-let [override (get-in real [:variants variant :override])]
          (reduce-kv
            (fn [acc joint-name actuator]
              (let [choice {:joint joint-name
                            :model (:model actuator)
                            :cont-nm (:cont-nm actuator)
                            :peak-nm (:peak-nm actuator)}
                    idx (first (keep-indexed #(when (= (:joint %2) joint-name) %1) acc))]
                (if idx (assoc acc idx choice) (conj acc choice))))
            base
            override))))))

(defn torque-headroom
  "For each joint that has an actuator in `actuators` (default: `arm`'s
  inline chain actuators, i.e. the `:all-qdd` default BOM — pass the
  result of `bom` to validate a named `:arm/realization` variant
  instead), the margin (N·m) between the joint's declared design
  requirement (`:joint/limit :effort`) and that actuator's continuous
  rating (`:cont-nm`). Negative means the assigned actuator is
  under-rated for the joint's design requirement."
  ([arm] (torque-headroom arm (chain-actuators arm)))
  ([arm actuators]
   (let [by-joint (into {} (map (juxt :joint identity)) actuators)]
     (for [joint (:arm/chain arm)
           :let [jname (:joint/name joint)
                 a (get by-joint jname)]
           :when a]
       {:joint/name jname
        :torque/required (get-in joint [:joint/limit :effort])
        :torque/rated (:cont-nm a)
        :torque/headroom (- (:cont-nm a) (get-in joint [:joint/limit :effort]))}))))

(defn underrated-joints
  "Joints whose assigned actuator's continuous torque rating falls below
  the joint's design requirement, for `actuators` (default: the
  `:all-qdd` default BOM)."
  ([arm] (underrated-joints arm (chain-actuators arm)))
  ([arm actuators]
   (filter #(neg? (:torque/headroom %)) (torque-headroom arm actuators))))
