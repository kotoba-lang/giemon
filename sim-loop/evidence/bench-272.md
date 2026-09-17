# bench-272 (daily cron)

## Judgement
- **unmeasured** — HOST LOAD gate exceeded: 15-min load average **54.92** vs threshold 2 × hw.ncpu (= 2 × 10 = **20**). Heavy test suites and seeded repro skipped (load). Baselines held without regression assertion, per gate policy.

## Load
- uptime: 16:06 up 11 days, 8:49, 6 users; load averages: 51.04 54.92 76.43
- hw.ncpu = 10; gate threshold = 20 (15-min). 54.92 > 20 → skip.

## Test suites
- kotoba-lang/robotics `clojure -M:test`: **skipped (load)**. Baseline (held): 23/558/0 @ HEAD ad99366.
- kotoba-lang/giemon `clojure -M:test`: **skipped (load)**. Baseline (held): 46/115/0 @ HEAD 41ac173.
- Known persistent defect (unmeasured this run): silent-zero test-runner after cljk rename — both suites report 0/0/0 RC=0 (27 consecutive benches, bench-244〜270). Remains top-priority repair before any bench/falsify can measure.

## Seeded reproduction
- **skipped (load)** — L1+ sim-loop learning job not exercised this run.

## Regression
- **none asserted** — no measurement performed this run (load gate).

## Repro commands (for next run under lower load)
- `cd orgs/kotoba-lang/robotics && clojure -M:test > /tmp/b_rob.txt 2>&1`
- `cd orgs/kotoba-lang/giemon && clojure -M:test > /tmp/b_gie.txt 2>&1`
- (JVM runner root cause: falsify-069 — .cljk not loadable by JVM require; runner repair precedes re-measure)

## Falsify status
- falsify-034 (FK guard repair 未実装) 残存。falsify-074 (kbb -M:test RC=1, deps floor 未接続) 残存。 governor silent-nil 経路 (falsify-071/072 起) 未実装確定現存。 No new falsification work this run.

## Change log
- No code changes. Evidence record only.
