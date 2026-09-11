# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-021
- ホスト負荷: load averages 4.78 (1min) / 12.07 (5min) / 16.75 (15min) 開始 (ncpu=10 →
  **中負荷**)。軽量数値解析 probe は実施可と判断し、NEXT だった
  off-diagonal inertia probe (falsify-008) を実行した。長時間シミュレータ実行は
  **skipped (load)**。テスト実行と軽量 seeded 再現は完了 (いずれも正常終了)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜020 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src + test の .clj* への seed/learn/train grep で該当 0 件 — 本回機械再確認)。
  L1 昇格条件は未達、OPEN の赤は解消されず。L0 定着を継続。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を arm_edn_test.clj と同一手順
    (unblob + reconstitute-arm) で再構成、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜020 の :xf/pos 数値と同一 (決定的再現を 19 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. falsify-008 (NEXT 項目の実施 — off-diagonal inertia 0-default 暗黙契約)
- 準備済み probe `probe_offdiag_inertia.py` を実行 (2 回実行 diff なし・決定的)。
- 詳細は `falsify-008.md` に記録。要約:
  - arm6: 0-default 読みで mismatches 0 (数値不一致なし)、ただし strict 読みでは
    6/7 link が落ちる — 暗黙契約のまま実装されておらず構造的赤は未解消。
  - caterpillar: **giemon_caterpillar_facade.urdf は XML コメント内 `--` (line 9)
    のため well-formed でない** — 標準 XML parser で parse 不能、
    caterpillar 側の parity oracle は fixture 修正しない限り成立不能 (新規赤)。
  - parity oracle の Clojure 実装は引き続き存在しない (falsify-001 の赤を再確認)。

## 4. 回帰の有無
- **回帰なし**。bench-001 → … → bench-021 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜021 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 19 点確認
  (本回 bench-021 は load 12.07 (5min)。bench-020 の 22.09、bench-019 の 22.65 より低い)。
- evidence の差分: 前回 (bench-020) 以降、falsify-008.md を新規追加
  (probe_offdiag_inertia.py は同梱済みだったものを実行・記録したもの。probe 自体の変更なし)。
  uncommitted は sim-loop/ のまま。テスト結果には影響なし。

## 5. skipped (load)
- 長時間シミュレータ実行は **skipped (load)**。テスト・軽量再現・falsify-008 軽量 probe での完了。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench021.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
# falsify-008:
python3 sim-loop/evidence/probe_offdiag_inertia.py   # 2 回実行して diff なしを確認
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
- 本回も terminal ツールの stdout が空になる障害が継続しており、コマンド出力を
  一時ファイル (/tmp/giemon_test_021.txt, /tmp/robotics_test_021.txt, /tmp/bench021_host.txt,
  /tmp/bench021_parity.log, /tmp/bench021_seedgrep.txt, /tmp/falsify008_run_021.txt,
  /tmp/falsify008_run_021_b.txt, /tmp/falsify008_deep.txt) 経由で取得して検証した。
  テスト結果の数字はファイルから直接読み取ったものである。
