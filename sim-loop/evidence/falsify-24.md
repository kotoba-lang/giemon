# falsify-24 — `rob/gate` は actuation payload (`:action/params`) を一切検査せず、非有限・非 map・無値 params の actuating action が無音 `:permit` (nil id/mission も正規生成)

日時: cron iteration (JST 2026-09-04, host load avg 19-31 / コア 10 → 軽量 in-memory REPL 測定のみ、fixture 読み込みなし)

## 仮説

falsify-12/13/19 で gate の kind×class 結合と allowed-set/safety の型無検査を潰したが、
gate が検査するのは `(:action/safety a)` の **クラス** のみで、actuation の実体
**payload `:action/params` は全 falsify で未着手**。`kotoba.robotics` の ns
docstring は「gives a governor the records it needs to **refuse unsafe actuation
before it ever reaches hardware**」と宣言し、`action-kinds` の docstring は
「:sense is read-only; the others actuate hardware」と明言する。つまり
`:actuate`/`:move`/`:grasp`/`:emit` の params が「hardware に届く実効入力」
である以上、gate が params を無検査なら契約の正面での fail-open のはず:

- `:params {:velocity ##Inf :torque ##NaN}` → falsify-11/14〜17 と同系の非有限が
  actuation payload として無音 `:permit` (`action-permitted?` も true)。
- `:params "not-a-map"` (文字列) / `:params nil` → payload 無し actuation が permit。
- `:params {:force -1000000}` → 常識外の値も gate は関知しない。
- `rob/action nil nil :actuate ...` → id/mission nil の actuating action が正規生成
  (falsify-23 の mission nil id と同系、こちらは **action 側**)。

対照仮説: `:safety-critical` の sign-off 経路は params が `##NaN` でも
`:require-sign-off` を維持する (クラス検査だけは生きている) のを確認する。

## 実測

コード: gitlibs `io.github.kotoba-lang/robotics/1d1f93e.../src/kotoba/robotics.cljc`
gate L120-129 (`:action/safety` のみ参照、`:action/params` 参照 0 件)、
action L60-71 (id/mission/params 無検査)。
実行: `clojure -M /tmp/f/f24.clj` (repl 出力は evidence 末尾の手順と同一)。

```
:H1-params-inf           => {:gate/decision :permit, :action "a1"}   (:actuate :medium, params {:velocity ##Inf :torque ##NaN})
:H2-params-string        => {:gate/decision :permit, :action "a2"}   (:move, params "not-a-map")
:H3-params-nil           => {:gate/decision :permit, :action "a3"}   (:move, params nil)
:H4-params-absurd-neg    => {:gate/decision :permit, :action "a4"}   (:grasp, params {:force -1000000})
:H5-nil-id-accepted      => {:action/id nil, :action/mission nil, :action/kind :actuate, :action/safety :medium, :action/params {}}
:H6-gate-never-mentions-params => {:gate/decision :permit, :action "a5"}  (正常 params の対照)
:H7-action-permitted-inf => true                                     (action-permitted? も Inf params で true)
:H8-sign-off-bypass-with-inf => {:gate/decision :require-sign-off, :safety :safety-critical}  (対照: クラス検査は生存、NaN params でも sign-off 維持)
```

読み取り:

- gate の permit 経路は `(:action/safety a)` のメンバーシップと
  `requires-sign-off?` のみ。`:action/params` は **ソース上参照 0 件** で、
  非有限 (`##Inf`/`##NaN`)・非 map (文字列)・nil・常識外負値のいずれの payload
  も無音 `:permit`。`action-permitted?` も gate 委譲で同一 (H7)。
- これは falsify-12 (kind×class 結合)・falsify-13/19 (set/safety 型) とは別の
  第 4 の無検査面: **クラスが正しくても中身が任意の actuation が通る**。
  gate docstring の「refuse unsafe actuation before it ever reaches hardware」は
  payload については何も担保していない。
- `rob/action` 自体も id/mission nil を無検査で正規化し (H5)、監査に
  「誰の・どのミッションの」action か分からない actuating レコードが乗る
  (falsify-23 の mission nil id と同一クラスの action 版)。
- 対照: H8 の通り `:safety-critical` は params `##NaN` でも
  `:require-sign-off` — クラス階層の検査は生存しており、破れは params 面
  (と id/mission 面) に限定される。

## Verdict: **refuted** (`rob/gate` は `:action/params` を参照せず、非有限・文字列・nil・常識外 params の actuating action を無音 `:permit` (action-permitted? も true)、`rob/action` も nil id/mission を無音正規化。対照: :safety-critical の sign-off は params ##NaN でも維持)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [kotoba.robotics :as rob]))
(def a (rob/action "a1" "m1" :actuate :medium :params {:velocity ##Inf :torque ##NaN}))
(prn (rob/gate a #{:low :medium}))
(prn (rob/action-permitted? a #{:low :medium}))
(prn (rob/action nil nil :actuate :medium))'
;; => {:gate/decision :permit, :action "a1"} / true / nil id+mission の正規 action レコード
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-24 実測 — `rob/gate` は `:action/params` を参照せず
(ソース参照 0 件)、非有限 (`##Inf`/`##NaN`)・文字列・nil・`{:force -1000000}` の
payload を持つ actuating action が無音 `:permit` (action-permitted? も true)、
`rob/action` も nil id/mission を正規生成 — 「hardware に届く前に unsafe actuation
を拒む」契約の payload 面での破れ。修理: gate の permit 経路に actuating kind
(falsify-12 の kind×class 検査と同一箇所) の params 有限性/型検査を追加
(非有限・非 map は `:invalid` 化または例外化、閾値検査までは契約外でも
有限性と map 型は最低限)、rob/action 入口の id/mission some? 検査は
falsify-23 の修理と同一パターンで rob 側入口 1 箇所にまとめられる。