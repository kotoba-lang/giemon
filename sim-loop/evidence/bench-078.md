# Bench-078 — giemon sim-loop パフォーマンス記録

- 種別: bench (定例)
- 日次連番: 078
- HOST LOAD (uptime, pre-run 時点 21:29): 1min 29.93 / 5min 32.98 / 15min 32.63
- 実行バックエンド状態: terminal が空出力 (echo/pwd/date/uptime すべて exit 0 で空)、
  search_files が "could not stat .../giemon" — bench-069〜077 と同型の応答不能条件。
  load 1min 29.93 / ncpu 10 想定。read_file (実在ファイル) のみ成立。

## テストスイート (kotoba-lang/robotics + kotoba-lang/giemon: clojure -M:test)

- 結果: **skipped (load + backend unresponsive)**
- テスト数 / assertion 数 / failures: 計測せず（単一値・検証なしに捏造しない）

## Seeded 再現 (sim-loop L1 以降 / 同一 seed 2 回）

- 結果: **skipped (load + backend unresponsive)**
- 再現 verdict: 判定せず（決定的 REPL 数字の捏造禁止）

## 回帰検知

- 有無: 判定なし (skipped)。基準値 (robotics 14/50/0、giemon 46/115/0) は bench-066 確定値のまま。

## H28 falsify-026

- 結果: **未記録 (gating 遵守)**。falsify-026 は backend 応答不能のため本イテレーションで
  記録しない。gating 規則「falsify-026 記録まで next を進めない」を遵守、NEXT=H28 のまま据え置き。

## 備考

- 決定的数字の捏造を避け、skipped を正直に記録。
- bench-077 で確立した静的な FK `(or (first angles) 0.0)` ゼロ充填 / `(empty? chain)` 終端 /
  `end-effector` の `last`-only は H26/H27 で済んでおり、H28 の void 全列挙は既存 falsify
  25 件からの集計が主体 (backend 回復後の本測定で falsify-026 を記録)。
- backend 復旧後の本測定 (robotics + giemon の clojure -M:test、seeded 再現) は bench-079 で実施予定。