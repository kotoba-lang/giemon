# bench-18 — 2026-09-04 (JST)

## Host load
- 11:50 JST: load averages 66.93 / 53.87 / 51.56, up 11 days (コア 10)
- 11:55 JST: load averages 54.61 / 55.19 / 53.07
- 高負荷のため重い seeded 再現実験は **skipped (load)**。

## テスト実行 (`clojure -M:test`)
| repo | tests | assertions | failures | errors | 前回比 |
|---|---|---|---|---|---|
| orgs/kotoba-lang/robotics | 14 | 50 | 0 | 0 | bench-4〜17 と同一数字、回帰なし |
| orgs/kotoba-lang/giemon | 46 | 115 | 0 | 0 | bench-4〜17 と同一数字、回帰なし |

実行時間: robotics 53s / giemon 71s (wall)。

回帰: なし。

## seeded 再現実行
- **not-run**: 対象不在 (`grep -rl seed src` in giemon → 0 件、bench-14〜17 と同様)。
  学習ジョブ (L1 以降) のコードが未実装のため seeded 再現は実行不能のまま。

## 備考
- コード修正なし (本 bot の役割外)。
- OPEN 赤は maturity.md の NEXT 項目のまま: falsify-1 fixture 修理 (3 キーのダブルエンコード解除)、
  falsify-6/10/11 torque fail-closed 化、falsify-7/8/9 facade 降格塞ぎ、falsify-12 rob 側 kind×class 結合検査、
  falsify-13 gate allowed-set nil 除去 + nil-safety :invalid 化。未着手。

## 再現コマンド
```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
grep -rl seed src | wc -l   # 0 → seeded 再現 not-run
```
