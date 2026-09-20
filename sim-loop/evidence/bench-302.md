# bench-302

## Judgement: unmeasured — skipped (load)

- Date anchor: 2026-09-20 (JST), uptime `13:05 up 1 day, 21:16`
- Load: 1/5/15-min = 32.46 / 36.58 / 35.29→35.32, hw.ncpu = 10 → 15-min ≈ 3.5x ncpu
- Gate: 15-min ≥ ~2x ncpu → heavy test runs skipped per skill load gate.

## Measurements

- `clojure -M:test` (robotics / giemon): **skipped (load)** — not run this iteration.
- seeded reproduction: not-applicable (sim-loop L0, no job).

## Reference values (据え置き)

- robotics: 23/558/0 @ ad99366 (HEAD unchanged, confirmed via `git rev-parse`)
- giemon: 46/115/0 @ 41ac173 (HEAD unchanged, confirmed)

## Regression

- New regression assertion: none (unmeasured — honest record, 基準値据え置き).
- Known persistent issue (unchanged): silent-zero clojure -M:test runner failure
  (falsify-069 root cause, .cljk load failure) — runner 修復未了. Unverifiable this
  run due to load gate.

## Falsify status

- FK guard repair (falsify-034 起) 残存なし変化 — 未着手のまま.
- No new falsify work this run (bench iteration only, no code change).

## Repro commands

- uptime; sysctl -n hw.ncpu
- cd orgs/kotoba-lang/robotics && git rev-parse --short HEAD   → ad99366
- cd orgs/kotoba-lang/giemon && git rev-parse --short HEAD     → 41ac173
- (heavy path skipped: cd <proj> && clojure -M:test)

No code change.
