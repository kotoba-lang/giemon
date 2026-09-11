# bench-240

## Judgement
measured (15-min load 14.57 on 10 cpus ≈ 1.5x band; test suites completed with real output).

## Test results
- robotics: `kbb -M:test` → Ran 23 tests containing 558 assertions. 0 failures, 0 errors. RC=0.
- giemon: `kbb -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0.

## Change vs baseline (bench-066: robotics 14/50/0, giemon 46/115/0)
- giemon: unchanged (46/115/0) — no regression.
- robotics: test count moved 14/50 → 23/558 with 0 failures/0 errors. NOT a failure regression; recorded as an honest observed change.
  - Robotics HEAD advanced: 9459ca0 (baseline) → 893ef76f3adf1c4b04904b304007646c0002a4a1.
  - Baseline numbers for robotics are stale; future benches should treat 23/558/0 as the current robotics reference unless a regression verdict is raised elsewhere.
- giemon HEAD unchanged: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (matches skill baseline).

## Seeded reproduction
not-applicable (sim-loop is L0, no learning job to re-seed).

## Regression
none (both suites exit 0, giemon at baseline, robotics fail/error counts 0 despite suite growth).

## Falsify status
falsify-034 (H35, FK guard repair) 残存: arm_test.cljc zero-fill 無変更のまま (本ベンチはコード変更なし、未確認変更は無し)。他 falsify は既存 verdict のまま。

## Repro commands
- cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
- cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test

## Environment
- uptime: 7:05 up 5 days, load averages: 5.84 15.13 14.57 (10 cpus)
- No code changes made. Timestamp-free, deterministic record.
