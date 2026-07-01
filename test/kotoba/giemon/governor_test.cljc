(ns kotoba.giemon.governor-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.robotics :as rob]
            [kotoba.giemon.governor :as gov]))

(deftest kaigo-mission-test
  (let [m (gov/kaigo-mission "M1" :otete "服薬管理")]
    (is (= "otete" (:mission/robot m)))
    (is (= :planned (:mission/status m)))))

(deftest kaigo-action-defaults-test
  (testing "otete action defaults to :medium safety"
    (let [a (gov/kaigo-action "A1" "M1" :otete :move)]
      (is (= :medium (:action/safety a)))))
  (testing "caterpillar action defaults to :low safety"
    (let [a (gov/kaigo-action "A1" "M1" :caterpillar :move)]
      (is (= :low (:action/safety a)))))
  (testing "explicit safety overrides the product default"
    (let [a (gov/kaigo-action "A1" "M1" :otete :move :safety :high)]
      (is (= :high (:action/safety a))))))

(deftest fall-detected-alert-test
  (testing "fall alert is always safety-critical and requires sign-off"
    (let [a (gov/fall-detected-alert "A2" "M1" :params {:location "hallway"})]
      (is (= :safety-critical (:action/safety a)))
      (is (rob/requires-sign-off? a))
      (is (= :emit (:action/kind a))))))
