# bench-279 — skipped (load 超過)

## 判定: unmeasured (skipped — HOST LOAD)

- 15-min load average: 20.08 (1-min 25.84, 5-min 16.16, 実測 uptime 25.84/20.08/16.16)。hw.ncpu = 10。
- gate: 15-min ≥ 2× ncpu (= 20) → 20.08 ≥ 20 で超過 (しかも 1-min が 25.84 へ上昇中)。
- clojure -M:test 両 suite / seeded 再現は省略 → unmeasured (honest)。
- 基準値据え置き: robotics 23/558/0・giemon 46/115/0。回帰 assert せず。

## 状態

- HEAD: 本走で未再読 — bench-275/276/277 記録 (robotics ad99366 / giemon 41ac173) を据え置き (変移は否定も肯定もしない)。
- silent-zero 持続 (clojure runner 0/0/0 RC=0 / kbb RC=1 dep 未解決) は本走未測定。
  bench-244〜276 の実測記録に変更なし。bench-271〜274/277/278 に続く load skip。
- NEXT の優先度変更なし: test-runner 修復 (cljk rename 後 silent-zero 解消) が全 bench/falsify の前提。
- falsify 状況変更なし (falsify-076 (H77) refuted が最新、FK guard repair 33 連続 refuted 未着手)。

## 再現コマンド

```
uptime   # 15-min load ≥ 2× sysctl -n hw.ncpu を確認 (本走: 25.84/20.08/16.16, ncpu=10)
```

## 回帰: 無判定 (unmeasured)

- コード変更: なし。
