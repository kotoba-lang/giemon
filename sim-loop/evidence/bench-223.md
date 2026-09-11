# bench-223

- date-run: 2026-09-09 JST (cron)
- load: 68.87 / 46.84 / 42.55 (1/5/15min), ncpu=10 → 15min ≈ 4.7x ncpu → load 超過
- gate: 15min load ≥ 2x ncpu → heavy test runs skipped (load)

## judgement
- kbb -M:test (robotics / giemon): **unmeasured — skipped (load)**。負荷帯が閾値を大きく超過するため実行を省略。基准値据え置き ( robotics 14/50/0、giemon 46/115/0 )。回帰は assert しない ( honest unmeasured )。
- seeded reproduction: **unmeasured — skipped (load)**。sim-loop L0 のため not-applicable が通常、本回は学習ジョブ再現実行自体も負荷超過で省略。
- regression: **none asserted** (unmeasured run; 前回 bench-222 の実測結果に基づく回帰指摘なし)。
- falsify status: falsify-034〜037 は refuted 済み・残存なし。コード変更なし。

## 再現コマンド
```
uptime && sysctl -n hw.ncpu   # gate: 15min >= 2x ncpu → skip
# (skip のため本回は test 実行コマンド不発)
```

## 決定性
- 本記録は決定的・タイムスタンプなし ( JST 日付は cron 由来の run 識別のみ )。
