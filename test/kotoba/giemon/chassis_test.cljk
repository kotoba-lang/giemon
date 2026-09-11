(ns kotoba.giemon.chassis-test
  (:require [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.chassis :as chassis]))

(deftest track-speeds->twist-test
  (testing "straight-line: both tracks equal speed -> zero angular velocity"
    (let [t (chassis/track-speeds->twist 1.0 2.0 2.0)]
      (is (= 2.0 (:twist/linear t)))
      (is (= 0.0 (:twist/angular t)))))
  (testing "differential speeds produce linear + angular velocity"
    (let [t (chassis/track-speeds->twist 1.0 1.0 3.0)]
      (is (= 2.0 (:twist/linear t)))
      (is (= 2.0 (:twist/angular t))))))

(deftest twist->track-speeds-test
  (testing "round-trips track-speeds->twist"
    (let [t (chassis/track-speeds->twist 1.0 1.0 3.0)
          s (chassis/twist->track-speeds 1.0 (:twist/linear t) (:twist/angular t))]
      (is (= 1.0 (:track/left s)))
      (is (= 3.0 (:track/right s))))))

(deftest turning-radius-test
  (testing "equal track speeds -> straight line, no defined radius"
    (is (nil? (chassis/turning-radius 1.0 2.0 2.0))))
  (testing "mirrored opposite speeds -> in-place pivot, radius 0"
    (is (= 0.0 (chassis/turning-radius 1.0 -1.0 1.0))))
  (testing "general turn matches the differential-drive ICC formula"
    (is (= 1.0 (chassis/turning-radius 1.0 1.0 3.0)))))

(deftest integrate-pose-test
  (testing "pure translation along heading 0"
    (let [p (chassis/integrate-pose {:pose/x 0.0 :pose/y 0.0 :pose/theta 0.0} 1.0 0.0 1.0)]
      (is (= 1.0 (:pose/x p)))
      (is (= 0.0 (:pose/y p)))
      (is (= 0.0 (:pose/theta p)))))
  (testing "pure rotation in place (linear 0 keeps x/y exact regardless of trig)"
    (let [p (chassis/integrate-pose {:pose/x 5.0 :pose/y 5.0 :pose/theta 0.0} 0.0 (/ Math/PI 2) 1.0)]
      (is (= 5.0 (:pose/x p)))
      (is (= 5.0 (:pose/y p)))
      (is (= (/ Math/PI 2) (:pose/theta p))))))

(def two-joint-boom-chassis
  {:chassis/boom
   {:arm/chain
    [{:joint/name "j1" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 0.0 1.0]
      :joint/limit {:lower -3.0 :upper 3.0 :effort 10} :joint/actuator {:cont-nm 20}}
     {:joint/name "j2" :joint/origin [0.0 0.0 1.0] :joint/axis [0.0 1.0 0.0]
      :joint/limit {:lower -1.0 :upper 1.0 :effort 30} :joint/actuator {:cont-nm 25}}]}
   :chassis/realization
   {:default :all-actuated}})

(deftest boom-arm-test
  (testing "joins :chassis/realization onto :chassis/boom as :arm/realization"
    (let [a (chassis/boom-arm two-joint-boom-chassis)]
      (is (= (:chassis/boom two-joint-boom-chassis) (dissoc a :arm/realization)))
      (is (= (:chassis/realization two-joint-boom-chassis) (:arm/realization a))))))

(deftest boom-forward-kinematics-test
  (let [xfs (chassis/boom-forward-kinematics two-joint-boom-chassis [0.0 0.0])]
    (is (= 2 (count xfs)))
    (is (= [0.0 0.0 2.0] (:xf/pos (last xfs))))))

(deftest boom-actuators-test
  (is (= 2 (count (chassis/boom-actuators two-joint-boom-chassis)))))

(deftest boom-bom-test
  (testing "default variant returns the inline chain actuators"
    (is (= (chassis/boom-actuators two-joint-boom-chassis)
           (chassis/boom-bom two-joint-boom-chassis :all-actuated)))))

(deftest boom-torque-headroom-test
  (testing "j1 has headroom, j2 is under-rated"
    (let [h (chassis/boom-torque-headroom two-joint-boom-chassis)]
      (is (= 10 (:torque/headroom (first h))))
      (is (= -5 (:torque/headroom (second h)))))))

(deftest boom-underrated-joints-test
  (let [under (chassis/boom-underrated-joints two-joint-boom-chassis)]
    (is (= 1 (count under)))
    (is (= "j2" (:joint/name (first under))))))
