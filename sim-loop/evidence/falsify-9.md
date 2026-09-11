# falsify-9: governor gate への明示 `:safety` キーワードによる posture 上書き迂回

日時: cron iteration (JST 2026-09-04, host load avg 約 23 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-6/7/8 はすべて facade の **デフォルト解決** `(get-in roles [product :default-safety] :medium)`
経路の迂回だった。未反証の隣接面は **呼び出し側の明示 `:safety` キーワード**:
`ops-action` は `(or safety (get-in ops-roles ...))` で明示指定をそのまま信じ、
product の設定 posture (:caterpillar=:high) に対する再検査が存在しない。
呼び出し側が `:safety :low` を渡せば、同一 gate 許可セットで
デフォルト経路なら `:deny` になるはずの action が `:permit` で通るのではないか。

## 実測

コード: `src/kotoba/giemon/governor.cljk` (L53-60) + `../robotics/src/kotoba/robotics.cljc` gate。
実行: `kbb -M -e ...` (giemon deps.edn、git sha pinned robotics 1d1f93e3)。

```
(def gate-set #{:low :medium})
(def a-override (gov/ops-action "op-1" "op-m-1" :caterpillar :actuate :safety :low :params {:spray "chemical"}))
(def a-default  (gov/ops-action "op-2" "op-m-1" :caterpillar :actuate :params {:spray "chemical"}))

(:action/safety a-override)          ;=> :low
(rob/gate a-override gate-set)       ;=> {:gate/decision :permit, :gate/action "op-1"}
(:action/safety a-default)           ;=> :high
(rob/gate a-default gate-set)        ;=> {:gate/decision :deny, :reason :safety-class-not-allowed}

;; 対照: 正しい ops gate-set #{:high :safety-critical}
(rob/gate a-default  #{:high :safety-critical}) ;=> {:gate/decision :require-sign-off, :gate/safety :high}
(rob/gate a-override #{:high :safety-critical}) ;=> {:gate/decision :deny, :reason :safety-class-not-allowed}

;; kaigo 側も同様に明示 :safety :low が文字列 product でそのまま通る (:action/safety = :low)
```

読み取り:
- 同一呼び出し者・同一 kind (:actuate)・同一 params (薬液噴射) で、
  デフォルト経路は gate-set `#{:low :medium}` により `:deny` なのに、
  `:safety :low` を 1 キーワード渡すだけで `:permit` に変わる。
- robotics gate 契約自体は破れていない (不正クラスは正しく deny/sign-off)。
  迂回は facade が caller 指定 safety を無検査で採用する点のみ。falsify-7/8 と同型の
  fail-open (posture が caller によって黙示的に消去できる) で、修理箇所は同一 facade。

## Verdict: refuted

governor gate の「no LLM-to-actuator shortcut」契約に対し、明示 `:safety` キーワードは
product の設定 posture を黙示的に上書きできる迂回路として機能する。

## 再現手順

```
cd orgs/kotoba-lang/giemon
kbb -M -e '(require (quote [kotoba.giemon.governor :as gov]) (quote [kotoba.robotics :as rob]))
(def a (gov/ops-action "op-1" "op-m-1" :caterpillar :actuate :safety :low :params {:spray "chemical"}))
(prn (rob/gate a #{:low :medium}))'
;; => {:gate/decision :permit, :gate/action "op-1"}
```

## コアへの 1 行メッセージ

falsify-6/7/8 の修理時に `ops-action`/`kaigo-action` は明示 `:safety` 指定も product 設定
posture (:high 等) に対して昇格のみ許可 (降格は拒否または require-sign-off) するよう検証せよ。
