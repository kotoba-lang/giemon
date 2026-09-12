# bench-242

## Judgement
unmeasured — HOST LOAD 超過のためテストスイート・seeded 再現を skipped (load)。

## Load gate
- 19:15 JST, up 6 days, load averages: 43.01 / 42.07 / 46.62 (15-min ≈ 42.07)
- hw.ncpu = 10 → 15-min ≈ 4.2x ncpu、ゲート閾値 (≥ ~2x) を大きく超過。
- bench-102 系列と同様、重い実験は省略。honest に unmeasured、基準値は据え置き (regression assert なし)。

## Baseline (unchanged reference)
- robotics: 23/558/0 @ HEAD 893ef76 (bench-240 確定値; 旧 14/50/0 @ 9459ca0)
- giemon: 46/115/0 @ HEAD d0d3cb4

## Seeded reproduction
not-applicable (sim-loop is L0, no learning job; L1 以降の seeded 再現対象なし)

## Regression
assert しない (unmeasured)。前回測定値から回帰・改善ともに判定材料なし。

## Falsify status
falsify-034 (H35) 残存 — FK angle-count guard repair 未実装 (arm.cljc L38 silent zero-fill、arm_test.cljc 20-22 緑 zero-fill 無変更)。変更なし (本回はコード読取・実行とも未実施のため、status/maturity.md の記載を引き継ぐ)。

## Repro commands
- 本回は skipped (load)。測定時の標準手順:
  - `cd orgs/kotoba-lang/robotics && clojure -M:test`
  - `cd orgs/kotoba-lang/giemon && clojure -M:test`
  - 注意: background terminal では workdir が無視されるため `cd ... && clojure -M:test > /tmp/out.txt 2>&1` 形式のスクリプトを使用。

## Notes
- 決定的記録・タイムスタンプなし。コード変更なし。
