# bench-271

## Judgement: unmeasured — skipped (load)

- Gate: hw.ncpu=10, 15-min load average 104.77 (≈10.5x ncpu) → gate 2x exceeded. Per load policy both `clojure -M:test` suites and any seeded reproduction were omitted this run. No baseline change asserted; robotics/giemon baselines held at prior values.
- HOST LOAD: 13:05 up 11 days, 5:48, load averages: 106.63 104.77 118.07 (ncpu=10)
- Test runs: not executed (skipped (load)). robotics: unmeasured. giemon: unmeasured.
- Seeded reproduction: not executed (skipped (load)); sim-loop remains L0 (no job) — not-applicable in measured runs.
- Git HEADs: not re-read this run (load skip); last recorded robotics ad99366 / giemon 00fd23f.
- Regression: none asserted — honest skip, no claim of pass or fail.
- Falsify status: unchanged from falsify-074 (H74 refuted, reconfirmed statically). Runner repair (cljk silent-zero, NEXT in maturity.md) still outstanding; FK guard repair still unimplemented (falsify-034 line, 31 consecutive refutations).
- Repro command (this run was skipped; standard procedure for reference):
  `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test` and
  `cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test`
- No code change.
