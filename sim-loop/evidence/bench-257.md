# bench-257

- date: 2026-09-14 JST (cron, deterministic record; no timestamp beyond this)
- run type: **skipped (load)** — test suites and seeded repro NOT run this iteration

## Host load at run start
- load averages: 17.82 25.31 22.10 (1/5/15min), hw.ncpu=10 → 15-min ≈ 2.21x ncpu
- gate: 15-min ≥ ~2x ncpu skip threshold → heavy `kbb -M:test` runs omitted per skill rule.
  Second uptime reading at meta capture: 13.56 23.26 21.50 (still ≥ 2x on 5/15-min).

## Test results
- robotics: skipped (load)
- giemon: skipped (load)
- No test counts obtained this run. Baselines (robotics 23/558/0, giemon 46/115/0) remain
  the standing reference; the known cljk silent-zero runner defect (falsify-069) is
  still the blocker to re-establishing them regardless of load.

## Git HEADs
- robotics HEAD: ad99366bc7bef949e86ee33b7e04d12525dffe46 (unchanged from bench-256 / maturity.md NEXT)
- giemon HEAD: 00fd23f9d04743323047c8c29c30aa18320daa70 (unchanged from bench-256 / maturity.md NEXT)

## Seeded reproduction (sim-loop L1+)
- not-applicable: sim-loop is L0, no learning job to reproduce (standing verdict);
  additionally skipped (load) this run.

## Regression judgement
- **unmeasured (skipped, load)** — no regression asserted; baselines held as-is per
  honest-record rule. No new regression signal.

## falsify status
- falsify-034..071: unchanged this run (no falsify work performed; bench-only run, and
  heavy work skipped for load).
- Top-priority repair items unchanged: test-runner fix (cljk silent-zero), then
  governor silent-nil rejected-record + negative test (falsify-071 recommendation),
  then FK guard repair re-verification (falsify-034).

## Reproduction command (for the next measured run)
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && git rev-parse HEAD && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && git rev-parse HEAD && kbb -M:test
```
