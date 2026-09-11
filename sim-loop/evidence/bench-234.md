# bench-234 (load skip)

## Judgement
unmeasured — HOST LOAD 超過のため test スイート・seeded 再現を skip。
基準値 (robotics 14/50/0, giemon 46/115/0) は据え置き、回帰 assert はしない (honest)。

## HOST LOAD (計測時点)
`22:05, up 4 days, 14:48, load averages: 22.49 23.57 29.82`
ncpu = 10 → 15-min load 23.57 ≈ 2.36x ncpu。skill のゲート (~2x) を超過。
重い `kbb -M:test` 実行は省略した。

## Test numbers
not measured this run (load gate)。

## Seeded reproduction
not-applicable / not measured (sim-loop L0、load gate)。

## Git HEADs
- giemon: d0d3cb4 (基準値確定時点から変化なし)
- robotics: 396fc33 (skill 基準メモの 9459ca0 から移動。回帰判定は不可能なので観測のみ記録)

## Regression
unknown (unmeasured) — load により判定不能。

## Falsify status
falsify-034 残存なし (maturity.md 正本どおり、変更なし)。

## Reproduction command
`uptime` (load 確認) → load 2.36x ncpu で skip。
次回は負荷が下がった段階で `cd orgs/kotoba-lang/robotics && kbb -M:test` と
`cd orgs/kotoba-lang/giemon && kbb -M:test` を実行し基準値 14/50/0・46/115/0 と比較。
