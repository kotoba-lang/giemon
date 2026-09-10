# bench-230

- 判定: measured (実測完走)
- HOST LOAD: 実行開始時 load averages 78.82/58.08/41.53 (15min 41.53, ncpu=10, ~4.2x) — ゲート閾値超過だが実行バックエンドは応答し両スイート完走したため実測を記録。giemon 実行時 71.58/57.74/41.79、完了時 79.21/60.61/43.29。
- robotics: `clojure -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors. RC=0
- giemon: `clojure -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0
- 基準値 (bench-066: robotics 14/50/0, giemon 46/115/0) と一致。回帰なし。
- git HEAD:
  - robotics: 396fc33d0a6d51c52736231d333337e973e6fa98 (bench-227/228/229 と同一)
  - giemon: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (基準一致)
- seeded 再現 verdict: not-applicable (sim-loop は L0, 学習ジョブなし)
- falsify 状態: falsify-034 (H35, FK guard repair 未実装) 残存 / falsify-035～037 refuted 済。変化なし。
- 再現コマンド:
  - cd orgs/kotoba-lang/robotics && clojure -M:test
  - cd orgs/kotoba-lang/giemon && clojure -M:test
- 決定的記録 / タイムスタンプなし。コード変更なし。
