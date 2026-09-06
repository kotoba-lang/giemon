# bench-064

- 測定日: 2026-09-06 JST
- HOST LOAD (uptime 記載): 1min 188.36 / 5min 157.31 / 15min 95.88 (avg, users 13)
- 実行コマンド: `clojure -M:test` (robotics, giemon) → **skipped (load)**。
  システム負荷が極端 (1min 188。`uptime`/`ls` でさえ応答が timeout/空出力に
  なる状況) のため、重量実験 (2 リポジトリのテストスイート + seeded 再現) は省略。

## テスト数字
- robotics: **未再実行 (skipped (load))** — 前回 bench-063 で 14 tests / 50 assertions / 0 failures
- giemon:   **未再実行 (skipped (load))** — 前回 bench-063 で 46 tests / 115 assertions / 0 failures

## 再現 verdict (seeded / sim-loop 学習ジョブ)
- **skipped (load)**。sim-loop 学習ジョブ (L1 以降) は従来どおり giemon リポジトリ内に
  未実装 (bench-062〜063 で機械確認済み)。既存決定関数の軽量 seeded 再現 surrogate も
  今回は負荷超過につき実行せず。

## 回帰の有無
- **本測定なし (skipped (load))**。回帰なしとは断定しない。↓
- bench-063 との比較: テスト数字の再確認が行えてないため「回帰なし」判定は保留。
  前回確定値 (robotics 14/50/0、giemon 46/115/0) を基準として次回再検証する。

## 備考
- 負荷 188 は bench 開始条件の許容域 (既定 60 秒超でも応答なし) を超えたため、
  決定的数字を捏造せず honesty-first で skipped 記録にした。
- 再実行条件: load 1min < 60 程度に落ちた後に bench-065 で通常実行する。