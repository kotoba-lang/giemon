# bench-309

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check: 15-min 42.10 (1-min 42.10, 5-min 43.31) / ncpu 10 → **≈4.2x** ≥ 2x gate
- pre-run script snapshot (earlier same window): 15-min 49.26 / ncpu 10 → ≈4.9x。負荷帯は bench-290 (3.9–5.2x) と同帯、bench-308 (7.0–7.2x) より低下。
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (measured, unchanged from bench-308)
- robotics: ad99366 (git rev-parse 実測・不変)
- giemon: 8c3c3e6 (git rev-parse 実測・不変)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-306.md` + `?? sim-loop/evidence/bench-307.md` + `?? sim-loop/evidence/bench-308.md` (bench-306/307/308 の記録自体が未 landed)。robotics は clean。src/test 不変。

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
