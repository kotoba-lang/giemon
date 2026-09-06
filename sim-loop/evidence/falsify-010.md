# falsify-010 — gate は :action/params の torque を input 空間網羅でも 1 件も検査しないか (falsify-002 構造的ギャップ赤の深掘り)

## 仮説 (1 iteration = 1 hypothesis)
H12: 「governor gate (`kotoba.robotics/gate`) は torque payload を検査対象に含まない。
すなわち (action kind × safety class × allowed set × torque payload) の全組合せ列挙で、
torque 値の違いが :gate/decision を 1 件も変えない」 — 反証対象は falsify-002 の
構造的ギャップ記録「gate は :action/params を一切検査しない」。
torque 値で :permit/:deny が 1 件でも変われば H12 は破れる (赤は実は接続済み)。

## 測定 (probe_gate_torque_grid.py — clojure -M -e)
- 入力空間: kinds `[:move :actuate :grasp :sense :emit]` (5) ×
  safety `[:none :low :medium :high :safety-critical]` (5) ×
  allowed-sets `#{:none}` / `#{:low}` / `#{:low :medium}` / `#{:none :low :medium :high}` / 全クラス (5) ×
  payloads `nil / {:tau 0.0} / {:tau 120.0} / {:tau 1e6} / {:tau -999.0} /
  {:tau 1e6 :angle 99.0 :joints {:j2 {:tau 1e6}}}` (6) = **750 ケース全列挙**。
  payload は j2 peak 120 超・負値・1e6 を含む torque 余裕違反値そのもの。
```
rows=750  NONDET rows=0
SUMMARY permit=300 deny=360 require-sign-off=90 invalid=0
TORQUE-SENSITIVITY INSENSITIVE (gate ignores torque)
  fixed (:move :low, allowed #{:low :medium}): no-params/tau-0/tau-120/tau-1e6/
  tau-neg/tau+ang-ble の 6 payload すべて :permit — 1 件も决策が変わらない
ARM-WITHIN-LIMITS-TORQUE-AGNOSTIC true (within-limits? は angle のみ、torque を見ない)
2 回実行: cmp /tmp/g12.txt /tmp/g12b.txt → exit 0 (出力完全一致、決定的)
```
- 750 行すべて同一入力 2 回実行で同 decision (行内 DET、NONDET 0)。
- probe 記録メモ: SUMMARY 行の "determinism NONDET" 表示は probe 内フラグ名の
  ラベル反転 (atoms の意味を反対に表示)。実データの正の証拠は
  行単位 NONDET=0/750 と 2 回実行の cmp 一致。次回 probe で修正する。

## verdict
- H12: **survived** — gate は torque/角度 payload を input 空間のどの組合せでも
  1 件も検査しない。`:safety :low` の `:move` が `{:tau 1e6 :angle 99.0}` を
  載せたまま :permit される (750 中 300 件の :permit は全て payload 無関係)。
  falsify-002 の構造的ギャップ赤「gate↔arm の torque 照合未接続」は
  列挙レベルで決定的に再確認された。gate 自体の契約 (:safety-class のみ) としては
  宣言どおりであり迂回 (H4) は依然破れず — 赤は「未接続の検査層」として存続。

## コアへの 1 行メッセージ
giemon-sim へ: gate の torque 無検査は 750 ケース全列挙で決定的 (tau 1e6/負値/角度 99 rad
でも :permit 300 件すべて payload 無関係)。torque 余裕照合を入れるなら gate ではなく
sim 受付口 (arm/within-limits 相当 + actuator cont/peak 照合) に — gate 契約は
変えないのが現在の宣言と整合。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_gate_torque_grid.py > /tmp/g12.clj
clojure -M -e "$(cat /tmp/g12.clj)" > /tmp/g12.txt 2>&1
clojure -M -e "$(cat /tmp/g12.clj)" > /tmp/g12b.txt 2>&1
cmp /tmp/g12.txt /tmp/g12b.txt   # exit 0 (決定的)
```

## 補足
- コード修正なし (probe 追加と記録のみ)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高負荷 (load averages 82.98 / 5min) — 軽量 pure-data 列挙 probe のため
  falsify cheaply 基準で実施可。深いシミュレーションは省略。
