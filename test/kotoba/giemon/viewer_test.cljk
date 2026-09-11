(ns kotoba.giemon.viewer-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.viewer :as viewer]))

(def two-joint-arm
  {:arm/chain
   [{:joint/name "j1" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 0.0 1.0]}
    {:joint/name "j2" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 1.0 0.0]}]})

(deftest arm-scene-ir-test
  (testing "one scene instance per chain link, in order"
    (let [ir (viewer/arm-scene-ir two-joint-arm [0.0 0.0])]
      (is (= :arm (:scene/model ir)))
      (is (= 2 (count (:scene/instances ir))))
      (is (= "link1" (:instance/link (first (:scene/instances ir)))))
      (is (= [0.0 0.0 2.0] (:instance/pos (last (:scene/instances ir))))))))

(deftest product-scene-ir-test
  (testing "stub scene for an in-design product has one origin instance"
    (let [ir (viewer/product-scene-ir :hitogata)]
      (is (= :hitogata (:scene/model ir)))
      (is (= 1 (count (:scene/instances ir))))
      (is (= [0.0 0.0 0.0] (:instance/pos (first (:scene/instances ir))))))))
