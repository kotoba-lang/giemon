# falsify-030 — H32: 監査用 export 層 (torque->json/csv, bom->json/csv) は数値フィールドの NaN/±∞ を silent に不正 JSON / 往復不能 CSV として出力するか

## 仮説 (1 iteration = 1 hypothesis)
H32: 「監査用 evidence の出口である export 層 (`export.torque->json` / `torque->csv` /
`bom->json` / `bom->csv`) は、数値フィールド (`:torque/headroom` / `:torque/rated` /
`:torque/required` / `:cont-nm` / `:price-jpy`) の **非有限値 (NaN/±∞)** を silent に
**不正 JSON / 往復不能 CSV** として出力する」。すなわち「export 層に数値の finite 検査
(isNaN / isInfinite / finite?) があり、NaN/±∞ を拒否・loud 化・別表現する」という代替仮説は
成立しない、という予測。

H29/H30 (FK NaN silent NaN pose 化・検知面 0 件) は**角度列**の NaN を扱い、
export 層 (`arm/torque-headroom` 経由の `:cont-nm` / `:joint/limit :effort` と
`chain-bom-rows` 経由の `:arm/chain` 直読) は FK を呼ばない void (falsify-025/026)。
従って export の**数値フィールド** NaN は未監査の独立次元。

判定規則: export test 群 (test/kotoba/giemon/export_test.cljc) に
NaN/±∞ の**数値フィールド**を入力し、その有限性・JSON 妥当性・CSV 往復を
assert する de facto な test ケースが 1 件でもあれば survived、皆無なら refuted。
(current fixture の数値は全部有限 — 潜在赤、非発火の framing は H19〜H31 と同型。)

## 実測 (source-deterministic; 行レベル静的読取・負荷非依存・決定的)
実行バックエンド (terminal / search / sandbox stat) が応答不能 (HOST LOAD
101.29 / 64.92 / 76.54、ncpu=10; bench-069〜085 同型条件) のため REPL 実行は
honesty-first で skipped。本仮説は export 実装 + export test の逐読で完全に確定でき、
決定的 (REPL 実行) 数字を捏造しない。read_file (実在 src/test/fixture) を盤に実施。

### 数値フィールドの serialization 面 (export.cljc 行レベル)
- **(a) `torque->json` (71–79)**: `headroom_nm` は `(:torque/headroom t)` を
  **非引用の裸数値**として `str` 連結 (行 77)。`required_nm` (76) / `rated_nm` (78) も同型。
  ここに `isFinite?` / `isNaN` / 数値判定は **皆無**。
  → headroom/rated/required のいずれかが NaN/±∞ なら `"headroom_nm":##NaN` /
  `"headroom_nm":##Inf` と**不正 JSON** (RFC 8259 は `####NaN` を数値として許可しない)
  を silent 出力。
- **(b) `torque->csv` (53–58)**: 同 3 数値を `csv-cell` → 非引用裸数値として join (行 57)。
  → NaN/±∞ はそのまま文字列化され、CSV 読取で数値型に往復できず **silent 往復不能**。
- **(c) `bom->json` (109–121)**: `:cont-nm` (117) / `:price-jpy` (119) は
  `(or (:cont-nm r) "null")` のみ — nil は "null" に変わるが **NaN/±∞ は (truthy で
  nil でない) そのまま str され不正 JSON** (finite 検査なし)。`:peak-nm` (118) も同型。
- **(d) `bom->csv` (98–107)**: `:cont-nm` / `:peak-nm` / `:price-jpy` を
  `csv-cell` (nil→"") のみ — NaN/±∞ は裸で poke (有限検査なし)。往復不能。
- **(e) `csv-cell` (8–18)**: RFC-4180 の引用対象は **文字列フィールドの制御文字
  (comma / quote / CR / LF) のみ** (行 16 の正規表現 `[",\n\r]`)。**数値の非有限性は
  引用条件に現れない** — NaN/±∞ は quoted も finite 変換もされず裸のまま。

### NaN/±∞ 数値フィールドの test oracle 集計 (test/kotoba/giemon/export_test.cljc 1–71)
- **全 test (products->csv 10–13 / torque->csv 15–17 / csv-CR 19–29 /
  products->json 31–33 / torque->json 35–39 / json-C0 41–51 / bom->csv 59–64 /
  bom->json 66–71)** を逐読した結果、数値フィールドに入るのは**正常有限値のみ**
  (10 / 20 / 60 / 42000 / 28000 / 30)。
- `Double/NaN`・`##NaN`・`##Inf`・`##-Inf`・`isNaN`・`isInfinite`・`finite?`・
  Math/NaN 比較を数値フィールドに入力する assert は **1 件も無い**。
- 既存 test の守備範囲は**文字列フィールド (joint 名) の制御文字エスケープ**
  (csv-CR 19–29、json-C0 41–51 — いずれも green、RFC-4180/RFC-8259 準拠確認済み)
  に集中し、**数値フィールドの非有限性は文字列制御文字と独立の un-tested 面**。

