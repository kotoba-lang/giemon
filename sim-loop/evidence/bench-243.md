# bench-243

## Verdict: skipped (load)

- date-run context: JST Sat 2026-09-12, ~01:12, cron (giemon-sim-bench)
- load: 54.09 / 66.24 / 78.72 (1/5/15-min), ncpu=10 → 15-min ≈ 6.6x ncpu。skill load gate (≥~2x) を大幅超過。
- git HEAD: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46, giemon 00fd23f9d04743323047c8c29c30aa18320daa70
- test 実行を試行したが、両スイートとも `Ran 0 tests containing 0 assertions, 0 failures` (exit 0)。
  基準値 (robotics 23/558/0, giemon 46/115/0) に到達しておらず、高負荷下で test スイートが
  正常にロードされない状態。本数値は測定として無効 → **unmeasured**、regression として assert しない。
- seeded 再現: skipped (load)
- regression 判定: none asserted (unmeasured, 基準値据え置き)
- falsify status: 変更なし (falsify-034 FK guard repair 未実装のまま、本 run はコード変更なし)
- next bench number: 244

## Repro command

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
# 本 run: load 15-min 66.24 vs ncpu 10 → load gate 超過、skip (load) 記録
```
