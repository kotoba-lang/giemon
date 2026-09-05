# falsify-7 — governor gate 迂回: `kaigo-action`/`ops-action` の typo 入力で安全クラスが黙示降格する fail-open がないか

## 仮説

`kotoba.giemon.governor` facade (`kaigo-action` / `ops-action`) は
`(or safety (get-in roles [product :default-safety] :medium))` でデフォルト安全クラスを解決する。
product 名や safety クラスを 1 文字でも間違えた入力が、例外を出さずに
**宣言されたポスチャーと異なる安全クラスの well-formed な action を生成**し、
gate に合法アクションとして流れる迂回路になる。

## 実測 (2026-09-03, JST)

実コード (`kotoba.giemon.governor` + `kotoba.robotics`) を clojure -M -e で実行:

1. **typo safety** `(gov/kaigo-action "A1" "M1" :otete :grasp :safety :safety-criticl)`
   → **nil** (`rob/action` が不明クラスで nil を返す)
2. **typo product (kaigo)** `(gov/kaigo-action "A2" "M1" :otete2 :grasp)`
   → `:safety :medium` の action が**無音で生成** (kaigo-roles が全製品 :medium のため
   kaigo 内では影響を観測できない)
3. **typo product (ops)** `(gov/ops-action "A6" "M1" :caterpilar :move)` — 本名 `:caterpillar`、
   ops-roles は :caterpillar に **:high** (化学液・歩行者近接) を宣言
   → **`:safety :medium` の action が無音で生成** (例外なし)
   - `(rob/action-permitted? a #{:low :medium})` → **true** (:medium 許可セットで通過)
   - `(rob/action-permitted? a #{:high})` → false
   つまり :high ポスチャーを要求するはずの操作が、kaigo 既定の許可セット構成では
   :medium として gate を素通しする。
4. **gate 単体は健全**: `(rob/gate nil ...)` → `{:gate/decision :invalid, :reason :not-an-action}`,
   不明クラス action も nil になるため gate 層での迂回は観測されず。

## verdict

**refuted** — giemon governor facade に無音ポスチャー降格の fail-open がある。
product typo で ops-roles の `:high` が `:medium` に黙示的に置き換わり、
その action は well-formed なので gate が拒む根拠を持たない。
(制約: `rob/gate` / `rob/action` 自体の契約は fail-closed で健全。
迂回は facade の `get-in ... :medium` デフォルト経路のみ。)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e "
(require '[kotoba.giemon.governor :as gov] '[kotoba.robotics :as rob])
(prn (gov/ops-action \"A6\" \"M1\" :caterpilar :move)) ; => :safety :medium (本名 :caterpillar は :high)
(prn (rob/action-permitted? *1 #{:low :medium}))        ; => true"
```

## コアへの 1 行メッセージ

giemon-sim へ: `ops-action`/`kaigo-action` は未知 product で無音 `:medium` に降格する
fail-open — 未知 product は例外 (fail-closed) にする修正を検討すること。
(gate 契約 `rob/gate` 自体は nil/不明クラスを正しく拒絶することも実測済み。)
