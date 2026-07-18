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

(deftest csv-export-quotes-a-bare-carriage-return
  ;; RFC 4180 requires quoting a field containing CR, LF, or a comma --
  ;; \r alone is also a line terminator every standard CSV reader
  ;; recognizes, but the check here only ever covered \n. Verified
  ;; against Python's csv module: an unquoted bare \r split the row into
  ;; two corrupted rows on read-back.
  (let [spec {:arm/chain
              [{:joint/name (str "j" (char 13) "1")
                :joint/limit {:effort 10} :joint/actuator {:cont-nm 20}}]}
        csv (export/torque->csv spec)]
    (is (str/includes? csv "\"j\r1\""))))

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

(def bom-arm-spec
  {:arm/chain
   [{:joint/name "j1" :joint/actuator {:model "Motor A" :cont-nm 20 :peak-nm 60 :price-jpy 42000 :buy "Vendor X"}}
    {:joint/name "j2" :joint/actuator {:model "Motor B" :cont-nm 10 :peak-nm 30 :price-jpy 28000 :buy "Vendor Y"}}
    {:joint/name "j3"}]})

(deftest bom->csv-test
  (let [csv (export/bom->csv bom-arm-spec)]
    (is (str/includes? csv "joint,model,cont_nm,peak_nm,price_jpy,buy"))
    (is (str/includes? csv "j1,Motor A,20,60,42000,Vendor X"))
    (is (str/includes? csv "j2,Motor B,10,30,28000,Vendor Y"))
    (is (not (str/includes? csv "j3")))))

(deftest bom->json-test
  (let [json (export/bom->json bom-arm-spec)]
    (is (str/includes? json "\"joint\":\"j1\""))
    (is (str/includes? json "\"price_jpy\":42000"))
    (is (str/includes? json "\"buy\":\"Vendor X\""))
    (is (not (str/includes? json "j3")))))
