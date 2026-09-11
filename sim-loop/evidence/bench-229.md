# bench-229

- 判定: measured (実測完走)
- HOST LOAD: 実行開始時 load averages 32.42/32.53/28.60 (15min 28.60, ncpu=10, ~2.9x) — ゲート閾値超過だが実行バックエンドは応答し両スイート完走したため実測を記録。完了時 load averages 34.43/33.95/29.79。
- robotics: `kbb -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors. RC=0
- giemon: `kbb -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0
- 基準値 (bench-066: robotics 14/50/0, giemon 46/115/0) と一致。回帰なし。
- git HEAD:
  - robotics: 396fc33 (bench-227/228 と同一)
  - giemon: d0d3cb4 (基準一致)
- seeded 再現 verdict: not-applicable (sim-loop は L0, 学習ジョブなし)
- falsify 状態: falsify-034 (H35, FK guard repair 未実装) 残存 / falsify-035～037 refuted 済。変化なし。
- 再現コマンド:
  - cd orgs/kotoba-lang/robotics && kbb -M:test
  - cd orgs/kotoba-lang/giemon && kbb -M:test
- 決定的記録 / タイムスタンプなし。コード変更なし。
