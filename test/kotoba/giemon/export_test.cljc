(ns kotoba.giemon.export-test
  (:require [clojure.string :as str]
            [clojure.test :refer [deftest is testing]]
            [kotoba.giemon.export :as export]))

(def arm-spec
  {:arm/chain
   [{:joint/name "j1" :joint/limit {:effort 10} :joint/actuator {:cont-nm 20}}]})

(deftest products->csv-test
  (let [csv (export/products->csv)]
    (is (str/includes? csv "Giemon Otete"))
    (is (str/includes? csv "product,kind,dof,status,kaigo_role"))))

(deftest torque->csv-test
  (let [csv (export/torque->csv arm-spec)]
    (is (str/includes? csv "j1,10,20,10"))))

(deftest products->json-test
  (let [json (export/products->json)]
    (is (str/includes? json "\"product\":\"Giemon Otete\""))))

(deftest torque->json-test
  (testing "escapes and formats the same headroom data as CSV"
    (let [json (export/torque->json arm-spec)]
      (is (str/includes? json "\"joint\":\"j1\""))
      (is (str/includes? json "\"headroom_nm\":10")))))
