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

(deftest json-export-escapes-every-c0-control-character
  ;; RFC 8259 requires EVERY control character U+0000-U+001F to be
  ;; escaped, not just \ " and \n -- a joint name (caller-supplied via
  ;; arm-spec) containing a raw tab or other control byte would
  ;; otherwise be copied through raw, producing invalid JSON (verified
  ;; against Python's strict json module).
  (let [spec {:arm/chain
              [{:joint/name (str "j" (char 9) "1" (char 1) "x")
                :joint/limit {:effort 10} :joint/actuator {:cont-nm 20}}]}
        json (export/torque->json spec)]
    (is (str/includes? json "\"joint\":\"j\\t1\\u0001x\""))))
