# bench-084

date: (未記録 — 実行バックエンド応答不能)
seed: n/a
command: n/a(実行不能)

test スイート: skipped (backend)
seeded 再現: skipped (backend)
回帰: 判定不能 (backend 応答不能)

## 理由
実行バックエンド (terminal / search) が応答不能: terminal は空出力 (echo/date/uptime すべて空、exit 0)、
sandbox stat 不能 (could not stat). HOST LOAD (pre-run 時点, 15:19) 27.67 / 24.24 /
24.87、ncpu=10、users=13。bench-077〜083 と同型の応答不能条件のため、test スイート・
seeded 再現とも省略した (skipped (backend))。決定的な falsify 静的読取も、sandbox が file
system を stat できず、ファイル読取不能のため実施不能。回帰判定は次回以降に持ち越し。

## next
- backend 復旧後、bench-084 を再実施 (テスト数 / 再現 verdict / 回帰有無 を記録)。
- 既存 bench-077〜083 (同型応答不能記録) との整合確認。