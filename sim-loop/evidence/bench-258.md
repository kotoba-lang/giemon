# bench-258

- judgement: measured (実行は完走。ただし既知 silent-zero 状態の持続観測)
- load: 22:06 JST, load 1m 10.40 / 15m 12.70, ncpu 10 (~1.3x) → 重い実験は通常実施 (2x gate 未満)
- HEADs: robotics ad99366 / giemon 00fd23f (前回 bench-257 と同一)

## kbb -M:test

- robotics: Ran 0 tests containing 0 assertions. 0 failures, 0 errors. RC=0
- giemon:   Ran 0 tests containing 0 assertions. 0 failures, 0 errors. RC=0

両 suite とも silent-zero (0/0/0 RC=0) が持続。bench-244〜257 と同一症状。
根因確定済 (falsify-069: JVM require が .cljk をロード不能) — runner 修復待ち。
基準値 robotics 23/558/0・giemon 46/115/0 の実測緑は現 HEAD で再現できず (既知回帰、追加の新規赤なし)。

## seeded 再現

- sim-loop は L0, 学習ジョブ無し → not-applicable。

## 回帰

- 回帰 assert: なし (silent-zero は bench-244 起の既知状態、変化なし)
- NEXT 項目 (test-runner 修復 / governor rejected レコード化+負テスト / FK guard repair) は未着手を確認

## 再現コマンド

cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && kbb -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && kbb -M:test

コード変更なし。
