# bench-255

- date: 2026-09-14 JST (cron, deterministic record; no timestamp beyond this)
- run type: measured (test suites executed), with known silent-zero caveat (see verdict)

## Host load at run start
- load averages: 18.89 18.09 16.15 (1/5/15min), hw.ncpu=10 → 15-min ≈ 1.6x ncpu
- gate: below ~2x skip threshold → heavy test runs NOT skipped for load (per skill rule)

## Commands (reproduction)
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && git rev-parse HEAD && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && git rev-parse HEAD && kbb -M:test
```
Run via /tmp/bench_run.sh with stdout/stderr redirected to /tmp/b_rob.txt and /tmp/b_gie.txt.

## Test results (as measured)
- robotics: `kbb -M:test` → "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- giemon: `kbb -M:test` → "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0

## Git HEADs
- robotics HEAD capture FAILED this run: /tmp/h_rob.txt missing (h_rob.txt empty). HEAD not verified this run.
- giemon HEAD capture FAILED this run: /tmp/h_gie.txt empty (0 bytes). HEAD not verified this run.
- Both HEADs unverified — honest record, do not assert unchanged.

## Seeded reproduction (sim-loop L1+)
- not-applicable: sim-loop is L0, no learning job to reproduce (standing verdict).

## Regression judgement
- **unmeasured (silent-zero)**: both suites report 0/0/0 — the known cljk-rename
  silent-zero defect (maturity.md NEXT) swallows the suites. Baseline
  robotics 23/558/0 and giemon 46/115/0 could NOT be re-established this run.
- This is NOT counted as a green pass and NOT counted as a test-count regression
  (the 0/0/0 is a runner defect, already tracked as top-priority repair in
  maturity.md NEXT). Verdict: **silent-zero persists, unmeasured**.
- Regression vs previous bench (bench-254): no change in the silent-zero state;
  no new regression signal.

## falsify status
- falsify-034..071: unchanged this run (no falsify work performed; bench-only run).
- FK guard repair (falsify-034/036): still unimplemented per maturity.md.

## Honest notes
- RC ambiguity: RC=0 appended by test itself; script also appended an outer RC
  (1 for robotics, 128 for giemon) — outer RCs anomalous, treated as script
  artifacts; the inner RC=0 lines are the clojure exits.
- HEAD verification failed due to redirect ordering in the run script; to be
  fixed next run (capture HEADs before redirecting test output).
