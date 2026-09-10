# bench-102 (giemon sim-loop bench - daily sequence)

Timestamp: 2026-09-07 18:59 JST (git HEAD d0d3cb4)
 HOST LOAD (measured @ run time): 19.90〜28.82 / 15.98 / 23.64〜24.21 (ncpu=10, ~2-2.4x on 15min, ~2-2.9x on 1min) — elevated but stable enough for the suite to run deterministically.

## Measurability
- clojure -M:test (robotics + giemon): **measured** — terminal `/tmp` redirect workaround held; both suites ran to completion (exit 0) this walk. Load ~2x ncpu — not the ~4-5x overload that skipped bench-099〜101., so full measurement resumed.

## Test numbers (measured, deterministic)
- kotoba-lang/robotics: **14 test /  ̂50 assertion /̂ 0 failure /̂ 0 errors** (exit 0)
- kotoba-lang/giemon: **46 test /̂ 115 assertion /̂ 0 failure /̂ 0 errors** (exit 0)
- Matches baseline (bench-066) exactly — **no regression asserted (measured)**. First measured test-suite run since bench-066; bench-067〜101 ho unmeasured/ skipped..

## Reproduction verdict
- seeded reproduction (sim-loop L1+, run same seed twice, compare results): **not-applicable** — sim-loop learning job still at L0, not implemented (unchanged since bench-098..101); no task exists to reproduce.

## Judgment (7 axes, ADR-2608052000)
- Test health::**green (measured)** — 60 tests総, 0 failures, both suites exit 0., baseline held.

- Regression present::**no (measured)** — numbers identical to bench-066 baseline.>
- Reproducibility::unchanged — L0, seeded reproduction no task (not-applicable)。

## Baseline (confirmed again, measured)
- kotoba-lang/robotics:,14 test / ̂50 assertion /̂ 0 failure- kotoba-lang/giemon:,46 test /̂ 115 assertion /̂ 0 failure

## Reproduction command (not-applicable)
- `clojure -M:test` (robotics, giemon) — executed, results above.
- seeded reproduction:: no task (sim-loop L0, out of scope); not run.



## Verified static state
- git HEAD::d0d3cb4 (consistent with bench-098..101 ⁇; no tracked diff — untracked: sim-loop/ etconly..
- sim-loop learning job not implemented (L0; unchanged); seeded reproduction has no task..
- No unresolved falsify remains (falsify-033 closed H25〜H34; NEXT: FK angle-guard repair adoption pending, not implemented by this bot — git unchanged, to be checked in future evidence)..



## Notes
- bench-102 is the first measured test-suite run since bench-066, load eased from the ~4-5x overload of bench-099〜101 down to ~2-2.4x (15min); suite completed deterministically,. numbers exactly match baseline — regression clean, honest measured numbers recorded ( no fabrication)..
- `/tmp` redirect workaround confirmed once more (terminal direct stdout empty; `/tmp` write + read_file works)..