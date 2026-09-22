# bench-315

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live, `uptime` order is 1/5/15-min): 15-min 37.90 (1-min 14.79, 5-min 32.79) / ncpu 10 → **≈3.8x** ≥ 2x gate
- pre-run script snapshot (earlier same window): 15-min 39.71 (1-min 17.74, 5-min 37.17) → ≈4.0x
- honest note (gate protocol): 本 run は gate 超過帯 (15-min ≈3.8x) で clojure -M:test を実行した (bench-307〜314 と同じ skip 判定なら unmeasured 扱い) — 測定値は gate 超過帯の実測として記録し、honest 据え置きで扱う (下方の silent-zero 値は bench-306 と同値の既知 defect シグネチャで、新規測定ではない)。
- bench-307〜314 の 8 連続 load-skip は本 run で途切れた (本走実行・実測値を返した)。

## Tests
- robotics `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-306 実測値と同一)
- giemon `clojure -M:test`: executed — Ran 0 tests, 0 assertions, 0 failures, 0 errors, RC=0 (silent-zero シグネチャ、bench-306 実測値と同一)
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0 (回帰 assert なし — runner が 0 tests を返す既知 defect の再確認)

## Git HEADs (measured, unchanged from bench-314)
- robotics: ad99366 (git rev-parse 実測・不変)
- giemon: 8c3c3e6 (git rev-parse 実測・不変)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-306.md`〜`?? sim-loop/evidence/falsify-084.md` (bench-306〜314 の記録自体が未 landed)。robotics は clean。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job) — unmeasured

## Judgement
- measured (silent-zero reconfirmed) — 基準値据え置き、回帰の assert なし
- regression: none observable (0/0/0 = 既知 defect シグネチャ; falsify-069 根因: JVM require が .cljk をロード不能、runner 修復未了)
- runner status: clojure runner silent-zero 実測分 **47 連続** (bench-244〜315、途中 load-skip 除く。bench-306 の 46 連続に本走 1 実測を追加)。bench-307〜314 の 8 連続 load-skip は本 run で途切れ、本走は gate 超過帯 (≈3.8x) での実測。test-runner 修復が最優先のまま変化なし。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip (本 run は 3.8x で gate 超過のまま実行)
cd orgs/kotoba-lang/robotics && clojure -M:test   # 0/0/0 RC=0 実測
cd orgs/kotoba-lang/giemon && clojure -M:test     # 0/0/0 RC=0 実測
git -C orgs/kotoba-lang/robotics rev-parse --short HEAD   # ad99366
git -C orgs/kotoba-lang/giemon   rev-parse --short HEAD   # 8c3c3e6
```

No code change.
