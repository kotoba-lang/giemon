# bench-228

- 判定: measured (実測完走)
- HOST LOAD: 実行開始時 load averages 29.81/27.29/27.10 (15min 27.10, ncpu=10, ~2.7x) — ゲート閾値超過のため本走は skipped (load) の候補だったが、実行バックエンドは応答し両スイート完走したため実測を記録。完了時 load averages 11.89/21.05/24.63。
- robotics: `kbb -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors. RC=0
- giemon: `kbb -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors. RC=0
- 基準値 (bench-066: robotics 14/50/0, giemon 46/115/0) と一致。回帰なし。
- git HEAD:
  - robotics: 396fc33d0a6d51c52736231d333337e973e6fa98 (bench-227 と同一。skill 基準メモの 9459ca0 から進んでいるが数字一致のため回帰 assert はしない)
  - giemon: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (基準一致)
- seeded 再現 verdict: not-applicable (sim-loop は L0, 学習ジョブなし)
- falsify 状態: falsify-034 (H35, FK guard repair 未実装) 残存 / falsify-035～037 refuted 済。変化なし。
- 再現コマンド:
  - cd orgs/kotoba-lang/robotics && kbb -M:test
  - cd orgs/kotoba-lang/giemon && kbb -M:test
- 決定的記録 / タイムスタンプなし。コード変更なし。
