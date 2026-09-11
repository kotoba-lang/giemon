# bench-128 — skipped (load)

状態: HOST LOAD 超過 (15min ≥ 2×ncpu≈20) で重い test 実行は省略。正直に unmeasured 記録。基準値据え置き。

- uptime (5:04 実測): 15min ≈ 33.99 (ncpu=10 に対し 約 3.4×)。5min 21.83、1min 13.59 — LOAD gate (15min ≥ ~2×ncpu≈20) を超過帯で継続中 (ただし降坂傾向)。

- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。



- git status: giemon porcelain = 4 未追跡のみ: sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md (tracked 変更なし)。robotics status 空 — コード変更なし。





- test スイート (robotics / giemon の `kbb -M:test`): **実行せず** — load 超過帯のため省略 (bench-127 と同方針)。fg 実行継続せず。









- seeded 再現 (L1+): 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。



- 回帰 assert: **しない** (unmeasured のため honest — 基準値 bench-066 (robotics 14/50/0、giemon 46/115/0) 据え置き)。



verdict: unmeasured / skipped (load)

再現コマンド: (load 沈静後の日次で) `kbb -M:test` (robotics + giemon) + seeded run