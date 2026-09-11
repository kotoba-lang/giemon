# falsify-17 — export.cljc の JSON/CSV 監査出力は非有限数 (`##NaN`/`##-Inf`) を生トークンで通し、RFC 8259 違反の無効 JSON と数値破壊 CSV を無音生成する

日時: cron iteration (JST 2026-09-04, host load avg 約 41-54 / コア 10 → 軽量 REPL 測定のみ)

## 仮説

falsify-11 で `:cont-nm` / `:effort` の `##NaN` が headroom に無音侵入する
ことが実測済み。export.cljc は "audit-grade evidence" と自称する
`torque->json` / `bom->json` で数値を `(str ...)` 直接補間のみで
エンコードするため、侵入した非有限数が生トークン `NaN` / `Infinity`
として監査 JSON に出るのではないか:

1. `torque->json`: falsify-11 と同一の `:cont-nm ##NaN` 破損入力
   (合法 EDN リテラル) で `rated_nm` / `headroom_nm` が生 `NaN` に →
   RFC 8259 非合法トークン。緩いパーサは無音受理、厳格パーサは例外。
2. `bom->json` (`chain-bom-rows` 経由) も同一。
3. CSV は `NaN` を文字通り出力し、下流数値パーサで無音破壊される。
4. `##-Inf` は `underrated-joints` には検出されるが、JSON には生
   `-Infinity` が出る。

## 実測

コード: `src/kotoba/giemon/export.cljk` (`torque->json` L71-79 の直接補間、
`bom->json` L109-121 の `(or ... "null")`、CSV は `csv-cell` = `(str v)`)。
実行: `clojure -M -e` (giemon deps.edn)、fixture は falsify-2〜5 確立の
2 段階 read。`##NaN` は j3 の `:joint/actuator :cont-nm` に注入
(合法 EDN リテラル)。検証は cheshire 5.13.0 と Python `json`
(parse_constant=raise、RFC 8259 準拠) の双方で実施。

```
:sanity                正常入力では underrated-joints 0 件、JSON 全行正常
:underrated (NaN 注入) ()                        — falsify-11 と同値、無音 0 件
:headroom (NaN 注入)   j3: :torque/rated ##NaN, :torque/headroom ##NaN
:torque-json (NaN)     [{"joint":"j3",...,"rated_nm":NaN,"headroom_nm":NaN,...}]
                       — 生 NaN トークン (文字列化・引用符化されない)
:torque-json cheshire parse-string → true (寛容パーサは無音受理)
:torque-json Python json parse_constant=raise → INVALID: non-finite token: NaN
:bom-json (NaN)        [{"joint":"j3","model":"Damiao DM-J10010-2EC","cont_nm":NaN,...}]
:bom-json 厳格         INVALID: non-finite token: NaN
:torque-csv (NaN)      j3,30,NaN,NaN
:bom-csv (NaN)         j3,DM-J10010-2EC,NaN,150,54000,...
underrated (##-Inf)    1 件検出 (j3 headroom ##-Inf — neg? で捕捉される面)
:torque-json (##-Inf)  "rated_nm":-Infinity 生トークン (RFC 8259 違反)
```

読み取り:

- `torque->json` / `bom->json` は数値の有限性を一切検査しない。
  falsify-11 の fail-open (`##NaN` 無音侵入) が出力層で増幅され、
  「違反検出 0 件」かつ「監査証拠 JSON が厳格パーサで解釈不能」の二重。
- cheshire は NaN を無音受理するが、RFC 8259 準拠リーダは例外 —
  同一ファイルがパーサにより可/不可が割れ、監査の可搬性契約が破れる。
- CSV は `NaN` を正規の数値セルのように見せる文字列として出力し、
  下流の数値パース (pandas 等) で無音破壊される (`csv-cell` の `\r`
  問題は既に修理済みだが、数値の有限性は見ていない)。
- 対照 (fail-closed 面): `##-Inf` は headroom が負になるため
  `underrated-joints` に 1 件検出される (ただし JSON 出力は依然生
  `-Infinity`)。nil `cont-nm` は JSON 側 `(or ... "null")` で正常化 —
  有限性検査は無い。

## verdict: **refuted** (監査 JSON が `##NaN`/`##-Inf` 生トークンで RFC 8259 違反を出力、厳格パーサで例外・寛容パーサで無音受理、CSV は NaN 正規装いの無音破壊 — falsify-11 の fail-open が出力層で増幅される 3 面を実測)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '
(require (quote [kotoba.giemon.export :as ex]) (quote [clojure.edn :as edn]))
(def base (first (edn/read-string (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))))
(def spec (assoc (edn/read-string (:arm/base base))
                 :arm/chain (edn/read-string (:arm/chain base))
                 :arm/realization (edn/read-string (:arm/realization base))))
(def corrupt (update spec :arm/chain (fn [c] (map-indexed
  (fn [i j] (if (= i 2) (assoc-in j [:joint/actuator :cont-nm] ##NaN) j)) c))))
(prn (ex/torque->json corrupt))'
;; => j3 行に生 NaN トークン。Python: json.load(open(f), parse_constant=raise)
;;    → INVALID: non-finite token: NaN。cheshire parse-string → 無音受理。
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-17 実測 — export.cljc の `torque->json` /
`bom->json` は数値を有限性無検査の `(str ...)` 補間で出すため、
falsify-11 で無音侵入が実測済みの `##NaN`/`##Inf` が生 `NaN` /
`-Infinity` トークンとして監査 JSON に出力される (RFC 8259 違反、
厳格パーサは例外・cheshire は無音受理)。CSV も `NaN` を正規数値セル
装いで出力。修理: falsify-11 と同一箇所 (rated/required 読み取り直後の
`Double/isFinite` 検査) に加え、export 層でも出力直前に非有限数を
例外化 (または `null` / 文字列マーカに正規化) すること。
