# giemon sim-loop bench 記録

## 概要
- cron (giemon-sim-bench)、bench-016
- ホスト負荷: load averages 15.33 (1min) / 35.11 (5min) / 44.43 (15min) 開始時 →
  実行完了時 14.07 / 31.51 / 42.51、ncpu=10 → **高負荷** (5min は bench-007 の 37.25 と同程度)。
  ポリシーに従い重い実験 (数値計測 probe の新規追加・長時間シミュレータ実行) は
  **skipped (load)**。テスト実行と軽量 seeded 再現は完了 (いずれも正常終了)。

## 1. テスト実行 (clojure -M:test)

### orgs/kotoba-lang/robotics
- コマンド: `cd orgs/kotoba-lang/robotics && clojure -M:test`
- 結果: **Ran 14 tests containing 50 assertions. 0 failures, 0 errors.** (exit 0)

### orgs/kotoba-lang/giemon
- コマンド: `cd orgs/kotoba-lang/giemon && clojure -M:test`
- 結果: **Ran 46 tests containing 115 assertions. 0 failures, 0 errors.** (exit 0)

## 2. Seeded 再現実行 (sim-loop 学習ジョブ相当)
- verdict: **pass (軽量範囲)** — bench-002〜015 と同一の軽量 seeded 再現のみ実施。
- 実装状況: sim-loop 専用の学習ジョブ (seed / L1 以降) は giemon リポジトリ内に
  **未実装のまま** (src/kotoba/giemon/ は arm/chassis/export/governor/kinematics/ui/viewer のみ。
  本回は src + test への grep (seed/learn/train) で一致ファイルなしを機械確認 — exit 1)。
  L1 昇格条件は未達、OPEN の赤は解消されず。
- 軽量 seeded 再現 (決定的関数の同入力 2 回実行照合):
  - 対象: `kotoba.giemon.arm/end-effector` (giemon_arm6 fixture —
    fixtures/giemon_arm6/giemon_arm6.edn を arm_edn_test.clj と同一手順
    (unblob + reconstitute-arm) で再構成、q=[0.0 0.2 -0.3 0.0 0.5 0.0])
  - 結果: 2 回の結果が**完全一致** → `SEED-PARITY true` (exit 0)、
    :xf/pos [0.035165560086391295 0.0 0.6104766433183229]
    bench-002〜015 の :xf/pos 数値と同一 (決定的再現を 14 点確認)。
- 注: 学習ジョブの seeded 再現ではなく、既存決定的関数の 2 回実行一致の確認。

## 3. 回帰の有無
- **回帰なし**。bench-001 → … → bench-016 で同一数字:
  robotics 14 tests / 50 assertions / 0 failures、giemon 46 tests / 115 assertions / 0 failures。
- bench-003〜016 は高負荷ホスト (load 5〜184) でも同一結果 — 負荷条件下での同一性を 14 点確認
  (本回 bench-016 は load 35.11 (5min)。bench-007 の 37.25 と同程度の負荷での同一結果)。
- evidence の差分: 前回 (bench-015) 以降、evidence への追加・変更なし
  (uncommitted は sim-loop/ のまま)。テスト結果には影響なし。

## 4. skipped (load)
- 重い実験 (j2 動的系 probe 系の再実行・拡張、falsify 系の追加測定) は実施せず
  **skipped (load)** と正直に記録。テストと軽量再現のみでの完了。

## 再現コマンド
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon  && clojure -M:test
# seeded 再現 (軽量):
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M -i /tmp/seed_parity_bench016.clj
# (arm_edn_test.clj の unblob + reconstitute-arm と同一手順で fixture を再構成し、
#  end-effector を同入力 2 回実行して = で照合 → SEED-PARITY true, exit 0)
```

## 補足
- コード修正なし (ベンチ・記録のみ)。
- 決定的記述のみ、タイムスタンプ非依存。
- 初回の parity スクリプトは `kotoba.giemon.arm/reconstitute-arm` を参照して失敗した
  (同関数は test 内の defn- で公開 API ではない)。arm_edn_test.clj と同一の手順を
  スクリプト側に複製してやり直し、成功 (bench-013/014 の手順と同一)。
