# bench-233 (cron, 2026-09-09)

## verdict
measured — 基準値一致、回帰なし。

## detail
- HOST LOAD (pre-run): load averages 19.16 / 22.64 / 24.88 (ncpu=10, 15min 約2.5x)。
  負荷超過帯だが実行バックエンドは応答可能であったため test スイート自体は完走
  させた。重い実験 (H 本測定・seeded 再現系の追加実行) は skipped (load)。
- kbb -M:test orgs/kotoba-lang/robotics: Ran 14 tests containing 50 assertions,
  0 failures, 0 errors, RC=0。基準値 (bench-066: 14/50/0) と一致。
- kbb -M:test orgs/kotoba-lang/giemon: Ran 46 tests containing 115 assertions,
  0 failures, 0 errors, RC=0。基準値 (bench-066: 46/115/0) と一致。
- git HEAD: robotics 396fc33、giemon d0d3cb4 (giemon は baseline 一致。robotics は
  skill 記載 baseline 9459ca0 から進んでいるが bench-232 と同 HEAD、テスト数は
  基準値一致のため回帰 assert はしない、honest 記録)。
- seeded 再現: not-applicable (sim-loop は L0、L1 以降の学習ジョブ無し)。
  重い seeded 実行は本回省略 (load)。
- 回帰の有無: なし (両スイート基準値完全一致、両 RC=0、HEAD 変動は bench-232 から無し)。
- falsify 状態: falsify-034〜037 いずれも refuted 済み、残存なし。コード修正なし。

## 再現コマンド
- cd orgs/kotoba-lang/robotics && kbb -M:test
- cd orgs/kotoba-lang/giemon && kbb -M:test

決定的・タイムスタンプなし。コード修正なし。
