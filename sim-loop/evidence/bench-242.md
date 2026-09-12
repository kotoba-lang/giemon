# bench-242

- date-anchor: cron run (JST 22:05, 2026-09-11)
- host load: `load averages: 71.85 113.79 113.16` (15-min 113.79), hw.ncpu=10 → 15-min ≈ 11.4x ncpu → **load gate exceeded (>=2x)**

## verdict: skipped (load)

- `clojure -M:test` (robotics / giemon): **not run** — host load far above gate (15-min 113.79 vs threshold ~20). Prior bench-064–101 / bench-241 style honest skip.
- seeded reproduction: **not run** (same reason).
- unmeasured; baselines held (unmeasured ≠ regression assert):
  - robotics baseline: 23/558/0 (HEAD 893ef76)
  - giemon baseline: 46/115/0 (HEAD d0d3cb4)
- **HEAD drift note (measured, cheap)**: current HEADs are
  - giemon: `00fd23f` (baseline reference d0d3cb4 is stale)
  - robotics: `ad99366` (baseline reference 893ef76 is stale)
  - Both repos advanced since the baseline was recorded. Baseline test numbers were NOT re-verified this run (load gate); baselines remain the last measured reference, now on older commits. Next measured run should re-baseline both suites at current HEADs.
- regression: **none observed** (nothing measured; no new failure evidence).
- falsify status: unchanged — falsify-034 (H35, FK angle-count guard repair 未実装) 残存なし状態を引き継ぎ; falsify-037 (H38) refuted 済み。
- code change: none (bot does not modify code).

## reproduce command

```
cd orgs/kotoba-lang/robotics && clojure -M:test   # expect 23/558/0
cd orgs/kotoba-lang/giemon && clojure -M:test     # expect 46/115/0
```
