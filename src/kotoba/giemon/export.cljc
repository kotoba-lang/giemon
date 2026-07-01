(ns kotoba.giemon.export
  "CSV/JSON export for the Giemon product registry and Otete arm torque
  headroom — audit-grade evidence, read-only. No network, no I/O."
  (:require [clojure.string :as str]
            [kotoba.giemon :as giemon]
            [kotoba.giemon.arm :as arm]))

(defn- csv-cell [v]
  (let [s (str (if (nil? v) "" v))]
    (if (re-find #"[\",\n]" s)
      (str "\"" (str/replace s "\"" "\"\"") "\"")
      s)))

(defn- csv-row [vals] (str/join "," (map csv-cell vals)))

(defn- json-str [v]
  (-> (str (if (nil? v) "" v))
      (str/replace "\\" "\\\\")
      (str/replace "\"" "\\\"")
      (str/replace "\n" "\\n")))

(defn products->csv []
  (str/join "\n"
    (cons (csv-row ["product" "kind" "dof" "status" "kaigo_role"])
          (for [[_ p] giemon/products]
            (csv-row [(:product/name p) (name (:product/kind p))
                      (:product/dof p "") (name (:product/status p))
                      (:product/kaigo-role p)])))))

(defn torque->csv [arm-spec]
  (str/join "\n"
    (cons (csv-row ["joint" "required_nm" "rated_nm" "headroom_nm"])
          (for [t (arm/torque-headroom arm-spec)]
            (csv-row [(:joint/name t) (:torque/required t)
                      (:torque/rated t) (:torque/headroom t)])))))

(defn products->json []
  (str "["
       (str/join ","
                 (for [[_ p] giemon/products]
                   (str "{\"product\":\"" (json-str (:product/name p)) "\","
                        "\"kind\":\"" (name (:product/kind p)) "\","
                        "\"dof\":" (or (:product/dof p) "null") ","
                        "\"status\":\"" (name (:product/status p)) "\","
                        "\"kaigo_role\":\"" (json-str (:product/kaigo-role p)) "\"}")))
       "]"))

(defn torque->json [arm-spec]
  (str "["
       (str/join ","
                 (for [t (arm/torque-headroom arm-spec)]
                   (str "{\"joint\":\"" (json-str (:joint/name t)) "\","
                        "\"required_nm\":" (:torque/required t) ","
                        "\"rated_nm\":" (:torque/rated t) ","
                        "\"headroom_nm\":" (:torque/headroom t) "}")))
       "]"))
