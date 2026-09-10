# bench-095 — SKIPPED (load 超過)

## verdict
- test スイート (robotics / giemon `clojure -M:test`): **skipped (load)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load)** — sim-loop 学習ジョブ未実装 (L0) のため対象外
- 回帰: **判定不能** (測定できず — unmeasured のため assert しない, honesty-first)

## 理由
- HOST LOAD (本 iteration 実測, redirect+read_file で読取): 25.00 / 25.75 / 33.29
  (1min/5min/15min, ncpu=10) — 実行バックエンド応答不能閾値を超過し継続上昇中。
- 実行バックエンド不安定: fresh probe (`uptime` / `date` / `pwd` / `ls`) がすべて
  空出力 (exit 0) のまま応答せず。stdout は redirect+read_file 経由でのみ成立。
  search_files / read_file は relative path で `could not stat` (sandbox 未起動/除去)
  を返し、absolute path のみ成立。execute_code は cron モード blocked。
- → bench-064〜094 と同型の load 超過 + バックエンド不安定条件。

## 測定手段なし
- 重い実験 (clojure test スイート / seeded 再現) は load 超過のため実行せず skipped 記録。
- 決定的 (REPL 実行) 数字は捏造せず、基準値 bench-066 確定を据え置き。
- git: HEAD d0d3cb4 (前回 bench-094 と同一)、diff 空 (untracked のみ)。コード変更なし。

## 再現手順
1. uptime で load 1min が ncpu=10 を超える / terminal が空出力 exit 0 を返す
2. 重い実験 (test スイート・seeded 再現) を実行せず skipped と記録
3. 基準値は bench-066 (robotics 14/50/0, giemon 46/115/0) を据え置き、回帰 assert しない
