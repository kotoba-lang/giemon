# Bench-077 — giemon sim-loop パフォーマンス記録

- 種別: bench (定例)
- 日次連番: 077
- HOST LOAD (uptime, pre-run 収集): 1min 76.38 / 5min 52.86 / 15min 41.20
  (ncpu 10 想定。1min 76 は大幅な過負荷)
- 実行バックエンド状態: terminal が空出力 (uptime/date 空、exit 0)、search_files が
  "could not stat" — read_file のみ応答。bench-069〜076 と同型の応答不能条件。

## テストスイート (kotoba-lang/robotics + kotoba-lang/giemon: clojure -M:test)

- 結果: **skipped (load + backend unresponsive)**
- テスト数 / assertion 数 / failures: 計測せず（未実行数字を捏造しない）

## Seeded 再現 (sim-loop L1 以降 / 同一 seed 2 回)

- 結果: **skipped (load + backend unresponsive)**
- 再現 verdict: 判定せず（決定的 REPL 数字の捏造禁止）

## 回帰検知

- 有無: 判定なし (skipped)
- 基準値保持: 判定未実施（bench-066 で確定済みの基準を保持のまま。本 bench で新たに評価せず）

## 再現コマンド

```
(skipped — backend 応答不能 (terminal 空出力) + load 1min 76.38 のため記録のみ。
実行環境回復後 bench-078 で再計測)
```

## 備考

- 決定的数字の捏造を避け、skipped を正直に記録。
- load 1min 76.38 は bench-064 (188) / bench-068 (160) ほどではないが、
  bench-071 (72) / bench-070 (97) と同等・超過の過負荷域。terminal/search_files が
  応答不能のため本測定は省略。
- NEXT=H28 (カメラ等の追加 down-stream consumers) の本測定も backend 回復後に
  bench-078+ で実施。静的読み取りが可能なら falsify 系で補完し得る（本 bench では
  スコープ外）。