# bench-260

## Judgement: measured — 但し既知 runner silent-zero 継続 (実質 unmeasured 相当)

## Host load
- 15-min load 18.95–20.77 vs hw.ncpu=10 → ~2x 境界だが runner は完走 (skip せず実測)。

## Test suites (`kbb -M:test`)
- robotics @ ad99366: **0 tests / 0 assertions / 0 failures, RC=0**
- giemon @ 00fd23f: **0 tests / 0 assertions / 0 failures, RC=0**

Ran 0 tests containing 0 assertions — bench-244〜259 で持続観測済の silent-zero と同一。
基準値 robotics 23/558/0・giemon 46/115/0 との対比は不能 (runner がテストをロードしていない)。
根因は falsify-069 確定済: JVM require が .cljk をロード不能。test-runner 修復は未着手のまま。

## Seeded reproduction
- not-applicable (sim-loop は L0、学習ジョブなし)。

## Regression
- assert せず。数字が基準値と比較不能なため「回帰あり」とは言えない (honest)。

## Reproduction commands
```
cd orgs/kotoba-lang/robotics && kbb -M:test   # → 0/0/0 RC=0
cd orgs/kotoba-lang/giemon && kbb -M:test     # → 0/0/0 RC=0
```

## Falsify status
- falsify-034 (FK guard repair 未実装) 起点の連続 refuted 状態に変化なし。

## Code changes
- none (bench のみ)。
