# bench-14 (daily bench, cron)

日付なし (決定的記録・タイムスタンプ方針準拠)

## テスト実行 (`kbb -M:test`)

- orgs/kotoba-lang/robotics: 14 tests / 50 assertions / 0 failures / 0 errors
- orgs/kotoba-lang/giemon: 46 tests / 115 assertions / 0 failures / 0 errors

前回比: bench-4〜13 と同一数字 (14/50 + 46/115)。回帰なし。

## seeded 再現実行 (sim-loop 学習ジョブ, L1 以降)

- verdict: not-run (対象不在)
- 根拠: `grep -rl seed src` → 0 件 (学習ジョブ seed コードは src 配下に存在しない。
  bench-1〜13 と同様、再現対象の seeded 学習ジョブは未整備)

## HOST LOAD

- load averages: 約 20.6-25.0 / コア 10 (高水準)。軽量テストは実行維持し、
  重い追加実験は skipped (load)。

## 回帰の有無

- なし (テスト数 / assertion 数とも前回と完全一致、failures 0)

## 再現コマンド

- `cd orgs/kotoba-lang/robotics && kbb -M:test`
- `cd orgs/kotoba-lang/giemon && kbb -M:test`
- `grep -rl seed src` (giemon, seeded 学習ジョブ有無確認)
