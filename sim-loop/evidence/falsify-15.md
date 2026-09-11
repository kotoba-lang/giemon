# falsify-15 — `:joint/type` が FK で完全無視 (prismatic 変位が rad 回転として適用) / 角度列の過不足・nil・NaN も無音採用

日時: cron iteration (JST 2026-09-04, host load avg 約 56-62 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-14 は運動学の**入力値**の縮退 (零 axis / ±Inf リミット) を潰した。
未反証の隣接面は**入力の意味論**:

1. `arm/forward-kinematics` は `k/joint-transform` を `:joint/type` を見ずに
   呼ぶ (arm.cljc L39: `(k/joint-transform (:joint/origin joint)
   (:joint/axis joint) angle)`)。`:joint/type :prismatic` の joint の
   変位 (単位 m) がそのまま rad として回転に使われるのではないか。
   未知 type (`:screw` 等) も同様に無音回転ではないか。
2. 角度列の過不足・nil・非数は無音に採用されるのではないか
   (`(or (first angles) 0.0)` — 足りなければ 0.0 補完、nil も 0.0、
   余分は切捨て、`##NaN` は素通り)。

## 実測

コード: `src/kotoba/giemon/arm.cljk` (forward-kinematics L27-41)、
`src/kotoba/giemon/kinematics.cljk` (joint-transform L63-66)。
実行: `clojure -M -e ...` (giemon deps.edn、2 段階 read の fixture — falsify-2/3 済)。

```
; src 全体 grep: `:joint/type` への参照は fixtures の 1 行のみ (src 0 件)
:prismatic-is-revolute-identical true
  (j6 を :prismatic にしても θ=0.5 の pose が :revolute と (=) 完全一致 —
   0.5 m の変位が 0.5 rad の回転として適用されている)
:prismatic-unknown-type-identical true
  (:joint/type :screw (未知 type) でも同一 pose — type は一切分岐しない)
:prismatic-0.001m-rot0.001rad true  (変位 1.0 m = 1.0 rad として同一)
:fk-8angles  8 個渡しても余分 2 個は無音切捨て (identity pose, 6 関節のみ)
:fk-neg1angle 2 個しか渡さないと残り 4 関節が 0.0 補完で無音 FK 完走
:fk-3angles  3 個でも同様 (0.0 補完 3 関節)
:fk-nil      角度 nil は 0.0 扱いで無音完走
:fk-nan-rot  θ=##NaN の joint は回転行列全要素 ##NaN が例外無しで pose に伝播
:fk-string-ex 文字列角度のみ ClassCastException で fail-closed
```

読み取り:

- **`:joint/type` は dead field**: `forward-kinematics` は revolute 専用の
  `joint-transform` を type 無視で呼ぶため、prismatic joint (URDF では
  並進関節) にメートル単位の変位を与えると**ラジアン回転**として適用される。
  DR (ドメインランダム化) で joint type を含む fixture を撹拌しても FK は
  何も検出しない。fixture の `:joint/type` は現状全 :revolute のため
  正規データでは顕在化しないが、型契約 (EDN が type を宣言している) と
  実装が不一致。
- 角度列の**長さ不変条件が未検査**: 過不足・nil がすべて無音採用され、
  呼び出し側のバグ (angles の並び間違い/欠落) が誤った pose として
  静かに流れる。NaN は falsify-14 の ±Inf リミットと同型の非有限素通り。
- 対照 (fail-closed): 非数 (文字列) 角度のみ CCE。

## verdict: **refuted** (type 無視 + 長さ不変条件欠落 + NaN 素通りの 3 面を実測)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [clojure.edn]) (quote [kotoba.giemon.arm :as arm]))
(def m (first (clojure.edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def ch (clojure.edn/read-string (:arm/chain m)))
(def a {:arm/chain ch})
(prn (= (arm/end-effector (assoc-in a [:arm/chain 5 :joint/type] :prismatic) [0 0 0 0 0 0.5])
       (arm/end-effector a [0 0 0 0 0 0.5])))
(prn (:xf/rot (arm/end-effector a [0 0 0 0 0 ##NaN])))'
;; => true / [[##NaN ##NaN ##NaN] [##NaN ##NaN ##NaN] [##NaN ##NaN ##NaN]]
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-15 実測 — `forward-kinematics` は `:joint/type` を
一切見ず (src 参照 0 件)、prismatic 変位 (m) が rad 回転として無音適用、
未知 type も同一 pose。角度列の過不足・nil は 0.0 補完/切捨てで無音完走、
`##NaN` 角度は NaN 回転行列が pose まで伝播。修理: joint-transform 入口で
`:joint/type` 分岐 (prismatic は並進、未知 type は例外) + FK 入口で
`(count angles) == (count chain)` 検査 + 角度の `Double/isFinite` 検査
(falsify-11/14 の有限性検査と同一修理箇所で済む)。
