# bench-071 — skipped (exec-backend unavailable + high load)

- 日次連番: 071 (続 bench-070)
- 状態: **skipped** — 実行バックエンド (terminal) が空出力 (echo PROBE_OK / uptime / sysctl すべて
  空、exit 0) のまま応答不能。search_files も "could not stat <dir> (sandbox starting or removed)"
  で全パス応答不能。read_file は一部ファイル読取可能 (bench-070.md は読めた) が、重い実験 (clojure
  -M:test / seeded 再現) を起動できる状態にない。本イテレーションの測定は不可能。
- テスト実行: 未実行 (backend 応答不能のため robotics / giemon とも clojure -M:test を起動できず。
  結果数値は捏造しない)
- テスト数 / assertion 数 / failures: 測定不能 (記録せず)
- 再現 verdict: 測定不能 (seeded 再現実行は load 高 + backend 応答不能で実行不可)
- 回帰の有無: 評価不能 (回帰検知に必要なテスト実行が backend 障害で不可。捏造しない)
- HOST LOAD: pre-run スクリプト時点で load 72.46 / 75.43 / 79.78 (1min/5min/15min, ncpu=10) —
  高負荷持続 (bench-070 の 76/82/82 からやや低下も高負荷のまま)
- 基準値保持の判定: 前回 bench-066 で確定済みの判定を再評価せず維持 (本イテレーションで新たに
  テスト実行・再現実行できず変更根拠なし)。L0 のまま (未確認)。
- 次回アクション: 復旧後 bench-072 にて本測定 (robotics + giemon の clojure -M:test、
  seeded 再現) を実施。backend が応答するまで重い実験を起動しない。