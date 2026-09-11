# bench-074 — SKIPPED (load / backend unresponsive)

host load (pre-run): 31.32 / 31.40 / 37.00 (1/5/15 min), ncpu=10, 15 users.
実行バックエンド (terminal) が空出力 (date/uptime 空、exit 0) のまま応答不能。
search_files / read_file も sandbox stat 不能で応答せず。

- kbb -M:test (robotics):   skipped (backend unresponsive)
- kbb -M:test (giemon):     skipped (backend unresponsive)
- seeded 再現 (L1+):            skipped (backend unresponsive)

回帰有無: 判定不能 (基準値は bench-066 で確定済み; load 超過により本測定なし)
再現コマンド: (実行不可)