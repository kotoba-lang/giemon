# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-011
- ホスト負荷: load averages 5.70 (1min) / 5.50 (5min) / 6.18 (15min)、ncpu=10 → **低〜中負荷**
  (テスト実行と軽量 seeded 再現は実施 — いずれも完了。重い長時間シミュレータ実行は
  対象が存在しないため N/A)

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜010 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src/kotoba/giemon/ は arm/chassis/export/governor/kinematics/ui/viewer の
  み。src + test への grep で seed/learn/train を含むファイルなし、本回も再確認)。
  L1 昇格条件は未達、OPEN の赤は解消されず。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜010 の :xf/pos 数値と同一 (決定的再現を 10 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → 002 → 003 → 004 → 005 → 006 → 007 → 008 → 009 → 010 → 011 で
  同一数字: robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜011 は高負荷ホスト (load 5〜37) でも同一結果 — 負荷条件下での同一性を 9 点確認。
- evidence の差分: 前回 (bench-010) 以降、evidence への追加・変更なし
  (uncommitted は sim-loop/ のまま)。テスト結果には影響なし。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench011.clj
# (arm_edn_test.clj の reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
