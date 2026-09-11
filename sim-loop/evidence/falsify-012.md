# falsify-012 — gate はアクション構造エッジ (params 非 map / nil / 深入れし
# torque 隠し / safety・kind・mission の型違反 / allowed-set nil・空) でも
# torque を一切照合せず decision が payload 無相関か (maturity.md NEXT (c))

## 仮説 (1 iteration = 1 hypothesis)
H14: 「gate はアクション自体の構造エッジ — `:params` が nil / vector /
文字列 / キーワード / 深入れし map 内に隠した torque / トップレベル tau /
巨大 map / safety が文字列・nil・未知キーワード・数値 / kind が未知・nil・
文字列 / mission が nil・キーワード・数値 / allowed-set が nil・空 —
のいずれでも torque payload を一切照合せず、decision は
(safety, allowed-set) のみで決まり payload・構造無相関である」 —
反証対象は falsify-011 の「未接続の検査層」赤の残り入力空間
(アクション構造面)。payload や構造で decision が変わる、または
決定性が破れる (同一入力で別 decision) ケースが 1 件でもあれば H14 は破れる。

## 測定 (probe_gate_structural_edges.py — kbb -M -e)
- 入力空間:
  - Part 1 構造エッジ: `:params` 8 種 (nil / vector `[{:joints {"j2" {:tau 1e6}}}]` /
    文字列 `"{:joints {:tau 1e6}}"` / キーワード `:torque` /
    深入れし `{:a {:b {:c {:d {:joints {"j2" {:tau 1e6}}}}}}}` /
    トップレベル `{:tau 1e6}` / 200 key の巨大 map (全値 1e6) /
    `{:joints {"j2" {:tau 1e6 :extra {:x 1}}}}`)
    × kinds `[:move :actuate :grasp]` (3) × safety `[:low :medium :high]` (3)
    = 72 ゲートケース (各ケース同一入力 2 回で決定性確認)。
  - Part 2 型違反: safety 4 種 (`"low"` / nil / `:bogus` / 1.0) × kind 4 種
    (`:move` / `:fly` / `"move"` / nil) × mission 4 種 (`"m1"` / nil / `:m1` / 42)
    = 64 ケース (params は一定 `{:joints {"j2" {:tau 1e6}}}`)。
  - Part 3 allowed-set エッジ: nil / `#{}` / `#{:low}` / `#{:low :medium :high}`
    の 4 ケース (params は tau 1e6)。
  - 合計 140 ケース (STRUCT-GATE-CASES 140)。
```
STRUCT (Part 1, 72 ケース): :low → 24 件すべて :permit、
  :medium → 24 件すべて :permit、:high → 24 件すべて :deny。
  params が nil でも vector でも文字列でも tau 1e6 をどこに隠しても
  (:tau 1e6 トップレベル・深入れし 5 層・巨大 map) decision 変化 0 件。
TYPE-EDGE (Part 2, 64 ケース): すべて :invalid — safety/kind/mission の
  型違反は gate が :invalid で一様に拒否し、tau 1e6 payload の有無とは無関係
  (:invalid は permit も deny も迂回しない安全側判定)。
ALLOWED-SET (Part 3): nil → :deny、#{} → :deny、#{:low} → :permit、
  #{:low :medium :high} → :permit — tau 1e6 を載せたまま allowed-set のみで決定。
STRUCT-GATE-DETERMINISM-FAILS 0 (Part 1 の 72 ケース 2 回実行で decision 不一致 0)。
2 回実行: diff /tmp/h14.txt /tmp/h14b.txt → 1 行差のみ (1 回目に付加した
  `EXIT:0` エコー行、clojure 出力本体は 0 行差 — 決定的)。
```

## verdict
- H14: **survived** — gate はアクション構造エッジ 140 ケース全件で
  torque payload と構造に無相関。:params が nil/非 map でも例外も :invalid も
  返さず :permit され (深入れし 5 層の tau 1e6・トップレベル tau 1e6・
  200 key 巨大 map を含む)、型違反は :invalid 一様拒否 (payload 無関係)、
  allowed-set nil/空は安全側 :deny。決定性も破れず (2 回実行差分 0 行)。
  falsify-002/010/011 の赤「gate↔arm の torque 照合未接続」はアクション
  構造面に拡張して決定的。sim 受付口の実装自体が存在しないため「不在」の
  決定的記録として存続 (コア側実装対象)。

## コアへの 1 行メッセージ
giemon-sim へ: gate は `:params` 非 map (nil/vector/文字列/キーワード) や
深入れし構造に隠した tau 1e6 も一切照合せず :permit する (72 ケース decision
変化 0、型違反は :invalid 一様・payload 無関係、allowed-set nil/空は :deny、
決定性差分 0 行)。torque 照合層を sim 受付口に実装する際は `:params` が
map であることの型検証 + torque key の深さ制限も要る (現在は構造検査自体が不在)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
python3 sim-loop/evidence/probe_gate_structural_edges.py > /tmp/h14.clj
kbb -M -e "$(cat /tmp/h14.clj)" > /tmp/h14.txt 2>&1
kbb -M -e "$(cat /tmp/h14.clj)" > /tmp/h14b.txt 2>&1
diff /tmp/h14.txt /tmp/h14b.txt   # clojure 出力本体 0 行差 (決定的)
```

## 補足
- コード修正なし (probe 追加と記録のみ。既存 probe・fixture・src は未変更)。
- 決定的記述のみ、タイムスタンプなし。
- HOST LOAD 高負荷 (load averages 84.39 70.12 53.49 / 5min) — 軽量 pure-data
  列挙 probe (140 ケース、物理シミュレーションなし) のため falsify cheaply
  基準で実施可。深いシミュレーションは省略。
- ツール環境メモ: 本 iteration も terminal stdout が空で返る障害が継続 —
  出力はファイルリダイレクト + read_file で取得。execute_code は cron で
  block のため python3 ファイル実行で代替。
