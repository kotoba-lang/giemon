# falsify-22 — `chassis/turning-radius` の pivot/直進判定が非有限速度で偽 nil (直進誤認) と ##NaN 半径を無音返す

日時: cron iteration (JST 2026-09-04 17:46-17:55, host load avg 27-49 / コア 10 → 軽量 in-memory REPL 測定のみ、fixture 読み込みなし)

## 仮説

falsify-16 は `twist->track-speeds` / `track-speeds->twist` の track-width 縮退化を潰したが、
同一 namespace の `turning-radius` (L33-43) と `integrate-pose` (L48-59) は未反証。
`turning-radius` は分岐 `cond` で
`(== left right) → nil` (直進)、`(zero? (+ left right)) → 0.0` (pivot)、
`:else → 計算` と**浮動小数点の直接比較で特異判定**している。
IEEE 754 の下で:

- `(== ##NaN ##NaN)` は false → NaN 速度は直進でも非 nil 分岐に落ち、半径は `##NaN` に。
- `(zero? (+ ##Inf ##-Inf))` は false (`##NaN`) → pivot (left=-right) 走行が pivot 判定から漏れて
  `##NaN` 半径に。
- `(== ##Inf ##Inf)` は true → **無限大速度の両輪が「直進」nil 判定に通る** (有限性検査不在)。

また `integrate-pose` は dt/theta の非有限を無検査で伝播する (falsify-16 の dt=-1.0 実測の
非有限版)。nil pose フィールドは NPE で fail-closed (対照群)。

## 実測

コード: `src/kotoba/giemon/chassis.cljc` turning-radius L33-43, integrate-pose L48-59。
実行: `clojure -M /tmp/f22.clj` + `clojure -M -e` REPL。

```
R1  (turning-radius ##NaN 1.0 2.0)       => ##NaN   (非直進・非pivot速度が NaN 半径)
R2  (turning-radius 0.5 ##Inf ##-Inf)    => ##NaN   (pivot (left=-right) が pivot 判定漏れ → NaN 半径)
R3  (turning-radius 0.5 ##NaN ##NaN)     => ##NaN   ((== NaN NaN)=false で :else 落ち)
R10 (turning-radius 0.5 -0.0 0.0)        => nil     (正当: -0.0==0.0 は直進扱いで妥当)
R17 (turning-radius 0.5 1e308 -1e308)    => 0.0     (pivot 判定は動作)
R18 (turning-radius 0.5 1.0 (+ 1.0 1e-300)) => nil  (正当: 1.0==(+ 1.0 1e-300) は直進扱い)
R11 (turning-radius -0.5 0.0 1.0)        => -0.25   (負幅の符号反転は falsify-16 再確認のみ)
R15 (turning-radius 0.5 ##-Inf ##-Inf)   => nil     (無限大速度が「直進」判定に通る — 有限性検査不在)
R16 (turning-radius 0.5 ##Inf ##Inf)     => nil     (同上、+Inf)
R4  (integrate-pose {...theta ##NaN} ...) => 全座標 ##NaN 伝播 (例外なし)
R5  (integrate-pose {...} 1.0 0.0 ##NaN)  => 全座標 ##NaN 伝播 (例外なし)
R6  (integrate-pose {...} 1.0 0.0 ##Inf)  => x ##Inf / y ##NaN / theta ##NaN (例外なし)
R7  (integrate-pose {:pose/y 0.0 :pose/theta 0.0} ...) => NullPointerException (fail-closed 対照)
R8  (track-speeds->twist 0.5 ##NaN 1.0)  => linear ##NaN / angular ##NaN (falsify-16 再確認)
R13 (twist->track-speeds 0.5 1.0 ##NaN)  => left/right ##NaN (同上)
R14 (track-speeds->twist nil 0.0 1.0)    => NullPointerException (fail-closed 対照)
```

読み取り:

- `turning-radius` は非有限入力に**例外も非有限フラグも出さず**、
  (a) pivot 走行 (`+Inf/-Inf`) を pivot 判定から漏らして `##NaN` 半径、
  (b) 無限大速度 (`±Inf` 両輪) を**「直進」nil と誤判定**、
  (c) NaN 速度をそのまま `##NaN` 半径 — の 3 面で無音に壊れる。
  特に (b) は `nil` = 「straight-line travel」契約の偽陰性: 非物理速度が
  直進と同じ正常値を返す。修理は turning-radius 入口の
  `(every? #(Double/isFinite %) [track-width left right])` 検査
  (非有限は例外化) — falsify-16 の track-width 検査と同一箇所に追加可能。
- `integrate-pose` は dt/theta の非有限を無音伝播する (NaN/Inf 全座標汚染)。
  修理: dt の `(pos? dt)` かつ `Double/isFinite` (falsify-16 の dt=-1.0 と同一箇所)、
  linear/angular の有限性検査も同時。
- 対照群: nil pose フィールド / nil width は NPE で fail-closed —
  破れは非有限 (NaN/±Inf) 経路に集中。整数オーバーフロー級の 1e308 対
  は pivot 0.0 正常、-0.0/微小差も正常 — 破れは**非有限のみ**。

## verdict: **refuted** (turning-radius の非有限入力で pivot 漏れ → ##NaN 半径、無限大速度の直進誤認 nil、NaN 速度の無音 ##NaN 半径を実測。integrate-pose も dt/theta 非有限の無音伝播を再確認)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [kotoba.giemon.chassis :as ch]))
(prn (ch/turning-radius 0.5 ##Inf ##-Inf))  ; => ##NaN  (pivot が NaN 半径に)
(prn (ch/turning-radius 0.5 ##Inf ##Inf))   ; => nil    (無限大速度が「直進」に)
(prn (ch/integrate-pose {:pose/x 0.0 :pose/y 0.0 :pose/theta 0.0} 1.0 0.0 ##Inf))
;; => #:pose{:x ##Inf, :y ##NaN, :theta ##NaN}  (例外なし)'
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-22 実測 — `chassis/turning-radius` は非有限速度を無検査で、
pivot (+Inf/-Inf) が `(zero? (+ left right))` 判定漏れで `##NaN` 半径、無限大両輪は
`(== left right)` true で**「直進」nil に誤判定** (直進契約の偽陰性)、NaN 速度は無音
`##NaN` 半径; `integrate-pose` は dt/theta 非有限を無音伝播 (全座標 NaN/Inf、例外なし)。
nil は NPE で fail-closed 対照。修理: turning-radius 入口の
`(every? #(Double/isFinite %) [track-width left right])` 検査 + integrate-pose の
dt `(pos? dt)` かつ `Double/isFinite` + linear/angular 有限性検査 —
falsify-16 の track-width/dt 有限性検査と同一箇所 (chassis.cljc 入口 1 箇所) に追加可能。
