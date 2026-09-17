# bench-274 — load 超過 skip

## 判定: unmeasured (skipped — HOST LOAD)

- 15-min load average: 30.35 (1-min 38.55)。hw.ncpu = 10。
- gate: 15-min ≥ ~2× ncpu (= 20) → 30.35 は gate 超 (~3.0× ncpu)。
- 重い実験 (clojure -M:test 両 suite, seeded 再現) を省略。test-runner silent-zero
  問題 (cljk rename 起, bench-244〜270 で 27 連続 0/0/0 RC=0) への触れ込み無し。
- 基準値は据え置き: robotics 23/558/0, giemon 46/115/0。回帰 assert はしない。

## 状態

- giemon HEAD: 41ac173 (前回 bench-273 と同一, 変化なし)。
- robotics: 本 checkout は giemon 単体配置のため path 無し (superproject worktree では無い)。
  robotics HEAD は未取得 (skip 判定に影響せず, load 超過が単独事由)。
- NEXT (status/maturity.md より) 変更なし: test-runner 修復が最優先。

## 再現コマンド

```
uptime   # 15-min load ≥ 2× sysctl -n hw.ncpu を確認
```

## 回帰: 無判定 (unmeasured)

- falsify 状態: falsify-034 起 FK guard repair 未着手 (31 連続 refuted), falsify-069
  で clojure runner 根因確定済み — いずれも本 run で変化なし。
- コード変更: なし。