### データ到達性 (潜在赤の発火条件)
- `:torque/headroom` = `(- :cont-nm :joint/limit :effort)` (arm.cljc 113) —
  両者 NaN なら差分 NaN。current fixture (giemon_arm6.edn) の `:cont-nm`/`:effort` は
  全 joint 有限 (40/40/40/30/…、行レベル確認) のため**現 fixture では非発火**。
- `chain-bom-rows` (export.cljc 81–96) は `:arm/chain` 直読 — future DR / variant /
  importer が NaN 付き actuator を持ち込めば `bom->json/csv` で silent に不正出力。
  → falsify-019/020/021 の「DR / variant / importer 将来経路で発火」framing と同型の潜在赤。

## verdict: **refuted**
H32 は成立: 監査用 export 層の数値フィールドに **finite 検査が皆無**で、NaN/±∞ を
silent に不正 JSON (`"headroom_nm":##NaN`) / 往復不能 CSV として出力する。
`torque->json` 71–79 は headroom/rated/required を非引用裸数値で str、`bom->json`
109–121 は cont-nm/peak-nm/price-jpy を `(or ... "null")` のみ (nil→null、NaN/±∞ は
truthy で裸 str)、`csv-cell` 8–18 の RFC-4180 引用は**文字列制御文字のみ**で数値の
非有限性は対象外。export test 層 (export_test.cljc 1–71、全部 green) は**文字列
置換・制御文字エスケープの強固な oracle** を持つ一方、**数値フィールドの NaN/±∞ を
入力・検証する oracle は 0 件** — 監査用 evidence の「audit-grade」保証が数値の
非有限性では破れる。H29/H30 の角度列 NaN と独立の**数値 serialization 破れ**。
現 fixture は有限のため非発火、将来の DR / variant / importer 経路の numeric contract。

## コア (giemon-sim) への 1 行 message
falsify-030: H32 refuted — 監査用 export 層 (torque->json/csv, bom->json/csv) の
数値フィールドに finite 検査が皆無で、NaN/±∞ を silent に不正 JSON (`##NaN`) / 往復不能
CSV として出力する (csv-cell の RFC-4180 引用は文字列制御文字のみ、export_test は文字列
エスケープは green でも数値 NaN oracle 0 件)。数値フィールドの finite guard (or JSON
`null` / rejection) 導入判断はコア側。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
# 本イテレーションは実行バックエンド (terminal/search/sandbox stat) が応答不能
# (bench-069〜085 同型条件、HOST LOAD 101.29 / 64.92 / 76.54、ncpu=10) のため REPL 実行は
# honesty-first で skipped。H32 は export 実装 + export test の行レベル静的読取のみで確定 —
# 実行数字を捏造せず「静的読取」として記録。
# 環境回復後に以下を byte 一致で読めば各面の確定内容を再確認できる:
#   src/kotoba/giemon/export.cljc 8–18 (csv-cell: RFC-4180 引用は [,",\n,\r] のみ、数値対象外),
#     53–58 (torque->csv: 裸数値 join), 71–79 (torque->json: headroom/rated/required 裸 str),
#     81–96 (chain-bom-rows: :arm/chain 直読), 98–121 (bom->csv/json: 裸数値 / (or ... "null"))
#   test/kotoba/giemon/export_test.cljc 1–71 (全数値フィールドは正常有限値のみ、NaN/∞ 0 件)
#   fixtures/giemon_arm6/giemon_arm6.edn (:cont-nm / :effort 全 joint 有限)
# 検索: grep -n "##NaN\|##Inf\|isNaN\|Double/NaN\|finite" test/kotoba/giemon/export_test.cljc → 0 件
```

## 補足
- コード修正なし (測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- 集計スコープの honesty 注記: search_files / shell が応答不能のため test ツリー全体の
  機械列挙は不能。本 falsify は export 層 + export test の逐読に基づく bound 付きの確定で、
  export が FK を呼ばない void (falsify-025/026) と整合する。文字列制御文字エスケープの
  oracle は csv-CR / json-C0 (export_test 19–29, 41–51) が既に green でカバー済み。
- HOST LOAD 高 (pre-run 1min 101.29 / 5min 64.92 / 15min 76.54、ncpu=10)。
  read_file (実在 src/test/fixture) のみ成立したため静的読取は盤に実施。test スイート /
  seeded 再現は一律 skipped (honesty-first、決定的数字を捏造せず、基準値保持の判定は
  bench-066 確定値: robotics 14/50/0、giemon 46/115/0)。
- NEXT: H32 の確定 (falsify-030) をもって next を進めて可。次候補は export 数値フィールド
  finite guard の導入判断 (falsify-019/020/021/029 の DR/variant/importer 将来経路 framing と
  同型) と、backend 復旧後の test スイート + seeded 再現の本測定 (bench-086 以降で実施予定)。