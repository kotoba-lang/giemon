# falsify-12 — `:safety :none` の hardware actuate が class メンバーシップ gate を無音 :permit

日時: cron iteration (JST 2026-09-04, host load avg 約 40→25 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-9 は facade の caller 指定 `:safety :low` 迂回を実測した。未反証の隣接面は
**分類そのものの欠落**: `kotoba.robotics` の doc は kind を「`:sense` は読み取り専用、
他は hardware を駆動」と宣言し (`robotics.cljc` L56-58)、`safety-classes` は `:none` を
合法 class として含む (L25-29)。`rob/action` は kind と class を**独立に**メンバーシップ
検査するだけで結合不変条件がなく (L64-71)、「actuating kind に `:none` は禁止」が
どこにもない。gate も class メンバーシップしか見ない (L120-129) ため、
`:actuate :none` は完全に合法なレコードとして生成でき、許可セットに `:none` が
入っている呼び出し側では `:permit` 直行するのではないか。
`:none` は正当な用途 (`:sense :none` の読み取り専用) があるため、
修理は「`:none` 削除」では壊れるのが予想 — kind×class 結合検査が必要なはず。

## 実測

コード: `../robotics/src/kotoba/robotics.cljc` (action L60-71 / gate L120-129 /
action-permitted? L131-142) + `src/kotoba/giemon/governor.cljk` facade (L29-33, L54-58)。
実行: `clojure -M -e ...` (giemon deps.edn、pinned robotics)。

```
--- rob/action 直: :actuate :none は例外なく合法レコード
(def a (rob/action "op-x" "op-m-1" :actuate :none :params {:spray "chemical"}))
;; => #:action{:id "op-x" :kind :actuate :safety :none :params {:spray "chemical"}}
:actuates? true                                   ; rob/actuates-hardware? が true を返す hardware action

--- gate は class メンバーシップしか見ないため :none 含み許可セットで permit 直行
(rob/gate a #{:none :low :medium})      ;=> {:gate/decision :permit, :gate/action "op-x"}
(rob/gate a #{:medium :high :safety-critical})  ;=> {:gate/decision :deny, :reason :safety-class-not-allowed}
(rob/action-permitted? a #{:none :low :medium}) ;=> true   (gate 委譲なので同一挙動)

--- facade 経由も同一: 明示 :safety :none がそのまま通る
(gov/ops-action "op-z" "op-m-1" :caterpillar :actuate :safety :none :params {:spray "chemical"})
;;  :action/safety=:none, :action/kind=:actuate
(rob/gate fa #{:none :low :medium})     ;=> {:gate/decision :permit, :gate/action "op-z"}
(rob/gate fa #{:medium :high :safety-critical}) ;=> {:gate/decision :deny ...}
(gov/kaigo-action "ka-1" "ka-m-1" :otete :actuate :safety :none :params {:grip 1})
(rob/gate fk #{:none :low})             ;=> {:gate/decision :permit, :gate/action "ka-1"}

--- 全 actuating kind で同型 (:move / :grasp / :emit)
(rob/gate (rob/action "op-m" "op-m-1" :move :none)  #{:none}) ;=> :permit
(rob/gate (rob/action "op-g" "op-m-1" :grasp :none) #{:none}) ;=> :permit
(rob/gate (rob/action "op-e" "op-m-1" :emit :none)  #{:none}) ;=> :permit

--- 対照 1: 未知 class は action 生成自体が nil (fail-closed 正常)
(rob/action "op-u" "op-m-1" :actuate :ultra-low) ;=> nil

--- 対照 2: :sense :none は正当経路 (:sense は読み取り専用)
(rob/gate (rob/action "op-y" "op-m-1" :sense :none) #{:none}) ;=> {:gate/decision :permit ...}
```

読み取り:
- `:none` は「無分類」でありながら legal class で、actuating kind との結合検査が
  存在しない。`:actuate :none` (薬液噴射パラメータ付き) が例外なく生成され、
  `:none` を許可セットに含む gate 設定で `:permit` 直行する。
- falsify-6〜11 の「欠落/typo/NaN による黙示降格・無音通過」と異なり、これは
  **正しい API 使用そのもの**で成立する迂回 — 呼び出し側の typo や欠落キーを
  fail-closed 化するだけでは塞げない面。rob 単体の `:deny` は許可セット次第で、
  「:none を許可するか」の判断を gate は何も支援しない。
- `:sense :none` の正当用途があるため、修理は class 側削除ではなく
  **kind×class 結合不変条件** (`actuates-hardware?` かつ `:none` → 例外 or gate で
  構造的 deny) が必要。`action-permitted?` は gate 完全委譲なので gate 直すだけで
  一貫する。

## Verdict: refuted

governor gate の「no LLM-to-actuator shortcut」契約に対し、`:safety :none` の
hardware actuate は class メンバーシップ gate を無音で `:permit` する。
`:none` は falsify-6〜11 のような入力破損を要らず、合法レコードのままで迂回する点で
既知の fail-open 系と別経路。robotics の gate 修理 (kind×class 結合検査) または
giemon facade 修理 (actuating kind への `:none` 指定を例外化) まで未修理。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [kotoba.robotics :as rob]) (quote [kotoba.giemon.governor :as gov]))
(def a (rob/action "op-x" "op-m-1" :actuate :none :params {:spray "chemical"}))
(prn (rob/gate a #{:none :low :medium}))
(prn (rob/gate (gov/ops-action "op-z" "op-m-1" :caterpillar :actuate :safety :none :params {:spray "chemical"}) #{:none :low :medium}))'
;; => {:gate/decision :permit, :gate/action "op-x"}
;;    {:gate/decision :permit, :gate/action "op-z"}
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-12 実測 — `:actuate :none` (他 :move/:grasp/:emit も同型) は
合法レコードとして生成でき `:none` 含み許可セットの gate で無音 `:permit`
(入力破損不要の正規 API 経路、falsify-6〜11 の fail-open 系とは別経路)。
修理は kind×class 結合不変条件: `actuates-hardware?` かつ `:none` を
gate 構造的 deny (または action 生成時例外) にすること。`:sense :none` の
正当読み取り経路は温存されること。
