# bench-068

- 測定日: 2026-09-06 JST
- HOST LOAD (uptime 記載、5 秒間隔再計測): 開始時 1min 52.88 / 5min 63.34 / 15min 85.20、
  再計測 58.95→54.79→56.89 (1min)。ncpu=10。高負荷だが bench-064/067 の再実行条件
  (load 1min < 60 程度) を開始時点で満たしたため、通常実行を試行。
- 実行コマンド: `clojure -M:test` (robotics, giemon) → **通常実行 (成功、exit 0)**。
- seeded 再現: `clojure -M -i /tmp/seed_parity_bench068.clj` → **SEED-PARITY true**。
- 長時間シミュレータ実行・probe (falsify 系) 隔線再実行は **役割外 / 省略** (bench-059〜067
  と同じ扱い。コード・測定追加を伴う実装側タスクのため本 bot は実施しない)。

## テスト数字
- robotics: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)
- giemon:   **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)
- 根拠: /tmp/bench_test_robotics.log、/tmp/bench_test_giemon.log から直接読み取り。

## 再現 verdict (seeded / sim-loop 学習ジョブ)
- **pass (軽量範囲)**。sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (git head d0d3cb4 = bench-062〜067 と同一、committed diff 空、機械確認)。
  L1 昇格条件未達 → L0 据え置き。
- 軽量 seeded 再現 (既存決定的関数 `kotoba.giemon.arm/end-effector` の同入力 2 回実行照合):
  giemon_arm6 fixture を unblob + reconstitute-arm で再構成、q=[0.0 0.2 -0.3 0.0 0.5 0.0]。
  結果 **SEED-PARITY true**、:xf/pos [0.035165560086391295 0.0 0.6104766433183229]、
  :xf/rot は bench-002〜066 と同一 (決定的再現を 63 点目として一致確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 回帰の有無
- **回帰なし**。bench-001 → … → bench-068 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
  bench-068 は高負荷 (開始 1min 52.88 / 5min 63.34 / 15min 85.20) でも 2 スイートとも
  bench-066/067 基準値と同一、seed parity (:xf/pos 63 点目一致) も同一。
- git diff 空・git head d0d3cb4 同一を機械確認 (コード修正なし)。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench068.clj
```

## 補足
- コード修正なし (ベンチ・記録のみ)。決定的記述のみ、タイムスタンプ非依存。
- terminal ツールの foreground stdout が空になる障害が継続しているため、コマンド出力を
  一時ファイル (/tmp/*.log, /tmp/*.txt) 経由で取得して検証した。
- /tmp/seed_parity_bench066.clj を /tmp/seed_parity_bench068.clj に複製して使用
  (内容は bench-002〜066 と同一)。
- NEXT: H26 「FK は角度列と chain 長の不一致を検証しない」を測る (maturity.md 記載の通り、
  測定・実装側タスクとして継続)。