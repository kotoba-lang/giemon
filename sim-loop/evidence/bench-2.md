# giemon sim-loop bench — bench-2

日時: 2026-09-03T10:36:21+0900 (JST)

## HOST LOAD

- load averages: **26.76 33.35 38.87** (uptime, 10 cores)。1分負荷はコア数の約 2.7 倍で
  高負荷。ただし低下傾向 (15min 38.87 → 1min 26.76)。

## テスト実行 (clojure -M:test)

- robotics: **skipped (load)** — 実行せず。host load avg がコア数の 2 倍超のため重いジョブを省略。
- giemon: **skipped (load)** — 同上。
- テスト数 / assertion 数 / failures: **記録なし (未実行)**。前回比: 判定不可
  (bench-1 も未実行のため 2 連続で回帰判定不可)。

## seeded 再現実行 (L1 以降)

- **skipped (load)** — seeded 学習ジョブは未整備 (maturity: 再現性 score 0) であり、
  負荷も高いため実行せず。verdict: **not-run**。

## スクリプト異常

- bench-1 で不在だった収集スクリプト `~/.hermes/profiles/giemon-sim-bench/scripts/giemon_sim_state.sh`
  は今回存在を確認 (内容: maturity/evidence/uptime/git status の軽量収集のみ)。本 bench も
  この軽量収集 + uptime + evidence 一覧のみを手動実行して記録した。

## 回帰の有無

- **unknown** — テストを走らせていないため回帰判定は不可。回帰の赤記録なし。
- 赤の現状: falsify-1 (refuted) は既存のまま変化なし (OPEN 赤)。新規赤なし。

## 再現コマンド

```
uptime
~/.hermes/profiles/giemon-sim-bench/scripts/giemon_sim_state.sh
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
```

(本記録では上記 clojure コマンドは未実行。load がコア数以下に下がった次回実行で
テスト数 / 再現 verdict を記録すること。)
