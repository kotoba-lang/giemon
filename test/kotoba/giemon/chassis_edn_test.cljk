(ns kotoba.giemon.chassis-edn-test
  "JVM-only: reads the actual giemon_caterpillar_facade.edn fixture (not a
  hand-copied subset) so these parity tests can't silently drift from the
  shipped fixture. Mirrors kotoba.giemon.arm-edn-test's pattern for
  giemon_arm6.edn.

  The fixture is stored as Datomic/Datascript tx-data (a single-entity
  vector: `[{:db/id -1 :chassis/name ... :chassis/boom \"<pr-str blob>\"
  ...}]`, EDN-datomize wrap-generic fan-out — same convention
  `giemon_arm6.edn` uses): its top-level keys are already namespaced
  (`:chassis/*`) so wrap-generic keeps them as-is unchanged, and
  non-scalar values (`:chassis/base`, `:chassis/drive`,
  `:chassis/base-geometry`, `:chassis/payload`, `:chassis/boom`,
  `:chassis/realization`, `:chassis/units`) are pr-str'd blobs.
  `reconstitute-chassis` rebuilds the original nested map that
  `kotoba.giemon.chassis` expects, unchanged from before the transform."
  (:require [clojure.edn :as edn]
            [clojure.java.io :as io]
            [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.chassis :as chassis]))

(defn- unblob [v]
  (if (string? v)
    (try (let [parsed (edn/read-string v)] (if (coll? parsed) parsed v))
         (catch Exception _ v))
    v))

(defn- reconstitute-chassis [tx-data]
  (into {} (map (fn [[k v]] [k (unblob v)]))
        (dissoc (first tx-data) :db/id)))

(def giemon-caterpillar-facade
  (reconstitute-chassis
   (edn/read-string (slurp (io/file "fixtures" "giemon_caterpillar_facade"
                                     "giemon_caterpillar_facade.edn")))))

(deftest fixture-shape-test
  (testing "top-level chassis identity"
    (is (= "giemon_caterpillar_facade" (:chassis/name giemon-caterpillar-facade)))
    (is (= :dual-track-ugv (:chassis/kind giemon-caterpillar-facade))))
  (testing "base chassis dimensions/parts cited from kami-app-giemon (23 real parts)"
    (is (= 23 (count (get-in giemon-caterpillar-facade [:chassis/base-geometry :parts])))))
  (testing "cleaning-fluid tank payload records capacity + fluid type as data"
    (let [tank (get-in giemon-caterpillar-facade [:chassis/payload :cleaning-fluid-tank])]
      (is (= 3.0 (:capacity-l tank)))
      (is (string? (:fluid-type tank))))))

(defn- arm-dof [chassis] (get-in chassis [:chassis/boom :arm/dof]))

(deftest boom-chain-shape-test
  (testing "4-joint revolute cleaning boom, base-first order"
    (is (= 4 (arm-dof giemon-caterpillar-facade)))))

(deftest boom-forward-kinematics-parity-test
  (let [xfs (chassis/boom-forward-kinematics giemon-caterpillar-facade [0.0 0.0 0.0 0.0])]
    (is (= 4 (count xfs)))
    (is (every? #(contains? % :xf/pos) xfs))))

(deftest default-variant-has-one-underrated-joint-test
  (testing "the dry-brush-only (default) BOM has exactly the documented
  j_nozzle_wrist torque shortfall (cont 2.5 < effort 3), per
  :chassis/realization :unresolved"
    (let [under (chassis/boom-underrated-joints giemon-caterpillar-facade)]
      (is (= 1 (count under)))
      (is (= "j_nozzle_wrist" (:joint/name (first under)))))))

(deftest wet-spray-override-lifts-boom-lift-test
  (let [base (chassis/boom-bom giemon-caterpillar-facade :dry-brush-only)
        wet (chassis/boom-bom giemon-caterpillar-facade :wet-spray)
        lift-base (first (filter #(= "j_boom_lift" (:joint %)) base))
        lift-wet (first (filter #(= "j_boom_lift" (:joint %)) wet))]
    (is (>= (:cont-nm lift-wet) 55.0))
    (is (> (:cont-nm lift-wet) (:cont-nm lift-base)))
    (testing "override replaces, not appends"
      (is (= (count base) (count wet))))))

(deftest unknown-boom-variant-test
  (is (nil? (chassis/boom-bom giemon-caterpillar-facade :no-such-variant))))
