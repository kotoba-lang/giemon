# giemon sim-loop bench 記録

## 概要
- 実行日: 2026-09-04 (JST) — cron (giemon-sim-bench)、bench-002
- ホスト負荷: load averages 5.08–6.54 (1min) / 8.75–10.46 (15min)、ncpu=10 → 中負荷
  (重い長時間シミュレータ実行は省略、軽量 seeded 再現は実施)

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)**
- 実装状況: sim-loop 専用の学習ジョブ (L1 以降) は giemon リポジトリ内に**未実装のまま**
  (src は arm/chassis/kinematics/governor/viewer/ui/export のみ。matirtiy OPEN の赤は解消されず)。
- 代替として、決定的数値計算の seeded 再現を同じ入力で 2 回実行して照合:
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の `:pos` / `:rot` が**完全一致** → `SEED-PARITY true` (exit 0)
- 注: これは学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。
  L1 昇格条件 (学習ジョブ実装) は未達。

## 3. 回帰の有無
- **回帰なし**。前回 (bench-001) と同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -e \
 '(require (quote [kotoba.giemon.arm :as arm]) (quote [clojure.edn :as edn]) (quote [clojure.java.io :as io])) ...'
# (arm_edn_test.clj の reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → true)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
