# bench-337 — 2026-10-07T22:10 JST (cron, main-2.local / ncpu 10)

## HOST LOAD gate

load averages: 159.00 141.96 124.25 (uptime 22:10) / ncpu 10 → **1-min ≈ 15.9x, 5-min ≈ 14.2x, 15-min ≈ 12.4x**

gate (約 2x) を大きく超過 → **全経路 skipped (load)**、重い clojure test・seeded 再現は実行しない (unmeasured)。

## HEAD (測定時点)

- robotics: `a1af59c971e37d6c62a313ca52b662c92ba34c25` (bench-332 記録時と不変)
- giemon: `cd05afbbd0a575b04e20dcda5e5a2e8dec01c934` (bench-332 記録時と不変)

giemon in-flight (untracked/M): scripts/edn-datomize.bb, sim-loop/status/_redcheck_tmp.txt, sim-loop/status/maturity.md (M) / evidence 配下 .hermes-tmp.Ytfzs4, bench-328/331/332/336.md (??)。src/test 未変更。

## Verdict

- clojure test (robotics / giemon): **skipped (load) — unmeasured**
- seeded 再現: **skipped (load) — unmeasured**
- 回帰: **判定不能 (本 run は未測定)** — 基準値据え置き (bench-066: robotics 14/50/0, giemon 46/115/0)、runner silent-zero 持続状況の更新は本 run では行えない。

## 再現コマンド

```
uptime; cd github/kotoba-lang/{robotics,giemon} && clojure -M:test
```

(決定的記録・タイムスタンプは run 実行時刻のみ。誇張なし。)
