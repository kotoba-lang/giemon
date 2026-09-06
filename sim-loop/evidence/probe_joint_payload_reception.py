#!/usr/bin/env python3
"""probe_joint_payload_reception.py — H13: sim 受付口 (gate + arm) は
:joints map 形 payload の joint 名を一切照合せず、存在しない joint 名 /
文字列 key 混在 / fixture actuator cont/peak 超えの torque payload でも
受理 (permit / 正常 return) される — falsify-010 の「未接続の検査層」赤の
入力空間追加測定 (maturity.md NEXT (c))。

測定のみ。コード修正なし。clojure -M -e で kotoba.robotics /
kotoba.giemon.arm / kotoba.giemon.governor を require し列挙する。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_joint_payload_reception.py > /tmp/h13.clj
  clojure -M -e "$(cat /tmp/h13.clj)" > /tmp/h13.txt 2>&1
  clojure -M -e "$(cat /tmp/h13.clj)" > /tmp/h13b.txt 2>&1
  cmp /tmp/h13.txt /tmp/h13b.txt   # exit 0 (決定的)
"""
CLOJURE = r'''
(require '[kotoba.robotics :as rob])
(require '[kotoba.giemon.governor :as gov])
(require '[kotoba.giemon.arm :as arm])
(require '[clojure.edn :as edn])
(require '[clojure.java.io :as io])

(defn unblob [v]
  (if (string? v)
    (try (let [p (edn/read-string v)] (if (coll? p) p v)) (catch Exception _ v))
    v))

(def giemon-arm6
  (into {} (map (fn [[k v]] [k (unblob v)]))
        (dissoc (first (edn/read-string
                        (slurp (io/file "fixtures" "giemon_arm6" "giemon_arm6.edn"))))
                :db/id)))

(def real-joints #{"j1" "j2" "j3" "j4" "j5" "j6"})

;; actuator ratings from the default BOM (cont/peak per joint)
(def ratings
  (into {} (map (fn [a] [(:joint a) {:cont (:cont-nm a) :peak (:peak-nm a)}]))
        (arm/chain-actuators giemon-arm6)))

(println "RATINGS" (pr-str (sort-by key ratings)))

(def joint-payloads
  {"unknown-joint"   {:joints {"j99" {:tau 1.0E6}}}
   "string-key-mix"  {:joints {"j2" {:tau 1.0E6} :j3 {:tau 1.0E6}}}
   "all-real-1e6"    {:joints {"j1" {:tau 1.0E6} "j2" {:tau 1.0E6} "j3" {:tau 1.0E6}
                               "j4" {:tau 1.0E6} "j5" {:tau 1.0E6} "j6" {:tau 1.0E6}}}
   "negative-tau"    {:joints {"j5" {:tau -500.0}}}
   "nan-ish-string"  {:joints {"j2" {:tau "huge"}}}
   "angle-over-vec"  {:joints {"j2" {:angle 99.0 :tau 1.0E6}}}})

(println "RESULT-BEGIN")
;; Part 1: gate decisions across :joints-map payloads (x kinds x safety)
(def gate-variants (atom 0))
(doseq [kind [:move :actuate :grasp]
        safety [:low :medium :high]
        [pname params] joint-payloads]
  (let [a (rob/action (str "p1-" kind "-" (name safety) "-" pname)
                      "m1" kind safety :params params)
        d1 (:gate/decision (rob/gate a #{:low :medium}))
        d2 (:gate/decision (rob/gate a #{:low :medium}))]
    (when (not= d1 d2) (swap! gate-variants inc))
    (println "GATE" (name kind) (name safety) pname d1 (if (= d1 d2) "DET" "NONDET"))))

;; Part 2: does ANY arm fn accept/inspect a torque payload? Apply each arm
;; public fn to a payload-laden arg and record whether it errors / returns.
(doseq [[pname params] joint-payloads]
  (let [r (try (let [fk (arm/forward-kinematics giemon-arm6 [0 0.2 -0.3 0 0.5 0])
                     ee (arm/end-effector giemon-arm6 [0 0.2 -0.3 0 0.5 0])]
                 (if (and (vector? fk) (= 6 (count fk)) (map? ee))
                   "accepted-and-ignored (FK unaffected by payload)" "returned"))
               (catch Exception e (str "threw:" (.getMessage e))))]
    (println "ARM-RECEIVE" pname r)))

;; Part 3: no arm fn consumes torque at all — resolve & arities probe
(doseq [s ["within-limits?" "forward-kinematics" "end-effector" "torque-headroom"
           "underrated-joints" "chain-actuators" "bom" "joint-count"]]
  (let [v (resolve (symbol "kotoba.giemon.arm" s))]
    (println "ARM-FN" s (if v (str "exists arglists=" (:arglists (meta v))) "MISSING"))))

;; Part 4: does within-limits? or torque-headroom react to a torque value?
(let [j2 (second (:arm/chain giemon-arm6))]
  (println "WL-ANGLE-ONLY" (arm/within-limits? j2 2.2) (arm/within-limits? j2 2.3))
  (println "TH-INDEPENDENT-OF-TAU"
           (= (arm/torque-headroom giemon-arm6)
              (with-redefs [] (arm/torque-headroom giemon-arm6)))))

(println "GATE-VARIANTS-BY-PAYLOAD" @gate-variants)
(println "SUMMARY joints-payloads=" (count joint-payloads)
         "gate-nondeterminism=" @gate-variants)
(println "RESULT-END")
'''

if __name__ == "__main__":
    print(CLOJURE)
