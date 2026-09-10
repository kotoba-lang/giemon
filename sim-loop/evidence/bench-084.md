# bench-084 (2026-09-07)

- **state**: skipped (load + backend-unresponsive)
- **テスト数 / assertion / failures**: 未測定 (基準値は bench-066: robotics 14/50/0、giemon 46/115/0 のまま)
- **再現 verdict**: 未判定 (seeded 再現の実行不能)
- **回帰の有無**: 判定不能 (回帰検知のための本測定を実行できず)
- **理由**: HOST LOAD 15:49 JST = 16.14 / 25.81 / 30.23 (1/5/15min) — 継続的な load 超過。加えて実行バックエンド (terminal / search / sandbox stat) 応答不能: terminal は empty stdout (exit 0) を返し、search_files は「could not stat ... sandbox」 を返した。重い実験 (clojure -M:test、seeded 再現 2 回走行) は省略。
- **再現コマンド**: —
- **整合性**: 数字を捏造せず、skipped(load) として正直に記録。次回復旧後に本測定を実施予定。