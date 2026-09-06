;; falsify-018 probe — H20: torque-headroom / bom joint-name correspondence
;; Claim under test: arm.cljc's torque-headroom / underrated-joints map each
;; chain joint to the CORRECT actuator via joint name, even when
;;   (a) two chain joints share the same :joint/name,
;;   (b) a :bom variant :override references a joint name that is duplicated,
;;   (c) an override references a name not present in the chain,
;;   (d) actuator data itself is malformed (nil cont-nm / nil effort).
;; A silent wrong pairing (headroom computed against the WRONG joint's
;; actuator/effort) would quietly flip underrated-joints verdicts — the exact
;; number the core uses to justify actuator assignment.
;; Measurement only — reads the implementation via clojure REPL, changes nothing.
;;
;; Usage: clojure -M -e "(load-file \"sim-loop/evidence/probe_bom_name_parity.clj\")"
;; (run from repo root /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon)

(require '[kotoba.giemon.arm :as arm])

(defn show [label v] (println label (pr-str v)))

;; ---- (a) duplicate joint names in the chain -------------------------------
;; j2 appears twice: first with cont-nm 40 / effort 40, second with
;; cont-nm 10 / effort 40. If pairing is by-name-with-map-collision, the
;; headroom for BOTH rows will read the LAST actuator (10) — the first
;; row's headroom would then be -30 instead of the correct 0.
(def dup-chain
  {:arm/chain
   [{:joint/name "j2" :joint/limit {:lower -2.2 :upper 2.2 :effort 40}
     :joint/actuator {:model "A" :cont-nm 40 :peak-nm 120}}
    {:joint/name "j2" :joint/limit {:lower -2.2 :upper 2.2 :effort 40}
     :joint/actuator {:model "B" :cont-nm 10 :peak-nm 30}}]})

(show "A1 chain-actuators(dup)      " (arm/chain-actuators dup-chain))
(show "A2 torque-headroom(dup)     " (arm/torque-headroom dup-chain))
(show "A3 underrated-joints(dup)   " (arm/underrated-joints dup-chain))

;; ---- (b) variant override on a duplicated name ----------------------------
;; Override replaces the FIRST index found (keep-indexed first match):
;; variant :strong assigns cont-nm 10 to "j2" — does it replace row 1, row 2,
;; or one row twice? Measure what the resulting BOM actually is.
(def dup-real
  (assoc dup-chain :arm/realization
         {:default :all-qdd
          :variants {:strong {:override {"j2" {:model "X" :cont-nm 10 :peak-nm 30}}}}}))
(show "B1 bom(dup, :strong)        " (arm/bom dup-real :strong))
(show "B2 bom(dup, :all-qdd)       " (arm/bom dup-real :all-qdd))
(show "B3 headroom(dup, :strong bom)" (arm/torque-headroom dup-chain (arm/bom dup-real :strong)))

;; ---- (c) override naming an unknown joint ---------------------------------
(def ghost-real
  {:arm/chain (vec (:arm/chain dup-chain))
   :arm/realization {:default :all-qdd
                     :variants {:weird {:override {"j99" {:model "G" :cont-nm 5 :peak-nm 8}}}}}})
(show "C1 bom(ghost :weird)        " (arm/bom ghost-real :weird))
(show "C2 headroom(chain, ghost bom)" (arm/torque-headroom (:arm/chain ghost-real)
                                                           (concat (arm/chain-actuators ghost-real)
                                                                   (drop 1 (arm/bom ghost-real :weird)))))
;; simpler: headroom with an actuator list that contains a joint not in chain
(show "C3 headroom(chain, extra-row)" (arm/torque-headroom dup-chain
                                                            (conj (arm/chain-actuators dup-chain)
                                                                  {:joint "j99" :model "G" :cont-nm 5 :peak-nm 8})))

;; ---- (d) malformed actuator data ------------------------------------------
(def nilchain
  {:arm/chain
   [{:joint/name "j1" :joint/limit {:effort 40} :joint/actuator {:model "N" :cont-nm nil :peak-nm 120}}
    {:joint/name "j2" :joint/limit {:effort nil} :joint/actuator {:model "M" :cont-nm 40 :peak-nm 30}}]})
(show "D1 headroom(nil fields)     " (try (arm/torque-headroom nilchain) (catch Exception e (str "EXC " (.getMessage e)))))
(show "D2 underrated(nil fields)   " (try (arm/underrated-joints nilchain) (catch Exception e (str "EXC " (.getMessage e)))))

(println "SUMMARY probe_bom_name_parity done")
