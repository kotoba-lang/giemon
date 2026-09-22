# bench-310

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check: 15-min 24.57 (1-min 24.26, 5-min 24.57) / ncpu 10 → **≈2.5x** ≥ 2x gate
- pre-run script snapshot (earlier same window): 15-min 24.50 / ncpu 10 → ≈2.5x。負荷帯は bench-309 (≈4.2x, 4.9x) より低下、bench-306 (≈1.2x) 以上で gate 超過継続。
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (measured, unchanged from bench-309)
- robotics: ad99366 (git rev-parse 実測・不変)
- giemon: 8c3c3e6 (git rev-parse 実測・不変)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-306.md` + `?? sim-loop/evidence/bench-307.md` + `?? sim-loop/evidence/bench-308.md` + `?? sim-loop/evidence/bench-309.md` (bench-306〜309 の記録自体が未 landed)。robotics は clean。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job; load-skipped anyway) — unmeasured

## Judgement
- unmeasured (load) — 基準値据え置き、回帰の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists unresolved per NEXT)
- runner status: clojure runner silent-zero (0/0/0 RC=0、bench-244〜306 実測分 46 連続、falsify-069 根因確定: JVM require が .cljk をロード不能) は本 run では未検証 (load skip)。test-runner 修復が最優先のまま変化なし。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip
clojure -M:test               # robotics / giemon (run when load < 2x ncpu)
git -C orgs/kotoba-lang/robotics rev-parse --short HEAD   # ad99366
git -C orgs/kotoba-lang/giemon   rev-parse --short HEAD   # 8c3c3e6
```

No code change.
