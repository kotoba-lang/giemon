#!/usr/bin/env python3
"""probe_gate_permit_surface.py — H17: gate :permit の下流消費面は
payload (torque) と mission 境界 (:mission/boundaries, :mission/max-steps)
に無相関か — maturity NEXT の残り深掘り候補 1 つを測定。

測定のみ。コード修正なし。kbb -M -e で kotoba.robotics を require し列挙。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_gate_permit_surface.py > /tmp/h17.clj
  kbb -M -e "$(cat /tmp/h17.clj)" > /tmp/h17.txt 2>&1
  kbb -M -e "$(cat /tmp/h17.clj)" > /tmp/h17b.txt 2>&1
  diff /tmp/h17.txt /tmp/h17b.txt   # clojure 出力本体 0 行差 (決定的)
"""
CLOJURE = r'''
(require '[clojure.string :as cstr])
(require '[kotoba.robotics :as rob])

(println "RESULT-BEGIN")
(def n (atom 0))
(def variants (atom 0))

(def clean-params {:joints {"j2" {:tau 0.0}}})

;; Part A: gate 返却レコードのキー集合は payload に依存しないか
(def recs (atom []))
(doseq [[vname params] {"clean"     clean-params
                        "tau-1e6"   {:joints {"j2" {:tau 1.0E6}}}
                        "tau-neg"   {:joints {"j2" {:tau -1.0E6}}}
                        "str-1e6"   {:joints {"j2" {:tau "1e6"}}}
                        "effort"    {:joints {"j2" {:effort 1.0E6}}}}]
  (let [a (rob/action "pA" "m1" :move :low :params params)
        r (rob/gate a #{:low :medium})]
    (swap! n inc)
    (swap! recs conj (vec (sort (keys r))))
    (println "A" vname "keys:" (pr-str (vec (sort (keys r))))
             "rec:" (pr-str r)
             "rec-contains-tau:" (pr-str (cstr/includes? (pr-str r) "tau")))))
(println "A key-sets-identical-across-payloads:"
         (pr-str (apply = @recs)))

;; Part B: :mission/boundaries と :mission/max-steps は gate に届くか
;; (mission を tight 側と loose 側の 2 通りで作り、同一 params の action で gate)
(let [mb (rob/mission "mB" "caterpillar" "patrol"
                      :boundaries {:max-velocity 0.1 :geo-fence :home}
                      :max-steps 3)
      ml (rob/mission "mB2" "caterpillar" "patrol"
                      :boundaries {:max-velocity 1.0E6 :geo-fence :none}
                      :max-steps 1.0E6)
      ab (rob/action "pB" "mB" :move :low :params {:joints {"j2" {:velocity 1.0E6}}})
      al (rob/action "pB" "mB2" :move :low :params {:joints {"j2" {:velocity 1.0E6}}})
      rb (rob/gate ab #{:low :medium})
      rl (rob/gate al #{:low :medium})]
  (swap! n inc)
  (println "B tight-boundary-gate:" (pr-str rb))
  (println "B loose-boundary-gate:" (pr-str rl))
  (println "B boundary-decisions-differ:" (pr-str (not= (:gate/decision rb) (:gate/decision rl))))
  (println "B gate-references-boundaries:"
           (pr-str (cstr/includes? (pr-str rb) "boundar")))
  (println "B gate-references-max-steps:"
           (pr-str (cstr/includes? (pr-str rb) "step"))))

;; Part C: action-permitted? boolean は payload に無相関か
(let [results (for [[vname params] {"clean"   clean-params
                                    "tau-1e6" {:joints {"j2" {:tau 1.0E6}}}
                                    "v-1e6"   {:joints {"j2" {:velocity 1.0E6}}}
                                    "kind-actuate" {:joints {"j2" {:tau 1.0E6}}}}]
                 [vname (rob/action-permitted?
                          (rob/action "pC" "m1"
                                      (if (= vname "kind-actuate") :actuate :move)
                                      :low :params params)
                          #{:low :medium})])]
  (swap! n inc)
  (println "C permitted results:" (pr-str (into {} results)))
  (println "C permitted-all-equal:" (pr-str (apply = (map second results)))))

;; Part D: require-sign-off 経路の返却面も payload 無相関か (high クラス)
(doseq [[vname params] {"clean"   clean-params
                        "tau-1e6" {:joints {"j2" {:tau 1.0E6}}}
                        "str"     {:joints {"j2" {:tau "1e6"}}}}]
  (let [a (rob/action "pD" "m1" :actuate :high :params params)
        r (rob/gate a #{:low :medium :high})]
    (swap! n inc)
    (println "D" vname "->" (pr-str r)
             "payload-in-rec:" (pr-str (cstr/includes? (pr-str r) "1e6")))))

;; Part E: invalid 経路 (nil action) も payload 無相関
(let [r1 (rob/gate nil #{:low})
      r2 (rob/gate {} #{:low})]
  (swap! n inc)
  (println "E nil-action:" (pr-str r1) "empty-map:" (pr-str r2)))

(println "PERMIT-SURFACE-CASES" @n)
(println "PERMIT-SURFACE-DETERMINISM-FAILS" @variants)
'''
print(CLOJURE)
