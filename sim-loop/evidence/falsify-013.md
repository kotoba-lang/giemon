# falsify-013 — gate の allowed-set 契約エッジ (非 set コレクション / 混在型 set)、
# governor 層経路 (kaigo/ops/safety-critical :emit)、id・mission-id 型エッジでも
# decision は (posture, allowed-set membership) のみで決まり payload 無相関か
# (maturity.md NEXT (c) の継続)

## 仮説 (1 iteration = 1 hypothesis)
H15: 「gate は allowed-set に非 set コレクション (vector / list / sorted-set /
lazy-seq / 文字列 / ネスト seq / 非キーワード要素混在 set) を渡しても、
governor 層 (kaigo-action / ops-action / fall-detected-alert /
chemical-dispense-alert) 経路でも、id・mission-id が nil / 数値 / キーワード
でも、decision は (action/safety, allowed-set membership) のみで決まり、
tau 1e6 payload とは無相関である (例外は安全側 :deny または :invalid)」 —
反証対象は falsify-012 (allowed-set nil/空/set 3 種のみ) の残り入力空間。
payload や governor 経路で decision が変わる、または決定性が破れる
(同一入力で別 decision) ケースが 1 件でもあれば H15 は破れる。

## 測定 (probe_gate_input_contract_edges.py — clojure -M -e)
- 入力空間:
  - Part 1 allowed-set 契約エッジ 9 種 (vector `[:low]` / list / sorted-set /
    lazy-seq / 文字列 `":low"` / `#{:low}` / 混在型 set `#{:low "low" 1}` /
    `#{:high}` / ネスト seq `(seq [[:low]])`)、params は一定 tau 1e6、
    各ケース同一入力 2 回で決定性確認。
  - Part 2 governor 層: kaigo-action (product :caterpillar と未知 :bogus)
    × params {tau 1e6, tau 0} (4 ケース) + 同一 product :caterpillar の
    kaigo (:low 既定) vs ops (:high 既定) 比較 + safety-critical :emit 2 関数
    (fall-detected-alert / chemical-dispense-alert) の tau 1e6 付き gate。
  - Part 3 id/mission-id 型エッジ 6 種 (通常 / nil id / 数値 id / キーワード id /
    nil mission-id / 数値 mission-id)。
  - 合計 21 ケース。
```
ASET (Part 1, 9 ケース): :low を membership に含む非 set コレクション
  (vector / list / sorted-set / lazy-seq) はすべて例外なく :permit、
  混在型 set #{:low "low" 1} も :permit。文字列 ":low" とネスト seq は
  membership miss で安全側 :deny、#{:high} は :deny。
  tau 1e6 payload による decision 変化 0 件。
GOV-KAIGO (4 ケース): 既知 product / 未知 product :bogus のいずれも
  tau 1e6 / tau 0 で同一 :permit (payload 無相関、product は posture 既定に
  のみ影響)。
GOV-DEFAULT-SAFETY: 同一 product :caterpillar・同一 tau 1e6 payload でも
  kaigo 既定 :low → :permit、ops 既定 :high → gate(#{:low :medium}) で :deny
  — decision は posture のみで決まり payload 不問 (製品文脈による既定の
  差分は ADR-2605142300 宣言どおり)。
GOV-SAFETY-CRITICAL: fall-detected-alert / chemical-dispense-alert とも
  allowed-set #{:low :medium :high} を許しても :deny (safety-critical は
  :permit されない)、tau 1e6 payload は params にそのまま伝播
  (payload-carried true)。
ID-EDGE (6 ケース): id/mission-id が nil / 42 / :p3 / 99 でもすべて
  例外なく :permit (tau 1e6 payload 付きのまま)。
GATE-CONTRACT-DETERMINISM-FAILS 0 (同一入力 2 回実行で decision 不一致 0)。
2 回実行: diff /tmp/h15.txt /tmp/h15b.txt → 0 行差 (決定的)。
```

## verdict
- H15: **survived** — allowed-set 契約エッジ 9 種・governor 層 7 ケース・
  id/mission-id 型エッジ 6 種の計 21 ケース全件で、decision は
  (posture, allowed-set membership) のみで決まり tau 1e6 payload と無相関。
  非 set コレクションでも例外を投げず membership で素通りし (:permit)、
  membership miss は安全側 :deny。混在型 set も :permit。governor 層の
  既定 posture 差 (kaigo :low vs ops :high) は decision を変えるが
  payload とは無相関。safety-critical :emit は tau 1e6 を載せたまま
  :deny (安全側)。id/mission-id の型違反も検査されない。
  falsify-002/010/011/012 の赤「gate↔arm の torque 照合未接続」は
  allowed-set 契約面 + governor 層 + id 型面に拡張して決定的。
  決定性も破れず (2 回実行差分 0 行)。

## コアへの 1 行メッセージ
giemon-sim へ: gate の allowed-set は型検査されない — vector/list/sorted-set/
lazy-seq/混在型 set はそのまま membership 評価され :low を含めば :permit、
文字列・ネスト seq は :deny (暗黙の truthy/falsey 依存)。torque 照合層を実装する
際は allowed-set が keyword の set であることの型検証も要る。加えて governor 層の
既定 posture (kaigo :low / ops :high) と id/mission-id の型は無検査で、
tau 1e6 payload は全経路 (safety-critical :emit 含む) をそのまま伝播する —
payload の滅菌点は gate にも governor にも arm にも存在しない。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_gate_input_contract_edges.py > /tmp/h15.clj
clojure -M -e "$(cat /tmp/h15.clj)" > /tmp/h15.txt 2>&1
clojure -M -e "$(cat /tmp/h15.clj)" > /tmp/h15b.txt 2>&1
diff /tmp/h15.txt /tmp/h15b.txt   # 0 行差 (決定的)
```

## 補足
- コード修正なし (probe 追加と記録のみ。既存 probe・fixture・src は未変更)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高負荷 (load averages 84.40 54.97 40.03 / 5min) — 軽量 pure-data
  列挙 probe (21 ケース、物理シミュレーションなし) のため falsify cheaply
  基準で実施可。深いシミュレーションは省略。
- probe 実装メモ: 初版の Part 3 を map リテラルで書くと key 衝突
  (Duplicate key: m1) で落ちたため vector of triples に修正 (実データに影響なし)。
- ツール環境メモ: 本 iteration も terminal stdout が空で返る障害が継続 —
  出力はファイルリダイレクト + read_file で取得。execute_code は cron で
  block のため python3 ファイル実行で代替。
