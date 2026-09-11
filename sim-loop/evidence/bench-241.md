# bench-241

- date-anchor: cron run (JST morning, 2026-09-11)
- host load: `load averages: 148.30 79.48 52.59` (15-min 79.48), hw.ncpu=10 → 15-min ≈ 7.9x ncpu → **load gate exceeded (>=2x)**

## verdict: skipped (load)

- `clojure -M:test` (robotics / giemon): **not run** — host load far above gate (15-min 79.48 vs threshold ~20). Prior bench-064–101 style honest skip.
- seeded reproduction: **not run** (same reason).
- unmeasured; baselines held (unmeasured ≠ regression assert):
  - robotics baseline: 23/558/0 (HEAD 893ef76)
  - giemon baseline: 46/115/0 (HEAD d0d3cb4)
- regression: **none observed** (nothing measured; no new failure evidence).
- falsify status: unchanged — falsify-034 (H35, FK angle-count guard repair 未実装) 残存なし状態を引き継ぎ; falsify-037 (H38) refuted 済み。
- code change: none (bot does not modify code).

## reproduce command

```
cd orgs/kotoba-lang/robotics && clojure -M:test   # expect 23/558/0
cd orgs/kotoba-lang/giemon && clojure -M:test     # expect 46/115/0
```
