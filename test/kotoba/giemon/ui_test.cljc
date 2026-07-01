(ns kotoba.giemon.ui-test
  (:require [clojure.test :refer [deftest is testing]]
            [clojure.string :as str]
            [kotoba.giemon.ui :as ui]))

(def arm-spec
  {:arm/chain
   [{:joint/name "j1" :joint/limit {:effort 10} :joint/actuator {:cont-nm 20}}]})

(deftest dashboard-test
  (testing "dashboard renders product names and the read-only banner"
    (let [html (ui/dashboard {})]
      (is (str/includes? html "Giemon Otete"))
      (is (str/includes? html "Giemon Hitogata"))
      (is (str/includes? html "read-only"))))
  (testing "dashboard renders the torque table when arm-spec is given"
    (let [html (ui/dashboard {:arm-spec arm-spec})]
      (is (str/includes? html "torque headroom")))))
