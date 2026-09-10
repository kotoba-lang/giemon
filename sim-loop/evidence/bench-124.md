# bench-124 — skipped (load)

状態: HOST LOAD 超過 (15min ≥ 2×ncpu≈20) で重い test 実行は省略。正直に unmeasured 記録。基準値据え置き。

- uptime (4:04〜4:09 実測): 15min = 26.22 → 30.64 (ncpu=10 に対し 約 2.6×〜3.1×)。1min 45〜50、5min 38〜41 — LOAD gate (15min ≥ ~2×ncpu≈20) 超過帯で継続上昇中。
- git HEAD: giemon `d0d3cb4`、robotics `9459ca0` — 基準値 (bench-066 確定) と不変。
- git status: giemon porcelain = 4 未追跡のみ: sim-loop/・simloop_files_list.txt・statout.txt・tmp_probe_write.md (tracked 変更なし)。robotics status 空 — コード変更なし。
- test スイート (robotics / giemon の `clojure -M:test`): **実行せず** — load 超過帯のため省略 (bench-099〜101 と同方針;本 walk は backend も起動直後に一時 stat 不能シグナルあり)。fg 実行継続せず。
- seeded 再現 (L1+): 対象なし (sim-loop L0、学習ジョブ未実装)。未実行。
- 回帰 assert: **しない** (unmeasured のため honest — 基準値 bench-066 (robotics 14/50/0、giemon 46/115/0) 据え置き)。

verdict: unmeasured / skipped (load)
再現コマンド: (load 沈静後の日次で) `clojure -M:test` (robotics + giemon) + seeded run