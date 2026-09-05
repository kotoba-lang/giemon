# falsify-14 — joint `:axis` 零ベクトルが例外無しに det −1 の鏡映変換 (不正回転) を無音生成 / `:joint/limit` ±Inf 境界も無音受理

日時: cron iteration (JST 2026-09-04, host load avg 約 55 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-5〜11 は torque 検査経路の fail-open を潰した。未反証の隣接面は
**運動学入力の縮退**:

1. `k/axis-angle->rot` は「not-necessarily-unit axis」と宣言するが、
   `normalize` は零ベクトルを**素通し**する (kinematics.cljc L22-27:
   `(if (zero? n) v ...)`)。axis `[0 0 0]` のとき Rodrigues の t*x² 等は
   全て 0 になり回転行列は `diag(cos θ, cos θ, cos θ)` に縮退する。
   θ=π なら `diag(-1,-1,-1)`、det −1 の**鏡映** (rotation ではない) が
   回転行列として返り、`end-effector` / `forward-kinematics` は例外も
   検出も無しにそれを pose として出すのではないか。
2. `arm/within-limits?` は `lower`/`upper` を `some?` 検査のみで採用し
   有限性を検査しないため、`:upper ##Inf` / `:lower ##-Inf` の joint が
   任意角度 (1e9 rad 等) を「制限内」と判定するのではないか
   (falsify-11 の ##NaN 系の隣接面: 無限リミットは合法に見える入力)。

## 実測

コード: `src/kotoba/giemon/kinematics.cljc` (normalize L22-27 /
axis-angle->rot L42-50)、`src/kotoba/giemon/arm.cljc` (within-limits? L15-19 /
forward-kinematics L27-41 / end-effector L43-45)。
実行: `clojure -M -e ...` (giemon deps.edn、2 段階 read の fixture — falsify-2/3 済)。

```
:zeroaxis-pi-rot  [[-1.0 0.0 0.0] [0.0 -1.0 0.0] [0.0 0.0 -1.0]]   <- j6 axis を [0 0 0] にし θ=π
:zeroaxis-pi-det  -1.0        <- 鏡映 (det=-1)。回転行列の契約破れ
:zeroaxis-pi-pos  [0.0 0.0 0.62...]  (位置は並進のみで生存)
:baseline-pi-det  1.0         (正しい axis [0 0 1] なら det=+1 の正規回転)
:zeroaxis-raw-rot (k/axis-angle->rot [0 0 0] Math/PI) => 同一の diag(-1,-1,-1)
:lim-inf-upper (arm/within-limits? {:joint/limit {:lower -3.0 :upper ##Inf}} 1e9) => true
:lim-inf-lower (arm/within-limits? {:joint/limit {:lower ##-Inf :upper 3.0}} -1e9) => true
:lim-nan-upper (:upper ##NaN, angle 1e6) => false  (<= が NaN で false になり偶然 fail-closed)
:lim-nil-bounds (lower/upper nil)         => false  (some? ガードは機能)
```

読み取り:

- **axis 零ベクトルは迂回路**: `normalize` の零通しが Rodrigues を
  `diag(c,c,c)` に縮退させ、θ=π で det −1 の鏡映が**例外無し**で
  FK pose になる (det +1 の回転という暗黙契約が破られる)。
  governor 側が FK pose を信頼する構成では、破損 fixture / DR 撹拌で
  鏡映姿勢が正規姿勢として流れ得る。torque 経路 (falsify-6/10/11) と
  同型の「無音不良入力採用」が運動学側にも存在する。
- **±Inf リミットは無音受理**: `some?` 検査のみで有限性を見ないため、
  `:upper ##Inf` の joint は実質リミット無し (1e9 rad も制限内)。
  `##NaN` は比較が false になり偶然 deny 侧に倒れるが、それは
  検査ではなく比較の副産物。
- 対照 (fail-closed 正常): nil bounds は deny、正しい axis は det +1。

## verdict: **refuted** (2 面とも契約に対する無音不良入力採用を実測)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [clojure.edn]) (quote [kotoba.giemon.arm :as arm]) (quote [kotoba.giemon.kinematics :as k]))
(def m (first (clojure.edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def ch (clojure.edn/read-string (:arm/chain m)))
(defn set-j6-axis [ax] {:arm/chain (mapv #(if (= (:joint/name %) "j6") (assoc % :joint/axis ax) %) ch)})
(prn (k/axis-angle->rot [0 0 0] Math/PI))
(prn (:xf/rot (arm/end-effector (set-j6-axis [0 0 0]) [0 0 0 0 0 Math/PI])))
(prn (arm/within-limits? {:joint/limit {:lower -3.0 :upper ##Inf}} 1e9))'
;; => [[-1.0 0.0 0.0] [0.0 -1.0 0.0] [0.0 0.0 -1.0]] / 同一 (det -1) / true
```

## コアへの 1 行メッセージ

`normalize` 零ベクトル通過を例外化 (または axis の norm 検査を
`joint-transform` 入口に) し、`within-limits?` の lower/upper に
`Double/isFinite` 検査を追加すること — falsify-11 の有限性検査と
同一修理箇所で済む。
