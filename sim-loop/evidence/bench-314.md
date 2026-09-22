# bench-314

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check (measured, live): 15-min 38.74 (1-min 49.01, 5-min 44.39) / ncpu 10 → **≈3.9x** ≥ 2x gate
- pre-run script snapshot (earlier same window): 15-min 37.86 → 同帯域。bench-311〜313 からやや低下したが gate 超過継続。
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (measured, unchanged from bench-313)
- robotics: ad99366 (git rev-parse 実測・不変)
- giemon: 8c3c3e6 (git rev-parse 実測・不変)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-306.md`〜`?? sim-loop/evidence/falsify-084.md` (bench-306〜313 の記録自体が未 landed)。robotics は clean。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job; load-skipped anyway) — unmeasured

## Judgement
- unmeasured (load) — 基準値据え置き、回帰の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists unresolved per NEXT)
- runner status: clojure runner silent-zero (0/0/0 RC=0、bench-244〜306 実測分 46 連続、falsify-069 根因確定: JVM require が .cljk をロード不能) は本 run でも未検証 (load skip、bench-307〜314 で 8 連続 skip)。test-runner 修復が最優先のまま変化なし。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip
clojure -M:test               # robotics / giemon (run when load < 2x ncpu)
git -C orgs/kotoba-lang/robotics rev-parse --short HEAD   # ad99366
git -C orgs/kotoba-lang/giemon   rev-parse --short HEAD   # 8c3c3e6
```

No code change.
