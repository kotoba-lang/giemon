# bench-305

- date-anchor: cron run, JST 2026-09-20 night (no timestamp dependency; deterministic)
- HOST LOAD at gate check: 15-min 24.19 (1-min 27.49) / ncpu 10 → **2.42x** ≥ 2x gate
  (run 開始 27.49 / 26.93 / 24.19、HEAD 取得時 26.24 / 26.71 / 24.16、数分前に
  30.51 / 26.18 / 23.40 — 数時間 23〜31 の持続高負荷帯、1-min > 15-min で上昇中)
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (unchanged, git rev-parse 実測)
- robotics: ad99366 (baseline-consistent)
- giemon: 41ac173 (baseline-consistent)
- In-flight: giemon working tree に ` M sim-loop/status/maturity.md` + untracked
  bench-270〜304 / falsify-074〜082 evidence 群のみ (bench 反復作業物、コード変更なし)

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job; load-skipped anyway) — unmeasured

## Judgement
- unmeasured (load) — 基準値据え置き、回帰の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists
  unresolved per NEXT — bench-244〜304 実測分 45 連続)
- runner status: clojure runner silent-zero (0/0/0 RC=0) は本 run では未検証
  (load skip、bench-290/291/293/294 と同型)。test-runner 修復が最優先のまま変化なし。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min 24.19 / 10 = 2.42x >= 2x -> skip
clojure -M:test               # robotics / giemon (run when load < 2x ncpu)
```

No code change.
