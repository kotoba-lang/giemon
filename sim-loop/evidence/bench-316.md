# bench-316

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 13.91 (1-min 15.46, 5-min 15.15) / ncpu 10 → **≈1.4x** < 2x gate → tests executed
- pre-run script snapshot (earlier same window): 15-min 17.60 ≈1.8x (gate 未満)
- test 終了時 load: 15-min 17.16 ≈1.7x (実行中 rise・gate 内完走)

## Tests
- robotics `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-315 実測値と同一)
- giemon `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-315 実測値と同一)
- test ファイル存在確認 (実測): robotics test/ 4 ns・giemon test/ 10 ns 全件 `*_test.cljk` (拡張子復帰なし、falsify-082 と同値)
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認)

## Git HEADs (measured)
- robotics: ad99366 (git rev-parse 実測・不変・clean)
- giemon: 8c3c3e6 → 69878b9 に前進 (git rev-parse 実測)。git diff --stat 8c3c3e6..69878b9 = 12 files +462/−3、全て sim-loop/ (bench-306..315.md / falsify-084.md / maturity.md) — **evidence-only 前進** (git diff --name-only 8c3c3e6..69878b9 -- src test deps.edn = 空)。src/test/deps.edn 不変につき giemon 基準値 46/115/0 の参照 HEAD を 69878b9 に更新・実測値不変。
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` (本 run の status 更新)。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job — seed / L1+ 学習ジョブ 0 件) — unmeasured

## Judgement
- measured (silent-zero reconfirmed) — 基準値据え置き、回帰の assert なし
- regression: none observable (0/0/0 = 既知 defect シグネチャ; falsify-069 根因: JVM require が .cljk をロード不能、runner 修復未了)
- runner status: clojure runner silent-zero 実測分 **48 連続** (bench-244〜316、途中 load-skip 除く。bench-315 の 47 連続に本走 1 実測を追加)
- falsify 新規なし (H1〜H85 全決着・未決残存なし)
- NEXT は runner repair + re-baseline を再発行 (継続、HEAD 参照を 69878b9 に更新)

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は 1.4x で gate 内実行)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && git diff --stat 8c3c3e6..69878b9   # evidence-only 前進確認
```
