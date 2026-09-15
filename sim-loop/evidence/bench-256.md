# bench-256

- date: 2026-09-14 JST (cron, deterministic record; no timestamp beyond this)
- run type: measured (test suites executed), with known silent-zero caveat (see verdict)

## Host load at run start
- load averages: 19.07 19.80 27.61 (1/5/15min), hw.ncpu=10 → 15-min ≈ 1.9x ncpu
- gate: below ~2x skip threshold → heavy test runs NOT skipped for load (per skill rule)
- load at meta capture: 15.66 20.05 25.99

## Commands (reproduction)
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && git rev-parse HEAD && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && git rev-parse HEAD && kbb -M:test
```
Run via /tmp/bench256.sh (robotics) with redirect to /tmp/b256_rob.txt; giemon first pass
produced an empty /tmp/b256_gie.txt with no RC line (run aborted, cause not captured),
re-run via /tmp/b256_gie.sh completed normally. /tmp/b256_meta.txt from the combined
script was lost in the same aborted pass; HEADs + uptime captured in a separate pass.

## Test results (as measured)
- robotics: `kbb -M:test` → "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0
- giemon: `kbb -M:test` → "Ran 0 tests containing 0 assertions. 0 failures, 0 errors." RC=0

## Git HEADs
- robotics HEAD: ad99366bc7bef949e86ee33b7e04d12525dffe46 (matches maturity.md NEXT reference)
- giemon HEAD: 00fd23f9d04743323047c8c29c30aa18320daa70 (matches maturity.md NEXT reference)
- Both HEADs verified this run.

## Seeded reproduction (sim-loop L1+)
- not-applicable: sim-loop is L0, no learning job to reproduce (standing verdict).

## Regression judgement
- **unmeasured (silent-zero)**: both suites report 0/0/0 — the known cljk-rename
  silent-zero defect (maturity.md NEXT; root cause falsify-069: JVM require cannot
  load .cljk) swallows the suites. Baseline robotics 23/558/0 and giemon 46/115/0
  could NOT be re-established this run.
- This is NOT counted as a green pass and NOT counted as a test-count regression
  (the 0/0/0 is a runner defect, already tracked as top-priority repair in
  maturity.md NEXT). Verdict: **silent-zero persists, unmeasured** (continuous
  observed bench-244 → bench-256).
- Regression vs previous bench (bench-255): no change in the silent-zero state;
  no new regression signal.

## falsify status
- falsify-034..071: unchanged this run (no falsify work performed; bench-only run).
- Top-priority repair items unchanged: test-runner fix (cljk silent-zero), then
  governor silent-nil rejected-record + negative test (falsify-071 recommendation),
  then FK guard repair re-verification (falsify-034).
