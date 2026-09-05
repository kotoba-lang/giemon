# bench-8

日時決定記録なし (タイムスタンプなし・決定的記録)。

## テスト実行 (`clojure -M:test`)

| repo | tests | assertions | failures | errors |
|---|---|---|---|---|
| orgs/kotoba-lang/robotics | 14 | 50 | 0 | 0 |
| orgs/kotoba-lang/giemon | 46 | 115 | 0 | 0 |

前回比 (bench-4〜7 と同一数字): robotics 14/50, giemon 46/115, 0 failures 0 errors。
回帰なし。

## seeded 再現実行

対象不在のため not-run: src 配下に `seed` を含むファイル 0 件 (grep で再確認)、
学習ジョブ (L1 以降) の実装なし。成熟度「再現性 0」と整合。

## HOST LOAD 判定

load average 約 17-22 (コア 10) — 高負荷。重い追加実験は skipped (load)。
軽量テスト実行のみ実施し上記に記録済み。

## 回帰

なし。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon && clojure -M:test
```
