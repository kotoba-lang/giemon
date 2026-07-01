(ns kotoba.giemon.kinematics-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.kinematics :as k]))

(defn approx= [a b] (< (Math/abs (- a b)) 1e-9))

(deftest joint-transform-zero-angle-test
  (testing "zero-angle joint transform is a pure translation"
    (let [xf (k/joint-transform [0.0 0.0 1.0] [0.0 0.0 1.0] 0.0)]
      (is (= [0.0 0.0 1.0] (:xf/pos xf)))
      (is (every? true? (map approx= (flatten (:xf/rot xf)) (flatten k/identity-rot)))))))

(deftest axis-angle-rotation-test
  (testing "rotating [1 0 0] by 90 degrees about z gives [0 1 0]"
    (let [rot (k/axis-angle->rot [0.0 0.0 1.0] (/ Math/PI 2))
          v (k/mat3-vec rot [1.0 0.0 0.0])]
      (is (approx= 0.0 (first v)))
      (is (approx= 1.0 (second v)))
      (is (approx= 0.0 (last v))))))

(deftest combine-test
  (testing "combining two pure-translation transforms adds positions"
    (let [p (k/transform k/identity-rot [1.0 0.0 0.0])
          c (k/transform k/identity-rot [0.0 2.0 0.0])
          w (k/combine p c)]
      (is (= [1.0 2.0 0.0] (:xf/pos w)))))
  (testing "combining with identity is a no-op"
    (let [p (k/transform (k/axis-angle->rot [0.0 0.0 1.0] 1.0) [1.0 0.0 0.0])
          w (k/combine p k/identity-transform)]
      (is (= p w)))))

(deftest normalize-test
  (testing "unit vector is unchanged"
    (is (= [1.0 0.0 0.0] (k/normalize [1.0 0.0 0.0]))))
  (testing "zero vector is returned unchanged (no divide-by-zero)"
    (is (= [0 0 0] (k/normalize [0 0 0])))))
