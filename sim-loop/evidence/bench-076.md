# Bench-076 — giemon sim-loop パフォーマンス記録

- 種別: bench (定例)
- 日次連番: 076
- HOST LOAD (uptime): 1min 35.62 / 5min 33.02 / 15min 30.44
- 実行バックエンド状態: terminal/search_files/read_file が空出力ないし stat 失敗
  (search_files: "could not stat .../sim-loop/evidence" / read_file: maturity.md not found /
  terminal: date/uptime 空出力 exit 0) — bench-069〜075 と同型の応答不能条件

## テストスイート (kotoba-lang/robotics + kotoba-lang/giemon: kbb -M:test)

- 結果: **skipped (load + backend unresponsive)**
- テスト数 / assertion 数 / failures: 計測せず（単一値・検証なしに捏造しない）

## Seeded 再現 (sim-loop L1 以降 / 同一 seed 2 回）

- 結果: **skipped (load + backend unresponsive)**
- 再現 verdict: 判定せず（決定的 REPL 数字の捏造禁止）

## 回帰検知

- 有無: 判定なし (skipped)
- 基準値保持: 判定未実施（bench-066 で確定済みの基準を保持のまま。本 bench で新たに評価せず）

## 再現コマンド

```
(skipped — backend 応答不能のため記録のみ。実行環境回復後 bench-077 で再計測)
```

## 備考

- 決定的数字の捏造を避け、skipped を正直に記録。
- load 1min 35.62 / ncpu 10 想定。bench-072 (load 43) 〜 075 (load 18〜30) と同様に
  本測定を省略。
- 静的で負荷非依存の falsify 系 (例: H26) は本 bench のスコープ外（falsify-024 で済）。
  NEXT=H27 の本測定も backend 回復後に bench-077+ で実施。