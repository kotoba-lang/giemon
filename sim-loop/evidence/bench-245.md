# bench-245

- date-order: 245 (last evidence file was bench-244). No timestamp (deterministic record).
- HEADs: robotics ad99366, giemon 00fd23f — unchanged from bench-244, still ahead of baseline (893ef76 / d0d3cb4).
- HOST LOAD at run: 15-min ~8.2–9.0, nproc=10 → < 2x ncpu, gate passed; heavy runs attempted.
- Context note: 4 persistent runaway nbb (amu) node processes at ~99% CPU each dominate the load (measured via ps, /tmp/b001_top.txt). Not caused by this bench.

## test suite (kbb -M:test)

- robotics: "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- giemon: "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- Same silent-zero as bench-244: cognitect JVM test-runner no longer discovers the renamed `*_test.cljk` files (test dirs contain only .cljk). Baseline robotics 23/558/0, giemon 46/115/0 (bench-240) — both still collapsed to 0/0/0. Regression state UNCHANGED (persisting red, not a new breakage).
- Repro: `cd <repo> && kbb -M:test` (robotics and giemon). Output: /tmp/b001_rob.txt, /tmp/b001_gie.txt.

## kbb -M:test

- NOT re-run this iteration (bench-244 measured both runners; budget-limited run re-tested only the clojure path to confirm persistence). bench-244's kbb result (RC=1 both projects) stands as last measurement.

## verdict

- judgement: **measured, REGRESSION persists** (silent-zero reproduced on both projects at identical HEADs as bench-244).
- numbers: clojure runner 0/0/0 both projects (baseline 23/558/0 robotics, 46/115/0 giemon — -100% vs baseline, unchanged since bench-244).
- regression: YES (carried over from bench-244; no new breakage observed this run).
- seeded repro: not-applicable (sim-loop is L0, no learning job).
- falsify status: no new falsify this run; falsify-034~037 verdicts unchanged. arm-test still not runnable green by the clojure runner (falsify-036's measured green is no longer reproducible at these HEADs).
- no code change made by this bench run (policy: bench never fixes).
- This red record is the honest bench-245 entry; implementation/refutation left to other agents.
