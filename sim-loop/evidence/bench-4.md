# giemon sim-loop bench — bench-4

日時: 2026-09-03T18:02:00+0900 (JST)

## HOST LOAD

- load averages: **13.25 14.03 18.73** (uptime, 10 cores)。bench-3 時点の 36.36 から
  低下傾向 (1min 13.25 はコア数の約 1.3 倍)。bench-3 の指示「次回は負荷が許せば必ず
  テストを実行して 4 連続 skip を避けること」に従いテストを実行した。

## テスト実行 (clojure -M:test)

- robotics: **実行済み** — `Ran 14 tests containing 50 assertions. 0 failures, 0 errors.`
- giemon: **実行済み** — `Ran 46 tests containing 115 assertions. 0 failures, 0 errors.`
- 合計: **60 tests / 165 assertions / 0 failures / 0 errors**。

## 前回比 / 回帰の有無

- **回帰判定不可 (ベースライン初回)** — bench-1〜3 は全てテスト未実行 (skipped (load))
  であり比較対象の数字が存在しない。本記録が最初の実行済み記録で、以降の比較基準になる。
- 新規赤なし: robotics / giemon とも 0 failures。既存の OPEN 赤 (falsify-1 refuted) に変化なし。

## seeded 再現実行 (L1 以降)

- **not-run** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0, 現在段階 L0 のまま)。
  同一 seed で 2 回実行すべき対象が存在しないため実行不可。負荷は本回では問題にならない
  (テストは実行済み) が、対象未整備のため verdict は **not-run** のまま。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
```

(本記録では上記 2 つの clojure コマンドを実行済み。出力は「テスト実行」節に記載。)

## 次回への引き継ぎ

- 次回から bench-4 の数字 (robotics 14/50, giemon 46/115) が比較基準。減少・failure 増は
  回帰として赤記録すること。
- seeded 再現は引き続き maturity の再現性スコアが 0 の間は not-run と正直に記録する。
