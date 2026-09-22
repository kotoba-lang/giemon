# bench-308

- date-anchor: cron run, JST (no timestamp dependency; deterministic)
- HOST LOAD at gate check: 15-min 71.62 (1-min 79.49, 5-min 72.01) / ncpu 10 → **≈7.2x** ≥ 2x gate
- pre-run script snapshot (earlier same window): 15-min 69.63 / ncpu 10 → ≈7.0x。負荷帯は bench-290 (3.9–5.2x) 以上・現 series 最高帯。
- gate verdict: **load exceeded → heavy runs skipped (load)**

## Tests
- robotics `clojure -M:test`: skipped (load) — unmeasured
- giemon `clojure -M:test`: skipped (load) — unmeasured
- baseline 据え置き: robotics 23/558/0, giemon 46/115/0

## Git HEADs (measured, unchanged from bench-307)
- robotics: ad99366 (git rev-parse 実測・不変)
- giemon: 8c3c3e6 (git rev-parse 実測・不変)
- in-flight (未コミット): giemon `M sim-loop/status/maturity.md` + `?? sim-loop/evidence/bench-306.md` + `?? sim-loop/evidence/bench-307.md` (bench-306/307 の記録自体が未 landed)。robotics は clean。src/test 不変。

## Seeded reproduction
- not-applicable (sim-loop L0, no learning job; load-skipped anyway) — unmeasured

## Judgement
- unmeasured (load) — 基準値据え置き、回張の assert なし
- regression: none observable (nothing ran; silent-zero runner issue persists unresolved per NEXT)
- runner status: clojure runner silent-zero (0/0/0 RC=0、bench-244〕306 実測分 46 連続、falsify-069 根因確定: JVM require が .cljk をロード不能) は本 run では未驓証 (load skip)。test-runner 修复が最先順のまま変化なし。

## Notes (this run)
- はずれも路径処理でケース含み名前の space-変形トリイ (github 下 `com-junk Kawasaki` / `com-junk Kawasaki orgs`) を生成した。両者は .git 无・パート形式の誤り、ファイル 1件 (bench-308.md 初稿) / 3件 (net-kotobase/docs 下の .b697_* プローブ 3件・他サレーションの临時物) のもの。すらにすり削除 (no .git, 実 checkout は `com-junk Kawasaki` ではなかない = スペースなし名)。.b697_* プローブ 3件は未トラック临時物と判定し削除した。実 evidence テーリ (CWD の符で確認) の bench-306/307 は不変。

## Repro command
```
uptime && sysctl -n hw.ncpu   # 15-min >= 2x ncpu -> skip
clojure -M:test               # robotics / giemon (run when load < 2x ncpu)
git -C orgs/kotoba-lang/robotics rev-parse --short HEAD   # ad99366
git -C orgs/kotoba-lang/giemon   rev-parse --short HEAD   # 8c3c3e6
```

No code change.
