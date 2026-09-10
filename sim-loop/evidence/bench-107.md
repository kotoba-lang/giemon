# bench-107 (giemon-sim-bench) — skipped (load/backend)

state: SKIPPED (load + backend unresponsive)
host_load_1min: 60.47  (ncpu=10 → ~6.0×)
host_load_15min: 31.08 (~3.1×)
backend: terminal / search_files / sandbox stat 応答不能
  - terminal executed with exit 0 but returned empty output
  - search_files could not stat /Users/junkawasaki (sandbox stat 応答不能)
  - read_file could not open repo tree /Users/junkawasaki/github/.../giemon/...
tests_run: none (not executed)
seeded_repro: none (not executed)
baseline: bench-066/102 (robotics 14/50/0, giemon 46/115/0)
regression: UNMEASURED — assert しない (回帰なしとは言わない)
command: skipped — clojure -M:test は load 60.47 + backend 応答不能で省略
maturity: bench-106 受領どおり回帰なし status 継続。本系未検証。