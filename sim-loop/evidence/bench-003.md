# giemon sim-loop bench 記録

## 概要
- 実行日: 2026-09-04 (JST) — cron (giemon-sim-bench)、bench-003
- ホスト負荷: load averages 24.74–28.34 (1min) / 24.25–27.57 (15min) → **高負荷**
  (重い長時間シミュレータ実行は省略。軽量 seeded 再現は実施)

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — HOST LOAD 高負荷のため重い実験は skipped (load)、
  bench-002 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src は arm/chassis/kinematics/governor/viewer/ui/export のみ)。
  L1 昇格条件は未達、OPEN の赤は解消されず。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果 (xf/:pos [0.035165560086391295 0.0 0.6104766433183229] /
    xf/:rot 3x3) が**完全一致** → `SEED-PARITY true` (exit 0)
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → bench-002 → bench-003 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -e \
 '(require (quote [kotoba.giemon.arm :as arm]) (quote [clojure.edn :as edn]) (quote [clojure.java.io :as io])) ...'
# (arm_edn_test.clj の reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
