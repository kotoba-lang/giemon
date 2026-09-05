# bench-17 — 2026-09-04 (JST)

## Host load
- 11:35 JST: load averages 52.53 / 48.53 / 47.11, up 11 days (コア 10)
- 11:41 JST: load averages 65.73 / 60.06 / 53.00
- 高負荷のため重い seeded 再現実験は **skipped (load)**。

## テスト実行 (`clojure -M:test`)
| repo | tests | assertions | failures | errors | 前回比 |
|---|---|---|---|---|---|
| orgs/kotoba-lang/robotics | 14 | 50 | 0 | 0 | bench-4〜16 と同一数字、回帰なし |
| orgs/kotoba-lang/giemon | 46 | 115 | 0 | 0 | bench-4〜16 と同一数字、回帰なし |

回帰: なし。

## seeded 再現実行
- **not-run**: 対象不在 (`grep -rl seed src` in giemon → 0 件、bench-14/15/16 と同様)。
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
