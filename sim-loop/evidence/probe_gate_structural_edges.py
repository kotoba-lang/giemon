#!/usr/bin/env python3
"""probe_gate_structural_edges.py — H14: gate はアクション自体の構造エッジ
(params 非 map / nil / 深入れし構造に隠した torque / safety の型違反 /
未知 kind / allowed-set nil・空) でも decision が payload と同様に無相関で、
どこにも torque 照合が存在しない — falsify-011 (:joints map) の入力空間を
アクション構造面に拡張測定 (maturity.md NEXT (c) の継続)。

測定のみ。コード修正なし。kbb -M -e で kotoba.robotics を require し列挙。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_gate_structural_edges.py > /tmp/h14.clj
  kbb -M -e "$(cat /tmp/h14.clj)" > /tmp/h14.txt 2>&1
  kbb -M -e "$(cat /tmp/h14.clj)" > /tmp/h14b.txt 2>&1
  cmp /tmp/h14.txt /tmp/h14b.txt   # exit 0 (決定的)
"""
CLOJURE = r'''
(require '[kotoba.robotics :as rob])

(println "RESULT-BEGIN")
(def gate-variants (atom 0))
(def n (atom 0))

(def structural-params
  {"nil-params"            nil
   "vector-params"         [{:joints {"j2" {:tau 1.0E6}}}]
   "string-params"         "{:joints {:tau 1.0E6}}"
   "kw-params"             :torque
   "deep-nested-tau"       {:a {:b {:c {:d {:joints {"j2" {:tau 1.0E6}}}}}}}
   "tau-top-level"         {:tau 1.0E6}
   "huge-map"              (into {} (map (fn [i] [(keyword (str "k" i)) 1.0E6])
                                         (range 200)))
   "embedded-fn-shape"     {:joints {"j2" {:tau 1.0E6 :extra {:x 1}}}}})

;; Part 1: structural param edges x kinds x safety
(doseq [kind [:move :actuate :grasp]
        safety [:low :medium :high]
        [pname params] structural-params]
  (let [a (try (rob/action (str "p1-" kind "-" (name safety) "-" pname)
                           "m1" kind safety :params params)
               (catch Exception e ::bad-action))
        res (if (= ::bad-action a)
              ::bad-action
              (try (:gate/decision (rob/gate a #{:low :medium}))
                   (catch Exception e (str "gate-threw:" (.getMessage e)))))]
    (swap! n inc)
    (println "STRUCT" (name kind) (name safety) pname "->" (pr-str res))
    (when (and (map? a) (not= res ::bad-action))
      (let [a2 (rob/action (str "p1-" kind "-" (name safety) "-" pname)
                           "m1" kind safety :params params)
            d2 (try (:gate/decision (rob/gate a2 #{:low :medium}))
                    (catch Exception e ::thr2))]
        (when (not= res d2) (swap! gate-variants inc))))))

;; Part 2: safety / kind / mission type violations (params constant torque payload)
(def tau-params {:joints {"j2" {:tau 1.0E6}}})
(doseq [safety ["low" nil :bogus 1.0]
        kind [:move :fly "move" nil]
        mission ["m1" nil :m1 42]]
  (let [r (try (let [a (rob/action "p2" mission kind safety :params tau-params)]
                 (:gate/decision (rob/gate a #{:low :medium})))
               (catch Exception e (str "threw:" (.getMessage e))))]
    (swap! n inc)
    (println "TYPE-EDGE" (pr-str safety) (pr-str kind) (pr-str mission) "->" (pr-str r))))

;; Part 3: allowed-set edges (nil / empty / superset) with tau payload
(doseq [[sname aset] {"nil-set" nil "empty-set" #{} "single-low" #{:low}
                      "with-high" #{:low :medium :high}}]
  (let [r (try (let [a (rob/action "p3" "m1" :move :low :params tau-params)]
                 (:gate/decision (rob/gate a aset)))
               (catch Exception e (str "threw:" (.getMessage e))))]
    (swap! n inc)
    (println "ALLOWED-SET" sname "->" (pr-str r))))

(println "STRUCT-GATE-CASES" @n)
(println "STRUCT-GATE-DETERMINISM-FAILS" @gate-variants)
'''
print(CLOJURE)
