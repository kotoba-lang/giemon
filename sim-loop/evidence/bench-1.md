# giemon sim-loop bench — bench-1

## テスト実行 (clojure -M:test)

- robotics: **skipped (load)** — 実行せず。host load avg 51.80 / 43.79 / 48.52 (uptime) のため重いジョブを省略。
- giemon: **skipped (load)** — 同上。
- テスト数 / assertion 数 / failures: **記録なし (未実行)**。前回比: 判定不可 (本記録が最初の bench 記録)。

## seeded 再現実行 (L1 以降)

- **skipped (load)** — 同一 seed での 2 回実行は重いため省略。verdict: **not-run**。

## スクリプト異常

- 設定された収集スクリプト `~/.hermes/profiles/giemon-sim-bench/scripts/giemon_sim_state.sh` が存在しない
  (scripts/ ディレクトリは空)。本 bench は uptime/evidence 確認のみを手動実行して記録した。

## 回帰の有無

- **unknown** — テストを走らせていないため回帰判定は不可。回帰の赤記録なし。

## 再現コマンド

```
uptime
cd orgs/kotoba-lang/robotics && clojure -M:test
cd orgs/kotoba-lang/giemon  && clojure -M:test
```

(本記録では上記 clojure コマンドは未実行。load が下がった次回実行でテスト数 / 再現 verdict を記録すること。)
