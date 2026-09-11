# bench-27 (2026-09-04 14:51 JST, cron)

## テスト
- robotics: `kbb -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
- giemon:   `kbb -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors.
- 前回 (bench-26) 比: 同値。回帰なし。

## seeded 再現
- `grep -rl seed src` → 0 件。seeded 学習ジョブ対象不在のため **not-run** (bench-14〜26 と同値)。

## 負荷
- load averages: 39.04 / 49.71 / 54.83 (コア 10)。高負荷のため重い追加実験は **skipped (load)**。
  軽量テスト実行のみ実施。

## verdict
- 回帰: なし。テスト 14/50 + 46/115, 0 failures 0 errors。
- 再現: not-run (対象不在)。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon   && kbb -M:test
grep -rl seed src
```
