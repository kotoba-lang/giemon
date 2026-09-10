# bench-096 — giemon sim-loop bench (skipped: load)

- 日次連番: 096
- 実行日: 2026-09-07 (JST)
- 状態: **skipped (load)** — 全測定省略

## 実行時環境
- HOST LOAD (uptime): load averages 39.29 / 67.42 / 64.49 (12 users, up 2 days)
- 実行バックエンド (terminal / search / sandbox stat): 応答不能
  - `terminal` が空出力 (exit 0) を返し、`search_files` が evidence ディレクトリを stat 不能
  - read_file も status/maturity.md を解決不能
- このため `clojure -M:test` (robotics / giemon) と seeded 再現実行のいずれも実行不可

## 判定 (7 軸, ADR-2608052000)
- テスト健全性: **unmeasured** — 実行不能のため回帰 assert せず (honest 維持)
- 再現 verdict: **未実行 (backend 応答不能)** — 決定的数字を捏造しない
- 回帰の有無: **assert なし** (unmeasured)

## 基準値 (前回確定, bench-066)
- kotoba-lang/robotics: 14 test / 50 assertion / 0 failure
- kotoba-lang/giemon: 46 test / 115 assertion / 0 failure

## 再現コマンド (未実行)
- `clojure -M:test` (robotics, giemon)
- seeded 再現: 同一 seed 2 回実行 → 結果一致検査

## 備考
- bench-064〜095 と同型の load 超過 + backend 応答不能 skip。
- falsify 系は本 bench 対象外 (test スイート / seeded 再現のみ)。
- 数字を捏造せず skipped を正直に記録。