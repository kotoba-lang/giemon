# bench-275 — test-runner silent-zero 持続 (実測)

## 判定: measured — silent-zero 継続 (0/0/0 RC=0 両 suite)

- 実測: `clojure -M:test` 両 suite とも `Ran 0 tests containing 0 assertions. 0 failures, 0 errors.`、RC=0。
- robotics: 0/0/0 RC=0, HEAD ad99366 (maturity NEXT の基準 HEAD と一致)。
- giemon: 0/0/0 RC=0, HEAD 41ac173。
- cljk rename 起 silent-zero は bench-244〜270 の 27 連続に続き **28 連続**。基準値との比較不能 — 回帰 assert はしない (基準値据え置き: robotics 23/558/0, giemon 46/115/0)。
- "Testing user" namespace 表示は falsify-069 (JVM require が .cljk をロード不能) と整合。runner 修復未着手。

## 状態

- HOST LOAD: 15-min 16.10 (1-min 12.61)。hw.ncpu = 10 → gate (≈20) 未満 (~1.6×) のため
  本 run は skip せず実測完走。bench-274 (15-min 30.35, ~3.0×) から負荷は回復。
- seeded 再現: not-applicable (sim-loop は L0, 学習ジョブ無し)。
- NEXT 変更なし: test-runner 修復 (.cljk → loader 登録 or 拡張子復帰) が最優先。
  暫定測定経路 `kbb --backend sci --classpath src:test` 21/52/0 は本 run では未実行
  (clojure runner 結果のみ記録、kbb 第2経路は bench-270 で RC=1 hard-fail のまま)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && clojure -M:test   # → 0/0/0 RC=0
cd orgs/kotoba-lang/giemon   && clojure -M:test   # → 0/0/0 RC=0
```

## 回帰: 無判定 (runner 壊死により測定不能 — silent-zero 持続 28 連続を記録)

- falsify 状態: falsify-034 起 FK guard repair 未着手、falsify-069 (runner 根因) 確定済み。
  本 run で変化なし。
- コード変更: なし。
