# bench-28 (2026-09-04 15:06 JST, cron)

## テスト
- robotics: `clojure -M:test` → Ran 14 tests containing 50 assertions. 0 failures, 0 errors.
- giemon:   `clojure -M:test` → Ran 46 tests containing 115 assertions. 0 failures, 0 errors.
- 前回 (bench-27) 比: 同値。回帰なし。

## seeded 再現
- `grep -rl seed src` → 0 件。seeded 学習ジョブ対象不在のため **not-run** (bench-14〜27 と同値)。

## 負荷
- load averages: 31.33 / 33.60 / 42.06 (コア 10)。高負荷のため重い追加実験は **skipped (load)**。
  軽量テスト実行のみ実施。

## verdict
- 回帰: なし。テスト 14/50 + 46/115, 0 failures 0 errors。
- 再現: not-run (対象不在)。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon   && clojure -M:test
grep -rl seed src
```
