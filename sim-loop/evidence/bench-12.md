# bench-12

- date-factor: cron 実行 (決定的記録・タイムスタンプなし)
- HOST LOAD: load averages 約 17.2–18.0 (1min/5min) / コア 10 (高負荷) → 重い実験は skipped (load)

## テスト実行

コマンド: `clojure -M:test` (各 repo で実行)

| repo | tests | assertions | failures | errors |
|---|---|---|---|---|
| robotics | 14 | 50 | 0 | 0 |
| giemon | 46 | 115 | 0 | 0 |

- 前回比 (bench-4〜11 と同一数字): 回帰なし。
- fixtures/giemon_arm6 EDN 二重エンコード (falsify-1, refuted) は未修理のまま。コード修正は本 bot の対象外。

## seeded 再現実行 (L1 以降の学習ジョブ)

- not-run: 対象不在 (giemon/src 配下 `seed` を含むファイル 0 件を再確認、`grep -rl seed src` → 0)。
- 重い追加実験: skipped (load)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon   && clojure -M:test
```

verdict: 回帰なし / 再現実行 not-run (対象不在) / 重い実験 skipped (load)
