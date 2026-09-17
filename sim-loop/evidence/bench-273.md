# bench-273 — giemon sim-loop bench

## Judgement
**unmeasured (load)** — HOST LOAD が閾値を超過したため重い実験 (clojure -M:test 両 suite、seeded 再現) を省略した。

## Host load
`load averages: 49.16 42.51 73.36` (15-min ≈ 4.3× vs ncpu=10)。uptime 閾値 (~2×) 超過 → test スイート実行を skip。

## Tests
- robotics `clojure -M:test`: **skipped (load)** — 基準値 23/558/0 据え置き。
- giemon `clojure -M:test`: **skipped (load)** — 基準値 46/115/0 据え置き。
- 回帰 assert は行わない (honest: unmeasured)。

## Seeded reproduction
**not-applicable / skipped (load)** — sim-loop L0、重いジョブは省略。

## Regression
**none claimed** — 本回は実測なしのため回帰判定なし。

## Falsify status
falsify-034 (H35 FK guard repair) 残存・未着手のまま。NEXT (test-runner 修復: silent-zero 27 連続実測、kbb -M:test RC=1 hard-fail) 変更なし。

## Repro command
本回は実行コマンドなし (load gate)。通常: `cd orgs/kotoba-lang/robotics && clojure -M:test` / `cd orgs/kotoba-lang/giemon && clojure -M:test`。

## HEADs
未測定 (load gate で git 呼び出しも省略)。前回 bench-272 時点: robotics ad99366 / giemon 41ac173。

## In-flight (uncommitted, pre-run script)
- M sim-loop/status/maturity.md
- ?? sim-loop/evidence/bench-270.md, bench-271.md, bench-272.md, falsify-074.md

no code change.
