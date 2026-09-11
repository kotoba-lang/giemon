# falsify-25 — `ui/torque-table` は headroom を `neg?` 1 点だけで :err/:ok 分類し、`##NaN` headroom が **:ok (緑)** 表示で運用コンソールに乗る (viewer は NaN 角度を NaN 回転行列のまま scene-IR 化)

日時: cron iteration (JST 2026-09-04, host load avg 20-33 / コア 10 → 軽量 in-memory REPL 測定のみ、fixture 読み込みなし)

## 仮説

falsify-6〜24 で arm / kinematics / chassis / export / gate / mission の fail-open
は潰したが、giemon 側の残る未反証 namespace は **ui.cljc (オペレータコンソール)**
と **viewer.cljc (scene-IR)**。ui/torque-table は
`(if (neg? (:torque/headroom t)) :err :ok)` で headroom を分類する (src L33-35)。
falsify-11 で `##NaN` の rated/required が headroom をセンチネルにし
`underrated-joints` の `neg?` フィルタを無音通過することは実測済み — ならば
同じ NaN headroom は ui 側でも `neg?` → false で **:ok クラス**になり、
オペレータコンソールが壊れた torque を正常表示するはず。生 `NaN` 文字列も
HTML にそのまま補間される (export 層 falsify-17 と同型の非有限流出)。
あわせて viewer/arm-scene-ir は FK 結果をそのまま scene-IR 化するため、
falsify-14/15 の NaN 角度伝播がレンダリング入力まで届くことを確認する。

## 実測

コード: `src/kotoba/giemon/ui.cljk` L33-35 (`neg?` 1 点分類、有限性検査なし)、
`src/kotoba/giemon/viewer.cljk` L13-23 (FK 結果の無検査 IR 化)。
実行: `clojure -M /tmp/f/f25.clj` + `/tmp/f/f25b.clj` (repl 出力は evidence 末尾の手順と同一)。

```
:H1-nan-required-j1-class  => "ok"   (:effort ##NaN の joint1、headroom ##NaN が :ok 表示)
:H2-nan-rated-j2-class     => "ok"   (:cont-nm ##NaN の joint2、同様に :ok)
:H3-inf-required-j1-class  => "err"  (対照: ##Inf は neg? ##-Inf headroom で err、非対称にしか検知)
:H4-neg-inf-headroom-j2    => "err"  (対照同様)
:H5-nan-in-markup?         => true   (生 "NaN" が HTML に補間される)
:H6-inf-in-markup?         => true   (生 "Infinity" も同様)
:H7-viewer-nan-angle-rot   => 全成分 ##NaN の 3x3 行列が :instance/rot に無音乗る
:H8-viewer-normal-rot      => 対照: 正常角度は正常回転行列
```

読み取り:

- `neg?` は `##NaN` に false を返すため、NaN headroom は **:err にならない**。
  falsify-11 の fail-open (非有限が torque 経路を無音通過) が ui 層で
  「正常 (ok クラス表示)」に増幅される — export 層 (falsify-17) と異なり
  こちらは **人間の運用判断の入力**が直接誤る。
- `##Inf` required だけは headroom `##-Inf` で偶然 err になるが、これは
  非有限検知ではなく符号の偶然で、NaN 面では完全に無防備。
- 生 `NaN`/`Infinity` トークンが HTML に乗る点は falsify-17 (JSON/CSV) の
  HTML 版。ui 側も export 側と同一の「出力直前の非有限検査」を欠く。
- viewer は NaN 角度の FK 結果 (NaN 回転行列) を例外無し scene-IR に載せる
  (falsify-14/15 の伝播終点を実測)。pos は origin のみで見えないため rot で確認。
- 対照: HTML エスケープ自体は html.core/esc が機能しており、
  破れは意味分類 (neg?) と非有限検査の欠落に限定される。

## Verdict: **refuted** (`ui/torque-table` は headroom を `neg?` 1 点だけで分類し `##NaN` headroom を :ok 表示 + 生 `NaN`/`Infinity` を HTML に補間、`viewer/arm-scene-ir` は NaN 角度の NaN 回転行列を無音 scene-IR 化。対照: ##Inf は neg? ##-Inf で偶然 err、HTML エスケープ自体は正常)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [kotoba.giemon.ui :as ui]) (quote [kotoba.giemon.viewer :as viewer]))
(def arm-nan {:arm/chain [{:joint/name "j1" :joint/limit {:effort ##NaN} :joint/actuator {:cont-nm 20}}]})
(prn (re-find #"class=\"[^\"]+\"" (second (clojure.string/split (ui/dashboard {:arm-spec arm-nan}) #"<td>j1</td>"))))
;; => "class=\"ok\""  (NaN headroom が ok 表示)
(def ir (viewer/arm-scene-ir {:arm/chain [{:joint/name "j1" :joint/axis [0 0 1] :joint/origin [1.0 2.0 3.0]}]} [##NaN]))
(prn (:instance/rot (first (:scene/instances ir))))'
;; => 全 ##NaN の 3x3 行列
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-25 実測 — `ui/torque-table` は headroom を `neg?`
1 点だけで :err/:ok 分類するため falsify-11 で無音侵入する `##NaN` headroom が
**:ok (正常) 表示**でオペレータコンソールに乗り、生 `NaN`/`Infinity` トークンも
HTML に補間される (falsify-17 の HTML 版 + 意味分類面の追加破れ)。
`viewer/arm-scene-ir` は falsify-14/15 の NaN 角度を NaN 回転行列のまま
scene-IR 化する。修理: torque-headroom 入口の `Double/isFinite` 検査
(falsify-11/17 と同一箇所で塞げば ui/viewer/export 3 面同時に消える) に加え、
ui 分類は `neg?` でなく有限性確認後の比較に変更する。
