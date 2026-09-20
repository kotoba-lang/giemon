# bench-294

- date-anchor: cron run, JST morning (no timestamp dependency; deterministic)
- HOST LOAD at gate check: 15-min 21.84 (1-min 20.48) / ncpu 10 → **2.2x** ≥ 2x gate
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (unchanged)
- robotics: ad99366 (baseline-consistent)
- giemon: 41ac173 (baseline-consistent)

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job; load-skipped anyway) — unmeasured

## Judgement
- unmeasured (load) — 基準値据え置き、回帰の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists unresolved per NEXT)
- runner status: clojure runner silent-zero (0/0/0 RC=0, bench-244〜292 連続実測) は本 run では未検証 (load skip)。test-runner 修復が最優先のまま変化なし。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip
clojure -M:test               # robotics / giemon (run when load < 2x ncpu)
```
