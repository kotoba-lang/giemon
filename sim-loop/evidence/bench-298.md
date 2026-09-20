# bench-298

- HEAD: robotics ad99366 / giemon 41ac173 (bench-297 と同値、不変)
- load: 15-min 16.07 / ncpu 10 ≈ 1.6x (開始時) → gate 未満 (≈2x 未満)、実行判定
- 実行: `clojure -M:test` 両 suite 完走 (/tmp redirect 経由)

## テスト結果 (実測)

| suite | tests | assertions | failures | RC |
|---|---|---|---|---|
| robotics | 0 | 0 | 0 | 0 |
| giemon  | 0 | 0 | 0 | 0 |

→ **silent-zero 持続**: bench-244〜298 実測分で 41 連続。runner 修復未了
(falsify-069 確定済み: JVM require が `.cljk` をロード不能のため 0/0/0 緑に見える)。

## seeded 再現

not-applicable (sim-loop は L0、学習ジョブ無し)。

## 回帰判定

- 基準値 (robotics 23/558/0 / giemon 46/115/0) は silent-zero のため測定不能、据え置き。
- 回帰 assert なし — **unmeasured (honest)**、実測分は 0/0/0 の持続記録。

## 再現コマンド

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics && clojure -M:test
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon && clojure -M:test
```

## falsify 状態

falsify-034 (FK guard repair) 以降 39 連続 refuted・未着手。falsify-069 (runner 根因) 確定済み。

## 判定

**judgement: measured (silent-zero 持続)** / 回帰: なし (測定不能に伴う assert なし) / コード変更: なし。
