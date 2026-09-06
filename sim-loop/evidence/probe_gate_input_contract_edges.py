#!/usr/bin/env python3
"""probe_gate_input_contract_edges.py — H15: gate の allowed-set に非 set コレクション
(vector / list / sorted-set / lazy-seq / 文字列 / 非キーワード要素混在 set) を渡して
も例外なく (または安全側に) 動作し、tau 1e6 payload は一切照合されないか。
さらに governor 層 (kaigo-action / ops-action / :emit :safety-critical) と
id・mission-id の型エッジでも decision が payload 無相関か — falsify-012
(allowed-set nil/空/set 3 種のみ) の入力空間を allowed-set 契約面 + governor 層に拡張。

測定のみ。コード修正なし。clojure -M -e で kotoba.robotics を require し列挙。

再現:
  cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
  python3 sim-loop/evidence/probe_gate_input_contract_edges.py > /tmp/h15.clj
  clojure -M -e "$(cat /tmp/h15.clj)" > /tmp/h15.txt 2>&1
  clojure -M -e "$(cat /tmp/h15.clj)" > /tmp/h15b.txt 2>&1
  diff /tmp/h15.txt /tmp/h15b.txt   # clojure 出力本体 0 行差 (決定的)
"""
CLOJURE = r'''
(require '[kotoba.robotics :as rob]
         '[kotoba.giemon.governor :as gov])

(println "RESULT-BEGIN")
(def n (atom 0))
(def variants (atom 0))

(def tau-params {:joints {"j2" {:tau 1.0E6}}})
(def clean-params {:joints {"j2" {:tau 0.0}}})

(defn gate-decision [action aset]
  (try (:gate/decision (rob/gate action aset))
       (catch Exception e (str "threw:" (.getMessage e)))))

;; Part 1: allowed-set non-set / mixed-type collections (tau 1e6 payload)
(def aset-variants
  {"vector"        [:low]
   "list"          (list :low :medium)
   "sorted-set"    (sorted-set :low)
   "lazy-seq"      (map identity [:low :medium])
   "string"        ":low"
   "kw-as-elem"    #{:low}
   "mixed-set"     #{:low "low" 1}
   "set-with-high" #{:high}
   "seq-of-vect"   (seq [[:low]])})

(doseq [[aname aset] aset-variants]
  (let [a  (rob/action "p1" "m1" :move :low :params tau-params)
        r  (gate-decision a aset)
        a2 (rob/action "p1" "m1" :move :low :params tau-params)
        r2 (gate-decision a2 aset)]
    (swap! n inc)
    (println "ASET" aname "->" (pr-str r))
    (when (not= r r2) (swap! variants inc))))

;; Part 2: governor layer — kaigo/ops/safety-critical paths, payload vs decision
;; 2a: kaigo-action unknown product fallback + payload invariance
(doseq [[pname product] {"known-caterpillar" :caterpillar
                         "unknown-bogus"    :bogus}
        [sname params] {"tau1e6" tau-params "tau0" clean-params}]
  (let [a  (gov/kaigo-action (str "p2a-" pname "-" sname) "m1" product :move
                             :safety :low :params params)
        r  (gate-decision a #{:low :medium})
        a2 (gov/kaigo-action (str "p2a-" pname "-" sname) "m1" product :move
                             :safety :low :params params)
        r2 (gate-decision a2 #{:low :medium})]
    (swap! n inc)
    (println "GOV-KAIGO" pname sname "->" (pr-str r))
    (when (not= r r2) (swap! variants inc))))

;; 2b: ops-action :caterpillar default :high vs kaigo :low for same product
(let [ak  (gov/kaigo-action "p2b-kaigo" "m1" :caterpillar :move
                            :params tau-params)
      ao  (gov/ops-action "p2b-ops" "m1" :caterpillar :move
                          :params tau-params)]
  (swap! n inc)
  (println "GOV-DEFAULT-SAFETY kaigo:" (pr-str (:action/safety ak))
           "ops:" (pr-str (:action/safety ao))
           "| gate(#{:low :medium}) kaigo:" (pr-str (gate-decision ak #{:low :medium}))
           "ops:" (pr-str (gate-decision ao #{:low :medium}))))

;; 2c: safety-critical :emit escalation with tau 1e6 — must not be :permit
(let [a  (gov/fall-detected-alert "p2c" "m1" :params tau-params)
      r  (gate-decision a #{:low :medium :high})
      a2 (gov/chemical-dispense-alert "p2c-chem" "m1" :params tau-params)
      r2 (gate-decision a2 #{:low :medium :high})]
  (swap! n inc)
  (println "GOV-SAFETY-CRITICAL fall:" (pr-str r) "chem:" (pr-str r2)
           "| payload-carried:" (pr-str (= tau-params (:action/params a)))))

;; Part 3: id / mission-id type edges with tau payload
(doseq [[iname id mid] [["normal-str"      "p3" "m1"]
                        ["nil-id"          nil "m1"]
                        ["numeric-id"      42  "m1"]
                        ["keyword-id"      :p3 "m1"]
                        ["nil-mission"     "p3" nil]
                        ["numeric-mission" "p3" 99]]]
  (let [a  (try (rob/action id mid :move :low :params tau-params)
                (catch Exception e ::bad))
        r  (if (= ::bad a) ::bad (gate-decision a #{:low :medium}))
        a2 (try (rob/action id mid :move :low :params tau-params)
                (catch Exception e ::bad))
        r2 (if (= ::bad a2) ::bad (gate-decision a2 #{:low :medium}))]
    (swap! n inc)
    (println "ID-EDGE" iname "->" (pr-str r))
    (when (not= r r2) (swap! variants inc))))

(println "GATE-CONTRACT-CASES" @n)
(println "GATE-CONTRACT-DETERMINISM-FAILS" @variants)
'''
print(CLOJURE)
