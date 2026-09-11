# falsify-20 — bom->json の数値スロットは型検査なしの生補間で、EDN 文字列値が JSON 構造注入として厳格パーサを通過する (偽キー `audit_injected` が監査レコードに混入、構造破壊トークンは無音不正 JSON 出力)

## 仮説

falsify-17 は数値スロットの **非有限値** (`##NaN`/`##-Inf`) を潰した。
未反証の隣接面は**数値スロットへの文字列値**。`bom->json` の
`"cont_nm\":" (or (:cont-nm r) "null")` と `torque->json` の
`"required_nm\":" (:torque/required t)` は `json-str` を経由せず
`(str ...)` 生補間のため、`(:cont-nm a)` が合法 EDN 文字列
(「actuator 定義の typo で文字列を書いた」等の合法リテラル) でも
JSON 構文トークンとしてそのまま出るはず。

1. `:cont-nm "0,\"audit_injected\":true"` → 厳格 JSON パーサが
   **成功**し、監査レコードに偽キーが混入しないか (RFC 8259 適合
   装いの監査改変 — falsify-17 の拒否型より深刻)
2. `:cont-nm "0}"` → 構造破壊で無音不正 JSON が出ないか
3. 対照: `torque->json` 側は `torque-headroom` の `-` 演算で CCE
   になり fail-closed するか (falsify-6 対照経路と同型)

## 実測

コード: `src/kotoba/giemon/export.cljk` — `bom->json` の
`(or (:cont-nm r) "null")` 生補間。実行: `kbb -M -e` (giemon
deps.edn)、fixture は falsify-2〜5 確立の 2 段階 read。検証は
Python `json` (strict)。

```
:face1 cont-nm "0,\"audit_injected\":true"
       出力 j3: {"joint":"j3",...,"cont_nm":0,"audit_injected":true,"peak_nm":150,...}
       Python strict json.load => PARSED-OK、j3 に {"audit_injected": true} 混入   ← 赤
:face2 cont-nm "0}"
       出力 j3: {"cont_nm":0},"peak_nm":150,...  (オブジェクト早期閉鎖)
       Python strict json.load => STRICT-REJECT (JSONDecodeError) — 不正 JSON 無音出力 ← 赤
:face3 torque 側 :effort "40" (文字列)
       torque-headroom の (- (:cont-nm a) effort) で ClassCastException
       (String cannot be cast to Number, arm.cljc:113) — fail-closed (対照)
```

読み取り:

- `bom->json` は数値スロットに **型検査を持たない**。合法 EDN
  文字列リテラルがそのまま JSON 構文として解釈され、
  (a) 厳格パーサ通過型の偽キー混入 (監査レコード改変) と
  (b) 無音不正 JSON 出力の 2 面で破れる。
- face1 は falsify-17 (非有限 → 厳格パーサが例外、可否パーサ依存)
  と異なり **strict ですら通過する**ため、監査用途としてより深刻。
  注入値は正当 EDN リテラル (`:cont-nm` は任意の EDN 値を取り得る)
  で falsify-6/11/17/18 と同一の「合法入力が無音で危険出力」クラス。
- `torque->json` は `torque-headroom` 内の減算が CCE で fail-closed
  (対照)。破れは BOM 出力側 (`bom->json` の price_jpy / peak_nm /
  cont_nm スロット、全部同型の生補間) に集中。
- `csv-cell` 側は `,` を含む文字列を引用するため face1 同値は CSV
  では文字列セルとして往復する (falsify-18 の意味検査不在は別問題)。

## Verdict: refuted

`bom->json` の数値スロット (cont_nm / peak_nm / price_jpy) は
falsify-17 の非有限検査に加え **数値型 (Number かつ finite) 検査**が
必要 — 非数値は例外化または `json-str` 経由の引用文字列化。
修理は falsify-17/18 と同一の export 層入口 1 箇所にまとめられる。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e '
(require (quote [kotoba.giemon.export :as ex]) (quote [clojure.edn :as edn]))
(def base (first (edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def spec (assoc (edn/read-string (:arm/base base))
                 :arm/chain (edn/read-string (:arm/chain base))
                 :arm/realization (edn/read-string (:arm/realization base))))
(def c1 (update-in spec [:arm/chain 2 :joint/actuator :cont-nm]
                   (constantly "0,\"audit_injected\":true")))
(spit "/tmp/f20a.json" (ex/bom->json c1))'
python3 -c "
import json
d=json.load(open('/tmp/f20a.json'))
print(d[2])   # => 偽キー audit_injected: true が混入した監査レコード
"
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-20 実測 — `bom->json` の数値スロット
(cont_nm/peak_nm/price_jpy) は型検査なし生補間で、合法 EDN 文字列が
JSON 構造注入として **厳格パーサ通過型の偽キー混入**
(`cont_nm "0,\"audit_injected\":true"` → 監査レコードに
`audit_injected: true`) と構造破壊不正 JSON (`"0}"`) の 2 面で流出
(strict パーサでも通る点で falsify-17 より深い)。対照: torque 経路は
CCE で fail-closed。修理: falsify-17 の有限性検査を「Number かつ
finite のみ数値スロットに出す」型検査へ拡張 (export 層入口 1 箇所、
falsify-17/18 と同時適用可)。
