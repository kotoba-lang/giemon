;; falsify-022 probe — H24: `within-limits?` RANGE 検証の静かな false が
;; false-pass に化ける経路 (limit 丸ごと欠落 / lower 欠落 / upper 欠落 /
;; nil / 型混在 / 逆転 / 範囲内角 / 範囲外角) の input 空間列挙測定。
;; Read-only: kotoba.giemon.arm の公開述語を in-memory EDN joint で直接呼ぶ。
;; コード修正なし。決定的 (RUN マーカー無し、タイムスタンプ無し)。
(require '[kotoba.giemon.arm :as arm])

(defn base-joint []
  ;; j2 相当の健全 limit (実 fixture: {:lower -2.2 :upper 2.2 :effort 40 :velocity 3})
  {:joint/name "j2"
   :joint/type :revolute
   :joint/axis [0 1 0]
   :joint/origin [0 0 0.06]
   :joint/limit {:lower -2.2 :upper 2.2 :effort 40 :velocity 3}})

(def variants
  {:V0-limit-ok        (base-joint)
   :V1-limit-missing   (dissoc (base-joint) :joint/limit)
   :V2-lower-missing   (update (base-joint) :joint/limit dissoc :lower)
   :V3-upper-missing   (update (base-joint) :joint/limit dissoc :upper)
   :V4-lower-nil       (assoc-in (base-joint) [:joint/limit :lower] nil)
   :V5-upper-nil       (assoc-in (base-joint) [:joint/limit :upper] nil)
   :V6-upper-str       (assoc-in (base-joint) [:joint/limit :upper] "2.2")
   :V7-lower-str       (assoc-in (base-joint) [:joint/limit :lower] "-2.2")
   :V8-inverted        (assoc-in (base-joint) [:joint/limit] {:lower 2.2 :upper -2.2})})

(def angles [-10.0 -2.2 0.0 2.2 10.0])

(defn probe [label f]
  (print "  " label " => ")
  (try
    (println (pr-str (f)))
    (catch Exception e
      (println "THROWS:" (.getSimpleName (class e)) "-" (.getMessage e)))))

(println "H24 — within-limits? limit 欠落面 input 空間列挙 (falsify-022)")
(println "angles:" (pr-str angles))
(println)

(doseq [[vk vt] variants]
  (println "--- " (name vk) " limit=" (pr-str (:joint/limit vt)))
  (doseq [a angles]
    (probe (format "%8.1f" a) #(arm/within-limits? vt a))))
(println)

;; false-pass 判定: どの変種が「不正/欠落 limit なのに true(受理)」を返すか集計
(println "== true(受理) を返した (変種 x 角) の一覧: false-pass の可否 ==")
(println "  [none なら false-pass は走らない]")
(doseq [[vk vt] variants]
  (doseq [a angles]
    (try
      (when (true? (arm/within-limits? vt a))
        (println "    ACCEPTED:" (name vk) "at" a))
      (catch Exception _ ()))))
(println "== 各変種の受理角数 ==")
(doseq [[vk vt] variants]
  (let [n (count (filter #(try (true? (arm/within-limits? vt %)) (catch Exception _ false)) angles))]
    (println "    " (name vk) "-> accepted" n "/" (count angles))))
(println "DONE")