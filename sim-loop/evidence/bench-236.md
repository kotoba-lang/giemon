# bench-236

- 判定: unmeasured — skipped (load)
- load: 15-min 26.54, 1-min 14.81 / ncpu 10 (hw.ncpu)。15-min ≥ 2x ncpu (20) のため
  重い実行 (`kbb -M:test` 両プロジェクト、seeded 再現) を省略。
- tests: robotics — skipped (load) / giemon — skipped (load)。test 数・assertion 数は本測定なし。
- seeded repro: skipped (load)。
- 回帰: 不明 (本測定なし)。基準値 (robotics 14/50/0、giemon 46/115/0) は据え置き、
  回帰 assert はしない (honest)。
- falsify status: 変更なし。falsify-034 (H35, FK guard repair 未実装) は open のまま。
- 再現コマンド: `cd orgs/kotoba-lang/robotics && kbb -M:test`、
  `cd orgs/kotoba-lang/giemon && kbb -M:test` (load 許容時に実施)。
- git HEAD: 本測定で確認せず (load gate skip)。前回記録値: giemon d0d3cb4 / robotics 9459ca0。
- コード変更: なし。
