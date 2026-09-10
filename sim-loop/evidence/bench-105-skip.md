# bench-105 — skipped (load + backend unresponsive)

状態: HOST LOAD 超過 + 実行バックエンド (terminal/search/sandbox stat) 応答不能。

- uptime (pre-run): 18.79 / 24.35 / 33.61 (ncpu=10 に対し 1min≈1.9x, 15min≈3.4x)
- test スイート (robotics / giemon): 実行不能 — backend が全ディレクトリを stat
  できず ("Terminal environment unavailable: could not stat ... the sandbox may
  still be starting or was removed")、terminal も出力空。
- seeded 再現 (L1+): 未実行 (同上)。
- 回帰 assert: しない (unmeasured のため honest — 基準値 bench-066/102 据え置き)。

verdict: unmeasured / skipped (load)
再現コマンド: (backend 復旧後の日次で) clojure -M:test + seeded run