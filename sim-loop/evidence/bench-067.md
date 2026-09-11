# bench-067

- 測定日: 2026-09-06 JST
- HOST LOAD (uptime 記載): 1min 74.29→92.70→99.45 / 5min 77.85→81.80→83.38 / 15min 79.29→80.67→81.23 (avg, users 14)。
  5 秒間隔の再計測で 92.70 → 99.45 と高負荷が持続・上昇 (一過性のスパイクではない)。
- 実行コマンド: `kbb -M:test` (robotics, giemon) → **skipped (load)**。
  bench-064 で明記した再実行条件 (load 1min < 60 程度) を満たしていないため、
  2 リポジトリのテストスイート + seeded 再現 (重量実験) は省略。

## テスト数字
- robotics: **未再実行 (skipped (load))** — 前回 bench-066 で 14 tests / 50 assertions / 0 failures
- giemon:   **未再実行 (skipped (load))** — 前回 bench-066 で 46 tests / 115 assertions / 0 failures

## 再現 verdict (seeded / sim-loop 学習ジョブ)
- **skipped (load)**。sim-loop 学習ジョブ (L1 以降) は giemon リポジトリ内に未実装
  (git head d0d3cb4 = bench-062〜066 と同一、committed diff 空、機械確認)。
  既存決定関数の軽量 seeded 再現 surrogate も今回は負荷超過につき実行せず。

## 回帰の有無
- **本測定なし (skipped (load))**。回帰なしとは断定しない。
- bench-066 との比較: テスト数字の再確認が行えてないため「回帰なし」判定は保留。
  前回確定値 (robotics 14/50/0、giemon 46/115/0) を基準として次回再検証する。

## 備考
- 負荷 (1min 74〜99、上昇中) は bench 実行の許容域 (bench-064 で設定した load 1min < 60
  の再実行条件) を超えたため、決定的数字を捏造せず honesty-first で skipped 記録に
  した。負荷が持続・上昇 (5 秒間隔でも 92.70 → 99.45) であることを 5 秒再測定で確認。
- git head は d0d3cb4 のまま (bench-062〜066 と同一) — コード修正なし維持を確認。
- 再実行条件: load 1min < 60 程度に落ちた後に bench-068 で通常実行する。