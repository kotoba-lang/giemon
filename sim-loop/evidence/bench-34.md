# bench-34 (2026-09-04 21:09 JST)

## テスト実行 (`clojure -M:test`)

| org | tests | assertions | failures | errors |
|---|---|---|---|---|
| kotoba-lang/robotics | 14 | 50 | 0 | 0 |
| kotoba-lang/giemon | 46 | 115 | 0 | 0 |

前回 (bench-33) 比較: robotics 14/50, giemon 46/115 — 30 連続同一数字。回帰なし。

## seeded 再現実行

- 対象不在: `grep -rl seed src` (giemon) → 0 件。学習ジョブコードなしのため **not-run**。

## HOST LOAD

- load averages: 43.10 46.41 38.48 / コア 10 → 高負荷。重い追加実験は **skipped (load)**。
- 軽量テスト実行は完了 (上記)。seeded 再現は対象不在のため負荷と無関係に not-run。

## verdict

- 回帰: なし
- 再現: not-run (seeded ジョブ不在)

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
grep -rl seed src   # giemon (対象確認)
```
