# bench-125 — skipped (load)

状態: HOST LOAD 超過 (15min ≥ 2×ncpu≈20) で重い test 実行は省略。正直に unmeasured 記録。基準値据え置き。

- uptime (4:20〜4:21 実測): 15min = 48.18 → 51.39 (ncpu=10 に対し 約 4.8×〜5.1×)。1min 77〜87、5min 62〜68 — LOAD gate (15min ≥ ~2×ncpu≈20) を大きく超過し継続上昇中。
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。
- git status: giemon porcelain = 4 未追跡のみ: sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md (tracked 変更なし)。robotics status 空 — コード変更なし。
- test スイート (robotics / giemon の `clojure -M:test`): **実行せず** — load 超過帯のため省略 (bench-099〜101、bench-124 と同方針)。fg 実行継続せず。
- seeded 再現 (L1+): 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。
- 回帰 assert: **しない** (unmeasured のため honest — 基準値 bench-066 (robotics 14/50/0、giemon 46/115/0) 据え置き)。

verdict: unmeasured / skipped (load)
再現コマンド: (load 沈静後の日次で) `clojure -M:test` (robotics + giemon) + seeded run