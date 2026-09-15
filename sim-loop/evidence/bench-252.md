# bench-252

judgement: **measured (silent-zero regression persists)**

- date-run: 2026-09-14 04:19 JST (決定的・タイムスタンプは記録のみ)
- host load: `up 8 days, 21:02, load averages: 15.85 15.41 15.82`, hw.ncpu=10
  → 15-min ≈ 1.6x < 2x gate, therefore ran (not skipped).

## test suites (kbb -M:test, /tmp redirect workaround)

| project | HEAD | tests | assertions | failures | RC |
|---|---|---|---|---|---|
| robotics | ad99366bc7bef949e86ee33b7e04d12525dffe46 | 0 | 0 | 0 | 0 |
| giemon | 00fd23f9d04743323047c8c29c30aa18320daa70 | 0 | 0 | 0 | 0 |

baseline: robotics 23/558/0, giemon 46/115/0 (bench-066 / maturity.md NEXT)。
実測は両 project とも **0/0/0 RC=0 の silent-zero** — `kbb -M:test` は緑を
装って何も測っていない (raw: "Ran 0 tests containing 0 assertions." / both HEADs
unchanged from bench-251)。maturity.md NEXT の test-runner 修復 (cljk rename 後の
silent-zero, kbb --classpath src:test + 明示 require で 21/52/0 緑という第2測定経路,
46/115 完全回復には deps floor 接続 + host interop 修正が別途必要) は
**解消されていない**。base 値との比較は不能、regression assert はしない
(honest: unmeasured-equivalent)。

## seeded reproduction

sim-loop は L0 (学習ジョブ無し) → not-applicable。skill 上 seeded 再現対象なし。

## regression

無しと主張できない (suite が 0 件走行 = 計測不能)。回帰検知は test-runner 修復まで停止中。

## falsify status

falsify-037 (H38, slice anchor bug) まで確定・残存項目なし。本 run での新規 falsify 無し。

## repro command

```
bash -c 'cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test'
bash -c 'cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test'
# → 両方 "Ran 0 tests containing 0 assertions." RC=0 (silent-zero)
```
