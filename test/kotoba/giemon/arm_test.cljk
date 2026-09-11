(ns kotoba.giemon.arm-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.arm :as arm]))

(def two-joint-arm
  {:arm/chain
   [{:joint/name "j1" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 0.0 1.0]
     :joint/limit {:lower -3.0 :upper 3.0 :effort 10} :joint/actuator {:cont-nm 20}}
    {:joint/name "j2" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 1.0 0.0]
     :joint/limit {:lower -1.0 :upper 1.0 :effort 30} :joint/actuator {:cont-nm 25}}]})

(deftest joint-count-test
  (is (= 2 (arm/joint-count two-joint-arm))))

(deftest forward-kinematics-test
  (testing "zero angles stack pure z-translations"
    (let [xfs (arm/forward-kinematics two-joint-arm [0.0 0.0])]
      (is (= 2 (count xfs)))
      (is (= [0.0 0.0 2.0] (:xf/pos (last xfs))))))
  (testing "missing angles default to 0.0"
    (is (= (arm/forward-kinematics two-joint-arm [0.0 0.0])
           (arm/forward-kinematics two-joint-arm [])))))

(deftest end-effector-test
  (is (= (arm/end-effector two-joint-arm [0.0 0.0])
         (last (arm/forward-kinematics two-joint-arm [0.0 0.0])))))

(deftest within-limits-test
  (is (arm/within-limits? (first (:arm/chain two-joint-arm)) 0.0))
  (is (not (arm/within-limits? (first (:arm/chain two-joint-arm)) 5.0))))

(deftest torque-headroom-test
  (testing "j1 has headroom, j2 is under-rated"
    (let [h (arm/torque-headroom two-joint-arm)]
      (is (= 10 (:torque/headroom (first h))))
      (is (= -5 (:torque/headroom (second h))))))
  (testing "underrated-joints finds only j2"
    (let [under (arm/underrated-joints two-joint-arm)]
      (is (= 1 (count under)))
      (is (= "j2" (:joint/name (first under)))))))
