# falsify-13 — 許可セットに混入した `nil` が `:action/safety nil` の生マップ action を無音 :permit

日時: cron iteration (JST 2026-09-04, host load avg 約 25-28 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-12 は gate の第 1 引数 (action) 側の kind×class 結合欠落を潰した。
未反証の隣接面は**第 2 引数 (allowed-set) 自体の破損**: `rob/gate` は
`(set allowed-safety-classes)` で無条件に set 強制し、メンバーシップ以外の
検査を一切しない (robotics.cljc L120-129)。ここで

1. 許可セット構築側が nil や破損値を混入させても黙って通るか
2. `:action/safety` が nil の生マップ (rob/action を経由しない map) が
   その nil メンバーシップと合致して `:permit` に到達しないか

を測定する。rob/action は未知 class で nil を返す (fail-closed 済み) ため、
nil-safety action は生マップでしか作れない点も確認する。

## 実測

コード: `../robotics/src/kotoba/robotics.cljc` (gate L120-129 /
action-permitted? L131-142)。実行: `kbb -M -e ...` (giemon deps.edn、pinned robotics)。

対象 action: `(rob/action "op-x" "op-m-1" :actuate :none {:spray "chemical"})`
(正規生成、`:action/safety :none`)。

```
:baseline           #{:none :low :medium}   => {:gate/decision :permit, :action "op-x"}   (既知: falsify-12)
:nil-set            nil                     => {:decision :deny, :reason :safety-class-not-allowed}  (fail-closed 正常)
:empty-set          #{}                     => {:decision :deny, ...}                                (fail-closed 正常)
:string-set         "medium"                => {:decision :deny, ...}   ("m"/"e"... にヒットせず deny)
:keyword-set        :medium                 => IllegalArgumentException (ISeq 生成不能, fail-closed)
:number-set         42                      => IllegalArgumentException (同上)
:map-set            {:none true :low true}  => {:decision :deny, ...}   (keyword は map のキー検索に一致しない)
:list-set           (:none :low)            => {:gate/decision :permit, :action "op-x"}  (set 強制で合法に通る)
:vec-set            [:none :low]            => {:gate/decision :permit, :action "op-x"}  (同上)
:nil-in-set         (conj #{:low :medium} nil) => {:decision :deny, ...}    (nil-safety ではない正規 action は deny)
:permitted-nil-set  action-permitted? a nil => false (gate 委譲で一貫)
:signoff-ctrl       :high action + #{:high :medium} => :require-sign-off (正常)

--- 赤: 生マップ + nil 含み許可セット
(def raw {:action/id "op-h" :action/mission "op-m-1" :action/kind :actuate
          :action/safety nil :action/params {}})
(rob/gate raw (conj #{:low :medium} nil))  => {:gate/decision :permit, :action "op-h"}
(rob/gate raw #{:low :medium})             => {:decision :deny, ...}   (nil セット無しは deny — 経路は nil メンバーシップのみ)
(rob/gate (assoc raw :action/safety :none) #{:none}) => :permit (対照: nil の代わりに :none なら falsify-12 と同型)
```

読み取り:
- gate は allowed-set を検証せず `(set x)` で素通しするため、**許可セットに
  `nil` が混入している構成では `:action/safety nil` の生マップ action が
  `nil = nil` のメンバーシップ一致で無音 `:permit` する**。
  kind は actuating (`:actuate`) でよい — falsify-12 の kind×class 結合欠落と
  疊なって、nil-safety の hardware actuate が gate を通る。
- 許可セット単独の破損 (nil / 空 / 文字列 / 数値 / map) はすべて deny または
  例外で fail-closed と実測 — 迂回に必要なのは「nil 含みセット ∧ nil-safety 生マップ」
  の**両方**。rob/action は nil-safety action を生成できない (未知 class → nil) ので、
  第 1 要件は gate が生マップを受け入れること (`(not (map? a))` しか見ない) が担う。
- リスト/ベクタの許可セットは set 強制で正しく機能する (堅牢、問題なし)。
- falsify-6〜11 の欠落系・falsify-12 の正規 API 経路と異なり、これは
  **gate 入力 2 つの組合せ破損**経路。単独ではどちらも通らない。

## Verdict: refuted

`:none` メンバーシップ経路 (falsify-12) に加え、許可セットの `nil` メンバーシップ
経路でも無音 `:permit` が実測された。成立条件は限定されるが (nil-safety 生マップ +
nil 含み許可セットの両方)、gate の契約「class メンバーシップで permit/deny を決める」
に対し、nil 同士の一致が permit を意味するのは構造的な穴。
`rob/gate` は allowed-set から nil を除去するか、`(:action/safety a)` が nil の
action を `:invalid` に落とす (または両方) まで未修理。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '(require (quote [kotoba.robotics :as rob]))
(def raw {:action/id "op-h" :action/mission "op-m-1" :action/kind :actuate
          :action/safety nil :action/params {}})
(prn (rob/gate raw (conj #{:low :medium} nil)))'
;; => {:gate/decision :permit, :gate/action "op-h"}
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-13 実測 — `rob/gate` は allowed-set を無検査で `(set x)`
強制するため、許可セットに nil が混入した構成では `:action/safety nil` の生マップ
action (rob/action 非経由) が nil メンバーシップ一致で無音 `:permit`
(actuating kind で成立、許可セット単独破損や正規生成 action では fail-closed と対照)。
修理は gate 側: allowed-set から nil/非 keyword の除去検査、または
`:action/safety` nil の action を `:invalid` 化 (両方推奨)。
falsify-12 の kind×class 結合検査と並行で適用されること。
