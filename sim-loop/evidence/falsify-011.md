# falsify-011 — sim 受付口は :joints map 形 payload の joint 名・torque 値を
一切照合せず fixture actuator cont/peak 超えでも受理するか (maturity.md NEXT (c))

## 仮説 (1 iteration = 1 hypothesis)
H13: 「`:action/params` の `:joints` map 形 payload (存在しない joint 名 /
文字列・キーワード key 混在 / fixture actuator cont/peak を超える tau /
負値 / 非数値) について、gate も arm 側受付関数も 1 件も照合を行わず、
`:permit` および正常 return される」 — 反証対象は falsify-010 で決定的化した
「未接続の検査層」赤の残り入力空間 (maturity.md NEXT (c): joint 名照合と
sim 側受容経路の不在測定)。payload で decision が変わる、または arm 側で
拒否/例外が 1 件でも起これば H13 は破れる。

## 測定 (probe_joint_payload_reception.py — kbb -M -e)
- 入力空間: `:joints` map payloads 6 種
  (`{"j99" {:tau 1e6}}` 存在しない joint / `{"j2"… :j3…}` 文字列・キーワード key 混在 /
  全 6 joint に tau 1e6 / 負値 tau -500 / 非数値 tau "huge" /
  angle 99 rad + tau 1e6) × kinds `[:move :actuate :grasp]` (3) ×
  safety `[:low :medium :high]` (3) = 54 ゲートケース +
  arm 受付 6 ケース + arm 公開関数 8 個の arglists 実査。
- fixture actuator 定格 (default BOM から実測):
  j1 {cont 40, peak 120} / j2 {40, 120} / j3 {40, 150} / j4 {20, 40} /
  j5 {10, 23.7} / j6 {8.3, 24.8} — すべて payload の tau 1e6 は cont/peak の
  桁外れ超過。
```
RATINGS (["j1" {:cont 40, :peak 120}] ["j2" {:cont 40, :peak 120}]
         ["j3" {:cont 40, :peak 150}] ["j4" {:cont 20, :peak 40}]
         ["j5" {:cont 10, :peak 23.7}] ["j6" {:cont 8.3, :peak 24.8}])
GATE: 54 ケース — :low/:medium は 6 payload 全部 :permit (36 件)、
  :high は allowed-set #{:low :medium} 外で :deny (18 件)。
  decision が payload で変わった数 = 0 (GATE-VARIANTS-BY-PAYLOAD 0)。
  54 件すべて同一入力 2 回実行で同 decision (DET、NONDET 0)。
ARM-RECEIVE: 6 payload すべて "accepted-and-ignored (FK unaffected by payload)"
  — arm 関数は torque payload を持つデータでも例外なく正常 return。
ARM-FN: within-limits? ([joint angle]) / forward-kinematics / end-effector /
  torque-headroom / underrated-joints / chain-actuators / bom / joint-count の
  8 関数が全存在、arglists に torque/params 引数を取るものは 0 個。
WL-ANGLE-ONLY: within-limits? j2 2.2→true / 2.3→false (角度のみ、torque 不問)。
TH-INDEPENDENT-OF-TAU true (torque-headroom は fixture 定格のみから計算)。
2 回実行: diff /tmp/h13.txt /tmp/h13b.txt → 0 行差 (決定的)。
```

## verdict
- H13: **survived** — `:joints` map 形 payload についても gate は 54 ケース
  全件 payload 無関係 (:permit 36 / :deny 18 は allowed-set のみで決まる)、
  arm 側受付関数も 6 payload 全部を例外なく受理し、torque を消費する
  関数は arm の 8 公開関数のどこにも存在しない。存在しない joint 名
  (j99)・key 型混在・tau 1e6 (全 joint の cont/peak を 4 桁超過)・負値・
  非数値文字列のいずれも 1 件も照合されない。
  falsify-002/010 の赤「gate↔arm の torque 照合未接続」は `:joints` map
  入力空間に拡張して決定的。sim 受付口の実装自体が存在しないため
  「不在」の決定的記録として存続 (コア側実装対象)。

## コアへの 1 行メッセージ
giemon-sim へ: `:joints` map 形 payload も照合対象外 — 存在しない joint 名
(j99)・key 型混在・tau 1e6 (全 joint cont/peak を桁外れ超過)・負値・非数値でも
gate 54 ケース :permit 36 件 payload 無関係・arm 関数は全受理 (torque を引数に
取る公開関数 0/8)。torque 余裕照合層は sim 受付口に実装する際 joint 名の
実在確認 + 定格照合の両方を入れる必要がある (現在は両方とも不在)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_joint_payload_reception.py > /tmp/h13.clj
kbb -M -e "$(cat /tmp/h13.clj)" > /tmp/h13.txt 2>&1
kbb -M -e "$(cat /tmp/h13.clj)" > /tmp/h13b.txt 2>&1
diff /tmp/h13.txt /tmp/h13b.txt   # 0 行差 (決定的)
```

## 補足
- コード修正なし (probe 追加と記録のみ。既存 probe・fixture・src は未変更)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 中負荷 (load averages 24.41 29.48 40.09 / 5min) — 軽量 pure-data
  列挙 probe のため falsify cheaply 基準で実施可。深いシミュレーションは省略。
- ツール環境メモ: 本 iteration も terminal stdout が空で返る障害が継続 —
  出力はファイルリダイレクト + read_file で取得。execute_code は cron で
  block のため前回同様 python3 ファイル実行で代替。
