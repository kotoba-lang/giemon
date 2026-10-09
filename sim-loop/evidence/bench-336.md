# bench-336 (2026-10-07 19:12 JST, main-2.local / junkawasaki)

## Host load (skip gate)
- 19:10 uptime: load 59.03 71.71 77.38 (ncpu 10)
- 19:12 uptime: load 50.25 63.65 73.25 (ncpu 10)
- 1-min ≈ 5.0x, 15-min ≈ 6.4x → 負荷 gate 超過。重い実験は一律省略。

## Verdict
- clojure -M:test (robotics / giemon): **skipped (load) unmeasured**。実行せず数字なし。
- seeded 再現 (L1 以降 sim-loop 学習ジョブ): **skipped (load) unmeasured**。
- kbb 第2経路: **skipped (load) unmeasured**。

## HEAD (実測 git log --oneline -1)
- robotics: a1af59c (Merge agent/robotics-fit-window) — 不変
- giemon: cd05afb (Merge repo-bot :landed — sim-loop evidence bench-327 + maturity.md) — 不変

## 回帰
- 本走は unmeasured につき回帰 assert せず honest。基準値 (robotics 57/624/0 kbb, giemon 46/115/0 kbb — bench-328) 据え置き。
- silent-zero (clojure runner 0/0/0 RC=0) の確認も本走は未実施 (load skip)。連続計数は bench-333 実測分まで据え置き。

## 再現コマンド (未実行・次回 gate 未満時に実施)
- cd /Users/junkawasaki/github/kotoba-lang/robotics && clojure -M:test
- cd /Users/junkawasaki/github/kotoba-lang/giemon && clojure -M:test
- kbb 両 suite (bench-328 手順)

## 備考
- giemon 作業ツリーに in-flight: M scripts/edn-datomize.bb, M sim-loop/status/_redcheck_tmp.txt, M sim-loop/status/maturity.md, ?? bench-328/331/332.md + .hermes-tmp.Ytfzs4。本走は追記のみ・コード変更なし。
- maturity.md 集計範囲: bench-001〜335。本 bench-336 は新規。
