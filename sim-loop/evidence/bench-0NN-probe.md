# bench-0NN — skipped (backend unavailable / load)

状態: terminal バックエンドが全コマンドに対して空出力 exit 0 (`date`/`uptime`/`printf` とも空)、
filesystem sandbox が stat 不能 (search_files が `kotoba-lang` 自体を stat 不可と報告)。
前回 bench-077〜083 と同一の "terminal 空出力 exit 0 / sandbox stat 不能" 応答不能条件。

実行: `clojure -M:test` (robotics / giemon)、seeded 再現 (L1以降) とも **skipped**。
バックエンドが戻らない (全ツールが空/ stat 不可) ため実測不能。誇張なし。

- test スイート: skipped (backend unavailable)
- seeded 再現: skipped (backend unavailable)
- 回帰: 判定不能 (実測なし)
- 再現コマンド: 該当なし (実行不能)

pre-run HOST LOAD: 28.58 / 32.97 / 31.17 (1min/5min/15min)