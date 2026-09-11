# bench-135 — unmeasured (HOST LOAD gate 超過で skip)

状態: HOST LOAD 15min ≈ 30.76-31.01 ( 06:49 実測: 1min 35.06-42.83、5min 36.27-37.60、15min 30.76-31.01) が ncpu=10 に対し ≈ 3.1×( Load gate ( 15min ≥  󰁣×ncpu = 20) を超過 — 前回 bench-133/134 の skip 帯 ( 15min ≈24.6-25.2) を大きく上回る高負荷帯。重い test スイート実行は応答不能リスク高のため省略 ( honest 据え置き)。

- uptime (06:49):: 1min 35.06-42.83、5min 36.27-37.60、15min ≈ 30.76-31.01 — いずれも gate ( 15min ≥  󰁣20) 超過。実行不可と判断。

負荷は高止まり。( 前回 bench-134 実測 ≈25乃至上昇トレンド継続)

- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 ( bench-066 確定) と不変。code 変更なし ( giemon porcelain は `?? sim-loop/` 未追跡のみ、robotics status 空)。

- test スイート: **unmeasured** — 負荷 gate 超過で実行省略。基準値 ( bench-066 確定: robotics  󰁣14/50/0、giemon 46/115/0、両者 exit 0) を据え置き、回帰 assert は行わない ( honest 不測)。

- seeded 再現 ( L1+):: 対象なし ( sim-loop は L0、学習ジョブ未実装)。not-applicable。

  - 回帰 assert: **なし** ( unmeasured) — コード無変更・HEAD 不変で回帰信号なし。新規 falsy なし ( H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。verdict: unmeasured ( load gate) / no new regression signal

再現コマンド: 今回 skip ( `kbb -M:test` は負荷 gate 超過で未実行)。次回 15min < 20 ( 2×ncpu) で実測再開予定。