# bench-100 — giemon sim-loop bench (skipped: load 超過 + backend 制限)

- 日次連番: 100
- 実行日: 2026-09-07 (JST) / cron 実行
- 状態: **skipped (load)** — 全重測定省略

## 実行時環境
- HOST LOAD (uptime): load averages 50.76 / 30.45 / 26.97 (12 users, up 2 days)
  - 15min 26.97 は ncpu=10 の 2 倍超 (2.7×)。1min 50.76 は 5.1×。
  - bench-064〜099 と同系の load 超過条件。重い実験 (test スイート / seeded 再現) は省略対象。
- 実行バックエンド (terminal): 直接 stdout が空 (exit 0) のまま応答せず。
  - `/tmp` redirect workaround のみ成立 (write を /tmp に redirect → read_file で回収)。
  - 実行コード系は cron モードで承認不可 (execute_code BLOCKED)。
  - read_file / write_file は absolute path で成立。git status / uptime / date は /tmp probe 経由で成立。
- このため `kbb -M:test` (robotics / giemon) と seeded 再現実行のいずれも実行せず。

## 判定 (7 軸, ADR-2608052000)
- テスト健全性: **unmeasured** — 実行不能のため回帰 assert せず (honest 維持)
- 再現 verdict: **未実行 (load 超過 + backend 制限)** — 決定的数字を捏造しない
- 回帰の有無: **assert なし** (unmeasured)

## 基準値 (前回確定, bench-066)
- kotoba-lang/robotics: 14 test / 50 assertion / 0 failure
- kotoba-lang/giemon: 46 test / 115 assertion / 0 failure
- 今回は測定不能のため基準値据え置き、回帰 assert しない。

## 再現コマンド (未実行)
- `kbb -M:test` (robotics, giemon)
- seeded 再現: 同一 seed 2 回実行 → 結果一致検査 (sim-loop L1 以降 — 現状 L0 で対象外)

## 検証済みの静的状態 (非測定)
- git HEAD: d0d3cb4 (`git rev-parse --short` で確認、NOTICE: Apache-2.0 等は前回確認)。
- sim-loop 学習ジョブ未実装 (L0) — seeded 再現の実体なし (前回 bench-098 と同じ)。
- untracked: sim-loop/ ほか tmp 系のみを本 profile の記録対象に変更なし。

## 備考
- bench-099 (直前行, 18:09 記録) も同型の load 超過 skip。本 walk はその次 (100)。
- 数字を捏造せず skipped を正直に記録 (基準値 bench-066 据え置き)。
- falsify-033 (H33, FK guard A/B 実測) が成立済み — NEXT として残る未決 falsify なし。
- /tmp redirect workaround 成立を本 walk でも確認 (benchprobe_100.txt 経由)。