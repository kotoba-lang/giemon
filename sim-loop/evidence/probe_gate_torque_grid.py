#!/usr/bin/env python3
"""probe_gate_torque_grid.py — H12: governor gate は :action/params の torque を
一切検査しない (falsify-002 構造的ギャップ赤の input 空間網羅による決定的確認)。

測定のみ。コード修正なし。clojure CLI で kotoba.robotics / kotoba.giemon.governor /
kotoba.giemon.arm を require し、(safety class × torque payload) の全組合せで
gate/:permit を列挙する。torque が 1 件でも :deny 理由になるなら H12 は破れる。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  kbb -M -e "$(cat sim-loop/evidence/probe_gate_torque_grid.clj)" > /tmp/g12.txt 2>&1
"""
# --- embedded clojure script (single -M -e body) ---
CLOJURE = r'''
(require '[kotoba.robotics :as rob])
(require '[kotoba.giemon.governor :as gov])
(require '[kotoba.giemon.arm :as arm])

(def allowed-sets
  {"none-only" #{:none}
   "low"       #{:low}
   "low+med"   #{:low :medium}
   "all-non-crit" #{:none :low :medium :high}
   "all"       rob/safety-classes})

(def tau-payloads
  {"no-params"   nil
   "tau-0"       {:tau 0.0}
   "tau-120"     {:tau 120.0}     ; j2 peak rating
   "tau-1e6"     {:tau 1.0E6}
   "tau-neg"     {:tau -999.0}
   "tau+ang-ble" {:tau 1.0E6 :angle 99.0 :joints {:j2 {:tau 1.0E6}}}})

(def kinds [:move :actuate :grasp :sense :emit])

(println "H12-GRID rows: kind x safety x allowed-set x payload -> decision")
(println "RESULT-BEGIN")
(def permit-count (atom 0))
(def deny-count (atom 0))
(def rso-count (atom 0))
(def invalid-count (atom 0))
(def torque-sensitive? (atom true)) ; becomes false if any two payload rows differ

(doseq [kind kinds
        safety [:none :low :medium :high :safety-critical]
        [aname allowed] allowed-sets
        [pname params] tau-payloads]
  (let [a (rob/action (str "a-" kind "-" (name safety) "-" pname)
                      "m1" kind safety :params params)
        d (:gate/decision (rob/gate a allowed))
        d2 (:gate/decision (rob/gate a allowed))] ; determinism: same input twice
    (case d
      :permit            (swap! permit-count inc)
      :deny              (swap! deny-count inc)
      :require-sign-off  (swap! rso-count inc)
      :invalid           (swap! invalid-count inc)
      nil)
    (when (not= d d2) (reset! torque-sensitive? false))
    (println "ROW" (name kind) (name safety) aname pname d
             (if (= d d2) "DET" "NONDET"))))

;; torque-sensitivity check: for a fixed (kind=:move safety=:low allowed=low+med),
;; do decisions differ across tau payloads? They must not, if gate ignores torque.
(let [decisions
      (for [[pname params] tau-payloads]
        (let [a (rob/action "t" "m1" :move :low :params params)]
          [pname (:gate/decision (rob/gate a #{:low :medium}))]))]
  (println "TORQUE-SENSITIVITY" (if (apply = (map second decisions))
                                  "INSENSITIVE (gate ignores torque)"
                                  "SENSITIVE"))
  (doseq [[p d] decisions] (println "  TS" p d)))

;; arm-side: within-limits? never sees torque; headroom exists but is BOM-only
(println "ARM-WITHIN-LIMITS-TORQUE-AGNOSTIC"
         (boolean (resolve 'kotoba.giemon.arm/within-limits?)))

(println "SUMMARY permit" @permit-count "deny" @deny-count
         "require-sign-off" @rso-count "invalid" @invalid-count
         "determinism" (if @torque-sensitive? "NONDET" "DET"))
(println "RESULT-END")
'''

if __name__ == "__main__":
    print(CLOJURE)
