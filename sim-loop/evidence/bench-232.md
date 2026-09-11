# bench-232 (cron, 2026-09-09)

## verdict
measured — 基準値一致、回帰なし。

## detail
- HOST LOAD (pre-run): load averages 19.64 / 25.65 / 24.61 (ncpu=10, 15min 約2.6x)。
  負荷超過帯だが実行バックエンドは応答可能であったため、本来の省略対象 (重い実験)
  のみ控え、test スイート自体は完走させた。実行後 15min load は 32.75 まで上昇。
- kbb -M:test orgs/kotoba-lang/robotics: 14 tests / 50 assertions / 0 failures,
  0 errors, RC=0。基準値 (bench-066: 14/50/0) と一致。
- kbb -M:test orgs/kotoba-lang/giemon: 46 tests / 115 assertions / 0 failures,
  0 errors, RC=0。基準値 (bench-066: 46/115/0) と一致。
- git HEAD: giemon d0d3cb4 (baseline 一致)。robotics 396fc33 (skill 記載 baseline
  9459ca0 から進んでいる。テスト数は基準値一致のため回帰 assert はしない、honest 記録)。
- seeded 再現: not-applicable (sim-loop は L0、L1 以降の学習ジョブ無し)。
- 回帰の有無: なし (両スイート基準値完全一致、両 RC=0)。
- falsify 状態: falsify-034〜037 いずれも refuted 済み、残存なし。コード修正なし。

## 再現コマンド
- cd orgs/kotoba-lang/robotics && kbb -M:test
- cd orgs/kotoba-lang/giemon && kbb -M:test

決定的・タイムスタンプなし。コード修正なし。
