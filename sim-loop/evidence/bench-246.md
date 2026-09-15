# bench-246

## load
- load averages: 9.00 9.34 9.61 (15-min 9.34) / hw.ncpu = 10 → ~0.93x ncpu, load gate OPEN (許可)。重い実験は実行した。

## runs (bash /tmp/bench_run.sh, foreground script, /tmp redirect workaround)
- robotics: `kbb -M:test` → RC=0, but **"Ran 0 tests containing 0 assertions. 0 failures, 0 errors."** runner header "Testing user".
- giemon:   `kbb -M:test` → RC=0, but **"Ran 0 tests containing 0 assertions. 0 failures, 0 errors."** runner header "Testing user".

### dir/diagnostics (bench-246 /tmp/b_probe3.txt)
- robotics test files exist: test/kotoba/robotics/{safety_invariants,ui,export}_test.cljk + test/kotoba/robotics_test.cljk (4 files)
- robotics src files exist: src/kotoba/robotics/{ui,export}.cljk + src/kotoba/robotics.cljk
- deps.edn :test alias intact (cognitect test-runner v0.5.1, extra-paths ["test"]).

### verdict on run validity
**INVALID RUN — test collection failed silently.** The runner found 0 namespaces (likely `.cljk` extension not discovered by cognitect test-runner default dir-scan), so exit 0 + 0 failures is a **false pass**, not a real green. Numbers below are recorded as-is but flagged `collection-failed`.

## numbers (as returned by the runner; collection-failed)
- robotics: 0 / 0 / 0 (baseline 23/558/0 HEAD 893ef76) — **MISMATCH due to collection failure**
- giemon:   0 / 0 / 0 (baseline 46/115/0) — **MISMATCH due to collection failure**

## git HEADs
- robotics: ad99366bc7bef949e86ee33b7e04d12525dffe46 (skill notes reference 893ef76 → HEAD has advanced since last recorded baseline)
- giemon:   00fd23f9d04743323047c8c29c30aa18320daa70 (skill notes d0d3cb4 → advanced)

## seeded reproduction
not-applicable (sim-loop is L0, no learning job) — unchanged from bench-245.

## regression
**Not asserted.** The 0/0/0 result is a runner-level collection failure (false pass), not a regression in the suites themselves; asserting regression from it would be dishonest. Prior bench runs (e.g. bench-102..) recorded real numbers; the same command today yields 0 tests. Investigation needed (test runner env, .cljk handling) — recorded as open issue for next bench.

## falsify
- falsify-034 status unchanged (残存).

## no code change
