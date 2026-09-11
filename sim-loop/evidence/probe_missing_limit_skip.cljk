;; falsify-020 probe — H22: joint with missing :joint/limit :effort in
;; torque-headroom / underrated-joints (false-pass surface #3).
;; Read-only: calls kotoba.giemon.arm / export / ui against in-memory EDN,
;; no code changes.
(require '[kotoba.giemon.arm :as arm])

(defn base-joint [nm effort cont-nm]
  {:joint/name nm
   :joint/type :revolute
   :joint/axis [0 0 1]
   :joint/origin [0 0 0.1]
   :joint/limit {:lower -2.0 :upper 2.0 :effort effort}
   :joint/actuator (when cont-nm {:model "M" :cont-nm cont-nm :peak-nm 100})})

(defn probe [label f]
  (print "--- " label " => ")
  (try
    (println (pr-str (f)))
    (catch Exception e
      (println "THROWS:" (.getSimpleName (class e)) "-" (.getMessage e)))))

;; (a) j2 actuator present but :joint/limit has NO :effort key (only lower/upper)
(def arm-no-effort
  {:arm/chain [(base-joint "j1" 40 40)
               (update (base-joint "j2" 40 40) :joint/limit dissoc :effort)
               (base-joint "j3" 30 40)]})

;; (b) j2 :joint/limit ENTIRELY missing (actuator still present)
(def arm-no-limit
  {:arm/chain [(base-joint "j1" 40 40)
               (dissoc (base-joint "j2" 40 40) :joint/limit)
               (base-joint "j3" 30 40)]})

;; (c) j2 effort explicitly nil (present key, nil value)
(def arm-effort-nil
  {:arm/chain [(base-joint "j1" 40 40)
               (assoc-in (base-joint "j2" 40 40) [:joint/limit :effort] nil)
               (base-joint "j3" 30 40)]})

;; (d) control: full valid fixture (under-rated j2 40 vs 10)
(def arm-control
  {:arm/chain [(base-joint "j1" 40 40)
               (base-joint "j2" 40 10)
               (base-joint "j3" 30 40)]})

(println "H22 — :joint/limit 欠落面 probe (falsify-020)")
(println "chain joint-count:" (arm/joint-count arm-no-effort))
(println)
(probe "(a) j2 limit {lower upper} NO :effort  [headroom]" #(arm/torque-headroom arm-no-effort))
(probe "(a) underrated" #(arm/underrated-joints arm-no-effort))
(probe "(a) joint-count vs headroom rows"
       #(vector (arm/joint-count arm-no-effort) (count (arm/torque-headroom arm-no-effort))))
(println)
(probe "(b) j2   NO :joint/limit  [headroom]" #(arm/torque-headroom arm-no-limit))
(probe "(b) underrated" #(arm/underrated-joints arm-no-limit))
(println)
(probe "(c) j2   :effort nil  [headroom]" #(arm/torque-headroom arm-effort-nil))
(probe "(c) underrated" #(arm/underrated-joints arm-effort-nil))
(println)
(probe "(d) control underrated (expect j2 row)" #(arm/underrated-joints arm-control))
(println)
(probe "(e) within-limits? on no-limit j2 at 0.0" #(arm/within-limits? (second (:arm/chain arm-no-limit)) 0.0))
(probe "(e) within-limits? on no-effort j2 at 0.0" #(arm/within-limits? (second (:arm/chain arm-no-effort)) 0.0))
(println)
(probe "(f) bom (all-qdd) on no-limit arm" #(arm/bom arm-no-limit :all-qdd))
(println)
(require '[kotoba.giemon.export :as export])
(require '[kotoba.giemon.ui :as ui])
(probe "(g) export torque->csv on no-effort arm" #(export/torque->csv arm-no-effort))
(probe "(g) export torque->json on no-effort arm" #(export/torque->json arm-no-effort))
(probe "(g) ui torque-table on no-effort arm" #(ui/torque-table arm-no-effort))
(println "DONE")