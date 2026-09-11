# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-013
- ホスト負荷: load averages 184.45 (1min) / 143.91 (5min) / 67.16 (15min) 開始時 →
  実行完了時 99.37 / 127.08 / 69.97、ncpu=10 → **高負荷**。
  ポリシーに従い重い実験 (数値計測 probe の新規追加・長時間シミュレータ実行) は
  **skipped (load)**。テスト実行と軽量 seeded 再現は完了 (いずれも正常終了)。

## 1. テスト実行 (kbb -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && kbb -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜012 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src/kotoba/giemon/ は arm/chassis/export/governor/kinematics/ui/viewer の
  み。本回も目視再確認、seed/learn/train を含む namespace なし)。
  L1 昇格条件は未達、OPEN の赤は解消されず。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜012 の :xf/pos 数値と同一 (決定的再現を 12 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-013 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜013 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 10 点確認
  (本回 bench-013 は load 184 の極度高負荷。bench-007 の 37.25 を上回る過去最高負荷での同一結果)。
- evidence の差分: 前回 (bench-012) 以降、evidence への追加・変更なし
  (uncommitted は sim-loop/ のまま)。テスト結果には影響なし。

## 4. skipped (load)
- 重い実験 (j2 動的系 probe 系の再実行・拡張、falsify 系の追加測定) は実施せず
  **skipped (load)** と正直に記録。テストと軽量再現のみでの完了。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && kbb -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M -i /tmp/seed_parity_bench013b.clj
# (arm_edn_test.clj の reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
