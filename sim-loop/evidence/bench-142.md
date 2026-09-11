# bench-142 — unmeasured ( HOST LOAD gate 超過で skip )

状態: HOST LOAD 15min 39.85 ( 8:35 実測: 1min 86.38,5min 52.85,15min 39.85) が ncpu=10 に対し 約 4.0x ( Load gate: 15min >= 2x ncpu =20) を超過。全窓( 1min,5min,15min) が gate 超過 ( >20) で応答不能リスク高。重い test スイート実行は省略 ( honest 据え置き)。

- uptime(8:35): 1min 86.38,5min 52.85,15min 39.85 — 15min が gate ( >=20) 超過。実行不可と判断。

- git HEAD: giemon d0d3cb4,robotics 9459ca0 — 基準値( bench-066 確定) と不変( 実測 git rev-parse --short 確認)。code 変更なし( giemon status は "?? sim-loop/" 未追跡のみ,robotics status 空)。

- test スイート: **unmeasured** — 負荷 gate 超過で実行省略。基準値( bench-066 確定: robotics 14/50/0,giemon 46/115/0,両者 exit 0) を据え置き,回帰 assert は行わない( honest 不測)。

- seeded 再現( L1+): 対象なし( sim-loop は L0,学習ジョブ未実装)。not-applicable。






- 回帰 assert: **なし** ( unmeasured) — コード無変更・HEAD 不変で回帰信号なし。新規 falsy なし。verdict: unmeasured( load gate) / no new regression signal

再現コマンド: 今回 skip( kbb -M:test は負荷 gate 超過で未実行)。次回 15min < 20( 2x ncpu) で実測再開予定。