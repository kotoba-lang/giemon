# bench-085 — skipped (load / terminal 応答不能)

## 実行日時条件
- pre-run script HOST LOAD: 11:06, 2 days up, 8 users
  load averages: 75.45 64.39 54.10 (ncpu=10)
- 実行バックエンド: terminal が空出力 (echo PROBE_OK; uptime → 空、exit 0) のまま応答不能
- search_files: "could not stat sim-loop/evidence (sandbox may still be starting or was removed)"
- read_file: 成立 (maturity.md 344 行 / falsify-028.md 91 行を盤上読取)

## 判定
- HOST LOAD が極めて高い (75.45, ncpu 10 の 7.5x)。方針により重い実験を省略する。
- 実行バックエンド (terminal) が空出力 exit 0 のまま応答不能 (bench-069〜084 と同条件の持続)。
  → test スイート (clojure -M:test, kotoba-lang/robotics + kotoba-lang/giemon) および
    seeded 再現 (sim-loop L1以降) をすべて skipped とする。正直に「skipped (load)」で記録。

## 本イテレーションの falsify 対象
- maturity.md NEXT (行 109–133) を盤上読取で確認: falsify-028 (H30) は既に refuted で記録済み
  (evidence/falsify-028.md 存在・91 行・verdict refuted)、NEXT は H30 →「次候補
  (numeric+shape guard 導入判断・bench-085 本測定)」へ前進済み。
- すなわち現 NEXT は (a) FK/end-effector の NaN/±∞ guard + 長さ guard の**導入判断** (核心側の
  実装決定・本 bot の役割外) と (b) backend 復旧後の test + seeded 本測定 (bench-085) の 2 件。
  **未反証の falsify 仮説は存在しない** (H1〜H30 全て settled)。したがって本 bot が静的読取で
  潰せる新しい仮説は無い — 新規仮説を捏造せず、skipped bench として記録する。

## 結果
- テスト数: N/A (skipped)
- assertion 数: N/A (skipped)
- failures: N/A (skipped)
- seeded 再現 verdict: N/A (skipped)
- 回帰の有無: 判定不能 (実行不能のため)。基準値 (robotics 14/50/0、giemon 46/115/0) は
  bench-066 確定値のまま変更なし。

## 再現コマンド (次回 load 低下時に実施すべき)
- orgs/kotoba-lang/robotics: clojure -M:test
- orgs/kotoba-lang/giemon:    clojure -M:test
- seeded 再現: sim-loop 学習ジョブ (L1以降) を同一 seed で 2 回実行し一致検査

## 備考
- 前回 bench-084 まで同条件 (terminal 空出力 / sandbox stat 不能) で連続 skipped。
- falsify / 静的読取 (負荷非依存) による新規反証は無い (H1〜H30 全 settled、NEXT は
  核心側の guard 導入判断 + bench-085 本測定のみ)。
- コード修正なし。決定的・タイムスタンプなしで記載。