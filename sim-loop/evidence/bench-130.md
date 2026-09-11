# bench-130 — load 超過 skip ( unmeasured)

状態: HOST LOAD 15min ~23.15 が ncpu=10 の ~2.3× で Load gate (15min ≥ 2×ncpu=20) 超過の負荷帯。重い test スイート実行を一律 skipped し honest に unmeasured 記録 (回帰 assert せず、基准値据え置き)。

- uptime (5:34 実測): 15min ≈ 23.15 (ncpu=10 に対し 約 2.3×)。5min 34.83、1min 34.83 — Load gate 超過帯で計測不能 ( bench-064～101 連続 load 超过 と同水準)。

- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基准値 ( bench-066 確定) と不変。code 変更なし ( giemon porcelain は `?? sim-loop/` 未追跡のみ、robotics status 空)。

- test スイート: **skipped (load)** — Load gate 超過で実行不要・honest に unmeasured。基準値 14/50/0 ( robotics)・46/115/0 ( giemon) 据え置き、回帰 assert せず。



- seeded 再現 ( L1+):  対象なし ( sim-loop は L0、学習ジョブ未実装)。not-applicable。



- 回帰 assert: **なし** ( unmeasured) — 実行不能帯のため回帰判定せず、新規 falsy なし ( H25～H41 全決着・未決残存なし、code 無変更で新仮説判定なし)。verdict: unmeasured (load above gate) / no new regression signal

再現コマンド: 未実行 ( load gate 超過で skip、`kbb -M:test` 省略)。seeded 再現は L0 で N/A。