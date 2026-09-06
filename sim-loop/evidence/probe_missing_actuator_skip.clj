;; falsify-019 probe — H21: missing-actuator joint is silently skipped by
;; torque-headroom / underrated-joints (false-pass surface).
;; Read-only: calls kotoba.giemon.arm against in-memory EDN, no code changes.
(require '[kotoba.giemon.arm :as arm])

(defn base-joint [nm effort cont-nm]
  {:joint/name nm
   :joint/type :revolute
   :joint/axis [0 0 1]
   :joint/origin [0 0 0.1]
   :joint/limit {:lower -2.0 :upper 2.0 :effort effort}
   :joint/actuator (when cont-nm {:model "M" :cont-nm cont-nm :peak-nm 100})})

;; (a) j2 has NO :joint/actuator at all (chain rebuild / importer drop path)
(def arm-missing-actuator
  {:arm/chain [(base-joint "j1" 40 40)
               (dissoc (base-joint "j2" 40 40) :joint/actuator)
               (base-joint "j3" 30 40)]})

;; (b) j2 actuator present but the whole actuator map nil-able fields: cont-nm nil
(def arm-nil-contnm
  {:arm/chain [(base-joint "j1" 40 40)
               (assoc-in (base-joint "j2" 40 40) [:joint/actuator :cont-nm] nil)
               (base-joint "j3" 30 40)]})

;; (c) baseline: all actuators present, one under-rated (control)
(def arm-control
  {:arm/chain [(base-joint "j1" 40 40)
               (base-joint "j2" 40 10)
               (base-joint "j3" 30 40)]})

(defn rep [label]
  (println "=== " label)
  (println "headroom:" (pr-str (arm/torque-headroom arm-missing-actuator)))
  (println "underrated:" (pr-str (arm/underrated-joints arm-missing-actuator))))

(println "--- (a) missing actuator on j2 (no effort violation elsewhere)")
(rep "a")
(println "rows returned for (a):" (count (arm/torque-headroom arm-missing-actuator))
         "chain joints:" (arm/joint-count arm-missing-actuator))

(println "--- (a2) missing actuator AND that joint is the under-rated one")
(def arm-missing-weakest
  {:arm/chain [(base-joint "j1" 40 40)
               (dissoc (base-joint "j2" 60 10) :joint/actuator)
               (base-joint "j3" 30 40)]})
(println "underrated:" (pr-str (arm/underrated-joints arm-missing-weakest)))

(println "--- (b) cont-nm nil on j2 (loud or silent?)")
(try
  (println "headroom:" (pr-str (arm/torque-headroom arm-nil-contnm)))
  (println "VERDICT(b): silent, no exception")
  (catch Exception e
    (println "VERDICT(b): throws:" (.getSimpleName (class e)) "-" (.getMessage e))))

(println "--- (c) control: under-rated j2 is detected")
(println "underrated:" (pr-str (arm/underrated-joints arm-control)))

(println "--- (d) bom with no :arm/realization at all")
(try
  (println "bom:" (pr-str (arm/bom arm-missing-actuator :all-qdd)))
  (catch Exception e
    (println "bom throws:" (.getSimpleName (class e)))))
(println "DONE")
