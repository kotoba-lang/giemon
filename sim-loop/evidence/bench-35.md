# bench-35 (2026-09-04 22:08 JST)

## テスト実行 (`kbb -M:test`)

| org | tests | assertions | failures | errors |
|---|---|---|---|---|
| kotoba-lang/robotics | 14 | 50 | 0 | 0 |
| kotoba-lang/giemon | 46 | 115 | 0 | 0 |

前回 (bench-34) 比較: robotics 14/50, giemon 46/115 — 31 連続同一数字。回帰なし。

## seeded 再現実行

- 対象不在: `grep -rl seed src` (giemon) → 0 件。学習ジョブコードなしのため **not-run**。

## HOST LOAD

- load averages: 26.50 30.55 35.60 / コア 10 → 高負荷。重い追加実験は **skipped (load)**。
- 軽量テスト実行は完了 (上記)。seeded 再現は対象不在のため負荷と無関係に not-run。

## verdict

- 回帰: なし
- 再現: not-run (seeded ジョブ不在)

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
grep -rl seed src   # giemon (対象確認)
```
