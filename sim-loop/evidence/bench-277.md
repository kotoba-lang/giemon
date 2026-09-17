# bench-277 — load 超過 skip

## 判定: unmeasured (skipped — HOST LOAD)

- 15-min load average: 60.15 (1-min 53.08, 実行中観測 81.35/53.34/31.88 → 64.86/63.64/41.45 → 51.75/62.74/45.04 → 53.08/60.15/46.76)。hw.ncpu = 10。
- gate: 15-min ≥ ~2× ncpu (= 20) → 60.15 は gate 超 (~6.0× ncpu)。
- 重い実験 (clojure -M:test 両 suite, seeded 再現, kbb 暫定経路) を省略。test-runner silent-zero 問題 (cljk rename 起, falsify-069 根因確定) への触れ込み無し。
- 基準値は据え置き: robotics 23/558/0, giemon 46/115/0。回帰 assert はしない (honest)。

## 状態

- giemon HEAD: 41ac173 (前回 bench-276 と同一, 変化なし)。
- robotics HEAD: ad99366 (前回 bench-276 と同一, 変化なし)。
- NEXT (status/maturity.md より) 変更なし: test-runner 修復 (clojure / kbb 両 runner 緑化, nbb.edn deps floor 接続) が最優先。falsify-034 起 FK guard repair 未着手・runner 修復後の再検証待ち。

## 再現コマンド

```
uptime   # 15-min load ≥ 2× sysctl -n hw.ncpu を確認
```

## 回帰: 無判定 (unmeasured)

- コード変更: なし。
