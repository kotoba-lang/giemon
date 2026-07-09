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

(def ^:private json-hex-digits "0123456789abcdef")

(defn- json-hex4
  "4-digit hex for a JSON `\\uXXXX` escape (portable: bit ops + a lookup
  table, no Long/Integer interop that would only work on :clj)."
  [n]
  (apply str (for [shift [12 8 4 0]] (nth json-hex-digits (bit-and (bit-shift-right n shift) 0xf)))))

(def ^:private json-string-escapes
  "RFC 8259 §7: EVERY control character U+0000-U+001F must be escaped in
  a JSON string, not just \\ \" and \\n -- an operator-supplied field
  containing a raw \\t, \\r, or other control byte would otherwise be
  copied through raw, producing invalid JSON (verified against Python's
  strict json module)."
  (into {\" "\\\"" \\ "\\\\"}
        (for [i (range 0x20)]
          [(char i) (case i
                      8 "\\b" 9 "\\t" 10 "\\n" 12 "\\f" 13 "\\r"
                      (str "\\u" (json-hex4 i)))])))

(defn- json-str [v]
  (str/escape (str (if (nil? v) "" v)) json-string-escapes))

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
