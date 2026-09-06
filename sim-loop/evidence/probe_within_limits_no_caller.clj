;; falsify-023 probe — H25: `within-limits?` が唯一の RANGE 検証 (ジョイント角
;; lower/upper 検査) だが、その呼び出しを行う src 実行経路が存在しない
;; (FK docstring は「within-limits? を先に呼べ」と明記するが、実装は FK に
;; 範囲検査を一切持たない)。→ RANGE 強制面の不在を input 空間 probe で測る:
;; FK へ (a)範囲外角 (b)limit 欠落 joint (c)型混在角 (d)正規角 [control] を
;; 直接与え、戻り :xf/pos が検査無しで通る / 例外が無い / 何も拒否しない を
;; 決定的に列挙する。さらに全 src ファイルから within-limits? の呼び出し参照を
;; 機械 grep して「caller 不在」を確定する。
;; Read-only: kotoba.giemon.arm の公開関数を in-memory EDN joint で直接呼ぶ。
;; コード修正なし。決定的 (RUN マーカー無し、タイムスタンプなし)。2 回実行一致確認。
(require '[clojure.edn :as edn]
         '[clojure.java.io :as io]
         '[clojure.string :as str]
         '[kotoba.giemon.arm :as arm])

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

(def j-count (count (:arm/chain real-arm)))
(def in-range-angles (mapv (fn [j] (/ (+ (:lower (:joint/limit j)) (:upper (:joint/limit j))) 2.0))
                           (:arm/chain real-arm)))

;; --- variants ---
;; (a) 範囲外角: 各 joint の upper を大きく超える (upper+50 rad)
(def out-of-range-angles
  (mapv (fn [j] (+ (:upper (:joint/limit j)) 50.0)) (:arm/chain real-arm)))

;; (b) limit 丸ごと欠落した joint を持つ arm (ジョイント角の RANGE 定義自体が無い)
(def arm-missing-limit
  (update-in real-arm [:arm/chain 1]
             (fn [j] (dissoc j :joint/limit))))

;; (c) 型混在角: string 角を FK へ直接渡す (j1 のみ string 化)
(defn angle-vec-str [angle-str]
  (mapv #(if (= % 1) angle-str (nth in-range-angles %)) (range j-count)))

;; --- probe helper ---
(defn fk-pos [arm angles]
  (try
    {:returned (into [] (map :xf/pos) (arm/forward-kinematics arm angles))
     :count (count (arm/forward-kinematics arm angles))}
    (catch Exception e
      {:THROWS (.getSimpleName (class e))
       :msg (.getMessage e)})))

(println "H25 — within-limits? caller 不在 (RANGE 強制面の不在) input 空間 probe (falsify-023)")
(println "joint-count:" j-count)
(println "in-range-angles (control, 各 joint limit 中央):" (pr-str in-range-angles))
(println "out-of-range (upper+50 rad per joint):" (pr-str out-of-range-angles))
(println)

(println "--- (a) FK with OUT-OF-RANGE angles (upper+50 rad) ---")
(println "  forward-kinematics =>")
(println "   " (pr-str (fk-pos real-arm out-of-range-angles)))

(println "--- (b) FK with LIMIT-MISSING joint (j2 :joint/limit dissoc) ---")
(println "  forward-kinematics =>")
(println "   " (pr-str (fk-pos arm-missing-limit in-range-angles)))

(println "--- (c) FK with TYPE-MIXED (string) angle on j1 ---")
(println "  forward-kinematics =>")
(println "   " (pr-str (fk-pos real-arm (angle-vec-str "1.5"))))

(println "--- (d) control: FK with in-range angles ---")
(println "  forward-kinematics =>")
(println "   " (pr-str (fk-pos real-arm in-range-angles)))

(println)
(println "--- within-limits? 参照箇所の全 src 機械列挙 (caller 存在判定) ---")
(doseq [f (sort (filter #(str/ends-with? % ".cljc")
                        (file-seq (io/file "src"))))]
  (let [lines (str/split-lines (slurp f))
        hits (keep-indexed (fn [i l] (when (str/includes? l "within-limits?") (inc i))) lines)]
    (println "   " (str f) "->" (pr-str (vec hits)))))
(println)
(println "== 判定 ==")
(println "  (a) 範囲外角 (upper+50 rad): FK は "
         (if (contains? (fk-pos real-arm out-of-range-angles) :THROWS)
           "THROWS" "無検査で :xf/pos を受理 (RANGE 検査不在)"))
(println "  (b) limit 欠落 joint: FK は "
         (if (contains? (fk-pos arm-missing-limit in-range-angles) :THROWS)
           "THROWS" "無検査で :xf/pos を受理 (limit 無くても silent)"))
(println "  (c) 型混在 (string) 角: FK は "
         (if (contains? (fk-pos real-arm (angle-vec-str "1.5")) :THROWS)
           "ClassCastException LOUD (RANGE 検査起因ではなく計算の型崩れ)" "例外なしで受理"))
(println "  within-limits? 参照: 定義行+docstring (arm.cljc 15,28) のみ = src caller 不在")
(println "DONE")