# bench-097 — giemon sim-loop bench (skipped: load)

- 日次連番: 097
- 実行日: 2026-09-07 (JST)
- 状態: **skipped (load)** — 全測定省略

## 実行時環境
- HOST LOAD (uptime): load averages 45.87 / 27.91 / 32.91 (12 users, up 2 days)
  - 1min 45.87 は ncpu=10 の 4 倍超。bench-064〜096 と同じ load 超過条件。
- 実行バックエンド (terminal / search / sandbox stat): 応答不能
  - `terminal` は直接 stdout が空 (exit 0) のまま応答せず。
  - `search_files` は `could not stat` (sandbox 未起動/除去)。
  - stdout は redirect (`> /tmp/...`) + read_file 経由でのみ成立。
  - read_file は absolute path で成立 (bench-095/096 と同型)。
- このため `kbb -M:test` (robotics / giemon) と seeded 再現実行のいずれも実行不可。

## 判定 (7 軸, ADR-2608052000)
- テスト健全性: **unmeasured** — 実行不能のため回帰 assert せず (honest 維持)
- 再現 verdict: **未実行 (backend 応答不能 + load 超過)** — 決定的数字を捏造しない
- 回帰の有無: **assert なし** (unmeasured)

## 基準値 (前回確定, bench-066)
- kotoba-lang/robotics: 14 test / 50 assertion / 0 failure
- kotoba-lang/giemon: 46 test / 115 assertion / 0 failure
- 今回は測定不能のため基準値据え置き、回帰 assert しない。

## 再現コマンド (未実行)
- `kbb -M:test` (robotics, giemon)
- seeded 再現: 同一 seed 2 回実行 → 結果一致検査 (sim-loop L1 以降、現状 L0 未実装で対象外)

## 検証済みの静的状態 (非測定)
- git HEAD: d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe (short d0d3cb4 — 前回 bench-096 と同一)
- git diff --stat: 空。tracked 変更なし (untracked: sim-loop/, tmp 系のみ)
- sim-loop 学習ジョブ未実装 (L0) — seeded 再現の実体なし。

## 備考
- bench-064〜096 と同型の load 超過 + backend 応答不能 skip。継続 30 件超。
- falsify 系は本 bench 対象外 (test スイート / seeded 再現のみ)。
- 数字を捏造せず skipped を正直に記録。
