(ns kotoba.giemon-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.giemon :as giemon]))

(deftest products-test
  (testing "otete is DOF 6 and shipping"
    (let [p (giemon/product :otete)]
      (is (= 6 (:product/dof p)))
      (is (= :shipping (:product/status p)))))
  (testing "hitogata is 17-axis and in-design"
    (is (= 17 (:product/dof (giemon/product :hitogata))))
    (is (= :in-design (:product/status (giemon/product :hitogata)))))
  (testing "caterpillar is in-design and not vaporware-orderable"
    (let [p (giemon/product :caterpillar)]
      (is (= :in-design (:product/status p)))
      (is (string? (:product/fixture p)))))
  (testing "unknown product returns nil"
    (is (nil? (giemon/product :nope)))))
