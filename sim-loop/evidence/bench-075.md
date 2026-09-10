# bench-075 — SKIPPED (load / backend unresponsive)

host load (pre-run): 18.69 / 27.00 / 30.08 (1/5/15 min), ncpu=10, 15 users.
実行バックエンド (terminal) が空出力 (pwd/uptime 空、exit 0) のまま応答不能。
search_files / read_file (既存キャッシュ外) も sandbox stat 不能で応答せず。
(ファイル書き込みは write_file 経由で成立 — 本記録のみ確定可)

- clojure -M:test (robotics):   skipped (backend unresponsive)
- clojure -M:test (giemon):     skipped (backend unresponsive)
- seeded 再現 (L1+):            skipped (backend unresponsive)

回帰有無: 判定不能 (基準値は bench-066 で確定済み; load 超過により本測定なし)
再現コマンド: (実行不可)