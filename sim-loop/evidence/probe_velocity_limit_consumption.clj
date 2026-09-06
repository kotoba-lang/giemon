;; falsify-021 probe (H23) — :joint/limit :velocity 消費検証
;; 測定専用 (evidence 配下、コード修正なし)。実 fixture giemon_arm6.edn から
;; reconstitute-arm で復元し、j2 の :joint/limit :velocity を {3(実fixture値),
;; 欠落, 型混在"high", 1000} と振って、全公開決定関数の出力が変化するか機械測定する。
;; RUN マーカー行は正規化対象 (2 回実行の diff 検知用)。決定的・タイムスタンプなし。

(require '[clojure.edn :as edn]
         '[clojure.java.io :as io]
         '[clojure.string :as str])

(defn- unblob [v]
  (if (string? v)
    (try (let [parsed (edn/read-string v)] (if (coll? parsed) parsed v))
         (catch Exception _ v))
    v))

(defn- reconstitute-arm [tx-data]
  (into {} (map (fn [[k v]] [k (unblob v)]))
        (dissoc (first tx-data) :db/id)))

(def real-arm
  (reconstitute-arm
   (edn/read-string (slurp (io/file "fixtures" "giemon_arm6" "giemon_arm6.edn")))))

;; --- 実 fixture の全 joint の :joint/limit :velocity を列挙 (control) ---
(def real-limits
  (mapv (fn [j] [(:joint/name j) (get-in j [:joint/limit :velocity] ::missing)])
        (:arm/chain real-arm)))

;; --- j2 の :joint/limit を各 variant に差し替えた arm ---
(defn j2-limit-variant [arm limit-map]
  (update-in arm [:arm/chain 1]
             (fn [j] (if (nil? limit-map)
                       (dissoc j :joint/limit)
                       (assoc j :joint/limit limit-map)))))

(def v-control (j2-limit-variant real-arm {:lower -2.2 :upper 2.2 :effort 40 :velocity 3}))
(def v-missing (j2-limit-variant real-arm {:lower -2.2 :upper 2.2 :effort 40}))
(def v-typed   (j2-limit-variant real-arm {:lower -2.2 :upper 2.2 :effort 40 :velocity "high"}))
(def v-absurd  (j2-limit-variant real-arm {:lower -2.2 :upper 2.2 :effort 40 :velocity 1000.0}))

(require '[kotoba.giemon.arm :as arm])

;; --- 測定対象: 公開決定関数群 (出力を pr-str で平坦化) ---
(defn measure [arm]
  (let [angles-edge [0.0 2.2 0.5 0.6 -0.4 0.7]]
    (pr-str {:within-edge (arm/within-limits? (nth (:arm/chain arm) 1) 2.2)
             :within-mid  (arm/within-limits? (nth (:arm/chain arm) 1) 0.0)
             :fk-edge-pos (:xf/pos (first (arm/forward-kinematics arm angles-edge)))
             :fk-edge-ee  (:xf/pos (arm/end-effector arm angles-edge))
             :torque      (arm/torque-headroom arm)
             :underrated  (arm/underrated-joints arm)
             :bom-model   (mapv :model (arm/bom arm :all-qdd))})))

(def results
  {:string/control (measure v-control)
   :string/missing (measure v-missing)
   :string/typed   (measure v-typed)
   :string/absurd  (measure v-absurd)})

(defn -main [& _]
  (println "RUN0 falsify-021 probe start")
  (println "real-fixture j2 :joint/limit =" (pr-str (get-in real-arm [:arm/chain 1 :joint/limit])))
  (println "real-fixture all-joint :joint/limit :velocity =" (pr-str real-limits))
  (println "V0-content    = " (:string/control results))
  (println "V1-missing    = " (:string/missing results))
  (println "V2-typed-str  = " (:string/typed results))
  (println "V3-absurd-1000= " (:string/absurd results))
  (println "V1-idx-vs-V0  = " (= (:string/control results) (:string/missing results)))
  (println "V2-idx-vs-V0  = " (= (:string/control results) (:string/typed results)))
  (println "V3-idx-vs-V0  = " (= (:string/control results) (:string/absurd results)))
  (println "src-contains-velocity-non-chassis ="
           (pr-str (into {}
                         (for [f (sort (filter #(str/ends-with? % ".cljc")
                                               (file-seq (io/file "src"))))]
                           [(str f) (str/includes? (slurp f) "velocity")]))))
  (println "RUN0 falsify-021 probe end"))

(-main)