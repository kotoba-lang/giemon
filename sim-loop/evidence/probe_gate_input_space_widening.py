#!/usr/bin/env python3
"""probe_gate_input_space_widening.py — H16: gate/arm 受付口の torque 無検査は、
これまで未測定の入力空間 (文字列化 torque / 別名キー torque-Nm-effort /
mission メタデータ経由 / バッチアクション内の 1 極端 torque) でも
決定的に不変か — falsify-014 (ENV-BLOCKED, inconclusive) の再試行。

測定のみ。コード修正なし。kbb -M -e で kotoba.robotics を require し列挙。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_gate_input_space_widening.py > /tmp/h16.clj
  kbb -M -e "$(cat /tmp/h16.clj)" > /tmp/h16.txt 2>&1
  kbb -M -e "$(cat /tmp/h16.clj)" > /tmp/h16b.txt 2>&1
  diff /tmp/h16.txt /tmp/h16b.txt   # clojure 出力本体 0 行差 (決定的)
"""
CLOJURE = r'''
(require '[kotoba.robotics :as rob])

(println "RESULT-BEGIN")
(def n (atom 0))
(def variants (atom 0))

(defn gate-decision [action aset]
  (try (:gate/decision (rob/gate action aset))
       (catch Exception e (str "threw:" (.getMessage e)))))

(def clean-params {:joints {"j2" {:tau 0.0}}})

;; Part A: string-encoded torque in nested payloads (vs numeric 0 baseline)
(def string-variants
  {"str-120"  {:joints {"j2" {:tau "120"}}}
   "str-1e6"  {:joints {"j2" {:tau "1e6"}}}
   "nested5"  {:joints {"j2" {:a {:b {:c {:d {:tau 1.0E6}}}}}}}
   "in-vec"   {:joints {"j2" {:tau [1.0E6]}}}
   "as-kw"    {:joints {"j2" {:tau '{:tau 1.0E6}}}}})
(doseq [[vname params] string-variants]
  (let [a  (rob/action "pA" "m1" :move :low :params params)
        r  (gate-decision a #{:low :medium})
        a2 (rob/action "pA" "m1" :move :low :params params)
        r2 (gate-decision a2 #{:low :medium})
        rc (gate-decision (rob/action "pA" "m1" :move :low :params clean-params)
                          #{:low :medium})]
    (swap! n inc)
    (println "A" vname "->" (pr-str r) "baseline-clean:" (pr-str rc)
             "payload-carried:" (pr-str (= params (:action/params a))))
    (when (not= r r2) (swap! variants inc))))

;; Part B: alternate torque key aliases
(doseq [[kname params] {"torque" {:joints {"j2" {:torque 1.0E6}}}
                        "Nm"     {:joints {"j2" {:Nm 1.0E6}}}
                        "effort" {:joints {"j2" {:effort 1.0E6}}}
                        "top-level" {:torque 1.0E6 :joints {"j2" {:tau 0.0}}}}]
  (let [a (rob/action "pB" "m1" :move :low :params params)
        r (gate-decision a #{:low :medium})
        rc (gate-decision (rob/action "pB" "m1" :move :low :params clean-params)
                          #{:low :medium})]
    (swap! n inc)
    (println "B" kname "->" (pr-str r) "baseline-clean:" (pr-str rc))))

;; Part C: torque in mission metadata (mission spec vs action params)
(let [mtau  (rob/mission "m1" "caterpillar" "patrol" :metadata {:tau 1.0E6})
      m0    (rob/mission "m1" "caterpillar" "patrol" :metadata {:tau 0.0})
      amtau (rob/action "pC1" "m1" :move :low)
      rmt   (gate-decision amtau #{:low :medium})
      am0   (rob/action "pC2" "m1" :move :low)
      rm0   (gate-decision am0 #{:low :medium})]
  (swap! n inc)
  (println "C mission-meta tau1e6 mission:" (pr-str mtau))
  (println "C mission-meta gate same-mission-id actions ->" (pr-str rmt)
           "vs tau0-mission:" (pr-str rm0)
           "| mission-differs:" (pr-str (not= mtau m0))))

;; Part D: batch action list where one action carries extreme torque
(let [acts [(rob/action "pD1" "m1" :move :low :params clean-params)
            (rob/action "pD2" "m1" :move :low :params {:joints {"j2" {:tau 1.0E6}}})
            (rob/action "pD3" "m1" :move :low :params clean-params)]
      ds   (mapv #(gate-decision % #{:low :medium}) acts)
      ds2  (mapv #(gate-decision % #{:low :medium}) acts)]
  (swap! n inc)
  (println "D batch decisions:" (pr-str ds))
  (when (not= ds ds2) (swap! variants inc))
  (println "D extreme-index-decision-differs-from-clean-neighbors:"
           (pr-str (not= (nth ds 1) (nth ds 0)))))

;; Part E: safety-critical :emit must remain :deny with every exotic payload
(doseq [[ename params] {"str-1e6" {:joints {"j2" {:tau "1e6"}}}
                        "effort"  {:joints {"j2" {:effort 1.0E6}}}
                        "numeric" {:joints {"j2" {:tau 1.0E6}}}}]
  (let [a (rob/action "pE" "m1" :emit :safety-critical :params params)
        r (gate-decision a #{:low :medium :high})]
    (swap! n inc)
    (println "E" ename "->" (pr-str r))))

(println "GATE-WIDENING-CASES" @n)
(println "GATE-WIDENING-DETERMINISM-FAILS" @variants)
'''
print(CLOJURE)
