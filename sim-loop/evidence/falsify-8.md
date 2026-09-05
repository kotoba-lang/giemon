# falsify-8 (日次連番 8)

## 仮説

falsify-7 は未知 **keyword** product の `:medium` 黙示降格のみ実測した。
未検の隣接経路 — **product=nil** と **product が文字列** (`"caterpillar"`) — も
`get-in ops-roles [product :default-safety] :medium` のデフォルト解決で
黙示 `:medium` に落ち、`rob/gate` を `:permit` で通る (fail-open)。

## 実測

再現コマンド:

```
cd orgs/kotoba-lang/giemon && clojure -M -e "
(require '[kotoba.giemon.governor :as gov] '[kotoba.robotics :as rob])
(def allowed #{:low :medium})
(:action/safety (gov/ops-action \"a1\" \"m1\" :caterpillar :move))      ; 対照
(:action/safety (gov/ops-action \"a2\" \"m1\" nil :move))               ; nil product
(:gate/decision (rob/gate (gov/ops-action \"a2\" \"m1\" nil :move) allowed))
(:action/safety (gov/ops-action \"a3\" \"m1\" \"caterpillar\" :move))   ; 文字列 product
(:gate/decision (rob/gate (gov/ops-action \"a3\" \"m1\" \"caterpillar\" :move) allowed))
(gov/kaigo-action \"a4\" \"m1\" :otete :move :safety \"medium\")        ; 文字列 safety"
```

実測値:

| 入力 | 生成 action safety | gate (`#{:low :medium}`) |
|---|---|---|
| 対照: `:caterpillar` (keyword) | `:high` | (許可セット外 → :deny が本来の意図) |
| `nil` product | `:medium` | **:permit** |
| `"caterpillar"` (文字列) | `:medium` | **:permit** |
| 文字列 safety `"medium"` | action 生成 **nil** | gate(:nil) → :invalid (fail-closed) |

解釈: ops-roles は同一 product `:caterpillar` に `:high` (街並み清掃・公衆空間・
薬液散布と ADR-2605142300 相当の危険度根拠付きで宣言) を与えている。
keyword/文字列混同や nil 伝播という統合バグ 1 個で `:high` → `:medium` に
黙示降格し、厳格な許可セットの下では本来 sign-off/deny になる action が
`:permit` で通る。rob 側は正しく fail-closed (`rob/action` は未知 safety で nil、
`rob/gate` は nil action で :invalid) — 迂回路は giemon facade の
`(get-in ... :medium)` デフォルト解決のみ。falsify-7 (typo keyword) と
同一クラスの第 2・第 3 経路の追加実測。

## verdict: **refuted**

(product=nil と文字列 product の 2 経路で、危険側 postures の黙示降格 + gate permit を実測)

## コアへの 1 行メッセージ

`kaigo-action`/`ops-action` の `(get-in roles [product :default-safety] :medium)` は
未知 keyword・typo・nil・文字列 product のすべてで黙示 `:medium` に降格するため、
既知 product 以外は例外 (fail-closed) にする修理が falsify-7 の修正と同時に必要。
