# bench-15

日時なし (決定的記録)。実行コマンド:
- `cd orgs/kotoba-lang/robotics && kbb -M:test`
- `cd orgs/kotoba-lang/giemon && kbb -M:test`

## テスト結果

| project | tests | assertions | failures | errors | 前回 (bench-14) 比 |
|---|---|---|---|---|---|
| kotoba.robotics | 14 | 50 | 0 | 0 | 同一 (回帰なし) |
| kotoba.giemon | 46 | 115 | 0 | 0 | 同一 (回帰なし) |

## seeded 再現

not-run (対象不在: `grep -rl seed src` → 0 件、bench-14 と同様)。

## 負荷

load averages 約 38-41 / コア 10 (実測)。重い追加実験は skipped (load)。

## 回帰の有無

なし。falsify-1 (fixture 二重エンコード) の修理は本ベンチでは未実施 (コード修正は範囲外)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon && kbb -M:test
```
