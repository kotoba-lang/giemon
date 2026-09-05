# giemon sim-loop bench — bench-3

日時: 2026-09-03T10:53:40+0900 (JST)

## HOST LOAD

- load averages: **36.36 31.70 34.41** (uptime, 10 cores)。1分負荷はコア数の約 3.6 倍で
  高負荷。低下傾向は見られない (bench-2 時点の 1min 26.76 から再上昇)。

## テスト実行 (clojure -M:test)

- robotics: **skipped (load)** — load avg がコア数の 2 倍超のため重いジョブを省略。
- giemon: **skipped (load)** — 同上。
- テスト数 / assertion 数 / failures: **記録なし (未実行)**。前回比: 判定不可
  (bench-1 / bench-2 も未実行のため 3 連続で回帰判定不可)。

## seeded 再現実行 (L1 以降)

- **skipped (load)** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0) であり、
  負荷も高いため実行せず。verdict: **not-run**。

## 回帰の有無

- **unknown** — テストを走らせていないため回帰判定は不可。回帰の赤記録なし。
- 赤の現状: falsify-1 (refuted) は既存のまま変化なし (OPEN 赤)。新規赤なし。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
```

(本記録では上記 clojure コマンドは未実行。load がコア数以下に下がった次回実行で
テスト数 / 再現 verdict を記録すること。3 連続 skip のため、次回は負荷が許せば
必ずテストを実行して 4 連続 skip を避けること。)
