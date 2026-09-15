# bench-244

- date-order: 244 (last evidence file was bench-243). No timestamp (deterministic record).
- HEADs: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46, giemon 00fd23f9d04743323047c8c29c30aa18320daa70. **Both advanced since baseline** (893ef76 / d0d3cb4): robotics landed cljk rename (da633e9, 4381dc2) + kbb cutover (a83706e, ad99366); giemon landed cljk rename (ddda171, d4d43f0) + cleanup lands (3fa68c6, a16d0a9, 00fd23f).
- HOST LOAD at run: 15-min 9.55-10.09, nproc=10 → < 2x ncpu, gate passed, heavy runs attempted.

## test suite (kbb -M:test)

- robotics: "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- giemon: "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- **REGRESSION (silent-zero):** baseline robotics 23/558/0, giemon 46/115/0 (bench-240). Both suites now discover ZERO tests under kbb -M:test. Cause is consistent with the landed cljk rename (test files are now `*_test.cljk`; the cognitect JVM test-runner no longer matches them) — this is measured behavior; root-cause attribution is inference, the 0/0/0 is measured.
- Repro: `cd <repo> && kbb -M:test` (robotics and giemon). Output: /tmp/b_rob.txt, /tmp/b_gie.txt.

## test suite (kbb -M:test) — follow-up attempt on the new mandated entry point

- robotics: RC=1. kbb warns 3 deps (html, css, cognitect test-runner) not on classpath; cljs.test substitution attempts 4 namespaces, then nbb_deps.js crash: ERR_INVALID_ARG_TYPE (paths[0] null).
- giemon: RC=1. kbb warns 5 deps (text, html, css, robotics, test-runner) not on classpath; 10 namespaces attempted, fails "Could not find namespace: clojure.java.io".
- So the new `kbb -M:test` entry point is also broken for both projects. No green path exists for either runner at these HEADs.

## verdict

- judgement: **measured, REGRESSION** (not unmeasured — both runners were executed; result is a measured silent-zero / hard failure, not a load skip).
- numbers: clojure runner 0/0/0 both projects (baseline 23/558/0 and 46/115/0 — -100%); kbb -M:test exit 1 both projects.
- regression: YES — test suite count collapsed to zero on both projects after the cljk-rename + kbb-cutover HEAD advance; also the kbb entry point fails to run.
- seeded repro: not-applicable (sim-loop is L0, no learning job).
- falsify status: no new falsify this run; falsify-034~037 verdicts unchanged (FK guard repair 未実装 chain stands; arm-test cannot even be run green right now — falsify-036's "5/11/0 緑" is no longer reproducible by either runner).
- no code change made by this bench run (policy: bench never fixes).
- This is the red record required by the role charter: regression detected, recorded honestly, implementation/refutation left to other agents.
