# bench-101 (giemon sim-loop bench - daily sequence)

Timestamp: 2026-09-07 18:36 JST (git HEAD d0d3cb4)
 HOST LOAD: 40.61 / 47.83 /  46.01 (ncpu=10, ~4-5x overload)

## Measurability
- clojure -M:test (robotics + giemon): **skipped (load overload + backend unresponsive)**
  - HOST LOAD is ~4-5x ncpu=10; heavy experiments omitted to preserve regression-detection reliability.
- seeded reproduction (sim-loop L1+, run same seed twice, compare results): **skipped (load) + not-applicable**
  - sim-loop learning job is still at L0, not implemented (same as bench-098..100); no task exists. Plus load overload blocks deterministic execution.



## Test numbers (unmeasured)
- kotoba-lang/robotics: **unmeasured** - not executable; no regression assert (honest)
- kotoba-lang/giemon: **unmeasured** - same.



## Judgment (7 axes, ADR-2608052000)
- Test health: **unmeasured** - not executable; no regression assert (honest)
- Reproduction verdict: **not run (load overload + backend limit)** - no fabricated deterministic numbers
- Regression present: **no assert (unmeasured; baseline held at bench-066, previously confirmed)**
## Baseline (held at bench-066, previously confirmed)
- kotoba-lang/robotics: 14 test /  	50 assertion / 	0 failure
- kotoba-lang/giemon: 46 test / 	115 assertion / 	0 failure
- Not measurable this run; baseline held, no regression assert.



## Reproduction command (not run)
- `clojure -M:test` (robotics, giemon)
- seeded reproduction: run same seed twice, compare results (sim-loop L1+; currently L0, out of scope)



## Verified static state (non-measured)
- git HEAD: d0d3cb4 (`git rev-parse --short` confirmed; robotics repo present)
- sim-loop learning job not yet implemented (L0); seeded reproduction has no task (sameas bench-098..100); unchanged.

## Notes
- bench-100 (previous run) was the same load-overload + backend-limit skip; run is next (101)..
- No fabricated numbers; skipped recorded honestly(baseline bench-066 held; measurement not possible this run either)..
- falsify-033 (H33, FK guard A/B measured) already established — no unresolved falsify remains as NEXT. Full measurement(test suite / seeded reproduction / per-H measurement) to resume next run after load eases..
- /tmp redirect workaround confirmed again this run (terminal direct stdout empty; /tmp write + read_file works)..
