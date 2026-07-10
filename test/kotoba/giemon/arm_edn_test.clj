(ns kotoba.giemon.arm-edn-test
  "JVM-only: reads the actual giemon_arm6.edn fixture (not a hand-copied
  subset) so these parity tests can't silently drift from the shipped
  fixture. Mirrors kami-articulated-scene's Rust test suite
  (default_bom_meets_chain_torque / harmonic_shoulder_override_lifts_j2 /
  unknown_bom_variant_errors).

  The fixture is stored as Datomic/Datascript tx-data (a single-entity
  vector: `[{:db/id -1 :arm/name ... :arm/chain \"<pr-str blob>\" ...}]`,
  EDN-datomize fan-out): its top-level keys are already namespaced
  (`:arm/*`) so wrap-generic keeps them as-is unchanged, and non-scalar
  values (`:arm/chain`, `:arm/base`, `:arm/realization`) are pr-str'd
  blobs. `reconstitute-arm` rebuilds the original nested map that
  `kotoba.giemon.arm` expects, unchanged from before the transform."
  (:require [clojure.edn :as edn]
            [clojure.java.io :as io]
            [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.arm :as arm]))

(defn- unblob [v]
  (if (string? v)
    (try (let [parsed (edn/read-string v)] (if (coll? parsed) parsed v))
         (catch Exception _ v))
    v))

(defn- reconstitute-arm [tx-data]
  (into {} (map (fn [[k v]] [k (unblob v)]))
        (dissoc (first tx-data) :db/id)))

(def giemon-arm6
  (reconstitute-arm
   (edn/read-string (slurp (io/file "fixtures" "giemon_arm6" "giemon_arm6.edn")))))

(deftest default-bom-meets-chain-torque-test
  (testing "every chain joint has an actuator in the default BOM, no violations"
    (let [b (arm/bom giemon-arm6 :all-qdd)]
      (is (= (arm/joint-count giemon-arm6) (count b)))
      (is (empty? (arm/underrated-joints giemon-arm6 b))))))

(deftest harmonic-shoulder-override-lifts-j2-test
  (let [base (arm/bom giemon-arm6 :all-qdd)
        h (arm/bom giemon-arm6 :harmonic-shoulder)
        j2-base (first (filter #(= "j2" (:joint %)) base))
        j2-h (first (filter #(= "j2" (:joint %)) h))
        j3-base (first (filter #(= "j3" (:joint %)) base))
        j3-h (first (filter #(= "j3" (:joint %)) h))]
    (is (>= (:cont-nm j2-h) 72.0))
    (is (> (:cont-nm j2-h) (:cont-nm j2-base)))
    (testing "non-overridden joints unchanged"
      (is (= (:model j3-base) (:model j3-h))))
    (testing "override replaces, not appends"
      (is (= (count base) (count h))))))

(deftest unknown-bom-variant-test
  (is (nil? (arm/bom giemon-arm6 :no-such-variant))))
