# falsify-18 — export.cljc の CSV 出力は CSV formula injection を無音通過させる (=/+/-/@/タブ先頭セルが引用有無にかかわらず危険値のまま往復、RFC 4180 適合のみで悪意値検査なし)

## 仮説

falsify-17 が非有限数 (出力値の破壊) を実測したのに対し、`csv-cell` は
フィールド内容の **意味** を一切検査していない。`:model` / `:buy` は
オペレータ供給の文字列であり、Excel/Sheets 等のスプレッドシートアプリは
`=` `+` `-` `@` (またはタブ) で始まるセルを数式として実行する。
RFC 4180 の引用規則を満たした CSV でも formula injection は成立する
はず (適合性と安全性は別次元)。

1. `bom->csv` で `:joint/actuator :model` に `"=1+1"` を注入 → CSV セル
   に生値のまま出る。
2. `"=HYPERLINK(\"http://evil.example\",\"x\")"` は引用されるが引用内
   でも `=` 先頭のまま → パーサ read-back で危険値が復元される。
3. 危険接頭辞ファミリー `= + - @ \t` が全滅で通る。
4. 対照: `bom->json` は `json-str` (制御文字エスケープ) で同一入力が
   厳格 JSON パーサで安全往復 → 注入面は CSV のみ。

## 実測

コード: `src/kotoba/giemon/export.cljc` — `csv-cell` L8-18 は
`re-find #"[\",\\n\\r]"` の 3 文字のみ検査 (L16 のコメント自体が
「RFC 4180 requires」を根拠に `\r` 追加を主張しており、意味検査の
不在は規準にすら入っていない)。実行: `clojure -M -e` (giemon
deps.edn)、fixture は falsify-2〜5 確立の 2 段階 read。注入先は
`:arm/chain 2` (j3) の `:joint/actuator`。検証は Python `csv` モジュール
(read-back) と `json` (strict) で実施。

```
:sanity             正常 j6 行 "j6,CubeMars AK70-10 / Unitree GO-M8010-6,8.3,24.8,60000," — 変化なし
bom->csv ":model" "1+1"     j3 行 raw:  j3,=1+1|cmd,40,150,54000,Foxtech(在庫あり) $357
                            — 引用なし生トークン。Python csv read-back '=1+1|cmd'
bom->csv ":model" "=HYPERLINK(...)"   j3 行 raw: j3,"=HYPERLINK(""http://evil.example"",""x"")",...
                            — RFC 4180 適合に引用されるが read-back は
                              '=HYPERLINK("http://evil.example","x")' 危険値そのまま
危険接頭辞 5 形状 read-back (=1+1 / +1+1 / -1+1 / @SUM(1) / \t=1+1)
                            全て先頭1文字が危険クラス (=,+,-,@,タブ) のまま復元 — 5/5 通過
tab 先頭 "a\tb"             csv-cell はタブを引用せず生タブで出力、read-back 'a\tb'
                            (csv-cell は \r 追加のみでタブ無検査 — 拙速修理の残り面)
bom->json 同一 ":model" 入力  Python json strict parse OK、j3 model 値は文字列として完全往復 — 無害
```

読み取り:

- `csv-cell` は「引用すべき 3 文字」の構文規則のみを持ち、フィールド
  が数式解釈されるという **意味的危険** を全く検査しない。引用は
  formula injection を防止しない (引用内の `=` セルは Excel/Sheets が
  依然数式として評価する)。
- 注入経路は正当 EDN リテラル (`:model` は文字列バリュー) で、
  falsify-6/11/17 と同一の「合法入力が無音で危険出力」クラス。
  非有限数 (falsify-17) に続き、危険文字列も無検査で監査 CSV に流出。
- JSON 側は `json-str` の制御文字エスケープで同一入力が strict
  パーサで安全往復する — 破れは CSV 出力に限定される。
- 対照 (fail-closed 面): `,` `"` `\n` `\r` は引用で正しく往復する
  (falsify-17 までの `\r` 修理は機能している)。破綻は意味検査不在の
  み。

## verdict: **refuted** (CSV 出力が formula injection を無音通過: `=`/`+`/`-`/`@`/タブ先頭のオペレータ供給文字列が引用の有無にかかわらず read-back で危険値そのまま復元 — RFC 4180 適合と安全性の混同。対照: bom->json は同一入力で strict JSON 往復無害、破れは CSV 層のみ)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '
(require (quote [kotoba.giemon.export :as ex]) (quote [clojure.edn :as edn]))
(def base (first (edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def spec (assoc (edn/read-string (:arm/base base))
                 :arm/chain (edn/read-string (:arm/chain base))
                 :arm/realization (edn/read-string (:arm/realization base))))
(def corrupt (update-in spec [:arm/chain 2 :joint/actuator :model]
                        (constantly "=HYPERLINK(\"http://evil.example\",\"x\")")))
(spit "/tmp/f18.csv" (ex/bom->csv corrupt))'
python3 -c "
import csv
rows=list(csv.reader(open('/tmp/f18.csv')))
print(rows[3][1])   # => =HYPERLINK(\"http://evil.example\",\"x\")  ←危険値が復元
"
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-18 実測 — `export.cljc` の `csv-cell` は
`,"` `\n` `\r` の 3 文字構文検査のみでフィールドの意味検査を持たず、
`:model` / `:buy` (オペレータ供給文字列) 先頭の `=` `+` `-` `@` /
タブが引用の有無にかかわらずそのまま監査 CSV に出て read-back で
危険値が復元される (CSV formula injection、Excel/Sheets で数式評価
される値)。JSON 側 (`bom->json`) は同一入力で strict 往復無害 —
破れは CSV 層のみ。修理: `csv-cell` (または出力直前の row 正規化)
で危険接頭辞 (= + - @ およびタブ) を検出したフィールドは
単引用符/エスケープ前置などのスプレッドシート安全化 (または例外化)
を追加 — falsify-17 の数値有限性検査と同時に export 層の入口で
1 箇所にまとめられる。タブ自体も csv-cell の引用対象外のまま
(falsify-17 の `\r` 修理で `\r` は入ったが `\t` は CSV では引用不要
という判断の裏付けがなく、タブ先頭は数式トリガ)。
